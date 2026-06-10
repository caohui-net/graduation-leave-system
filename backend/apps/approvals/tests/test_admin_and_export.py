from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.views import sanitize_excel_formula

User = get_user_model()


class AdminSuperuserTest(APITestCase):
    """Test ADMIN role can approve/reject any step and decided_by is recorded."""

    def setUp(self):
        self.student = User.objects.create_user(
            user_id='20200001', name='测试学生',
            role='student', department='计算机学院', building='1号楼'
        )
        self.dorm_manager = User.objects.create_user(
            user_id='M001', name='宿管员1',
            role='dorm_manager', building='1号楼'
        )
        self.admin = User.objects.create_user(
            user_id='A001', name='管理员',
            role='admin'
        )

        self.application = Application.objects.create(
            application_id='app_test001',
            student=self.student,
            student_name=self.student.name,
            class_id='CS2020',
            contact_phone='13800138000',
            leave_date='2026-07-01',
            status=ApplicationStatus.PENDING_DORM_MANAGER
        )

        self.approval = Approval.objects.create(
            approval_id='apv_test001',
            application=self.application,
            step=ApprovalStep.DORM_MANAGER,
            approver=self.dorm_manager,
            approver_name=self.dorm_manager.name,
            decision=ApprovalDecision.PENDING
        )

    def test_admin_can_approve_dorm_manager_step(self):
        """ADMIN can approve dorm manager step."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            f'/api/approvals/{self.approval.approval_id}/approve/',
            {'comment': 'ADMIN代审批'}
        )
        self.assertEqual(response.status_code, 200)
        self.approval.refresh_from_db()
        self.assertEqual(self.approval.decision, ApprovalDecision.APPROVED)
        self.assertEqual(self.approval.decided_by, self.admin)

    def test_admin_can_reject_any_step(self):
        """ADMIN can reject any step."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            f'/api/approvals/{self.approval.approval_id}/reject/',
            {'comment': 'ADMIN驳回'}
        )
        self.assertEqual(response.status_code, 200)
        self.approval.refresh_from_db()
        self.assertEqual(self.approval.decision, ApprovalDecision.REJECTED)
        self.assertEqual(self.approval.decided_by, self.admin)


class ExcelExportTest(APITestCase):
    """Test Excel export permissions and formula injection prevention."""

    def setUp(self):
        self.student = User.objects.create_user(
            user_id='20200002', name='学生',
            role='student'
        )
        self.dean = User.objects.create_user(
            user_id='D001', name='学工部',
            role='dean'
        )
        self.admin = User.objects.create_user(
            user_id='A002', name='管理员',
            role='admin'
        )

    def test_student_cannot_export(self):
        """Student cannot export."""
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/approvals/export/')
        self.assertEqual(response.status_code, 403)

    def test_dean_can_export(self):
        """DEAN can export."""
        self.client.force_authenticate(user=self.dean)
        response = self.client.get('/api/approvals/export/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    def test_admin_can_export(self):
        """ADMIN can export."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/approvals/export/')
        self.assertEqual(response.status_code, 200)

    def test_sanitize_excel_formula(self):
        """Test formula injection prevention."""
        self.assertEqual(sanitize_excel_formula('=SUM(A1:A10)'), "'=SUM(A1:A10)")
        self.assertEqual(sanitize_excel_formula('+1234'), "'+1234")
        self.assertEqual(sanitize_excel_formula('-cmd'), "'-cmd")
        self.assertEqual(sanitize_excel_formula('@remote'), "'@remote")
        self.assertEqual(sanitize_excel_formula('normal text'), 'normal text')
        self.assertEqual(sanitize_excel_formula(''), '')
        self.assertEqual(sanitize_excel_formula(None), None)
