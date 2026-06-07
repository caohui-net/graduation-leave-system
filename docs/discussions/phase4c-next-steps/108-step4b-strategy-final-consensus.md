# Phase 4C Step 4B策略最终共识

**日期：** 2026-06-02  
**参与方：** Codex + Claude  
**文档编号：** 108

---

## 共识结论

**一致决策：采用选项组合2（扩展User模型+不允许API覆盖name），立即执行Step 4B实现。**

---

## 核心决策

### 1. User模型扩展

**新增字段：**
- phone: CharField(max_length=20, null=True, blank=True)
- email: EmailField(null=True, blank=True)
- department: CharField(max_length=100, null=True, blank=True)

### 2. 字段权威性划分

| 字段类别 | 字段 | 权威来源 | API行为 |
|---------|------|---------|---------|
| 身份核心 | user_id | CSV/本地 | 只匹配 |
| 身份展示 | name | CSV | 不修改 |
| 角色权限 | role | CSV/本地 | 只验证 |
| 业务核心 | class_id/is_graduating/graduation_year | CSV | 不修改 |
| 补充资料 | phone/email/department | 学工API | 仅更新已存在学生 |

### 3. mapper扩展

**新增：** email字段提取

### 4. 更新规则

- API非空且与本地不同 → 更新
- API缺失/None/空 → 保持本地值
- 不创建新用户
- 角色冲突不更新
- 核心字段不覆盖

---

## Step 4B实施范围

**Phase 1：模型+migration（10-15分钟）**
- 修改backend/apps/users/models.py
- makemigrations生成migration
- migrate应用

**Phase 2：mapper扩展（10-15分钟）**
- 修改backend/apps/users/integrations/xg_user_mapper.py
- 修改backend/apps/users/tests/test_xg_user_mapper.py

**Phase 3：同步服务（25-40分钟）**
- 新增apply_xg_user_sync()函数
- 实现8个测试场景验收

**预计总时间：** 45-70分钟

---

## 验收标准（9点）

1. ✅ migration只包含phone/email/department
2. ✅ mapper测试覆盖email
3. ✅ 服务测试覆盖更新补充字段
4. ✅ 服务测试覆盖API缺失保持本地值
5. ✅ 服务测试覆盖幂等
6. ✅ 服务测试覆盖不创建用户
7. ✅ 服务测试覆盖角色冲突
8. ✅ 服务测试覆盖核心字段不覆盖
9. ✅ Step 4A warning调整

---

## 执行授权

✅ Codex推荐选项组合2（doc 106）  
✅ Claude完全同意（doc 107）  
✅ 无分歧点  
✅ 用户授权自主执行

**立即执行Step 4B Phase 1（模型扩展）。**
