# Phase 4C 证据索引

**版本：** v1.0  
**创建日期：** 2026-06-01  
**目的：** 让验收不依赖聊天记录，所有证据可快速定位

---

## 测试命令

### 后端测试

```bash
# 运行所有后端测试
docker compose exec backend python manage.py test --keepdb

# 运行特定模块测试
docker compose exec backend python manage.py test apps.applications.tests --keepdb
docker compose exec backend python manage.py test apps.approvals.tests --keepdb
docker compose exec backend python manage.py test apps.attachments.tests --keepdb
docker compose exec backend python manage.py test apps.users.tests --keepdb

# 运行CSV导入测试
docker compose exec backend python manage.py test apps.users.tests.test_import_csv --keepdb
```

### Smoke测试

```bash
# 完整端到端测试（15步）
./tests/smoke_test.sh

# P0修复测试
./tests/test_p0_fixes.sh
```

---

## 测试通过统计

| 测试类别 | 通过数量 | 文件路径 |
|---------|---------|----------|
| 申请流程测试 | 4个 | `backend/apps/applications/tests/test_application_flow.py` |
| 申请约束测试 | 3个 | `backend/apps/applications/tests/test_constraints.py` |
| 申请错误测试 | 5个 | `backend/apps/applications/tests/test_error_cases.py` |
| 序列化器验证测试 | 7个 | `backend/apps/applications/tests/test_serializer_validation.py` |
| 详情权限测试 | 3个 | `backend/apps/applications/tests/test_detail_permissions.py` |
| 列表权限测试 | 1个 | `backend/apps/applications/tests/test_list_permissions.py` |
| 审批权限测试 | 5个 | `backend/apps/approvals/tests/test_permissions.py` |
| 审批驳回测试 | 2个 | `backend/apps/approvals/tests/test_rejection_flow.py` |
| 审批状态机测试 | 4个 | `backend/apps/approvals/tests/test_state_machine.py` |
| 附件上传测试 | 5个 | `backend/apps/attachments/tests/test_upload.py` |
| 附件列表测试 | 6个 | `backend/apps/attachments/tests/test_list.py` |
| 附件下载测试 | 4个 | `backend/apps/attachments/tests/test_download.py` |
| 附件删除测试 | 4个 | `backend/apps/attachments/tests/test_delete.py` |
| CSV导入测试 | 9个 | `backend/apps/users/tests/test_import_csv.py` |
| **总计** | **62个** | - |

---

## Smoke测试脚本

**路径：** `tests/smoke_test.sh`

**覆盖场景：**
- H1: Happy path（学生→辅导员→学工部完整审批流程）
- 附件生命周期（上传→列表→下载→删除）
- N2: 跨辅导员审批负向测试（403 FORBIDDEN）

**步骤数：** 15步

---

## CSV导入

### 导入命令

**路径：** `backend/apps/users/management/commands/import_csv.py`

**用法：**
```bash
# Dry-run模式（预览）
docker compose exec backend python manage.py import_csv \
  --students /path/to/students.csv --dry-run

# 实际导入
docker compose exec backend python manage.py import_csv \
  --counselors /path/to/counselors.csv
docker compose exec backend python manage.py import_csv \
  --mappings /path/to/mappings.csv
docker compose exec backend python manage.py import_csv \
  --students /path/to/students.csv
```

### CSV模板

**路径：** `backend/data/templates/`

| 模板文件 | 必填字段 |
|---------|---------|
| `counselors_template.csv` | employee_id, name |
| `class_mappings_template.csv` | class_id, counselor_employee_id |
| `students_template.csv` | student_id, name, class_id, is_graduating, graduation_year |

---

## Docker部署

### 部署文档

**路径：** `DEPLOYMENT.md`

**快速启动（6步）：**
1. 环境配置：`cp .env.example .env.docker`
2. 启动服务：`docker compose up -d`
3. 数据库迁移：`docker compose exec backend python manage.py migrate`
4. 加载数据：`docker compose exec backend python manage.py seed_data`
5. 验证安装：`./tests/smoke_test.sh`
6. 访问应用：http://localhost:8001

### 环境变量模板

**路径：** `.env.example`

**关键变量：**
- `SECRET_KEY`：Django密钥
- `DB_PASSWORD`：数据库密码
- `JWT_SECRET_KEY`：JWT密钥
- `ALLOWED_HOSTS`：允许的域名
- `MEDIA_ROOT`：媒体文件根目录
- `MEDIA_URL`：媒体文件URL前缀

### Docker配置

**路径：** `docker-compose.yml`

**关键配置：**
- PostgreSQL容器（端口5432）
- Backend容器（端口8001）
- postgres_data volume（数据库持久化）
- media_data volume（附件持久化）

---

## API契约文档

### 契约版本

| 版本 | 路径 | 状态 |
|------|------|------|
| v0.1 | `docs/contracts/contract-v0.1.md` | 已冻结 |
| v0.2 | `docs/api/contract-v0.2.md` | 已完成 |
| v0.3 | `docs/api/contract-v0.3.md` | Final（附件功能） |

### v0.3契约内容

**路径：** `docs/api/contract-v0.3.md`

**包含：**
- 7个API端点（用户/申请/审批/附件）
- 4个状态枚举
- 状态机转换规则
- 权限矩阵（3角色×7操作）
- 6个错误码定义
- 请求/响应样例

---

## 关键配置文件

### Backend配置

| 文件 | 用途 |
|------|------|
| `backend/config/settings/base.py` | 基础配置 |
| `backend/config/settings/dev.py` | 开发配置 |
| `backend/config/settings/prod.py` | 生产配置 |
| `backend/requirements/base.txt` | 基础依赖 |
| `backend/requirements/dev.txt` | 开发依赖 |
| `backend/requirements/prod.txt` | 生产依赖 |

### Frontend配置

| 文件 | 用途 |
|------|------|
| `miniprogram/app.json` | 小程序配置（页面注册） |
| `miniprogram/project.config.json` | WeChat DevTools配置 |
| `miniprogram/types/api.ts` | TypeScript类型定义 |
| `miniprogram/services/api.ts` | API客户端 |

---

## 数据对接文档

**路径：** `docs/数据对接说明文档.md`

**内容：**
- 宿舍管理系统对接规范
- API接口定义
- CSV数据文件格式
- 字段映射说明

---

## 系统设计文档

**路径：** `docs/design/2026-05-27-system-design.md`

**内容：**
- 系统架构设计
- 数据库设计（7个核心表）
- API设计（19个端点）
- 认证授权设计
- 审批流程设计
- 部署架构设计

---

## Claude-Codex讨论记录

### Phase 4C讨论

**路径：** `docs/discussions/phase4c-next-steps/`

**关键文档：**
- `19-claude-next-phase-strategy-request.md`：Claude策略提案
- `20-codex-next-phase-strategy-response.md`：Codex审查（修正版E策略）
- `21-claude-consensus-narrowed-strategy.md`：共识文档（两条主线）
- `22-claude-post-execution-next-steps.md`：执行后下一步分析
- `23-codex-post-execution-next-steps-response.md`：Codex审查（证据闭环）
- `24-claude-consensus-evidence-closure.md`：证据闭环共识

### Week 3讨论

**路径：** `docs/discussions/week3-day1-review-2026-05-30/`

**关键文档：**
- `01-codex-review.md`：Codex识别7个P1问题
- `07-claude-consensus-narrowed-strategy.md`：Day 2执行计划共识

---

## Git提交记录

### 最近提交

```bash
# 查看最近5次提交
git log --oneline -5

# 查看Track 1和Track 2提交
git log --oneline --grep="CSV导入\|Docker"
```

### 关键提交

- Track 1: CSV导入v1硬化（字段对齐 + dry-run + 事务 + 校验 + 摘要 + 9测试）
- Track 2: Docker/media/smoke硬化（media volume + .env.example + DEPLOYMENT.md + 附件smoke测试）
- 文档更新：Track 1和Track 2完成状态

---

## 验收清单

**路径：** `docs/acceptance/phase4c-acceptance-checklist.md`

**内容：**
- Backend API功能验收（4个模块）
- CSV导入v1验收
- Docker/media持久化验收
- Smoke test验收
- Miniprogram静态状态
- WeChat DevTools待验证项
- 外部依赖阻塞项

---

**索引版本：** v1.0  
**最后更新：** 2026-06-01  
**维护说明：** 本索引应在每次重大更新后同步更新
