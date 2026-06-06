"""
Django management command to import students from File5 CSV.

Supports File5 format with building_name field.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.users.models import User, UserRole
import csv
from pathlib import Path


class Command(BaseCommand):
    help = 'Import students from File5 CSV (v2 format with real student numbers)'

    def add_arguments(self, parser):
        parser.add_argument('--file', required=True, help='Input CSV file path')
        parser.add_argument('--dry-run', action='store_true', help='Dry run without writing to DB')
        parser.add_argument('--mode', choices=['append', 'clean'], default='append',
                            help='Import mode: append (default) or clean (delete all students first)')

    def handle(self, *args, **options):
        file_path = options['file']
        dry_run = options['dry_run']
        mode = options['mode']

        if not Path(file_path).exists():
            raise CommandError(f'File not found: {file_path}')

        # Safety check for clean mode
        if mode == 'clean' and not dry_run:
            from apps.applications.models import Application
            active_apps = Application.objects.exclude(status='rejected').count()
            if active_apps > 0:
                raise CommandError(
                    f'Cannot clean import: {active_apps} active applications exist. '
                    'Use append mode or manually clear applications first.'
                )

        stats = self._import_students(file_path, dry_run, mode)
        self._print_results(stats, dry_run)

    def _import_students(self, file_path, dry_run, mode):
        stats = {
            'total': 0,
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'errors': []
        }

        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            # Validate required columns
            required = ['user_id', 'name', 'class_id']
            missing = [col for col in required if col not in reader.fieldnames]
            if missing:
                raise CommandError(f'Missing required columns: {", ".join(missing)}')

            if mode == 'clean' and not dry_run:
                deleted = User.objects.filter(role=UserRole.STUDENT).delete()
                self.stdout.write(f'Deleted {deleted[0]} existing students')

            rows = list(reader)
            stats['total'] = len(rows)

            with transaction.atomic():
                for row in rows:
                    try:
                        self._process_row(row, stats, dry_run)
                    except Exception as e:
                        stats['errors'].append(f"Row {stats['total']}: {str(e)}")

                if dry_run:
                    # Rollback transaction in dry-run
                    raise Exception('Dry run - rolling back')

        return stats

    def _process_row(self, row, stats, dry_run):
        user_id = row['user_id'].strip()
        name = row['name'].strip()
        department = row.get('department', '').strip()
        class_id = row.get('class_id', '').strip()
        building = row.get('building_name', '').strip()
        phone = row.get('phone', '').strip()
        email = row.get('email', '').strip()
        graduation_year = int(row.get('graduation_year', 2026))

        # Skip TMP IDs
        if user_id.startswith('TMP2026_'):
            stats['skipped'] += 1
            stats['errors'].append(f'{user_id}: TMP ID not allowed in import')
            return

        if dry_run:
            # Dry run: just count
            exists = User.objects.filter(user_id=user_id).exists()
            if exists:
                stats['updated'] += 1
            else:
                stats['created'] += 1
        else:
            # Real import
            user, created = User.objects.update_or_create(
                user_id=user_id,
                defaults={
                    'name': name,
                    'department': department,
                    'class_id': class_id,
                    'building': building if building else None,
                    'phone': phone if phone else None,
                    'email': email if email else None,
                    'role': UserRole.STUDENT,
                    'graduation_year': graduation_year,
                    'is_graduating': True,
                    'active': True,
                }
            )

            if created:
                stats['created'] += 1
            else:
                stats['updated'] += 1

    def _print_results(self, stats, dry_run):
        mode_label = 'DRY RUN' if dry_run else 'IMPORT'
        self.stdout.write(f'\n=== {mode_label} RESULTS ===')
        self.stdout.write(f'Total rows: {stats["total"]}')
        self.stdout.write(f'Created: {stats["created"]}')
        self.stdout.write(f'Updated: {stats["updated"]}')
        self.stdout.write(f'Skipped: {stats["skipped"]}')

        if stats['errors']:
            self.stdout.write(self.style.WARNING(f'\nErrors ({len(stats["errors"])}):'))
            for err in stats['errors'][:10]:
                self.stdout.write(f'  - {err}')
            if len(stats['errors']) > 10:
                self.stdout.write(f'  ... and {len(stats["errors"]) - 10} more')

        if not dry_run and len(stats['errors']) == 0:
            self.stdout.write(self.style.SUCCESS(f'\n✓ Import successful'))
