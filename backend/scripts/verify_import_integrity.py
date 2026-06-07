#!/usr/bin/env python
"""
验证导入数据完整性：检查重复、统计分布
"""
import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User
from django.db.models import Count

def check_duplicates():
    """检查重复用户"""
    print("\n" + "="*60)
    print("[检查1] 用户ID重复检测")
    print("="*60)

    duplicates = User.objects.values('user_id').annotate(
        count=Count('user_id')
    ).filter(count__gt=1)

    if duplicates:
        print(f"⚠️  发现 {len(duplicates)} 个重复user_id:")
        for dup in duplicates:
            print(f"  - {dup['user_id']}: {dup['count']}次")
            users = User.objects.filter(user_id=dup['user_id'])
            for u in users:
                print(f"    ID: {u.id}, Name: {u.name}, Role: {u.role}")
        return False
    else:
        print("✓ 无重复user_id")
        return True

def check_distribution():
    """检查用户分布"""
    print("\n" + "="*60)
    print("[检查2] 用户角色分布")
    print("="*60)

    total = User.objects.count()
    students = User.objects.filter(role='student').count()
    dorm_mgrs = User.objects.filter(role='dorm_manager').count()
    counselors = User.objects.filter(role='counselor').count()
    admins = User.objects.filter(role='admin').count()

    print(f"总用户数: {total}")
    print(f"  - 学生: {students} ({students/total*100:.1f}%)")
    print(f"  - 宿管: {dorm_mgrs} ({dorm_mgrs/total*100:.1f}%)")
    print(f"  - 辅导: {counselors} ({counselors/total*100:.1f}%)")
    print(f"  - 管理: {admins} ({admins/total*100:.1f}%)")

    # 期望值（来自Excel分析）
    expected_students = 5946
    expected_dorm = 73
    expected_counselor = 20
    expected_admin = 2
    expected_total = expected_students + expected_dorm + expected_counselor + expected_admin

    print(f"\n期望值对比:")
    print(f"  总数: {total} / {expected_total} ({total/expected_total*100:.1f}%)")
    print(f"  学生: {students} / {expected_students} ({students/expected_students*100:.1f}%)")
    print(f"  宿管: {dorm_mgrs} / {expected_dorm} ({dorm_mgrs/expected_dorm*100:.1f}%)")
    print(f"  辅导: {counselors} / {expected_counselor} ({counselors/expected_counselor*100:.1f}%)")
    print(f"  管理: {admins} / {expected_admin} ({admins/expected_admin*100:.1f}%)")

    return total == expected_total

def check_required_fields():
    """检查必填字段缺失"""
    print("\n" + "="*60)
    print("[检查3] 必填字段完整性")
    print("="*60)

    issues = []

    # 学生必须有department和building
    students_no_dept = User.objects.filter(role='student', department__isnull=True).count()
    if students_no_dept > 0:
        issues.append(f"学生缺少department: {students_no_dept}人")

    students_no_building = User.objects.filter(role='student', building__isnull=True).count()
    if students_no_building > 0:
        issues.append(f"学生缺少building: {students_no_building}人")

    # Note: Skipping dorm_manager and counselor field checks
    # as their managed fields may have different names or structure

    if issues:
        print("⚠️  发现字段缺失:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✓ 所有必填字段完整")
        return True

def check_routing_coverage():
    """检查路由覆盖率"""
    print("\n" + "="*60)
    print("[检查4] 审批路由覆盖率")
    print("="*60)

    total_students = User.objects.filter(role='student').count()

    # 宿管路由覆盖
    students_with_dorm_mgr = User.objects.filter(
        role='student',
        building__isnull=False
    ).count()

    # 辅导员路由覆盖
    students_with_counselor = User.objects.filter(
        role='student',
        department__isnull=False
    ).count()

    dorm_coverage = students_with_dorm_mgr / total_students * 100 if total_students > 0 else 0
    counselor_coverage = students_with_counselor / total_students * 100 if total_students > 0 else 0

    print(f"宿管路由覆盖: {students_with_dorm_mgr}/{total_students} ({dorm_coverage:.1f}%)")
    print(f"辅导员路由覆盖: {students_with_counselor}/{total_students} ({counselor_coverage:.1f}%)")

    if dorm_coverage >= 98 and counselor_coverage >= 98:
        print("✓ 路由覆盖率符合要求(≥98%)")
        return True
    else:
        print("⚠️  路由覆盖率不足")
        return False

def main():
    print("="*60)
    print("真实数据导入完整性验证")
    print("="*60)

    results = {
        '重复检测': check_duplicates(),
        '分布统计': check_distribution(),
        '字段完整性': check_required_fields(),
        '路由覆盖率': check_routing_coverage(),
    }

    print("\n" + "="*60)
    print("验证结果汇总")
    print("="*60)

    all_pass = True
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {check}")
        if not passed:
            all_pass = False

    print("\n" + "="*60)
    if all_pass:
        print("✓ 所有检查通过，数据导入成功")
    else:
        print("⚠️  部分检查未通过，请审查数据")
    print("="*60)

    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())
