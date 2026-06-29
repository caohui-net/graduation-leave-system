# class_id 字段修复记录

**日期**: 2026-06-29  
**修复人**: Claude (Kiro CLI)  
**环境**: 生产环境 + 测试环境

---

## 问题描述

### 发现时间
2026-06-29

### 问题现象
生产数据库中 99.4% 的学生（21,939/21,940）的 `class_id` 字段被错误写入为**8位纯数字**（辅导员工号），而非正确的**班级名称**（如"电信202201"）。

### 影响范围
- **生产环境**: 21,939 条错误记录
- **测试环境**: 同步生产数据，存在相同问题
- **业务影响**: 
  - 审批流程中的班级路由逻辑失效
  - 无法按班级统计和查询学生
  - 班级辅导员关联错误

### 数据示例

| 字段 | 错误值 | 正确值 |
|------|--------|--------|
| class_id | 19881345 | 电信202201 |
| class_id | 20210021 | 英语202302 |
| class_id | 20240026 | 生科202301 |

---

## 问题分析

### 根本原因
数据导入脚本 `import_students.py` 存在逻辑错误，将辅导员工号写入了 `class_id` 字段。

### 数据流追踪
1. **源数据**: CSV/Excel 文件中包含正确的班级名称
2. **导入脚本**: 直接复制 CSV 的 `class_id` 字段到数据库
3. **数据库**: 写入了错误的辅导员工号

### 关键发现
用户明确指出：**"教师工号与 class_id 无关，不应该产生任何映射关系"**

---

## 数据源分析

### 数据源文件

#### 1. 毕业生数据
- **文件**: `backend/data/file5_students_merged_v2.csv`
- **记录数**: 5,946 条
- **覆盖**: 毕业生（is_graduating=true）
- **字段**: 包含正确的 `class_id` 字段

#### 2. 在校生数据
- **文件**: `docs/15975名在校生（不含毕业生）.xls`
- **记录数**: 15,975 条
- **覆盖**: 在校生（is_graduating=null）
- **字段**: `班级` 列包含班级名称
- **问题**: 602 条记录的班级字段为空

### 数据覆盖统计

| 数据源 | 记录数 | 有效记录 |
|--------|--------|----------|
| CSV（毕业生） | 5,946 | 5,675 |
| Excel（在校生） | 15,975 | 15,373 |
| **总计** | **21,921** | **21,048** |
| 数据库学生总数 | - | 21,940 |
| **覆盖率** | - | **95.9%** |

### 数据缺失分析
- **Excel班级为空**: 602 条
- **两个数据源都未覆盖**: 289 条
- **总计未覆盖**: 891 条（4.1%）

---

## 修复方案

### 三阶段修复策略

#### 阶段1: 备份生产数据
```bash
# 生产数据库备份
docker exec production-db-1 pg_dump -U postgres -d graduation_leave \
  -F c -f /tmp/prod_backup_20260629.dump

# 备份大小: 3.8MB
# 保存位置: 172.17.12.196:/tmp/prod_backup_20260629.dump
```

#### 阶段2: 同步到测试环境
```bash
# 重建测试数据库
docker exec staging-db-1 psql -U postgres \
  -c "CREATE DATABASE graduation_leave WITH TEMPLATE template0;"

# 恢复备份
docker exec staging-db-1 pg_restore -U postgres \
  -d graduation_leave --clean --if-exists /tmp/prod_backup_20260629.dump
```

#### 阶段3: 开发修复脚本
- **脚本位置**: `backend/apps/users/management/commands/repair_class_id.py`
- **功能**: 
  1. 从 CSV 加载毕业生的 class_id
  2. 从 Excel 加载在校生的班级信息
  3. 通过 user_id (学号) 匹配更新数据库

### 修复脚本核心逻辑

```python
# 1. 加载数据源
graduating = load_from_csv('data/file5_students_merged_v2.csv')  # 5,675条
current = load_from_excel('docs/15975名在校生（不含毕业生）.xls')  # 15,373条
all_mapping = {**current, **graduating}  # 21,048条

# 2. 批量更新
for student in User.objects.filter(role='student'):
    if student.user_id in all_mapping:
        student.class_id = all_mapping[student.user_id]
        student.save(update_fields=['class_id'])
```

---

## 执行过程

### 测试环境验证

**执行命令**:
```bash
docker exec staging-backend-1 python3 manage.py repair_class_id --apply
```

**结果**:
- 需要更新: 21,048 条
- 未找到: 891 条
- 执行成功: ✅

**数据验证**:
```sql
SELECT 
  COUNT(*) FILTER (WHERE class_id ~ '[a-zA-Z一-龥]') as fixed,
  COUNT(*) FILTER (WHERE class_id ~ '^[0-9]{8}$') as corrupted
FROM users WHERE role='student';

-- 结果: fixed=21,049, corrupted=891
```

### 生产环境执行

**执行时间**: 2026-06-29 17:05  
**执行命令**:
```bash
docker exec production-backend-1 python3 manage.py repair_class_id --apply
```

**结果**:
- CSV加载: 5,675 条毕业生记录
- Excel加载: 15,373 条在校生记录
- 总计映射: 21,048 条记录
- 需要更新: 21,048 条
- 未找到: 891 条
- **执行成功**: ✅

### 清理错误数据

**问题**: 未修复的891条记录仍保留错误的辅导员工号  
**要求**: 设为空值，业务判定为"不处理"而非错误处理

**执行**:
```sql
-- 测试环境
UPDATE users SET class_id = NULL 
WHERE role='student' AND class_id ~ '^[0-9]{8}$';
-- 更新 891 条

-- 生产环境
UPDATE users SET class_id = NULL 
WHERE role='student' AND class_id ~ '^[0-9]{8}$';
-- 更新 891 条
```

---

## 最终结果

### 修复统计

| 状态 | 数量 | 百分比 | 说明 |
|------|------|--------|------|
| ✅ 已修复 | 21,049 | 95.9% | 从源数据成功恢复班级名称 |
| ⚠️ 设为空值 | 891 | 4.1% | 源数据缺失，设为NULL |
| ❌ 错误数据 | 0 | 0% | 无错误数据 |
| 📊 总计 | 21,940 | 100% | 全部学生 |

### 修复前后对比

| 指标 | 修复前 | 修复后 | 改善 |
|------|--------|--------|------|
| 错误记录数 | 21,939 | 0 | -100% |
| 正确记录数 | 1 | 21,049 | +2,104,800% |
| 空值记录数 | 0 | 891 | +891 |
| 错误率 | 99.4% | 0% | **-99.4%** |

### 样例验证

| 学号 | 修复前 | 修复后 |
|------|--------|--------|
| 2023130140202 | 20210021 | 英语202302 ✅ |
| 2023220240208 | 19881345 | 电信202302 ✅ |
| 2025230440223 | 20240026 | 生科202501 ✅ |
| 2023230240114 | 20240026 | 生科202301 ✅ |
| 2024300120531 | 20230044 | 土木202405(专升本) ✅ |

---

## 经验总结

### 成功因素
1. ✅ **完整备份**: 生产数据完整备份，确保可回滚
2. ✅ **测试验证**: 在staging环境充分测试后再上生产
3. ✅ **数据溯源**: 找到原始Excel数据源，覆盖95.9%记录
4. ✅ **业务理解**: 将未找到数据设为NULL而非保留错误值

### 改进建议

#### 1. 数据导入流程
- **建议**: 建立数据导入前的字段映射验证机制
- **实施**: 在 import_students.py 中添加 class_id 格式校验
- **预期**: 避免辅导员工号误写入 class_id

#### 2. 数据完整性
- **问题**: 891条学生缺少班级信息
- **建议**: 联系教务处补全这891名学生的班级数据
- **文件**: Excel中602条班级为空的记录需要补充

#### 3. 数据验证
- **建议**: 添加数据库约束，限制 class_id 格式
- **实施**: 
  ```sql
  ALTER TABLE users ADD CONSTRAINT check_class_id_format
  CHECK (class_id IS NULL OR class_id !~ '^[0-9]{8}$');
  ```
- **预期**: 防止纯数字工号误写入

#### 4. 文档更新
- **待更新**: docs/数据导入记录.md 需补充在校生Excel数据源
- **待更新**: 修复脚本需加入代码仓库并写入文档

---

## 附录

### 相关文件

#### 数据源
- backend/data/file5_students_merged_v2.csv - 毕业生数据
- docs/15975名在校生（不含毕业生）.xls - 在校生数据

#### 脚本
- backend/apps/users/management/commands/repair_class_id.py - 修复脚本
- backend/apps/users/management/commands/import_students.py - 原导入脚本

#### 备份
- 172.17.12.196:/tmp/prod_backup_20260629.dump - 生产环境备份

#### 计划
- plans/sparkling-sparking-pike.md - 修复计划文档

### 执行命令清单

```bash
# 1. 备份生产数据
docker exec production-db-1 pg_dump -U postgres -d graduation_leave \
  -F c -f /tmp/prod_backup_20260629.dump

# 2. 安装依赖（如需要）
docker exec production-backend-1 pip3 install xlrd

# 3. 执行修复（dry-run）
docker exec production-backend-1 python3 manage.py repair_class_id

# 4. 执行修复（实际执行）
docker exec production-backend-1 python3 manage.py repair_class_id --apply

# 5. 清理错误数据
docker exec production-db-1 psql -U postgres -d graduation_leave \
  -c "UPDATE users SET class_id = NULL WHERE role='student' AND class_id ~ '^[0-9]{8}$';"

# 6. 验证结果
docker exec production-db-1 psql -U postgres -d graduation_leave \
  -c "SELECT COUNT(*) FILTER (WHERE class_id IS NULL) as null_count, 
             COUNT(*) FILTER (WHERE class_id ~ '[a-zA-Z一-龥]') as fixed,
             COUNT(*) as total 
      FROM users WHERE role='student';"
```

---

**文档版本**: v1.0  
**创建日期**: 2026-06-29  
**最后更新**: 2026-06-29  
**状态**: ✅ 修复完成
