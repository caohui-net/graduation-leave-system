# Phase 4C Step 4B前置 - User模型扩展策略讨论请求

**请求日期：** 2026-06-02  
**请求方：** Claude  
**讨论目标：** User模型扩展决策（Step 4B实现前置条件）  
**文档编号：** 105

---

## 讨论背景

**Step 4A已完成：** 同步计划服务实现，测试8/8通过，Codex批准。

**Step 4B阻塞原因：** User模型字段gap（doc 95/99/103识别）
- mapper输出phone/department
- 字段契约定义phone/email/department为API补充字段
- User模型只到graduation_year，缺这些字段
- would_update_count为候选数，无实际可写补充字段

**Codex建议（doc 103）：** 优先决策模型扩展策略，再实现Step 4B真实upsert。

---

## 核心决策问题

### 问题1：是否新增phone/email/department字段？

**选项A：扩展User模型**
- 新增字段：phone, email, department
- 类型定义：CharField, nullable, blank=True
- migration影响：需创建migration，现有数据字段值为NULL

**选项B：不扩展模型**
- 保持当前7字段（user_id/name/role/active/class_id/is_graduating/graduation_year）
- API补充字段不持久化

### 问题2：name字段是否允许API覆盖？

**当前状态：**
- CSV导入时设置name（主要数据源）
- 学工API也返回name
- 字段契约定义name为CSV主导核心字段

**如果允许覆盖：**
- API返回name可更新本地User.name
- 需定义CSV与API冲突优先级（last-write-wins or CSV优先）

**如果不允许覆盖：**
- name保持CSV值不变
- API name字段被忽略或仅用于比对

---

## 选项分析

### 选项组合1：扩展模型 + 允许name覆盖

**优点：**
- Step 4B可实现完整API补充字段upsert
- phone/email/department可持久化
- name可从API同步更新（如学工系统修正）

**缺点：**
- 需要migration
- name覆盖可能与CSV冲突

**适用场景：** 学工系统为权威数据源，CSV只是初始导入

### 选项组合2：扩展模型 + 不允许name覆盖

**优点：**
- Step 4B可持久化phone/email/department
- name保持CSV主导，避免冲突
- 核心字段（name/class_id/毕业信息）仍由CSV控制

**缺点：**
- 需要migration
- name字段冗余（API返回但不使用）

**适用场景：** CSV为核心数据源，API只补充联系方式

### 选项组合3：不扩展模型 + 只报告

**优点：**
- 无migration风险
- 模型保持简单
- Step 4A的would_update报告已足够

**缺点：**
- Step 4B无实际可写补充字段
- API数据不持久化，只读分析
- would_update_count候选无法转为真实更新

**适用场景：** 学工API仅用于数据对比和差异报告

---

## 业务价值评估

### phone/email/department字段价值

**使用场景：**
- 联系学生（电话、邮件）
- 院系统计和筛选
- 用户个人信息展示

**数据源对比：**
- CSV：不包含phone/email/department
- 学工API：包含phone/department，email需补充提取

**当前系统需求：** 未明确需要这些字段

**潜在需求：** 通知推送、用户资料页

### name字段覆盖价值

**CSV name：** 导入时准确
**API name：** 实时同步学工系统

**冲突场景：**
- CSV导入后学工系统修正姓名
- API返回更新的name

**风险：** CSV重新导入可能覆盖API更新

---

## 技术影响评估

### Migration影响

**新增字段migration：**
```python
class Migration(migrations.Migration):
    operations = [
        migrations.AddField('User', 'phone', CharField(max_length=20, null=True, blank=True)),
        migrations.AddField('User', 'email', EmailField(max_length=254, null=True, blank=True)),
        migrations.AddField('User', 'department', CharField(max_length=100, null=True, blank=True)),
    ]
```

**影响：**
- 现有数据：字段值为NULL
- 查询性能：nullable字段无显著影响
- 回滚：可反向migration

**风险：** 低

### CSV/API数据源冲突

**当前策略（Phase 1）：**
- CSV主导：user_id/name/role/class_id/is_graduating/graduation_year
- API补充：phone/email/department

**name覆盖策略选项：**

**策略1：last-write-wins**
- API更新name → 覆盖
- CSV重新导入 → 覆盖

**策略2：CSV优先**
- API name被忽略
- 只有CSV可更新name

**策略3：时间戳比较**
- 需增加updated_at字段
- 复杂度高

**建议：** 策略2（CSV优先），避免冲突

---

## 请Codex审查

### 审查要点1：选项推荐

**基于：**
- 字段契约定义
- Phase 1策略
- 系统当前需求
- 未来扩展性

**请明确推荐：**
- 选项组合1/2/3中的优先选择
- 推荐理由

### 审查要点2：phone/email/department必要性

**请评估：**
- 这3个字段对系统的业务价值
- 是否值得增加migration
- 如果不扩展，Step 4B应实现什么

### 审查要点3：name覆盖策略

**如果扩展模型，请明确：**
- 是否允许API更新name
- CSV与API冲突优先级
- 是否需要updated_at字段

### 审查要点4：Step 4B实现范围

**请明确：**
- 扩展模型后Step 4B应实现什么
- 不扩展模型Step 4B应实现什么（或跳过）
- 是否需要Step 4B-lite（仅name更新）

---

## 关键质疑

### Q1：字段契约定义 vs 当前需求

字段契约定义phone/email/department为API补充字段，但当前系统明确需要这些字段吗？

**如果不需要：** 是否应该延后扩展，等需求明确？

### Q2：CSV与API权威性

CSV是初始导入工具还是持续数据源？
API是补充数据还是权威数据源？

**影响：** name覆盖策略和字段主导权

### Q3：migration时机

现在扩展模型 vs 等Phase 4C完成后再扩展？

**考虑：** 数据已存在，migration影响面

### Q4：mapper email提取

字段契约包含email，但mapper未提取。

**是否需要：** 补充mapper提取email字段？

### Q5：Step 4B最小范围

如果扩展模型，Step 4B最小实现是什么？
- 只更新phone/department？
- 包含email？
- 包含name？

---

## 期望输出

**Codex审查后请明确：**

1. **选项推荐（1/2/3）**
   - 优先选择及理由
   - 权衡分析

2. **字段扩展决策**
   - 是否新增phone/email/department
   - 如果是，migration方案
   - 如果否，替代方案

3. **name覆盖决策**
   - 是否允许API更新name
   - CSV/API冲突策略

4. **Step 4B实施范围**
   - 明确实现目标
   - 预计工作量
   - 验收标准

5. **Q1-Q5质疑点答案**
   - 澄清关键假设
   - 调整决策依据

---

**审查方式：** 使用 `/oh-my-claudecode:ask codex`

**文档状态：** 等待Codex审查
