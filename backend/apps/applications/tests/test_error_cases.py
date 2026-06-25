from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus


class ErrorCasesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.student1 = User.objects.create_user(
            user_id='2020001',
            password='2020001',
            name='张三',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            building='1号楼',
            department='计算机学院',
            is_graduating=True,
            graduation_year=2024
        )

        self.student2 = User.objects.create_user(
            user_id='2020002',
            password='2020002',
            name='李四',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            building='1号楼',
            department='计算机学院',
            is_graduating=True,
            graduation_year=2024
        )

        self.student3 = User.objects.create_user(
            user_id='2020003',
            password='2020003',
            name='王五',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            building='1号楼',
            department='计算机学院',
            is_graduating=True,
            graduation_year=2024
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
            name='学工部',
            role=UserRole.DEAN
        )

    def test_dorm_blocked_error(self):
        """测试宿舍清退未完成阻断提交"""
        response = self.client.post('/api/auth/login', {
            'user_id': '2020003',
            'password': '2020003'
        }, format='json')
        token = response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/applications/', {
            'contact_phone': '13800138000',
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data['error']['code'], 'DORM_BLOCKED')

    def test_conflict_duplicate_application(self):
        """测试重复提交申请"""
        response = self.client.post('/api/auth/login', {
            'user_id': '2020001',
            'password': '2020001'
        })
        token = response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # First submission
        response = self.client.post('/api/applications/', {
            'contact_phone': '13800138000',
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Second submission (should fail)
        response = self.client.post('/api/applications/', {
            'contact_phone': '13800138000',
            'reason': '再次提交',
            'leave_date': (timezone.now().date() + timedelta(days=2)).isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['error']['code'], 'CONFLICT')

    def test_forbidden_access_other_student_application(self):
        """测试学生访问他人申请"""
        # Student1 creates application
        response = self.client.post('/api/auth/login', {
            'user_id': '2020001',
            'password': '2020001'
        })
        token1 = response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token1}')
        response = self.client.post('/api/applications/', {
            'contact_phone': '13800138000',
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        application_id = response.data['application_id']

        # Student2 tries to access Student1's application
        response = self.client.post('/api/auth/login', {
            'user_id': '2020002',
            'password': '2020002'
        })
        token2 = response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token2}')
        response = self.client.get(f'/api/applications/{application_id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

    def test_not_found_application(self):
        """测试申请不存在"""
        response = self.client.post('/api/auth/login', {
            'user_id': '2020001',
            'password': '2020001'
        })
        token = response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/applications/app_nonexistent/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error']['code'], 'NOT_FOUND')

    def test_validation_error_missing_fields(self):
        """测试参数验证失败"""
        response = self.client.post('/api/auth/login', {
            'user_id': '2020001',
            'password': '2020001'
        })
        token = response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/applications/', {
            'reason': '毕业离校'
            # Missing leave_date
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
