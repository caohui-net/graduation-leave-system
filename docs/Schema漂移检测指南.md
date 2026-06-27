# Schema漂移检测指南

**版本**: v1.0  
**最后更新**: 2026-06-27

---

## 概述

Schema漂移检测自动对比数据库实际状态与Django models定义，及早发现不一致问题。

**常见漂移场景**:
- 手动执行的DDL操作未生成migration
- 生产环境热修复未同步到代码
- 多分支并行开发导致的schema冲突
- 历史遗留的未记录变更

---

## 工作原理

```
Django Models → 生成临时数据库 → 对比实际数据库 → 输出差异SQL
```

1. 基于Django models创建临时数据库（应用所有migrations）
2. 使用migra工具对比临时库vs实际库
3. 输出差异SQL（如有）
4. 差异>阈值时CI告警

---

## 使用方法

### 本地手动检测

```bash
cd backend
export DB_HOST=localhost
export DB_NAME=graduation_dev
export DB_USER=postgres
export DB_PASSWORD=yourpassword

./scripts/check-schema-drift.sh
```

### CI自动检测

- **触发时机**: 每天凌晨2点自动执行
- **触发条件**: schedule或workflow_dispatch
- **失败处理**: 发送告警邮件/Slack通知

手动触发：
```bash
# GitHub Actions
gh workflow run deployment-check.yml
```

---

## 输出解读

### ✅ 无漂移
```
✅ No schema drift detected
Schema drift check completed successfully
```

### ❌ 检测到漂移
```
❌ Schema drift detected!

alter table "users" add column "new_field" varchar(100);
alter table "applications" drop column "deprecated_field";

Action required: Review differences and create migration if needed
```

**处理步骤**:
1. 确认差异是否预期内
2. 如果是手动变更，创建对应migration记录
3. 如果是未预期变更，回滚或修复

---

## 配置说明

### 依赖安装

```bash
pip install migra psycopg2-binary
```

### 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `DB_HOST` | 数据库主机 | `localhost` |
| `DB_NAME` | 数据库名称 | `graduation_prod` |
| `DB_USER` | 数据库用户 | `readonly_user` |
| `DB_PASSWORD` | 数据库密码 | `password` |

**权限要求**: 需要CREATEDB权限（用于创建临时库）

---

## 最佳实践

### 1. 定期检测
- 每日自动检测（staging/production）
- PR合并前手动检测

### 2. 漂移处理
```bash
# 发现漂移后，生成migration记录
python manage.py makemigrations --empty myapp
# 编辑migration文件，记录实际变更
```

### 3. 紧急修复流程
```
生产热修复 → 立即创建migration → 同步到staging/dev
```

### 4. 权限隔离
- 使用只读账号检测（安全）
- 临时库自动创建和清理

---

## 故障排查

### 问题1: migra未安装
```bash
pip install migra psycopg2-binary
```

### 问题2: 权限不足（无法创建临时库）
```sql
-- 授予CREATEDB权限
ALTER USER readonly_user CREATEDB;

-- 或使用有权限的账号
export DB_USER=migration_user
```

### 问题3: 误报（django_migrations表差异）
```bash
# 脚本已过滤django_migrations表，如仍有误报：
# 检查是否有其他元数据表差异
```

### 问题4: 检测超时
```bash
# 大型数据库可能较慢，调整超时：
timeout 600 ./scripts/check-schema-drift.sh
```

---

## 集成到发布流程

### 发布前检查
```bash
# 部署检查清单中添加
- [ ] Schema漂移检测通过
```

### 告警配置
```yaml
# .github/workflows/deployment-check.yml
on:
  schedule:
    - cron: '0 2 * * *'  # 每天检测
  
# 失败时发送通知
- name: Notify on failure
  if: failure()
  run: |
    curl -X POST $SLACK_WEBHOOK \
      -d '{"text":"Schema drift detected in production!"}'
```

---

## 高级功能

### 1. 生成修复SQL
```bash
# 输出差异SQL到文件
migra "$ACTUAL_DB" "$MODEL_DB" > schema_fix.sql

# 审查后应用
psql -f schema_fix.sql
```

### 2. 忽略特定表
```bash
# 修改脚本，添加过滤
migra --exclude-schema public.legacy_table "$ACTUAL_DB" "$MODEL_DB"
```

### 3. 对比两个环境
```bash
# 对比staging vs production
migra "$STAGING_DB_URL" "$PROD_DB_URL"
```

---

## 维护记录

| 日期 | 操作 | 备注 |
|------|------|------|
| 2026-06-27 | 初始版本 | P2自动化任务 |

---

**负责人**: 运维团队  
**审批**: 技术负责人
