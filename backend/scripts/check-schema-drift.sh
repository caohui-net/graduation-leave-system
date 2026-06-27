#!/bin/bash
# Schema漂移检测 - 对比数据库实际状态与Django models定义

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Schema Drift Detection"
echo "=========================================="

# 环境变量检查
if [ -z "$DB_HOST" ] || [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ]; then
    echo -e "${RED}Error: Database credentials not set${NC}"
    echo "Required: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD"
    exit 1
fi

# 检查migra是否安装
if ! command -v migra &> /dev/null; then
    echo -e "${YELLOW}Warning: migra not installed, installing...${NC}"
    pip install migra psycopg2-binary -q
fi

# 构建数据库URL
DB_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}"

# 生成临时数据库（基于Django models）
TEMP_DB="${DB_NAME}_schema_temp_$$"
echo "Creating temporary database: $TEMP_DB"

createdb -h "$DB_HOST" -U "$DB_USER" "$TEMP_DB" 2>/dev/null || {
    echo -e "${YELLOW}Warning: Using existing temp database${NC}"
}

TEMP_DB_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${TEMP_DB}"

# 应用所有migrations到临时库
echo "Applying Django migrations to temp database..."
python manage.py migrate --database=default --settings=config.settings.base --run-syncdb --no-input 2>&1 | grep -v "No changes detected" || true

# 执行漂移检测
echo ""
echo "Comparing actual database vs Django models..."
echo "=========================================="

DRIFT_OUTPUT=$(mktemp)
migra --unsafe "$TEMP_DB_URL" "$DB_URL" > "$DRIFT_OUTPUT" 2>&1 || true

# 检查漂移
if [ -s "$DRIFT_OUTPUT" ]; then
    DRIFT_CONTENT=$(cat "$DRIFT_OUTPUT")

    # 过滤掉django_migrations表的差异（正常）
    if echo "$DRIFT_CONTENT" | grep -v "django_migrations" | grep -q "alter table\|create table\|drop table\|add column\|drop column"; then
        echo -e "${RED}❌ Schema drift detected!${NC}"
        echo ""
        cat "$DRIFT_OUTPUT"
        echo ""
        echo -e "${RED}Action required: Review differences and create migration if needed${NC}"

        # 清理
        dropdb -h "$DB_HOST" -U "$DB_USER" "$TEMP_DB" 2>/dev/null || true
        rm -f "$DRIFT_OUTPUT"
        exit 1
    else
        echo -e "${GREEN}✅ No significant schema drift detected${NC}"
    fi
else
    echo -e "${GREEN}✅ No schema drift detected${NC}"
fi

# 清理
echo "Cleaning up temporary database..."
dropdb -h "$DB_HOST" -U "$DB_USER" "$TEMP_DB" 2>/dev/null || true
rm -f "$DRIFT_OUTPUT"

echo ""
echo -e "${GREEN}Schema drift check completed successfully${NC}"
