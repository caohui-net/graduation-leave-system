#!/usr/bin/env python3
"""系统就绪验证脚本 - 检查数据完整性和角色流程覆盖"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User
from django.db.models import Count, Q

def verify_system():
    print("="*70)
    print("系统就绪验证报告")
    print("="*70)

    # 1. 用户统计
    print("\n[1] 用户统计")
    print("-"*70)
    students = User.objects.filter(role='student')
    dorm_managers = User.objects.filter(role='dorm_manager')
    counselors = User.objects.filter(role='counselor')
    admins = User.objects.filter(role='admin')

    print(f"学生: {students.count()}")
    print(f"  - 本科生: {students.filter(Q(user_id__startswith='2020') | Q(user_id__startswith='2021') | Q(user_id__startswith='2022') | Q(user_id__startswith='2023') | Q(user_id__startswith='2024')).exclude(user_id__regex=r'^\d{4}045').count()}")
    print(f"  - 研究生: {students.filter(user_id__regex=r'^\d{4}045').count()}")
    print(f"宿管员: {dorm_managers.count()}")
    print(f"辅导员: {counselors.count()}")
    print(f"管理员: {admins.count()}")
    print(f"总计: {User.objects.count()}")

    # 2. 学生数据完整性
    print(f"\n[2] 学生数据完整性检查")
    print("-"*70)

    missing_building = students.filter(Q(building__isnull=True) | Q(building=''))
    missing_department = students.filter(Q(department__isnull=True) | Q(department=''))
    missing_both = students.filter(
        Q(building__isnull=True) | Q(building=''),
        Q(department__isnull=True) | Q(department='')
    )

    print(f"缺少building: {missing_building.count()} ({missing_building.count()/students.count()*100:.1f}%)")
    print(f"缺少department: {missing_department.count()} ({missing_department.count()/students.count()*100:.1f}%)")
    print(f"两者都缺: {missing_both.count()} ({missing_both.count()/students.count()*100:.1f}%)")

    complete = students.exclude(Q(building__isnull=True) | Q(building='')).exclude(Q(department__isnull=True) | Q(department=''))
    print(f"✓ 数据完整: {complete.count()} ({complete.count()/students.count()*100:.1f}%)")

    # 3. 宿管员覆盖率
    print(f"\n[3] 宿管员覆盖检查")
    print("-"*70)

    student_buildings = set(students.exclude(Q(building__isnull=True) | Q(building='')).values_list('building', flat=True))
    manager_buildings = set(dorm_managers.exclude(Q(building__isnull=True) | Q(building='')).values_list('building', flat=True))

    print(f"学生楼栋数: {len(student_buildings)}")
    print(f"宿管覆盖楼栋数: {len(manager_buildings)}")

    uncovered_buildings = student_buildings - manager_buildings
    if uncovered_buildings:
        print(f"⚠ 无宿管覆盖: {len(uncovered_buildings)}个楼栋")
        for b in list(uncovered_buildings)[:5]:
            count = students.filter(building=b).count()
            print(f"  - {b}: {count}人")
        if len(uncovered_buildings) > 5:
            print(f"  ... 还有{len(uncovered_buildings)-5}个")
    else:
        print(f"✓ 所有楼栋已覆盖")

    # 4. 辅导员覆盖率
    print(f"\n[4] 辅导员覆盖检查")
    print("-"*70)

    student_departments = set(students.exclude(Q(department__isnull=True) | Q(department='')).values_list('department', flat=True))
    counselor_departments = set(counselors.exclude(Q(department__isnull=True) | Q(department='')).values_list('department', flat=True))

    print(f"学生学院数: {len(student_departments)}")
    print(f"辅导员覆盖学院数: {len(counselor_departments)}")

    uncovered_departments = student_departments - counselor_departments
    if uncovered_departments:
        print(f"⚠ 无辅导员覆盖: {len(uncovered_departments)}个学院")
        for d in list(uncovered_departments)[:5]:
            count = students.filter(department=d).count()
            print(f"  - {d}: {count}人")
        if len(uncovered_departments) > 5:
            print(f"  ... 还有{len(uncovered_departments)-5}个")
    else:
        print(f"✓ 所有学院已覆盖")

    # 5. 阻塞用户（无法完成流程）
    print(f"\n[5] 流程阻塞分析")
    print("-"*70)

    # 学生必须有building和department才能完成流程
    blocked = students.filter(
        Q(building__isnull=True) | Q(building='') |
        Q(department__isnull=True) | Q(department='')
    )

    print(f"流程阻塞学生: {blocked.count()} ({blocked.count()/students.count()*100:.1f}%)")
    if blocked.count() > 0:
        print(f"  - 缺building: {blocked.filter(Q(building__isnull=True) | Q(building='')).count()}")
        print(f"  - 缺department: {blocked.filter(Q(department__isnull=True) | Q(department='')).count()}")

        if blocked.count() <= 20:
            print(f"\n阻塞学生清单:")
            for s in blocked[:20]:
                missing = []
                if not s.building:
                    missing.append('building')
                if not s.department:
                    missing.append('department')
                print(f"  {s.user_id} | {s.name} | 缺:{','.join(missing)}")

    # 6. 系统就绪状态
    print(f"\n{'='*70}")
    print("系统就绪评估")
    print("="*70)

    issues = []

    if missing_building.count() > 0:
        issues.append(f"⚠ {missing_building.count()}学生缺building")
    if missing_department.count() > 0:
        issues.append(f"⚠ {missing_department.count()}学生缺department")
    if uncovered_buildings:
        issues.append(f"⚠ {len(uncovered_buildings)}楼栋无宿管")
    if uncovered_departments:
        issues.append(f"⚠ {len(uncovered_departments)}学院无辅导员")

    if issues:
        print("系统状态: ⚠ 部分就绪（有阻塞）")
        for issue in issues:
            print(f"  {issue}")
        print(f"\n可用用户: {complete.count()}/{students.count()} ({complete.count()/students.count()*100:.1f}%)")
    else:
        print("系统状态: ✅ 完全就绪")
        print(f"所有{students.count()}名学生可完成审批流程")

    return blocked.count() == 0

if __name__ == '__main__':
    success = verify_system()
    sys.exit(0 if success else 1)
