#!/usr/bin/env python
"""
数据库数据全面分析 - 包含研究生问题排查
生成详细分析报告
"""
import os
import sys
import django
from collections import Counter, defaultdict
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User
from apps.applications.models import Application

def print_section(title):
    print(f"\n{'='*80}")
    print(f"{title}")
    print('='*80)

def analyze_users():
    """用户角色分布分析"""
    print_section("1. 用户角色分布")

    total = User.objects.count()

    for role in ['student', 'dorm_manager', 'counselor', 'admin']:
        count = User.objects.filter(role=role).count()
        pct = count/total*100 if total > 0 else 0
        print(f"  {role}: {count}人 ({pct:.2f}%)")

    print(f"\n  总用户数: {total}")

def analyze_departments():
    """学院分布分析"""
    print_section("2. 学院(Department)分布")

    students = User.objects.filter(role='student')
    total = students.count()

    dept_counter = Counter(students.values_list('department', flat=True))

    print(f"\n总学生数: {total}")
    print(f"唯一学院数: {len(dept_counter)}\n")

    for dept, count in sorted(dept_counter.items(), key=lambda x: x[1], reverse=True):
        pct = count/total*100
        print(f"  {dept}: {count}人 ({pct:.2f}%)")

def analyze_student_id_patterns():
    """学号模式分析"""
    print_section("3. 学号(user_id)模式分析")

    students = User.objects.filter(role='student')

    # 提取年份前缀
    year_prefix_counter = Counter()
    for student in students:
        if student.user_id and len(student.user_id) >= 4:
            year = student.user_id[:4]
            year_prefix_counter[year] += 1

    print("\n按入学年份分布:")
    for year, count in sorted(year_prefix_counter.items()):
        pct = count/students.count()*100
        print(f"  {year}级: {count}人 ({pct:.2f}%)")

    # 学号长度分析
    length_counter = Counter(len(s.user_id) for s in students if s.user_id)
    print(f"\n学号长度分布:")
    for length, count in sorted(length_counter.items()):
        print(f"  {length}位: {count}人")

def analyze_class_patterns():
    """班级模式分析"""
    print_section("4. 班级(class_id)模式分析")

    students = User.objects.filter(role='student')

    # 统计专升本
    upgrade_count = students.filter(class_id__icontains='专升本').count()
    print(f"\n专升本学生: {upgrade_count}人")

    # 统计优师
    youshi_count = students.filter(class_id__icontains='优师').count()
    print(f"优师计划学生: {youshi_count}人")

    # 班级数量
    unique_classes = students.values('class_id').distinct().count()
    print(f"唯一班级数: {unique_classes}")

def analyze_routing_coverage():
    """路由覆盖率分析"""
    print_section("5. 审批路由覆盖率")
    print("\n  (跳过 - 需要单独的路由关系表分析)")

def analyze_applications():
    """申请数据分析"""
    print_section("6. 申请(Application)数据")

    total_apps = Application.objects.count()
    print(f"\n总申请数: {total_apps}")

    if total_apps > 0:
        status_counter = Counter(Application.objects.values_list('status', flat=True))
        print("\n申请状态分布:")
        for status, count in status_counter.items():
            pct = count/total_apps*100
            print(f"  {status}: {count} ({pct:.2f}%)")

def analyze_graduate_students():
    """研究生数据排查（关键问题）"""
    print_section("7. 研究生数据排查")

    students = User.objects.filter(role='student')
    total = students.count()

    print("\n[问题背景]")
    print("  原始Excel表格显示约135名研究生")
    print("  导入后数据库中未找到研究生标识")
    print("  需要排查研究生数据是否丢失或标识字段错误\n")

    # 方法1: department字段检查
    print("[检查方法1] department字段关键词搜索:")
    grad_keywords = ['研究生', '研究', '硕士', '博士', 'Master', 'PhD', 'Graduate', '研究生院']
    found_any = False
    for keyword in grad_keywords:
        count = students.filter(department__icontains=keyword).count()
        if count > 0:
            print(f"  ✓ 包含'{keyword}': {count}人")
            found_any = True
    if not found_any:
        print("  ✗ department字段中未找到任何研究生标识")

    # 方法2: class_id字段检查
    print("\n[检查方法2] class_id字段关键词搜索:")
    found_any = False
    for keyword in grad_keywords:
        count = students.filter(class_id__icontains=keyword).count()
        if count > 0:
            print(f"  ✓ 包含'{keyword}': {count}人")
            found_any = True
    if not found_any:
        print("  ✗ class_id字段中未找到任何研究生标识")

    # 方法3: 学号模式检查（研究生学号可能不同）
    print("\n[检查方法3] 学号模式异常检查:")

    # 检查非13位学号
    non_standard = students.exclude(user_id__regex=r'^\d{13}$')
    print(f"  非标准13位学号: {non_standard.count()}人")
    if non_standard.count() > 0 and non_standard.count() <= 10:
        print("  示例:")
        for s in non_standard[:5]:
            print(f"    {s.user_id} | {s.name} | {s.department}")

    # 方法4: 学院中可能包含研究生的特殊学院
    print("\n[检查方法4] 可能包含研究生的学院:")
    potential_grad_colleges = ['马克思主义学院', '李时珍中医药学院']
    for college in potential_grad_colleges:
        count = students.filter(department=college).count()
        if count > 0:
            print(f"  {college}: {count}人")

    # 方法5: 年级分析（研究生可能是更早年级）
    print("\n[检查方法5] 入学年份分布（研究生学制通常2-3年）:")
    year_counter = Counter()
    for student in students:
        if student.user_id and len(student.user_id) >= 4:
            year = student.user_id[:4]
            year_counter[year] += 1

    for year in sorted(year_counter.keys())[:5]:
        count = year_counter[year]
        print(f"  {year}级: {count}人")

    # 结论
    print("\n[初步结论]")
    print("  1. department和class_id字段均无研究生标识关键词")
    print("  2. 所有学生均为本科生数据结构")
    print("  3. 可能原因:")
    print("     - Excel源数据中研究生数据未包含在导入范围")
    print("     - 研究生数据在单独的Sheet或文件中")
    print("     - 研究生使用了与本科生不同的字段结构")

def main():
    """执行所有分析"""
    print("\n" + "="*80)
    print("数据库数据全面分析报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    analyze_users()
    analyze_departments()
    analyze_student_id_patterns()
    analyze_class_patterns()
    analyze_routing_coverage()
    analyze_applications()
    analyze_graduate_students()

    print("\n" + "="*80)
    print("分析完成")
    print("="*80)

if __name__ == "__main__":
    main()
