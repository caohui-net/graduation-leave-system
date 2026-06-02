# Phase 2B Option 1执行审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对：** 65-phase2b-option1-execution-review-request.md  
**审查类型：** 执行后审查

---

## 审查结论

**结论：需要补充修改后再commit。**

Option 1方向正确：v0.1契约删除`DORM_CLEARANCE_BLOCKED`，代码枚举删除该类型，宿舍阻断路径保持422同步失败且不创建通知。`APPLICATION_SUBMITTED`改为关联`approval/{approval_id}`也与当前实现一致。

但当前仍有两个需要处理的问题：

1. **P1：迁移文件仍保留`dorm_clearance_blocked`选择项，存在模型/迁移漂移。**
2. **P2：通知契约示例仍使用大写type字符串，与API实际返回的小写枚举值不一致。**

---

## 发现的问题

### P1：迁移文件仍保留已删除枚举

**位置：** `backend/apps/notifications/migrations/0001_initial.py:22`

**问题描述：**  
`NotificationType`模型已删除`DORM_CLEARANCE_BLOCKED`，当前模型只有4个枚举值：

- `application_submitted`
- `approval_approved`
- `approval_rejected`
- `approval_timeout_warning`

但初始迁移的`type`字段choices仍包含：

```python
('dorm_clearance_blocked', '宿舍清退阻断')
```

**验证结果：**

```bash
PYTHONPATH=. python backend/manage.py makemigrations --check --dry-run
```

输出显示Django会生成：

```text
Migrations for 'notifications':
  backend/apps/notifications/migrations/0002_alter_notification_type.py
    - Alter field type on notification
```

**影响：**

- 代码与迁移状态不一致。
- CI若执行`makemigrations --check --dry-run`会失败。
- 新环境按迁移建库时，字段choices仍会显示旧类型，虽然数据库层通常不强制choices，但迁移定义与契约不一致。

**修复建议：**

如果当前迁移尚未作为稳定生产基线发布，直接同步修改`0001_initial.py`移除该choice最干净；如果迁移历史需要保持不可变，则生成并提交`0002_alter_notification_type.py`。

本项目当前仍处Draft/MVP阶段，且这是刚创建的通知初始迁移，建议直接修正`0001_initial.py`，然后重新运行：

```bash
PYTHONPATH=. python backend/manage.py makemigrations --check --dry-run
```

预期输出应为`No changes detected`。

---

### P2：契约API示例仍使用大写type字符串

**位置：**

- `docs/api/notification-contract-v0.1.md:165`
- `docs/api/notification-contract-v0.1.md:279`
- `docs/api/notification-contract-v0.1.md:374`

**问题描述：**  
契约事件表使用符号名`APPLICATION_SUBMITTED`等可以接受，但API响应示例和伪代码/ shell示例中的实际`type`值仍写成`APPROVAL_APPROVED`。当前模型和测试均使用小写落库值，例如`approval_approved`、`application_submitted`。

**影响：**

- API消费者会误以为响应字段`type`返回大写值。
- 与此前Phase 2A已达成的“小写枚举值”一致性要求冲突。

**修复建议：**

保留2.1事件枚举表中的符号名也可以，但在API响应示例、创建示例、伪代码中使用实际序列化值：

- `APPROVAL_APPROVED` -> `approval_approved`
- `APPLICATION_SUBMITTED` -> `application_submitted`
- 其他同理

也可以在2.1增加一句说明：表中枚举名为文档符号名，API/数据库实际值为对应小写snake_case。

---

## 审查通过的部分

### 1. `DORM_CLEARANCE_BLOCKED`契约删除基本完整

`docs/api/notification-contract-v0.1.md`事件枚举表已只剩4类通知，详细说明章节也不再包含宿舍阻断通知。对v0.1自动通知契约而言，这符合Option 1。

补充说明：`docs/PROJECT-SUMMARY.md`和旧讨论文档仍存在历史引用，这是历史记录，不必作为本次契约修正的阻塞项；但如果`PROJECT-SUMMARY.md`被当作当前状态摘要使用，应在后续归档时同步更新。

### 2. `APPLICATION_SUBMITTED`关联`approval`语义合理

代码顺序显示，申请创建后立即创建辅导员审批记录，再调用通知服务：

- `backend/apps/applications/views.py:150`创建`Application`
- `backend/apps/applications/views.py:161`创建`Approval`
- `backend/apps/applications/views.py:170`调用`notify_application_submitted(...)`

通知服务实际写入：

- `entity_type='approval'`
- `entity_id=approval.pk`
- `type=NotificationType.APPLICATION_SUBMITTED`

对应位置：`backend/apps/notifications/services.py:29-33`。

因此辅导员收到通知时，关联审批记录已经存在。当前同步执行路径下，不存在“通知指向不存在approval”的edge case，除非后续把通知创建异步化或将`Application/Approval`创建与通知创建拆成不同事务；那应另行引入事务提交后触发或补偿策略。

### 3. 阻断测试覆盖了Option 1核心行为

`backend/apps/notifications/tests/test_auto_notifications_api.py:245-257`覆盖了三点：

- 422阻断响应。
- 未创建`Application`。
- 未给学生创建通知。
- 未给辅导员创建`application_submitted`通知。

这已经覆盖Option 1的核心验收点。验证422错误message可以作为P2增强，但不是当前commit门禁；当前断言已足够证明“阻断不产生申请、不产生通知”。

---

## 验证记录

### 引用搜索

```bash
rg -n "DORM_CLEARANCE_BLOCKED|dorm_clearance_blocked|宿舍清退阻断|APPLICATION_SUBMITTED|application_submitted|NotificationType" docs backend -S
```

关键结果：

- 业务代码未发现`DORM_CLEARANCE_BLOCKED`残留引用。
- `backend/apps/notifications/migrations/0001_initial.py:22`仍保留`dorm_clearance_blocked`。
- 历史讨论文档存在旧引用，属于历史记录。

### 迁移检查

```bash
PYTHONPATH=. python backend/manage.py makemigrations --check --dry-run
```

结果：失败，提示会生成`0002_alter_notification_type.py`。

### 目标测试

```bash
PYTHONPATH=. python backend/manage.py test apps.notifications.tests.test_auto_notifications apps.notifications.tests.test_auto_notifications_api --keepdb --noinput
```

结果：通过，12 tests OK。

说明：本地默认`python3`无Django；使用`uv run --python 3.11 --with-requirements backend/requirements/dev.txt`提供隔离依赖环境。直接运行`python backend/manage.py`需要`PYTHONPATH=.`，否则项目现有`from backend.schema import ErrorResponseSerializer`导入会失败。

---

## 最终建议

**暂不commit。** 先完成两个补充修正：

1. 修正通知迁移choices，确保`makemigrations --check --dry-run`无变更。
2. 修正`notification-contract-v0.1.md`中API示例/伪代码的type实际值为小写snake_case。

完成后可重新运行目标测试和迁移检查。若两者通过，本次Option 1执行可以commit。

---

**文档编号：** 66  
**状态：** Codex审查完成，等待Claude修复
