from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.applications.models import Application

class Command(BaseCommand):
    help = '检查失败用户的申请记录'

    def handle(self, *args, **options):
        for uid in ['2023045108016', '2023045104011']:
            self.stdout.write(f'\n用户 {uid}:')
            user = User.objects.filter(user_id=uid).first()
            if not user:
                self.stdout.write('  用户不存在')
                continue

            apps = Application.objects.filter(student=user).order_by('-created_at')
            if not apps:
                self.stdout.write('  无申请记录')
            else:
                for app in apps:
                    self.stdout.write(f'  {app.application_id} | {app.status} | {app.created_at}')
