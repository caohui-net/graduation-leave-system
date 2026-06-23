"""
导入用户数据：辅导员和学生
"""
from django.core.management.base import BaseCommand
from apps.users.models import User, UserRole
import openpyxl
import xlrd
import os

class Command(BaseCommand):
    help = '导入辅导员和学生数据'

    def handle(self, *args, **options):
        base_dir = '/app'

        # 导入辅导员
        counselor_file = os.path.join(base_dir, 'docs/20260622-暑期留校名单审批的辅导员教师信息统计表.xlsx')
        self.import_counselors(counselor_file)

        # 导入学生
        student_file = os.path.join(base_dir, 'docs/15975名在校生（不含毕业生）.xls')
        self.import_students(student_file)

        self.stdout.write(self.style.SUCCESS('✅ 导入完成'))

    def import_counselors(self, file_path):
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active

        created = 0
        updated = 0

        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row[3]:
                continue

            user_id = str(row[3])
            name = row[2]
            phone = str(row[4])[:20] if row[4] else None  # 截断到20字符
            department = row[1]

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

        self.stdout.write(f'辅导员: 新增 {created}, 更新 {updated}')

    def import_students(self, file_path):
        wb = xlrd.open_workbook(file_path)
        ws = wb.sheet_by_index(0)

        created = 0
        updated = 0

        for i in range(1, ws.nrows):
            row = ws.row_values(i)

            user_id = str(int(row[0])) if isinstance(row[0], float) else str(row[0])
            name = row[1]
            gender = row[2]
            department = row[4]
            major = row[5]
            class_id = row[6]
            level = row[7]

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

        self.stdout.write(f'学生: 新增 {created}, 更新 {updated}')
