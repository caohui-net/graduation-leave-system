from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus
from apps.users.class_mapping import ClassMapping


class ApplicationConstraintsTestCase(TestCase):
    def setUp(self):
        # Create student
        self.student = User.objects.create_user(
            user_id='2020001',
            name='张三',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            is_graduating=True,
            graduation_year=2024,
            password='2020001',
            building='1号楼',
            department='计算机学院'
        )

        # Create counselor
        self.counselor = User.objects.create_user(
            user_id='T001',
            name='李老师',
            role=UserRole.COUNSELOR,
            password='T001',
            department='计算机学院'
        )
        self.dorm_manager = User.objects.create_user(
            user_id='M001',
            name='宿管员',
            role=UserRole.DORM_MANAGER,
            password='M001',
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

        self.client = APIClient()

    def test_duplicate_submission_conflict(self):
        """测试重复提交返回409"""
        self.client.force_authenticate(user=self.student)

        # First submission
        response1 = self.client.post(
            '/api/applications/',
            {
                'reason': '毕业离校',
                'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
            },
            format='json'
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Second submission attempt
        response2 = self.client.post(
            '/api/applications/',
            {
                'reason': '再次提交',
                'leave_date': (timezone.now().date() + timedelta(days=2)).isoformat()
            },
            format='json'
        )
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
