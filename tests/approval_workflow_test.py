#!/usr/bin/env python3
"""
Complete Approval Workflow Test - P1 Priority
Tests full end-to-end approval process from submission to final status
"""
import requests
import json
import subprocess
from datetime import datetime, date

BASE_URL = "http://localhost:8001"

# Test users (matching building and department)
# Student: 物理与电信学院, 荷园6栋
# Dorm Manager: 荷园6栋
# Counselor: 物理与电信学院
STUDENT = {"user_id": "2022220040109", "password": "password123"}
DORM_MANAGER = {"user_id": "92001364", "password": "password123"}
COUNSELOR = {"user_id": "20220052", "password": "password123"}
STUDENT_B = {"user_id": "2022220040203", "password": "password123"}  # Also 荷园6栋

results = []


def cleanup_test_data():
    """Clean up test applications to enable repeatable test runs"""
    print("Cleaning up test data...")
    cleanup_cmd = """
from apps.applications.models import Application
from apps.approvals.models import Approval
for sid in ['2022220040109', '2022220040203']:
    Approval.objects.filter(application__student_id=sid).delete()
    Application.objects.filter(student_id=sid).delete()
print('Test data cleaned')
"""
    try:
        subprocess.run(
            ["docker", "exec", "graduation-leave-system-backend-1",
             "python", "manage.py", "shell", "-c", cleanup_cmd],
            check=True, capture_output=True, text=True
        )
        print("  ✓ Test data cleanup successful")
    except subprocess.CalledProcessError as e:
        print(f"  ⚠ Cleanup failed (non-fatal): {e.stderr}")


def login(user_id, password):
    """Login and return token"""
    resp = requests.post(f"{BASE_URL}/api/auth/login", json={
        "user_id": user_id,
        "password": password
    })
    if resp.status_code == 200:
        return resp.json()["access_token"]
    raise Exception(f"Login failed: {resp.status_code} - {resp.text}")


def test_complete_approval_workflow():
    """
    Test Scenario 1: Complete approval workflow (Happy Path)
    Student submit → Dorm manager approve → Counselor approve → Status=approved
    """
    result = {
        "scenario": "Complete Approval Workflow (Happy Path)",
        "steps": {},
        "success": False,
        "error": None
    }

    try:
        # Step 1: Student login and submit application
        student_token = login(STUDENT["user_id"], STUDENT["password"])
        result["steps"]["student_login"] = "PASS"

        # Submit application
        headers = {"Authorization": f"Bearer {student_token}"}
        submit_resp = requests.post(f"{BASE_URL}/api/applications/", headers=headers, json={
            "contact_phone": "13800138000",
            "reason": "测试完整审批流程",
            "leave_date": str(date.today())
        })

        if submit_resp.status_code != 201:
            result["steps"]["submit_application"] = "FAIL"
            result["error"] = f"Submit failed: {submit_resp.status_code} - {submit_resp.text}"
            return result

        app_data = submit_resp.json()
        app_id = app_data["application_id"]
        result["steps"]["submit_application"] = "PASS"
        result["application_id"] = app_id

        # Verify initial status
        if app_data["status"] != "pending_dorm_manager":
            result["steps"]["initial_status"] = "FAIL"
            result["error"] = f"Expected pending_dorm_manager, got {app_data['status']}"
            return result
        result["steps"]["initial_status"] = "PASS"

        # Step 2: Dorm manager login and approve
        dorm_token = login(DORM_MANAGER["user_id"], DORM_MANAGER["password"])
        result["steps"]["dorm_login"] = "PASS"

        # Get pending approvals
        headers = {"Authorization": f"Bearer {dorm_token}"}
        approvals_resp = requests.get(f"{BASE_URL}/api/approvals/", headers=headers)

        if approvals_resp.status_code != 200:
            result["steps"]["get_dorm_approvals"] = "FAIL"
            result["error"] = f"Get approvals failed: {approvals_resp.status_code}"
            return result

        approvals = approvals_resp.json()["results"]
        dorm_approval = next((a for a in approvals if a["application_id"] == app_id), None)

        if not dorm_approval:
            result["steps"]["get_dorm_approvals"] = "FAIL"
            result["error"] = "Dorm manager approval not found"
            return result
        result["steps"]["get_dorm_approvals"] = "PASS"
        result["dorm_approval_id"] = dorm_approval["approval_id"]

        # Approve as dorm manager
        approve_resp = requests.post(
            f"{BASE_URL}/api/approvals/{dorm_approval['approval_id']}/approve/",
            headers=headers,
            json={"comment": "宿管审批通过"}
        )

        if approve_resp.status_code != 200:
            result["steps"]["dorm_approve"] = "FAIL"
            result["error"] = f"Dorm approval failed: {approve_resp.status_code} - {approve_resp.text}"
            return result
        result["steps"]["dorm_approve"] = "PASS"

        # Verify status changed to pending_counselor
        app_resp = requests.get(f"{BASE_URL}/api/applications/{app_id}/", headers={"Authorization": f"Bearer {student_token}"})
        if app_resp.json()["status"] != "pending_counselor":
            result["steps"]["status_after_dorm"] = "FAIL"
            result["error"] = f"Expected pending_counselor, got {app_resp.json()['status']}"
            return result
        result["steps"]["status_after_dorm"] = "PASS"

        # Step 3: Counselor login and approve
        counselor_token = login(COUNSELOR["user_id"], COUNSELOR["password"])
        result["steps"]["counselor_login"] = "PASS"

        # Get counselor pending approvals
        headers = {"Authorization": f"Bearer {counselor_token}"}
        approvals_resp = requests.get(f"{BASE_URL}/api/approvals/", headers=headers)

        if approvals_resp.status_code != 200:
            result["steps"]["get_counselor_approvals"] = "FAIL"
            result["error"] = f"Get approvals failed: {approvals_resp.status_code}"
            return result

        approvals = approvals_resp.json()["results"]
        counselor_approval = next((a for a in approvals if a["application_id"] == app_id), None)

        if not counselor_approval:
            result["steps"]["get_counselor_approvals"] = "FAIL"
            result["error"] = "Counselor approval not found"
            return result
        result["steps"]["get_counselor_approvals"] = "PASS"
        result["counselor_approval_id"] = counselor_approval["approval_id"]

        # Approve as counselor
        approve_resp = requests.post(
            f"{BASE_URL}/api/approvals/{counselor_approval['approval_id']}/approve/",
            headers=headers,
            json={"comment": "辅导员审批通过"}
        )

        if approve_resp.status_code != 200:
            result["steps"]["counselor_approve"] = "FAIL"
            result["error"] = f"Counselor approval failed: {approve_resp.status_code} - {approve_resp.text}"
            return result
        result["steps"]["counselor_approve"] = "PASS"

        # Verify final status is approved
        app_resp = requests.get(f"{BASE_URL}/api/applications/{app_id}/", headers={"Authorization": f"Bearer {student_token}"})
        if app_resp.json()["status"] != "approved":
            result["steps"]["final_status"] = "FAIL"
            result["error"] = f"Expected approved, got {app_resp.json()['status']}"
            return result
        result["steps"]["final_status"] = "PASS"

        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result


def test_permission_isolation():
    """
    Test Scenario 2: Permission isolation
    Student B cannot approve Student A's application
    """
    result = {
        "scenario": "Permission Isolation",
        "steps": {},
        "success": False,
        "error": None
    }

    try:
        # Step 1: Student B submits application
        student_b_token = login(STUDENT_B["user_id"], STUDENT_B["password"])
        result["steps"]["student_b_login"] = "PASS"

        headers = {"Authorization": f"Bearer {student_b_token}"}
        submit_resp = requests.post(f"{BASE_URL}/api/applications/", headers=headers, json={
            "contact_phone": "13800138002",
            "reason": "测试权限隔离",
            "leave_date": str(date.today())
        })

        if submit_resp.status_code != 201:
            result["steps"]["submit_application"] = "FAIL"
            result["error"] = f"Submit failed: {submit_resp.status_code}"
            return result

        app_id = submit_resp.json()["application_id"]
        result["steps"]["submit_application"] = "PASS"
        result["application_id"] = app_id

        # Step 2: Get dorm approval ID for Student B's application
        dorm_token = login(DORM_MANAGER["user_id"], DORM_MANAGER["password"])
        headers = {"Authorization": f"Bearer {dorm_token}"}
        approvals_resp = requests.get(f"{BASE_URL}/api/approvals/", headers=headers)
        approvals = approvals_resp.json()["results"]
        dorm_approval = next((a for a in approvals if a["application_id"] == app_id), None)

        if not dorm_approval:
            result["steps"]["get_approval_id"] = "FAIL"
            result["error"] = "Approval not found"
            return result
        result["steps"]["get_approval_id"] = "PASS"
        approval_id = dorm_approval["approval_id"]

        # Step 3: Student A tries to approve Student B's application (should fail with 403)
        student_a_token = login(STUDENT["user_id"], STUDENT["password"])
        result["steps"]["student_a_login"] = "PASS"

        headers = {"Authorization": f"Bearer {student_a_token}"}
        approve_resp = requests.post(
            f"{BASE_URL}/api/approvals/{approval_id}/approve/",
            headers=headers,
            json={"comment": "尝试非法审批"}
        )

        # Should return 403 Forbidden
        if approve_resp.status_code == 403:
            result["steps"]["permission_denied"] = "PASS"
            result["success"] = True
        else:
            result["steps"]["permission_denied"] = "FAIL"
            result["error"] = f"Expected 403, got {approve_resp.status_code}"

    except Exception as e:
        result["error"] = str(e)

    return result


def test_dorm_manager_rejection():
    """
    Test Scenario 3: Dorm manager rejection path
    Student submit → Dorm manager reject → Status=rejected
    """
    result = {
        "scenario": "Dorm Manager Rejection Path",
        "steps": {},
        "success": False,
        "error": None
    }

    try:
        # Cleanup this student's existing applications first
        cleanup_cmd = f"""
from apps.applications.models import Application
from apps.approvals.models import Approval
Approval.objects.filter(application__student_id='{STUDENT["user_id"]}').delete()
Application.objects.filter(student_id='{STUDENT["user_id"]}').delete()
"""
        subprocess.run(
            ["docker", "exec", "graduation-leave-system-backend-1",
             "python", "manage.py", "shell", "-c", cleanup_cmd],
            check=True, capture_output=True, text=True
        )

        # Step 1: Student login and submit application
        student_token = login(STUDENT["user_id"], STUDENT["password"])
        result["steps"]["student_login"] = "PASS"

        headers = {"Authorization": f"Bearer {student_token}"}
        submit_resp = requests.post(f"{BASE_URL}/api/applications/", headers=headers, json={
            "contact_phone": "13800138000",
            "reason": "测试宿管拒绝路径",
            "leave_date": str(date.today())
        })

        if submit_resp.status_code != 201:
            result["steps"]["submit_application"] = "FAIL"
            result["error"] = f"Submit failed: {submit_resp.status_code}"
            return result

        app_data = submit_resp.json()
        app_id = app_data["application_id"]
        result["steps"]["submit_application"] = "PASS"
        result["application_id"] = app_id

        # Step 2: Dorm manager login and get pending approval
        dorm_token = login(DORM_MANAGER["user_id"], DORM_MANAGER["password"])
        result["steps"]["dorm_login"] = "PASS"

        headers = {"Authorization": f"Bearer {dorm_token}"}
        approvals_resp = requests.get(f"{BASE_URL}/api/approvals/", headers=headers)

        if approvals_resp.status_code != 200:
            result["steps"]["get_dorm_approvals"] = "FAIL"
            result["error"] = f"Get approvals failed: {approvals_resp.status_code}"
            return result

        approvals = approvals_resp.json()["results"]
        dorm_approval = next((a for a in approvals if a["application_id"] == app_id), None)

        if not dorm_approval:
            result["steps"]["get_dorm_approvals"] = "FAIL"
            result["error"] = "Dorm manager approval not found"
            return result
        result["steps"]["get_dorm_approvals"] = "PASS"

        # Step 3: Reject as dorm manager
        reject_resp = requests.post(
            f"{BASE_URL}/api/approvals/{dorm_approval['approval_id']}/reject/",
            headers=headers,
            json={"comment": "宿管拒绝测试"}
        )

        if reject_resp.status_code != 200:
            result["steps"]["dorm_reject"] = "FAIL"
            result["error"] = f"Dorm rejection failed: {reject_resp.status_code} - {reject_resp.text}"
            return result
        result["steps"]["dorm_reject"] = "PASS"

        # Step 4: Verify final status is rejected
        app_resp = requests.get(f"{BASE_URL}/api/applications/{app_id}/", headers={"Authorization": f"Bearer {student_token}"})
        if app_resp.json()["status"] != "rejected":
            result["steps"]["final_status"] = "FAIL"
            result["error"] = f"Expected rejected, got {app_resp.json()['status']}"
            return result
        result["steps"]["final_status"] = "PASS"

        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result


def test_counselor_rejection():
    """
    Test Scenario 4: Counselor rejection path
    Student submit → Dorm manager approve → Counselor reject → Status=rejected
    """
    result = {
        "scenario": "Counselor Rejection Path",
        "steps": {},
        "success": False,
        "error": None
    }

    try:
        # Cleanup this student's existing applications first
        cleanup_cmd = f"""
from apps.applications.models import Application
from apps.approvals.models import Approval
Approval.objects.filter(application__student_id='{STUDENT_B["user_id"]}').delete()
Application.objects.filter(student_id='{STUDENT_B["user_id"]}').delete()
"""
        subprocess.run(
            ["docker", "exec", "graduation-leave-system-backend-1",
             "python", "manage.py", "shell", "-c", cleanup_cmd],
            check=True, capture_output=True, text=True
        )

        # Step 1: Student login and submit application
        student_token = login(STUDENT_B["user_id"], STUDENT_B["password"])
        result["steps"]["student_login"] = "PASS"

        headers = {"Authorization": f"Bearer {student_token}"}
        submit_resp = requests.post(f"{BASE_URL}/api/applications/", headers=headers, json={
            "contact_phone": "13800138002",
            "reason": "测试辅导员拒绝路径",
            "leave_date": str(date.today())
        })

        if submit_resp.status_code != 201:
            result["steps"]["submit_application"] = "FAIL"
            result["error"] = f"Submit failed: {submit_resp.status_code}"
            return result

        app_data = submit_resp.json()
        app_id = app_data["application_id"]
        result["steps"]["submit_application"] = "PASS"
        result["application_id"] = app_id

        # Step 2: Dorm manager approve first
        dorm_token = login(DORM_MANAGER["user_id"], DORM_MANAGER["password"])
        result["steps"]["dorm_login"] = "PASS"

        headers = {"Authorization": f"Bearer {dorm_token}"}
        approvals_resp = requests.get(f"{BASE_URL}/api/approvals/", headers=headers)
        approvals = approvals_resp.json()["results"]
        dorm_approval = next((a for a in approvals if a["application_id"] == app_id), None)

        if not dorm_approval:
            result["steps"]["get_dorm_approvals"] = "FAIL"
            result["error"] = "Dorm approval not found"
            return result
        result["steps"]["get_dorm_approvals"] = "PASS"

        approve_resp = requests.post(
            f"{BASE_URL}/api/approvals/{dorm_approval['approval_id']}/approve/",
            headers=headers,
            json={"comment": "宿管通过"}
        )

        if approve_resp.status_code != 200:
            result["steps"]["dorm_approve"] = "FAIL"
            result["error"] = f"Dorm approval failed: {approve_resp.status_code}"
            return result
        result["steps"]["dorm_approve"] = "PASS"

        # Step 3: Counselor login and reject
        counselor_token = login(COUNSELOR["user_id"], COUNSELOR["password"])
        result["steps"]["counselor_login"] = "PASS"

        headers = {"Authorization": f"Bearer {counselor_token}"}
        approvals_resp = requests.get(f"{BASE_URL}/api/approvals/", headers=headers)

        if approvals_resp.status_code != 200:
            result["steps"]["get_counselor_approvals"] = "FAIL"
            result["error"] = f"Get approvals failed: {approvals_resp.status_code}"
            return result

        approvals = approvals_resp.json()["results"]
        counselor_approval = next((a for a in approvals if a["application_id"] == app_id), None)

        if not counselor_approval:
            result["steps"]["get_counselor_approvals"] = "FAIL"
            result["error"] = "Counselor approval not found"
            return result
        result["steps"]["get_counselor_approvals"] = "PASS"

        reject_resp = requests.post(
            f"{BASE_URL}/api/approvals/{counselor_approval['approval_id']}/reject/",
            headers=headers,
            json={"comment": "辅导员拒绝测试"}
        )

        if reject_resp.status_code != 200:
            result["steps"]["counselor_reject"] = "FAIL"
            result["error"] = f"Counselor rejection failed: {reject_resp.status_code} - {reject_resp.text}"
            return result
        result["steps"]["counselor_reject"] = "PASS"

        # Step 4: Verify final status is rejected
        app_resp = requests.get(f"{BASE_URL}/api/applications/{app_id}/", headers={"Authorization": f"Bearer {student_token}"})
        if app_resp.json()["status"] != "rejected":
            result["steps"]["final_status"] = "FAIL"
            result["error"] = f"Expected rejected, got {app_resp.json()['status']}"
            return result
        result["steps"]["final_status"] = "PASS"

        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result


if __name__ == "__main__":
    print("=== Complete Approval Workflow Test (P1) ===")
    print(f"Start time: {datetime.now().isoformat()}")
    print()

    # Clean up test data to enable repeatable runs
    cleanup_test_data()
    print()

    # Test 1: Complete approval workflow
    print("Test 1: Complete Approval Workflow (Happy Path)")
    result1 = test_complete_approval_workflow()
    results.append(result1)

    if result1["success"]:
        print(f"  ✓ SUCCESS")
        print(f"    Application ID: {result1.get('application_id')}")
        print(f"    All steps passed: {', '.join(result1['steps'].keys())}")
    else:
        print(f"  ✗ FAILED - {result1['error']}")
        print(f"    Steps: {result1['steps']}")
    print()

    # Test 2: Permission isolation
    print("Test 2: Permission Isolation")
    result2 = test_permission_isolation()
    results.append(result2)

    if result2["success"]:
        print(f"  ✓ SUCCESS - Permission isolation verified")
        print(f"    Application ID: {result2.get('application_id')}")
    else:
        print(f"  ✗ FAILED - {result2['error']}")
        print(f"    Steps: {result2['steps']}")
    print()

    # Test 3: Dorm manager rejection
    print("Test 3: Dorm Manager Rejection Path")
    result3 = test_dorm_manager_rejection()
    results.append(result3)

    if result3["success"]:
        print(f"  ✓ SUCCESS - Dorm rejection path verified")
        print(f"    Application ID: {result3.get('application_id')}")
    else:
        print(f"  ✗ FAILED - {result3['error']}")
        print(f"    Steps: {result3['steps']}")
    print()

    # Test 4: Counselor rejection
    print("Test 4: Counselor Rejection Path")
    result4 = test_counselor_rejection()
    results.append(result4)

    if result4["success"]:
        print(f"  ✓ SUCCESS - Counselor rejection path verified")
        print(f"    Application ID: {result4.get('application_id')}")
    else:
        print(f"  ✗ FAILED - {result4['error']}")
        print(f"    Steps: {result4['steps']}")
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
    if failed > 0:
        print("=== Failed Tests Details ===")
        for r in results:
            if not r["success"]:
                print(f"Scenario: {r['scenario']}")
                print(f"  Error: {r['error']}")
                print(f"  Steps: {r['steps']}")
                print()

    # Save report
    with open("/tmp/approval_workflow_test_report.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "summary": {"total": len(results), "passed": passed, "failed": failed}
        }, f, indent=2, ensure_ascii=False)

    print(f"Report saved to /tmp/approval_workflow_test_report.json")
