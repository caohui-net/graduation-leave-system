#!/usr/bin/env python
"""
数据库数据详细分析 - 聚焦研究生数据问题
"""
import os
import sys
import django
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User

def analyze_graduate_students():
    """分析研究生数据"""
    print("\n" + "="*80)
    print("1. 研究生数据统计")
    print("="*80)

    # 研究生识别：department包含"研究生"
    graduates = User.objects.filter(role='student', department__icontains='研究生')
    grad_count = graduates.count()

    total_students = User.objects.filter(role='student').count()

    print(f"总学生数: {total_students}")
    print(f"研究生数: {grad_count} ({grad_count/total_students*100:.2f}%)")
    print(f"本科生数: {total_students - grad_count} ({(total_students-grad_count)/total_students*100:.2f}%)")

    return graduates

def analyze_missing_building(graduates):
    """分析缺少building的学生"""
    print("\n" + "="*80)
    print("2. 缺少building字段分析")
    print("="*80)

    # 所有缺少building的学生
    no_building = User.objects.filter(role='student', building__isnull=True)
    no_building_count = no_building.count()

    # 研究生中缺少building
    grad_no_building = graduates.filter(building__isnull=True)
    grad_no_building_count = grad_no_building.count()

    # 本科生中缺少building
    undergrad_no_building_count = no_building_count - grad_no_building_count

    print(f"缺少building总数: {no_building_count}")
    print(f"  - 研究生: {grad_no_building_count} ({grad_no_building_count/no_building_count*100:.2f}%)")
    print(f"  - 本科生: {undergrad_no_building_count} ({undergrad_no_building_count/no_building_count*100:.2f}%)")

    return no_building, grad_no_building

def analyze_department_distribution(graduates):
    """分析研究生院系分布"""
    print("\n" + "="*80)
    print("3. 研究生院系分布")
    print("="*80)

    dept_counter = Counter(graduates.values_list('department', flat=True))

    print(f"研究生院系数量: {len(dept_counter)}")
    print(f"\n院系分布（前10）:")
    for dept, count in dept_counter.most_common(10):
        print(f"  {dept}: {count}人")

    return dept_counter

def analyze_building_distribution(graduates):
    """分析研究生楼栋分布"""
    print("\n" + "="*80)
    print("4. 研究生楼栋分布")
    print("="*80)

    # 有building的研究生
    grads_with_building = graduates.exclude(building__isnull=True)
    building_counter = Counter(grads_with_building.values_list('building', flat=True))

    print(f"有楼栋数据的研究生: {grads_with_building.count()}")
    print(f"涉及楼栋数量: {len(building_counter)}")
    print(f"\n楼栋分布（前10）:")
    for building, count in building_counter.most_common(10):
        print(f"  {building}: {count}人")

    return building_counter

def analyze_counselor_coverage(graduates):
    """分析研究生辅导员覆盖"""
    print("\n" + "="*80)
    print("5. 研究生辅导员覆盖分析")
    print("="*80)

    grad_with_dept = graduates.exclude(department__isnull=True)
    grad_no_dept = graduates.filter(department__isnull=True)

    print(f"有department的研究生: {grad_with_dept.count()}")
    print(f"缺少department的研究生: {grad_no_dept.count()}")

    # 检查是否有辅导员管理"研究生"学院
    counselors = User.objects.filter(role='counselor')
    print(f"\n辅导员总数: {counselors.count()}")

    # 检查辅导员管理的学院（需要看实际字段）
    # 这里假设辅导员没有特定的"管理研究生"字段

    return grad_with_dept, grad_no_dept

def analyze_class_info(graduates):
    """分析研究生班级信息"""
    print("\n" + "="*80)
    print("6. 研究生班级/年级信息")
    print("="*80)

    # 检查class_id分布
    class_counter = Counter(
        graduates.exclude(class_id__isnull=True).values_list('class_id', flat=True)
    )

    # 检查graduation_year分布
    year_counter = Counter(
        graduates.exclude(graduation_year__isnull=True).values_list('graduation_year', flat=True)
    )

    print(f"有class_id的研究生: {len([g for g in graduates if g.class_id])}")
    print(f"有graduation_year的研究生: {len([g for g in graduates if g.graduation_year])}")

    print(f"\n毕业年份分布:")
    for year, count in sorted(year_counter.items()):
        print(f"  {year}年: {count}人")

    return class_counter, year_counter

def generate_sample_data(graduates, grad_no_building):
    """生成样本数据"""
    print("\n" + "="*80)
    print("7. 样本数据（各取5条）")
    print("="*80)

    print("\n有building的研究生样本:")
    grads_with_building = graduates.exclude(building__isnull=True)[:5]
    for g in grads_with_building:
        print(f"  {g.user_id} | {g.name} | {g.department} | {g.building} | {g.class_id}")

    print("\n缺少building的研究生样本:")
    for g in grad_no_building[:5]:
        print(f"  {g.user_id} | {g.name} | {g.department} | {g.building} | {g.class_id}")

def main():
    print("="*80)
    print("数据库详细分析 - 研究生数据问题")
    print("分析时间:", "2026-06-07")
    print("="*80)

    # 1. 研究生统计
    graduates = analyze_graduate_students()

    # 2. 缺少building分析
    no_building, grad_no_building = analyze_missing_building(graduates)

    # 3. 院系分布
    dept_dist = analyze_department_distribution(graduates)

    # 4. 楼栋分布
    building_dist = analyze_building_distribution(graduates)

    # 5. 辅导员覆盖
    grad_with_dept, grad_no_dept = analyze_counselor_coverage(graduates)

    # 6. 班级/年级信息
    class_dist, year_dist = analyze_class_info(graduates)

    # 7. 样本数据
    generate_sample_data(graduates, grad_no_building)

    # 生成问题总结
    print("\n" + "="*80)
    print("问题总结与建议")
    print("="*80)

    grad_count = graduates.count()
    grad_no_building_count = grad_no_building.count()

    issues = []

    if grad_no_building_count > 0:
        issues.append(
            f"P1: {grad_no_building_count}名研究生缺少building字段 "
            f"({grad_no_building_count/grad_count*100:.1f}%)，"
            "影响宿管员审批路由"
        )

    if grad_no_dept.count() > 0:
        issues.append(
            f"P2: {grad_no_dept.count()}名研究生缺少department字段，"
            "影响辅导员审批路由"
        )

    if issues:
        print("\n发现问题:")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
    else:
        print("\n✓ 未发现数据完整性问题")

    print("\n建议:")
    if grad_no_building_count > 0:
        print("1. 排查116名缺少building学生的来源（File1 vs File2）")
        print("2. 确认是否需要为研究生补充楼栋数据")
        print("3. 如无法补充，确认业务是否接受研究生无宿管审批")

    print("\n" + "="*80)

if __name__ == "__main__":
    main()
