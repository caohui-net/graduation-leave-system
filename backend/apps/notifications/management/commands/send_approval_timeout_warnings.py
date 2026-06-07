from django.core.management.base import BaseCommand
from apps.notifications.services import create_approval_timeout_warnings


class Command(BaseCommand):
    help = 'Send approval timeout warning notifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate without creating notifications'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No notifications will be created'))

        result = create_approval_timeout_warnings(dry_run=dry_run)

        self.stdout.write(self.style.SUCCESS(
            f"Created: {result['created']}, Skipped: {result['skipped']}"
        ))

        if result['warnings']:
            self.stdout.write('\nWarnings:')
            for warning in result['warnings']:
                self.stdout.write(
                    f"  - Approval {warning['approval_id']}: "
                    f"{warning['approver']} ({warning['days']} days)"
                )
