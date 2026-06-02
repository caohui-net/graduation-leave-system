# Phase 4C Step 4A最终共识 - 实现完成

**日期：** 2026-06-02  
**参与方：** Codex + Claude  
**文档编号：** 104

---

## 共识结论

**一致决策：Step 4A同步计划服务实现完成，批准提交，进入Step 4B模型扩展讨论。**

Codex与Claude完全同意：P1修复已落地，测试覆盖完整，8/8通过验收。

---

## 核心共识点

### 1. P1修复执行完成

**问题：** would_update_count语义歧义（doc 99识别）

**修复完成：**
- ✅ docstring注释："候选数，不代表当前模型可持久化写入数"
- ✅ warning强化："{N} sync candidates exist, but no API supplemental fields can be persisted"
- ✅ user_id主键注释：不捕获MultipleObjectsReturned

**Codex评估：** 通过。语义已明确锁定，不再误导。

### 2. 测试覆盖验收通过

**测试结果：** 8/8 passed (0.032s)

**场景覆盖（全部通过）：**
1. ✅ mapper skip透传统计（修正断言匹配实际skip_reason）
2. ✅ existing student候选数语义验证
3. ✅ missing_local不创建用户（Phase 1边界）
4. ✅ role conflict结构完整性
5. ✅ 服务只读不修改DB核心字段
6. ✅ 字段gap warning强化文本
7. ✅ 空输入处理
8. ✅ 混合场景分类互斥性

**Codex评估：** 测试策略正确（Django TestCase + 真实DB），覆盖完整。

### 3. 发现处理

**发现：** mapper skip_reason实际值为字段级别
- 'missing_user_id'
- 'missing_name'
- 'unknown_user_identity: {value}'

**处理：** 测试断言调整匹配实际输出，合理且必要。

**Codex确认：** 修正正确。

---

## 批准决策

**Codex批准（doc 103）：**
1. ✅ 批准提交当前服务修改和测试
2. ✅ 批准创建最终共识文档
3. ✅ 批准进入Step 4B模型扩展讨论

**Claude同意。**

---

## 产出物

**代码文件：**
- backend/apps/users/services/xg_user_sync.py（修改）
- backend/apps/users/tests/test_xg_user_sync.py（新建）

**讨论文档：**
- doc 98：实施审查请求
- doc 99：Codex审查响应（P1识别）
- doc 100：Claude同意修复
- doc 101：实施与测试请求
- doc 102：完成总结
- doc 103：Codex最终审查通过

**提交记录：**
- feat: Phase 4C Step 4A完成 - 同步计划服务+测试

---

## Step 4B前置条件

**Codex建议：** 优先决策User模型扩展策略

**待决策问题：**

**问题1：是否新增phone/email/department字段？**
- 选项A：扩展User模型，增加3个字段
- 选项B：不扩展，只更新name字段

**问题2：name字段是否允许API覆盖？**
- 当前：CSV主导核心字段（包括name）
- 学工API也返回name
- 需定义冲突优先级

**影响：**
- 选项A：Step 4B可实现完整API补充字段upsert
- 选项B：Step 4B受限，would_update实际无可写补充字段

---

## 下一步执行

**立即启动：** Step 4B前置讨论 - User模型扩展策略

**讨论范围：**
1. 评估phone/email/department字段业务价值
2. 分析migration影响和风险
3. 定义CSV与API数据源冲突优先级
4. 决策选项A或B

**预计时间：** 讨论20-30分钟 + 实现（如选项A）40-60分钟

---

## 执行授权

✅ Codex与Claude已达成完整共识  
✅ Step 4A验收通过  
✅ 无遗留问题  
✅ 用户授权自主执行  

**立即进入Step 4B前置讨论。**
