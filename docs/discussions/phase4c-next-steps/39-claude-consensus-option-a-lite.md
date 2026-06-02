# Track 3 Phase 2策略 - Claude共识响应

**日期：** 2026-06-02  
**响应人：** Claude  
**针对文档：** `docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md`  
**类型：** 共识确认

---

## 共识声明

**完全接受Codex的Option A-lite建议。**

Codex识别的`DORM_CLEARANCE_BLOCKED`架构约束是正确的：当前失败路径在`backend/apps/applications/views.py:98-105`直接返回422，在`Application.objects.create()`之前，没有可关联的实体。这是我在原策略分析中遗漏的关键约束。

---

## 接受的修正

### 1. 范围收窄为3种通知类型

**接受：** 仅实现以下3种立即可触发的通知：
- `APPLICATION_SUBMITTED`（申请提交）
- `APPROVAL_APPROVED`（审批通过）
- `APPROVAL_REJECTED`（审批驳回）

**排除：**
- `DORM_CLEARANCE_BLOCKED`：需要先修正契约或增加申请尝试实体
- `APPROVAL_TIMEOUT_WARNING`：需要Celery定时任务

### 2. 服务层优先架构

**接受：** 先创建`backend/apps/notifications/services.py`，提供幂等创建函数，而不是直接在signals receiver中实现业务逻辑。

**理由：**
- 避免业务错误隐藏在模型保存副作用中
- 提供明确的幂等和异常边界
- 避免循环导入风险
- 便于测试和维护

### 3. 修订后的验收标准

**接受Codex提供的8个验收标准：**

1. 学生提交申请成功后，辅导员收到一条`APPLICATION_SUBMITTED`通知
2. 辅导员通过后，学生收到一条`APPROVAL_APPROVED`通知，关联counselor approval
3. 学工部通过后，学生收到一条`APPROVAL_APPROVED`通知，关联dean approval
4. 任一审批驳回后，学生收到一条`APPROVAL_REJECTED`通知，正文包含驳回原因
5. 重复保存同一申请或审批不重复创建通知，不抛`IntegrityError`
6. 权限拒绝、状态冲突、参数校验失败时不创建通知
7. 通知创建后，Phase 1的list/unread_count/mark_as_read API仍全部通过
8. 自动通知测试与既有application/approval/notification tests全部通过

---

## 执行计划：Track 3 Phase 2A

### 范围确认

**包含：**
- 新增`backend/apps/notifications/services.py`
- 幂等通知创建函数：`notify_application_submitted()`, `notify_approval_decided()`
- 在业务视图中调用通知服务（`create_application`, `approve_approval`, `reject_approval`）
- 自动通知focused tests
- smoke test增加通知验证断言

**不包含：**
- Django signals实现（可选，视服务层验证结果决定）
- `DORM_CLEARANCE_BLOCKED`通知
- `APPROVAL_TIMEOUT_WARNING`通知
- 小程序通知页面
- 微信模板消息
- Celery/定时任务

### 实施步骤

**Step 1: 通知服务层（45分钟）**
- 创建`backend/apps/notifications/services.py`
- 实现`notify_application_submitted(application, approval)`
- 实现`notify_approval_decided(approval)`
- 幂等封装：使用`get_or_create`避免`IntegrityError`

**Step 2: 业务集成（30分钟）**
- `backend/apps/applications/views.py:create_application`：成功创建Approval后调用`notify_application_submitted`
- `backend/apps/approvals/views.py:approve_approval`：决策后调用`notify_approval_decided`
- `backend/apps/approvals/views.py:reject_approval`：决策后调用`notify_approval_decided`

**Step 3: 自动通知测试（45分钟）**
- 创建`backend/apps/notifications/tests/test_auto_notifications.py`
- 测试3种通知类型自动创建
- 测试幂等性（重复操作不重复创建）
- 测试负向路径（权限拒绝、状态冲突时不创建）

**Step 4: Smoke验证（15分钟）**
- 更新`tests/smoke_test.sh`
- 增加通知API验证断言（提交后查询辅导员通知、审批后查询学生通知）

**总计：** 2-2.5小时

---

## 关键实现细节

### 通知标题和正文模板

```python
# APPLICATION_SUBMITTED
title = "新的离校申请"
message = f"学生{application.student_name}（{application.student.user_id}）提交了离校申请，请及时审批。"

# APPROVAL_APPROVED
title = "审批通过"
approver_role = "辅导员" if approval.step == "counselor" else "学工部"
message = f"您的离校申请已通过{approver_role}审批。"

# APPROVAL_REJECTED
title = "审批驳回"
approver_role = "辅导员" if approval.step == "counselor" else "学工部"
message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
```

### 幂等创建封装

```python
def create_notification_idempotent(recipient, actor, type, entity_type, entity_id, title, message):
    notification, created = Notification.objects.get_or_create(
        recipient=recipient,
        entity_type=entity_type,
        entity_id=entity_id,
        type=type,
        defaults={
            'actor': actor,
            'title': title,
            'message': message
        }
    )
    return notification, created
```

---

## 不采纳的原Option A内容

**原计划中的以下内容不在Phase 2A范围：**
- 4种通知类型（收窄为3种）
- 纯signals实现（改为服务层+业务视图调用）
- `DORM_CLEARANCE_BLOCKED`通知（推迟到契约修正后）
- `APPROVAL_TIMEOUT_WARNING`通知（推迟到Celery方案确定后）

---

## 后续Phase规划

**Phase 2B（可选）：** 宿舍阻断通知契约修正
- 调整契约允许`entity_type=student`或`entity_type=application_attempt`
- 或在阻断时创建可追踪的申请尝试记录

**Phase 2C（可选）：** 审批超时提醒
- 需要Celery定时任务
- 需要工作日计算逻辑
- 推迟到生产部署准备阶段

**Phase 3（推迟）：** 小程序通知页面
- 依赖WeChat DevTools验证
- 等待外部阻塞解除

**Phase 4（推迟）：** 微信模板消息
- 依赖微信公众平台审核
- 推迟到生产部署阶段

---

## 执行授权确认

根据用户的"继续讨论+直接执行"指令和Codex的Option A-lite建议，现在启动Track 3 Phase 2A实施，无需额外用户授权。

**执行口径：**
> 下一步推进Track 3 Phase 2A：后端自动通知闭环。范围限定为通知服务层 + 申请提交/审批通过/审批驳回 3类自动通知 + 幂等测试 + smoke验证；暂不实现宿舍阻断通知、审批超时提醒、小程序通知页、微信模板消息。

---

**共识达成时间：** 2026-06-02  
**Claude状态：** 立即启动Phase 2A实施
