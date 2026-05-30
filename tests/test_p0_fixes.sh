#!/bin/bash
# Test P0 fixes: resubmission after rejection + approval history filter

BASE_URL="http://localhost:8001"

echo "=== Testing P0 Fixes ==="
echo

# Reset data
echo "1. Resetting data..."
docker compose exec backend python manage.py seed_data --reset > /dev/null 2>&1

# Login as student
echo "2. Student login..."
TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020001","password":"2020001"}' | jq -r '.access_token')

# Submit first application
echo "3. Submitting first application..."
APP_ID=$(curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason":"第一次申请","leave_date":"2024-06-30"}' | jq -r '.application_id')
echo "   Application ID: $APP_ID"

# Try to submit again (should fail - pending exists)
echo "4. Try duplicate submission (should fail)..."
RESULT=$(curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason":"重复申请","leave_date":"2024-06-30"}')
echo "   Result: $(echo $RESULT | jq -r '.error.message')"

# Counselor rejects
echo "5. Counselor rejects application..."
COUNSELOR_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T001","password":"T001"}' | jq -r '.access_token')

APPROVAL_ID=$(curl -s -X GET "$BASE_URL/api/approvals/" \
  -H "Authorization: Bearer $COUNSELOR_TOKEN" | jq -r '.results[0].approval_id')

curl -s -X POST "$BASE_URL/api/approvals/$APPROVAL_ID/reject/" \
  -H "Authorization: Bearer $COUNSELOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"需要修改"}' > /dev/null

echo "   Rejected approval: $APPROVAL_ID"

# Student resubmits after rejection (should succeed)
echo "6. Student resubmits after rejection (should succeed)..."
APP_ID2=$(curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason":"修改后重新申请","leave_date":"2024-06-30"}' | jq -r '.application_id')
echo "   New application ID: $APP_ID2"

if [ "$APP_ID2" != "null" ]; then
  echo "   ✓ Resubmission after rejection works!"
else
  echo "   ✗ Resubmission failed"
fi

# Test approval history filter
echo "7. Testing approval history filter..."

# Pending approvals (default)
PENDING_COUNT=$(curl -s -X GET "$BASE_URL/api/approvals/" \
  -H "Authorization: Bearer $COUNSELOR_TOKEN" | jq -r '.count')
echo "   Pending approvals: $PENDING_COUNT"

# Rejected approvals
REJECTED_COUNT=$(curl -s -X GET "$BASE_URL/api/approvals/?decision=rejected" \
  -H "Authorization: Bearer $COUNSELOR_TOKEN" | jq -r '.count')
echo "   Rejected approvals: $REJECTED_COUNT"

# All approvals
ALL_COUNT=$(curl -s -X GET "$BASE_URL/api/approvals/?decision=all" \
  -H "Authorization: Bearer $COUNSELOR_TOKEN" | jq -r '.count')
echo "   All approvals: $ALL_COUNT"

if [ "$ALL_COUNT" -gt "$PENDING_COUNT" ]; then
  echo "   ✓ Approval history filter works!"
else
  echo "   ✗ Filter may not be working"
fi

echo
echo "=== Test Complete ==="
