#!/usr/bin/env python3
"""
Post-import validation script for Phase 3 data integrity checks.
Validates student-counselor-dorm_manager routing coverage after data import.
"""

import sys
import os
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User, UserRole
from django.db.models import Count
from collections import defaultdict


def validate_students():
    """Validate all students have department and building for routing."""
    students = User.objects.filter(role=UserRole.STUDENT, active=True)
    total = students.count()

    no_dept = students.filter(department__isnull=True).count()
    no_building = students.filter(building__isnull=True).count()
    no_building_empty = students.filter(building='').count()

    print(f"\n=== Student Validation ===")
    print(f"Total active students: {total}")
    print(f"Missing department: {no_dept}")
    print(f"Missing building (NULL): {no_building}")
    print(f"Missing building (empty): {no_building_empty}")

    if no_dept > 0 or no_building > 0 or no_building_empty > 0:
        print("⚠ WARNING: Some students missing routing data")
        return False
    print("✓ All students have routing data")
    return True


def validate_counselor_coverage():
    """Validate every student department has at least one counselor."""
    students = User.objects.filter(role=UserRole.STUDENT, active=True).exclude(department__isnull=True)
    counselors = User.objects.filter(role=UserRole.COUNSELOR, active=True)

    student_depts = set(students.values_list('department', flat=True).distinct())
    counselor_depts = set(counselors.values_list('department', flat=True).distinct())

    missing_depts = student_depts - counselor_depts

    print(f"\n=== Counselor Coverage ===")
    print(f"Student departments: {len(student_depts)}")
    print(f"Counselor departments: {len(counselor_depts)}")

    if missing_depts:
        print(f"⚠ WARNING: {len(missing_depts)} departments without counselors:")
        for dept in sorted(missing_depts):
            count = students.filter(department=dept).count()
            print(f"  - {dept}: {count} students")
        return False

    print("✓ All student departments have counselors")

    # Check multi-counselor departments
    dept_counts = counselors.values('department').annotate(count=Count('user_id'))
    multi = [d for d in dept_counts if d['count'] > 1]
    if multi:
        print(f"\nℹ {len(multi)} departments with multiple counselors:")
        for d in sorted(multi, key=lambda x: x['count'], reverse=True)[:5]:
            print(f"  - {d['department']}: {d['count']} counselors")

    return True


def validate_dorm_manager_coverage():
    """Validate every student building has at least one dorm manager."""
    from django.db.models import Count

    students = User.objects.filter(role=UserRole.STUDENT, active=True).exclude(building__isnull=True).exclude(building='')
    dorm_managers = User.objects.filter(role=UserRole.DORM_MANAGER, active=True)

    student_buildings = set(students.values_list('building', flat=True).distinct())
    manager_buildings = set(dorm_managers.values_list('building', flat=True).distinct())

    missing_buildings = student_buildings - manager_buildings

    print(f"\n=== Dorm Manager Coverage ===")
    print(f"Student buildings: {len(student_buildings)}")
    print(f"Dorm manager buildings: {len(manager_buildings)}")

    if missing_buildings:
        print(f"⚠ WARNING: {len(missing_buildings)} buildings without dorm managers:")
        for bldg in sorted(missing_buildings)[:10]:
            count = students.filter(building=bldg).count()
            print(f"  - {bldg}: {count} students")
        return False

    print("✓ All student buildings have dorm managers")

    # Check multi-manager buildings
    bldg_counts = dorm_managers.values('building').annotate(count=Count('user_id'))
    multi = [b for b in bldg_counts if b['count'] > 1]
    if multi:
        print(f"\nℹ {len(multi)} buildings with multiple managers:")
        for b in sorted(multi, key=lambda x: x['count'], reverse=True)[:5]:
            print(f"  - {b['building']}: {b['count']} managers")

    return True


def validate_sample_routing():
    """Sample 100 random students and verify they can be routed."""
    import random

    students = list(User.objects.filter(role=UserRole.STUDENT, active=True).exclude(department__isnull=True).exclude(building__isnull=True).exclude(building=''))

    if len(students) < 100:
        sample = students
    else:
        sample = random.sample(students, 100)

    print(f"\n=== Sample Routing Validation ===")
    print(f"Testing {len(sample)} random students...")

    failures = []
    for student in sample:
        # Check dorm manager
        dm = User.objects.filter(role=UserRole.DORM_MANAGER, building=student.building, active=True).first()
        if not dm:
            failures.append(f"Student {student.user_id}: No dorm manager for building {student.building}")
            continue

        # Check counselor
        counselor = User.objects.filter(role=UserRole.COUNSELOR, department=student.department, active=True).first()
        if not counselor:
            failures.append(f"Student {student.user_id}: No counselor for department {student.department}")

    if failures:
        print(f"⚠ WARNING: {len(failures)} routing failures:")
        for f in failures[:10]:
            print(f"  - {f}")
        return False

    print(f"✓ All {len(sample)} students can be routed")
    return True


def main():
    print("=" * 60)
    print("Post-Import Validation Script")
    print("=" * 60)

    results = []
    results.append(validate_students())
    results.append(validate_counselor_coverage())
    results.append(validate_dorm_manager_coverage())
    results.append(validate_sample_routing())

    print("\n" + "=" * 60)
    if all(results):
        print("✓ ALL VALIDATIONS PASSED")
        print("=" * 60)
        return 0
    else:
        print("⚠ SOME VALIDATIONS FAILED")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
