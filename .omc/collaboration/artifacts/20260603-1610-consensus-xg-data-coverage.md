# XG API数据覆盖度分析 - Claude-Codex共识文档

**协作类型：** 独立分析 → 共识综合  
**参与方：** Claude + Codex  
**综合方：** Claude  
**完成时间：** 2026-06-03T16:10:00Z

---

## 一、核心共识

### 1.1 总体结论

**Claude与Codex一致认定：XG API当前数据 ❌ 无法替代CSV主数据源，只能作为补充信息源。**

**关键证据：**
- 缺失3个P0关键字段：`class_id`、`is_graduating`、`graduation_year`
- 缺失班级-辅导员映射关系
- 缺失宿舍清退状态数据
- 基础字段质量优秀（number/name/status 100%完整）

### 1.2 推荐策略

**双方一致推荐：Phase 1（CSV主导 + XG API补充）**

```
数据流向：
CSV导入 → 创建用户 + 核心业务字段（class_id/is_graduating/graduation_year）
   ↓
XG API → 仅更新已存在用户的补充字段（phone/department/active）
```

---

## 二、字段覆盖度对比分析

### 2.1 Claude分析（数据质量视角）

| 维度 | 覆盖度 | 评分 |
|-----|-------|------|
| 完全覆盖字段 | 3/11 (27%) | name/number/department |
| 部分覆盖字段 | 1/11 (9%) | phone (80%完整) |
| 无覆盖字段 | 7/11 (64%) | 包括3个CRITICAL字段 |
| 数据质量综合 | 95/100 | A级 |

### 2.2 Codex分析（业务流程视角）

| 业务域 | 覆盖情况 | 影响等级 |
|-------|---------|---------|
| 身份识别 | ✓ 可用 | number/name 100% |
| 申请资格判定 | ✗ 不可用 | 缺is_graduating/graduation_year |
| 审批路由分配 | ✗ 不可用 | 缺class_id+映射关系 |
| 宿舍清退验证 | ✗ 不可用 | 非用户API范围 |
| 展示信息补充 | ⚠️ 部分可用 | phone 80%, department存在 |

### 2.3 共识结论

**一致认定：**
- 基础字段覆盖良好（身份识别可用）
- 核心业务字段缺失严重（3/7必填字段缺失）
- 数据质量优秀但覆盖度不足

---

## 三、关键缺失字段影响对比

### 3.1 class_id缺失

**Claude评估：** 🔴 CRITICAL - 阻断核心业务流程
- 无法自动分配审批人
- 无法建立ClassMapping
- 新用户创建缺少必填字段

**Codex评估：** P0 - 审批路由无法落地
- 无法完成 `class_id -> ClassMapping -> counselor` 查询
- 禁止用院系/专业/班级名称临时拼接class_id

**共识：** 两方一致认定为P0阻断性问题。class_id必须由CSV维护，不能推导或假设。

### 3.2 is_graduating缺失

**Claude评估：** 🔴 CRITICAL - 影响核心业务逻辑
- 无法判定申请资格
- 批次管理困难

**Codex评估：** P0 - 申请资格判定失败
- XG API总量32,039条，远超"当届毕业生约1000人"
- 直接同步会扩大账号范围和申请入口

**共识：** P0问题。API不得自行创建申请资格，继续由CSV维护毕业生名单。

### 3.3 graduation_year缺失

**Claude评估：** 🔴 CRITICAL - 影响数据归档
- 数据归档困难
- 报表统计缺少维度

**Codex评估：** P0 - 批次归档失去依据
- 无法区分往届/当届/下一届
- 统计审核批次关闭失去依据

**共识：** P0问题。继续由CSV维护，只有XG提供可信毕业年份后才允许API主导模式。

---

## 四、Codex独有发现（实现层面）

### 4.1 Mapper与实际数据结构不匹配（P1）

**问题：** 实际XG API返回：
```json
"user_identity": {"id": 4, "name": "学生"}
```

当前mapper假设 `user_identity` 为字符串值 `'1'` 或 `'student'`，导致实际学生可能被全部跳过。

**位置：** `backend/apps/users/integrations/xg_user_mapper.py:41, 59-67`

**建议：** 支持对象结构，优先按 `user_identity.name == "学生"` 判定。

### 4.2 Department数组处理错误（P1）

**问题：** 实际返回为数组：
```json
"department": [{"name": "计算机学院", "level": 2}]
```

当前mapper直接赋值，可能将列表写入数据库字符串字段。

**位置：** `backend/apps/users/integrations/xg_user_mapper.py:44, 81`

**建议：** 取 `department[0].name` 或按层级选择，添加空数组测试。

### 4.3 字段覆盖文档状态过期（P1）

**问题：** `docs/phase4c-xg-field-coverage.md` 仍标记"待live测试确认"，但实际采集已完成。

**建议：** 升级为基于2026-06-03 live样本的正式版本。

---

## 五、数据质量评估对比

### 5.1 Claude评估

| 指标 | 得分 | 等级 |
|-----|------|------|
| 数据完整性 | 95/100 | A |
| 关联完整性 | 97/100 | A |
| 数据一致性 | 100/100 | A+ |
| 可用性 | 90/100 | A |
| **综合得分** | **95/100** | **A** |

### 5.2 Codex评估

| 维度 | 评价 | 风险 |
|-----|------|------|
| 身份基础字段 | 高 | 样本量仅20需扩大验证 |
| 手机号质量 | 中 | 20%空字符串需归一化 |
| 关联对象质量 | 中高 | user对象10%缺失需容错 |
| 结构一致性 | 中 | 响应结构与文档不一致 |
| 业务覆盖质量 | 低 | 缺核心字段阻断替代 |

### 5.3 共识

**一致认定：**
- XG提供的字段质量优秀（95/100, A级）
- 但业务字段覆盖度严重不足
- 存在实现层面适配问题需修复

---

## 六、推荐策略详细规则

### 6.1 Phase 1执行规则

**允许操作：**
- ✓ CSV创建维护所有用户主数据
- ✓ XG API匹配本地已存在学生
- ✓ XG API更新phone/email/department/active
- ✓ 对空值、缺失对象、错误结构容错
- ✓ 输出dry-run报告

**禁止操作：**
- ✗ XG API创建新学生
- ✗ XG API覆盖class_id/is_graduating/graduation_year
- ✗ 因XG未返回而自动停用本地用户
- ✗ 用部门名/班级名推导class_id
- ✗ 将XG用户API视为宿舍清退接口

### 6.2 切换到Phase 2的前提条件

**Codex定义的门槛（必须全部满足）：**
1. XG提供稳定唯一class_id，能与ClassMapping对齐
2. 提供is_graduating和graduation_year或等价字段
3. 提供辅导员employee_id及班级-辅导员关系
4. 支持按条件过滤或可靠增量同步
5. 全量采集测试稳定，报告口径统一
6. 完成毕业生名单与CSV差异对账，业务方确认规则

---

## 七、立即行动清单

### 7.1 修复mapper实现问题（P1，本周）

**Codex识别，Claude确认执行：**
1. 更新 `map_xg_user_to_internal()`：
   - 支持 `user_identity.name == "学生"` 和 `user_identity.id == 4`
   - 支持 `department` 数组，取 `department[0].name`
   - `phone=""` 归一化为 NULL
   - 完整 `status` 映射规则

2. 添加基于真实结构的单元测试

3. 更新 `docs/phase4c-xg-field-coverage.md`：
   - 从"待live确认"改为"基于2026-06-03 live样本"
   - 明确"不可替代CSV"结论

### 7.2 文档更新（本周）

1. 更新 `docs/PROJECT-SUMMARY.md`：
   - 添加XG API数据分析完成记录
   - 确认Phase 1策略

2. 更新 `.omc/session-context.json`：
   - 记录协作讨论完成
   - 引用本共识文档

3. 在 `docs/数据对接说明文档.md` 中明确Phase 1策略

### 7.3 向外部系统确认缺失接口（本月）

**Codex建议，需业务方推进：**
- 向XG/教务系统确认：毕业批次字段、班级编码
- 向人事系统确认：班级辅导员关系接口
- 向宿舍系统确认：清退状态实时API

---

## 八、分歧与差异

**无实质性分歧。**

Claude侧重数据质量和业务影响评估，Codex侧重实现层面风险和具体修复建议。两方结论完全一致，分析互补。

---

## 九、最终裁决

**审查结论：**
- ✓ **通过**"CSV主导 + XG API补充"策略
- ✗ **不通过**"XG API替代CSV主数据源"策略
- ⚠️ **要求修复** mapper实现问题后再执行API同步

**生效时间：** 2026-06-03  
**下次审查：** 2026-09-01（秋季学期，重新评估XG API字段扩展情况）

---

**协作文档：**
- Claude分析：`.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md`
- Codex审查：`.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md`
- 本共识文档：`.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md`

