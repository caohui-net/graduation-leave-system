#!/bin/bash
# 监控告警配置脚本 - Schema漂移和Migration检测告警

set -e

echo "=========================================="
echo "Monitoring & Alert Configuration"
echo "=========================================="

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. 创建告警配置目录
ALERT_DIR=".monitoring/alerts"
mkdir -p "$ALERT_DIR"

# 2. Schema漂移告警配置
cat > "$ALERT_DIR/schema-drift-alert.json" << 'EOF'
{
  "name": "Schema Drift Detection Alert",
  "description": "Alert when schema drift is detected between database and Django models",
  "trigger": {
    "type": "cron",
    "schedule": "0 2 * * *",
    "command": "backend/scripts/check-schema-drift.sh"
  },
  "conditions": {
    "exit_code": 1,
    "contains": "Schema drift detected"
  },
  "actions": [
    {
      "type": "log",
      "level": "error",
      "message": "Schema drift detected in production database"
    },
    {
      "type": "webhook",
      "url": "${ALERT_WEBHOOK_URL}",
      "payload": {
        "text": "⚠️ Schema drift detected in {{environment}}",
        "severity": "high",
        "timestamp": "{{timestamp}}"
      }
    }
  ],
  "rate_limit": {
    "interval": "1h",
    "max_alerts": 3
  }
}
EOF

echo -e "${GREEN}✅ Schema drift alert configuration created${NC}"

# 3. Migration检查告警配置
cat > "$ALERT_DIR/migration-check-alert.json" << 'EOF'
{
  "name": "Unapplied Migration Alert",
  "description": "Alert when unapplied migrations are detected before deployment",
  "trigger": {
    "type": "pre_deploy",
    "command": "backend/scripts/check-migrations.sh"
  },
  "conditions": {
    "exit_code": 1,
    "contains": "unapplied migration"
  },
  "actions": [
    {
      "type": "block_deployment",
      "message": "Deployment blocked: unapplied migrations detected"
    },
    {
      "type": "log",
      "level": "error",
      "message": "Unapplied migrations detected, deployment blocked"
    }
  ]
}
EOF

echo -e "${GREEN}✅ Migration check alert configuration created${NC}"

# 4. 配置验证失败告警
cat > "$ALERT_DIR/config-validation-alert.json" << 'EOF'
{
  "name": "Configuration Validation Alert",
  "description": "Alert when environment configuration validation fails",
  "trigger": {
    "type": "pre_deploy",
    "command": "backend/scripts/validate-config.py {{env_file}}"
  },
  "conditions": {
    "exit_code": 1
  },
  "actions": [
    {
      "type": "block_deployment",
      "message": "Deployment blocked: configuration validation failed"
    },
    {
      "type": "log",
      "level": "error",
      "message": "Configuration validation failed for {{environment}}"
    },
    {
      "type": "webhook",
      "url": "${ALERT_WEBHOOK_URL}",
      "payload": {
        "text": "❌ Configuration validation failed for {{environment}}",
        "severity": "critical"
      }
    }
  ]
}
EOF

echo -e "${GREEN}✅ Configuration validation alert created${NC}"

# 5. 创建告警配置README
cat > "$ALERT_DIR/README.md" << 'EOF'
# 监控告警配置

本目录包含三环境治理框架的监控告警配置。

## 告警类型

### 1. Schema漂移告警 (`schema-drift-alert.json`)
- **触发**: 每日凌晨2点自动检测
- **条件**: 数据库实际状态与Django models不一致
- **动作**:
  - 记录错误日志
  - 发送Webhook通知（可配置Slack/钉钉）
- **限流**: 1小时内最多3次告警

### 2. Migration检查告警 (`migration-check-alert.json`)
- **触发**: 部署前自动检查
- **条件**: 检测到未应用的migrations
- **动作**:
  - 阻断部署
  - 记录错误日志

### 3. 配置验证告警 (`config-validation-alert.json`)
- **触发**: 部署前自动检查
- **条件**: 环境配置验证失败
- **动作**:
  - 阻断部署
  - 记录错误日志
  - 发送Webhook通知

## 集成方式

### GitHub Actions集成

已在 `.github/workflows/deployment-check.yml` 中集成：
- Migration检查（PR/push时触发）
- Schema漂移检测（每日定时）

### Webhook配置

设置环境变量：
```bash
export ALERT_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

支持的Webhook格式：
- Slack Incoming Webhooks
- 钉钉机器人
- 企业微信机器人
- 自定义HTTP Webhook

### 日志集成

告警日志写入：
- 开发环境: `logs/alerts.log`
- 生产环境: `/var/log/graduation/alerts.log`

## 测试告警

```bash
# 测试Schema漂移告警
cd backend
./scripts/check-schema-drift.sh || echo "Alert triggered"

# 测试Migration检查告警
cd backend
./scripts/check-migrations.sh || echo "Alert triggered"

# 测试配置验证告警
cd backend
python scripts/validate-config.py .env.production || echo "Alert triggered"
```

## 告警静默

临时禁用告警（维护窗口）：
```bash
export DISABLE_ALERTS=true
```

## 告警历史

查看告警历史：
```bash
grep "Schema drift\|unapplied migration\|validation failed" /var/log/graduation/alerts.log
```

## 升级告警

当前为基础配置，未来可集成：
- Prometheus + Alertmanager
- Grafana告警
- PagerDuty
- OpsGenie
EOF

echo -e "${GREEN}✅ Alert configuration README created${NC}"

# 6. 创建告警测试脚本
cat > "$ALERT_DIR/test-alerts.sh" << 'EOF'
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
EOF

chmod +x "$ALERT_DIR/test-alerts.sh"
echo -e "${GREEN}✅ Alert test script created${NC}"

# 完成
echo ""
echo "=========================================="
echo -e "${GREEN}✅ Monitoring & Alert Configuration Complete${NC}"
echo ""
echo "Files created:"
echo "  - .monitoring/alerts/schema-drift-alert.json"
echo "  - .monitoring/alerts/migration-check-alert.json"
echo "  - .monitoring/alerts/config-validation-alert.json"
echo "  - .monitoring/alerts/README.md"
echo "  - .monitoring/alerts/test-alerts.sh"
echo ""
echo "Next steps:"
echo "  1. Configure webhook URL: export ALERT_WEBHOOK_URL=..."
echo "  2. Test alerts: .monitoring/alerts/test-alerts.sh"
echo "  3. Review CI integration in .github/workflows/deployment-check.yml"
