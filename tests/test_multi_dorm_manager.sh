#!/bin/bash
# Test multi-dorm-manager approval workflow
# Scenario: Student in 1号楼 submits application, both M001 and M003 receive approval tasks

set -e

BASE_URL="http://localhost:8001"

echo "=== Multi-Dorm-Manager Approval Test ==="

# 1. Student login
echo "1. Student 2020001 login..."
STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020001","password":"2020001"}' \
  | jq -r '.access_token')

if [ -z "$STUDENT_TOKEN" ] || [ "$STUDENT_TOKEN" = "null" ]; then
  echo "✗ Student login failed"
  exit 1
fi
echo "✓ Student login success"

# 2. Submit application
echo "2. Submit application..."
LEAVE_DATE=$(date -d "+1 day" +%Y-%m-%d)
APP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"reason\":\"测试多宿管员审批\",\"leave_date\":\"$LEAVE_DATE\"}")

APP_ID=$(echo "$APP_RESPONSE" | jq -r '.application_id')
if [ -z "$APP_ID" ] || [ "$APP_ID" = "null" ]; then
  echo "✗ Application submit failed"
  echo "$APP_RESPONSE" | jq '.'
  exit 1
fi
echo "✓ Application submitted: $APP_ID"

# 3. Check approvals count
APPROVALS_COUNT=$(echo "$APP_RESPONSE" | jq '.approvals | length')
echo "  Approvals created: $APPROVALS_COUNT"

if [ "$APPROVALS_COUNT" != "2" ]; then
  echo "✗ Expected 2 approvals (M001 and M003), got $APPROVALS_COUNT"
  exit 1
fi
echo "✓ Both M001 and M003 received approval tasks"

# Extract approval IDs
M001_APPROVAL_ID=$(echo "$APP_RESPONSE" | jq -r '.approvals[] | select(.approver_name=="宿管员1") | .approval_id')
M003_APPROVAL_ID=$(echo "$APP_RESPONSE" | jq -r '.approvals[] | select(.approver_name=="宿管员3") | .approval_id')

echo "  M001 approval: $M001_APPROVAL_ID"
echo "  M003 approval: $M003_APPROVAL_ID"

# 4. M001 login
echo "4. M001 login..."
M001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"M001","password":"M001"}' \
  | jq -r '.access_token')
echo "✓ M001 login success"

# 5. M001 approve
echo "5. M001 approve..."
M001_APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$M001_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $M001_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"同意"}')

M001_DECISION=$(echo "$M001_APPROVE_RESPONSE" | jq -r '.decision')
if [ "$M001_DECISION" != "approved" ]; then
  echo "✗ M001 approve failed"
  exit 1
fi
echo "✓ M001 approved"

# 6. Check M003's approval status
echo "6. Check M003's approval status..."
M003_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"M003","password":"M003"}' \
  | jq -r '.access_token')

M003_APPROVAL_STATUS=$(curl -s "$BASE_URL/api/approvals/$M003_APPROVAL_ID/" \
  -H "Authorization: Bearer $M003_TOKEN")

M003_DECISION=$(echo "$M003_APPROVAL_STATUS" | jq -r '.decision')
M003_COMMENT=$(echo "$M003_APPROVAL_STATUS" | jq -r '.comment')

if [ "$M003_DECISION" != "approved" ]; then
  echo "✗ M003 approval not auto-completed, decision: $M003_DECISION"
  exit 1
fi

if ! echo "$M003_COMMENT" | grep -q "已由宿管员1完成审批"; then
  echo "✗ M003 comment missing auto-complete message: $M003_COMMENT"
  exit 1
fi

echo "✓ M003 approval auto-completed with message: $M003_COMMENT"

echo ""
echo "=== All tests passed ==="
