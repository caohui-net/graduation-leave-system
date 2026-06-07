#!/usr/bin/env python3
"""简单CSV匹配脚本 - 无需pandas"""
import csv
from pathlib import Path

docs_dir = Path('/home/caohui/projects/graduation-leave-system/docs')

# 读取研究生学号
print("Reading graduates...")
graduates = {}
with open(docs_dir / '硕士研究生-毕业生290人.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['学号']:
            graduates[row['学号'].strip()] = row['姓名'].strip()

print(f"Graduates: {len(graduates)}")

# 读取入住信息
print("Reading housing info...")
housing = {}
with open(docs_dir / '20260606-毕业生入住基本信息.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        user_id = row['学号'].strip()
        housing[user_id] = {
            'building': row.get('楼栋名称', '').strip(),
            'department': row.get('学院名称', '').strip(),
            'name': row.get('姓名', '').strip()
        }

print(f"Housing records: {len(housing)}")

# 匹配
matched = []
unmatched = []

for grad_id, grad_name in graduates.items():
    if grad_id in housing:
        h = housing[grad_id]
        matched.append({
            'user_id': grad_id,
            'name': grad_name,
            'building': h['building'],
            'department': h['department']
        })
    else:
        unmatched.append({'user_id': grad_id, 'name': grad_name})

# 统计
print(f"\n{'='*60}")
print("Match Results")
print(f"{'='*60}")
print(f"Total graduates: {len(graduates)}")
print(f"Matched: {len(matched)} ({len(matched)/len(graduates)*100:.1f}%)")
print(f"Unmatched: {len(unmatched)} ({len(unmatched)/len(graduates)*100:.1f}%)")

# 检查匹配记录的数据完整性
has_building = sum(1 for m in matched if m['building'])
has_department = sum(1 for m in matched if m['department'])
has_both = sum(1 for m in matched if m['building'] and m['department'])

print(f"\nData completeness in matched records:")
print(f"  Has building: {has_building}/{len(matched)} ({has_building/len(matched)*100:.1f}%)")
print(f"  Has department: {has_department}/{len(matched)} ({has_department/len(matched)*100:.1f}%)")
print(f"  Has BOTH: {has_both}/{len(matched)} ({has_both/len(matched)*100:.1f}%)")

# 样本展示
if matched:
    print(f"\nSample matched records (first 5):")
    for i, m in enumerate(matched[:5], 1):
        print(f"{i}. {m['user_id']} | {m['name']} | {m['building']} | {m['department']}")

# 导出完整匹配结果
output_file = docs_dir / 'graduate_housing_matched.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['学号', '姓名', 'building', 'department'])
    writer.writeheader()
    for m in matched:
        writer.writerow({
            '学号': m['user_id'],
            '姓名': m['name'],
            'building': m['building'],
            'department': m['department']
        })

print(f"\n✓ Matched data exported to: {output_file}")

if has_both >= len(matched) * 0.9:
    print(f"\n{'='*60}")
    print("✅ SUCCESS: 90%+ matched graduates have complete data!")
    print(f"{'='*60}")
    print(f"This file can be used for graduate import.")
else:
    print(f"\n{'='*60}")
    print(f"⚠ WARNING: Only {has_both}/{len(matched)} have complete data")
    print(f"{'='*60}")
