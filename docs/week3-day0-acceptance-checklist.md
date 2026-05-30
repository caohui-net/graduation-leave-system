# Week 3 Day 1-2 - 最小闭环验收清单

**日期：** 2026-05-30  
**目标：** 验证最小闭环可复现运行  
**范围：** 登录 → 提交 → 辅导员审批 → 学工部审批 → 查询状态

---

## 验收标准（8项必须证明）

### 1. 迁移成功执行 ✓/✗

**验证命令：**
```bash
docker compose exec backend python manage.py migrate
```

**成功标准：**
- [ ] 命令执行无错误
- [ ] 所有表创建成功（users, applications, approvals, class_mappings）
- [ ] 数据库连接正常

**失败处理：**
- 检查PostgreSQL容器是否启动
- 检查数据库配置（.env.docker）
- 查看迁移文件是否有语法错误

---

### 2. Seed数据足以支持两级审批 ✓/✗

**验证命令：**
```bash
docker compose exec backend python manage.py seed_data
```

**成功标准：**
- [ ] 至少2个学生（不同班级）
- [ ] 至少2个辅导员（对应不同班级）
- [ ] 1个学工部
- [ ] 2条班级映射关系正确

**验证查询：**
```sql
-- 检查用户数量
SELECT role, COUNT(*) FROM users GROUP BY role;
-- 预期：student=2, counselor=2, dean=1

-- 检查班级映射
SELECT * FROM class_mappings WHERE active=true;
-- 预期：2条记录
```

**失败处理：**
- 检查seed_data命令输出
- 手动查询数据库验证数据
- 必要时使用Django admin手动创建

---

### 3. 登录后学生能提交申请 ✓/✗

**验证步骤：**

**Step 1: 学生登录**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "2020001", "password": "2020001"}'
```

**预期响应：**
```json
{
  "token": "eyJ...",
  "user": {
    "user_id": "2020001",
    "name": "张三",
    "role": "student"
  }
}
```

**Step 2: 提交申请**
```bash
curl -X POST http://localhost:8000/api/applications \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "毕业离校",
    "leave_date": "2024-07-01"
  }'
```

**预期响应：**
```json
{
  "application_id": 1,
  "student_id": "2020001",
  "status": "pending_counselor",
  "dorm_checkout_status": "completed"
}
```

**成功标准：**
- [ ] 登录返回JWT token
- [ ] 提交申请返回application_id
- [ ] 状态为pending_counselor
- [ ] 宿舍清退状态为completed

**失败处理：**
- 401错误：检查JWT配置
- 400错误：检查请求参数
- 409错误：检查宿舍清退mock配置

---

### 4. 辅导员能审批对应学生申请 ✓/✗

**验证步骤：**

**Step 1: 辅导员登录**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "T001", "password": "T001"}'
```

**Step 2: 审批申请**
```bash
curl -X POST http://localhost:8000/api/approvals/1/approve \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"comment": "同意"}'
```

**预期响应：**
```json
{
  "approval_id": 1,
  "application_id": 1,
  "step": "counselor",
  "decision": "approved",
  "comment": "同意"
}
```

**Step 3: 验证申请状态变更**
```bash
curl -X GET http://localhost:8000/api/applications/1 \
  -H "Authorization: Bearer <student_token>"
```

**预期响应：**
```json
{
  "application_id": 1,
  "status": "pending_dean",
  "approvals": [
    {
      "step": "counselor",
      "decision": "approved",
      "approver_name": "王老师"
    }
  ]
}
```

**成功标准：**
- [ ] 辅导员能登录
- [ ] 审批操作成功
- [ ] 申请状态从pending_counselor变为pending_dean
- [ ] 审批记录正确创建

**失败处理：**
- 403错误：检查权限校验逻辑
- 404错误：检查申请ID是否存在
- 状态未变更：检查状态机逻辑

---

### 5. 学工部能进行最终审批 ✓/✗

**验证步骤：**

**Step 1: 学工部登录**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "D001", "password": "D001"}'
```

**Step 2: 审批申请**
```bash
curl -X POST http://localhost:8000/api/approvals/2/approve \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"comment": "同意离校"}'
```

**预期响应：**
```json
{
  "approval_id": 2,
  "application_id": 1,
  "step": "dean",
  "decision": "approved",
  "comment": "同意离校"
}
```

**Step 3: 验证最终状态**
```bash
curl -X GET http://localhost:8000/api/applications/1 \
  -H "Authorization: Bearer <student_token>"
```

**预期响应：**
```json
{
  "application_id": 1,
  "status": "approved",
  "approvals": [
    {
      "step": "counselor",
      "decision": "approved"
    },
    {
      "step": "dean",
      "decision": "approved"
    }
  ]
}
```

**成功标准：**
- [ ] 学工部能登录
- [ ] 审批操作成功
- [ ] 申请状态从pending_dean变为approved
- [ ] 两条审批记录都存在

**失败处理：**
- 检查学工部权限配置
- 检查状态机最终状态逻辑

---

### 6. 学生能查询最终状态 ✓/✗

**验证步骤：**
```bash
curl -X GET http://localhost:8000/api/applications/1 \
  -H "Authorization: Bearer <student_token>"
```

**预期响应：**
```json
{
  "application_id": 1,
  "student_id": "2020001",
  "status": "approved",
  "reason": "毕业离校",
  "leave_date": "2024-07-01",
  "dorm_checkout_status": "completed",
  "approvals": [
    {
      "step": "counselor",
      "decision": "approved",
      "approver_name": "王老师",
      "comment": "同意",
      "decided_at": "2024-05-30T10:00:00Z"
    },
    {
      "step": "dean",
      "decision": "approved",
      "approver_name": "刘主任",
      "comment": "同意离校",
      "decided_at": "2024-05-30T10:05:00Z"
    }
  ]
}
```

**成功标准：**
- [ ] 学生能查询自己的申请
- [ ] 状态显示正确（approved）
- [ ] 审批历史完整
- [ ] 时间戳正确

**失败处理：**
- 检查序列化器配置
- 检查审批记录关联

---

### 7. 学生不能查询或操作他人申请（负向权限验证）✓/✗

**验证步骤：**

**Step 1: 学生2登录**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "2020002", "password": "2020002"}'
```

**Step 2: 尝试查询学生1的申请**
```bash
curl -X GET http://localhost:8000/api/applications/1 \
  -H "Authorization: Bearer <student2_token>"
```

**预期响应：**
```json
{
  "error": "FORBIDDEN",
  "message": "无权访问此申请"
}
```
**HTTP状态码：** 403

**Step 3: 尝试修改学生1的申请（如果有更新接口）**
```bash
curl -X PATCH http://localhost:8000/api/applications/1 \
  -H "Authorization: Bearer <student2_token>" \
  -H "Content-Type: application/json" \
  -d '{"reason": "恶意修改"}'
```

**预期响应：**
```json
{
  "error": "FORBIDDEN",
  "message": "无权修改此申请"
}
```
**HTTP状态码：** 403

**成功标准：**
- [ ] 学生2查询学生1申请返回403
- [ ] 学生2修改学生1申请返回403
- [ ] 错误消息清晰

**失败处理：**
- 如果返回200：权限校验缺失，P0阻塞问题
- 如果返回404：权限校验逻辑错误，应该403而非404

---

### 8. 宿舍清退可用Mock通过，但接口边界有记录 ✓/✗

**验证步骤：**

**Step 1: 检查Mock实现**
```bash
# 查看MockDormCheckoutProvider代码
cat backend/apps/applications/services/dorm_checkout.py
```

**预期内容：**
- [ ] MockDormCheckoutProvider类存在
- [ ] check_status方法实现
- [ ] 返回completed状态（对于2020001、2020002）

**Step 2: 验证Mock调用**
```bash
# 提交申请时会调用宿舍清退检查
curl -X POST http://localhost:8000/api/applications \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "测试宿舍清退",
    "leave_date": "2024-07-01"
  }'
```

**预期响应：**
```json
{
  "application_id": 2,
  "dorm_checkout_status": "completed"
}
```

**Step 3: 检查接口边界文档**
```bash
# 查看接口定义
cat backend/apps/applications/services/dorm_checkout.py | grep -A 10 "class DormCheckoutProvider"
```

**预期内容：**
- [ ] 接口抽象类定义
- [ ] check_status方法签名
- [ ] 返回值类型注释
- [ ] 异常处理占位

**成功标准：**
- [ ] Mock返回completed状态
- [ ] 申请提交不被阻塞
- [ ] 接口抽象类已定义
- [ ] 有TODO注释标记真实API集成点

**失败处理：**
- Mock返回pending：检查student_id映射
- 接口未定义：补充抽象类定义

---

## 可复现验证入口

### 方式1：Smoke Test脚本（推荐）

**创建：** `tests/smoke_test.sh`

```bash
#!/bin/bash
set -e

echo "=== 最小闭环Smoke Test ==="

# 1. 学生登录
STUDENT_TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "2020001", "password": "2020001"}' \
  | jq -r '.token')

echo "✓ 学生登录成功"

# 2. 提交申请
APP_ID=$(curl -s -X POST http://localhost:8000/api/applications \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason": "毕业离校", "leave_date": "2024-07-01"}' \
  | jq -r '.application_id')

echo "✓ 申请提交成功: $APP_ID"

# 3. 辅导员审批
COUNSELOR_TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "T001", "password": "T001"}' \
  | jq -r '.token')

curl -s -X POST http://localhost:8000/api/approvals/1/approve \
  -H "Authorization: Bearer $COUNSELOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment": "同意"}' > /dev/null

echo "✓ 辅导员审批成功"

# 4. 学工部审批
DEAN_TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "D001", "password": "D001"}' \
  | jq -r '.token')

curl -s -X POST http://localhost:8000/api/approvals/2/approve \
  -H "Authorization: Bearer $DEAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment": "同意离校"}' > /dev/null

echo "✓ 学工部审批成功"

# 5. 查询最终状态
STATUS=$(curl -s -X GET http://localhost:8000/api/applications/$APP_ID \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.status')

if [ "$STATUS" = "approved" ]; then
  echo "✓ 最终状态正确: approved"
else
  echo "✗ 最终状态错误: $STATUS"
  exit 1
fi

echo "=== 所有测试通过 ==="
```

**执行：**
```bash
chmod +x tests/smoke_test.sh
./tests/smoke_test.sh
```

---

### 方式2：Postman集合

**导出：** `tests/minimum_loop.postman_collection.json`

**包含请求：**
1. 学生登录
2. 提交申请
3. 辅导员登录
4. 辅导员审批
5. 学工部登录
6. 学工部审批
7. 查询最终状态
8. 负向权限验证

---

### 方式3：命令序列文档

**文档：** `docs/manual-verification-steps.md`

**内容：** 逐步curl命令，可手动复制执行

---

## 问题分类标准

### P0（阻塞闭环）
- 迁移失败
- 登录失败
- 提交申请失败
- 审批操作失败
- 状态机不工作
- 权限校验缺失

### P1（影响验收）
- 错误消息不清晰
- 审批记录缺失字段
- 时间戳格式错误
- Mock配置不完整

### P2（不影响闭环）
- 代码注释缺失
- 日志输出不足
- 性能未优化
- 测试覆盖不足

---

## Day 2输出要求

### 必须产出
1. **可复现验证脚本**（smoke_test.sh或Postman集合）
2. **P0问题清单**（如果有）
3. **P1/P2问题清单**
4. **Week 3后续开发优先级**

### 决策门评估
- **继续Week 3扩展开发**：最小闭环通过，仅剩P1/P2问题
- **Day 3修复P0**：闭环接近通过，剩余明确局部P0缺陷
- **停止并重设计**：发现架构级阻塞（状态机错误、数据模型缺陷、契约冲突）

---

**文档状态：** 已完成  
**Day 0准备状态：** 全部完成（环境策略、seed数据、验收清单）  
**下一步：** 开始Day 1执行
