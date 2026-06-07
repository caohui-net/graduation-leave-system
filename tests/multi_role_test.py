#!/usr/bin/env python3
"""
Multi-Role Workflow Test Script
Tests login and basic operations for different user roles
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8001"

# Test users for each role
TEST_USERS = {
    "student": {"user_id": "2022240340415", "password": "password123", "role": "student"},
    "counselor": {"user_id": "20020559", "password": "password123", "role": "counselor"},
    "dorm_manager": {"user_id": "92001364", "password": "password123", "role": "dorm_manager"},
    "admin": {"user_id": "19970545", "password": "password123", "role": "admin"},
    "student_2": {"user_id": "2022190140302", "password": "password123", "role": "student"},
}

results = []

def test_role_login(role, user_id, password):
    """Test login for a specific role"""
    result = {
        "role": role,
        "user_id": user_id,
        "steps": {},
        "success": False,
        "error": None
    }

    try:
        # Step 1: Login
        login_resp = requests.post(f"{BASE_URL}/api/auth/login", json={
            "user_id": user_id,
            "password": password
        })

        if login_resp.status_code != 200:
            result["error"] = f"Login failed: {login_resp.status_code} - {login_resp.text}"
            result["steps"]["login"] = "FAIL"
            return result

        token = login_resp.json()["access_token"]
        user_data = login_resp.json()["user"]
        result["steps"]["login"] = "PASS"
        result["user_role"] = user_data.get("role")
        result["user_name"] = user_data.get("name")

        # Step 2: Test role-specific endpoint access
        headers = {"Authorization": f"Bearer {token}"}

        if role == "student":
            # Test: Get my applications
            resp = requests.get(f"{BASE_URL}/api/applications/", headers=headers)
            if resp.status_code == 200:
                result["steps"]["list_applications"] = "PASS"
                result["application_count"] = len(resp.json().get("results", []))
            else:
                result["steps"]["list_applications"] = "FAIL"
                result["error"] = f"List applications failed: {resp.status_code}"

        elif role == "counselor":
            # Test: Get pending approvals
            resp = requests.get(f"{BASE_URL}/api/approvals/pending/", headers=headers)
            if resp.status_code == 200:
                result["steps"]["list_pending_approvals"] = "PASS"
                result["pending_count"] = len(resp.json().get("results", []))
            else:
                result["steps"]["list_pending_approvals"] = "FAIL"
                result["error"] = f"List approvals failed: {resp.status_code}"

        elif role == "dorm_manager":
            # Test: Get pending approvals
            resp = requests.get(f"{BASE_URL}/api/approvals/pending/", headers=headers)
            if resp.status_code == 200:
                result["steps"]["list_pending_approvals"] = "PASS"
                result["pending_count"] = len(resp.json().get("results", []))
            else:
                result["steps"]["list_pending_approvals"] = "FAIL"
                result["error"] = f"List approvals failed: {resp.status_code}"

        elif role == "academic_staff":
            # Test: Get pending approvals
            resp = requests.get(f"{BASE_URL}/api/approvals/pending/", headers=headers)
            if resp.status_code == 200:
                result["steps"]["list_pending_approvals"] = "PASS"
                result["pending_count"] = len(resp.json().get("results", []))
            else:
                result["steps"]["list_pending_approvals"] = "FAIL"
                result["error"] = f"List approvals failed: {resp.status_code}"

        elif role == "admin":
            # Test: Get all applications
            resp = requests.get(f"{BASE_URL}/api/applications/", headers=headers)
            if resp.status_code == 200:
                result["steps"]["list_all_applications"] = "PASS"
                result["application_count"] = len(resp.json().get("results", []))
            else:
                result["steps"]["list_all_applications"] = "FAIL"
                result["error"] = f"List applications failed: {resp.status_code}"

        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result

print("=== Multi-Role Workflow Test - 5 Rounds ===")
print(f"Start time: {datetime.now().isoformat()}")
print()

# Run tests for each role
for i, (role, user_info) in enumerate(TEST_USERS.items(), 1):
    print(f"Round {i}: Testing {role} - {user_info['user_id']}")
    result = test_role_login(role, user_info["user_id"], user_info["password"])
    results.append(result)

    if result["success"]:
        print(f"  ✓ SUCCESS - {result.get('user_name', 'Unknown')}")
    else:
        print(f"  ✗ FAILED - {result['error']}")
    print()

# Summary
print("=== Test Summary ===")
passed = sum(1 for r in results if r["success"])
failed = len(results) - passed
print(f"Total: {len(results)}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print()

# Detailed results
print("=== Detailed Results ===")
for i, r in enumerate(results, 1):
    print(f"Round {i}: {r['role']} - {r.get('user_id', 'N/A')}")
    if r.get("user_name"):
        print(f"  User: {r['user_name']} (role={r.get('user_role')})")
    for step, status in r["steps"].items():
        print(f"  {step}: {status}")
    if r.get("application_count") is not None:
        print(f"  Applications: {r['application_count']}")
    if r.get("pending_count") is not None:
        print(f"  Pending approvals: {r['pending_count']}")
    if r.get("error"):
        print(f"  Error: {r['error']}")
    print()

# Save to file
with open("/tmp/multi_role_test_report.json", "w") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {"total": len(results), "passed": passed, "failed": failed}
    }, f, indent=2, ensure_ascii=False)

print(f"Report saved to /tmp/multi_role_test_report.json")
