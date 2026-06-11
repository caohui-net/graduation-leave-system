#!/usr/bin/env python3
"""导入学生宿舍数据"""
import os
import sys
import django
import xlrd

# Django setup
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.users.models import User

def import_students(filepath, dry_run=False):
    wb = xlrd.open_workbook(filepath)
    sh = wb.sheet_by_index(0)

    updated = 0
    skipped = 0
    errors = []

    print(f"{'[DRY RUN] ' if dry_run else ''}开始处理 {sh.nrows - 1} 条记录...\n")

    # Skip header row
    for row_idx in range(1, sh.nrows):
        try:
            campus = sh.cell_value(row_idx, 0)
            building = sh.cell_value(row_idx, 1)
            room_number = sh.cell_value(row_idx, 2)
            name = sh.cell_value(row_idx, 3)
            gender = sh.cell_value(row_idx, 4)
            major = sh.cell_value(row_idx, 5)
            department = sh.cell_value(row_idx, 6)
            class_id = sh.cell_value(row_idx, 7)
            level = sh.cell_value(row_idx, 8)
            year = sh.cell_value(row_idx, 9)

            # Convert room_number to string
            if isinstance(room_number, float):
                room_number = str(int(room_number))
            else:
                room_number = str(room_number)

            # Convert year to int
            if isinstance(year, float):
                year = int(year)
            elif isinstance(year, str) and year.isdigit():
                year = int(year)
            else:
                year = None

            # 匹配策略：姓名+楼栋双重验证
            users = User.objects.filter(name=name, building=building, role='student')

            if users.exists():
                user = users.first()

                if not dry_run:
                    # 仅更新新字段，不覆盖已有数据
                    user.campus = campus
                    user.room_number = room_number
                    if not user.gender:
                        user.gender = gender
                    if not user.major:
                        user.major = major
                    if not user.level:
                        user.level = level
                    user.save()

                updated += 1
            else:
                # 不创建新用户，记录跳过
                skipped += 1
                if skipped <= 5:  # Only log first 5
                    errors.append(f"Row {row_idx + 1}: 未找到匹配用户 - {name} @ {building}")

        except Exception as e:
            errors.append(f"Row {row_idx + 1}: {str(e)}")

    print(f"\n{'[DRY RUN] ' if dry_run else ''}导入完成:")
    print(f"  匹配更新: {updated}")
    print(f"  未匹配跳过: {skipped}")
    if errors:
        print(f"\n前{min(len(errors), 10)}条信息:")
        for err in errors[:10]:
            print(f"    {err}")

if __name__ == '__main__':
    import sys
    filepath = '/home/caohui/projects/graduation-leave-system/docs/1-5830名毕业生（含研究生）.xls'

    # Dry run test first
    dry_run = '--dry-run' in sys.argv or '-d' in sys.argv

    if dry_run:
        print("=" * 60)
        print("DRY RUN 模式 - 不会修改数据库")
        print("=" * 60)
        import_students(filepath, dry_run=True)
    else:
        print("=" * 60)
        print("正式导入模式 - 将修改数据库")
        print("=" * 60)
        confirm = input("确认继续？(yes/no): ")
        if confirm.lower() == 'yes':
            import_students(filepath, dry_run=False)
        else:
            print("已取消导入")
