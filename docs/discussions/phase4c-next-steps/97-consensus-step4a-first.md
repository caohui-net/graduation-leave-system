# Phase 4C Step 3后续优先级 - 最终共识

**日期：** 2026-06-02  
**参与方：** Codex + Claude  
**文档编号：** 97

---

## 共识结论

**一致决策：执行 B-prime - Step 4A同步计划服务优先。**

Codex与Claude完全同意：不单独做Step 3.5，不做Step 4B真实upsert（先解决模型字段gap）。

---

## 核心共识点

### 1. 优先级：Step 4A同步计划服务

✅ **立即执行（40-50分钟）：**
- 文件：`backend/apps/users/services/xg_user_sync.py`
- 功能：`plan_xg_user_sync(xg_users: list[dict]) -> dict`
- 范围：生成同步计划，不写DB
- 内置dry-run summary能力

✅ **测试：** `backend/apps/users/tests/test_xg_user_sync.py`（8个场景）

---

### 2. 关键发现：User模型字段gap（P1）

**一致认定：**
- mapper输出phone/department/email
- User模型只到graduation_year
- 缺失：phone, email, department字段
- 影响：Step 4B不能实现真实upsert

**User模型当前字段：**
- user_id（主键）
- name
- role
- active
- class_id
- is_graduating
- graduation_year

**缺失字段：**
- phone（mapper输出，字段契约定义为API补充）
- email（字段契约定义，mapper未提取）
- department（mapper输出，字段契约定义为API补充）

---

### 3. 新用户创建边界（P1）

**一致规则：**
- Phase 1：API不创建新用户（缺class_id/is_graduating/graduation_year）
- mapper成功但本地不存在 → 计入missing_local，不创建
- Step 4A显式执行此规则

---

### 4. Step 4A判定规则

**同步计划服务必须实现：**

1. **mapper skip透传：** skip_reason存在 → 计入skipped_count
2. **本地不存在：** 不创建 → 计入missing_local_count
3. **角色冲突：** 本地存在但role≠student → 计入conflicts
4. **已存在学生：** 计入existing_count, would_update_count
5. **核心字段保护：** 不覆盖class_id/is_graduating/graduation_year
6. **补充字段警告：** phone/department无模型字段 → 输出warnings

---

### 5. Step 4A输出格式

**Summary结构：**
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

---

### 6. Step 4B延后（等待决策）

**前置条件：** 必须先决策模型扩展策略

**选项1（推荐）：模型扩展路线**
- 给User增加phone/email/department
- migration + 字段定义
- 实现幂等更新补充字段

**选项2：只更新姓名路线**
- 允许API更新name
- 定义CSV与API冲突优先级
- 不扩展模型

**双方建议：** 优先选项1

---

### 7. Step 3.5不单独实现

**一致共识：**
- dry-run价值在于计划能力（属于服务层）
- Step 4A已内置dry-run summary
- 不单独做命令层dry-run

---

### 8. Step 5延后

**命令入口等待：**
- Step 4B完成后再做
- 命令只做薄入口，不承载同步规则

---

## 执行计划

### Phase 1：Step 4A实现（立即执行）

**实现：**
1. 创建服务文件：`xg_user_sync.py`
2. 实现`plan_xg_user_sync()`函数
3. 创建测试文件：`test_xg_user_sync.py`
4. 8个测试场景
5. 运行测试验证

**预计时间：** 40-50分钟

### Phase 2：模型扩展决策（Step 4A后讨论）

**讨论：**
- 评估Step 4A的warning输出
- 决策选项1 vs 选项2
- 如果选项1，设计migration

**预计时间：** 讨论10-15分钟 + 实现30-40分钟

### Phase 3：Step 4B + Step 5（模型扩展后）

**延后到模型扩展决策完成。**

---

## 后续补充

**mapper改进（如果模型扩展包含email）：**
- mapper增加email字段提取
- 增加test_email_field测试

---

## 执行授权

✅ Codex与Claude已达成完整共识  
✅ 执行方案明确且必要  
✅ 无分歧点  
✅ 用户授权自主执行  

**立即执行Step 4A（40-50分钟）。**

**暂停点：** Step 4A完成后，讨论模型扩展策略，不自动执行Step 4B。
