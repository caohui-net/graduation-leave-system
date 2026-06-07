#!/bin/bash
# 真实数据导入执行脚本（容器内手动执行）
# 使用方法：docker compose exec -it backend bash
# 然后在容器内执行：bash scripts/execute_import_manual.sh

set -e  # 遇到错误立即退出

echo "=== 真实数据导入流程（手动执行） ==="
echo "开始时间: $(date)"
echo ""

# Step 1: 验证当前状态
echo "[Step 1] 数据库状态验证"
python scripts/verify_db_status.py
echo ""

# Step 2: 备份数据库
echo "[Step 2] 数据库备份"
python scripts/backup_database.py
echo ""

# Step 3: CSV文件验证
echo "[Step 3] CSV文件行数验证"
wc -l data/file5_students_merged_v2.csv data/dorm_managers_processed.csv data/counselors_processed.csv data/additional_staff.csv
echo ""

# Step 4: Dry-run验证
echo "[Step 4] Dry-run导入验证"
python manage.py import_staff --file data/dorm_managers_processed.csv --dry-run
python manage.py import_staff --file data/counselors_processed.csv --dry-run
python manage.py import_staff --file data/additional_staff.csv --dry-run
python manage.py import_students --file data/file5_students_merged_v2.csv --mode clean --dry-run
echo ""

# Step 5: 测试数据清理预览
echo "[Step 5] 测试数据清理预览"
python manage.py cleanup_test_data --dry-run
echo ""

read -p "确认清理测试数据？(y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "操作取消"
    exit 1
fi

# Step 6: 清理测试数据
echo "[Step 6] 清理测试数据"
python manage.py cleanup_test_data
echo ""

# Step 7: 导入真实数据
echo "[Step 7] 导入真实数据"
python manage.py import_staff --file data/dorm_managers_processed.csv
python manage.py import_staff --file data/counselors_processed.csv
python manage.py import_staff --file data/additional_staff.csv
python manage.py import_students --file data/file5_students_merged_v2.csv --mode clean
echo ""

# Step 8: 验证导入结果
echo "[Step 8] 导入结果验证"
python scripts/verify_db_status.py
echo ""

echo "=== 导入完成 ==="
echo "结束时间: $(date)"
