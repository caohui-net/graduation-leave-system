from django.core.management.base import BaseCommand
from apps.users.models import User

class Command(BaseCommand):
    help = '查询研究生用户的楼栋分布'

    def handle(self, *args, **options):
        # 研究生学号特征：2023045开头
        graduates = User.objects.filter(
            user_id__startswith='2023045',
            role='student'
        ).values('user_id', 'name', 'building', 'room_number', 'active')

        if not graduates:
            self.stdout.write('未找到研究生用户')
            return

        self.stdout.write(f'\n找到 {len(graduates)} 个研究生用户:\n')

        building_stats = {}
        for g in graduates:
            building = g['building'] or '未分配'
            building_stats[building] = building_stats.get(building, 0) + 1
            self.stdout.write(
                f"  {g['user_id']} | {g['name']} | {g['building'] or '无'} | "
                f"{g['room_number'] or '无'} | {'激活' if g['active'] else '停用'}"
            )

        self.stdout.write(f'\n楼栋统计:')
        for building, count in sorted(building_stats.items()):
            self.stdout.write(f"  {building}: {count}人")

        # 检查宿管员覆盖
        self.stdout.write(f'\n宿管员覆盖情况:')
        for building in building_stats.keys():
            if building == '未分配':
                continue
            managers = User.objects.filter(
                role='dorm_manager',
                building=building,
                active=True
            ).count()
            status = '✓' if managers > 0 else '✗ 缺失'
            self.stdout.write(f"  {building}: {status} ({managers}人)")
