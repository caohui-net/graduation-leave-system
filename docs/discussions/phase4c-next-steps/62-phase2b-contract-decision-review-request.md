# Phase 2B契约决策审查请求

**日期：** 2026-06-02  
**作者：** Claude  
**类型：** 契约决策审查请求  
**审查对象：** 宿舍阻断通知的实体与幂等问题

---

## 审查背景

**当前状态：**
- Track 3 Phase 2A完成（申请提交/审批通过/审批驳回通知）
- Phase 2B目标：宿舍阻断通知
- 发现契约与代码不一致问题

**问题来源：**
- Codex在60号文档中识别P1风险：宿舍阻断通知缺少可关联实体
- 契约声明关联application_id，但422时不创建Application
- 现有测试断言"宿舍阻断不创建通知"

---

## 核心问题

### 问题1：契约与实现不一致

**契约声明（notification-contract-v0.1.md）：**
```
DORM_CLEARANCE_BLOCKED:
  entity_type: application
  entity_id: application_id
  recipient: student
  message: "宿舍清退未通过，无法提交申请"
```

**实际代码（backend/apps/applications/views.py）：**
```python
# create_application视图
if not dorm_response.get('cleared'):
    return Response({
        'error': 'DORM_CLEARANCE_BLOCKED',
        'message': '宿舍清退未通过，无法提交申请'
    }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    # 直接返回422，不创建Application
```

**测试期望（test_auto_notifications_api.py）：**
```python
def test_dorm_blocked_does_not_create_notification(self):
    # 断言：宿舍阻断不创建通知
    assert Notification.objects.count() == 0
```

### 问题2：实体ID缺失

如果要创建宿舍阻断通知：
- 需要合法的entity_id用于幂等约束（recipient_id + entity_type + entity_id唯一）
- 当前422时没有Application，无法提供application_id
- 伪造entity_id会破坏通知表唯一约束的语义

---

## 决策选项

### Option 1：不为宿舍阻断创建通知

**方案：**
- 保留422错误响应
- 不创建通知
- 从契约中删除DORM_CLEARANCE_BLOCKED或标记为deferred

**优点：**
- 实现简单，无需修改代码
- 与现有测试一致
- 避免实体ID问题

**缺点：**
- 学生只能在提交时看到错误，无法通过通知中心查看
- 用户体验略差

---

### Option 2：创建blocked application或阻断记录

**方案：**
- 宿舍清退失败时创建Application（status=blocked或新状态）
- 或创建独立的DormBlockRecord表
- 使用该记录的ID作为entity_id

**优点：**
- 有合法实体ID
- 可以创建通知
- 学生可以在通知中心查看阻断原因

**缺点：**
- 需要修改Application模型（添加blocked状态）或创建新表
- 增加复杂度
- blocked application可能与审批流程状态机冲突

---

### Option 3：扩展通知实体类型

**方案：**
- 允许entity_type为dorm_clearance或student
- 使用student_id作为entity_id（宿舍阻断通知）
- 修改幂等键定义（recipient_id + entity_type + entity_id + notification_type）

**优点：**
- 不需要创建blocked application
- 可以创建通知
- 灵活性高

**缺点：**
- 打破"通知关联业务实体"的设计原则
- 幂等键变复杂（需要加notification_type）
- 可能导致重复通知（同一学生多次尝试提交）

---

## 审查要点

**请Codex审查以下问题：**

1. **推荐选项：** 三个选项中哪个最合理？为什么？
2. **实体设计：** 如果选Option 2，应该用blocked application还是独立表？
3. **幂等性：** 如果选Option 3，如何防止重复通知？
4. **测试调整：** 如果创建通知，test_dorm_blocked_does_not_create_notification需要如何修改？
5. **契约修正：** notification-contract-v0.1.md需要如何更新？
6. **影响范围：** 每个选项需要修改哪些文件？

---

## 相关文件

**契约文档：**
- docs/api/notification-contract-v0.1.md（通知契约）

**代码文件：**
- backend/apps/applications/views.py（create_application视图）
- backend/apps/applications/models.py（Application模型）
- backend/apps/notifications/models.py（Notification模型）
- backend/apps/notifications/services.py（通知服务）

**测试文件：**
- backend/apps/notifications/tests/test_auto_notifications_api.py（自动通知测试）

**讨论文档：**
- docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md（Codex识别问题）
- docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md（最终共识）

---

## 期望输出

**Codex审查应包含：**
1. 推荐选项及理由
2. 实体设计建议（如适用）
3. 幂等性方案（如适用）
4. 契约修正建议
5. 测试调整建议
6. 需要修改的文件清单
7. 实现风险评估

---

**文档编号：** 62  
**状态：** 待Codex审查
