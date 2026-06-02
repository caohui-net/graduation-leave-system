"""XG用户同步管理命令"""
from django.core.management.base import BaseCommand
from apps.users.integrations.xg_user_client import XGUserAPIClient
from apps.users.services.xg_user_sync import apply_xg_user_sync


class Command(BaseCommand):
    help = 'Sync users from XG system to local database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply',
            action='store_true',
            help='Apply changes to database (default is dry-run)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit number of users to fetch (for testing)'
        )

    def handle(self, *args, **options):
        apply_mode = options['apply']
        limit = options.get('limit')

        self.stdout.write('Fetching users from XG API...')

        client = XGUserAPIClient()
        users = []

        try:
            for page_users in client.fetch_all_users():
                users.extend(page_users)
                if limit and len(users) >= limit:
                    users = users[:limit]
                    break
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching users: {e}'))
            return

        self.stdout.write(f'Fetched {len(users)} users')

        mode_str = 'apply mode' if apply_mode else 'dry-run mode'
        self.stdout.write(f'Running sync ({mode_str})...')

        result = apply_xg_user_sync(users, dry_run=not apply_mode)

        self.stdout.write(self.style.SUCCESS('\nSync completed!'))
        self.stdout.write(f'\nResults:')
        self.stdout.write(f'  Total fetched: {result["total_fetched"]}')
        self.stdout.write(f'  Mapped: {result["mapped_count"]}')
        self.stdout.write(f'  Skipped: {result["skipped_count"]}')
        self.stdout.write(f'  Updated: {result["updated_count"]}')
        self.stdout.write(f'  Conflicts: {len(result["conflicts"])}')
        self.stdout.write(f'  Missing local: {result["missing_local_count"]}')

        if result['skipped_by_reason']:
            self.stdout.write('\nSkip reasons:')
            for reason, count in result['skipped_by_reason'].items():
                self.stdout.write(f'  {reason}: {count}')

        if result['conflicts']:
            self.stdout.write(self.style.WARNING(f'\n{len(result["conflicts"])} conflicts detected'))

        if not apply_mode:
            self.stdout.write(self.style.WARNING('\nDry-run mode: no changes written to database'))
            self.stdout.write('Use --apply to write changes')
