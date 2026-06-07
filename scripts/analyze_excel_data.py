#!/usr/bin/env python3
"""分析Excel文件数据源是否满足项目需求"""
import pandas as pd
import sys

# 文件路径
FILES = {
    '学生基准': 'docs/1-5830名毕业生（含研究生）.xls',
    '学生补充': 'docs/2026届预计毕业生5675人.xlsx',
    '学院辅导员': 'docs/2026年学院辅导员信息统计表.xls',
    '社区辅导员': 'docs/2026年社区辅导员信息统计表.xls',
}

# 项目需求字段
REQUIREMENTS = {
    '学生': ['user_id(学号)', 'name(姓名)', 'class_id(班级ID)', 'is_graduating(毕业生标识)',
             'graduation_year(毕业年份)', 'department(院系)', 'phone(手机号)'],
    '辅导员': ['employee_id(工号)', 'name(姓名)', 'department(院系)'],
    '宿管员': ['employee_id(工号)', 'name(姓名)'],
    'ClassMapping': ['class_id(班级ID)', 'counselor_id(辅导员工号)']
}

def analyze_file(file_path, name):
    """分析单个文件"""
    print(f"\n{'='*60}")
    print(f"文件：{name}")
    print(f"路径：{file_path}")
    print(f"{'='*60}")

    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)

        print(f"\n行数：{len(df)}")
        print(f"列数：{len(df.columns)}")
        print(f"\n列名：")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")

        print(f"\n前3行数据示例：")
        print(df.head(3).to_string())

        # 检查是否有空值
        print(f"\n空值统计：")
        null_counts = df.isnull().sum()
        for col in df.columns:
            if null_counts[col] > 0:
                print(f"  {col}: {null_counts[col]} ({null_counts[col]/len(df)*100:.1f}%)")

        return df

    except Exception as e:
        print(f"\n❌ 读取失败: {e}")
        return None

def main():
    print("Excel数据源分析")
    print("="*60)

    results = {}
    for name, path in FILES.items():
        df = analyze_file(path, name)
        if df is not None:
            results[name] = df

    # 需求对比分析
    print(f"\n\n{'='*60}")
    print("需求对比分析")
    print(f"{'='*60}")

    print("\n项目需求字段：")
    for entity, fields in REQUIREMENTS.items():
        print(f"\n{entity}：")
        for field in fields:
            print(f"  - {field}")

    print(f"\n分析完成。请根据上述列名判断是否满足需求。")

if __name__ == '__main__':
    main()
