#!/bin/bash
# Integration Test Script for Graduation Leave System
# Tests login, application creation, and approval workflows

API_BASE="http://localhost:8001/api"
PASSED=0
FAILED=0

echo "=== Integration Test Suite ==="
echo

# Test 1: Student Login
echo "[TEST 1] Student login (2024220220323/test123 - 孙芮)"
STUDENT_TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2024220220323","password":"test123"}' \
  | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
if [ -n "$STUDENT_TOKEN" ]; then
  echo "✓ Student login successful"
  ((PASSED++))
else
  echo "✗ Student login failed"
  ((FAILED++))
fi

# Test 2: Dorm Manager Login
echo "[TEST 2] Dorm manager login (92025040/test123 - 孙凤)"
DM_TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"92025040","password":"test123"}' \
  | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
if [ -n "$DM_TOKEN" ]; then
  echo "✓ Dorm manager login successful"
  ((PASSED++))
else
  echo "✗ Dorm manager login failed"
  ((FAILED++))
fi

# Test 3: Counselor Login
echo "[TEST 3] Counselor login (20250015/test123 - 胡晓炀)"
COUNSELOR_TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"20250015","password":"test123"}' \
  | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
if [ -n "$COUNSELOR_TOKEN" ]; then
  echo "✓ Counselor login successful"
  ((PASSED++))
else
  echo "✗ Counselor login failed"
  ((FAILED++))
fi

# Test 4: Admin Login
echo "[TEST 4] Admin login (20144020/test123 - 肖延量)"
ADMIN_TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"20144020","password":"test123"}' \
  | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
if [ -n "$ADMIN_TOKEN" ]; then
  echo "✓ Admin login successful"
  ((PASSED++))
else
  echo "✗ Admin login failed"
  ((FAILED++))
fi

# Test 5: Get Approvals (Dorm Manager)
echo "[TEST 5] Get approval list (dorm manager)"
APPROVAL_COUNT=$(curl -s "$API_BASE/approvals/" \
  -H "Authorization: Bearer $DM_TOKEN" \
  | grep -o '"count":[0-9]*' | cut -d':' -f2)
if [ -n "$APPROVAL_COUNT" ]; then
  echo "✓ Approval list retrieved (count: $APPROVAL_COUNT)"
  ((PASSED++))
else
  echo "✗ Failed to retrieve approval list"
  ((FAILED++))
fi

# Test 6: Get Approval Detail
echo "[TEST 6] Get approval detail"
APPROVAL_ID=$(curl -s "$API_BASE/approvals/" \
  -H "Authorization: Bearer $DM_TOKEN" \
  | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -n "$APPROVAL_ID" ]; then
  APPROVAL_DETAIL=$(curl -s "$API_BASE/approvals/$APPROVAL_ID/" \
    -H "Authorization: Bearer $DM_TOKEN")
  if echo "$APPROVAL_DETAIL" | grep -q "student_name"; then
    echo "✓ Approval detail retrieved with student_name"
    ((PASSED++))
  else
    echo "✗ Approval detail missing student_name"
    ((FAILED++))
  fi
else
  echo "⊘ No approvals available to test detail"
fi

# Test 7: Get Application (Student)
echo "[TEST 7] Get application list (student)"
APP_COUNT=$(curl -s "$API_BASE/applications/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | grep -o '"count":[0-9]*' | cut -d':' -f2)
if [ -n "$APP_COUNT" ]; then
  echo "✓ Application list retrieved (count: $APP_COUNT)"
  ((PASSED++))
else
  echo "✗ Failed to retrieve application list"
  ((FAILED++))
fi

# Test 8: Get Application Detail with Status
echo "[TEST 8] Get application detail (for timeline)"
APP_ID=$(curl -s "$API_BASE/applications/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | grep -o '"application_id":"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -n "$APP_ID" ]; then
  APP_DETAIL=$(curl -s "$API_BASE/applications/$APP_ID/" \
    -H "Authorization: Bearer $STUDENT_TOKEN")
  if echo "$APP_DETAIL" | grep -q '"status"'; then
    APP_STATUS=$(echo "$APP_DETAIL" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    echo "✓ Application detail retrieved (status: $APP_STATUS)"
    ((PASSED++))
  else
    echo "✗ Application detail missing status"
    ((FAILED++))
  fi
else
  echo "⊘ No applications available to test detail"
fi

echo
echo "=== Test Results ==="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo

if [ $FAILED -eq 0 ]; then
  echo "✓ All tests passed"
  exit 0
else
  echo "✗ Some tests failed"
  exit 1
fi
