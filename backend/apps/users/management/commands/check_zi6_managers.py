from django.core.management.base import BaseCommand
from apps.users.models import User

class Command(BaseCommand):
    help = '检查紫园6栋宿管员详情'

    def handle(self, *args, **options):
        # 检查紫园6栋宿管员
        self.stdout.write('\n紫园6栋宿管员:')
        managers = User.objects.filter(
            role='dorm_manager',
            building='紫园6栋',
            active=True
        )
        for m in managers:
            self.stdout.write(f'  {m.user_id} | {m.name} | building={m.building} | active={m.active}')

        # 检查fallback
        self.stdout.write('\nFallback宿管员(92008149):')
        fallback = User.objects.filter(user_id='92008149').first()
        if fallback:
            self.stdout.write(f'  {fallback.user_id} | {fallback.name} | role={fallback.role} | building={fallback.building} | active={fallback.active}')
        else:
            self.stdout.write('  ✗ 不存在')

        # 检查失败用户的building字段
        self.stdout.write('\n失败用户building字段:')
        for uid in ['2023045108016', '2023045104011']:
            u = User.objects.filter(user_id=uid).first()
            if u:
                self.stdout.write(f'  {u.user_id} | building="{u.building}" | active={u.active}')
