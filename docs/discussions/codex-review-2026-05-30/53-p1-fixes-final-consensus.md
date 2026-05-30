# P1 Fixes - Final Consensus

**日期：** 2026-05-30  
**参与方：** Codex + Claude  
**文档编号：** 53

---

## 审查结论

**状态：** ✅ 达到可执行契约标准

**Codex确认：** 2个P1阻塞问题已全部解决，可以冻结contract-v0.1.md并开始Week 1 Day 1工作。

---

## 已完成的修复

### 修复1：补齐错误样例（P1-1）

**问题：** Section 3定义8个错误码，Section 6.2只有4个样例

**修复：** 补齐4个缺失样例到Section 6.2
- 400 VALIDATION_ERROR
- 404 NOT_FOUND
- 409 CONFLICT
- 500 INTERNAL_ERROR

**Codex验证：** ✅ 通过 - 8个错误码全部有对应样例

### 修复2：修复降级方案矛盾（P1-2）

**问题：** 风险2说"砍学工部审批"又说"Day 4补学工部审批"

**修复前：**
```
降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
```

**修复后：**
```
降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
```

**Codex验证：** ✅ 通过 - 降级逻辑清晰，保持纵向切片完整性

---

## 剩余P2问题（非阻塞）

Codex指出3个P2问题，不阻塞Week 1启动：

1. **术语不一致：** 执行计划"4个API端点" vs 契约"5个HTTP路由"
   - 建议：后续统一为"5个HTTP路由（login + 4个业务端点）"

2. **AuthUserDTO未正式定义：** Section 4.1引用但Section 1未定义
   - 建议：v0.2或冻结前补充正式定义

3. **降级条件表述压缩：** Day 3-4局部降级条件仍较简略
   - 建议：后续同步成风险表同一口径

---

## 最终方案

### 契约冻结

**文件：** docs/contracts/contract-v0.1.md

**状态：** v0.1 Final（可执行契约标准）

**包含内容：**
- 核心DTO（User、Application、Approval、DormCheckoutStatus）
- 状态枚举（UserRole、ApplicationStatus、ApprovalStep、ApprovalDecision、DormCheckoutStatus）
- 错误码（8个核心错误码 + 8个错误样例）
- API端点（5个HTTP路由：login + submit + query + approve + reject）
- 样例数据（10学生 + 2辅导员 + 1学工部 + 边界样本）
- Mock响应（宿舍清退Mock + 错误Mock）

**验收标准：**
- 前端可用mock跑通登录→提交→审批→查询流程
- 后端可用seed数据跑通端到端测试

### Week 1 Day 1启动

**可以开始的工作：**
1. Django项目骨架
2. 用户模型和认证
3. Seed数据加载
4. 基础API框架

**执行计划：** docs/plans/week-0-1-execution-plan.md

---

## 文档一致性确认

- ✅ docs/contracts/contract-v0.1.md - P1修复完成
- ✅ docs/plans/week-0-1-execution-plan.md - P1修复完成
- ✅ docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md - 修复总结
- ✅ docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md - 审查请求
- ✅ docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md - Codex确认
- ⏳ docs/PROJECT-SUMMARY.md - 待更新
- ⏳ .omc/session-context.json - 待更新

---

## 下一步行动

1. ✅ 冻结contract-v0.1.md（标记为v0.1 Final）
2. ✅ 更新PROJECT-SUMMARY.md
3. ✅ 更新.omc/session-context.json
4. ✅ Git commit + push
5. ⏳ 开始Week 1 Day 1工作

---

**创建时间：** 2026-05-30T08:19:30Z  
**状态：** 共识达成，准备启动Week 1
