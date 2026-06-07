"""
Django management command to cleanup test data before real data import.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, connection
from apps.users.models import User
from apps.applications.models import Application


class Command(BaseCommand):
    help = 'Cleanup test data (delete all users when count < 100)'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Preview without deleting')

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # Safety check
        total_users = User.objects.count()
        if total_users >= 100:
            raise CommandError(
                f'安全检查失败: 当前有{total_users}个用户（>=100），'
                '可能是真实数据，拒绝清理。'
            )

        # Get counts by role
        stats = {
            'total_users': total_users,
            'students': User.objects.filter(role='student').count(),
            'dorm_managers': User.objects.filter(role='dorm_manager').count(),
            'counselors': User.objects.filter(role='counselor').count(),
            'admins': User.objects.filter(role='admin').count(),
            'applications': Application.objects.count(),
        }

        if dry_run:
            self.stdout.write('\n=== DRY RUN: 预览清理内容 ===')
            self.stdout.write(f'总用户: {stats["total_users"]}')
            self.stdout.write(f'  - 学生: {stats["students"]}')
            self.stdout.write(f'  - 宿管: {stats["dorm_managers"]}')
            self.stdout.write(f'  - 辅导: {stats["counselors"]}')
            self.stdout.write(f'  - 管理: {stats["admins"]}')
            self.stdout.write(f'申请数: {stats["applications"]}')
            self.stdout.write('\n✓ Dry run完成，未删除数据\n')
        else:
            self.stdout.write('\n=== 清理测试数据 ===')

            with transaction.atomic():
                # Use raw SQL to delete approvals and notifications (bypasses ORM)
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM approvals")
                    apv_deleted = cursor.rowcount

                    cursor.execute("DELETE FROM notifications")
                    notif_deleted = cursor.rowcount

                # Then delete Applications and Users via ORM
                app_deleted = Application.objects.all().delete()[0]
                user_deleted = User.objects.all().delete()[0]

                self.stdout.write(f'✓ 删除审批: {apv_deleted}条')
                self.stdout.write(f'✓ 删除通知: {notif_deleted}条')
                self.stdout.write(f'✓ 删除申请: {app_deleted}条')
                self.stdout.write(f'✓ 删除用户: {user_deleted}个')
                self.stdout.write(self.style.SUCCESS('\n清理完成\n'))
