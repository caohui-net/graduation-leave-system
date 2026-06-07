#!/usr/bin/env python
"""
Department字段详细分析 - 排查研究生识别问题
"""
import os
import sys
import django
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User

def main():
    print("="*80)
    print("Department字段详细分析")
    print("="*80)

    students = User.objects.filter(role='student')
    total = students.count()

    print(f"\n总学生数: {total}")

    # 统计所有department值
    dept_counter = Counter(students.values_list('department', flat=True))

    print(f"\n唯一department数量: {len(dept_counter)}")
    print(f"\nDepartment值列表（按数量排序）:")
    for dept, count in dept_counter.most_common(50):
        pct = count/total*100
        marker = " ← 研究生?" if dept and '研究' in dept else ""
        print(f"  {dept}: {count}人 ({pct:.2f}%){marker}")

    # 检查可能的研究生标识
    possible_grad_keywords = ['研究生', '研究', '硕士', '博士', 'Master', 'PhD', 'Graduate']

    print(f"\n" + "="*80)
    print("可能的研究生标识检查:")
    print("="*80)

    for keyword in possible_grad_keywords:
        count = students.filter(department__icontains=keyword).count()
        if count > 0:
            print(f"  包含'{keyword}': {count}人")

    # 检查class_id或user_id模式
    print(f"\n" + "="*80)
    print("学号模式分析（前20条）:")
    print("="*80)

    for student in students[:20]:
        print(f"  {student.user_id} | {student.department} | {student.class_id}")

if __name__ == "__main__":
    main()
