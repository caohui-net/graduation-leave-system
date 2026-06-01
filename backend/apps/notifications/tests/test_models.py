from django.test import TestCase
from django.db import IntegrityError
from apps.users.models import User
from apps.notifications.models import Notification, NotificationType, EntityType


class NotificationModelTest(TestCase):
    def setUp(self):
        self.student = User.objects.create(
            user_id='2020001',
            name='测试学生',
            role='student',
            class_id='CS2020-01'
        )
        self.counselor = User.objects.create(
            user_id='T001',
            name='测试辅导员',
            role='counselor'
        )

    def test_create_notification(self):
        """测试创建通知"""
        notification = Notification.objects.create(
            recipient=self.student,
            actor=self.counselor,
            type=NotificationType.APPROVAL_APPROVED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_12345678',
            title='审批通过',
            message='您的离校申请已通过辅导员审批'
        )
        self.assertIsNotNone(notification.notification_id)
        self.assertTrue(notification.notification_id.startswith('not_'))
        self.assertEqual(len(notification.notification_id), 12)
        self.assertEqual(notification.recipient, self.student)
        self.assertIsNone(notification.read_at)

    def test_notification_id_auto_generated(self):
        """测试notification_id自动生成"""
        n1 = Notification.objects.create(
            recipient=self.student,
            type=NotificationType.APPLICATION_SUBMITTED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_11111111',
            title='申请已提交',
            message='您的离校申请已提交'
        )
        n2 = Notification.objects.create(
            recipient=self.student,
            type=NotificationType.APPLICATION_SUBMITTED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_22222222',
            title='申请已提交',
            message='您的离校申请已提交'
        )
        self.assertNotEqual(n1.notification_id, n2.notification_id)

    def test_unique_constraint(self):
        """测试唯一约束：同一接收者+实体+类型只能有一条通知"""
        Notification.objects.create(
            recipient=self.student,
            type=NotificationType.APPROVAL_APPROVED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_12345678',
            title='审批通过',
            message='您的离校申请已通过审批'
        )
        with self.assertRaises(IntegrityError):
            Notification.objects.create(
                recipient=self.student,
                type=NotificationType.APPROVAL_APPROVED,
                entity_type=EntityType.APPLICATION,
                entity_id='app_12345678',
                title='审批通过（重复）',
                message='重复通知'
            )

    def test_different_recipient_allows_duplicate(self):
        """测试不同接收者可以有相同实体的通知"""
        student2 = User.objects.create(
            user_id='2020002',
            name='测试学生2',
            role='student',
            class_id='CS2020-01'
        )
        n1 = Notification.objects.create(
            recipient=self.student,
            type=NotificationType.APPROVAL_APPROVED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_12345678',
            title='审批通过',
            message='通知1'
        )
        n2 = Notification.objects.create(
            recipient=student2,
            type=NotificationType.APPROVAL_APPROVED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_12345678',
            title='审批通过',
            message='通知2'
        )
        self.assertNotEqual(n1.notification_id, n2.notification_id)

    def test_ordering(self):
        """测试默认排序（按创建时间倒序）"""
        n1 = Notification.objects.create(
            recipient=self.student,
            type=NotificationType.APPLICATION_SUBMITTED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_11111111',
            title='通知1',
            message='消息1'
        )
        n2 = Notification.objects.create(
            recipient=self.student,
            type=NotificationType.APPROVAL_APPROVED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_22222222',
            title='通知2',
            message='消息2'
        )
        notifications = list(Notification.objects.all())
        self.assertEqual(notifications[0].notification_id, n2.notification_id)
        self.assertEqual(notifications[1].notification_id, n1.notification_id)
