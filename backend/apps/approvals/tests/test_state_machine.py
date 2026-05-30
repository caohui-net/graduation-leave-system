from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.users.class_mapping import ClassMapping


class ApprovalStateMachineTestCase(TestCase):
    def setUp(self):
        # Create student
        self.student = User.objects.create_user(
            user_id='2020001',
            name='张三',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            password='2020001'
        )

        # Create counselor
        self.counselor = User.objects.create_user(
            user_id='T001',
            name='李老师',
            role=UserRole.COUNSELOR,
            password='T001'
        )

        # Create dean
        self.dean = User.objects.create_user(
            user_id='D001',
            name='赵主任',
            role=UserRole.DEAN,
            password='D001'
        )

        # Create class mapping
        ClassMapping.objects.create(
            class_id='CS2020-01',
            counselor=self.counselor,
            counselor_name='李老师',
            active=True
        )

        # Create application
        self.application = Application.objects.create(
            application_id='app_test001',
            student=self.student,
            student_name='张三',
            class_id='CS2020-01',
            reason='测试原因',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        # Create counselor approval
        self.approval = Approval.objects.create(
            approval_id='apv_test001',
            application=self.application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name='李老师',
            decision=ApprovalDecision.PENDING
        )

        self.client = APIClient()

    def test_duplicate_approval_conflict(self):
        """测试重复审批返回409"""
        self.client.force_authenticate(user=self.counselor)

        # First approval
        response1 = self.client.post(
            f'/api/approvals/{self.approval.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        # Second approval attempt
        response2 = self.client.post(
            f'/api/approvals/{self.approval.approval_id}/approve/',
            {'comment': '再次同意'},
            format='json'
        )
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
