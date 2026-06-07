#!/usr/bin/env python
"""
真实数据导入脚本（非交互版本）
直接执行所有步骤，无需用户确认
"""
import os
import sys
import subprocess
from datetime import datetime

def run_command(cmd, description):
    """执行命令并显示输出"""
    print(f"\n{'='*60}")
    print(f"[{description}]")
    print(f"命令: {' '.join(cmd)}")
    print(f"{'='*60}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    if result.returncode != 0:
        print(f"错误: 命令执行失败 (退出码 {result.returncode})")
        sys.exit(1)

    return result

def main():
    print("="*60)
    print("真实数据导入流程（非交互自动执行）")
    print(f"开始时间: {datetime.now()}")
    print("="*60)

    # Step 1: 验证当前状态
    run_command(
        ["python", "scripts/verify_db_status.py"],
        "Step 1: 数据库状态验证"
    )

    # Step 2: 备份数据库
    run_command(
        ["python", "scripts/backup_database.py"],
        "Step 2: 数据库备份"
    )

    # Step 3: CSV文件验证
    print("\n" + "="*60)
    print("[Step 3: CSV文件行数验证]")
    print("="*60)
    files = [
        "data/file5_students_merged_v2.csv",
        "data/dorm_managers_processed.csv",
        "data/counselors_processed.csv",
        "data/additional_staff.csv"
    ]
    for f in files:
        if os.path.exists(f):
            with open(f) as fp:
                lines = sum(1 for _ in fp)
            print(f"{lines:>6} {f}")
        else:
            print(f"警告: 文件不存在 {f}")

    # Step 4: Dry-run验证
    run_command(
        ["python", "manage.py", "import_staff",
         "--file", "data/dorm_managers_processed.csv", "--dry-run"],
        "Step 4a: Dry-run验证 - 宿管"
    )

    run_command(
        ["python", "manage.py", "import_staff",
         "--file", "data/counselors_processed.csv", "--dry-run"],
        "Step 4b: Dry-run验证 - 辅导员"
    )

    run_command(
        ["python", "manage.py", "import_staff",
         "--file", "data/additional_staff.csv", "--dry-run"],
        "Step 4c: Dry-run验证 - 额外职工"
    )

    run_command(
        ["python", "manage.py", "import_students",
         "--file", "data/file5_students_merged_v2.csv",
         "--mode", "clean", "--dry-run"],
        "Step 4d: Dry-run验证 - 学生"
    )

    # Step 5: 测试数据清理预览
    run_command(
        ["python", "manage.py", "cleanup_test_data", "--dry-run"],
        "Step 5: 测试数据清理预览"
    )

    # Step 6: 清理测试数据（自动执行，无需确认）
    print("\n" + "="*60)
    print("[Step 6: 清理测试数据]")
    print("⚠️  即将清理所有测试数据（自动执行）")
    print("="*60)

    run_command(
        ["python", "manage.py", "cleanup_test_data"],
        "Step 6: 执行清理"
    )

    # Step 7: 导入真实数据
    run_command(
        ["python", "manage.py", "import_staff",
         "--file", "data/dorm_managers_processed.csv"],
        "Step 7a: 导入宿管"
    )

    run_command(
        ["python", "manage.py", "import_staff",
         "--file", "data/counselors_processed.csv"],
        "Step 7b: 导入辅导员"
    )

    run_command(
        ["python", "manage.py", "import_staff",
         "--file", "data/additional_staff.csv"],
        "Step 7c: 导入额外职工"
    )

    run_command(
        ["python", "manage.py", "import_students",
         "--file", "data/file5_students_merged_v2.csv",
         "--mode", "clean"],
        "Step 7d: 导入学生"
    )

    # Step 8: 验证导入结果
    run_command(
        ["python", "scripts/verify_db_status.py"],
        "Step 8: 导入结果验证"
    )

    print("\n" + "="*60)
    print("导入完成")
    print(f"结束时间: {datetime.now()}")
    print("="*60)

if __name__ == "__main__":
    main()
