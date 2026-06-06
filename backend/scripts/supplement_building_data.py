#!/usr/bin/env python3
"""
补充116名File2独有学生的楼栋数据
读取用户填写的CSV，更新File5，重新导入
"""
import csv
import sys
from pathlib import Path

def update_file5_with_building_data(filled_csv_path: str, file5_path: str, output_path: str):
    """
    更新File5中116名学生的楼栋数据

    Args:
        filled_csv_path: 用户填写的CSV（backend/data/missing_building_data_request.csv）
        file5_path: 原始File5（backend/data/file5_students_merged.csv）
        output_path: 更新后的File5输出路径
    """
    # Load filled building data
    building_data = {}
    with open(filled_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = row['学号'].strip()
            building = row['楼栋名称（待补充）'].strip()
            room = row['寝室号（待补充）'].strip()
            if building:  # Only update if filled
                building_data[user_id] = {'building': building, 'room': room}

    # Update File5
    updated_rows = []
    with open(file5_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = row['user_id']
            if user_id in building_data:
                row['building_name'] = building_data[user_id]['building']
                row['room_number'] = building_data[user_id]['room']
            updated_rows.append(row)

    # Write updated File5
    if updated_rows:
        fieldnames = list(updated_rows[0].keys())
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

    print(f"✓ Updated {len(building_data)} students with building data")
    print(f"✓ Output: {output_path}")
    return len(building_data)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Update File5 with building data from filled CSV')
    parser.add_argument('--filled-csv', required=True, help='User-filled CSV with building data')
    parser.add_argument('--file5', required=True, help='Original File5 path')
    parser.add_argument('--output', required=True, help='Updated File5 output path')

    args = parser.parse_args()

    updated_count = update_file5_with_building_data(args.filled_csv, args.file5, args.output)

    print(f"\n✓ Building data supplement completed")
    print(f"✓ {updated_count} students updated")
    print(f"\n下一步：重新运行数据导入")
    print(f"  python3 manage.py import_students --file {args.output}")
