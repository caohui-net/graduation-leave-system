from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalDecision


class ApplicationFlowTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.student = User.objects.create_user(
            user_id='2020001',
            password='2020001',
            name='张三',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            is_graduating=True,
            graduation_year=2024
        )

        self.counselor = User.objects.create_user(
            user_id='T001',
            password='T001',
            name='李老师',
            role=UserRole.COUNSELOR
        )

        self.dean = User.objects.create_user(
            user_id='D001',
            password='D001',
            name='赵主任',
            role=UserRole.DEAN
        )

    def test_complete_application_flow(self):
        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""

        # Step 1: 学生登录
        response = self.client.post('/api/auth/login/', {
            'user_id': '2020001',
            'password': '2020001'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        student_token = response.data['access_token']

        # Step 2: 学生提交申请
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.post('/api/applications/', {
            'reason': '毕业离校',
            'leave_date': '2024-06-30'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], ApplicationStatus.PENDING_COUNSELOR)
        application_id = response.data['application_id']

        # Step 3: 辅导员登录
        response = self.client.post('/api/auth/login/', {
            'user_id': 'T001',
            'password': 'T001'
        })
        counselor_token = response.data['access_token']

        # Step 4: 辅导员审批通过
        application = Application.objects.get(application_id=application_id)
        counselor_approval = application.approvals.filter(step='counselor').first()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {counselor_token}')
        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/approve/', {
            'comment': '同意离校'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)

        # Step 5: 学工部登录
        response = self.client.post('/api/auth/login/', {
            'user_id': 'D001',
            'password': 'D001'
        })
        dean_token = response.data['access_token']

        # Step 6: 学工部审批通过
        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.PENDING_DEAN)
        dean_approval = application.approvals.filter(step='dean').first()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dean_token}')
        response = self.client.post(f'/api/approvals/{dean_approval.approval_id}/approve/', {
            'comment': '同意离校'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Step 7: 查询申请状态
        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.APPROVED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.get(f'/api/applications/{application_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], ApplicationStatus.APPROVED)
        self.assertEqual(len(response.data['approvals']), 2)
