"""清理测试数据管理命令"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.users.models import User
from apps.applications.models import Application
from apps.approvals.models import Approval
from apps.notifications.models import Notification


class Command(BaseCommand):
    help = '清理测试数据（测试用户及关联的申请、审批、通知）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='预览将删除的数据，不实际删除',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # 定义测试账号
        test_ids = [
            '2020001', '2020002', '2020003', '2020004', '2020005',
            '2020006', '2020007', '2020008', '2020009', '2020010',
            'M001', 'M002', 'M003', 'T001', 'T002', 'D001'
        ]

        self.stdout.write('=== 测试数据清理 ===\n')

        # 统计测试数据
        test_users = User.objects.filter(user_id__in=test_ids)
        test_apps = Application.objects.filter(student__user_id__in=test_ids)
        test_approvals = Approval.objects.filter(approver__user_id__in=test_ids)
        test_notifications = Notification.objects.filter(recipient__user_id__in=test_ids)

        self.stdout.write(f'测试用户: {test_users.count()}')
        self.stdout.write(f'关联申请: {test_apps.count()}')
        self.stdout.write(f'关联审批: {test_approvals.count()}')
        self.stdout.write(f'关联通知: {test_notifications.count()}')

        if dry_run:
            self.stdout.write(self.style.WARNING('\n[DRY RUN] 未实际删除数据'))
            transaction.set_rollback(True)
        else:
            # 删除顺序：通知→审批→申请→用户
            deleted_notif = test_notifications.delete()
            self.stdout.write(f'\n✓ 删除通知: {deleted_notif[0]}条')

            deleted_approvals = test_approvals.delete()
            self.stdout.write(f'✓ 删除审批: {deleted_approvals[0]}条')

            deleted_apps = test_apps.delete()
            self.stdout.write(f'✓ 删除申请: {deleted_apps[0]}条')

            deleted_users = test_users.delete()
            self.stdout.write(f'✓ 删除用户: {deleted_users[0]}条')

            remaining = User.objects.count()
            self.stdout.write(self.style.SUCCESS(f'\n剩余用户: {remaining}'))
