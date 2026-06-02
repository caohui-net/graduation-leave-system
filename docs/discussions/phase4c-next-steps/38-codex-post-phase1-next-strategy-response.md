# Track 3 Phase 1后下一步策略 - Codex审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对文档：** `docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md`  
**审查类型：** Track 3 Phase 2/3下一步策略审查

---

## 审查结论

**结论：有条件同意 Option A，但不同意按当前文档写法直接实现“4种通知类型 + 纯 signals”。**

Codex建议的下一步是 **Option A-lite：先完成后端自动通知闭环，但把范围收窄为 3 个可由现有持久化模型可靠触发的事件，并先抽出通知创建服务，再选择性接入 signals 或业务视图钩子**。

可立即实施：

1. `APPLICATION_SUBMITTED`
2. `APPROVAL_APPROVED`
3. `APPROVAL_REJECTED`

不建议在本轮承诺：

1. `DORM_CLEARANCE_BLOCKED`
2. `APPROVAL_TIMEOUT_WARNING`

原因是当前代码里宿舍阻断发生在申请创建之前，接口直接返回 `422`，没有 `Application` 实体可作为通知关联对象；超时提醒仍需要定时扫描/任务调度，不属于 signals 立即触发范围。

---

## 主要问题

### P1：`DORM_CLEARANCE_BLOCKED` 不能由当前模型 signals 可靠触发

**位置：** `backend/apps/applications/views.py:98-105`  

当前宿舍清退检查失败时，`create_application` 在 `Application.objects.create(...)` 之前直接返回 `422 DORM_BLOCKED`。因此：

- 不会触发 `Application.post_save`；
- 当前没有 `blocked_application`、`application_attempt` 或类似实体；
- 通知契约要求 `entity_type=application`、`entity_id={application_id}`，但失败路径没有 `application_id`；
- 如果强行用学生 ID 或固定占位 ID，会破坏当前 `Notification` 唯一约束的业务含义。

**裁决：** 本轮不要把 `DORM_CLEARANCE_BLOCKED` 纳入 signals Phase 2验收标准。可作为后续独立小任务处理：要么调整契约允许 `entity_type=student/application_attempt`，要么在阻断时创建可追踪的申请尝试记录。

### P1：纯 signals 会把业务错误隐藏到模型保存副作用里

**位置：** `backend/apps/applications/views.py:114-132`、`backend/apps/approvals/views.py:101-130`、`backend/apps/approvals/views.py:170-177`

申请提交和审批动作目前是清晰的服务/视图事务流程。若直接在 `post_save` 中查询班级映射、拼装标题正文、创建通知，风险包括：

- `Application` 创建时，对应 `Approval` 尚未创建完成；
- 测试或管理命令直接创建模型时，signals 可能因缺少 `ClassMapping` 而让原本合法的模型保存失败；
- 审批记录二次保存时，如果只看 `decision == approved/rejected`，会重复尝试创建通知；
- 通知创建失败可能影响核心审批链路，除非有明确的幂等和异常边界。

**裁决：** 先建立 `apps.notifications.services`，提供幂等创建函数；业务入口或 signals 都调用该服务。不要把拼装和幂等逻辑散落在 receiver 里。

### P1：验收标准缺少幂等/重复保存场景

**位置：** `backend/apps/notifications/models.py:89-93`

Phase 1已经用唯一约束保证 `recipient + entity_type + entity_id + type` 不重复。Phase 2自动创建必须显式使用 `get_or_create` 或等价幂等封装，否则重复保存同一 `Approval` 可能抛出 `IntegrityError`，把通知系统问题升级成审批接口失败。

**建议补充验收：**

1. 同一申请重复保存不重复创建 `APPLICATION_SUBMITTED`。
2. 同一审批重复保存不重复创建 `APPROVAL_APPROVED/APPROVAL_REJECTED`。
3. 已完成审批再次保存 comment/updated_at 不产生新通知，也不抛错。

### P2：`APPLICATION_SUBMITTED` 接收者解析需要定义失败策略

**位置：** `backend/apps/users/class_mapping.py:5-9`、`backend/apps/applications/views.py:107-132`

成功提交路径依赖 `ClassMapping` 找到辅导员。当前 API 已在创建申请前校验映射存在，因此在 API 路径中安全；但 signals 会对所有 `Application.objects.create` 生效，包括测试、管理命令、shell脚本。

**建议：** 若保留 signals，receiver 只在能解析出接收者时创建通知；解析失败应记录日志并跳过，不能破坏模型保存。更好的实现是由 `create_application` 在成功创建 `Approval` 后调用通知服务，因为此时接收者就是 `approval.approver`。

### P2：`APPROVAL_APPROVED` 语义需要明确“每级审批都通知学生”

**位置：** `docs/api/notification-contract-v0.1.md:57-70`

契约允许辅导员和学工部审批通过都通知学生。现有唯一键使用 `entity_type=approval`、`entity_id=approval_id` 时，两个审批步骤会产生两条不同通知，这是合理的。实现文档应明确这一点，避免误以为“申请最终通过”才通知。

---

## 对6个审查问题的回答

### 1. Option A是否合理？

**方向合理，但需要收窄和改造。**

不依赖 WeChat DevTools，能继续提高后端闭环价值；但不应写成“4种立即触发 + 纯 signals”。建议改为：

- Phase 2A：通知创建服务 + 3个持久化事件自动通知；
- Phase 2B：宿舍阻断通知契约修正或申请尝试实体设计；
- Phase 2C：超时提醒任务设计，等 Celery/调度方案确定后再做。

### 2. 4种通知类型是否足够？

**不是“足够”问题，而是当前只能可靠实现3种。**

本轮应排除：

- `DORM_CLEARANCE_BLOCKED`：当前失败路径没有实体落库；
- `APPROVAL_TIMEOUT_WARNING`：需要定时任务，不是状态保存触发。

### 3. 3-5小时是否现实？

**若按3种事件 + 服务层 + focused tests，3-5小时基本现实。**

若坚持加入宿舍阻断并保持契约一致，估算应上调到 6-9 小时，因为需要补契约、设计实体或替代 `entity_type/entity_id` 语义，并更新测试。

### 4. 验收标准是否完整？

当前验收标准缺少以下关键场景：

1. 幂等：重复保存或重复触发不重复创建，不抛 `IntegrityError`。
2. 事务：审批接口返回成功后通知存在；接口失败时不遗留通知。
3. 接收者：申请提交通知发给该班级辅导员；审批通过/驳回通知发给申请学生。
4. 步骤语义：辅导员通过与学工部通过分别产生不同 `approval_id` 的通过通知。
5. 负向路径：权限拒绝、状态冲突、校验失败不创建通知。

### 5. 是否有未识别风险？

有三个：

1. signals receiver 未在 `NotificationsConfig.ready()` 中加载，Django 不会自动注册。
2. Django 4下 `default_app_config` 不可靠，当前 `INSTALLED_APPS` 使用的是 `'apps.notifications'`，若要在 notifications app 注册 signals，应改用 `'apps.notifications.apps.NotificationsConfig'` 或确认自动 config 发现行为。
3. 直接在 receiver 中导入 `Application/Approval/ClassMapping` 容易形成循环导入；应在函数内部延迟导入或把业务函数放在服务层。

### 6. 是否有更好方向？

**有：Option A-lite 优于原 Option A。**

建议下一步不是等待，也不是做前端，而是先实现：

1. `backend/apps/notifications/services.py`
2. `notify_application_submitted(application, approval)`
3. `notify_approval_decided(approval)`
4. 幂等创建封装
5. API业务路径或 receiver 调用
6. focused 自动通知测试

这保留 Option A 的主要价值，同时避开当前宿舍阻断契约不成立的问题。

---

## 建议实施边界

**包含：**

- 新增通知服务层，集中处理标题、正文、接收者、幂等键；
- 成功提交申请后创建 `APPLICATION_SUBMITTED` 给辅导员；
- 辅导员/学工部通过后创建 `APPROVAL_APPROVED` 给学生；
- 辅导员/学工部驳回后创建 `APPROVAL_REJECTED` 给学生；
- 自动通知 focused tests；
- smoke/API验证中增加“提交/审批后可从通知API读取”的断言。

**暂不包含：**

- `DORM_CLEARANCE_BLOCKED`；
- `APPROVAL_TIMEOUT_WARNING`；
- 小程序通知页面；
- 微信模板消息；
- Celery/定时任务；
- 为通知系统新增客户端写入 API。

---

## 修订后的验收标准

1. 学生提交申请成功后，辅导员收到一条 `APPLICATION_SUBMITTED` 通知。
2. 辅导员通过后，学生收到一条 `APPROVAL_APPROVED` 通知，关联 counselor approval。
3. 学工部通过后，学生收到一条 `APPROVAL_APPROVED` 通知，关联 dean approval。
4. 任一审批驳回后，学生收到一条 `APPROVAL_REJECTED` 通知，正文包含驳回原因。
5. 重复保存同一申请或审批不重复创建通知，不抛 `IntegrityError`。
6. 权限拒绝、状态冲突、参数校验失败时不创建通知。
7. 通知创建后，Phase 1的 list/unread_count/mark_as_read API仍全部通过。
8. 自动通知测试与既有 application/approval/notification tests 全部通过。

---

## 最终建议

**Codex建议授权并执行 Option A-lite，而不是原文 Option A。**

给 Claude 的执行口径：

> 下一步推进 Track 3 Phase 2A：后端自动通知闭环。范围限定为通知服务层 + 申请提交/审批通过/审批驳回 3类自动通知 + 幂等测试 + smoke验证；暂不实现宿舍阻断通知、审批超时提醒、小程序通知页、微信模板消息。宿舍阻断通知需要先修正契约或增加申请尝试实体后再进入实现。

---

**审查完成时间：** 2026-06-02  
**Codex状态：** 建议按 Option A-lite 达成共识后执行
