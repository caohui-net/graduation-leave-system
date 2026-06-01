#!/bin/bash
# Week 3 Day 1 Smoke Test - Minimum Viable Loop
# Base URL: http://localhost:8001 (Docker Compose)

set -e

BASE_URL="http://localhost:8001"

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
echo "Test attachment content" > /tmp/test_attachment.txt
UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/$APP_ID/attachments/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -F "file=@/tmp/test_attachment.txt" \
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
  "$BASE_URL/api/applications/$APP_ID/attachments/$ATTACHMENT_ID/download/" \
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
  "$BASE_URL/api/applications/$APP_ID/attachments/$ATTACHMENT_ID/" \
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
COUNSELOR_NOTIF_COUNT=$(curl -s "$BASE_URL/api/notifications/unread_count/" \
  -H "Authorization: Bearer $T001_TOKEN" \
  | jq -r '.unread_count')

if [ "$COUNSELOR_NOTIF_COUNT" -lt "1" ]; then
  echo "✗ Counselor notification not created: expected ≥1, got $COUNSELOR_NOTIF_COUNT"
  exit 1
fi

echo "  ✓ Counselor has $COUNSELOR_NOTIF_COUNT unread notification(s)"

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
STUDENT_NOTIF_COUNT=$(curl -s "$BASE_URL/api/notifications/unread_count/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.unread_count')

if [ "$STUDENT_NOTIF_COUNT" -lt "1" ]; then
  echo "✗ Student notification not created: expected ≥1, got $STUDENT_NOTIF_COUNT"
  exit 1
fi

echo "  ✓ Student has $STUDENT_NOTIF_COUNT unread notification(s)"

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
echo "--- N2: Cross-counselor approval (negative test) ---"

# N2: T002 tries to approve T001's approval (should fail)
echo "12. T002 login..."
T002_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T002","password":"T002"}' \
  | jq -r '.access_token')

if [ -z "$T002_TOKEN" ] || [ "$T002_TOKEN" = "null" ]; then
  echo "✗ T002 login failed"
  exit 1
fi
echo "✓ T002 login success"

# Login as student 2020002 (CS2020-02, counselor T002)
echo "13. Student 2020002 login..."
STUDENT2_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020002","password":"2020002"}' \
  | jq -r '.access_token')

if [ -z "$STUDENT2_TOKEN" ] || [ "$STUDENT2_TOKEN" = "null" ]; then
  echo "✗ Student 2020002 login failed"
  exit 1
fi
echo "✓ Student 2020002 login success"

# Create application for 2020002 (will be assigned to T002)
echo "14. Create application for 2020002..."
TEST_APP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $STUDENT2_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"reason\":\"测试跨班级审批\",\"leave_date\":\"$LEAVE_DATE\"}")

TEST_APP_ID=$(echo "$TEST_APP_RESPONSE" | jq -r '.application_id')
TEST_COUNSELOR_APPROVAL=$(echo "$TEST_APP_RESPONSE" | jq -r '.approvals[] | select(.step=="counselor") | .approval_id')

echo "  Test application: $TEST_APP_ID"
echo "  Test approval (T002): $TEST_COUNSELOR_APPROVAL"

# T002 tries to approve T001's approval
echo "15. T002 tries to approve T001's approval (should fail)..."
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
