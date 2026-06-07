from django.test import TestCase
from rest_framework.test import APIClient
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from django.utils import timezone


class ApplicationDetailPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Students (use IDs that mock provider recognizes as COMPLETED)
        self.student1 = User.objects.create(user_id='2020001', name='学生1', role=UserRole.STUDENT, class_id='CS2020-01', building='1号楼', department='计算机学院')
        self.student1.set_password('2020001')
        self.student1.save()

        self.student2 = User.objects.create(user_id='2020002', name='学生2', role=UserRole.STUDENT, class_id='CS2020-02', building='2号楼', department='软件学院')
        self.student2.set_password('2020002')
        self.student2.save()

        # Counselors
        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR, department='计算机学院')
        self.counselor1.set_password('T001')
        self.counselor1.save()

        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR, department='软件学院')
        self.counselor2.set_password('T002')
        self.counselor2.save()

        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER, building='1号楼')
        self.dorm_manager1.set_password('M001')
        self.dorm_manager1.save()

        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER, building='2号楼')
        self.dorm_manager2.set_password('M002')
        self.dorm_manager2.save()

        # Deans
        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
        self.dean1.set_password('D001')
        self.dean1.save()

        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
        self.dean2.set_password('D002')
        self.dean2.save()

        # Class mappings
        ClassMapping.objects.create(class_id='CS2020-01', dorm_manager=self.dorm_manager1, dorm_manager_name='宿管员1', counselor=self.counselor1, counselor_name='辅导员1', active=True)
        ClassMapping.objects.create(class_id='CS2020-02', dorm_manager=self.dorm_manager2, dorm_manager_name='宿管员2', counselor=self.counselor2, counselor_name='辅导员2', active=True)

    def test_student_cannot_access_other_student_application(self):
        # Student1 creates application
        self.client.force_authenticate(user=self.student1)
        response = self.client.post('/api/applications/', {
            'contact_phone': '13800138000',
            'reason': '测试',
            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
        }, format='json')
        self.assertEqual(response.status_code, 201)
        app_id = response.data['application_id']

        # Student2 tries to access Student1's application
        self.client.force_authenticate(user=self.student2)
        response = self.client.get(f'/api/applications/{app_id}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

    def test_counselor_cannot_access_cross_class_application(self):
        # Student from CS2020-01 creates application
        self.client.force_authenticate(user=self.student1)
        response = self.client.post('/api/applications/', {
            'contact_phone': '13800138000',
            'reason': '测试',
            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
        }, format='json')
        self.assertEqual(response.status_code, 201)
        app_id = response.data['application_id']

        # Counselor T002 (assigned to CS2020-02) tries to access
        self.client.force_authenticate(user=self.counselor2)
        response = self.client.get(f'/api/applications/{app_id}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

    def test_dean_cannot_access_in_progress_application(self):
        # Student creates application
        self.client.force_authenticate(user=self.student1)
        response = self.client.post('/api/applications/', {
            'contact_phone': '13800138000',
            'reason': '测试',
            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
        }, format='json')
        self.assertEqual(response.status_code, 201)
        app_id = response.data['application_id']

        # Dean archive role cannot access in-progress applications
        self.client.force_authenticate(user=self.dean2)
        response = self.client.get(f'/api/applications/{app_id}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
