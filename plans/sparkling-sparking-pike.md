# 生产环境 class_id 数据修复计划

## 问题描述

**问题**: 21,939个学生（99.4%）的 class_id 字段被错误写入为辅导员工号（纯数字），应该是班级名称（如"电信202201"）。

**影响范围**:
- 生产环境: 21,939/22,077 用户
- 开发环境: 21,939/22,077 用户
- 影响审批流程的班级路由逻辑

**数据对比**:
```
CSV源文件:  class_id = "电信(专升本)202403"
数据库实际: class_id = 19881345
```

---

## 修复策略（用户建议）

1. **备份生产环境数据**
2. **同步生产数据到开发/测试环境**
3. **在测试环境进行修复操作测试**

---

## 环境信息

**生产环境**:
- 服务器: 172.17.12.196
- 数据库容器: production-db-1
- 数据库名: graduation_leave
- 表名: users
- 受影响记录: 21,939/22,077

**测试环境 (Staging)**:
- 服务器: 172.17.12.196
- 数据库容器: staging-db-1
- 端口: 15432

**开发环境**:
- 服务器: 172.17.12.199
- 数据库: graduation_dev
- 表名: users_user

**数据源**:
- **毕业生**: backend/data/file5_students_merged_v2.csv (5,946条，class_id字段)
- **在校生**: docs/15975名在校生（不含毕业生）.xls (15,975条，班级字段)
- 完整覆盖21,940名学生

---

## 修复方案

### Phase 1: 备份生产数据

**目标**: 创建生产数据库完整备份，支持回滚

**步骤**:
```bash
# 1. SSH到生产服务器
ssh caohui@172.17.12.196

# 2. 导出生产数据库
docker exec production-db-1 pg_dump -U postgres graduation_leave \
  > /tmp/graduation_leave_backup_$(date +%Y%m%d_%H%M%S).sql

# 3. 压缩备份文件
gzip /tmp/graduation_leave_backup_*.sql

# 4. 验证备份文件大小和完整性
ls -lh /tmp/graduation_leave_backup_*.sql.gz
```

**成功标准**: 备份文件 >10MB，无错误信息

---

### Phase 2: 同步生产数据到测试环境

**目标**: 将生产数据复制到staging和开发环境

**步骤**:

**2.1 同步到Staging环境**:
```bash
# 在196服务器上
# 导出生产数据
docker exec production-db-1 pg_dump -U postgres graduation_leave \
  > /tmp/prod_export.sql

# 导入到staging
docker exec -i staging-db-1 psql -U postgres -d graduation_leave \
  < /tmp/prod_export.sql
```

**2.2 同步到开发环境**:
```bash
# 从196复制到199
scp caohui@172.17.12.196:/tmp/prod_export.sql /tmp/

# 导入到开发环境
psql -h localhost -U postgres -d graduation_dev < /tmp/prod_export.sql
```

**成功标准**: 
- staging环境users表有21,939条纯数字class_id记录
- 开发环境users_user表有21,939条纯数字class_id记录

---

### Phase 3: 开发修复脚本

**目标**: 编写Python脚本从CSV提取正确class_id并更新数据库

**脚本设计**:

```python
#!/usr/bin/env python3
"""
修复 class_id 数据脚本
从 CSV 读取正确的班级名称，更新数据库
"""
import csv
import psycopg2

def fix_class_id(csv_file, db_config, dry_run=True):
    # 1. 读取CSV构建 user_id -> class_id 映射
    mapping = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = row['user_id'].strip()
            class_id = row['class_id'].strip()
            mapping[user_id] = class_id
    
    # 2. 连接数据库
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    
    # 3. 批量更新
    updated = 0
    for user_id, class_id in mapping.items():
        if dry_run:
            print(f"[DRY RUN] {user_id}: {class_id}")
        else:
            cur.execute(
                "UPDATE users SET class_id = %s WHERE user_id = %s",
                (class_id, user_id)
            )
            updated += cur.rowcount
    
    if not dry_run:
        conn.commit()
    
    print(f"更新记录数: {updated}/{len(mapping)}")
```

**执行流程**:
1. 在staging环境执行 dry-run
2. 验证映射数量和格式
3. 执行实际更新
4. 验证结果

---

### Phase 4: 在Staging环境测试

**目标**: 验证修复脚本正确性

**步骤**:
```bash
# 1. 执行dry-run
python fix_class_id.py --csv backend/data/file5_students_merged_v2.csv \
  --db staging --dry-run

# 2. 查看前10条预期更新
# 应该看到 user_id -> 新class_id（班级名称）

# 3. 执行实际更新
python fix_class_id.py --csv backend/data/file5_students_merged_v2.csv \
  --db staging

# 4. 验证结果
docker exec staging-db-1 psql -U postgres -d graduation_leave -c "
  SELECT 
    COUNT(*) as 总数,
    COUNT(*) FILTER (WHERE class_id ~ '[^0-9]') as 文本格式,
    COUNT(*) FILTER (WHERE class_id ~ '^[0-9]+$') as 纯数字
  FROM users;
"
```

**成功标准**: 
- 文本格式class_id >21,900条
- 纯数字class_id <50条

---

### Phase 5: 在生产环境执行

**目标**: 修复生产数据

**前置条件**:
- ✅ 备份文件已创建
- ✅ Staging测试通过

**步骤**:
```bash
# 1. 最终确认备份
ls -lh /tmp/graduation_leave_backup_*.sql.gz

# 2. 执行修复（使用production-db-1容器）
python fix_class_id.py --csv backend/data/file5_students_merged_v2.csv \
  --db production

# 3. 验证结果
docker exec production-db-1 psql -U postgres -d graduation_leave -c "
  SELECT 
    COUNT(*) FILTER (WHERE class_id ~ '[^0-9]') as 文本格式,
    COUNT(*) FILTER (WHERE class_id ~ '^[0-9]+$') as 纯数字
  FROM users;
"

# 4. 抽查10个用户
docker exec production-db-1 psql -U postgres -d graduation_leave -c "
  SELECT user_id, name, class_id FROM users LIMIT 10;
"
```

**回滚方案**（如果失败）:
```bash
# 恢复备份
gunzip /tmp/graduation_leave_backup_*.sql.gz
docker exec -i production-db-1 psql -U postgres -d graduation_leave \
  < /tmp/graduation_leave_backup_*.sql
```

---

## 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 备份失败 | 低 | 高 | 验证备份文件大小，测试恢复 |
| CSV数据不完整 | 中 | 高 | 先验证CSV记录数=数据库记录数 |
| 更新脚本错误 | 低 | 高 | Staging环境充分测试，dry-run |
| 生产更新失败 | 低 | 高 | 事务控制，立即回滚 |

---

## 前置验证步骤

**在开始修复前，必须验证**：

```bash
# 1. 验证CSV记录数
wc -l backend/data/file5_students_merged_v2.csv
# 预期: 5947行（含表头）

# 2. 验证CSV中class_id字段格式
python3 << 'EOF'
import csv
with open('backend/data/file5_students_merged_v2.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    total = 0
    text_format = 0
    for row in reader:
        total += 1
        if row['class_id'] and not row['class_id'].isdigit():
            text_format += 1
    print(f"总记录: {total}")
    print(f"文本格式class_id: {text_format}")
    print(f"纯数字class_id: {total - text_format}")
EOF
# 预期: 文本格式 >5900

# 3. 验证CSV与数据库user_id的覆盖率
python3 << 'EOF'
import csv
import psycopg2

# 读取CSV的user_id集合
csv_ids = set()
with open('backend/data/file5_students_merged_v2.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csv_ids.add(row['user_id'])

# 查询数据库的user_id集合
conn = psycopg2.connect(
    host='172.17.12.196',
    dbname='graduation_leave',
    user='postgres'
)
cur = conn.cursor()
cur.execute("SELECT user_id FROM users WHERE class_id ~ '^[0-9]+$'")
db_ids = {row[0] for row in cur.fetchall()}

# 计算覆盖率
covered = csv_ids & db_ids
print(f"CSV记录数: {len(csv_ids)}")
print(f"数据库待修复记录数: {len(db_ids)}")
print(f"可覆盖记录数: {len(covered)}")
print(f"覆盖率: {len(covered)/len(db_ids)*100:.1f}%")
print(f"未覆盖记录数: {len(db_ids - csv_ids)}")

if len(db_ids - csv_ids) > 0:
    print("\n未覆盖的user_id样本（前10个）:")
    for uid in list(db_ids - csv_ids)[:10]:
        print(f"  {uid}")
EOF
# 预期: 覆盖率 >99%
```

**如果覆盖率 <95%**:
- 停止修复流程
- 调查未覆盖记录的来源
- 补充CSV数据或使用其他数据源

---

## 待确认事项

- [ ] CSV文件是否包含所有22,077个用户的正确class_id？（通过前置验证确认）
- [ ] 是否需要同时更新ClassMapping表？（待用户确认）
- [ ] 修复后是否需要重启应用？（待用户确认）
- [ ] 未被CSV覆盖的记录如何处理？（手动处理或保持现状）

---

## 任务清单

- [ ] Task #16: 备份生产数据库
- [ ] Task #17: 同步生产数据到开发/测试环境
- [ ] Task #18: 开发修复脚本并在测试环境验证
- [ ] Task #19: 在生产环境执行修复并验证
