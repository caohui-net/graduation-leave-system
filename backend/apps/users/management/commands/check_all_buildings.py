from django.core.management.base import BaseCommand
from apps.users.models import User

class Command(BaseCommand):
    help = '检查所有可能的building值'

    def handle(self, *args, **options):
        # 查询所有不同的building值
        buildings = User.objects.exclude(building__isnull=True).exclude(building='').values_list('building', flat=True).distinct()

        self.stdout.write('\n所有building值（包含"紫"或"6"）:')
        zi_buildings = [b for b in buildings if '紫' in b or '6' in b]
        for b in sorted(zi_buildings):
            count = User.objects.filter(building=b, role='student').count()
            manager_count = User.objects.filter(building=b, role='dorm_manager', active=True).count()
            self.stdout.write(f'  "{b}": {count}个学生, {manager_count}个宿管员')
