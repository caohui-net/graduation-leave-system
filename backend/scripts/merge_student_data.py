#!/usr/bin/env python3
"""
Merge File1 (base student data) with File2 (supplemental student numbers).
Generates File5 with complete student records and temp IDs for missing XH.
"""
import csv
import json
from pathlib import Path
from typing import Dict, List, Set
import sys

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))
from generate_temp_user_ids import determine_user_id
from normalize_colleges import normalize_college_name


def load_file2_by_key(file2_path: str) -> Dict[str, dict]:
    """Load File2 and index by (name + normalized_college + BH) key."""
    file2_index = {}

    with open(file2_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['XM'].strip()
            college_raw = row['FY'].strip()
            bh = row['BH'].strip()

            try:
                college_norm = normalize_college_name(college_raw)
            except ValueError:
                continue  # Skip if college can't be normalized

            key = f"{name}|{college_norm}|{bh}"
            file2_index[key] = row

    return file2_index


def merge_files(file1_path: str, file2_path: str, output_path: str) -> dict:
    """
    Merge File1 and File2, generate File5 with complete student data.

    Returns merge report with statistics.
    """
    file2_index = load_file2_by_key(file2_path)

    stats = {
        'total_file1_rows': 0,
        'matched_count': 0,
        'file1_only_count': 0,
        'file2_only_count': 0,
        'grad_generated_ids': 0,
        'tmp_generated_ids': 0,
        'normalization_failures': 0,
        'skipped_rows': []
    }

    output_rows = []
    matched_file2_keys = set()  # Track matched File2 rows

    with open(file1_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row_idx, row in enumerate(reader, start=1):
            stats['total_file1_rows'] += 1

            # Extract File1 fields
            name = row['学生姓名'].strip()
            college_raw = row['学院名称'].strip()
            building = row['楼栋名称'].strip()
            room = row['寝室号'].strip()
            major = row['专业'].strip()
            grade = row['年级'].strip()
            class_name = row['班级'].strip()
            level = row['层次'].strip()  # 本科/硕士/博士

            # Normalize college
            try:
                college_norm = normalize_college_name(college_raw)
            except ValueError:
                stats['normalization_failures'] += 1
                stats['skipped_rows'].append({
                    'row': row_idx,
                    'name': name,
                    'college': college_raw,
                    'reason': 'college_normalization_failed'
                })
                continue

            # Try to match with File2
            match_key = f"{name}|{college_norm}|{class_name}"
            file2_row = file2_index.get(match_key)

            # Track matched File2 keys
            if file2_row:
                matched_file2_keys.add(match_key)

            # Determine if graduate student
            is_graduate = level in ['硕士', '博士']

            # Get student_no and generate user_id
            student_no = file2_row['XH'].strip() if file2_row else None
            user_id, user_id_source = determine_user_id(
                student_no=student_no,
                name=name,
                college=college_norm,
                building=building,
                room=room,
                row_index=row_idx,
                is_graduate=is_graduate
            )

            # Update statistics
            if file2_row:
                stats['matched_count'] += 1
            else:
                stats['file1_only_count'] += 1
                if user_id_source == 'grad_generated':
                    stats['grad_generated_ids'] += 1
                elif user_id_source == 'tmp_generated':
                    stats['tmp_generated_ids'] += 1

            # Build output row
            output_row = {
                'source_row_id': row_idx,
                'user_id': user_id,
                'user_id_source': user_id_source,
                'student_no': student_no or '',
                'name': name,
                'department': college_norm,
                'major': major,
                'grade': grade,
                'class_id': class_name,
                'level': level,
                'building_name': building,
                'room_number': room,
                'phone': file2_row.get('SJHM', '').strip() if file2_row else '',
                'email': file2_row.get('email', '').strip() if file2_row else '',
            }

            output_rows.append(output_row)

    # Process File2-only rows (user decision: import them)
    for match_key, file2_row in file2_index.items():
        if match_key not in matched_file2_keys:
            stats['file2_only_count'] += 1

            # Parse match_key to get name, college, class
            name, college_norm, class_name = match_key.split('|')

            # Extract File2 data
            student_no = file2_row['XH'].strip()

            # File2-only row output
            output_row = {
                'source_row_id': f'FILE2_{stats["file2_only_count"]}',
                'user_id': student_no,
                'user_id_source': 'file2_only',
                'student_no': student_no,
                'name': name,
                'department': college_norm,
                'major': '',  # Not in File2
                'grade': '',  # Not in File2
                'class_id': class_name,
                'level': '',  # Not in File2
                'building_name': '',  # Not in File2
                'room_number': '',  # Not in File2
                'phone': file2_row.get('SJHM', '').strip(),
                'email': file2_row.get('email', '').strip(),
            }

            output_rows.append(output_row)

    # Write File5
    if output_rows:
        fieldnames = list(output_rows[0].keys())
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(output_rows)

    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Merge File1 and File2 to generate File5')
    parser.add_argument('--file1', required=True, help='Path to File1 CSV')
    parser.add_argument('--file2', required=True, help='Path to File2 CSV')
    parser.add_argument('--output', required=True, help='Output path for File5')
    parser.add_argument('--report', help='Optional merge report JSON output path')

    args = parser.parse_args()

    print(f"Merging {args.file1} + {args.file2} → {args.output}")

    stats = merge_files(args.file1, args.file2, args.output)

    print("\n=== Merge Report ===")
    print(f"Total File1 rows: {stats['total_file1_rows']}")
    print(f"Matched with File2: {stats['matched_count']}")
    print(f"File1 only: {stats['file1_only_count']}")
    print(f"  - Graduate IDs generated: {stats['grad_generated_ids']}")
    print(f"  - Temp IDs generated: {stats['tmp_generated_ids']}")
    print(f"File2 only: {stats['file2_only_count']}")
    print(f"Normalization failures: {stats['normalization_failures']}")
    print(f"Output rows: {stats['total_file1_rows'] + stats['file2_only_count'] - stats['normalization_failures']}")

    if stats['skipped_rows']:
        print(f"\n⚠️  Skipped {len(stats['skipped_rows'])} rows (see report)")

    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print(f"\nFull report saved to: {args.report}")

    print("\n✓ Merge completed")
