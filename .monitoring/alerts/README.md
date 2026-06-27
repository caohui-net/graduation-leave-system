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
