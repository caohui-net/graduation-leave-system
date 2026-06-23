#!/bin/bash
# 环境文件路径检测脚本
# 用法: bash check-file-structure.sh

echo "=== 环境文件路径检测 ==="

ERRORS=0

# 检查不应存在的重复目录
echo "检查重复目录结构..."
if [ -d "backend/backend" ]; then
    echo "❌ 发现重复目录: backend/backend/"
    find backend/backend -type f | head -5
    ERRORS=$((ERRORS + 1))
fi

if [ -d "backend/frontend" ]; then
    echo "❌ 发现重复目录: backend/frontend/"
    find backend/frontend -type f | head -5
    ERRORS=$((ERRORS + 1))
fi

# 检查关键文件位置
echo "检查关键文件位置..."
FILES=(
    "backend/apps/applications/services.py"
    "backend/scripts/deploy-staging.sh"
    "backend/scripts/deploy-prod.sh"
    "backend/docs/staging-test-checklist.md"
    "frontend/src/views/ApplicationTypeSelect.vue"
)

for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "⚠️  缺失文件: $file"
        ERRORS=$((ERRORS + 1))
    else
        echo "✓ $file"
    fi
done

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ 文件结构正常"
    exit 0
else
    echo "❌ 发现 $ERRORS 个问题"
    exit 1
fi
