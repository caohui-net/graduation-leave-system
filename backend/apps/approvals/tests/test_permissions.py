from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.users.class_mapping import ClassMapping
import uuid


class ApprovalPermissionsTestCase(TestCase):
    def setUp(self):
        # Create students
        self.student1 = User.objects.create_user(
            user_id='2020001',
            name='张三',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            password='2020001'
        )
        self.student2 = User.objects.create_user(
            user_id='2020002',
            name='李四',
            role=UserRole.STUDENT,
            class_id='CS2020-02',
            password='2020002'
        )

        # Create counselors
        self.counselor1 = User.objects.create_user(
            user_id='T001',
            name='李老师',
            role=UserRole.COUNSELOR,
            password='T001'
        )
        self.counselor2 = User.objects.create_user(
            user_id='T002',
            name='王老师',
            role=UserRole.COUNSELOR,
            password='T002'
        )

        # Create class mappings
        ClassMapping.objects.create(
            class_id='CS2020-01',
            counselor=self.counselor1,
            counselor_name='李老师',
            active=True
        )
        ClassMapping.objects.create(
            class_id='CS2020-02',
            counselor=self.counselor2,
            counselor_name='王老师',
            active=True
        )

        # Create application for student1
        self.application1 = Application.objects.create(
            application_id='app_test001',
            student=self.student1,
            student_name='张三',
            class_id='CS2020-01',
            reason='测试原因',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        # Create counselor approval for application1
        self.approval1 = Approval.objects.create(
            approval_id='apv_test001',
            application=self.application1,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor1,
            approver_name='李老师',
            decision=ApprovalDecision.PENDING
        )

        self.client = APIClient()

    def test_cross_counselor_approve_forbidden(self):
        """测试跨辅导员审批返回403"""
        # T002 tries to approve T001's application
        self.client.force_authenticate(user=self.counselor2)
        response = self.client.post(
            f'/api/approvals/{self.approval1.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cross_counselor_reject_forbidden(self):
        """测试跨辅导员驳回返回403"""
        # T002 tries to reject T001's application
        self.client.force_authenticate(user=self.counselor2)
        response = self.client.post(
            f'/api/approvals/{self.approval1.approval_id}/reject/',
            {'comment': '不同意'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
