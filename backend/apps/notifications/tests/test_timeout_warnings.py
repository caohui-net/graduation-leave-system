from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from apps.notifications.services import create_approval_timeout_warnings
from apps.notifications.models import Notification, NotificationType
from apps.applications.models import Application
from apps.approvals.models import Approval, ApprovalDecision

User = get_user_model()


class ApprovalTimeoutWarningTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            user_id='2020001',
            name='测试学生',
            role='student',
            class_id='CS2020-1',
            building='1号楼',
            department='计算机学院'
        )
        self.counselor = User.objects.create_user(
            user_id='T001',
            name='测试辅导员',
            role='counselor',
            class_id='CS2020-1',
            department='计算机学院'
        )
        self.dorm_manager = User.objects.create_user(
            user_id='M001',
            name='测试宿管员',
            role='dorm_manager',
            building='1号楼'
        )

    def test_counselor_timeout_3_days(self):
        """Test counselor approval timeout after 3 days"""
        app = Application.objects.create(
            student=self.student,
            reason='毕业离校',
            leave_date='2026-07-01'
        )
        approval = Approval.objects.create(
            application=app,
            step='counselor',
            approver=self.counselor
        )
        approval.created_at = timezone.now() - timedelta(days=4)
        approval.save()

        result = create_approval_timeout_warnings()

        self.assertEqual(result['created'], 1)
        self.assertEqual(Notification.objects.filter(
            type=NotificationType.APPROVAL_TIMEOUT_WARNING,
            recipient=self.counselor
        ).count(), 1)

    def test_dorm_manager_timeout_2_days(self):
        """Test dorm manager approval timeout after 2 days"""
        app = Application.objects.create(
            student=self.student,
            reason='毕业离校',
            leave_date='2026-07-01'
        )
        approval = Approval.objects.create(
            application=app,
            step='dorm_manager',
            approver=self.dorm_manager
        )
        approval.created_at = timezone.now() - timedelta(days=3)
        approval.save()

        result = create_approval_timeout_warnings()

        self.assertEqual(result['created'], 1)
        self.assertEqual(Notification.objects.filter(
            type=NotificationType.APPROVAL_TIMEOUT_WARNING,
            recipient=self.dorm_manager
        ).count(), 1)

    def test_no_timeout_not_notified(self):
        """Test that approvals within threshold are not notified"""
        app = Application.objects.create(
            student=self.student,
            reason='毕业离校',
            leave_date='2026-07-01'
        )
        Approval.objects.create(
            application=app,
            step='counselor',
            approver=self.counselor
        )

        result = create_approval_timeout_warnings()

        self.assertEqual(result['created'], 0)
        self.assertEqual(Notification.objects.count(), 0)

    def test_approved_not_notified(self):
        """Test that approved/rejected approvals are not notified"""
        app = Application.objects.create(
            student=self.student,
            reason='毕业离校',
            leave_date='2026-07-01'
        )
        approval = Approval.objects.create(
            application=app,
            step='counselor',
            approver=self.counselor,
            decision=ApprovalDecision.APPROVED
        )
        approval.created_at = timezone.now() - timedelta(days=4)
        approval.save()

        result = create_approval_timeout_warnings()

        self.assertEqual(result['created'], 0)
        self.assertEqual(Notification.objects.count(), 0)

    def test_idempotent_no_duplicate(self):
        """Test that repeated runs don't create duplicate notifications"""
        app = Application.objects.create(
            student=self.student,
            reason='毕业离校',
            leave_date='2026-07-01'
        )
        approval = Approval.objects.create(
            application=app,
            step='counselor',
            approver=self.counselor
        )
        approval.created_at = timezone.now() - timedelta(days=4)
        approval.save()

        result1 = create_approval_timeout_warnings()
        self.assertEqual(result1['created'], 1)

        result2 = create_approval_timeout_warnings()
        self.assertEqual(result2['created'], 0)
        self.assertEqual(result2['skipped'], 1)
        self.assertEqual(Notification.objects.count(), 1)

    def test_dry_run_mode(self):
        """Test dry run mode doesn't create notifications"""
        app = Application.objects.create(
            student=self.student,
            reason='毕业离校',
            leave_date='2026-07-01'
        )
        approval = Approval.objects.create(
            application=app,
            step='counselor',
            approver=self.counselor
        )
        approval.created_at = timezone.now() - timedelta(days=4)
        approval.save()

        result = create_approval_timeout_warnings(dry_run=True)

        self.assertEqual(result['created'], 1)
        self.assertEqual(Notification.objects.count(), 0)
        self.assertIn('approval_id', result['warnings'][0])
