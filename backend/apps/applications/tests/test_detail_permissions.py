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
        self.student1 = User.objects.create(user_id='2020001', name='学生1', role=UserRole.STUDENT, class_id='CS2020-01')
        self.student1.set_password('2020001')
        self.student1.save()

        self.student2 = User.objects.create(user_id='2020002', name='学生2', role=UserRole.STUDENT, class_id='CS2020-02')
        self.student2.set_password('2020002')
        self.student2.save()

        # Counselors
        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
        self.counselor1.set_password('T001')
        self.counselor1.save()

        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
        self.counselor2.set_password('T002')
        self.counselor2.save()

        # Deans
        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
        self.dean1.set_password('D001')
        self.dean1.save()

        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
        self.dean2.set_password('D002')
        self.dean2.save()

        # Class mappings
        ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
        ClassMapping.objects.create(class_id='CS2020-02', counselor=self.counselor2, counselor_name='辅导员2', active=True)

    def test_student_cannot_access_other_student_application(self):
        # Student1 creates application
        self.client.force_authenticate(user=self.student1)
        response = self.client.post('/api/applications/', {
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

    def test_dean_cannot_access_non_assigned_application(self):
        # Student creates application
        self.client.force_authenticate(user=self.student1)
        response = self.client.post('/api/applications/', {
            'reason': '测试',
            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
        }, format='json')
        self.assertEqual(response.status_code, 201)
        app_id = response.data['application_id']

        # Counselor approves (creates dean approval for D001)
        self.client.force_authenticate(user=self.counselor1)
        approvals = self.client.get('/api/approvals/').data['results']
        approval_id = approvals[0]['approval_id']
        self.client.post(f'/api/approvals/{approval_id}/approve/', {'comment': '同意'}, format='json')

        # Dean D002 (different dean) tries to access
        self.client.force_authenticate(user=self.dean2)
        response = self.client.get(f'/api/applications/{app_id}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
