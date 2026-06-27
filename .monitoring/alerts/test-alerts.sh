#!/bin/bash
# 告警测试脚本

echo "Testing alerts..."

# 测试Schema漂移告警
echo "[1/3] Testing schema drift alert..."
cd ../.. && cd backend
if ! ./scripts/check-schema-drift.sh 2>&1 | grep -q "No schema drift"; then
    echo "✅ Schema drift alert would trigger"
else
    echo "ℹ️  No schema drift detected"
fi

# 测试Migration检查告警
echo "[2/3] Testing migration check alert..."
if ! ./scripts/check-migrations.sh 2>&1 | grep -q "No unapplied"; then
    echo "✅ Migration check alert would trigger"
else
    echo "ℹ️  No unapplied migrations"
fi

# 测试配置验证告警
echo "[3/3] Testing config validation alert..."
if [ -f ".env.production.example" ]; then
    if ! python scripts/validate-config.py .env.production.example 2>&1 | grep -q "passed"; then
        echo "✅ Config validation alert would trigger"
    else
        echo "ℹ️  Configuration valid"
    fi
else
    echo "⚠️  .env.production.example not found"
fi

cd ../..
echo "Alert tests completed"
