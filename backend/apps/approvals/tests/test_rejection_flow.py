from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import ApprovalDecision


class RejectionFlowTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

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

        # Create class mapping
        ClassMapping.objects.create(
            class_id='CS2020-01',
            counselor=self.counselor,
            counselor_name='李老师',
            active=True
        )

    def test_counselor_rejection(self):
        """测试辅导员驳回申请"""
        # Student login and submit
        response = self.client.post('/api/auth/login', {
            'user_id': '2020001',
            'password': '2020001'
        })
        student_token = response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.post('/api/applications/', {
            'reason': '毕业离校',
            'leave_date': '2024-06-30'
        })
        application_id = response.data['application_id']

        # Counselor login and reject
        response = self.client.post('/api/auth/login', {
            'user_id': 'T001',
            'password': 'T001'
        })
        counselor_token = response.data['access_token']

        application = Application.objects.get(application_id=application_id)
        counselor_approval = application.approvals.filter(step='counselor').first()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {counselor_token}')
        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/reject/', {
            'comment': '材料不齐全'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)

        # Verify application status
        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.REJECTED)

    def test_dean_rejection(self):
        """测试学工部驳回申请"""
        # Student login and submit
        response = self.client.post('/api/auth/login', {
            'user_id': '2020001',
            'password': '2020001'
        })
        student_token = response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.post('/api/applications/', {
            'reason': '毕业离校',
            'leave_date': '2024-06-30'
        })
        application_id = response.data['application_id']

        # Counselor approve
        response = self.client.post('/api/auth/login', {
            'user_id': 'T001',
            'password': 'T001'
        })
        counselor_token = response.data['access_token']

        application = Application.objects.get(application_id=application_id)
        counselor_approval = application.approvals.filter(step='counselor').first()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {counselor_token}')
        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/approve/', {
            'comment': '同意'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Dean login and reject
        response = self.client.post('/api/auth/login', {
            'user_id': 'D001',
            'password': 'D001'
        })
        dean_token = response.data['access_token']

        application.refresh_from_db()
        dean_approval = application.approvals.filter(step='dean').first()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dean_token}')
        response = self.client.post(f'/api/approvals/{dean_approval.approval_id}/reject/', {
            'comment': '不符合离校条件'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)

        # Verify application status
        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.REJECTED)
