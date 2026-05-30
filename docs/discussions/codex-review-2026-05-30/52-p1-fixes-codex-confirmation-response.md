# P1 Fixes - Codex Confirmation Response

**审查日期：** 2026-05-30
**审查人：** Codex
**针对文档：** 51-p1-fixes-confirmation-request.md
**审查类型：** P1修复确认

---

## 审查结论

**可执行契约标准：** 是

**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。

**结论：** 可以冻结 `docs/contracts/contract-v0.1.md` 为 v0.1 Final，并开始 Week 1 Day 1 工作。

---

## P1修复验证

### 修复1：错误样例补齐

**验证结果：通过**

`docs/contracts/contract-v0.1.md` Section 3定义的8个错误码为：

1. `VALIDATION_ERROR` - 400
2. `AUTH_REQUIRED` - 401
3. `FORBIDDEN` - 403
4. `NOT_FOUND` - 404
5. `CONFLICT` - 409
6. `DORM_BLOCKED` - 422
7. `PROVIDER_UNAVAILABLE` - 503
8. `INTERNAL_ERROR` - 500

Section 6.2现在逐一提供了对应样例：

| HTTP状态 | 错误码 | 样例位置 | 结论 |
|---------|--------|----------|------|
| 400 | `VALIDATION_ERROR` | Section 6.2 | 通过 |
| 401 | `AUTH_REQUIRED` | Section 6.2 | 通过 |
| 403 | `FORBIDDEN` | Section 6.2 | 通过 |
| 404 | `NOT_FOUND` | Section 6.2 | 通过 |
| 409 | `CONFLICT` | Section 6.2 | 通过 |
| 422 | `DORM_BLOCKED` | Section 6.2 | 通过 |
| 500 | `INTERNAL_ERROR` | Section 6.2 | 通过 |
| 503 | `PROVIDER_UNAVAILABLE` | Section 6.2 | 通过 |

样例格式均采用统一的：

```json
{
  "error": {
    "code": "...",
    "message": "...",
    "details": {}
  }
}
```

其中401和403省略 `details`，这对v0.1可接受；如果后续要生成严格schema，可在v0.2明确 `details` 为可选字段。

### 修复2：降级方案修正

**验证结果：通过**

风险2当前表述为：

```text
如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
```

该表述已经满足可执行降级逻辑：

1. 触发点明确：Day 3结束，申请提交API仍未完成或不稳定。
2. 砍范围明确：砍学工部审批。
3. Day 4目标明确：集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环。
4. 顺延范围明确：学工部审批推到Week 2 Day 1。

这保留了纵向切片的最小业务闭环，没有退化成孤立查询接口，也没有继续承诺同一天补回被砍范围。

---

## 剩余问题

### P0/P1问题

无。

当前没有继续阻塞契约冻结或Week 1 Day 1启动的问题。

### P2问题

1. `week-0-1-execution-plan.md` 仍有“4个API端点可用”的表述，和契约“5个HTTP路由”容易产生术语混淆。建议后续改为“4个业务HTTP路由可用，不含Day 1-2登录路由”，或在Week 1验收处统一写“5个HTTP路由覆盖4个核心能力”。
2. `AuthUserDTO` 仍未在Section 1正式定义。Section 4.1已有解释，对v0.1实现不构成阻塞；建议v0.2或冻结前顺手补充正式DTO定义。
3. Day 3-4局部降级条件中“如Day 3结束申请提交API未完成 -> 保留最短闭环”的一句仍较压缩。风险表已给出清晰版本，因此不再构成P1；建议后续同步成同一口径，减少计划文档内重复表达的维护成本。

---

## 建议

1. 冻结 `docs/contracts/contract-v0.1.md` 为 v0.1 Final。
2. 开始 Week 1 Day 1 工作：Django项目骨架、用户模型和认证、Seed数据加载、基础API框架。
3. 将上述P2作为非阻塞清理项处理，不应继续阻塞Week 1启动。

