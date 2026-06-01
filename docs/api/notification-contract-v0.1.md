# 通知系统契约 v0.1

**版本：** v0.1  
**状态：** Draft  
**创建日期：** 2026-06-01  
**目的：** 定义通知系统最小契约，为后续实现提供设计基础

---

## 1. 概述

本契约定义毕业生离校申请审批系统的通知功能最小契约。通知系统用于向用户推送申请状态变更、审批结果、系统提醒等信息。

**设计原则：**
- 最小化：只定义核心通知读取功能
- 幂等性：同一业务事件不重复创建通知
- 权限隔离：用户只能读取自己的通知

**非目标：**
- 微信模板消息推送（推迟到生产部署）
- 小程序通知页面（推迟到DevTools可用）
- 实时推送（WebSocket/SSE）
- 消息中心运营功能

---

## 2. 通知事件类型

### 2.1 事件枚举

| 事件类型 | 枚举值 | 触发时机 | 接收者 |
|---------|--------|----------|--------|
| 申请提交 | APPLICATION_SUBMITTED | 学生提交离校申请 | 辅导员 |
| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
| 宿舍清退阻断 | DORM_CLEARANCE_BLOCKED | 宿舍清退未完成阻断申请 | 学生 |
| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |

### 2.2 事件详细说明

#### APPLICATION_SUBMITTED（申请提交）

**触发条件：** 学生成功提交离校申请

**接收者：** 该学生的辅导员

**通知内容：**
- 标题：`新的离校申请`
- 正文：`学生{student_name}（{student_id}）提交了离校申请，请及时审批。`

**关联实体：**
- entity_type: `application`
- entity_id: `{application_id}`

---

#### APPROVAL_APPROVED（审批通过）

**触发条件：** 辅导员或学工部审批通过

**接收者：** 申请学生

**通知内容：**
- 标题：`审批通过`
- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）

**关联实体：**
- entity_type: `approval`
- entity_id: `{approval_id}`

---

#### APPROVAL_REJECTED（审批驳回）

**触发条件：** 辅导员或学工部驳回申请

**接收者：** 申请学生

**通知内容：**
- 标题：`审批驳回`
- 正文：`您的离校申请被{approver_role}驳回。驳回原因：{comment}`

**关联实体：**
- entity_type: `approval`
- entity_id: `{approval_id}`

---

#### DORM_CLEARANCE_BLOCKED（宿舍清退阻断）

**触发条件：** 宿舍管理系统返回清退未完成

**接收者：** 申请学生

**通知内容：**
- 标题：`宿舍清退未完成`
- 正文：`您的离校申请因宿舍清退未完成而被阻断，请先完成宿舍清退手续。`

**关联实体：**
- entity_type: `application`
- entity_id: `{application_id}`

---

#### APPROVAL_TIMEOUT_WARNING（审批超时提醒）

**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理

**接收者：** 待审批的辅导员/学工部

**通知内容：**
- 标题：`审批超时提醒`
- 正文：`学生{student_name}的离校申请已超过{days}个工作日未审批，请及时处理。`

**关联实体：**
- entity_type: `approval`
- entity_id: `{approval_id}`

---

## 3. 数据模型

### 3.1 Notification字段草案

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| notification_id | String | 是 | 通知ID，格式：not_xxxxxxxx（8位随机字符） |
| recipient_id | String | 是 | 接收者用户ID（外键：User.user_id） |
| actor_id | String | 否 | 触发者用户ID（外键：User.user_id），可为空 |
| type | Enum | 是 | 通知类型（见2.1事件枚举） |
| title | String | 是 | 通知标题（最大100字符） |
| body | String | 是 | 通知正文（最大500字符） |
| entity_type | Enum | 是 | 关联实体类型：application/approval |
| entity_id | String | 是 | 关联实体ID |
| read_at | DateTime | 否 | 已读时间，未读为null |
| created_at | DateTime | 是 | 创建时间 |

### 3.2 索引建议

```sql
-- 主键索引
PRIMARY KEY (notification_id)

-- 接收者查询索引（最常用）
INDEX idx_recipient_created (recipient_id, created_at DESC)

-- 未读通知查询索引
INDEX idx_recipient_unread (recipient_id, read_at) WHERE read_at IS NULL

-- 幂等性唯一约束（防止重复通知）
UNIQUE INDEX idx_notification_idempotency (recipient_id, entity_type, entity_id, type)
```

---

## 4. API契约

### 4.1 列出通知

**端点：** `GET /api/notifications/`

**权限：** 认证用户

**查询参数：**
- `read` (可选): `true`/`false`/`all`，默认`all`
- `limit` (可选): 每页数量，默认20，最大100
- `offset` (可选): 偏移量，默认0

**请求示例：**
```http
GET /api/notifications/?read=false&limit=20&offset=0
Authorization: Bearer {access_token}
```

**响应示例（200 OK）：**
```json
{
  "count": 5,
  "results": [
    {
      "notification_id": "not_a1b2c3d4",
      "type": "APPROVAL_APPROVED",
      "title": "审批通过",
      "body": "您的离校申请已通过辅导员审批。",
      "entity_type": "approval",
      "entity_id": "apv_12345678",
      "read_at": null,
      "created_at": "2026-06-01T10:30:00Z",
      "actor": {
        "user_id": "T001",
        "name": "张老师"
      }
    }
  ]
}
```

**RBAC规则：**
- 用户只能查询自己的通知（recipient_id = request.user.user_id）
- 管理员不默认拥有跨用户读取权限

---

### 4.2 未读通知数

**端点：** `GET /api/notifications/unread_count/`

**权限：** 认证用户

**请求示例：**
```http
GET /api/notifications/unread_count/
Authorization: Bearer {access_token}
```

**响应示例（200 OK）：**
```json
{
  "unread_count": 3
}
```

---

### 4.3 标记单条已读

**端点：** `PATCH /api/notifications/{notification_id}/read/`

**权限：** 认证用户，且notification.recipient_id = request.user.user_id

**请求示例：**
```http
PATCH /api/notifications/not_a1b2c3d4/read/
Authorization: Bearer {access_token}
```

**响应示例（200 OK）：**
```json
{
  "notification_id": "not_a1b2c3d4",
  "read_at": "2026-06-01T11:00:00Z"
}
```

**错误响应（403 FORBIDDEN）：**
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "您无权标记此通知为已读"
  }
}
```

---

### 4.4 全部标记已读

**端点：** `POST /api/notifications/mark_all_read/`

**权限：** 认证用户

**请求示例：**
```http
POST /api/notifications/mark_all_read/
Authorization: Bearer {access_token}
```

**响应示例（200 OK）：**
```json
{
  "marked_count": 5
}
```

---

## 5. 幂等性规则

### 5.1 通知创建幂等

**规则：** 同一业务状态变更不重复创建同类通知给同一接收者

**实现建议：**
- 在创建通知前检查是否已存在相同的(recipient_id, entity_type, entity_id, type)组合
- 如果已存在，跳过创建
- 数据库唯一约束保证幂等性：`UNIQUE(recipient_id, entity_type, entity_id, type)`

**示例：**
```python
# 伪代码
existing = Notification.objects.filter(
    recipient_id=recipient_id,
    entity_type='approval',
    entity_id=approval_id,
    type='APPROVAL_APPROVED'
).exists()

if not existing:
    Notification.objects.create(...)
```

### 5.2 状态变更触发

**规则：** 通知创建应在业务事务提交后触发

**实现建议：**
- 使用Django signals的`post_save`信号
- 在信号处理器中检查状态变更（如approval.decision从pending变为approved）
- 只在状态实际变更时创建通知

---

## 6. RBAC权限矩阵

| 操作 | 学生 | 辅导员 | 学工部 | 说明 |
|------|------|--------|--------|------|
| 列出自己的通知 | ✓ | ✓ | ✓ | 所有用户可查询自己的通知 |
| 查询未读数 | ✓ | ✓ | ✓ | 所有用户可查询自己的未读数 |
| 标记自己的通知已读 | ✓ | ✓ | ✓ | 所有用户可标记自己的通知 |
| 全部标记已读 | ✓ | ✓ | ✓ | 所有用户可标记自己的所有通知 |
| 查询他人通知 | ✗ | ✗ | ✗ | 任何角色都不能查询他人通知 |
| 删除通知 | ✗ | ✗ | ✗ | v0.1不支持删除（软删除可在后续版本考虑） |

**注意：** 管理员角色不默认拥有跨用户读取通知的权限。如需管理员查看所有通知，应在后续版本中明确设计。

---

## 7. 错误码

| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| FORBIDDEN | 403 | 无权访问该通知 |
| NOT_FOUND | 404 | 通知不存在 |
| VALIDATION_ERROR | 400 | 请求参数验证失败（包括通知已读等状态错误） |

**注意：** 复用现有后端错误码，保持API一致性。`ALREADY_READ`等业务状态错误归入`VALIDATION_ERROR`类别。

---

## 8. 实现阶段划分

### Phase 0: 契约草案（当前阶段）

**交付物：** 本文档

**时间：** 2-3小时

**范围：** 纯文档设计，不涉及代码实现

---

### Phase 1: 后端MVP（需单独授权）

**前置条件：** 用户明确授权启动Track 3实现

**交付物：**
- Django Notification模型
- 数据库迁移文件
- Serializer和ViewSet
- 4个API端点实现
- 单元测试（15-20个测试）

**时间估算：** 0.5-1天

**验收标准：**
- 所有API端点可通过Postman/curl验证
- 单元测试覆盖率>80%
- 数据库唯一约束测试通过（UNIQUE(recipient_id, entity_type, entity_id, type)）
- RBAC权限测试通过
- 已读状态测试通过
- 分页/过滤测试通过

**注意：** 业务幂等性测试（同一业务状态变更不重复创建通知）推迟到Phase 2（信号触发）实现。

**测试数据创建：**

Phase 1不实现通知创建API（通知应由系统自动创建），因此需要其他方式创建测试数据：

1. **Management Command（推荐）：** `python manage.py seed_notifications`
   - 创建预定义的测试通知数据
   - 支持--user参数指定接收者
   - 支持--count参数指定数量
   - 可重复执行，用于自动化测试和演示

2. **Django Shell：** 手动创建通知对象
   ```python
   from apps.notifications.models import Notification
   Notification.objects.create(
       recipient_id="2020001",
       type="APPROVAL_APPROVED",
       title="审批通过",
       body="您的离校申请已通过辅导员审批。",
       entity_type="approval",
       entity_id="apv_12345678"
   )
   ```

3. **Test Fixture：** 用于单元测试
   - `apps/notifications/fixtures/test_notifications.json`
   - 包含各种场景的测试数据

---

### Phase 2: 信号触发（需单独审查）

**前置条件：** Phase 1完成且通过审查

**交付物：**
- Django signals实现
- 5种事件触发逻辑
- 事务边界处理
- 幂等性保证

**时间估算：** 0.5天

**审查要点：**
- 事务边界是否正确
- 幂等性是否保证
- 状态机副作用是否可控

---

### Phase 3: 小程序通知页（需DevTools可用）

**前置条件：** WeChat DevTools验证通过

**交付物：**
- 通知列表页面
- 通知详情跳转
- 未读标记UI

**时间估算：** 0.5-1天

---

### Phase 4: 微信模板消息（需生产部署）

**前置条件：** 生产环境部署 + 微信公众平台配置

**交付物：**
- 微信模板消息配置
- Celery异步任务
- 模板消息推送逻辑

**时间估算：** 0.5-1天

---

## 9. 技术约束

### 9.1 数据库

- 使用PostgreSQL
- 通知表预计数据量：10万条/年（假设1000学生，每人100条通知）
- 保留策略：建议保留1年，超过1年的通知可归档或删除

### 9.2 性能要求

- 列表查询响应时间：<200ms（分页20条）
- 未读数查询响应时间：<100ms
- 标记已读响应时间：<100ms

### 9.3 并发处理

- 通知创建应在独立事务中，避免阻塞主业务流程
- 建议使用异步任务（Celery）创建通知，但v0.1可以同步创建

---

## 10. 后续扩展方向

以下功能不在v0.1范围内，可在后续版本考虑：

- 通知分类（系统通知/业务通知/运营通知）
- 通知优先级（高/中/低）
- 通知过期时间
- 通知软删除
- 通知批量操作
- 通知搜索
- 通知导出
- 管理员通知管理界面
- 实时推送（WebSocket/SSE）
- 邮件通知
- 短信通知

---

## 11. 参考文档

- 系统设计文档：`docs/design/2026-05-27-system-design.md`
- API契约v0.3：`docs/api/contract-v0.3.md`
- 数据对接说明：`docs/数据对接说明文档.md`

---

**契约版本：** v0.1 Draft  
**最后更新：** 2026-06-01  
**下一步：** 等待用户授权进入Phase 1实现
