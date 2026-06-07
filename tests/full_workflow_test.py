#!/usr/bin/env python3
"""
Full Workflow Test Script
Tests complete application submission and approval flow
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8001"
TEST_STUDENTS = [
    "2022240340415",  # 邱君祎 - 化学化工学院
    "2022190140302",  # 汪晓蔓 - 旅游文化与地理科学学院
    "2022190140325",  # 张家祥 - 旅游文化与地理科学学院
    "2022250140422",  # 熊仁祥 - 体育学院
    "2022250140610",  # 李冠杰 - 体育学院
]

results = []

def test_workflow(student_id):
    """Test full workflow for one student"""
    result = {
        "student_id": student_id,
        "steps": {},
        "success": False,
        "error": None
    }

    try:
        # Step 1: Login
        login_resp = requests.post(f"{BASE_URL}/api/auth/login", json={
            "user_id": student_id,
            "password": "password123"
        })

        if login_resp.status_code != 200:
            result["error"] = f"Login failed: {login_resp.status_code}"
            result["steps"]["login"] = "FAIL"
            return result

        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        result["steps"]["login"] = "PASS"

        # Step 2: Create application
        leave_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        app_data = {
            "contact_phone": "13800138000",
            "reason": "测试离校申请",
            "leave_date": leave_date
        }

        app_resp = requests.post(
            f"{BASE_URL}/api/applications/",
            json=app_data,
            headers=headers
        )

        if app_resp.status_code not in [200, 201]:
            result["error"] = f"Application creation failed: {app_resp.status_code} - {app_resp.text}"
            result["steps"]["create_application"] = "FAIL"
            return result

        app_id = app_resp.json()["application_id"]
        result["application_id"] = app_id
        result["steps"]["create_application"] = "PASS"

        # Step 3: Check application status
        detail_resp = requests.get(
            f"{BASE_URL}/api/applications/{app_id}/",
            headers=headers
        )

        if detail_resp.status_code != 200:
            result["error"] = f"Get application failed: {detail_resp.status_code}"
            result["steps"]["check_status"] = "FAIL"
            return result

        status = detail_resp.json()["status"]
        result["status"] = status
        result["steps"]["check_status"] = "PASS"
        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result

print("=== Full Workflow Test - 5 Rounds ===")
print(f"Start time: {datetime.now().isoformat()}")
print()

for i, student_id in enumerate(TEST_STUDENTS, 1):
    print(f"Round {i}: Testing student {student_id}")
    result = test_workflow(student_id)
    results.append(result)

    if result["success"]:
        print(f"  ✓ SUCCESS - Application {result.get('application_id')} created")
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
    print(f"Round {i}: {r['student_id']}")
    for step, status in r["steps"].items():
        print(f"  {step}: {status}")
    if r.get("application_id"):
        print(f"  Application ID: {r['application_id']}")
    if r.get("error"):
        print(f"  Error: {r['error']}")
    print()

# Save to file
with open("/tmp/workflow_test_report.json", "w") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {"total": len(results), "passed": passed, "failed": failed}
    }, f, indent=2, ensure_ascii=False)

print(f"Report saved to /tmp/workflow_test_report.json")
