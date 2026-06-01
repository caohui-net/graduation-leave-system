from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from apps.users.models import User
from apps.notifications.models import Notification, NotificationType, EntityType


class NotificationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student1 = User.objects.create(
            user_id='2020001',
            name='学生1',
            role='student',
            class_id='CS2020-01'
        )
        self.student2 = User.objects.create(
            user_id='2020002',
            name='学生2',
            role='student',
            class_id='CS2020-02'
        )
        self.counselor = User.objects.create(
            user_id='T001',
            name='辅导员',
            role='counselor'
        )

    def test_list_notifications(self):
        """测试列表API"""
        Notification.objects.create(
            recipient=self.student1,
            type=NotificationType.APPLICATION_SUBMITTED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_11111111',
            title='通知1',
            message='消息1'
        )
        Notification.objects.create(
            recipient=self.student1,
            type=NotificationType.APPROVAL_APPROVED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_22222222',
            title='通知2',
            message='消息2'
        )

        self.client.force_authenticate(user=self.student1)
        response = self.client.get('/api/notifications/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_with_read_filter(self):
        """测试read过滤"""
        n1 = Notification.objects.create(
            recipient=self.student1,
            type=NotificationType.APPLICATION_SUBMITTED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_11111111',
            title='未读通知',
            message='消息1'
        )
        n2 = Notification.objects.create(
            recipient=self.student1,
            type=NotificationType.APPROVAL_APPROVED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_22222222',
            title='已读通知',
            message='消息2',
            read_at=timezone.now()
        )

        self.client.force_authenticate(user=self.student1)

        response = self.client.get('/api/notifications/?read=unread')
        self.assertEqual(response.data['count'], 1)

        response = self.client.get('/api/notifications/?read=read')
        self.assertEqual(response.data['count'], 1)

        response = self.client.get('/api/notifications/?read=all')
        self.assertEqual(response.data['count'], 2)

    def test_list_pagination(self):
        """测试分页"""
        for i in range(5):
            Notification.objects.create(
                recipient=self.student1,
                type=NotificationType.APPLICATION_SUBMITTED,
                entity_type=EntityType.APPLICATION,
                entity_id=f'app_{i:08d}',
                title=f'通知{i}',
                message=f'消息{i}'
            )

        self.client.force_authenticate(user=self.student1)

        response = self.client.get('/api/notifications/?limit=2&offset=0')
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 2)

        response = self.client.get('/api/notifications/?limit=2&offset=2')
        self.assertEqual(len(response.data['results']), 2)

    def test_list_rbac(self):
        """测试RBAC：只能看到自己的通知"""
        Notification.objects.create(
            recipient=self.student1,
            type=NotificationType.APPLICATION_SUBMITTED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_11111111',
            title='学生1的通知',
            message='消息1'
        )
        Notification.objects.create(
            recipient=self.student2,
            type=NotificationType.APPLICATION_SUBMITTED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_22222222',
            title='学生2的通知',
            message='消息2'
        )

        self.client.force_authenticate(user=self.student1)
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.data['count'], 1)

    def test_unread_count(self):
        """测试未读数API"""
        Notification.objects.create(
            recipient=self.student1,
            type=NotificationType.APPLICATION_SUBMITTED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_11111111',
            title='未读1',
            message='消息1'
        )
        Notification.objects.create(
            recipient=self.student1,
            type=NotificationType.APPROVAL_APPROVED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_22222222',
            title='已读',
            message='消息2',
            read_at=timezone.now()
        )

        self.client.force_authenticate(user=self.student1)
        response = self.client.get('/api/notifications/unread_count/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['unread_count'], 1)

    def test_mark_as_read(self):
        """测试标记已读API"""
        notification = Notification.objects.create(
            recipient=self.student1,
            type=NotificationType.APPLICATION_SUBMITTED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_11111111',
            title='通知',
            message='消息'
        )

        self.client.force_authenticate(user=self.student1)
        response = self.client.patch(f'/api/notifications/{notification.notification_id}/read/')

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['read_at'])

        notification.refresh_from_db()
        self.assertIsNotNone(notification.read_at)

    def test_mark_as_read_idempotent(self):
        """测试标记已读幂等性"""
        notification = Notification.objects.create(
            recipient=self.student1,
            type=NotificationType.APPLICATION_SUBMITTED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_11111111',
            title='通知',
            message='消息'
        )

        self.client.force_authenticate(user=self.student1)

        response1 = self.client.patch(f'/api/notifications/{notification.notification_id}/read/')
        self.assertEqual(response1.status_code, 200)
        first_read_at = response1.data['read_at']

        response2 = self.client.patch(f'/api/notifications/{notification.notification_id}/read/')
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data['read_at'], first_read_at)

    def test_mark_as_read_forbidden(self):
        """测试标记已读权限：不能标记他人通知"""
        notification = Notification.objects.create(
            recipient=self.student1,
            type=NotificationType.APPLICATION_SUBMITTED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_11111111',
            title='通知',
            message='消息'
        )

        self.client.force_authenticate(user=self.student2)
        response = self.client.patch(f'/api/notifications/{notification.notification_id}/read/')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

    def test_mark_as_read_not_found(self):
        """测试标记已读：通知不存在"""
        self.client.force_authenticate(user=self.student1)
        response = self.client.patch('/api/notifications/not_99999999/read/')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error']['code'], 'NOT_FOUND')

    def test_mark_all_read(self):
        """测试全部已读API"""
        Notification.objects.create(
            recipient=self.student1,
            type=NotificationType.APPLICATION_SUBMITTED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_11111111',
            title='未读1',
            message='消息1'
        )
        Notification.objects.create(
            recipient=self.student1,
            type=NotificationType.APPROVAL_APPROVED,
            entity_type=EntityType.APPLICATION,
            entity_id='app_22222222',
            title='未读2',
            message='消息2'
        )

        self.client.force_authenticate(user=self.student1)
        response = self.client.post('/api/notifications/mark_all_read/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['marked_count'], 2)

        unread_count = Notification.objects.filter(
            recipient=self.student1,
            read_at__isnull=True
        ).count()
        self.assertEqual(unread_count, 0)
