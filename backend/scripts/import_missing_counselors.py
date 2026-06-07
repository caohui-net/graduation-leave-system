#!/usr/bin/env python3
"""导入3个缺失学院的辅导员"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User

# 3个缺失学院的辅导员数据
counselors = [
    {
        'user_id': '20220048',
        'name': '吴灿',
        'department': '文学院（苏东坡书院）',
        'phone': '19186463550'
    },
    {
        'user_id': '20210054',
        'name': '郑红妍',
        'department': '生物与农业资源学院',
        'phone': '13387118599'
    },
    {
        'user_id': '20240020',
        'name': '王娜娜',
        'department': '音乐学院、黄梅戏学院',
        'phone': '15507175955'
    }
]

print(f"准备导入{len(counselors)}名辅导员")

stats = {'created': 0, 'updated': 0, 'errors': []}

for item in counselors:
    try:
        user, created = User.objects.update_or_create(
            user_id=item['user_id'],
            defaults={
                'name': item['name'],
                'role': 'counselor',
                'department': item['department'],
                'phone': item.get('phone', ''),
                'email': '',
                'building': ''
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
print("导入汇总")
print("="*60)
print(f"创建: {stats['created']}")
print(f"更新: {stats['updated']}")
print(f"错误: {len(stats['errors'])}")

if stats['errors']:
    print(f"\n错误清单:")
    for err in stats['errors']:
        print(f"  {err}")

sys.exit(0 if len(stats['errors']) == 0 else 1)
