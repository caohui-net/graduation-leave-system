# 毕业生离校申请审批系统 - 测试指南

**版本：** 1.0  
**日期：** 2026-06-07  
**状态：** MVP测试就绪

---

## 一、测试环境准备

### 1.1 环境验证

**检查服务状态：**
```bash
cd /home/caohui/projects/graduation-leave-system
docker ps --filter "name=graduation-leave-system"
```

**预期输出：**
- `graduation-leave-system-backend-1`: Up（端口 0.0.0.0:8001->8000/tcp）
- `graduation-leave-system-db-1`: Up (healthy)（端口 0.0.0.0:5432->5432/tcp）

### 1.2 访问地址

**本机访问（推荐）：**
- API文档（Swagger UI）: http://localhost:8001/api/schema/swagger-ui/
- Django管理后台: http://localhost:8001/admin/

**局域网访问（其他设备）：**
- API文档: http://172.17.12.199:8001/api/schema/swagger-ui/
- Django管理后台: http://172.17.12.199:8001/admin/

**主要API端点：**
- 登录: `POST /api/auth/login/`
- 用户信息: `GET /api/auth/me/`
- 提交申请: `POST /api/applications/`
- 申请列表: `GET /api/applications/`
- 审批列表: `GET /api/approvals/`
- 执行审批: `POST /api/approvals/{id}/approve/` 或 `/reject/`

---

## 二、测试账号

### 2.1 测试账号清单

**统一密码：** `test123`

| 角色 | 账号 | 姓名 | 院系/部门 | 用途 |
|------|------|------|-----------|------|
| **学生** | 2024220220323 | 孙芮 | 物理与电信学院 | 提交离校申请 |
| **学生** | 2024220220109 | 徐茜茜 | 物理与电信学院 | 提交离校申请 |
| **学生** | 2024220220114 | 章雯荆 | 物理与电信学院 | 提交离校申请 |
| **宿管员** | 92025040 | 孙凤 | - | 宿舍审批（第一级） |
| **辅导员** | 20250015 | 胡晓炀 | - | 学院审批（第二级） |
| **管理员** | 20144020 | 肖延量 | - | 系统管理 |

**注意事项：**
- 这些账号为真实生产数据，仅临时设置测试密码
- 测试完成后将恢复原始状态
- 原始密码为空（Excel导入时未设置）

### 2.2 数据库统计

- **总用户数：** 6,060人
- **学生数：** 5,965人
- **宿管员：** 73人
- **辅导员：** 20人
- **管理员：** 2人

---

## 三、测试流程

### 3.1 Phase 1: 学生提交申请

**测试账号：** 2024220220323（孙芮）/ test123

**测试步骤：**

#### API测试（使用Swagger UI或curl）

**1. 登录获取Token**
```bash
curl -X POST http://localhost:8001/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "2024220220323",
    "password": "test123"
  }'
```

**预期返回：**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "user_id": "2024220220323",
    "name": "孙芮",
    "role": "student",
    "department": "物理与电信学院"
  }
}
```

**2. 获取用户信息**
```bash
curl -X GET http://localhost:8001/api/auth/me/ \
  -H "Authorization: Bearer <access_token>"
```

**3. 提交离校申请**
```bash
curl -X POST http://localhost:8001/api/applications/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_phone": "13800138000",
    "reason": "毕业离校测试申请",
    "expected_leave_date": "2026-07-01"
  }'
```

**预期返回：**
```json
{
  "id": 1,
  "student": {
    "user_id": "2024220220323",
    "name": "孙芮"
  },
  "contact_phone": "13800138000",
  "reason": "毕业离校测试申请",
  "expected_leave_date": "2026-07-01",
  "status": "pending",
  "current_stage": "dorm_manager",
  "created_at": "2026-06-07T19:00:00Z"
}
```

**4. 查看申请列表**
```bash
curl -X GET http://localhost:8001/api/applications/ \
  -H "Authorization: Bearer <access_token>"
```

**验证要点：**
- ✓ 登录成功获取token
- ✓ 可获取用户信息
- ✓ 申请提交成功
- ✓ 申请状态为pending
- ✓ 当前审批阶段为dorm_manager

---

### 3.2 Phase 2: 宿管员审批

**测试账号：** 92025040（孙凤）/ test123

**测试步骤：**

**1. 登录获取宿管员Token**
```bash
curl -X POST http://localhost:8001/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "92025040",
    "password": "test123"
  }'
```

**2. 查看待审批列表**
```bash
curl -X GET http://localhost:8001/api/approvals/ \
  -H "Authorization: Bearer <dorm_manager_token>"
```

**预期返回：** 包含学生孙芮的申请，status为pending

**3. 执行审批（通过）**
```bash
curl -X POST http://localhost:8001/api/approvals/{approval_id}/approve/ \
  -H "Authorization: Bearer <dorm_manager_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "宿舍物品检查完毕，同意离校"
  }'
```

**预期返回：**
```json
{
  "id": 1,
  "status": "approved",
  "comment": "宿舍物品检查完毕，同意离校",
  "approved_at": "2026-06-07T19:05:00Z"
}
```

**4. 再次查看申请状态**
申请的current_stage应变为counselor，等待辅导员审批。

**验证要点：**
- ✓ 宿管员能看到待审批申请
- ✓ 审批操作成功
- ✓ 审批记录已保存
- ✓ 申请流转到下一环节（辅导员）

---

### 3.3 Phase 3: 辅导员审批

**测试账号：** 20250015（胡晓炀）/ test123

**测试步骤：**

**1. 登录获取辅导员Token**
```bash
curl -X POST http://localhost:8001/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "20250015",
    "password": "test123"
  }'
```

**2. 查看待审批列表**
```bash
curl -X GET http://localhost:8001/api/approvals/ \
  -H "Authorization: Bearer <counselor_token>"
```

**3. 执行审批（通过）**
```bash
curl -X POST http://localhost:8001/api/approvals/{approval_id}/approve/ \
  -H "Authorization: Bearer <counselor_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "学业成绩审核通过，同意离校"
  }'
```

**预期结果：**
- 辅导员审批完成
- 申请current_stage变为dean（等待院长审批）
- 如无院长审批需求，申请可能直接完成（取决于配置）

**验证要点：**
- ✓ 辅导员能看到宿管审批后的申请
- ✓ 辅导员审批成功
- ✓ 申请流转到最终环节

---

### 3.4 Phase 4: 查看最终结果

**学生查看申请状态：**
```bash
curl -X GET http://localhost:8001/api/applications/{application_id}/ \
  -H "Authorization: Bearer <student_token>"
```

**预期返回：**
```json
{
  "id": 1,
  "status": "approved" 或 "pending",
  "current_stage": "dean" 或 "completed",
  "approvals": [
    {
      "stage": "dorm_manager",
      "approver_name": "孙凤",
      "status": "approved",
      "comment": "宿舍物品检查完毕，同意离校"
    },
    {
      "stage": "counselor",
      "approver_name": "胡晓炀",
      "status": "approved",
      "comment": "学业成绩审核通过，同意离校"
    }
  ]
}
```

---

## 四、边界测试

### 4.1 拒绝流程测试

**测试步骤：**
1. 学生提交新申请
2. 宿管员执行拒绝操作

**拒绝API调用：**
```bash
curl -X POST http://localhost:8001/api/approvals/{approval_id}/reject/ \
  -H "Authorization: Bearer <dorm_manager_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "宿舍物品未归还，暂不批准离校"
  }'
```

**预期结果：**
- 审批状态变为rejected
- 申请状态变为rejected
- 学生可查看拒绝原因

### 4.2 权限验证测试

**测试场景：**
1. 学生尝试审批他人申请（应失败）
2. 宿管员尝试审批辅导员阶段申请（应失败）
3. 未登录访问保护接口（应返回401）

**测试示例：**
```bash
# 学生token访问审批接口（应失败）
curl -X POST http://localhost:8001/api/approvals/{approval_id}/approve/ \
  -H "Authorization: Bearer <student_token>" \
  -H "Content-Type: application/json" \
  -d '{"comment":"test"}'
```

**预期返回：** 403 Forbidden

### 4.3 数据验证测试

**无效数据提交：**
```bash
# 缺少必填字段
curl -X POST http://localhost:8001/api/applications/ \
  -H "Authorization: Bearer <student_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_phone": "13800138000"
  }'
```

**预期返回：** 400 Bad Request，包含字段验证错误信息

---

## 五、小程序测试（可选）

### 5.1 准备工作

1. 安装微信开发者工具
2. 导入项目：`/home/caohui/projects/graduation-leave-system/miniprogram`
3. 配置后端地址（如需要）

### 5.2 配置后端地址

编辑`miniprogram/utils/config.ts`或相关配置文件：
```typescript
export const API_BASE_URL = 'http://172.17.12.199:8001/api'
```

### 5.3 测试步骤

1. **登录页面测试**
   - 输入测试账号（2024220220323 / test123）
   - 验证登录成功
   - 检查token存储

2. **学生申请页面测试**
   - 填写申请表单
   - 上传附件（可选）
   - 提交申请
   - 查看提交结果

3. **审批页面测试**
   - 切换宿管员/辅导员账号
   - 查看待审批列表
   - 执行审批操作
   - 验证审批结果

---

## 六、故障排查

### 6.1 连接问题

**问题：** 无法访问http://localhost:8001

**排查步骤：**
1. 检查Docker容器状态：`docker ps`
2. 检查端口占用：`lsof -i:8001`
3. 尝试局域网IP：http://172.17.12.199:8001
4. 检查防火墙设置

### 6.2 认证问题

**问题：** Token无效或过期

**解决方案：**
1. 重新登录获取新token
2. 检查token格式：`Bearer <token>`
3. 验证用户账号密码

### 6.3 审批流程问题

**问题：** 审批操作失败

**排查步骤：**
1. 确认approval_id正确
2. 确认当前角色有权限审批此阶段
3. 检查申请当前状态（current_stage）
4. 查看后端日志：`docker logs graduation-leave-system-backend-1`

---

## 七、测试完成检查清单

### 7.1 功能验证

- [ ] 学生登录成功
- [ ] 学生提交申请成功
- [ ] 宿管员审批成功（通过）
- [ ] 辅导员审批成功（通过）
- [ ] 审批拒绝流程正常
- [ ] 申请状态流转正确
- [ ] 权限控制生效
- [ ] 数据验证正常

### 7.2 API端点验证

- [ ] POST /api/auth/login/ - 登录
- [ ] GET /api/auth/me/ - 获取用户信息
- [ ] POST /api/applications/ - 提交申请
- [ ] GET /api/applications/ - 查看申请列表
- [ ] GET /api/applications/{id}/ - 查看申请详情
- [ ] GET /api/approvals/ - 查看审批列表
- [ ] POST /api/approvals/{id}/approve/ - 审批通过
- [ ] POST /api/approvals/{id}/reject/ - 审批拒绝

### 7.3 数据完整性

- [ ] 申请记录正确保存
- [ ] 审批记录正确关联
- [ ] 时间戳正确记录
- [ ] 用户信息正确关联

---

## 八、测试数据清理

### 8.1 恢复原始密码

测试完成后，执行以下命令恢复账号原始状态：

```bash
docker exec graduation-leave-system-backend-1 python manage.py shell -c "
from apps.users.models import User
test_ids = ['2024220220323', '2024220220109', '2024220220114', '92025040', '20250015', '20144020']
for uid in test_ids:
    user = User.objects.get(user_id=uid)
    user.set_unusable_password()
    user.save()
    print(f'✓ 已恢复 {uid} ({user.name})')
"
```

### 8.2 删除测试申请（可选）

**警告：** 此操作不可逆，谨慎执行！

```bash
docker exec graduation-leave-system-backend-1 python manage.py shell -c "
from apps.applications.models import Application
test_student_ids = ['2024220220323', '2024220220109', '2024220220114']
count = Application.objects.filter(student_id__in=test_student_ids).count()
print(f'即将删除 {count} 条测试申请记录')
# Application.objects.filter(student_id__in=test_student_ids).delete()
# print('测试申请记录已删除')
"
```

---

## 九、附录

### 9.1 测试账号备份

备份文件位置：`.omc/password_backup_20260607.json`

### 9.2 相关文档

- 系统设计文档：`docs/design/2026-05-27-system-design.md`
- 数据对接文档：`docs/数据对接说明文档.md`
- 项目总结：`docs/PROJECT-SUMMARY.md`
- 测试账号清单：`.omc/test-accounts.md`

### 9.3 技术支持

如遇问题，检查以下资源：
1. 后端日志：`docker logs graduation-leave-system-backend-1 -f`
2. 数据库日志：`docker logs graduation-leave-system-db-1`
3. API文档：http://localhost:8001/api/schema/swagger-ui/

---

**文档版本：** 1.0  
**创建日期：** 2026-06-07  
**最后更新：** 2026-06-07  
**状态：** 就绪
