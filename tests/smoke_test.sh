#!/bin/bash
# Week 3 Day 1 Smoke Test - Minimum Viable Loop
# Base URL: http://localhost:8001 (Docker Compose)
#
# Prerequisites:
# - Clean database (no existing applications for test users)
# - Seeded test data (users, class mappings)
#
# To reset environment before running:
#   SMOKE_RESET=1 ./tests/smoke_test.sh
#
# Manual reset steps:
#   docker compose down -v
#   docker compose up -d --wait
#   docker compose exec backend python manage.py migrate
#   docker compose exec backend python manage.py seed_data

set -e

BASE_URL="http://localhost:8001"

# Check and handle SMOKE_RESET
if [ "${SMOKE_RESET}" = "1" ]; then
  echo "=== SMOKE_RESET=1: Resetting environment ==="
  echo "1. Stopping containers and removing volumes..."
  docker compose down -v

  echo "2. Starting containers..."
  docker compose up -d --wait

  echo "3. Running migrations..."
  docker compose exec backend python manage.py migrate

  echo "4. Seeding test data..."
  docker compose exec backend python manage.py seed_data

  echo "✓ Environment reset complete"
  echo ""
fi

echo "=== Week 3 Day 1 Smoke Test ==="
echo "Base URL: $BASE_URL"
echo ""

# H1: Happy path (Class A)
echo "--- H1: Happy Path (2020001 → T001 → D001) ---"

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
  -d "{\"reason\":\"毕业离校\",\"leave_date\":\"$LEAVE_DATE\"}")

APP_ID=$(echo "$APP_RESPONSE" | jq -r '.application_id')
APP_STATUS=$(echo "$APP_RESPONSE" | jq -r '.status')

if [ -z "$APP_ID" ] || [ "$APP_ID" = "null" ]; then
  echo "✗ Application submit failed"
  echo "$APP_RESPONSE" | jq '.'
  exit 1
fi

if [ "$APP_STATUS" != "pending_counselor" ]; then
  echo "✗ Application status wrong: $APP_STATUS (expected: pending_counselor)"
  exit 1
fi

echo "✓ Application submitted: $APP_ID (status: $APP_STATUS)"

# Extract counselor approval ID
COUNSELOR_APPROVAL_ID=$(echo "$APP_RESPONSE" | jq -r '.approvals[] | select(.step=="counselor") | .approval_id')

if [ -z "$COUNSELOR_APPROVAL_ID" ] || [ "$COUNSELOR_APPROVAL_ID" = "null" ]; then
  echo "✗ Counselor approval not created"
  exit 1
fi

echo "  Counselor approval: $COUNSELOR_APPROVAL_ID"

# 3. Upload attachment
echo "3. Upload attachment..."
echo "Test attachment content" > /tmp/test_attachment.pdf
UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/$APP_ID/attachments/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -F "file=@/tmp/test_attachment.pdf" \
  -F "attachment_type=other")

ATTACHMENT_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.attachment_id')

if [ -z "$ATTACHMENT_ID" ] || [ "$ATTACHMENT_ID" = "null" ]; then
  echo "✗ Attachment upload failed"
  echo "$UPLOAD_RESPONSE" | jq '.'
  exit 1
fi

echo "✓ Attachment uploaded: $ATTACHMENT_ID"

# 4. List attachments
echo "4. List attachments..."
LIST_RESPONSE=$(curl -s "$BASE_URL/api/applications/$APP_ID/attachments/" \
  -H "Authorization: Bearer $STUDENT_TOKEN")

ATTACHMENT_COUNT=$(echo "$LIST_RESPONSE" | jq -r '.attachments | length')

if [ "$ATTACHMENT_COUNT" != "1" ]; then
  echo "✗ Attachment list failed: expected 1, got $ATTACHMENT_COUNT"
  exit 1
fi

echo "✓ Attachment list success: $ATTACHMENT_COUNT attachment(s)"

# 5. Download attachment
echo "5. Download attachment..."
DOWNLOAD_STATUS=$(curl -s -w "\n%{http_code}" -o /tmp/downloaded_attachment.txt \
  "$BASE_URL/api/attachments/$ATTACHMENT_ID/download/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | tail -1)

if [ "$DOWNLOAD_STATUS" != "200" ]; then
  echo "✗ Attachment download failed: HTTP $DOWNLOAD_STATUS"
  exit 1
fi

echo "✓ Attachment download success"

# 6. Delete attachment
echo "6. Delete attachment..."
DELETE_STATUS=$(curl -s -w "\n%{http_code}" -X DELETE \
  "$BASE_URL/api/attachments/$ATTACHMENT_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | tail -1)

if [ "$DELETE_STATUS" != "204" ]; then
  echo "✗ Attachment delete failed: HTTP $DELETE_STATUS"
  exit 1
fi

echo "✓ Attachment deleted"

# Verify attachment list is empty
FINAL_LIST=$(curl -s "$BASE_URL/api/applications/$APP_ID/attachments/" \
  -H "Authorization: Bearer $STUDENT_TOKEN")
FINAL_COUNT=$(echo "$FINAL_LIST" | jq -r '.attachments | length')

if [ "$FINAL_COUNT" != "0" ]; then
  echo "✗ Attachment still exists after delete"
  exit 1
fi

echo "  Verified: attachment list empty"

# 7. Counselor login
echo "7. Counselor T001 login..."
T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T001","password":"T001"}' \
  | jq -r '.access_token')

if [ -z "$T001_TOKEN" ] || [ "$T001_TOKEN" = "null" ]; then
  echo "✗ Counselor login failed"
  exit 1
fi
echo "✓ Counselor login success"

# Verify counselor received APPLICATION_SUBMITTED notification
echo "  Verifying counselor notification..."
COUNSELOR_NOTIFS=$(curl -s "$BASE_URL/api/notifications/" \
  -H "Authorization: Bearer $T001_TOKEN")

COUNSELOR_APP_NOTIF=$(echo "$COUNSELOR_NOTIFS" | jq -r ".results[] | select(.type == \"application_submitted\" and (.message | contains(\"2020001\")))")

if [ -z "$COUNSELOR_APP_NOTIF" ]; then
  echo "✗ Counselor APPLICATION_SUBMITTED notification not found"
  echo "Available notifications:"
  echo "$COUNSELOR_NOTIFS" | jq '.results[] | {type, message}'
  exit 1
fi

NOTIF_TYPE=$(echo "$COUNSELOR_APP_NOTIF" | jq -r '.type')
NOTIF_ENTITY_TYPE=$(echo "$COUNSELOR_APP_NOTIF" | jq -r '.entity_type')

if [ "$NOTIF_TYPE" != "application_submitted" ]; then
  echo "✗ Notification type wrong: $NOTIF_TYPE (expected: application_submitted)"
  exit 1
fi

if [ "$NOTIF_ENTITY_TYPE" != "approval" ]; then
  echo "✗ Notification entity_type wrong: $NOTIF_ENTITY_TYPE (expected: approval)"
  exit 1
fi

echo "  ✓ Counselor received APPLICATION_SUBMITTED notification (type: $NOTIF_TYPE, entity_type: $NOTIF_ENTITY_TYPE)"

# 8. Counselor approve
echo "8. Counselor approve..."
APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$COUNSELOR_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $T001_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"同意"}')

APPROVE_DECISION=$(echo "$APPROVE_RESPONSE" | jq -r '.decision')

if [ "$APPROVE_DECISION" != "approved" ]; then
  echo "✗ Counselor approve failed"
  echo "$APPROVE_RESPONSE" | jq '.'
  exit 1
fi

echo "✓ Counselor approved"

# Verify student received APPROVAL_APPROVED notification
echo "  Verifying student notification..."
STUDENT_NOTIFS=$(curl -s "$BASE_URL/api/notifications/" \
  -H "Authorization: Bearer $STUDENT_TOKEN")

STUDENT_APPROVE_NOTIF=$(echo "$STUDENT_NOTIFS" | jq -r ".results[] | select(.type == \"approval_approved\" and (.message | contains(\"辅导员\")))")

if [ -z "$STUDENT_APPROVE_NOTIF" ]; then
  echo "✗ Student APPROVAL_APPROVED notification not found"
  echo "Available notifications:"
  echo "$STUDENT_NOTIFS" | jq '.results[] | {type, message}'
  exit 1
fi

NOTIF_TYPE=$(echo "$STUDENT_APPROVE_NOTIF" | jq -r '.type')
NOTIF_ENTITY_TYPE=$(echo "$STUDENT_APPROVE_NOTIF" | jq -r '.entity_type')

if [ "$NOTIF_TYPE" != "approval_approved" ]; then
  echo "✗ Notification type wrong: $NOTIF_TYPE (expected: approval_approved)"
  exit 1
fi

if [ "$NOTIF_ENTITY_TYPE" != "approval" ]; then
  echo "✗ Notification entity_type wrong: $NOTIF_ENTITY_TYPE (expected: approval)"
  exit 1
fi

echo "  ✓ Student received APPROVAL_APPROVED notification (type: $NOTIF_TYPE, entity_type: $NOTIF_ENTITY_TYPE)"

# Verify application status changed
APP_STATUS_AFTER=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.status')

if [ "$APP_STATUS_AFTER" != "pending_dean" ]; then
  echo "✗ Application status not updated: $APP_STATUS_AFTER (expected: pending_dean)"
  exit 1
fi

echo "  Application status: $APP_STATUS_AFTER"

# Extract dean approval ID
DEAN_APPROVAL_ID=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.approvals[] | select(.step=="dean") | .approval_id')

if [ -z "$DEAN_APPROVAL_ID" ] || [ "$DEAN_APPROVAL_ID" = "null" ]; then
  echo "✗ Dean approval not created"
  exit 1
fi

echo "  Dean approval: $DEAN_APPROVAL_ID"

# 9. Dean login
echo "9. Dean D001 login..."
DEAN_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"D001","password":"D001"}' \
  | jq -r '.access_token')

if [ -z "$DEAN_TOKEN" ] || [ "$DEAN_TOKEN" = "null" ]; then
  echo "✗ Dean login failed"
  exit 1
fi
echo "✓ Dean login success"

# 10. Dean approve
echo "10. Dean approve..."
DEAN_APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$DEAN_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $DEAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"批准"}')

DEAN_DECISION=$(echo "$DEAN_APPROVE_RESPONSE" | jq -r '.decision')

if [ "$DEAN_DECISION" != "approved" ]; then
  echo "✗ Dean approve failed"
  echo "$DEAN_APPROVE_RESPONSE" | jq '.'
  exit 1
fi

echo "✓ Dean approved"

# Verify student received second APPROVAL_APPROVED notification
echo "  Verifying student notification..."
STUDENT_NOTIF_COUNT_FINAL=$(curl -s "$BASE_URL/api/notifications/unread_count/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.unread_count')

if [ "$STUDENT_NOTIF_COUNT_FINAL" -lt "2" ]; then
  echo "✗ Student notification count wrong: expected ≥2, got $STUDENT_NOTIF_COUNT_FINAL"
  exit 1
fi

echo "  ✓ Student has $STUDENT_NOTIF_COUNT_FINAL unread notification(s)"

# 11. Verify final status
echo "11. Verify final status..."
FINAL_STATUS=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.status')

if [ "$FINAL_STATUS" != "approved" ]; then
  echo "✗ Final status wrong: $FINAL_STATUS (expected: approved)"
  exit 1
fi

echo "✓ Final status: $FINAL_STATUS"

echo ""
echo "--- H2: Rejection Path (2020002 → T002 reject) ---"

# 12. Student 2020002 login
echo "12. Student 2020002 login..."
STUDENT2_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020002","password":"2020002"}' \
  | jq -r '.access_token')

if [ -z "$STUDENT2_TOKEN" ] || [ "$STUDENT2_TOKEN" = "null" ]; then
  echo "✗ Student 2020002 login failed"
  exit 1
fi
echo "✓ Student 2020002 login success"

# 13. Submit application
echo "13. Submit application..."
APP2_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $STUDENT2_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"reason\":\"测试驳回流程\",\"leave_date\":\"$LEAVE_DATE\"}")

APP2_ID=$(echo "$APP2_RESPONSE" | jq -r '.application_id')
COUNSELOR2_APPROVAL_ID=$(echo "$APP2_RESPONSE" | jq -r '.approvals[] | select(.step=="counselor") | .approval_id')

if [ -z "$APP2_ID" ] || [ "$APP2_ID" = "null" ]; then
  echo "✗ Application submit failed"
  exit 1
fi

echo "✓ Application submitted: $APP2_ID"
echo "  Counselor approval: $COUNSELOR2_APPROVAL_ID"

# 14. T002 login
echo "14. T002 login..."
T002_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T002","password":"T002"}' \
  | jq -r '.access_token')

if [ -z "$T002_TOKEN" ] || [ "$T002_TOKEN" = "null" ]; then
  echo "✗ T002 login failed"
  exit 1
fi
echo "✓ T002 login success"

# 15. T002 reject
echo "15. T002 reject..."
REJECT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$COUNSELOR2_APPROVAL_ID/reject/" \
  -H "Authorization: Bearer $T002_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"材料不齐全，请补充"}')

REJECT_DECISION=$(echo "$REJECT_RESPONSE" | jq -r '.decision')

if [ "$REJECT_DECISION" != "rejected" ]; then
  echo "✗ Counselor reject failed"
  echo "$REJECT_RESPONSE" | jq '.'
  exit 1
fi

echo "✓ Counselor rejected"

# Verify student received APPROVAL_REJECTED notification
echo "  Verifying student rejection notification..."
STUDENT2_NOTIFS=$(curl -s "$BASE_URL/api/notifications/" \
  -H "Authorization: Bearer $STUDENT2_TOKEN")

STUDENT2_REJECT_NOTIF=$(echo "$STUDENT2_NOTIFS" | jq -r ".results[] | select(.type == \"approval_rejected\" and (.message | contains(\"材料不齐全\")))")

if [ -z "$STUDENT2_REJECT_NOTIF" ]; then
  echo "✗ Student APPROVAL_REJECTED notification not found"
  echo "Available notifications:"
  echo "$STUDENT2_NOTIFS" | jq '.results[] | {type, message}'
  exit 1
fi

NOTIF_TYPE=$(echo "$STUDENT2_REJECT_NOTIF" | jq -r '.type')
NOTIF_ENTITY_TYPE=$(echo "$STUDENT2_REJECT_NOTIF" | jq -r '.entity_type')
NOTIF_MESSAGE=$(echo "$STUDENT2_REJECT_NOTIF" | jq -r '.message')

if [ "$NOTIF_TYPE" != "approval_rejected" ]; then
  echo "✗ Notification type wrong: $NOTIF_TYPE (expected: approval_rejected)"
  exit 1
fi

if [ "$NOTIF_ENTITY_TYPE" != "approval" ]; then
  echo "✗ Notification entity_type wrong: $NOTIF_ENTITY_TYPE (expected: approval)"
  exit 1
fi

if ! echo "$NOTIF_MESSAGE" | grep -q "材料不齐全"; then
  echo "✗ Notification message missing rejection reason: $NOTIF_MESSAGE"
  exit 1
fi

echo "  ✓ Student received APPROVAL_REJECTED notification with reason (type: $NOTIF_TYPE, entity_type: $NOTIF_ENTITY_TYPE)"

echo ""
echo "--- N2: Cross-counselor approval (negative test) ---"

# N2: T002 tries to approve T001's approval (should fail)
# (Reusing T002_TOKEN from H2 scenario)
echo "16. T002 tries to approve T001's approval (should fail)..."
CROSS_APPROVE_STATUS=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/approvals/$COUNSELOR_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $T002_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"尝试跨班级审批"}' \
  | tail -1)

if [ "$CROSS_APPROVE_STATUS" != "403" ]; then
  echo "✗ Cross-counselor approve should return 403, got: $CROSS_APPROVE_STATUS"
  exit 1
fi

echo "✓ Cross-counselor approve blocked (403)"

echo ""
echo "=== All tests passed ==="
