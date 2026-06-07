#!/usr/bin/env python3
"""
研究生数据导入脚本
Import graduate students with building and department data
"""
import os
import sys
import django
import csv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User

def import_graduates(csv_file, dry_run=True):
    """
    Import graduate students from CSV

    CSV format: 学号,姓名,building,department
    """
    stats = {
        'total': 0,
        'created': 0,
        'updated': 0,
        'skipped': 0,
        'errors': []
    }

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            stats['total'] += 1
            user_id = row['学号'].strip()
            name = row['姓名'].strip()
            building = row['building'].strip()
            department = row['department'].strip()

            # Validation
            if not user_id or not name:
                stats['errors'].append(f"Row {stats['total']}: Missing user_id or name")
                stats['skipped'] += 1
                continue

            if not building:
                stats['errors'].append(f"Row {stats['total']} ({user_id}): Missing building")
                stats['skipped'] += 1
                continue

            if not department:
                stats['errors'].append(f"Row {stats['total']} ({user_id}): Missing department")
                stats['skipped'] += 1
                continue

            if dry_run:
                print(f"[DRY-RUN] Would import: {user_id} | {name} | {building} | {department}")
                stats['created'] += 1
            else:
                try:
                    user, created = User.objects.update_or_create(
                        user_id=user_id,
                        defaults={
                            'name': name,
                            'role': 'student',
                            'building': building,
                            'department': department,
                            'class_id': None,
                            'is_graduating': True,
                            'graduation_year': 2026,
                        }
                    )
                    if created:
                        stats['created'] += 1
                        print(f"✓ Created: {user_id} | {name}")
                    else:
                        stats['updated'] += 1
                        print(f"✓ Updated: {user_id} | {name}")
                except Exception as e:
                    stats['errors'].append(f"{user_id}: {str(e)}")
                    stats['skipped'] += 1

    print("\n" + "="*60)
    print("Import Summary")
    print("="*60)
    print(f"Total rows: {stats['total']}")
    print(f"Created: {stats['created']}")
    print(f"Updated: {stats['updated']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"Errors: {len(stats['errors'])}")

    if stats['errors']:
        print("\nErrors:")
        for error in stats['errors'][:10]:
            print(f"  - {error}")
        if len(stats['errors']) > 10:
            print(f"  ... and {len(stats['errors']) - 10} more")

    return stats

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Import graduate students')
    parser.add_argument('csv_file', help='CSV file with graduate data')
    parser.add_argument('--apply', action='store_true', help='Apply changes (default is dry-run)')

    args = parser.parse_args()

    dry_run = not args.apply

    if dry_run:
        print("=== DRY-RUN MODE (use --apply to execute) ===\n")

    stats = import_graduates(args.csv_file, dry_run=dry_run)

    sys.exit(0 if stats['skipped'] == 0 else 1)
