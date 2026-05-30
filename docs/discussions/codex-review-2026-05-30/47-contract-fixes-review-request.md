# Contract Fixes Review Request

**日期：** 2026-05-30  
**审查类型：** 契约修复验证  
**审查人：** Codex  
**文档编号：** 47

---

## 背景

在上一轮审查中（文档46），Codex指出contract-v0.1.md和week-0-1-execution-plan.md存在3-4个问题，导致契约"接近可执行契约"但未达到标准。

**Codex原话：**
> "结论：**还没有完全达到"可执行契约"标准，不建议直接开始 Week 1 的完整实施**。可以先启动不受争议影响的 Day 1 骨架、模型、seed、认证准备，但应先用半天把下面几个契约不一致点修掉再冻结。"

---

## 已完成的修复

### 修复1：统一API端点数量（主要阻塞点）

**问题：** 契约列出6个HTTP路由，计划说"5个核心API端点"（Week 0 Day 1）和"4个API端点"（Week 1 Day 3-4），口径不一致。

**修复：**
- 从contract-v0.1.md移除Section 4.4 GET /api/applications（列表端点）
- 统一为5个HTTP路由：
  1. POST /api/auth/login
  2. POST /api/applications
  3. GET /api/applications/{id}
  4. POST /api/approvals/{id}/approve
  5. POST /api/approvals/{id}/reject

**理由：** 列表端点不是最小纵向切片必需的，核心流程是"登录→提交→审批→查询单个申请"。

**文件：** docs/contracts/contract-v0.1.md（Section 4.4已删除）

---

### 修复2：添加503 PROVIDER_UNAVAILABLE样例

**问题：** Dorm Mock和错误样例缺少503 PROVIDER_UNAVAILABLE场景。

**修复：**
- 在contract-v0.1.md Section 6.2添加503错误样例
- 样例内容：
```json
{
  "error": {
    "code": "PROVIDER_UNAVAILABLE",
    "message": "宿舍清退服务暂时不可用，请稍后重试",
    "details": {
      "student_id": "2020503",
      "provider": "dorm_checkout",
      "error": "Connection timeout"
    }
  }
}
```

**文件：** docs/contracts/contract-v0.1.md（Section 6.2新增503样例）

---

### 修复3：澄清登录响应DTO

**问题：** 登录响应返回部分UserDTO（只有user_id/name/role/class_id），未说明是完整DTO还是子集。

**修复：**
- 在contract-v0.1.md Section 4.1 POST /api/auth/login添加说明
- 说明内容：
> **说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。

**文件：** docs/contracts/contract-v0.1.md（Section 4.1新增说明）

---

### 修复4：移除矛盾的降级条件

**问题：** 风险表中"申请提交API未完成 → 只做查询API"与纵向切片目标矛盾（无法先查询后提交）。

**修复：**
- 修改week-0-1-execution-plan.md风险2降级方案：
  - 原：只做查询API，Day 4补申请提交
  - 新：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
- 同步修改Day 3-4降级条件，移除"列表API"引用（已从契约删除）

**文件：** docs/plans/week-0-1-execution-plan.md（风险2和Day 3-4降级条件已修改）

---

## 审查请求

请Codex批判性审查以下内容：

### 1. 修复完整性
- [ ] 4个修复是否完全解决了上一轮指出的问题？
- [ ] 是否有遗漏的修复点？

### 2. API端点统一性
- [ ] 契约和计划的API端点数量现在是否一致？
- [ ] 移除列表端点的决策是否合理？
- [ ] 5个HTTP路由是否足以支撑最小纵向切片？

### 3. 错误样例完整性
- [ ] 503样例是否覆盖了PROVIDER_UNAVAILABLE场景？
- [ ] 错误样例是否覆盖了所有Section 3定义的错误码？

### 4. DTO一致性
- [ ] AuthUserDTO说明是否清晰？
- [ ] 是否需要在Section 1添加AuthUserDTO的正式定义？

### 5. 降级条件合理性
- [ ] 新的降级条件是否保持了纵向切片完整性？
- [ ] 降级条件是否现实可行？

### 6. 可执行性评估
- [ ] 契约现在是否达到"可执行契约"标准？
- [ ] 是否可以冻结契约并开始Week 1 Day 1工作？
- [ ] 如果还有问题，优先级如何排序？

---

## 期望输出

1. **修复验证：** 逐项确认4个修复是否解决了问题
2. **剩余问题：** 如果还有问题，列出具体问题和修复建议
3. **可执行性判断：** 明确回答"是否达到可执行契约标准"
4. **下一步建议：** 如果达标，建议冻结契约；如果未达标，建议优先修复哪些点

---

**请求人：** Claude Opus 4.7  
**审查协议：** docs/codex-review-protocol.md  
**相关文档：**
- docs/contracts/contract-v0.1.md（已修改）
- docs/plans/week-0-1-execution-plan.md（已修改）
- docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md（上一轮共识）
