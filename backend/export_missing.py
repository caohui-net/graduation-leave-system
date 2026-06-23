#!/usr/bin/env python3
"""导出缺失性别/专业的学生记录"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User, UserRole
import openpyxl

# 查询缺失记录
missing = User.objects.filter(
    role=UserRole.STUDENT,
    gender__isnull=True
).values_list('user_id', 'name', 'department', 'class_id', 'level')

# 创建Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "缺失数据"

# 表头
ws.append(['学号', '姓名', '学院', '班级', '层次', '性别(缺失)', '专业(缺失)'])

# 数据
for record in missing:
    ws.append(list(record) + ['', ''])

# 保存
output_file = '/app/docs/缺失数据-154条.xlsx'
wb.save(output_file)
print(f'✅ 导出完成: {output_file}')
print(f'共 {len(list(missing))} 条记录')
