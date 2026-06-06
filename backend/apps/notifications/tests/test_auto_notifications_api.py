"""
API-level tests for automatic notification creation.

Verifies that notifications created by business logic are visible through the API
and that negative paths (permission denied, status conflicts) don't create notifications.
"""

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.notifications.models import Notification
from apps.users.class_mapping import ClassMapping

User = get_user_model()


class AutoNotificationAPITest(TestCase):
    """Test automatic notifications are visible through API."""

    def setUp(self):
        """Create test users and class mapping."""
        self.client = APIClient()

        self.student = User.objects.create_user(
            user_id='2020001',
            name='测试学生',
            role='student',
            class_id='CS2021-1',
            building='1号楼',
            department='计算机学院'
        )
        self.counselor = User.objects.create_user(
            user_id='T001',
            name='张老师',
            role='counselor',
            department='计算机学院'
        )
        self.dorm_manager = User.objects.create_user(
            user_id='M001',
            name='宿管员',
            role='dorm_manager',
            building='1号楼'
        )
        self.dean = User.objects.create_user(
            user_id='D001',
            name='学工部',
            role='dean'
        )

        ClassMapping.objects.create(
            class_id='CS2021-1',
            dorm_manager=self.dorm_manager,
            dorm_manager_name=self.dorm_manager.name,
            counselor=self.counselor,
            counselor_name=self.counselor.name,
            active=True
        )

    def test_application_submitted_notification_visible_via_api(self):
        """Test dorm manager can see APPLICATION_SUBMITTED notification via API after student submits."""
        # Student submits application (triggers notification)
        self.client.force_authenticate(user=self.student)
        response = self.client.post('/api/applications/', {
            'reason': '毕业离校',
            'leave_date': '2026-07-01'
        })
        self.assertEqual(response.status_code, 201)

        # Dorm manager checks notifications via API
        self.client.force_authenticate(user=self.dorm_manager)
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, 200)

        notifications = response.json()['results']
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]['type'], 'application_submitted')
        self.assertEqual(notifications[0]['entity_type'], 'approval')
        self.assertIn('测试学生', notifications[0]['message'])

    def test_approval_approved_notification_visible_via_api(self):
        """Test student can see APPROVAL_APPROVED notification via API after counselor approves."""
        # Create application and approval
        application = Application.objects.create(
            application_id='app_test001',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2026-07-01',
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

        # Counselor approves (triggers notification)
        self.client.force_authenticate(user=self.counselor)
        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
            'comment': '同意'
        })
        self.assertEqual(response.status_code, 200)

        # Student checks notifications via API
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, 200)

        notifications = response.json()['results']
        self.assertGreaterEqual(len(notifications), 1)

        # Find the approval notification
        approval_notif = [n for n in notifications if n['type'] == 'approval_approved'][0]
        self.assertEqual(approval_notif['entity_type'], 'approval')
        self.assertIn('辅导员', approval_notif['message'])

    def test_approval_rejected_notification_includes_reason(self):
        """Test APPROVAL_REJECTED notification includes rejection reason in message."""
        # Create application and approval
        application = Application.objects.create(
            application_id='app_test002',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2026-07-01',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test002',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.PENDING
        )

        # Counselor rejects with reason
        self.client.force_authenticate(user=self.counselor)
        response = self.client.post(f'/api/approvals/{approval.approval_id}/reject/', {
            'comment': '材料不齐全，请补充'
        })
        self.assertEqual(response.status_code, 200)

        # Student checks notification
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, 200)

        notifications = response.json()['results']
        reject_notif = [n for n in notifications if n['type'] == 'approval_rejected'][0]
        self.assertIn('材料不齐全，请补充', reject_notif['message'])

    def test_permission_denied_does_not_create_notification(self):
        """Test that permission denied does not create spurious notifications."""
        # Create application for student1
        student2 = User.objects.create_user(
            user_id='2021002',
            name='其他学生',
            role='student',
            class_id='CS2021-2',
            building='2号楼',
            department='软件学院'
        )

        application = Application.objects.create(
            application_id='app_test003',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2026-07-01',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test003',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.PENDING
        )

        # Student2 tries to approve (should fail with permission denied)
        self.client.force_authenticate(user=student2)
        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
            'comment': '同意'
        })
        self.assertIn(response.status_code, [403, 404])

        # Verify no notification was created
        self.assertEqual(Notification.objects.filter(
            entity_type='approval',
            entity_id=approval.pk
        ).count(), 0)

    def test_status_conflict_does_not_create_notification(self):
        """Test that status conflict (e.g., re-approving) does not create duplicate notifications."""
        # Create application and approval
        application = Application.objects.create(
            application_id='app_test004',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2026-07-01',
            status=ApplicationStatus.APPROVED
        )

        approval = Approval.objects.create(
            approval_id='apv_test004',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.APPROVED  # Already approved
        )

        # Counselor tries to approve again (should fail with conflict)
        self.client.force_authenticate(user=self.counselor)
        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
            'comment': '再次同意'
        })
        self.assertEqual(response.status_code, 409)

        # Verify only one notification exists (from initial approval, not from failed re-approval)
        self.assertEqual(Notification.objects.filter(
            recipient=self.student,
            entity_type='approval',
            entity_id=approval.pk
        ).count(), 0)  # No notification because we created approval directly, not through API

    def test_dorm_blocked_does_not_create_notification(self):
        """Test that dorm checkout blockage does not create notifications."""
        # Create student with non-completed dorm status (use ID not in mock data)
        blocked_student = User.objects.create_user(
            user_id='2021999',
            name='被阻断学生',
            role='student',
            class_id='CS2021-1',
            building='1号楼',
            department='计算机学院'
        )

        # Student tries to submit application (should fail with 422 dorm blocked)
        self.client.force_authenticate(user=blocked_student)
        response = self.client.post('/api/applications/', {
            'reason': '毕业离校',
            'leave_date': '2026-07-01'
        })
        self.assertEqual(response.status_code, 422)

        # Verify no Application was created (422 is synchronous validation failure)
        self.assertEqual(Application.objects.filter(student=blocked_student).count(), 0)

        # Verify no notification was created for the blocked student
        self.assertEqual(Notification.objects.filter(recipient=blocked_student).count(), 0)

        # Verify no notification was created for counselor
        self.assertEqual(Notification.objects.filter(
            recipient=self.dorm_manager,
            type='application_submitted'
        ).count(), 0)
