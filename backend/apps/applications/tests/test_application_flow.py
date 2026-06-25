from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import ApprovalDecision, ApprovalStep


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
            graduation_year=2024,
            building='1号楼',
            department='计算机学院'
        )

        self.counselor = User.objects.create_user(
            user_id='T001',
            password='T001',
            name='李老师',
            role=UserRole.COUNSELOR,
            class_id='CS2020-01',
            department='计算机学院'
        )

        self.dorm_manager = User.objects.create_user(
            user_id='M001',
            password='M001',
            name='宿管员',
            role=UserRole.DORM_MANAGER,
            building='1号楼'
        )

        self.dean = User.objects.create_user(
            user_id='D001',
            password='D001',
            name='赵主任',
            role=UserRole.DEAN
        )

    def test_complete_application_flow(self):
        """测试完整的申请流程：登录→提交→宿管员审批→辅导员审批→学工部归档查询"""

        # Step 1: 学生登录
        response = self.client.post('/api/auth/login', {
            'user_id': '2020001',
            'password': '2020001'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        student_token = response.data['access_token']

        # Step 2: 学生提交申请
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.post('/api/applications/', {
            'contact_phone': '13800138000',
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], ApplicationStatus.PENDING_DORM_MANAGER)
        application_id = response.data['application_id']

        # Step 3: 宿管员登录
        response = self.client.post('/api/auth/login', {
            'user_id': 'M001',
            'password': 'M001'
        }, format='json')
        dorm_manager_token = response.data['access_token']

        # Step 4: 宿管员审批通过
        application = Application.objects.get(application_id=application_id)
        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dorm_manager_token}')
        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/approve/', {
            'comment': '宿舍清退通过'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)

        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.PENDING_COUNSELOR)

        # Step 5: 辅导员登录
        response = self.client.post('/api/auth/login', {
            'user_id': 'T001',
            'password': 'T001'
        }, format='json')
        counselor_token = response.data['access_token']

        # Step 6: 辅导员审批通过
        counselor_approval = application.approvals.get(step=ApprovalStep.COUNSELOR)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {counselor_token}')
        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/approve/', {
            'comment': '同意离校'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)

        # Step 7: 查询申请状态 - 辅导员审批后直接完成（2级审批）
        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.APPROVED)

        # Step 8: 最终状态查询
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.get(f'/api/applications/{application_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], ApplicationStatus.APPROVED)
        self.assertEqual(len(response.data['approvals']), 2)  # 2-level approval
