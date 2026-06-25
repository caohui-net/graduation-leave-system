from django.test import TestCase
from rest_framework.test import APIClient
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision


class ApplicationListPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.student1 = User.objects.create(user_id='S001', name='学生1', role=UserRole.STUDENT, class_id='CS2020-01')
        self.student1.set_password('S001')
        self.student1.save()

        self.student2 = User.objects.create(user_id='S002', name='学生2', role=UserRole.STUDENT, class_id='CS2020-02')
        self.student2.set_password('S002')
        self.student2.save()

        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR, class_id='CS2020-01')
        self.counselor1.set_password('T001')
        self.counselor1.save()

        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR, class_id='CS2020-02')
        self.counselor2.set_password('T002')
        self.counselor2.save()

        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
        self.dorm_manager1.set_password('M001')
        self.dorm_manager1.save()

        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
        self.dorm_manager2.set_password('M002')
        self.dorm_manager2.save()

        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
        self.dean.set_password('D001')
        self.dean.save()

        # Create applications
        self.app1 = Application.objects.create(
            application_id='app_001',
            student=self.student1,
            student_name='学生1',
            class_id='CS2020-01',
            reason='测试',
            leave_date='2024-07-01',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        self.app2 = Application.objects.create(
            application_id='app_002',
            student=self.student2,
            student_name='学生2',
            class_id='CS2020-02',
            reason='测试',
            leave_date='2024-07-01',
            status=ApplicationStatus.APPROVED
        )

        # Create approvals
        Approval.objects.create(
            approval_id='apv_001',
            application=self.app1,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor1,
            approver_name='辅导员1',
            decision=ApprovalDecision.PENDING
        )

    def test_student_sees_only_own_applications(self):
        self.client.force_authenticate(user=self.student1)
        response = self.client.get('/api/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['application_id'], 'app_001')

    def test_student_cannot_see_other_student_applications(self):
        self.client.force_authenticate(user=self.student1)
        response = self.client.get('/api/applications/')
        app_ids = [app['application_id'] for app in response.data['results']]
        self.assertNotIn('app_002', app_ids)

    def test_counselor_sees_only_pending_counselor_approvals(self):
        self.client.force_authenticate(user=self.counselor1)
        response = self.client.get('/api/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['application_id'], 'app_001')

    def test_counselor_cannot_see_other_counselor_applications(self):
        self.client.force_authenticate(user=self.counselor2)
        response = self.client.get('/api/applications/')
        self.assertEqual(response.data['count'], 0)

    def test_dean_sees_only_approved_applications_for_archive(self):
        self.client.force_authenticate(user=self.dean)
        response = self.client.get('/api/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['application_id'], 'app_002')

    def test_response_format_no_nested_approvals(self):
        self.client.force_authenticate(user=self.student1)
        response = self.client.get('/api/applications/')
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertNotIn('approvals', response.data['results'][0])
