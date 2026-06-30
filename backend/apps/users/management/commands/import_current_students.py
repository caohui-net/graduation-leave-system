"""
Django management command to import current students from Excel.

Imports 15,975 current students (non-graduating) with level field mapping.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.users.models import User, UserRole
import xlrd
from pathlib import Path


class Command(BaseCommand):
    help = 'Import current students from Excel (15975名在校生)'

    def add_arguments(self, parser):
        parser.add_argument('file', help='Input Excel file path')
        parser.add_argument('--dry-run', action='store_true', help='Dry run without writing to DB')
        parser.add_argument('--mode', choices=['append', 'update'], default='update',
                            help='Import mode: append (create only) or update (update existing)')

    def handle(self, *args, **options):
        file_path = options['file']
        dry_run = options['dry_run']
        mode = options['mode']

        if not Path(file_path).exists():
            raise CommandError(f'File not found: {file_path}')

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

        try:
            wb = xlrd.open_workbook(file_path)
            sheet = wb.sheet_by_index(0)
        except Exception as e:
            raise CommandError(f'Failed to read Excel: {str(e)}')

        # Validate header row
        headers = [sheet.cell(0, i).value for i in range(sheet.ncols)]
        expected = ['学号', '姓名', '性别', '年级', '学院名称', '专业', '班级', '层次', '学制']
        if headers != expected:
            raise CommandError(f'Unexpected columns. Expected: {expected}, Got: {headers}')

        stats['total'] = sheet.nrows - 1  # Exclude header

        with transaction.atomic():
            for row_idx in range(1, sheet.nrows):
                try:
                    self._process_row(sheet, row_idx, stats, dry_run, mode)
                except Exception as e:
                    stats['errors'].append(f"Row {row_idx + 1}: {str(e)}")

            if dry_run:
                transaction.set_rollback(True)

        return stats

    def _process_row(self, sheet, row_idx, stats, dry_run, mode):
        # Extract fields (0-indexed)
        user_id = str(sheet.cell(row_idx, 0).value).strip()
        name = str(sheet.cell(row_idx, 1).value).strip()
        gender = str(sheet.cell(row_idx, 2).value).strip() if sheet.cell(row_idx, 2).value else ''
        grade = str(sheet.cell(row_idx, 3).value).strip() if sheet.cell(row_idx, 3).value else ''
        department = str(sheet.cell(row_idx, 4).value).strip()
        major = str(sheet.cell(row_idx, 5).value).strip() if sheet.cell(row_idx, 5).value else ''
        class_id = str(sheet.cell(row_idx, 6).value).strip() if sheet.cell(row_idx, 6).value else ''
        level = str(sheet.cell(row_idx, 7).value).strip()  # 层次 -> level
        duration = str(sheet.cell(row_idx, 8).value).strip() if sheet.cell(row_idx, 8).value else ''

        # Validate required fields
        if not user_id or not name or not department:
            stats['skipped'] += 1
            stats['errors'].append(f'Row {row_idx + 1}: Missing required field (user_id/name/department)')
            return

        # Clean user_id (remove .0 from Excel number format)
        if user_id.endswith('.0'):
            user_id = user_id[:-2]

        if dry_run:
            # Dry run: just count
            exists = User.objects.filter(user_id=user_id).exists()
            if exists:
                stats['updated'] += 1
            else:
                stats['created'] += 1
        else:
            # Real import
            if mode == 'append':
                # Create only if not exists
                if User.objects.filter(user_id=user_id).exists():
                    stats['skipped'] += 1
                    return

                User.objects.create(
                    user_id=user_id,
                    name=name,
                    gender=gender if gender else None,
                    department=department,
                    major=major if major else None,
                    class_id=class_id if class_id else None,
                    level=level if level else None,  # ✓ Map 层次 to level
                    role=UserRole.STUDENT,
                    is_graduating=None,  # Current students
                    active=True,
                )
                stats['created'] += 1
            else:
                # Update existing records
                user, created = User.objects.update_or_create(
                    user_id=user_id,
                    defaults={
                        'name': name,
                        'gender': gender if gender else None,
                        'department': department,
                        'major': major if major else None,
                        'class_id': class_id if class_id else None,
                        'level': level if level else None,  # ✓ Map 层次 to level
                        'role': UserRole.STUDENT,
                        'is_graduating': None,
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
