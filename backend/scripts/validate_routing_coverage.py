#!/usr/bin/env python3
"""
Validate routing coverage for all students.
Ensures every student can be routed to dorm manager and counselor.
"""
import csv
import json
from collections import defaultdict
from typing import Dict, List, Set


def load_students(file5_path: str) -> List[dict]:
    """Load File5 student data."""
    students = []
    with open(file5_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        students = list(reader)
    return students


def load_dorm_managers(file3_path: str) -> Dict[str, List[str]]:
    """
    Load File3 dorm manager data.
    Returns: {building_name: [manager_ids]}
    """
    building_managers = defaultdict(list)

    with open(file3_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            building = row['楼栋号'].strip()
            manager_id = row['职工号'].strip()

            if manager_id and manager_id != '暂未申请':
                building_managers[building].append(manager_id)

    return dict(building_managers)


def load_counselors(file4_path: str) -> Dict[str, str]:
    """
    Load File4 counselor data.
    Returns: {department: counselor_id}
    """
    dept_counselors = {}

    with open(file4_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            department = row['学院'].strip()
            counselor_id = row['职工号'].strip()

            if counselor_id:
                dept_counselors[department] = counselor_id

    return dept_counselors


def validate_routing(file5_path: str, file3_path: str, file4_path: str) -> dict:
    """
    Validate that all students can be routed to approvers.

    Returns validation report with coverage statistics.
    """
    students = load_students(file5_path)
    building_managers = load_dorm_managers(file3_path)
    dept_counselors = load_counselors(file4_path)

    report = {
        'total_students': len(students),
        'dorm_manager_coverage': 0,
        'counselor_coverage': 0,
        'fully_routable': 0,
        'missing_dorm_manager': [],
        'missing_counselor': [],
        'unroutable_students': []
    }

    for student in students:
        user_id = student['user_id']
        name = student['name']
        building = student['building_name']
        department = student['department']

        # Check dorm manager routing
        has_dorm_manager = building in building_managers
        if has_dorm_manager:
            report['dorm_manager_coverage'] += 1
        else:
            report['missing_dorm_manager'].append({
                'user_id': user_id,
                'name': name,
                'building': building
            })

        # Check counselor routing
        has_counselor = department in dept_counselors
        if has_counselor:
            report['counselor_coverage'] += 1
        else:
            report['missing_counselor'].append({
                'user_id': user_id,
                'name': name,
                'department': department
            })

        # Check full routing
        if has_dorm_manager and has_counselor:
            report['fully_routable'] += 1
        else:
            report['unroutable_students'].append({
                'user_id': user_id,
                'name': name,
                'building': building,
                'department': department,
                'missing': {
                    'dorm_manager': not has_dorm_manager,
                    'counselor': not has_counselor
                }
            })

    # Calculate percentages
    total = report['total_students']
    report['dorm_manager_coverage_pct'] = (report['dorm_manager_coverage'] / total * 100) if total > 0 else 0
    report['counselor_coverage_pct'] = (report['counselor_coverage'] / total * 100) if total > 0 else 0
    report['fully_routable_pct'] = (report['fully_routable'] / total * 100) if total > 0 else 0

    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Validate routing coverage')
    parser.add_argument('--file5', required=True, help='Path to File5 (merged students)')
    parser.add_argument('--file3', required=True, help='Path to File3 (dorm managers)')
    parser.add_argument('--file4', required=True, help='Path to File4 (counselors)')
    parser.add_argument('--report', help='Optional JSON report output path')

    args = parser.parse_args()

    print("Validating routing coverage...")
    report = validate_routing(args.file5, args.file3, args.file4)

    print("\n=== Routing Coverage Report ===")
    print(f"Total students: {report['total_students']}")
    print(f"\nDorm manager coverage: {report['dorm_manager_coverage']}/{report['total_students']} ({report['dorm_manager_coverage_pct']:.1f}%)")
    print(f"Counselor coverage: {report['counselor_coverage']}/{report['total_students']} ({report['counselor_coverage_pct']:.1f}%)")
    print(f"Fully routable: {report['fully_routable']}/{report['total_students']} ({report['fully_routable_pct']:.1f}%)")

    # Gate check
    if report['fully_routable_pct'] == 100.0:
        print("\n✓ PASS: 100% routing coverage achieved")
        exit_code = 0
    else:
        print(f"\n✗ FAIL: {len(report['unroutable_students'])} students cannot be routed")
        print("\nMissing dorm managers for buildings:")
        missing_buildings = set(s['building'] for s in report['missing_dorm_manager'])
        for building in sorted(missing_buildings):
            count = sum(1 for s in report['missing_dorm_manager'] if s['building'] == building)
            print(f"  - {building}: {count} students")

        print("\nMissing counselors for departments:")
        missing_depts = set(s['department'] for s in report['missing_counselor'])
        for dept in sorted(missing_depts):
            count = sum(1 for s in report['missing_counselor'] if s['department'] == dept)
            print(f"  - {dept}: {count} students")

        exit_code = 1

    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\nFull report saved to: {args.report}")

    exit(exit_code)
