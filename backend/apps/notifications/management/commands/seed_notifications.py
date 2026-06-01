from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import User
from apps.notifications.models import Notification, NotificationType, EntityType


class Command(BaseCommand):
    help = '创建测试通知数据'

    def handle(self, *args, **options):
        students = User.objects.filter(role='student')[:3]

        if not students:
            self.stdout.write(self.style.ERROR('未找到学生用户，请先创建用户'))
            return

        created_count = 0

        for i, student in enumerate(students):
            Notification.objects.create(
                recipient=student,
                type=NotificationType.APPLICATION_SUBMITTED,
                entity_type=EntityType.APPLICATION,
                entity_id=f'app_{i:08d}',
                title='申请已提交',
                message=f'您的离校申请已提交，等待审批'
            )
            created_count += 1

            if i == 0:
                Notification.objects.create(
                    recipient=student,
                    type=NotificationType.APPROVAL_APPROVED,
                    entity_type=EntityType.APPLICATION,
                    entity_id=f'app_{i+100:08d}',
                    title='申请已通过',
                    message='您的离校申请已通过审批',
                    read_at=timezone.now()
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'成功创建 {created_count} 条通知'))
