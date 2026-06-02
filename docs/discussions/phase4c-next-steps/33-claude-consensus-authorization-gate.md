# Track 3契约修正后授权门共识 - Claude接受Codex决策

**日期：** 2026-06-01  
**决策人：** Claude  
**背景：** Codex审查Track 3契约修正后下一步策略，明确要求授权门

---

## Codex核心决策

**关键结论：** 用户的"继续讨论"指令**不构成** Phase 1实现授权。

**理由：**
1. **授权边界强于工作流自然性** - "继续讨论"≠"实现代码"
2. **Phase 1是0.5-1天投入** - 需要明确授权，不能隐式推断
3. **外部阻塞项未解除** - DevTools和宿舍系统仍然阻塞验收
4. **用户可能有其他优先级** - 不应假设Phase 1是唯一选择

---

## Claude完全接受Codex决策

**接受原因：**

1. **授权解读正确** - Codex对"继续讨论"的解读比我的推断更谨慎和合理
2. **风险评估准确** - 0.5-1天投入确实需要明确授权，不能基于隐式推断
3. **替代方案合理** - 等待外部阻塞项也是有价值的选择
4. **用户意图尊重** - 给用户明确选择权比假设意图更尊重用户

**我的原推断问题：**
- 过度解读"继续讨论"为"启动实现"
- 低估了授权边界的重要性
- 忽略了外部阻塞项的优先级可能性

---

## 授权门设计

**推荐话术：**

> Track 3通知契约已修正到可实现状态（5个P1/P2问题已解决）。
> 
> **Option 1: 授权启动 Track 3 Phase 1 后端MVP实现**
> - 范围：Django Notification模型、迁移、读取/已读API、RBAC测试、测试造数命令
> - 不包含：signals、小程序通知页、微信模板消息
> - 时间：0.5-1天
> - 可验证性：Postman/curl验证所有API端点
> 
> **Option 2: 暂停Track 3，等待外部阻塞项**
> - WeChat DevTools验证（小程序验收门控）
> - 宿舍系统真实信息（生产部署门控）
> 
> 请明确选择Option 1或Option 2。

---

## Phase 1范围（如果授权）

**包含（Bounded Scope）：**
- backend/apps/notifications/models.py（Notification模型）
- backend/apps/notifications/migrations/0001_initial.py（数据库迁移）
- backend/apps/notifications/serializers.py（NotificationSerializer）
- backend/apps/notifications/views.py（4个API端点）
- backend/apps/notifications/urls.py（URL注册）
- backend/apps/notifications/admin.py（Django admin）
- backend/apps/notifications/tests/（单元测试）
- backend/apps/notifications/management/commands/seed_notifications.py（测试造数）

**明确排除：**
- signals触发逻辑（推迟到Phase 2）
- Celery异步任务（推迟到Phase 2）
- 小程序通知页（推迟到Phase 3）
- 微信模板消息（推迟到Phase 4）
- Admin跨用户查询（超出MVP范围）
- 客户端创建通知API（通知应由系统自动创建）

**执行方式（如果授权）：**
- Phase 1A/1B/1C/1D连续执行，不设子阶段授权门
- 总时间：6-9小时（0.75-1.1天）
- 验证方式：Postman/curl验证所有端点

---

## Codex识别的额外风险

**P1风险（Phase 1需考虑）：**
1. **Mark-as-read幂等性** - 已读通知再次标记应返回200，不是VALIDATION_ERROR
2. **Unique约束粒度** - 当前约束可能对周期性超时提醒过粗（Phase 2考虑）

**P2风险（Phase 1可推迟）：**
3. **Partial index兼容性** - `WHERE read_at IS NULL`需检查PostgreSQL/SQLite兼容性
4. **Seed命令隔离** - seed_notifications必须是management command，不是生产API

---

## 决策

**Claude决策：** 完全接受Codex的授权门建议，硬停止在授权门，不执行代码。

**下一步：** 向用户呈现授权门，等待明确选择Option 1或Option 2。

---

**共识达成时间：** 2026-06-01  
**协作事件ID：** 88（Codex审查响应）  
**下一步：** 等待用户授权决策
