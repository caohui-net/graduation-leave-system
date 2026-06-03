# Codex审查请求：XG API数据覆盖度分析

**审查类型：** 数据对接方案审查  
**请求方：** Claude  
**审查方：** Codex  
**日期：** 2026-06-03

---

## 一、审查目标

分析XG学工系统API实际采集的数据是否满足毕业生离校申请审批系统的业务需求。

**关键问题：**
1. XG API提供的字段能否支持核心业务流程？
2. 缺失的字段对系统有何影响？
3. 数据质量是否达到生产标准？
4. 推荐何种数据对接策略？

---

## 二、审查范围

### 需求文档
- `docs/数据对接说明文档.md` - 定义系统对数据的需求

**关键需求：**
- 学生基本信息：student_id, name, department, major, **class_id**, grade, **graduation_year**, **is_graduating**, phone, email
- 辅导员基本信息：employee_id, name, department, phone, email, is_active
- 班级-辅导员映射：class_id, counselor_employee_id

### 实际数据文档
- `docs/XG-API-ACTUAL-DATA-SAMPLES.md` - XG API实际采集数据（2026-06-03，32,039条记录）
- `docs/phase4c-xg-field-coverage.md` - 字段映射分析文档
- `docs/XG-API-DATA-EXAMPLES.md` - API数据结构示例

**实际提供字段：**
- number（学号/工号）
- name（姓名）
- phone（手机号，80%完整）
- department（部门）
- status（状态）
- user_identity（身份信息）

---

## 三、审查要点

### 3.1 字段覆盖度
- 必填字段是否完整？
- 缺失哪些关键字段？
- 缺失字段对业务的影响？

### 3.2 数据质量
- 字段完整性（NULL值/空字符串比例）
- 数据准确性
- 数据一致性

### 3.3 业务可行性
- **class_id缺失** - 能否自动分配审批人？
- **is_graduating缺失** - 能否判定申请资格？
- **graduation_year缺失** - 能否正确归档？

### 3.4 对接策略
评估以下方案可行性：
- 方案A：CSV主导 + API补充（当前实施）
- 方案B：API主导 + CSV补充（需字段扩展）

---

## 四、期望输出

### Codex审查文档结构
1. **数据完整性评估**
   - 必填字段覆盖情况
   - 缺失字段清单及影响评级

2. **数据质量评估**
   - 完整性评分
   - 准确性评分
   - 可用性评分

3. **业务影响分析**
   - 关键缺失字段对核心流程的影响
   - 风险等级评估

4. **对接策略建议**
   - 推荐方案
   - 理由说明
   - 风险和缓解措施

5. **问题清单**
   - P0（阻断性问题）
   - P1（重要问题）
   - P2（优化建议）

---

## 五、审查标准

**严格性要求：**
- 基于实际数据，不假设未验证字段
- 明确标注每个结论的证据来源
- 识别所有P0阻断性问题
- 评估数据质量对生产环境的影响

**输出格式：**
- 结构化文档（Markdown）
- 清晰的问题分级（P0/P1/P2）
- 每个问题包含：现象/影响/建议

---

## 六、相关文档路径

**需求文档：**
- `docs/数据对接说明文档.md` （第2-4章：学生/辅导员/班级映射需求）

**实际数据：**
- `docs/XG-API-ACTUAL-DATA-SAMPLES.md` （实际采集测试结果）
- `docs/XG-API-DATA-EXAMPLES.md` （API响应结构示例）
- `docs/phase4c-xg-field-coverage.md` （字段映射方案）

**系统设计：**
- `docs/design/2026-05-27-system-design.md` （User模型定义）
- `backend/apps/users/models.py` （User模型实现）

---

## 七、审查输出位置

**Codex审查结果：** `.omc/collaboration/artifacts/20260603-[时间]-codex-xg-data-review.md`

---

**请求状态：** 待Codex审查
