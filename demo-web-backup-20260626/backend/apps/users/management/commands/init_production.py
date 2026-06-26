from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from apps.users.models import User
from apps.applications.models import Application
from apps.approvals.models import Approval
from apps.attachments.models import Attachment
from apps.notifications.models import Notification

class Command(BaseCommand):
    help = '初始化生产环境数据：清空申请/审批数据，重置用户密码为登录号'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化生产环境数据...')
        
        # 1. 清空申请和审批相关数据
        self.stdout.write('清空申请和审批数据...')
        Notification.objects.all().delete()
        Attachment.objects.all().delete()
        Approval.objects.all().delete()
        Application.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('✓ 申请和审批数据已清空'))
        
        # 2. 重置所有用户密码为登录号
        self.stdout.write('重置用户密码...')
        users = User.objects.all()
        count = 0
        for user in users:
            user.password = make_password(user.user_id)
            user.save(update_fields=['password'])
            count += 1
            if count % 100 == 0:
                self.stdout.write(f'已处理 {count} 个用户...')
        
        self.stdout.write(self.style.SUCCESS(f'✓ 已重置 {count} 个用户密码'))
        self.stdout.write(self.style.SUCCESS('生产环境初始化完成！'))
