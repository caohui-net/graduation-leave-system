#!/usr/bin/env python3
"""
创建申请并跳过宿管员审批，直接进入辅导员审批
用法: python scripts/create_application_skip_dorm.py <student_id> <contact_phone> <leave_date> [reason]
"""
import sys
import os
import django
import uuid
from datetime import datetime

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import transaction
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus, DormCheckoutStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision

def create_application_skip_dorm(student_id, contact_phone, leave_date, reason=''):
    with transaction.atomic():
        # Get student
        try:
            student = User.objects.select_for_update().get(user_id=student_id, role=UserRole.STUDENT)
        except User.DoesNotExist:
            print(f"错误: 学生 {student_id} 不存在")
            return False

        # Check existing applications
        existing = Application.objects.filter(
            student=student,
            status__in=[ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.APPROVED]
        ).first()
        if existing:
            print(f"错误: 学生已有待审批或已通过的申请 (application_id={existing.application_id})")
            return False

        # Find counselor by department
        counselor = User.objects.filter(
            role=UserRole.COUNSELOR,
            department=student.department,
            active=True
        ).order_by('user_id').first()

        if not counselor:
            print(f"错误: 找不到学院 {student.department} 的辅导员")
            return False

        # Create application (directly to counselor)
        application = Application.objects.create(
            application_id=f'app_{uuid.uuid4().hex[:8]}',
            student=student,
            student_name=student.name,
            class_id=student.class_id,
            contact_phone=contact_phone,
            reason=reason,
            leave_date=leave_date,
            status=ApplicationStatus.PENDING_COUNSELOR,
            dorm_checkout_status=DormCheckoutStatus.COMPLETED
        )

        # Create counselor approval (skip dorm manager)
        approval = Approval.objects.create(
            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=counselor,
            approver_name=counselor.name,
            decision=ApprovalDecision.PENDING
        )

        print(f"✓ 申请创建成功")
        print(f"  application_id: {application.application_id}")
        print(f"  学生: {student.name} ({student.user_id})")
        print(f"  状态: {application.status}")
        print(f"  辅导员: {counselor.name} ({counselor.user_id})")
        print(f"  审批ID: {approval.approval_id}")

        return True

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("用法: python scripts/create_application_skip_dorm.py <student_id> <contact_phone> <leave_date> [reason]")
        print("示例: python scripts/create_application_skip_dorm.py 2022200140134 15997263657 2026-07-16 '特殊申请'")
        sys.exit(1)

    student_id = sys.argv[1]
    contact_phone = sys.argv[2]
    leave_date = sys.argv[3]
    reason = sys.argv[4] if len(sys.argv) > 4 else ''

    success = create_application_skip_dorm(student_id, contact_phone, leave_date, reason)
    sys.exit(0 if success else 1)
