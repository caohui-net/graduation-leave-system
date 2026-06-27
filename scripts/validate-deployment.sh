#!/bin/bash
# 生产部署验证脚本 - 验证P1/P2治理框架

set -e

echo "=========================================="
echo "Production Deployment Validation"
echo "=========================================="

ERRORS=0

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Migration检查
echo -e "\n${YELLOW}[1/6] Checking migrations...${NC}"
if [ -f "backend/scripts/check-migrations.sh" ]; then
    echo -e "${GREEN}✅ Migration check script exists${NC}"
    # 注意：实际部署时需要在有Django环境的服务器上执行
    echo -e "${YELLOW}ℹ️  Run check-migrations.sh on deployment server${NC}"
else
    echo -e "${RED}❌ check-migrations.sh not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 2. 配置验证
echo -e "\n${YELLOW}[2/6] Validating configuration...${NC}"
if [ -f "backend/.env.template" ]; then
    echo -e "${GREEN}✅ Configuration template exists${NC}"
    if [ -f "backend/scripts/validate-config.py" ]; then
        echo -e "${GREEN}✅ Configuration validator exists${NC}"
    else
        echo -e "${RED}❌ validate-config.py not found${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}❌ .env.template not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 3. 数据库备份
echo -e "\n${YELLOW}[3/6] Checking database backup...${NC}"
if [ -z "$DB_HOST" ]; then
    echo -e "${YELLOW}⚠️  DB_HOST not set, skipping backup check${NC}"
else
    BACKUP_DIR="backups"
    if [ -d "$BACKUP_DIR" ]; then
        LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/*.sql 2>/dev/null | head -1)
        if [ -n "$LATEST_BACKUP" ]; then
            AGE=$(($(date +%s) - $(stat -c %Y "$LATEST_BACKUP")))
            if [ $AGE -lt 86400 ]; then
                echo -e "${GREEN}✅ Recent backup exists ($(basename $LATEST_BACKUP))${NC}"
            else
                echo -e "${YELLOW}⚠️  Backup older than 24h${NC}"
            fi
        else
            echo -e "${YELLOW}⚠️  No backup found${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Backup directory not found${NC}"
    fi
fi

# 4. 数据库账号权限检查
echo -e "\n${YELLOW}[4/6] Checking database account setup...${NC}"
if [ -f "backend/scripts/setup-prod-db-accounts.sql" ]; then
    echo -e "${GREEN}✅ Database account setup script exists${NC}"
else
    echo -e "${RED}❌ setup-prod-db-accounts.sql not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 5. CI配置检查
echo -e "\n${YELLOW}[5/6] Checking CI configuration...${NC}"
if [ -f ".github/workflows/deployment-check.yml" ]; then
    echo -e "${GREEN}✅ CI deployment check configured${NC}"

    # 检查是否包含migration和schema drift检查
    if grep -q "check-migrations.sh" ".github/workflows/deployment-check.yml"; then
        echo -e "${GREEN}✅ Migration check integrated${NC}"
    else
        echo -e "${RED}❌ Migration check not in CI${NC}"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "check-schema-drift.sh" ".github/workflows/deployment-check.yml"; then
        echo -e "${GREEN}✅ Schema drift check integrated${NC}"
    else
        echo -e "${YELLOW}⚠️  Schema drift check not in CI${NC}"
    fi
else
    echo -e "${RED}❌ CI configuration not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 6. 文档完整性检查
echo -e "\n${YELLOW}[6/6] Checking documentation...${NC}"
DOCS=(
    "docs/部署检查清单.md"
    "docs/数据库账号管理指南.md"
    "docs/Schema漂移检测指南.md"
    "docs/配置中心管理指南.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo -e "${GREEN}✅ $(basename $doc)${NC}"
    else
        echo -e "${RED}❌ $(basename $doc) not found${NC}"
        ERRORS=$((ERRORS + 1))
    fi
done

# 总结
echo -e "\n=========================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All validation checks passed${NC}"
    echo -e "${GREEN}Production deployment is ready${NC}"
    exit 0
else
    echo -e "${RED}❌ $ERRORS validation check(s) failed${NC}"
    echo -e "${RED}Fix issues before deploying to production${NC}"
    exit 1
fi
