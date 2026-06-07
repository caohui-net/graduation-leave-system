from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import ApprovalDecision, ApprovalStep


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
            graduation_year=2024,
            building='1号楼',
            department='计算机学院'
        )

        self.counselor = User.objects.create_user(
            user_id='T001',
            password='T001',
            name='李老师',
            role=UserRole.COUNSELOR,
            department='计算机学院'
        )

        self.dorm_manager = User.objects.create_user(
            user_id='M001',
            password='M001',
            name='宿管员',
            role=UserRole.DORM_MANAGER,
            building='1号楼'
        )

        # Create class mapping
        ClassMapping.objects.create(
            class_id='CS2020-01',
            dorm_manager=self.dorm_manager,
            dorm_manager_name='宿管员',
            counselor=self.counselor,
            counselor_name='李老师',
            active=True
        )

    def _submit_application(self):
        # Student login and submit
        response = self.client.post('/api/auth/login', {
            'user_id': '2020001',
            'password': '2020001'
        })
        student_token = response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.post('/api/applications/', {
            'contact_phone': '13800138000',
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['application_id']

    def _approve_dorm_manager_step(self, application):
        response = self.client.post('/api/auth/login', {
            'user_id': 'M001',
            'password': 'M001'
        })
        dorm_manager_token = response.data['access_token']

        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dorm_manager_token}')
        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/approve/', {
            'comment': '宿舍清退通过'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dorm_manager_rejection(self):
        """测试宿管员驳回申请"""
        application_id = self._submit_application()

        response = self.client.post('/api/auth/login', {
            'user_id': 'M001',
            'password': 'M001'
        })
        dorm_manager_token = response.data['access_token']

        application = Application.objects.get(application_id=application_id)
        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dorm_manager_token}')
        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/reject/', {
            'comment': '宿舍清退未完成'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)

        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.REJECTED)

    def test_counselor_rejection(self):
        """测试辅导员驳回申请"""
        application_id = self._submit_application()
        application = Application.objects.get(application_id=application_id)
        self._approve_dorm_manager_step(application)

        # Counselor login and reject
        response = self.client.post('/api/auth/login', {
            'user_id': 'T001',
            'password': 'T001'
        })
        counselor_token = response.data['access_token']

        application.refresh_from_db()
        counselor_approval = application.approvals.get(step=ApprovalStep.COUNSELOR)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {counselor_token}')
        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/reject/', {
            'comment': '材料不齐全'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)

        # Verify application status
        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.REJECTED)
