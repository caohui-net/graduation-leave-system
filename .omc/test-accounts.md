# 测试账号清单

**创建时间：** 2026-06-07  
**状态：** 临时测试密码已设置  
**备份文件：** `.omc/password_backup_20260607.json`

---

## 测试账号（统一密码：test123）

### 学生账号（3个）
| 学号 | 姓名 | 院系 | 班级 | 用途 |
|------|------|------|------|------|
| 2024220220323 | 孙芮 | 物理与电信学院 | 电信(专升本)202403 | 提交离校申请 |
| 2024220220109 | 徐茜茜 | 物理与电信学院 | 电信(专升本)202401 | 提交离校申请 |
| 2024220220114 | 章雯荆 | 物理与电信学院 | 电信(专升本)202401 | 提交离校申请 |

### 宿管员账号（1个）
| 工号 | 姓名 | 角色 | 用途 |
|------|------|------|------|
| 92025040 | 孙凤 | dorm_manager | 审批宿舍离校 |

### 辅导员账号（1个）
| 工号 | 姓名 | 角色 | 院系 | 用途 |
|------|------|------|------|------|
| 20250015 | 胡晓炀 | counselor | - | 审批学院离校 |

### 管理员账号（1个）
| 工号 | 姓名 | 角色 | 用途 |
|------|------|------|------|
| 20144020 | 肖延量 | admin | 系统管理 |

---

## 测试流程建议

### 1. 学生端测试（使用孙芮账号）
- 登录：2024220220323 / test123
- 提交离校申请
- 上传附件
- 查看审批进度

### 2. 宿管审批测试（使用孙凤账号）
- 登录：92025040 / test123
- 查看待审批列表
- 审批学生离校申请（通过/拒绝）

### 3. 辅导员审批测试（使用胡晓炀账号）
- 登录：20250015 / test123
- 查看待审批列表
- 审批学生离校申请（通过/拒绝）

### 4. 管理员测试（使用肖延量账号）
- 登录：20144020 / test123
- 查看全部申请
- 管理用户信息

---

## 访问地址

**后端API：** http://localhost:8001  
**小程序开发者工具：** 需配置 miniprogram 项目

**API基础URL：** `http://localhost:8001/api/`

### 主要API端点
- 登录：`POST /api/auth/login/`
- 用户信息：`GET /api/users/me/`
- 提交申请：`POST /api/applications/`
- 审批列表：`GET /api/approvals/`
- 审批操作：`POST /api/approvals/{id}/approve/` 或 `/reject/`

---

## 恢复原状态

**说明：** 这些账号原始密码为空（Excel导入时未设置），无需恢复。

**如需清除测试密码：**
```bash
docker exec graduation-leave-system-backend-1 python manage.py shell -c "
from apps.users.models import User
test_ids = ['2024220220323', '2024220220109', '2024220220114', '92025040', '20250015', '20144020']
for uid in test_ids:
    user = User.objects.get(user_id=uid)
    user.set_unusable_password()
    user.save()
    print(f'✓ 已重置 {uid} ({user.name})')
"
```

**如需删除测试记录（谨慎）：**
```bash
docker exec graduation-leave-system-backend-1 python manage.py shell -c "
from apps.applications.models import Application
from apps.approvals.models import Approval
# 删除测试数据的申请记录
test_student_ids = ['2024220220323', '2024220220109', '2024220220114']
Application.objects.filter(student_id__in=test_student_ids).delete()
print('测试申请记录已删除')
"
```

---

**完成测试后告知Claude，将执行状态恢复操作。**
