# Round 3 Claude分析 - Part 1: 架构与数据库

**分析日期：** 2026-05-27  
**分析人：** Claude Opus 4.7  
**分析范围：** 第1-2章（系统架构、数据库设计）

---

## 第1章：系统架构设计

### 发现的问题

#### MAJOR - 模块职责边界模糊

**问题描述：**
`integrations`模块职责定义为"外部系统集成"，但实际只对接宿舍管理系统。未来如需对接图书馆系统、财务系统，是否都放在同一模块？模块划分缺乏扩展性考虑。

**影响范围：**
- 代码组织混乱
- 难以维护多个外部系统
- 职责不清晰

**建议方案：**
```python
apps/integrations/
├── base.py           # 集成基类
├── dorm/            # 宿舍系统集成
│   ├── client.py
│   └── models.py
├── library/         # 图书馆系统（未来）
└── finance/         # 财务系统（未来）
```

#### MAJOR - Celery任务队列必要性存疑

**问题描述：**
设计中Celery用于：通知发送、文件上传、凭证生成。但单实例部署场景下，这些任务是否真的需要异步？
- 微信通知：HTTP请求通常<500ms，是否值得引入Celery复杂度？
- 文件上传：本地文件系统写入很快，异步意义不大
- 凭证生成：PDF生成可能需要异步，但频率低

**影响范围：**
- 增加系统复杂度（Redis、Celery Worker、Celery Beat）
- 增加故障点
- 增加运维成本

**建议方案：**
1. **Phase 1实施**：先同步实现，测量实际性能
2. **性能测试后决策**：如果通知发送成为瓶颈，再引入Celery
3. **渐进式引入**：只对真正耗时的操作（PDF生成）使用异步

#### MINOR - MinIO标记为"可选"但未说明决策标准

**问题描述：**
设计中MinIO标记为"可选的未来扩展"，但未说明何时需要MinIO：
- 文件数量达到多少？
- 存储容量达到多少？
- 什么场景触发迁移？

**建议方案：**
明确决策标准：
- 文件总数 > 100,000
- 存储容量 > 500GB
- 需要CDN加速
- 需要多实例部署时

### 优点总结

- ✓ 模块划分清晰（6个核心模块）
- ✓ 技术栈成熟稳定（Django 4.2 LTS）
- ✓ 单实例部署符合需求场景
- ✓ Docker容器化便于部署

### 改进建议

1. **简化初期架构**：Phase 1不引入Celery，先用同步实现
2. **明确扩展路径**：文档化何时需要MinIO、何时需要Celery
3. **模块重组**：integrations按外部系统分子目录

---

## 第2章：数据库设计

### 发现的问题

#### CRITICAL - applications_history表设计冗余

**问题描述：**
`applications_history`表存储完整申请快照（JSON），但：
1. **存储冗余**：每次状态变更存储完整JSON，数据量大
2. **查询困难**：JSON字段难以查询和分析
3. **与audit_logs重复**：audit_logs已记录字段级变更（old_value/new_value）

**影响范围：**
- 存储空间浪费（每个申请可能有5-10个版本）
- 查询性能差
- 维护成本高

**建议方案：**
**删除applications_history表**，改用audit_logs的字段级追踪：
```sql
-- audit_logs已有字段
field_name VARCHAR(100)     -- 修改字段
old_value TEXT              -- 修改前值
new_value TEXT              -- 修改后值

-- 查询申请历史
SELECT * FROM audit_logs 
WHERE resource_type='application' 
  AND resource_id=123 
ORDER BY created_at DESC;
```

如果确实需要完整快照，只在关键节点创建：
- 提交申请时（version=0）
- 最终通过时（version=final）

#### MAJOR - 乐观锁version字段使用场景不明确

**问题描述：**
`applications`表有`version`字段用于乐观锁，但：
1. **并发场景罕见**：同一申请同时被两个审批人操作的概率极低
2. **状态机已保护**：状态转换规则已限制非法操作
3. **增加复杂度**：客户端需要处理409冲突

**影响范围：**
- 客户端需要实现重试逻辑
- 用户体验差（需要刷新重试）
- 实际并发冲突可能很少发生

**建议方案：**
1. **Phase 1不实现乐观锁**：先用数据库事务+状态机保护
2. **监控实际冲突**：记录状态转换失败次数
3. **按需引入**：如果冲突频繁（>1%），再加乐观锁

#### MAJOR - 索引策略过度设计

**问题描述：**
`applications`表有9个索引，包括3个复合索引：
- `idx_approver_status` (current_approver_id, status, submit_time)
- `idx_student_status` (student_id, status, created_at)
- `idx_status_deleted` (status, is_deleted, submit_time)

**问题：**
1. **写入性能影响**：每次INSERT/UPDATE需要维护9个索引
2. **存储开销**：索引占用大量空间
3. **可能未使用**：部分索引可能查询覆盖不到

**影响范围：**
- 写入性能下降
- 存储空间浪费
- 维护成本高

**建议方案：**
**渐进式索引策略**：
1. **Phase 1只建基础索引**：
   - `idx_student_id` (学生查看自己申请)
   - `idx_status` (按状态筛选)
   - `idx_application_no` (唯一编号查询)

2. **性能测试后按需添加**：
   - 监控慢查询日志
   - 根据实际查询模式添加复合索引

3. **删除未使用索引**：
   - 定期检查索引使用率
   - 删除命中率<1%的索引

#### MAJOR - audit_logs表3年保留策略存储压力

**问题描述：**
审计日志保留3年，按500并发用户估算：
- 每天操作：500用户 × 10操作/天 = 5,000条
- 3年总量：5,000 × 365 × 3 = 5,475,000条
- 存储空间：~5.5M × 1KB = 5.5GB（仅audit_logs表）

**影响范围：**
- 查询性能下降（全表扫描慢）
- 备份时间长
- 存储成本高

**建议方案：**
1. **分区表**：按月分区，查询只扫描相关分区
```sql
CREATE TABLE audit_logs (
    ...
) PARTITION BY RANGE (created_at);

CREATE TABLE audit_logs_2026_05 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
```

2. **归档策略**：
   - 1年内：在线查询（PostgreSQL）
   - 1-3年：归档存储（压缩文件）
   - 3年后：删除或冷存储

3. **索引优化**：
   - 只在最近3个月分区建全索引
   - 历史分区只建时间索引

#### MINOR - 软删除is_deleted字段不一致

**问题描述：**
部分表有`is_deleted`字段（users, applications, attachments），部分表没有（approvals, notifications）。不一致的设计增加理解成本。

**建议方案：**
明确软删除策略：
- **需要软删除**：用户数据、申请数据、附件（合规要求）
- **不需要软删除**：审批记录、通知（历史数据，不删除）

### 优点总结

- ✓ 表结构规范，遵循3NF
- ✓ 外键约束清晰（ON DELETE策略合理）
- ✓ 字段类型选择合适
- ✓ 注释完整

### 改进建议

1. **删除applications_history表**：用audit_logs字段级追踪替代
2. **简化索引策略**：Phase 1只建基础索引，按需添加
3. **audit_logs分区**：按月分区，优化查询性能
4. **推迟乐观锁**：Phase 1不实现，监控后按需引入
5. **统一软删除策略**：明确哪些表需要软删除

---

## 实施建议优先级

### P0 - 必须修改（阻塞实施）
1. 删除applications_history表，简化设计
2. 简化索引策略（只建基础索引）

### P1 - 强烈建议（影响质量）
3. audit_logs分区表设计
4. 推迟乐观锁实现

### P2 - 可选优化
5. integrations模块重组
6. 明确MinIO决策标准
7. 统一软删除策略

---

**分析完成时间：** 2026-05-27  
**下一部分：** Part 2 - API与认证设计
