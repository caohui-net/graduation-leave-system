"""
Tests for automatic notification creation.

Verifies that notifications are created automatically when:
- Student submits application (APPLICATION_SUBMITTED)
- Approval is approved (APPROVAL_APPROVED)
- Approval is rejected (APPROVAL_REJECTED)

Also tests idempotency and negative paths.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.notifications.models import Notification
from apps.notifications.services import notify_application_submitted, notify_approval_decided

User = get_user_model()


class AutoNotificationTest(TestCase):
    """Test automatic notification creation."""

    def setUp(self):
        """Create test users and base data."""
        self.student = User.objects.create_user(
            user_id='2021001',
            name='测试学生',
            role='student',
            class_id='CS2021-1'
        )
        self.counselor = User.objects.create_user(
            user_id='T001',
            name='张老师',
            role='counselor'
        )
        self.dean = User.objects.create_user(
            user_id='D001',
            name='赵主任',
            role='dean'
        )

    def test_application_submitted_notification(self):
        """Test APPLICATION_SUBMITTED notification creation."""
        application = Application.objects.create(
            application_id='app_test001',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test001',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.PENDING
        )

        notification, created = notify_application_submitted(application, approval)

        self.assertTrue(created)
        self.assertEqual(notification.recipient, self.counselor)
        self.assertEqual(notification.actor, self.student)
        self.assertEqual(notification.type, 'application_submitted')
        self.assertEqual(notification.entity_type, 'approval')
        self.assertEqual(notification.entity_id, approval.pk)
        self.assertIn('测试学生', notification.message)
        self.assertIn('2021001', notification.message)

    def test_approval_approved_notification_counselor(self):
        """Test APPROVAL_APPROVED notification for counselor approval."""
        application = Application.objects.create(
            application_id='app_test002',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test002',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.APPROVED
        )

        notification, created = notify_approval_decided(approval)

        self.assertTrue(created)
        self.assertEqual(notification.recipient, self.student)
        self.assertEqual(notification.actor, self.counselor)
        self.assertEqual(notification.type, 'approval_approved')
        self.assertEqual(notification.entity_type, 'approval')
        self.assertEqual(notification.entity_id, approval.pk)
        self.assertIn('辅导员', notification.message)

    def test_approval_approved_notification_dean(self):
        """Test APPROVAL_APPROVED notification for dean approval."""
        application = Application.objects.create(
            application_id='app_test003',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_DEAN
        )

        approval = Approval.objects.create(
            approval_id='apv_test003',
            application=application,
            step=ApprovalStep.DEAN,
            approver=self.dean,
            approver_name=self.dean.name,
            decision=ApprovalDecision.APPROVED
        )

        notification, created = notify_approval_decided(approval)

        self.assertTrue(created)
        self.assertEqual(notification.recipient, self.student)
        self.assertEqual(notification.actor, self.dean)
        self.assertEqual(notification.type, 'approval_approved')
        self.assertIn('学工部', notification.message)

    def test_approval_rejected_notification(self):
        """Test APPROVAL_REJECTED notification creation."""
        application = Application.objects.create(
            application_id='app_test004',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test004',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.REJECTED,
            comment='材料不齐全'
        )

        notification, created = notify_approval_decided(approval)

        self.assertTrue(created)
        self.assertEqual(notification.recipient, self.student)
        self.assertEqual(notification.actor, self.counselor)
        self.assertEqual(notification.type, 'approval_rejected')
        self.assertIn('驳回', notification.message)
        self.assertIn('材料不齐全', notification.message)

    def test_idempotency_application_submitted(self):
        """Test that repeated calls don't create duplicate notifications."""
        application = Application.objects.create(
            application_id='app_test005',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test005',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.PENDING
        )

        notification1, created1 = notify_application_submitted(application, approval)
        self.assertTrue(created1)

        notification2, created2 = notify_application_submitted(application, approval)
        self.assertFalse(created2)
        self.assertEqual(notification1.pk, notification2.pk)

        self.assertEqual(Notification.objects.filter(
            recipient=self.counselor,
            entity_type='approval',
            entity_id=approval.pk,
            type='application_submitted'
        ).count(), 1)

    def test_idempotency_approval_decided(self):
        """Test that repeated approval decisions don't create duplicate notifications."""
        application = Application.objects.create(
            application_id='app_test006',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test006',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.APPROVED
        )

        notification1, created1 = notify_approval_decided(approval)
        self.assertTrue(created1)

        notification2, created2 = notify_approval_decided(approval)
        self.assertFalse(created2)
        self.assertEqual(notification1.pk, notification2.pk)

        self.assertEqual(Notification.objects.filter(
            recipient=self.student,
            entity_type='approval',
            entity_id=approval.pk,
            type='approval_approved'
        ).count(), 1)
