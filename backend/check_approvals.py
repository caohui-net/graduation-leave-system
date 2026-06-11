#!/usr/bin/env python3
"""查询已审批的Application和Approval详情"""
import os
import sys
import django

# Add backend directory to path
sys.path.insert(0, '/home/caohui/projects/graduation-leave-system/backend')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.applications.models import Application
from apps.approvals.models import Approval

print("=== 已审批的Application详情 ===\n")

approved_apps = Application.objects.filter(status='approved').order_by('created_at')

print(f"总数: {approved_apps.count()}条\n")

for app in approved_apps:
    print(f"申请ID: {app.application_id}")
    print(f"学生: {app.student_name} ({app.student_id})")
    print(f"状态: {app.status}")

    # 查询关联的审批记录
    approvals = Approval.objects.filter(application_id=app.application_id).order_by('created_at')
    print(f"审批记录数: {approvals.count()}")

    for approval in approvals:
        print(f"  - {approval.step}: {approval.decision} (审批人: {approval.approver_name})")

    print("-" * 60)

print("\n=== Approval记录统计 ===")
print(f"Total Approvals: {Approval.objects.count()}")
print(f"Pending: {Approval.objects.filter(decision='pending').count()}")
print(f"Approved: {Approval.objects.filter(decision='approved').count()}")
print(f"Rejected: {Approval.objects.filter(decision='rejected').count()}")
