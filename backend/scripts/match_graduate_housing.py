#!/usr/bin/env python3
"""
研究生入住信息匹配脚本
Cross-reference graduate students with housing data files
"""
import pandas as pd
from pathlib import Path

def match_graduate_housing():
    """Match graduate students with housing information"""

    docs_dir = Path(__file__).parent.parent.parent / 'docs'

    # Load graduate students (290)
    print("Loading graduate students...")
    graduates = pd.read_excel(docs_dir / '硕士研究生-毕业生290人.xls')
    print(f"Graduates: {len(graduates)} rows")
    print(f"Columns: {graduates.columns.tolist()}\n")

    # Load housing info file
    print("Loading housing info (20260606-毕业生入住基本信息.xls)...")
    housing = pd.read_excel(docs_dir / '20260606-毕业生入住基本信息.xls')
    print(f"Housing: {len(housing)} rows")
    print(f"Columns: {housing.columns.tolist()}\n")

    # Load no-building comparison file
    print("Loading no-building comparison (无楼栋信息学生对比表.csv)...")
    no_building = pd.read_csv(docs_dir / '无楼栋信息学生对比表.csv')
    print(f"No-building: {len(no_building)} rows")
    print(f"Columns: {no_building.columns.tolist()}\n")

    # Normalize column names
    grad_id_col = graduates.columns[1]  # Assume 2nd column is student ID

    # Find ID column in housing file
    housing_id_cols = [col for col in housing.columns if '学号' in str(col) or 'user_id' in str(col).lower()]
    housing_id_col = housing_id_cols[0] if housing_id_cols else housing.columns[0]

    # Find ID column in no-building file
    no_building_id_cols = [col for col in no_building.columns if '学号' in str(col) or 'user_id' in str(col).lower()]
    no_building_id_col = no_building_id_cols[0] if no_building_id_cols else no_building.columns[0]

    print(f"Graduate ID column: {grad_id_col}")
    print(f"Housing ID column: {housing_id_col}")
    print(f"No-building ID column: {no_building_id_col}\n")

    # Match with housing file
    grad_ids = set(graduates[grad_id_col].astype(str).str.strip())
    housing_ids = set(housing[housing_id_col].astype(str).str.strip())
    no_building_ids = set(no_building[no_building_id_col].astype(str).str.strip())

    matched_housing = grad_ids & housing_ids
    matched_no_building = grad_ids & no_building_ids

    print("="*60)
    print("Match Results")
    print("="*60)
    print(f"Total graduates: {len(grad_ids)}")
    print(f"Matched in housing file: {len(matched_housing)} ({len(matched_housing)/len(grad_ids)*100:.1f}%)")
    print(f"Matched in no-building file: {len(matched_no_building)} ({len(matched_no_building)/len(grad_ids)*100:.1f}%)")
    print(f"Unmatched: {len(grad_ids - matched_housing - matched_no_building)}")

    # Check what fields are available in housing file for matched graduates
    if matched_housing:
        print(f"\n{'='*60}")
        print("Sample matched graduate from housing file:")
        print("="*60)
        sample_id = list(matched_housing)[0]
        sample_row = housing[housing[housing_id_col].astype(str).str.strip() == sample_id].iloc[0]
        for col in housing.columns:
            print(f"{col}: {sample_row[col]}")

        # Check for building/department columns
        building_cols = [col for col in housing.columns if '楼栋' in str(col) or 'building' in str(col).lower()]
        dept_cols = [col for col in housing.columns if '学院' in str(col) or 'department' in str(col).lower()]

        print(f"\n{'='*60}")
        print("Key fields check:")
        print("="*60)
        print(f"Building columns found: {building_cols}")
        print(f"Department columns found: {dept_cols}")

        if building_cols or dept_cols:
            print(f"\n✓ Housing file contains needed fields!")
            # Count how many graduates have non-null values
            matched_df = housing[housing[housing_id_col].astype(str).str.strip().isin(matched_housing)]
            if building_cols:
                non_null_building = matched_df[building_cols[0]].notna().sum()
                print(f"  - {non_null_building}/{len(matched_housing)} have building data")
            if dept_cols:
                non_null_dept = matched_df[dept_cols[0]].notna().sum()
                print(f"  - {non_null_dept}/{len(matched_housing)} have department data")
        else:
            print(f"\n⚠ Housing file does NOT contain building/department fields")

    return {
        'total_graduates': len(grad_ids),
        'matched_housing': len(matched_housing),
        'matched_no_building': len(matched_no_building),
        'housing_has_building': len([col for col in housing.columns if '楼栋' in str(col) or 'building' in str(col).lower()]) > 0,
        'housing_has_department': len([col for col in housing.columns if '学院' in str(col) or 'department' in str(col).lower()]) > 0
    }

if __name__ == '__main__':
    try:
        results = match_graduate_housing()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
