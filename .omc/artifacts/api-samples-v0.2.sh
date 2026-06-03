#!/bin/bash
# API Response Samples for v0.2 Contract
# Generated: 2026-05-31

BASE_URL="http://localhost:8001"
OUT_DIR=".omc/artifacts/api-samples"
mkdir -p "$OUT_DIR"

echo "Collecting API samples..."

# 1. Login (Student)
curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020001","password":"2020001"}' > "$OUT_DIR/01-login-student.json"

TOKEN=$(jq -r '.access_token' "$OUT_DIR/01-login-student.json")

# 2. Submit Application
curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason":"毕业离校","leave_date":"2024-06-30"}' > "$OUT_DIR/02-submit-application.json"

APP_ID=$(jq -r '.application_id' "$OUT_DIR/02-submit-application.json")

# 3. List Applications (Student)
curl -s -X GET "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $TOKEN" > "$OUT_DIR/03-list-applications-student.json"

# 4. Get Application Detail
curl -s -X GET "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $TOKEN" > "$OUT_DIR/04-get-application-detail.json"

# 5. Login (Counselor)
curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T001","password":"T001"}' > "$OUT_DIR/05-login-counselor.json"

COUNSELOR_TOKEN=$(jq -r '.access_token' "$OUT_DIR/05-login-counselor.json")

# 6. List Approvals (Counselor)
curl -s -X GET "$BASE_URL/api/approvals/" \
  -H "Authorization: Bearer $COUNSELOR_TOKEN" > "$OUT_DIR/06-list-approvals-counselor.json"

APPROVAL_ID=$(jq -r '.results[0].approval_id' "$OUT_DIR/06-list-approvals-counselor.json")

# 7. Approve
curl -s -X POST "$BASE_URL/api/approvals/$APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $COUNSELOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"同意"}' > "$OUT_DIR/07-approve.json"

# 8. Login (Dean)
curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"D001","password":"D001"}' > "$OUT_DIR/08-login-dean.json"

DEAN_TOKEN=$(jq -r '.access_token' "$OUT_DIR/08-login-dean.json")

# 9. List Approvals (Dean)
curl -s -X GET "$BASE_URL/api/approvals/" \
  -H "Authorization: Bearer $DEAN_TOKEN" > "$OUT_DIR/09-list-approvals-dean.json"

# 10. Error samples
curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason":"重复提交","leave_date":"2024-06-30"}' > "$OUT_DIR/10-error-conflict.json"

echo "✓ Samples collected in $OUT_DIR/"
ls -lh "$OUT_DIR/"
