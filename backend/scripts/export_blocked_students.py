#!/usr/bin/env python3
"""导出阻塞学生数据到CSV"""
import sys
from pathlib import Path
import csv

sys.path.insert(0, str(Path(__file__).parent.parent))
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User

# 3个无辅导员覆盖的学院
blocked_departments = [
    '音乐学院、黄梅戏学院',
    '文学院（苏东坡书院）',
    '生物与农业资源学院'
]

print(f"查询{len(blocked_departments)}个无辅导员覆盖的学院...")

blocked_students = User.objects.filter(
    role='student',
    department__in=blocked_departments
).order_by('department', 'user_id')

print(f"找到{blocked_students.count()}名阻塞学生")

# 导出CSV
output_file = Path(__file__).parent.parent.parent / 'docs' / 'blocked_students_72.csv'

with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['学号', '姓名', '学院', '楼栋', '班级', '阻塞原因'])

    for s in blocked_students:
        writer.writerow([
            s.user_id,
            s.name,
            s.department,
            s.building or '(无)',
            s.class_id or '(无)',
            f'学院"{s.department}"无辅导员覆盖'
        ])

print(f"✓ 导出完成: {output_file}")
print(f"  共{blocked_students.count()}人")

# 按学院统计
from django.db.models import Count
dept_stats = blocked_students.values('department').annotate(count=Count('user_id'))
print(f"\n学院分布:")
for stat in dept_stats:
    print(f"  {stat['department']}: {stat['count']}人")
