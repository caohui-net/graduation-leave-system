"""
修复 class_id 字段 - 从CSV和Excel源文件恢复正确的班级名称

数据源:
- 毕业生: data/file5_students_merged_v2.csv
- 在校生: docs/15975名在校生（不含毕业生）.xls
"""

from django.core.management.base import BaseCommand
import csv
import xlrd
from apps.users.models import User


class Command(BaseCommand):
    help = '修复class_id字段'

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true', help='实际执行修复（默认dry-run）')

    def handle(self, *args, **options):
        dry_run = not options['apply']

        # 加载毕业生数据
        csv_path = 'data/file5_students_merged_v2.csv'
        graduating = {}

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = row.get('user_id', '').strip()
                class_id = row.get('class_id', '').strip()
                if user_id and class_id:
                    graduating[user_id] = class_id

        self.stdout.write(f"CSV加载 {len(graduating)} 条毕业生记录")

        # 加载在校生数据
        excel_path = 'docs/15975名在校生（不含毕业生）.xls'
        current = {}

        wb = xlrd.open_workbook(excel_path)
        sheet = wb.sheet_by_index(0)
        headers = [sheet.cell_value(0, col) for col in range(sheet.ncols)]
        user_id_col = headers.index('学号')
        class_col = headers.index('班级')

        for row_idx in range(1, sheet.nrows):
            user_id = str(int(sheet.cell_value(row_idx, user_id_col))).strip()
            class_name = sheet.cell_value(row_idx, class_col).strip()
            if user_id and class_name:
                current[user_id] = class_name

        self.stdout.write(f"Excel加载 {len(current)} 条在校生记录")

        # 合并映射
        all_mapping = {**current, **graduating}
        self.stdout.write(f"总计映射 {len(all_mapping)} 条记录\n")

        # 修复
        students = User.objects.filter(role='student')
        total = students.count()
        updated = 0
        already_correct = 0
        not_found = 0

        self.stdout.write(f"开始处理 {total} 名学生...\n")

        for student in students:
            user_id = student.user_id
            current_class_id = student.class_id or ''

            if user_id in all_mapping:
                correct_class_id = all_mapping[user_id]

                if current_class_id == correct_class_id:
                    already_correct += 1
                else:
                    if not dry_run:
                        student.class_id = correct_class_id
                        student.save(update_fields=['class_id'])
                    updated += 1

                    if updated <= 5:
                        self.stdout.write(f"  {user_id}: '{current_class_id}' → '{correct_class_id}'")
            else:
                not_found += 1
                if not_found <= 5:
                    self.stdout.write(f"  ⚠ {user_id} 未在源数据中找到")

        self.stdout.write(f"\n修复统计:")
        self.stdout.write(f"  需要更新: {updated}")
        self.stdout.write(f"  已正确: {already_correct}")
        self.stdout.write(f"  未找到: {not_found}")
        self.stdout.write(f"  总计: {total}")

        if dry_run:
            self.stdout.write(self.style.WARNING("\n** DRY RUN 模式 - 未实际修改数据 **"))
        else:
            self.stdout.write(self.style.SUCCESS("\n** 修复完成！**"))
