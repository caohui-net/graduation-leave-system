# Phase 2B契约决策 - Codex审查响应

**日期：** 2026-06-02  
**审查人：** Codex  
**类型：** 契约决策审查响应  
**针对：** 62-phase2b-contract-decision-review-request.md

---

## 审查结论

**建议当前采用 Option 1：不为宿舍阻断创建通知，将 `DORM_CLEARANCE_BLOCKED` 从 v0.1 自动通知契约中删除或标记为 deferred。**

理由：当前宿舍阻断是申请提交接口的同步校验失败，而不是已创建业务实体上的状态变更。`create_application` 在宿舍未清退时直接返回 `422`，不会创建 `Application`；通知模型又要求幂等键绑定明确实体。因此在不新增实体的前提下创建通知，会破坏 `entity_id` 语义。

如果产品明确要求“通知中心可回看宿舍阻断原因”，再采用 Option 2 的独立 `DormClearanceBlock` / `DormBlockRecord` 表。不要优先使用 blocked application，也不建议使用 `student_id` 伪装业务事件实体。

---

## 发现的问题

### 问题1：当前不能按契约创建宿舍阻断通知 [P1]

**位置：**
- `docs/api/notification-contract-v0.1.md:89`
- `docs/api/notification-contract-v0.1.md:99`
- `backend/apps/applications/views.py:137`
- `backend/apps/applications/views.py:150`

契约要求 `DORM_CLEARANCE_BLOCKED` 关联 `application_id`，但代码在宿舍状态非 `completed` 时直接返回 `422`，`Application.objects.create(...)` 在后续分支才执行。也就是说阻断路径没有合法 `application_id`。

**建议：** v0.1中删除该自动通知承诺，或在事件表中标记为 deferred：当前仅通过 `POST /api/applications/` 的 `422 DORM_BLOCKED` 响应告知学生。

### 问题2：blocked application会污染申请状态机 [P1]

**位置：**
- `backend/apps/applications/models.py:6`
- `backend/apps/applications/models.py:21`
- `backend/apps/applications/views.py:118`

如果为阻断创建 `Application(status=blocked)`，需要重新定义列表展示、重复提交限制、审批流创建条件、可见性、统计口径和清退后重提行为。它不是单纯新增一个状态，会让“申请”同时表达“已提交审批对象”和“提交失败尝试”两种语义。

**建议：** 如果必须持久化阻断事件，优先新建独立表，不要把阻断塞进 `Application`。

### 问题3：使用 `student_id` 作为通知实体会让幂等语义过粗 [P1]

**位置：**
- `backend/apps/notifications/models.py:89`

当前唯一约束是 `(recipient, entity_type, entity_id, type)`。如果 `entity_type=student` 且 `entity_id=student_id`，同一个学生未来所有宿舍阻断都会折叠成同一条通知，无法表达不同阻断记录、不同原因或清退后再次阻断。

**建议：** 不选 Option 3。除非引入真正的 `DormClearanceBlock` 记录，否则不要创建该通知。

### 问题4：通知契约还有一个相邻不一致点，应一并修正 [P2]

**位置：**
- `docs/api/notification-contract-v0.1.md:51`
- `backend/apps/notifications/services.py:29`

契约写 `APPLICATION_SUBMITTED` 关联 `application`，但服务实际用 `entity_type='approval'`、`entity_id=approval.pk` 创建通知。考虑接收者是辅导员，通知入口要处理的是待审批记录，当前实现使用 `approval` 更合理。

**建议：** 本次修订 `notification-contract-v0.1.md` 时一并把 `APPLICATION_SUBMITTED` 的关联实体改为 `approval/{approval_id}`，避免后续 Phase 2B 文档只修宿舍阻断而留下旧冲突。

---

## 对审查要点的回答

### 1. 推荐选项

推荐 **Option 1** 作为当前 v0.1 / A-lite 决策：

- 保留 `422 DORM_BLOCKED` 同步响应。
- 不创建通知。
- `notification-contract-v0.1.md` 删除 `DORM_CLEARANCE_BLOCKED`，或保留在“Deferred / 后续版本”章节。
- 当前测试 `test_dorm_blocked_does_not_create_notification` 的方向保持正确，但断言应强化为“学生和辅导员都没有宿舍阻断/申请提交通知”。

### 2. 如果选 Option 2，实体设计怎么做

如果产品必须要通知中心留痕，建议独立表，不建议 blocked application。

建议表意：

```text
DormClearanceBlock
- block_id: blk_xxxxxxxx, primary key
- student: FK(User)
- dorm_status
- blocking_reason
- provider_error_code
- checked_at
- last_attempt_at
- resolved_at nullable
- created_at
```

通知使用：

```text
type = dorm_clearance_blocked
entity_type = dorm_clearance_block
entity_id = block_id
recipient = student
```

这样通知有合法业务实体，且不会污染申请审批状态机。

### 3. 如果选 Option 3，如何防重复

不推荐 Option 3。若临时采用，至少不要修改唯一约束；当前唯一约束已包含 `type`。但必须接受一个后果：同一学生的宿舍阻断通知会长期只有一条。

更好的折中不是扩大幂等键，而是新增阻断记录实体。把 `student_id + dorm_status + blocking_reason + unresolved` 归并到一个 open block record，再由通知引用该 record。

### 4. 测试如何调整

采用 Option 1：

- 保留并改名为 `test_dorm_blocked_returns_422_without_notification`。
- 断言响应 `error.code == DORM_BLOCKED`。
- 断言 `Application.objects.filter(student=blocked_student).count() == 0`。
- 断言 `Notification.objects.filter(recipient=blocked_student).count() == 0`。
- 保留辅导员没有 `application_submitted` 通知的断言。

采用 Option 2：

- 将原测试改为断言创建 `DormClearanceBlock` 和一条学生通知。
- 断言不创建 `Application` 和 `Approval`。
- 连续提交两次时，通知数量仍为1，阻断记录可更新 `last_attempt_at`。
- 断言辅导员不收到通知。

### 5. 契约如何修正

采用 Option 1 时，建议修订：

- 事件枚举移除 `DORM_CLEARANCE_BLOCKED`，或移动到 `Deferred events`。
- 删除详细事件说明中的 `entity_type: application / entity_id: application_id`。
- 在非目标或说明中写明：宿舍阻断当前是申请提交接口的同步错误响应，不进入通知中心。
- 同步修正 `APPLICATION_SUBMITTED` 的实体为 `approval/{approval_id}`，匹配现有服务实现。

### 6. 影响文件清单

Option 1 最小修改：

- `docs/api/notification-contract-v0.1.md`
- `backend/apps/notifications/tests/test_auto_notifications_api.py`

Option 2 独立表修改：

- `backend/apps/applications/models.py` 或新增 `backend/apps/dormitory/models.py`
- 对应 migration
- `backend/apps/applications/views.py`
- `backend/apps/notifications/models.py`
- `backend/apps/notifications/services.py`
- `backend/apps/notifications/tests/test_auto_notifications_api.py`
- `docs/api/notification-contract-v0.1.md`
- 如暴露阻断记录 API，再更新 schema/serializer/urls

Option 3 修改：

- `backend/apps/notifications/models.py`
- migration
- `backend/apps/notifications/services.py`
- `backend/apps/applications/views.py`
- `backend/apps/notifications/tests/test_auto_notifications_api.py`
- `docs/api/notification-contract-v0.1.md`

### 7. 实现风险评估

Option 1风险最低。主要风险是产品体验较弱，但当前用户已经在提交动作中即时收到明确错误，且该事件不是异步通知的强需求。

Option 2风险中等。独立表方案语义清楚，但会增加数据模型、迁移、测试和后续清退状态同步问题。只有在“通知中心留痕”是明确产品需求时才值得做。

Option 3风险最高。实现看似简单，但实体语义弱，幂等粒度粗，会给后续审计、重复阻断、原因变化和数据解释留下债务。

---

## 最终建议

Phase 2B不要直接实现宿舍阻断通知。当前应把 Phase 2B 定义为“契约修正优先”：从 v0.1 自动通知范围中移除或 defer `DORM_CLEARANCE_BLOCKED`，保持同步 `422` 阻断行为，并加强现有负路径测试。

如果后续要做“宿舍阻断通知中心留痕”，先单独立项 `DormClearanceBlock` 实体，再基于该实体创建通知。

**文档编号：** 63  
**状态：** Codex建议采用 Option 1；Option 2仅作为后续产品需求成立时的扩展方案
