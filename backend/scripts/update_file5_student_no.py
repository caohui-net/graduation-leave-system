#!/usr/bin/env python3
"""
Update File5 student numbers from temporary IDs to real student numbers.

Usage:
    python3 update_file5_student_no.py \
        --input backend/data/file5_students_merged.csv \
        --mapping backend/data/missing_student_no_filled.csv \
        --output backend/data/file5_students_merged_v2.csv
"""

import csv
import sys
import argparse
from pathlib import Path


def load_mapping(mapping_file):
    """Load TMP ID to real student number mapping."""
    mapping = {}
    with open(mapping_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Support both English and Chinese column names
            tmp_id = (row.get('user_id') or row.get('临时ID') or '').strip()
            real_no = (row.get('student_no') or row.get('学号（待补充）') or '').strip()
            name = (row.get('name') or row.get('姓名') or '').strip()

            if tmp_id.startswith('TMP2026_'):
                if real_no and real_no != '':
                    mapping[tmp_id] = {'student_no': real_no, 'name': name}

    return mapping


def update_file5(input_file, mapping, output_file):
    """Update File5 with real student numbers."""
    stats = {
        'total': 0,
        'updated': 0,
        'skipped': 0,
        'errors': []
    }

    with open(input_file, 'r', encoding='utf-8-sig') as fin, \
         open(output_file, 'w', encoding='utf-8', newline='') as fout:

        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            stats['total'] += 1
            user_id = row['user_id'].strip()

            if user_id.startswith('TMP2026_'):
                if user_id in mapping:
                    # Verify name match
                    if row['name'].strip() == mapping[user_id]['name']:
                        row['user_id'] = mapping[user_id]['student_no']
                        row['user_id_source'] = 'file2_xh_updated'
                        stats['updated'] += 1
                    else:
                        stats['errors'].append(f"Name mismatch for {user_id}: {row['name']} vs {mapping[user_id]['name']}")
                        stats['skipped'] += 1
                else:
                    stats['errors'].append(f"No mapping for {user_id}")
                    stats['skipped'] += 1

            writer.writerow(row)

    return stats


def validate_output(output_file, expected_total, expected_updated):
    """Validate the output file."""
    with open(output_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        total = 0
        tmp_count = 0

        for row in reader:
            total += 1
            if row['user_id'].startswith('TMP2026_'):
                tmp_count += 1

        return {
            'total': total,
            'tmp_remaining': tmp_count,
            'matches_expected': total == expected_total,
            'no_tmp_remaining': tmp_count == 0
        }


def main():
    parser = argparse.ArgumentParser(description='Update File5 student numbers')
    parser.add_argument('--input', required=True, help='Input File5 CSV')
    parser.add_argument('--mapping', required=True, help='Mapping CSV with real student numbers')
    parser.add_argument('--output', required=True, help='Output File5 v2 CSV')
    parser.add_argument('--dry-run', action='store_true', help='Dry run without writing output')

    args = parser.parse_args()

    # Validate input files
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not Path(args.mapping).exists():
        print(f"Error: Mapping file not found: {args.mapping}", file=sys.stderr)
        sys.exit(1)

    # Load mapping
    print(f"Loading mapping from {args.mapping}...")
    mapping = load_mapping(args.mapping)
    print(f"Loaded {len(mapping)} mappings")

    if args.dry_run:
        print("\n=== DRY RUN MODE ===")
        print("Mappings:")
        for tmp_id, info in list(mapping.items())[:5]:
            print(f"  {tmp_id} -> {info['student_no']} ({info['name']})")
        print(f"  ... and {len(mapping) - 5} more")
        return

    # Update File5
    print(f"\nUpdating {args.input}...")
    stats = update_file5(args.input, mapping, args.output)

    # Print results
    print(f"\n=== Update Results ===")
    print(f"Total rows: {stats['total']}")
    print(f"Updated: {stats['updated']}")
    print(f"Skipped: {stats['skipped']}")

    if stats['errors']:
        print(f"\nErrors ({len(stats['errors'])}):")
        for err in stats['errors'][:10]:
            print(f"  - {err}")
        if len(stats['errors']) > 10:
            print(f"  ... and {len(stats['errors']) - 10} more")

    # Validate output
    print(f"\nValidating {args.output}...")
    validation = validate_output(args.output, stats['total'], stats['updated'])
    print(f"Total rows in output: {validation['total']}")
    print(f"TMP IDs remaining: {validation['tmp_remaining']}")
    print(f"Validation: {'✓ PASS' if validation['no_tmp_remaining'] else '✗ FAIL - TMP IDs remain'}")

    if validation['no_tmp_remaining'] and len(stats['errors']) == 0:
        print(f"\n✓ Success: File5 v2 created at {args.output}")
        sys.exit(0)
    else:
        print(f"\n✗ Warning: Output created but has issues")
        sys.exit(1)


if __name__ == '__main__':
    main()
