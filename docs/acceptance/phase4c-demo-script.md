# Phase 4C 演示脚本

**版本：** v1.0  
**创建日期：** 2026-06-01  
**目的：** 可顺序执行的端到端演示路径

---

## 前置准备

### 环境要求

- Docker和Docker Compose已安装
- 端口8001可用
- jq命令行工具已安装（用于JSON解析）

### 检查环境

```bash
# 检查Docker
docker --version
docker compose version

# 检查jq
jq --version

# 检查端口
lsof -i :8001 || echo "端口8001可用"
```

---

## 演示流程

### 步骤1：启动Docker环境

```bash
# 进入项目目录
cd /path/to/graduation-leave-system

# 启动服务
docker compose up -d

# 等待服务健康（约10秒）
sleep 10

# 检查服务状态
docker compose ps
```

**预期输出：** backend和db容器状态为"running (healthy)"

---

### 步骤2：数据库迁移

```bash
# 执行迁移
docker compose exec backend python manage.py migrate

# 验证迁移
docker compose exec backend python manage.py showmigrations
```

**预期输出：** 所有迁移标记为[X]

---

### 步骤3：加载测试数据

```bash
# 加载seed数据
docker compose exec backend python manage.py seed_data

# 验证数据
docker compose exec backend python manage.py shell -c "
from apps.users.models import User
print(f'Users: {User.objects.count()}')
print(f'Students: {User.objects.filter(role=\"student\").count()}')
print(f'Counselors: {User.objects.filter(role=\"counselor\").count()}')
print(f'Deans: {User.objects.filter(role=\"dean\").count()}')
"
```

**预期输出：**
- Users: 13
- Students: 10
- Counselors: 2
- Deans: 1

---

### 步骤4：学生登录并提交申请

```bash
BASE_URL="http://localhost:8001"

# 学生登录
STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020001","password":"2020001"}' \
  | jq -r '.access_token')

echo "Student token: ${STUDENT_TOKEN:0:20}..."

# 提交申请
LEAVE_DATE=$(date -d "+1 day" +%Y-%m-%d)
APP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"reason\":\"毕业离校\",\"leave_date\":\"$LEAVE_DATE\"}")

APP_ID=$(echo "$APP_RESPONSE" | jq -r '.application_id')
APP_STATUS=$(echo "$APP_RESPONSE" | jq -r '.status')

echo "Application ID: $APP_ID"
echo "Status: $APP_STATUS"
```

**预期输出：**
- Application ID: app_xxxxxxxx
- Status: pending_counselor

---

### 步骤5：上传附件

```bash
# 创建测试附件
echo "毕业离校申请附件 - 测试文件" > /tmp/test_attachment.txt

# 上传附件
UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/$APP_ID/attachments/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -F "file=@/tmp/test_attachment.txt" \
  -F "attachment_type=other")

ATTACHMENT_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.attachment_id')

echo "Attachment ID: $ATTACHMENT_ID"
```

**预期输出：** Attachment ID: att_xxxxxxxx

---

### 步骤6：列出附件

```bash
# 列出附件
LIST_RESPONSE=$(curl -s "$BASE_URL/api/applications/$APP_ID/attachments/" \
  -H "Authorization: Bearer $STUDENT_TOKEN")

ATTACHMENT_COUNT=$(echo "$LIST_RESPONSE" | jq -r '.attachments | length')

echo "Attachment count: $ATTACHMENT_COUNT"
echo "$LIST_RESPONSE" | jq '.attachments[0] | {attachment_id, attachment_type, uploaded_at}'
```

**预期输出：** Attachment count: 1

---

### 步骤7：下载附件

```bash
# 下载附件
curl -s -o /tmp/downloaded_attachment.txt \
  "$BASE_URL/api/applications/$APP_ID/attachments/$ATTACHMENT_ID/download/" \
  -H "Authorization: Bearer $STUDENT_TOKEN"

# 验证内容
cat /tmp/downloaded_attachment.txt
```

**预期输出：** 毕业离校申请附件 - 测试文件

---

### 步骤8：辅导员审批

```bash
# 提取辅导员审批ID
COUNSELOR_APPROVAL_ID=$(echo "$APP_RESPONSE" | jq -r '.approvals[] | select(.step=="counselor") | .approval_id')

echo "Counselor approval ID: $COUNSELOR_APPROVAL_ID"

# 辅导员登录
T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T001","password":"T001"}' \
  | jq -r '.access_token')

echo "Counselor token: ${T001_TOKEN:0:20}..."

# 辅导员审批
APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$COUNSELOR_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $T001_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"同意"}')

APPROVE_DECISION=$(echo "$APPROVE_RESPONSE" | jq -r '.decision')

echo "Counselor decision: $APPROVE_DECISION"
```

**预期输出：** Counselor decision: approved

---

### 步骤9：验证状态变更

```bash
# 查询申请状态
APP_STATUS_AFTER=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.status')

echo "Application status after counselor approval: $APP_STATUS_AFTER"
```

**预期输出：** Application status after counselor approval: pending_dean

---

### 步骤10：学工部审批

```bash
# 提取学工部审批ID
DEAN_APPROVAL_ID=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.approvals[] | select(.step=="dean") | .approval_id')

echo "Dean approval ID: $DEAN_APPROVAL_ID"

# 学工部登录
DEAN_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"D001","password":"D001"}' \
  | jq -r '.access_token')

echo "Dean token: ${DEAN_TOKEN:0:20}..."

# 学工部审批
DEAN_APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$DEAN_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $DEAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"批准"}')

DEAN_DECISION=$(echo "$DEAN_APPROVE_RESPONSE" | jq -r '.decision')

echo "Dean decision: $DEAN_DECISION"
```

**预期输出：** Dean decision: approved

---

### 步骤11：验证最终状态

```bash
# 查询最终状态
FINAL_STATUS=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.status')

echo "Final application status: $FINAL_STATUS"

# 查询完整申请详情
curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq '{application_id, status, approvals: [.approvals[] | {step, decision, decided_at}]}'
```

**预期输出：** Final application status: approved

---

### 步骤12：错误处理演示 - 跨辅导员审批

```bash
# T002登录
T002_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T002","password":"T002"}' \
  | jq -r '.access_token')

# T002尝试审批T001的审批（应该失败）
CROSS_APPROVE_STATUS=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/approvals/$COUNSELOR_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $T002_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"尝试跨班级审批"}' \
  | tail -1)

echo "Cross-counselor approve HTTP status: $CROSS_APPROVE_STATUS"
```

**预期输出：** Cross-counselor approve HTTP status: 403

---

### 步骤13：错误处理演示 - 重复提交

```bash
# 尝试重复提交申请（应该失败）
DUPLICATE_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"reason\":\"重复提交\",\"leave_date\":\"$LEAVE_DATE\"}" \
  | tail -1)

echo "Duplicate submission HTTP status: $DUPLICATE_RESPONSE"
```

**预期输出：** Duplicate submission HTTP status: 409

---

## 清理环境

```bash
# 停止服务
docker compose down

# 清理测试文件
rm -f /tmp/test_attachment.txt /tmp/downloaded_attachment.txt

echo "演示环境已清理"
```

---

## 完整演示脚本

将以上所有步骤合并为一个可执行脚本：

**路径：** `tests/demo_script.sh`

```bash
#!/bin/bash
# Phase 4C 完整演示脚本

set -e

BASE_URL="http://localhost:8001"

echo "=== Phase 4C 演示脚本 ==="
echo ""

# 步骤1-3: 环境准备
echo "--- 步骤1-3: 环境准备 ---"
docker compose up -d
sleep 10
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_data
echo "✓ 环境准备完成"
echo ""

# 步骤4: 学生登录并提交申请
echo "--- 步骤4: 学生登录并提交申请 ---"
STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020001","password":"2020001"}' \
  | jq -r '.access_token')

LEAVE_DATE=$(date -d "+1 day" +%Y-%m-%d)
APP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"reason\":\"毕业离校\",\"leave_date\":\"$LEAVE_DATE\"}")

APP_ID=$(echo "$APP_RESPONSE" | jq -r '.application_id')
echo "✓ 申请已提交: $APP_ID"
echo ""

# 步骤5-7: 附件操作
echo "--- 步骤5-7: 附件操作 ---"
echo "测试附件内容" > /tmp/test_attachment.txt
UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/$APP_ID/attachments/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -F "file=@/tmp/test_attachment.txt" \
  -F "attachment_type=other")
ATTACHMENT_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.attachment_id')
echo "✓ 附件已上传: $ATTACHMENT_ID"
echo ""

# 步骤8: 辅导员审批
echo "--- 步骤8: 辅导员审批 ---"
COUNSELOR_APPROVAL_ID=$(echo "$APP_RESPONSE" | jq -r '.approvals[] | select(.step=="counselor") | .approval_id')
T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T001","password":"T001"}' \
  | jq -r '.access_token')
curl -s -X POST "$BASE_URL/api/approvals/$COUNSELOR_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $T001_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"同意"}' > /dev/null
echo "✓ 辅导员审批通过"
echo ""

# 步骤10: 学工部审批
echo "--- 步骤10: 学工部审批 ---"
DEAN_APPROVAL_ID=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.approvals[] | select(.step=="dean") | .approval_id')
DEAN_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"D001","password":"D001"}' \
  | jq -r '.access_token')
curl -s -X POST "$BASE_URL/api/approvals/$DEAN_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $DEAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"批准"}' > /dev/null
echo "✓ 学工部审批通过"
echo ""

# 步骤11: 验证最终状态
echo "--- 步骤11: 验证最终状态 ---"
FINAL_STATUS=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.status')
echo "✓ 最终状态: $FINAL_STATUS"
echo ""

# 步骤12-13: 错误处理演示
echo "--- 步骤12-13: 错误处理演示 ---"
T002_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T002","password":"T002"}' \
  | jq -r '.access_token')
CROSS_STATUS=$(curl -s -w "%{http_code}" -o /dev/null -X POST "$BASE_URL/api/approvals/$COUNSELOR_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $T002_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"跨班级"}')
echo "✓ 跨辅导员审批阻断: HTTP $CROSS_STATUS"
echo ""

echo "=== 演示完成 ==="
```

---

**演示脚本版本：** v1.0  
**最后更新：** 2026-06-01  
**执行时间：** 约2-3分钟
