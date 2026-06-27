from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Reset passwords for test environment. NEVER USE IN PRODUCTION.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--role',
            type=str,
            help='Filter users by role (e.g., student, admin, counselor)',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='123456',
            help='Password to set. Use "userid" to set password same as user_id. Defaults to "123456".',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force run even if it looks like production (requires ALLOW_DANGEROUS_COMMANDS=true).',
        )

    def handle(self, *args, **options):
        # 1. 安全检查
        if not settings.DEBUG:
            if not options['force'] or os.environ.get('ALLOW_DANGEROUS_COMMANDS') != 'true':
                raise CommandError(
                    "DANGER: settings.DEBUG is False. This script should not run in production. "
                    "Use --force and set ALLOW_DANGEROUS_COMMANDS=true if you really know what you are doing."
                )
        
        # 追加防御：基于域名或常用标志拦截
        if hasattr(settings, 'ALLOWED_HOSTS') and any('218.75.196.218' in host for host in settings.ALLOWED_HOSTS):
             if not options['force']:
                 raise CommandError("DANGER: 218.75.196.218 found in ALLOWED_HOSTS. Aborting to protect production.")

        User = get_user_model()
        role_filter = options['role']
        password_input = options['password']

        qs = User.objects.all()
        if role_filter:
            qs = qs.filter(role=role_filter)

        count = qs.count()
        if count == 0:
            self.stdout.write(self.style.WARNING("No users found matching criteria."))
            return

        self.stdout.write(self.style.NOTICE(f"Found {count} users. Updating passwords..."))
        
        updated_count = 0
        for user in qs:
            pwd = user.user_id if password_input == 'userid' else password_input
            user.set_password(pwd)
            user.save(update_fields=['password'])
            updated_count += 1
            
            if updated_count % 1000 == 0:
                 self.stdout.write(f"Processed {updated_count}/{count} users...")

        self.stdout.write(self.style.SUCCESS(f'Successfully reset password for {updated_count} users.'))
