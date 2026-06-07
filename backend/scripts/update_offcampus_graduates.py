#!/usr/bin/env python3
"""更新17名校外住宿研究生的department字段"""
import sys
from pathlib import Path
import csv

sys.path.insert(0, str(Path(__file__).parent.parent))
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User

# 读取17名研究生学院归属
mapping_file = Path(__file__).parent.parent.parent / 'docs' / '17名研究生学院归属.csv'

updates = []
with open(mapping_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        updates.append({
            'user_id': row['学号'].strip(),
            'name': row['姓名'].strip(),
            'department': row['学院名称'].strip(),
            'note': row['备注'].strip()
        })

print(f"准备更新{len(updates)}名校外住宿研究生")

stats = {'updated': 0, 'created': 0, 'errors': []}

for item in updates:
    try:
        user, created = User.objects.update_or_create(
            user_id=item['user_id'],
            defaults={
                'name': item['name'],
                'role': 'student',
                'department': item['department'],
                'building': '',  # 校外住宿，留空触发兜底
                'is_graduating': True,
                'graduation_year': 2026,
                'class_id': None
            }
        )
        if created:
            stats['created'] += 1
            print(f"✓ 创建: {item['user_id']} | {item['name']} | {item['department']}")
        else:
            stats['updated'] += 1
            print(f"✓ 更新: {item['user_id']} | {item['name']} | {item['department']}")
    except Exception as e:
        stats['errors'].append(f"{item['user_id']}: {str(e)}")
        print(f"✗ 错误: {item['user_id']}: {e}")

print(f"\n{'='*60}")
print("更新汇总")
print("="*60)
print(f"创建: {stats['created']}")
print(f"更新: {stats['updated']}")
print(f"错误: {len(stats['errors'])}")

if stats['errors']:
    print(f"\n错误清单:")
    for err in stats['errors']:
        print(f"  {err}")

sys.exit(0 if len(stats['errors']) == 0 else 1)
