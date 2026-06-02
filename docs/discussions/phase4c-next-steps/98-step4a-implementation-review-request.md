# Phase 4C Step 4A实现审查请求

**请求日期：** 2026-06-02  
**请求方：** Claude  
**审查目标：** Step 4A同步计划服务实现方案  
**文档编号：** 98

---

## 审查背景

根据文档97共识，已完成Step 4A服务文件创建：

**已创建文件：**
- `backend/apps/users/services/xg_user_sync.py`
- 实现：`plan_xg_user_sync(xg_users: List[dict]) -> Dict`

**待创建：**
- `backend/apps/users/tests/test_xg_user_sync.py`（8个测试场景）

---

## 审查要点

### 1. 服务实现逻辑验证

**实现路径：** `backend/apps/users/services/xg_user_sync.py`

**核心判定规则（文档97要求）：**

1. mapper有skip_reason → 计入skipped
2. mapper成功但本地不存在 → 计入missing_local，不创建
3. 本地存在但role≠student → 计入conflicts
4. 本地存在且是student → 计入would_update
5. phone/department无模型字段 → 输出warning

**请审查：**
- 是否正确调用map_xg_user_to_internal()
- 本地存在性检查是否正确（User.objects.get）
- 角色冲突判定是否准确
- missing_local计数逻辑是否符合Phase 1策略
- warning生成是否完整

### 2. 返回结构验证

**文档97要求的9个字段：**
```python
{
    'total_fetched': int,
    'mapped_count': int,
    'skipped_count': int,
    'skipped_by_reason': dict,
    'existing_count': int,
    'missing_local_count': int,
    'would_update_count': int,
    'conflicts': list,
    'warnings': list
}
```

**请审查：**
- 返回结构是否完整
- 字段类型是否正确
- skipped_by_reason的dict结构是否合理
- conflicts的list结构是否包含必要信息

### 3. 测试覆盖策略

**文档97要求的8个测试场景：**

1. mapper skip透传统计
2. 已存在学生进入existing
3. 不存在学生不创建（missing_local）
4. 本地角色冲突
5. 不覆盖class_id/is_graduating/graduation_year
6. phone/department无模型字段warning
7. 空输入
8. 混合场景

**请审查：**
- 这8个场景是否覆盖所有关键路径
- 是否需要补充场景（如多个skip_reason的统计）
- 测试数据构造策略是否合理
- mock策略（User.objects.get）是否充分

### 4. Phase 1边界保护

**关键约束（文档95/96/97强调）：**

- API不创建新用户（缺class_id/is_graduating/graduation_year）
- mapper返回class_id=None但skip_reason=None的情况必须处理
- 本地不存在 → 计入missing_local + warning

**请审查：**
- 新用户创建边界是否正确执行
- missing_local的warning信息是否清晰
- 是否误判为可创建用户

### 5. 模型字段gap处理

**P1发现（文档95）：**
- mapper输出phone/department
- User模型无这些字段
- Step 4A必须输出明确warning

**请审查：**
- warning是否在would_update_count>0时输出
- warning文本是否准确描述gap
- 是否影响existing_count/would_update_count判定

---

## 关键质疑点

### Q1：User.objects.get异常处理

当user_id不存在时，`User.objects.get()`抛出`User.DoesNotExist`。

**请审查：**
- 异常捕获是否正确
- 是否误将异常计入其他类别
- 是否遗漏其他可能异常（MultipleObjectsReturned）

### Q2：would_update计数准确性

当本地用户存在且role='student'时，计入would_update。

**请质疑：**
- 当前实现是否真的需要更新？
- mapper输出的字段有哪些可以写入User模型？
- 如果没有可写字段，would_update是否误导性？

根据文档95/97，当前User模型可安全写入的API字段：
- name（但CSV主导，是否允许API覆盖未决）
- phone/department（模型无字段，不能写）

**这是否意味着would_update实际为0？**

### Q3：conflicts结构完整性

当本地role≠student时，计入conflicts。

**请审查conflicts元素结构：**
- 是否包含user_id
- 是否包含reason（'role_mismatch'）
- 是否包含local_role和api_role用于对比
- 是否需要更多上下文信息

### Q4：skipped_by_reason统计

mapper可能返回多种skip_reason（文档93定义）：
- 'missing_required_field'
- 'invalid_user_identity'

**请审查：**
- skipped_by_reason的dict是否正确累加
- 是否处理None作为key的情况
- 统计逻辑是否健壮

### Q5：测试场景5的必要性

文档97要求测试"不覆盖class_id/is_graduating/graduation_year"。

**请质疑：**
- Step 4A是只读分析，不写DB
- 这个测试是否应该在Step 4B实现？
- 还是在Step 4A中验证"不计入可更新字段"？

---

## 期望输出

**Codex审查后请明确：**

1. **实现逻辑是否符合文档97共识**
   - 5条判定规则是否全部正确实现
   - 是否发现遗漏或错误判定

2. **测试覆盖是否充分**
   - 8个场景是否足够
   - 是否需要增删场景
   - mock策略是否合理

3. **关键质疑点的答案**
   - Q1-Q5是否暴露实现缺陷
   - 是否需要调整实现策略

4. **后续执行建议**
   - 如果实现有问题，先修正服务文件
   - 如果实现正确，直接创建测试文件
   - 测试通过后的下一步

---

## 审查方式

请使用 `/oh-my-claudecode:ask codex` 审查：
- 服务文件路径：`backend/apps/users/services/xg_user_sync.py`
- 参考文档：docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md
- 字段契约：docs/phase4c-xg-field-coverage.md

**重要：** 审查时请同时验证服务实现与共识文档的一致性。

---

**文档状态：** 等待Codex审查
