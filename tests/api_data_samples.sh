#!/bin/bash
# API数据示例采集脚本
# 测试所有可读GET端点并收集响应示例

set -e

BASE_URL="http://localhost:8001"
OUTPUT_DIR="docs/api-samples"
mkdir -p "$OUTPUT_DIR"

echo "=== API数据采集开始 ==="
echo "Base URL: $BASE_URL"
echo "Output: $OUTPUT_DIR"
echo ""

# 1. 学生登录获取token
echo "1. 学生登录..."
STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020001","password":"2020001"}' \
  | jq -r '.access_token')

if [ -z "$STUDENT_TOKEN" ] || [ "$STUDENT_TOKEN" = "null" ]; then
  echo "✗ 登录失败"
  exit 1
fi
echo "✓ 登录成功"

# 2. 获取申请列表
echo "2. 获取申请列表..."
curl -s "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq '.' > "$OUTPUT_DIR/applications_list.json"
echo "✓ 保存至 applications_list.json"

# 3. 获取第一个申请详情
APP_ID=$(jq -r '.results[0].application_id // empty' "$OUTPUT_DIR/applications_list.json")
if [ -n "$APP_ID" ]; then
  echo "3. 获取申请详情 ($APP_ID)..."
  curl -s "$BASE_URL/api/applications/$APP_ID/" \
    -H "Authorization: Bearer $STUDENT_TOKEN" \
    | jq '.' > "$OUTPUT_DIR/application_detail.json"
  echo "✓ 保存至 application_detail.json"
fi

# 4. 获取通知列表
echo "4. 获取通知列表..."
curl -s "$BASE_URL/api/notifications/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq '.' > "$OUTPUT_DIR/notifications_list.json"
echo "✓ 保存至 notifications_list.json"

# 5. 获取未读通知数
echo "5. 获取未读通知数..."
curl -s "$BASE_URL/api/notifications/unread_count/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq '.' > "$OUTPUT_DIR/notifications_unread_count.json"
echo "✓ 保存至 notifications_unread_count.json"

# 6. 辅导员登录
echo "6. 辅导员登录..."
COUNSELOR_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T001","password":"T001"}' \
  | jq -r '.access_token')

if [ -n "$COUNSELOR_TOKEN" ] && [ "$COUNSELOR_TOKEN" != "null" ]; then
  echo "✓ 辅导员登录成功"

  # 7. 获取审批列表
  echo "7. 获取审批列表（辅导员视角）..."
  curl -s "$BASE_URL/api/approvals/" \
    -H "Authorization: Bearer $COUNSELOR_TOKEN" \
    | jq '.' > "$OUTPUT_DIR/approvals_list_counselor.json"
  echo "✓ 保存至 approvals_list_counselor.json"
fi

echo ""
echo "=== 采集完成 ==="
echo "结果保存在: $OUTPUT_DIR/"
ls -lh "$OUTPUT_DIR/"
