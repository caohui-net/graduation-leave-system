#!/usr/bin/env python3
"""
导入用户数据：辅导员和学生
"""
import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.users.models import User, UserRole
import openpyxl
import xlrd

def import_counselors(file_path):
    """导入辅导员数据"""
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    created = 0
    updated = 0

    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[3]:  # 职工号为空，跳过
            continue

        user_id = str(row[3])  # 职工号
        name = row[2]  # 姓名
        phone = str(row[4]) if row[4] else None  # 电话
        department = row[1]  # 学院

        user, is_created = User.objects.update_or_create(
            user_id=user_id,
            defaults={
                'name': name,
                'role': UserRole.COUNSELOR,
                'phone': phone,
                'department': department,
                'active': True,
            }
        )

        if is_created:
            created += 1
        else:
            updated += 1

    print(f"✅ 辅导员: 新增 {created}, 更新 {updated}")

def import_students(file_path):
    """导入学生数据"""
    wb = xlrd.open_workbook(file_path)
    ws = wb.sheet_by_index(0)

    created = 0
    updated = 0

    for i in range(1, ws.nrows):
        row = ws.row_values(i)

        user_id = str(int(row[0])) if isinstance(row[0], float) else str(row[0])  # 学号
        name = row[1]  # 姓名
        gender = row[2]  # 性别
        department = row[4]  # 学院
        major = row[5]  # 专业
        class_id = row[6]  # 班级
        level = row[7]  # 层次

        user, is_created = User.objects.update_or_create(
            user_id=user_id,
            defaults={
                'name': name,
                'role': UserRole.STUDENT,
                'gender': gender,
                'department': department,
                'major': major,
                'class_id': class_id,
                'level': level,
                'active': True,
            }
        )

        if is_created:
            created += 1
        else:
            updated += 1

    print(f"✅ 学生: 新增 {created}, 更新 {updated}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(__file__))

    print("开始导入用户数据...\n")

    # 导入辅导员
    counselor_file = os.path.join(base_dir, 'docs/20260622-暑期留校名单审批的辅导员教师信息统计表.xlsx')
    import_counselors(counselor_file)

    # 导入学生
    student_file = os.path.join(base_dir, 'docs/15975名在校生（不含毕业生）.xls')
    import_students(student_file)

    print("\n✅ 导入完成")
