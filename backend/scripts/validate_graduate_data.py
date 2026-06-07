#!/usr/bin/env python3
"""
研究生数据验证脚本
Validate graduate student data before import
"""
import csv
import sys
from pathlib import Path

def validate_graduate_csv(csv_file, counselors_file, dorm_managers_file):
    """
    Validate graduate student CSV against system data

    Returns: (is_valid, errors, warnings, stats)
    """
    errors = []
    warnings = []
    stats = {
        'total_rows': 0,
        'valid_rows': 0,
        'missing_building': 0,
        'missing_department': 0,
        'unknown_building': 0,
        'unknown_department': 0,
        'duplicate_ids': 0
    }

    # Load valid buildings from dorm managers
    valid_buildings = set()
    try:
        with open(dorm_managers_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'building' in row or '楼栋号' in row:
                    building = row.get('building') or row.get('楼栋号', '').strip()
                    if building:
                        valid_buildings.add(building)
    except FileNotFoundError:
        warnings.append(f"Dorm managers file not found: {dorm_managers_file}")
    except Exception as e:
        warnings.append(f"Error reading dorm managers: {str(e)}")

    # Load valid departments from counselors
    valid_departments = set()
    try:
        with open(counselors_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'department' in row or '学院' in row:
                    dept = row.get('department') or row.get('学院', '').strip()
                    if dept:
                        valid_departments.add(dept)
    except FileNotFoundError:
        warnings.append(f"Counselors file not found: {counselors_file}")
    except Exception as e:
        warnings.append(f"Error reading counselors: {str(e)}")

    # Validate graduate CSV
    seen_ids = set()

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Check headers
            required_fields = ['学号', '姓名', 'building', 'department']
            missing_fields = [f for f in required_fields if f not in reader.fieldnames]
            if missing_fields:
                errors.append(f"Missing required columns: {', '.join(missing_fields)}")
                return False, errors, warnings, stats

            for idx, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                stats['total_rows'] += 1
                row_valid = True

                user_id = row.get('学号', '').strip()
                name = row.get('姓名', '').strip()
                building = row.get('building', '').strip()
                department = row.get('department', '').strip()

                # Check required fields
                if not user_id:
                    errors.append(f"Row {idx}: Missing 学号")
                    row_valid = False

                if not name:
                    errors.append(f"Row {idx}: Missing 姓名")
                    row_valid = False

                if not building:
                    errors.append(f"Row {idx} ({user_id}): Missing building")
                    stats['missing_building'] += 1
                    row_valid = False
                elif valid_buildings and building not in valid_buildings:
                    warnings.append(f"Row {idx} ({user_id}): Unknown building '{building}'")
                    stats['unknown_building'] += 1

                if not department:
                    errors.append(f"Row {idx} ({user_id}): Missing department")
                    stats['missing_department'] += 1
                    row_valid = False
                elif valid_departments and department not in valid_departments:
                    warnings.append(f"Row {idx} ({user_id}): Unknown department '{department}'")
                    stats['unknown_department'] += 1

                # Check duplicates
                if user_id and user_id in seen_ids:
                    errors.append(f"Row {idx}: Duplicate 学号 '{user_id}'")
                    stats['duplicate_ids'] += 1
                    row_valid = False
                else:
                    seen_ids.add(user_id)

                if row_valid:
                    stats['valid_rows'] += 1

    except FileNotFoundError:
        errors.append(f"Graduate CSV file not found: {csv_file}")
        return False, errors, warnings, stats
    except Exception as e:
        errors.append(f"Error reading graduate CSV: {str(e)}")
        return False, errors, warnings, stats

    is_valid = len(errors) == 0 and stats['valid_rows'] == stats['total_rows']

    return is_valid, errors, warnings, stats


def print_report(is_valid, errors, warnings, stats):
    """Print validation report"""
    print("="*60)
    print("Graduate Data Validation Report")
    print("="*60)

    print(f"\nTotal rows: {stats['total_rows']}")
    print(f"Valid rows: {stats['valid_rows']}")

    if stats['missing_building'] > 0:
        print(f"⚠ Missing building: {stats['missing_building']}")
    if stats['missing_department'] > 0:
        print(f"⚠ Missing department: {stats['missing_department']}")
    if stats['duplicate_ids'] > 0:
        print(f"⚠ Duplicate IDs: {stats['duplicate_ids']}")
    if stats['unknown_building'] > 0:
        print(f"⚠ Unknown buildings: {stats['unknown_building']}")
    if stats['unknown_department'] > 0:
        print(f"⚠ Unknown departments: {stats['unknown_department']}")

    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for i, error in enumerate(errors[:10], 1):
            print(f"  {i}. {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")

    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for i, warning in enumerate(warnings[:10], 1):
            print(f"  {i}. {warning}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more warnings")

    print("\n" + "="*60)
    if is_valid:
        print("✅ Validation PASSED - Ready to import")
    else:
        print("❌ Validation FAILED - Fix errors before import")
    print("="*60)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Validate graduate student data')
    parser.add_argument('csv_file', help='Graduate student CSV file')
    parser.add_argument('--counselors', default='backend/data/2026年学院辅导员信息统计表.csv',
                       help='Counselors CSV file')
    parser.add_argument('--dorm-managers', default='backend/data/2026年社区辅导员信息统计表.csv',
                       help='Dorm managers CSV file')

    args = parser.parse_args()

    is_valid, errors, warnings, stats = validate_graduate_csv(
        args.csv_file,
        args.counselors,
        args.dorm_managers
    )

    print_report(is_valid, errors, warnings, stats)

    sys.exit(0 if is_valid else 1)
