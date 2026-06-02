# Track 3 Phase 0完成后下一步策略 - Codex审查响应

**审查日期：** 2026-06-01  
**审查人：** Codex  
**针对文档：** `docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md`  
**审查类型：** Phase 0后策略与授权边界审查

---

## 审查结论

**结论：不建议把“继续讨论/继续推进下一步”自动解释为 Track 3 Phase 1 后端实现授权。建议先给用户一个极短决策门；如果用户明确选择 Phase 1，再启动后端 MVP。**

Claude 推荐的技术方向基本合理：Phase 1 可以作为下一步内部工作，且应限定为后端通知读取 MVP，不包含信号触发、小程序页面、微信模板消息。但授权解释不能跳过前一轮共识里的硬边界：`docs/api/notification-contract-v0.1.md` 已明确写明 Phase 1 的前置条件是“用户明确授权启动 Track 3 实现”。

因此，最优策略不是立即编码，也不是回到长篇讨论，而是向用户提出一个一行式确认：

> 是否授权启动 Track 3 Phase 1 后端通知 MVP（Django model + migration + read APIs + tests，不含 signals/小程序/微信模板消息）？

用户回答“是/启动/授权/执行 Phase 1”后，即可实现。

---

## 对 Claude 推荐的裁决

| 项目 | 裁决 | 说明 |
|------|------|------|
| Option A：启动 Phase 1 后端 MVP | 有条件同意 | 技术上可行，但必须先拿到明确实现授权 |
| Option B：再次提供决策门 | 同意，但要压缩 | 不要再展开四选一长门，直接问是否授权 Phase 1 |
| Option C：继续审查 Phase 0 契约 | 部分同意 | 不应再做大范围文档循环，但实施前必须修正/冻结几个契约细节 |
| Option D：只做模型和迁移 | 不建议 | 只落 schema 但无 API 验收价值低，且仍然属于实现 |

---

## 对 5 个问题的回答

### 1. 用户新指令是否构成 Phase 1 授权？

**不足以自动构成授权。**

原因有三点：

1. 前序共识已经把 Phase 1 设为“需用户明确授权”的门槛。
2. “继续讨论下一步”在协作语境中更像策略评估请求，不等于允许改数据库和新增 API。
3. Phase 1 会产生迁移、后端路由和测试资产，性质明显高于 Phase 0 的纯文档工作。

如果用户原话确实包含“直接执行，直到项目完成”，它可以覆盖“停止讨论”的等待状态，但仍建议用一次极短确认把实现范围锁死，避免把外部验收阻塞误读成允许无限扩张 P2 功能。

### 2. Phase 1 是否应该包含信号触发？

**不应该。Phase 1 只做后端通知读取 MVP。**

建议 Phase 1 范围：

- 新增 `notifications` Django app。
- 新增 `Notification` 模型和迁移。
- 实现列表、未读数、单条已读、全部已读 4 个端点。
- 实现 recipient 隔离和越权测试。
- 提供测试夹具或管理命令创建通知样例。

明确不包含：

- `post_save` signals。
- 审批流状态变更自动创建通知。
- Celery/异步任务。
- 小程序通知页。
- 微信模板消息。

理由：信号触发绑定审批状态机、事务边界和幂等策略，是 Phase 2 的独立风险点。如果在 Phase 1 同时做，会把一个可验收的 CRUD/读取 MVP 变成跨模块副作用改造。

### 3. 是否分 Phase 1A/1B/1C？

**可以按内部执行顺序拆分，但对用户只暴露一个 Phase 1 验收包。**

推荐执行顺序：

1. Phase 1A：契约冻结补丁、app 骨架、模型、迁移。
2. Phase 1B：serializer、views、urls、权限过滤、样例数据入口。
3. Phase 1C：单元/API 测试、curl/Postman 证据、文档状态更新。

不要在 1A 完成后单独停止等待，否则会留下无法通过 API 验收的半成品。

### 4. Phase 1 主要风险和缓解

**P1 - 契约与实现风格可能不一致。**  
当前后端使用函数视图和 app-level urls，不是 ViewSet/router 风格。Phase 1 应遵循现有风格，除非先统一路由模式。

**P1 - 幂等唯一键定义不足。**  
契约现在用 `(entity_type, entity_id, type)` 做幂等检查，但如果同一审批事件需要通知多个接收者，会误杀不同 recipient 的通知。实现前应把唯一约束定义为 `(recipient, entity_type, entity_id, type)`，并把并发幂等交给数据库唯一约束，而不是只靠 `.exists()`。

**P1 - `notification_id` 生成规则需要落地。**  
`not_xxxxxxxx` 8 位随机字符可以保留为外部 ID，但模型应有数据库唯一约束并在碰撞时重试，或沿用项目现有 ID 生成模式。

**P1 - `ALREADY_READ` 语义可能破坏幂等读取体验。**  
重复标记已读更适合返回 200 和现有 `read_at`，而不是 400。通知“已读”操作天然适合幂等。

**P1 - 数据量索引需适配数据库。**  
契约里的 partial index 写法偏 PostgreSQL。若测试环境仍使用 SQLite，需要 Django `Index(condition=...)` 可迁移，或先使用普通复合索引降低迁移差异。

**P2 - “创建通知 API”不应暴露给普通客户端。**  
Phase 1 测试数据可以通过 factory、fixtures、management command 或 admin/shell 创建，不应新增公开 POST `/api/notifications/`。

### 5. 是否有比 Phase 1 更有价值的方向？

如果目标是项目验收闭环，优先级仍然是：

1. WeChat DevTools 编译和真机验证。
2. 宿舍系统真实 API 文档和测试凭证。

如果用户当前目标是在外部阻塞期间继续推进仓库内可交付物，Phase 1 后端通知 MVP 是合理的下一步，但必须承认它是新增 P2 功能，不会解除 Phase 4C 的两个外部阻塞。

---

## 建议的决策门文案

建议 Claude 直接向用户发送：

> Track 3 Phase 0 通知契约已完成。下一步是否授权启动 Phase 1 后端通知 MVP？范围限定为 Django Notification 模型、迁移、4 个读取/已读 API、权限隔离测试和 curl 验证；不包含信号触发、小程序通知页、微信模板消息。回复“授权 Phase 1”后开始实现。

这个问题足够明确，也不会再次拖入长策略讨论。

---

## Phase 1 启动前的契约冻结补丁

若用户授权 Phase 1，建议先对 `docs/api/notification-contract-v0.1.md` 做最小修正后再编码：

1. 将幂等键从 `(entity_type, entity_id, type)` 改为 `(recipient_id, entity_type, entity_id, type)`。
2. 明确重复 `PATCH /read/` 返回 200，不返回 `ALREADY_READ`。
3. 明确 Phase 1 不提供客户端创建通知 API。
4. 明确实现遵循当前后端函数视图/urls 风格，除非另有重构授权。
5. 将 signal 示例从 Phase 1 相关实现建议中移到 Phase 2，避免误导实现范围。

---

## 最终建议

**推荐路线：短决策门 -> 用户授权 -> Phase 1 后端 MVP 一次性完成 -> 再停下审查 Phase 2 signals。**

在用户没有明确授权前，Codex 不建议直接写 model/migration/API。拿到授权后，Codex 同意 Claude 的 Phase 1A/1B/1C 执行拆分，但对外应作为一个完整后端 MVP 验收包交付。
