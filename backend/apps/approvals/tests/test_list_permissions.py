from django.test import TestCase
from rest_framework.test import APIClient
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision


class ApprovalListPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.student = User.objects.create(user_id='S001', name='学生', role=UserRole.STUDENT, class_id='CS2020-01')
        self.student.set_password('S001')
        self.student.save()

        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
        self.counselor1.set_password('T001')
        self.counselor1.save()

        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
        self.counselor2.set_password('T002')
        self.counselor2.save()

        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
        self.dean1.set_password('D001')
        self.dean1.save()

        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
        self.dean2.set_password('D002')
        self.dean2.save()

        # Create application
        self.app = Application.objects.create(
            application_id='app_001',
            student=self.student,
            student_name='学生',
            class_id='CS2020-01',
            reason='测试',
            leave_date='2024-07-01',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        # Create approvals
        self.approval_c1 = Approval.objects.create(
            approval_id='apv_c1',
            application=self.app,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor1,
            approver_name='辅导员1',
            decision=ApprovalDecision.PENDING
        )

        self.approval_d1 = Approval.objects.create(
            approval_id='apv_d1',
            application=self.app,
            step=ApprovalStep.DEAN,
            approver=self.dean1,
            approver_name='学工部1',
            decision=ApprovalDecision.PENDING
        )

    def test_student_403_on_approval_list(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/approvals/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

    def test_counselor_sees_only_own_pending_approvals(self):
        self.client.force_authenticate(user=self.counselor1)
        response = self.client.get('/api/approvals/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['approval_id'], 'apv_c1')

    def test_counselor_cannot_see_other_counselor_approvals(self):
        self.client.force_authenticate(user=self.counselor2)
        response = self.client.get('/api/approvals/')
        self.assertEqual(response.data['count'], 0)

    def test_dean_sees_only_own_pending_approvals(self):
        self.client.force_authenticate(user=self.dean1)
        response = self.client.get('/api/approvals/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['approval_id'], 'apv_d1')

    def test_dean_cannot_see_other_dean_approvals(self):
        self.client.force_authenticate(user=self.dean2)
        response = self.client.get('/api/approvals/')
        self.assertEqual(response.data['count'], 0)

    def test_response_format_count_and_results(self):
        self.client.force_authenticate(user=self.counselor1)
        response = self.client.get('/api/approvals/')
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertNotIn('next', response.data)
        self.assertNotIn('previous', response.data)
