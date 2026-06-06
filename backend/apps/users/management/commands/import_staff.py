"""
Django management command to import staff from CSV.

Supports staff types: DORM_MANAGER, COUNSELOR, ADMIN.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.users.models import User, UserRole
import csv
from pathlib import Path


class Command(BaseCommand):
    help = 'Import staff (dorm managers, counselors, admins) from CSV'

    def add_arguments(self, parser):
        parser.add_argument('--file', required=True, help='Input CSV file path')
        parser.add_argument('--dry-run', action='store_true', help='Dry run without writing to DB')

    def handle(self, *args, **options):
        file_path = options['file']
        dry_run = options['dry_run']

        if not Path(file_path).exists():
            raise CommandError(f'File not found: {file_path}')

        stats = self._import_staff(file_path, dry_run)
        self._print_results(stats, dry_run)

    def _import_staff(self, file_path, dry_run):
        stats = {
            'total': 0,
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'errors': [],
            'by_role': {}
        }

        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            # Support both Chinese and English column names
            rows = list(reader)
            stats['total'] = len(rows)

            with transaction.atomic():
                for row in rows:
                    try:
                        self._process_row(row, stats, dry_run)
                    except Exception as e:
                        stats['errors'].append(f"Row {stats['total']}: {str(e)}")

                if dry_run:
                    transaction.set_rollback(True)

        return stats

    def _process_row(self, row, stats, dry_run):
        # Support both Chinese and English column names
        user_id = (row.get('职工号') or row.get('user_id') or '').strip()
        name = (row.get('姓名') or row.get('name') or '').strip()
        role_str = (row.get('角色') or row.get('role') or '').strip()
        phone = (row.get('手机') or row.get('phone') or '').strip()
        building = (row.get('楼栋') or row.get('building') or '').strip()

        if not user_id or not name or not role_str:
            stats['skipped'] += 1
            stats['errors'].append(f'Missing required fields: user_id={user_id}, name={name}, role={role_str}')
            return

        # Map role string to UserRole
        role_map = {
            '宿管员': UserRole.DORM_MANAGER,
            'DORM_MANAGER': UserRole.DORM_MANAGER,
            '辅导员': UserRole.COUNSELOR,
            'COUNSELOR': UserRole.COUNSELOR,
            '学工管理员': UserRole.ADMIN,
            'ADMIN': UserRole.ADMIN,
        }

        role = role_map.get(role_str)
        if not role:
            stats['skipped'] += 1
            stats['errors'].append(f'{user_id}: Unknown role "{role_str}"')
            return

        # Validate building requirement
        if role == UserRole.DORM_MANAGER and not building:
            # Allow empty building for fallback dorm manager
            from django.conf import settings
            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
            if user_id != fallback_id:
                self.stdout.write(
                    self.style.WARNING(
                        f'{user_id} ({name}): DORM_MANAGER without building (not fallback manager)'
                    )
                )

        if dry_run:
            exists = User.objects.filter(user_id=user_id).exists()
            if exists:
                stats['updated'] += 1
            else:
                stats['created'] += 1
            stats['by_role'][role] = stats['by_role'].get(role, 0) + 1
        else:
            user, created = User.objects.update_or_create(
                user_id=user_id,
                defaults={
                    'name': name,
                    'role': role,
                    'phone': phone if phone else None,
                    'building': building if building else None,
                    'active': True,
                }
            )

            if created:
                stats['created'] += 1
            else:
                stats['updated'] += 1

            stats['by_role'][role] = stats['by_role'].get(role, 0) + 1

    def _print_results(self, stats, dry_run):
        mode_label = 'DRY RUN' if dry_run else 'IMPORT'
        self.stdout.write(f'\n=== {mode_label} RESULTS ===')
        self.stdout.write(f'Total rows: {stats["total"]}')
        self.stdout.write(f'Created: {stats["created"]}')
        self.stdout.write(f'Updated: {stats["updated"]}')
        self.stdout.write(f'Skipped: {stats["skipped"]}')

        if stats['by_role']:
            self.stdout.write('\nBy role:')
            for role, count in stats['by_role'].items():
                self.stdout.write(f'  {role}: {count}')

        if stats['errors']:
            self.stdout.write(self.style.WARNING(f'\nErrors ({len(stats["errors"])}):'))
            for err in stats['errors'][:10]:
                self.stdout.write(f'  - {err}')
            if len(stats['errors']) > 10:
                self.stdout.write(f'  ... and {len(stats['errors']) - 10} more')

        if not dry_run and len(stats['errors']) == 0:
            self.stdout.write(self.style.SUCCESS(f'\n✓ Import successful'))
