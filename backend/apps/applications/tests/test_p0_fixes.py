from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalDecision, ApprovalStep
from apps.users.models import UserRole

User = get_user_model()


class ResubmissionAfterRejectionTest(TestCase):
    def setUp(self):
        self.student = User.objects.create(
            user_id='S001',
            name='Test Student',
            role=UserRole.STUDENT,
            class_id='CS2020-01'
        )
        self.counselor = User.objects.create(
            user_id='C001',
            name='Test Counselor',
            role=UserRole.COUNSELOR,
            class_id='CS2020-01'
        )

    def test_can_resubmit_after_rejection(self):
        # Create and reject first application
        app1 = Application.objects.create(
            application_id='app_001',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='First attempt',
            leave_date='2024-06-30',
            status=ApplicationStatus.REJECTED
        )

        # Should be able to create second application after rejection
        app2 = Application.objects.create(
            application_id='app_002',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='Second attempt',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        self.assertEqual(Application.objects.filter(student=self.student).count(), 2)
        self.assertEqual(app2.status, ApplicationStatus.PENDING_COUNSELOR)

    def test_cannot_resubmit_while_pending(self):
        # Create pending application
        app1 = Application.objects.create(
            application_id='app_001',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='First attempt',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        # Try to create second application while first is pending
        app2 = Application(
            application_id='app_002',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='Second attempt',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        # Should raise validation error
        with self.assertRaises(Exception):
            app2.full_clean()


class ApprovalDecisionFilterTest(TestCase):
    def setUp(self):
        self.student = User.objects.create(
            user_id='S001',
            name='Test Student',
            role=UserRole.STUDENT,
            class_id='CS2020-01'
        )
        self.counselor = User.objects.create(
            user_id='C001',
            name='Test Counselor',
            role=UserRole.COUNSELOR,
            class_id='CS2020-01'
        )

        # Create applications with different approval states
        self.app_pending = Application.objects.create(
            application_id='app_pending',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='Pending',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        self.app_approved = Application.objects.create(
            application_id='app_approved',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='Approved',
            leave_date='2024-06-30',
            status=ApplicationStatus.APPROVED
        )

        self.app_rejected = Application.objects.create(
            application_id='app_rejected',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='Rejected',
            leave_date='2024-06-30',
            status=ApplicationStatus.REJECTED
        )

        # Create approvals
        self.approval_pending = Approval.objects.create(
            approval_id='apv_pending',
            application=self.app_pending,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.PENDING
        )

        self.approval_approved = Approval.objects.create(
            approval_id='apv_approved',
            application=self.app_approved,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.APPROVED
        )

        self.approval_rejected = Approval.objects.create(
            approval_id='apv_rejected',
            application=self.app_rejected,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.REJECTED
        )

    def test_filter_pending_approvals(self):
        approvals = Approval.objects.filter(
            approver=self.counselor,
            decision=ApprovalDecision.PENDING
        )
        self.assertEqual(approvals.count(), 1)
        self.assertEqual(approvals.first().approval_id, 'apv_pending')

    def test_filter_approved_approvals(self):
        approvals = Approval.objects.filter(
            approver=self.counselor,
            decision=ApprovalDecision.APPROVED
        )
        self.assertEqual(approvals.count(), 1)
        self.assertEqual(approvals.first().approval_id, 'apv_approved')

    def test_filter_rejected_approvals(self):
        approvals = Approval.objects.filter(
            approver=self.counselor,
            decision=ApprovalDecision.REJECTED
        )
        self.assertEqual(approvals.count(), 1)
        self.assertEqual(approvals.first().approval_id, 'apv_rejected')

    def test_filter_all_approvals(self):
        approvals = Approval.objects.filter(approver=self.counselor)
        self.assertEqual(approvals.count(), 3)
