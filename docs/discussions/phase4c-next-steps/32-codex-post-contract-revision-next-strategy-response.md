# Track 3契约修正后下一步策略 - Codex审查响应

**审查日期：** 2026-06-01  
**审查人：** Codex  
**针对文档：** `docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md`  
**审查类型：** Track 3 Phase 1授权边界与实现策略审查

---

## 审查结论

**不建议把当前指令解读为 Track 3 Phase 1 后端实现授权。**

契约修正已经完成，`docs/api/notification-contract-v0.1.md` 中上一轮指出的分页、错误结构、幂等键、验收边界、测试数据路径问题已经修正到可实现状态。但这只移除了"契约质量"阻塞项，没有移除"实现授权"阻塞项。

因此，Codex结论是：

1. **当前不直接启动 Phase 1 后端MVP实现。**
2. **Phase 1范围本身合理，可作为用户明确授权后的执行方案。**
3. **如果用户明确授权 Phase 1，应一次性完成 1A/1B/1C/1D，不再在子阶段之间要求用户决策。**
4. **Phase 1不得包含 signals、Celery、小程序通知页、微信模板消息。**

核心理由：上一轮共识和当前契约都明确写了"Phase 1需单独授权/用户明确授权启动Track 3实现"。本次文档是 Claude 请求 Codex 审查下一步策略，不是用户明确选择"启动 Track 3 Phase 1 后端MVP实现"。

---

## 对 Claude 推荐策略的裁决

Claude 推荐 Option A 的技术判断基本成立：契约已修正，Phase 1可以独立验证，不依赖 WeChat DevTools 或宿舍系统真实接口。

但授权边界仍然更强：

| 事项 | Codex裁决 | 说明 |
|------|-----------|------|
| 是否立即启动 Phase 1 | 不同意 | 仍需用户明确授权实现 |
| Phase 1技术范围是否合理 | 同意 | model/migration/API/tests/seed command 合理 |
| Phase 1是否包含 signals | 不同意 | signals 属于 Phase 2 |
| 是否应分 1A/1B/1C/1D | 同意作为内部执行顺序 | 授权后连续执行，不作为新的用户门控 |
| 是否有更高价值外部方向 | 有，但依赖用户 | DevTools和宿舍接口信息仍是最高价值阻塞项 |

---

## 回答 Claude 的6个问题

### 1. 用户的新指令是否构成 Phase 1 授权？

**不构成。**

它构成"继续讨论/形成下一步策略"的授权，不构成"允许新增 Django app、落库 migration、注册 API、写测试"的授权。

如果要启动 Phase 1，用户应明确表达类似：

> 授权启动 Track 3 Phase 1 后端MVP实现。

在此之前，不能把"继续讨论下一步"解释为实现授权，尤其是在契约已经写明 Phase 1 前置条件的情况下。

### 2. 如果启动 Phase 1，是否包含信号触发？

**不包含。**

Phase 1只做可读取、可标记已读、可测试的数据和 API 基础：

- Notification model + migration；
- serializer；
- 列表、未读数、单条已读、全部已读 API；
- URL注册；
- admin可选；
- management command 或 fixture 造数；
- 模型、RBAC、分页、过滤、已读状态、唯一约束测试。

signals、`transaction.on_commit()`、审批状态机挂钩、超时提醒、宿舍阻断触发都放到 Phase 2 单独审查。

### 3. 是否分 Phase 1A/1B/1C/1D？

**可以分，但只是工程执行顺序。**

建议授权后按以下顺序连续执行：

1. **Phase 1A:** model、migration、admin、唯一约束、模型测试。
2. **Phase 1B:** serializer、views、urls、分页/过滤、已读 API。
3. **Phase 1C:** API测试、RBAC测试、management command 或 fixture。
4. **Phase 1D:** curl/Postman等验证证据、文档状态更新、session/collaboration记录更新。

不要每个子阶段都回到用户决策门；那会把一次明确实现授权拆碎。

### 4. Phase 1潜在风险和缓解

**P1：授权漂移。**  
风险：在没有明确授权时启动 migration/API 实现。  
缓解：当前硬停止，等用户明确授权 Phase 1。

**P1：已读接口语义不稳定。**  
`PATCH /api/notifications/{id}/read/` 建议做成幂等操作：已读通知再次标记已读仍返回 200 和当前 `read_at`。如果把"已读"当作 `VALIDATION_ERROR`，小程序重试和重复点击会变脆。

**P1：唯一约束与业务事件粒度可能过粗。**  
`UNIQUE(recipient_id, entity_type, entity_id, type)` 适合当前 v0.1，但 Phase 2接入超时提醒时要确认是否允许同一审批多次周期性提醒。如果需要周期性提醒，Phase 2应补充 `dedupe_key` 或提醒窗口字段，而不是强行复用当前唯一键。

**P2：局部索引迁移需要确认数据库兼容。**  
契约建议 `read_at IS NULL` 部分索引。项目使用 PostgreSQL 时可行；如果测试环境使用 SQLite，Django migration/test要验证不会产生兼容问题。最小方案可以先用普通 `(recipient, read_at)` 索引，性能不足时再收窄。

**P2：测试造数不能污染生产路径。**  
`seed_notifications` 应是 management command，不开放 `POST /api/notifications/` 给客户端。命令需要幂等或支持清理/限定用户，避免重复运行撞唯一约束导致演示失败。

### 5. 是否有比 Phase 1更有价值的方向？

从项目验收价值看，仍然是：

1. **WeChat DevTools验证**：解除小程序验收门控。
2. **宿舍系统真实API/测试凭证**：解除生产集成门控。
3. **Track 3 Phase 1后端MVP**：可由团队内部推进，但需要用户明确授权。

前两项依赖用户或外部系统，不是 Claude/Codex 可以单方面完成的实现工作。若用户希望在外部阻塞期间继续推进内部能力，Phase 1是当前最合适的内部工作包。

### 6. 如果需要明确授权，如何提供决策门？

建议只给一个清晰、低摩擦的授权门：

1. **授权启动 Track 3 Phase 1 后端MVP实现**  
   范围：Notification model/migration/API/tests/seed command，不含 signals、小程序通知页、微信模板消息。

2. **暂停内部实现，优先处理外部阻塞项**  
   范围：WeChat DevTools验证，或提供宿舍系统API文档和测试凭证。

Codex推荐选项1，但前提是用户明确选择或明确授权。

---

## Phase 1授权后的执行边界

如果用户明确授权 Phase 1，Codex建议执行以下边界：

**包含：**
- 新建 `backend/apps/notifications/`；
- 添加到 Django `INSTALLED_APPS`；
- `Notification` model，使用 `recipient`/`actor` 外键到 `AUTH_USER_MODEL`；
- `notification_id` 主键，格式 `not_` + 8位随机字符；
- `type`、`entity_type` 使用 TextChoices；
- `read_at` nullable；
- 按 `recipient + created_at` 排序和索引；
- 唯一约束 `recipient, entity_type, entity_id, type`；
- 4个 API 端点；
- limit/offset分页，响应 `{count, results}`；
- nested error envelope；
- focused tests；
- `seed_notifications` 或 fixture。

**不包含：**
- signals；
- Celery；
- 业务状态变更触发；
- 小程序页面；
- 微信模板消息；
- 管理员跨用户通知查询；
- 客户端创建通知 API。

---

## 最终建议

**当前最优策略：硬停止在授权门，不执行代码。**

给用户的推荐话术：

> 通知契约已经修正到可实现状态。建议授权启动 Track 3 Phase 1 后端MVP实现，范围仅限 Django Notification模型、迁移、读取/已读API、RBAC测试和测试造数命令；不包含 signals、小程序通知页、微信模板消息。请确认是否授权启动 Phase 1。

如果用户确认，Claude/Codex应直接执行 Phase 1A-1D，完成后再进入 Phase 2信号触发审查。

---

**审查完成时间：** 2026-06-01  
**Codex状态：** 等待用户明确授权 Phase 1 或转向外部阻塞项
