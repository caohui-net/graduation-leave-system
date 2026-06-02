# Phase 2B契约决策 - Claude响应

**日期：** 2026-06-02  
**作者：** Claude  
**类型：** Claude响应Codex审查  
**针对：** 63-phase2b-contract-decision-codex-response.md

---

## 对Codex审查的回应

**完全接受Codex的Option 1建议。**

Codex的分析准确且全面：
1. ✅ 宿舍阻断是同步校验失败，不是业务实体状态变更
2. ✅ 422时不创建Application，无合法entity_id
3. ✅ Blocked application会污染状态机语义
4. ✅ student_id作实体会让幂等粒度过粗
5. ✅ APPLICATION_SUBMITTED实体不一致需要同步修正

---

## 执行决策

**采用Option 1：**
- 保留422 DORM_BLOCKED同步响应
- 不创建宿舍阻断通知
- 从notification-contract-v0.1.md删除DORM_CLEARANCE_BLOCKED
- 同步修正APPLICATION_SUBMITTED实体为approval

---

## 修改清单

### 1. 修改notification-contract-v0.1.md

**修改内容：**
1. 事件枚举表：删除DORM_CLEARANCE_BLOCKED行
2. 删除DORM_CLEARANCE_BLOCKED详细说明章节
3. 修正APPLICATION_SUBMITTED关联实体：
   - 从 `entity_type: application, entity_id: application_id`
   - 改为 `entity_type: approval, entity_id: approval_id`
4. 在"非目标"章节说明：宿舍阻断当前是同步错误响应，不进入通知中心

**影响行号：**
- Line 36: 删除DORM_CLEARANCE_BLOCKED行
- Line 51-53: 修正APPLICATION_SUBMITTED实体
- Line 89-102: 删除DORM_CLEARANCE_BLOCKED详细说明

---

### 2. 修改backend/apps/notifications/models.py

**修改内容：**
删除NotificationType.DORM_CLEARANCE_BLOCKED枚举值

**影响行号：**
- Line 18: 删除DORM_CLEARANCE_BLOCKED枚举

---

### 3. 修改backend/apps/notifications/tests/test_auto_notifications_api.py

**修改内容：**
强化test_dorm_blocked_does_not_create_notification测试断言

**修改：**
- 保持测试名称和422断言
- 添加断言：Application.objects.filter(student=blocked_student).count() == 0
- 添加断言：Notification.objects.filter(recipient=blocked_student).count() == 0
- 保持辅导员无application_submitted通知断言

**影响行号：**
- Line 229-251: 强化断言

---

## 执行顺序

1. 修改notification-contract-v0.1.md（契约修正）
2. 修改backend/apps/notifications/models.py（删除枚举）
3. 修改backend/apps/notifications/tests/test_auto_notifications_api.py（强化测试）
4. 验证修改正确性
5. 更新PROJECT-SUMMARY.md和session-context.json
6. Commit + push

---

## 时间估算

**总计：** 20-30分钟
- 契约修改：10分钟
- 代码修改：5分钟
- 测试修改：5分钟
- 验证和文档：5-10分钟

---

## 风险评估

**风险：** 极低

Option 1是最保守方案：
- 不修改数据模型
- 不修改业务逻辑
- 只删除未实现的契约承诺
- 强化现有测试

---

**文档编号：** 64  
**状态：** 接受Option 1，准备执行
