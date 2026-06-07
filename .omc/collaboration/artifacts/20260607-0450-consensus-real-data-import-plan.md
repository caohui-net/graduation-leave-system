# 真实数据导入执行方案 - 最终共识

**日期：** 2026-06-07  
**状态：** Codex审查通过，待执行  
**讨论ID：** DISCUSS-真实数据导入准备-1780807144

---

## 共识决策

采用**门禁方案**：先验源数据 → 备份 → 安全清理 → 真实导入 → 闭环验证

---

## 数据源修正

**总计：6041条记录**
- 学生：5946条（file5_students_merged_v2.csv）
- 宿管员：72条（dorm_managers_processed.csv）
- 辅导员：20条（counselors_processed.csv）
- 管理员：3条（additional_staff.csv，2学工管理员 + 1兜底宿管92008149）

---

## 4个阻塞问题（必须先解决）

### P0-1: 确认目标数据库连接
- **问题**：必须确认连接的是目标数据库，而非空开发库或旧测试库
- **验证**：检查数据库名称、用户数、连接信息

### P0-2: 备份当前数据库
- **问题**：必须先备份并检查受PROTECT约束的数据
- **命令**：`python manage.py dumpdata > reports/pre_real_import_$(date +%Y%m%d%H%M%S).json`

### P0-3: 测试数据差异识别
- **问题**：需使用CSV allowlist差异识别测试账号
- **测试账号**：M001/M002/M003, T001/T002, D001, 2020001-2020010
- **策略**：删除确认测试账号及其依赖数据（applications, approvals）

### P0-4: 验收口径修正
- **问题**：导入验收口径从6040修正为6041
- **路由覆盖**：
  - 辅导员：100%（5946/5946）
  - 宿管直接：98.05%（5830/5946）
  - Fallback：116人通过92008149兜底宿管
  - 实际可路由：100%（5830直接 + 116 fallback）

---

## 执行步骤（8步）

### Step 1: 数据库连接确认（2分钟）
```bash
cd backend
docker compose exec -T backend python manage.py shell <<'EOF'
from django.conf import settings
print(f"数据库: {settings.DATABASES['default']['NAME']}")
print(f"主机: {settings.DATABASES['default']['HOST']}")
from apps.users.models import User
print(f"当前用户数: {User.objects.count()}")
EOF
```

### Step 2: 数据备份（5分钟）
```bash
mkdir -p reports
docker compose exec -T backend python manage.py dumpdata > reports/pre_real_import_$(date +%Y%m%d%H%M%S).json
ls -lh reports/pre_real_import_*.json
```

### Step 3: 源CSV验证（5分钟）
```bash
# 验证CSV行数
wc -l backend/data/file5_students_merged_v2.csv
wc -l backend/data/dorm_managers_processed.csv
wc -l backend/data/counselors_processed.csv
wc -l backend/data/additional_staff.csv

# Dry-run导入验证
docker compose exec -T backend python manage.py import_staff --file data/dorm_managers_processed.csv --dry-run
docker compose exec -T backend python manage.py import_staff --file data/counselors_processed.csv --dry-run
docker compose exec -T backend python manage.py import_staff --file data/additional_staff.csv --dry-run
docker compose exec -T backend python manage.py import_students --file data/file5_students_merged_v2.csv --mode clean --dry-run
```

### Step 4: 测试数据清理（10分钟）
```bash
# 识别测试账号
docker compose exec -T backend python manage.py shell <<'EOF'
from apps.users.models import User
from apps.applications.models import Application
from apps.approvals.models import Approval

test_ids = ['2020001','2020002','2020003','2020004','2020005','2020006','2020007','2020008','2020009','2020010','M001','M002','M003','T001','T002','D001']
test_users = User.objects.filter(user_id__in=test_ids)
print(f"测试用户: {test_users.count()}")

# 检查依赖数据
apps = Application.objects.filter(student__user_id__in=test_ids)
print(f"测试申请: {apps.count()}")
approvals = Approval.objects.filter(approver__user_id__in=test_ids)
print(f"测试审批: {approvals.count()}")
EOF

# 删除测试数据（需手动执行删除脚本）
```

### Step 5: 真实数据导入（20分钟）
```bash
# 按顺序导入
docker compose exec -T backend python manage.py import_staff --file data/dorm_managers_processed.csv
docker compose exec -T backend python manage.py import_staff --file data/counselors_processed.csv
docker compose exec -T backend python manage.py import_staff --file data/additional_staff.csv
docker compose exec -T backend python manage.py import_students --file data/file5_students_merged_v2.csv --mode clean
```

### Step 6: 导入验证（5分钟）
```bash
# 用户数统计
docker compose exec -T backend python manage.py shell <<'EOF'
from apps.users.models import User
total = User.objects.count()
students = User.objects.filter(role='student').count()
dorm_mgrs = User.objects.filter(role='dorm_manager').count()
counselors = User.objects.filter(role='counselor').count()
admins = User.objects.filter(role='admin').count()

print(f"总用户: {total} (预期6041)")
print(f"学生: {students} (预期5946)")
print(f"宿管: {dorm_mgrs} (预期73: 72+1兜底)")
print(f"辅导: {counselors} (预期20)")
print(f"管理: {admins} (预期2)")
EOF

# 路由覆盖验证
docker compose exec -T backend python scripts/validate_import.py
```

### Step 7: 审批链路抽样测试（10分钟）
```bash
# 提交测试申请（选1个有楼栋学生 + 1个无楼栋学生）
# 验证宿管审批路由
# 验证辅导员审批路由
```

### Step 8: 文档更新（5分钟）
- 更新PROJECT-SUMMARY.md
- 更新session-context.json
- 提交Git记录

---

## 验收标准

✅ **用户数验收：**
- 总用户 = 6041（容忍±10）
- 学生 = 5946（容忍±5）
- 宿管 = 73（72普通 + 1兜底）
- 辅导 = 20
- 管理 = 2

✅ **路由覆盖验收：**
- 辅导员覆盖 = 100%（5946/5946）
- 宿管直接覆盖 ≥ 98%（5830/5946）
- Fallback路由 = 116人通过92008149

✅ **审批链路验收：**
- 有楼栋学生 → 宿管审批（非92008149）
- 无楼栋学生 → 兜底宿管审批（92008149）
- 辅导员审批正常工作

✅ **数据一致性验收：**
- 无TMP临时ID残留
- department字段覆盖率 ≥ 99%
- building字段覆盖率 ≥ 98%

---

## 回滚方案

**如导入失败或数据错误：**
1. 停止backend容器
2. 恢复备份数据库：`docker compose exec -T db psql -U postgres -d graduation_leave < reports/pre_real_import_YYYYMMDDHHMMSS.json`
3. 重启容器
4. 检查数据一致性

---

## 风险控制

⚠️ **高风险操作：**
- 测试数据清理（不可逆）
- 学生数据导入--mode clean（会删除现有数据）

✅ **缓解措施：**
- 执行前完整备份
- Dry-run验证所有CSV
- 清理前确认仅测试数据
- 分步执行，每步验证

---

**执行状态：** 待开始  
**预计时间：** 60-80分钟  
**责任人：** Claude + 用户监督
