# Phase 4C 下一步优先级 - 最终共识

**日期：** 2026-06-02  
**参与方：** Codex + Claude  
**文档编号：** 93

---

## 共识结论

**一致决策：执行 A-prime - Step 2C-lite 字段映射契约优先。**

Codex与Claude完全同意：不跳过Step 2C，不直接实现写库同步命令。

---

## 核心共识点

### 1. 优先级顺序

✅ **立即执行：Step 2C-lite（30-40分钟）**
- 产出：`docs/phase4c-xg-field-coverage.md`
- 内容：字段映射表 + 处理规则 + API/CSV并存策略

✅ **随后执行：Step 3 只读mapper（40-50分钟）**
- 产出：`backend/apps/users/integrations/xg_user_mapper.py`
- 产出：`backend/apps/users/tests/test_xg_user_mapper.py`
- 范围：纯转换函数，不写数据库

✅ **延后执行：Step 4/5（依赖Step 3通过）**
- Step 4：幂等upsert + 冲突报告
- Step 5：management command入口

---

### 2. 风险识别共识

双方一致认可5个直接写库风险：

1. **主键风险**：`number`是否等同`student_id`未确认
2. **权限链风险**：`class_id`缺失导致辅导员可见性断裂
3. **毕业范围风险**：`is_graduating`/`graduation_year`缺失导致范围模糊
4. **角色识别风险**：`user_identity`值域未知导致角色错误
5. **回滚成本风险**：DB错误修复成本远高于mapper测试错误

---

### 3. 字段映射契约要求

✅ **必须包含内容：**
- 学工API字段清单（基于文档样例）
- 内部User模型必需字段清单
- 字段映射表（内部目标 + 来源字段 + 状态 + 处理规则）
- 缺失字段处理规则（跳过/报告/禁止）
- API/CSV并存策略
- Step 3 mapper测试样例

✅ **字段映射表示例：**

| 内部目标 | 来源字段 | 状态 | 处理规则 |
| --- | --- | --- | --- |
| User.user_id | number | 样例可用，需确认 | 必填；缺失跳过 |
| User.name | name | 样例可用，需确认 | 必填；缺失跳过 |
| User.role | user_identity | 值域未知 | 只接受学生值；未知跳过 |
| User.class_id | 未确认 | 缺失 | CSV维护，API不覆盖 |
| User.is_graduating | 未确认 | 缺失 | CSV维护，API不覆盖 |
| User.graduation_year | 未确认 | 缺失 | CSV维护，API不覆盖 |

---

### 4. API/CSV并存策略

✅ **共识原则：**
- 字段未完全覆盖前，API只能补充或更新可确定字段
- API不能替代CSV导入主路径
- 初期不因API未返回某用户就自动停用本地用户
- 先输出差异报告，等live数据稳定后再决定停用规则

---

### 5. Step 3范围界定

✅ **只做：**
- 纯转换函数：`map_xg_user_to_internal(xg_user: dict) -> dict`
- 单元测试：8个场景（完整映射 + 6种缺失 + 多缺失）
- 返回格式包含`skip_reason`字段说明跳过原因

✅ **不做：**
- 不写数据库
- 不实现Provider完整接口
- 不实现幂等upsert
- 不创建management command

---

### 6. 折中方案

✅ **可选Step 3.5：`sync_xg_users --dry-run`演示命令**
- 本质：Step 2C-lite + Step 3组合
- 只读取和输出映射报告，不写数据库
- 提高可见性，避免误写库
- 实现时机：Step 3 mapper通过测试后

---

## 执行授权

✅ Codex与Claude已达成完整共识  
✅ 执行方案明确且必要  
✅ 无分歧点  
✅ 用户授权自主执行  

**立即开始执行Step 2C-lite。**

---

**预计总耗时：** 80-105分钟（Step 2C-lite 30-40分钟 + Step 3 40-50分钟 + 可选Step 3.5 10-15分钟）
