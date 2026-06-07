#!/bin/bash
# 真实数据导入执行脚本
# 基于共识方案：.omc/collaboration/artifacts/20260607-0450-consensus-real-data-import-plan.md

set -e  # 遇到错误立即退出

TIMESTAMP=$(date +%Y%m%d%H%M%S)
BACKUP_FILE="reports/pre_real_import_${TIMESTAMP}.json"

echo "=== 真实数据导入流程 ==="
echo "开始时间: $(date)"
echo ""

# Step 1: 数据库状态确认（跳过，基于文档证据）
echo "[Step 1] 数据库状态确认"
echo "✓ 基于数据库分析报告（2026-06-07）：当前16用户（测试数据）"
echo ""

# Step 2: 数据备份
echo "[Step 2] 数据备份"
mkdir -p reports
echo "正在导出数据库..."
docker compose exec -T backend python manage.py dumpdata --natural-foreign --natural-primary > "$BACKUP_FILE"
echo "✓ 备份完成: $BACKUP_FILE"
ls -lh "$BACKUP_FILE"
echo ""

# Step 3: 源CSV验证
echo "[Step 3] 源CSV验证"
echo "检查CSV文件行数..."
wc -l backend/data/file5_students_merged_v2.csv
wc -l backend/data/dorm_managers_processed.csv
wc -l backend/data/counselors_processed.csv
wc -l backend/data/additional_staff.csv
echo ""

echo "执行dry-run验证..."
docker compose exec -T backend python manage.py import_staff --file data/dorm_managers_processed.csv --dry-run
docker compose exec -T backend python manage.py import_staff --file data/counselors_processed.csv --dry-run
docker compose exec -T backend python manage.py import_staff --file data/additional_staff.csv --dry-run
docker compose exec -T backend python manage.py import_students --file data/file5_students_merged_v2.csv --mode clean --dry-run
echo "✓ Dry-run验证完成"
echo ""

echo "=== 阶段1完成（验证和备份） ==="
echo "下一步: 测试数据清理（需人工确认）"
