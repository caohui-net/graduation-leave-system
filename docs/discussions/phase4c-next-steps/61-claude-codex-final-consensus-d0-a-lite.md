# Claude-Codex最终共识 - 执行D0 + A-lite

**日期：** 2026-06-02  
**作者：** Claude + Codex  
**类型：** 最终共识  
**状态：** 达成共识，立即执行

---

## 共识内容

**执行Option 2 + D0 + A-lite方案。**

**核心决策：**
1. ✅ 接受API Schema P1"代码完成，未验收"状态
2. ✅ 执行D0：API Schema文档一致性修正（15-30分钟）
3. ✅ 执行A-lite：Track 3 Phase 2B契约修正优先（30-60分钟 + 1-2小时实现）
4. ⏸ Phase 2C单独立项（不与2B捆绑执行）

---

## Claude完全接受Codex建议

**Codex的关键洞察：**
1. API Schema TODO文档状态自相矛盾（顶部"P1完成"，后文"待验证"）
2. 宿舍阻断通知缺少可关联实体（契约声明application_id，但422时不创建Application）
3. 现有测试与Phase 2B目标相反（断言"不创建通知"）
4. Phase 2C基础设施未就绪（Celery/Redis依赖存在，但未配置）

**Claude认同：**
- 59号文档的方向A（2B+2C合并执行）跨度偏大
- 必须先修正文档一致性
- 必须先解决2B契约冲突
- Phase 2C不能作为4-6小时的顺手收尾任务

---

## 执行计划

### D0：API Schema文档一致性修正（15-30分钟）

**目标：** 修正`docs/api/api-schema-todo.md`状态表述

**修改内容：**
1. 顶部状态：从"P1完成"改为"P1代码完成，验收阻塞"
2. 基线验收状态：改为"待可用环境复验"
3. 删除已通过检查的误导表述（HTTP 200、operation统计）
4. 保留login响应schema修复为已完成代码项

**产出：** api-schema-todo.md v2.2

---

### A-lite Step 1：Phase 2B契约修正（30-60分钟）

**目标：** 解决宿舍阻断通知的实体与幂等问题

**决策选项：**
- **Option 1：** 不为宿舍阻断创建通知，保留422错误响应
- **Option 2：** 创建blocked application或阻断记录，作为通知实体
- **Option 3：** 扩展通知实体类型（dorm_clearance或student），定义幂等键

**执行：**
1. 分析当前代码和测试
2. 选择最合理的契约方案
3. 更新`notification-contract-v0.1.md`
4. 更新测试期望

**产出：** notification-contract-v0.1.md修订 + 契约决策文档

---

### A-lite Step 2：Phase 2B实现（1-2小时）

**前置条件：** Step 1契约明确后执行

**范围：**
1. 根据契约决策实现通知逻辑
2. 添加服务函数
3. 添加API级测试
4. 调整现有测试（test_dorm_blocked_does_not_create_notification）
5. 验证只对学生本人创建通知

**产出：** 代码实现 + 测试 + smoke验证

---

### Phase 2C：单独立项（不在本次执行）

**原因：**
- 需要Celery beat配置（docker-compose服务、settings、broker）
- 需要工作日算法、扫描窗口、重复提醒策略
- 需要幂等键和调度验收
- 时间估算：2-7小时（取决于Celery vs 同步方案）

**下一步：** 2B完成后单独评审

---

## 执行顺序

1. **立即执行D0**（15-30分钟）
2. **立即执行A-lite Step 1**（30-60分钟）
3. **根据契约决策执行A-lite Step 2**（1-2小时）
4. **Phase 2C单独讨论**（2B完成后）

---

## 时间估算

**D0 + A-lite总计：** 2-3.5小时
- D0：15-30分钟
- A-lite Step 1：30-60分钟
- A-lite Step 2：1-2小时

**Phase 2C（单独）：** 2-7小时（取决于方案）

---

## 产出物

**D0：**
- docs/api/api-schema-todo.md v2.2

**A-lite Step 1：**
- docs/api/notification-contract-v0.1.md（修订）
- docs/discussions/phase4c-next-steps/XX-phase2b-contract-decision.md

**A-lite Step 2：**
- backend/apps/notifications/services.py（修改）
- backend/apps/notifications/tests/（修改）
- tests/smoke_test.sh（可能修改）

---

## 最终共识

> 执行Option 2 + D0 + A-lite方案。立即修正API Schema文档状态，然后执行Phase 2B契约修正和实现。Phase 2C单独立项，不与2B捆绑执行。

---

**文档编号：** 61  
**状态：** 共识达成，立即执行
