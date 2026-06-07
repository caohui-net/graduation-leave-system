#!/usr/bin/env python3
"""标准化学生学院名称以匹配辅导员学院名称"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User

# 学院名称标准化映射
DEPT_MAPPING = {
    '音乐与戏剧学院': '音乐学院、黄梅戏学院',
    '文学院(苏东坡书院)': '文学院（苏东坡书院）',  # 半角→全角
    '文学院': '文学院（苏东坡书院）'  # 假设单独的"文学院"也属于苏东坡书院
}

print("学院名称标准化")
print("="*60)

stats = {'updated': 0, 'errors': []}

for old_name, new_name in DEPT_MAPPING.items():
    students = User.objects.filter(role='student', department=old_name)
    count = students.count()

    if count == 0:
        print(f"跳过: {old_name} (0人)")
        continue

    print(f"\n{old_name} → {new_name}")
    print(f"  影响学生: {count}人")

    try:
        updated = students.update(department=new_name)
        stats['updated'] += updated
        print(f"  ✓ 更新: {updated}人")
    except Exception as e:
        stats['errors'].append(f"{old_name}: {str(e)}")
        print(f"  ✗ 错误: {e}")

print(f"\n{'='*60}")
print("标准化汇总")
print("="*60)
print(f"更新学生: {stats['updated']}人")
print(f"错误: {len(stats['errors'])}")

if stats['errors']:
    print(f"\n错误清单:")
    for err in stats['errors']:
        print(f"  {err}")

sys.exit(0 if len(stats['errors']) == 0 else 1)
