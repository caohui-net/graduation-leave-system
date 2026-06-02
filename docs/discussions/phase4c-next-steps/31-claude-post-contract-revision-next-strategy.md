# Track 3契约修正后下一步策略 - Claude分析

**日期：** 2026-06-01  
**分析人：** Claude  
**背景：** Track 3契约修正完成，用户再次要求继续讨论下一步

---

## 当前状态快照

**已完成里程碑：**
- ✅ M1: Backend Ops Hardening Complete
- ✅ M2: Phase 4C Evidence Ready
- ✅ Track 3 Phase 0: 通知契约草案v0.1
- ✅ Track 3契约修正：5个P1/P2问题已修正

**Track 3进度：**
- Phase 0: 通知契约草案 ✅ 完成（2.5小时）
- 契约修正 ✅ 完成（30-60分钟）
- Phase 1: 后端MVP实现 ⏸ 等待授权（0.5-1天）
- Phase 2: 信号触发 ⏸ 等待Phase 1完成
- Phase 3: 小程序通知页 ⏸ 等待DevTools
- Phase 4: 微信模板消息 ⏸ 等待生产部署

**外部阻塞项：**
1. WeChat DevTools验证（小程序验收门控）
2. 宿舍管理系统真实集成（需API文档和测试凭证）

---

## 问题陈述

Track 3契约修正完成后，用户第三次使用相同指令要求继续讨论下一步。前两次使用该指令分别导致了：
1. 第一次：Phase 4C证据闭环完成
2. 第二次：Track 3 Phase 0通知契约草案完成

**核心问题：**
1. 契约修正完成后，是否应该启动Phase 1实现？
2. 还是应该等待外部阻塞项解除？
3. 是否有比Phase 1更有价值的工作方向？
4. 用户的新指令是否构成Phase 1授权？

---

## 可选策略分析

### Option A: 启动Track 3 Phase 1 - 后端MVP实现

**描述：** 实现通知系统后端MVP（Django model + migration + serializer + viewset + API + 测试）

**优势：**
- 契约已修正，所有P1/P2问题已解决
- 实现路径清晰，风险可控
- 不依赖外部阻塞项
- 可以通过Postman/curl验证
- 自然延续Track 3工作流程

**风险：**
- 可能违反"Phase 1需明确授权"的共识
- 实现后如果发现新问题，需要返工
- 投入0.5-1天时间，但小程序验收仍被DevTools阻塞

**工作量估算：** 0.5-1天
- Phase 1A: Django Notification模型 + migration（1-2小时）
- Phase 1B: Serializer + ViewSet + 4个API端点（2-3小时）
- Phase 1C: 单元测试（2-3小时，15-20个测试）
- Phase 1D: 验证和文档（1小时）

**关键决策点：**
- Phase 1是否包含信号触发？（推荐：不包含，Phase 2单独实现）
- 如何创建测试数据？（推荐：management command）
- 幂等性检查放在哪一层？（推荐：信号层，Phase 1不实现）

---

### Option B: 等待WeChat DevTools验证

**描述：** 暂停Track 3，等待用户完成DevTools安装和验证

**优势：**
- 解除小程序验收的最高价值阻塞项
- 验证通过后可以完整测试小程序功能
- 避免在无法验收的情况下继续开发

**风险：**
- 完全依赖用户操作，Claude无法推进
- 可能需要较长等待时间
- 项目进度停滞

**工作量估算：** 用户操作，Claude等待

---

### Option C: 收集宿舍系统真实信息

**描述：** 等待用户提供宿舍管理系统的真实API文档和测试凭证

**优势：**
- 解除生产部署的关键阻塞项
- 可以实现真实的宿舍清退检查
- 避免Mock数据与真实系统不一致

**风险：**
- 完全依赖用户操作，Claude无法推进
- 可能需要较长等待时间
- 宿舍系统可能不存在或不可用

**工作量估算：** 用户操作，Claude等待

---

### Option D: 再次提供决策门

**描述：** 向用户明确确认是否授权Phase 1实现

**优势：**
- 遵守原共识（Phase 1需明确授权）
- 给用户明确的选择权
- 避免误解用户意图

**风险：**
- 可能让用户感觉流程繁琐
- 用户可能已经通过"继续讨论"隐式授权
- 与用户"无需我的干预，直接执行"的指令冲突

**决策门选项：**
1. 启动Track 3 Phase 1实现（后端MVP）
2. 等待WeChat DevTools验证
3. 等待宿舍系统信息收集
4. 其他方向（用户自定义）

---

### Option E: 实施Phase 1的最小子集（验证性实现）

**描述：** 只实现Notification模型和迁移，不实现API，用于验证数据结构设计

**优势：**
- 风险最小（只改数据库schema）
- 可以验证模型设计是否合理
- 为后续API实现打基础
- 如果发现问题，回滚成本低

**风险：**
- 可能被认为是"半成品"
- 无法通过API验证功能
- 可能需要后续再次迁移

**工作量估算：** 1-2小时
- Django Notification模型
- 数据库迁移
- 模型单元测试（5-8个测试）

---

## Claude推荐策略

**推荐：Option A - 启动Track 3 Phase 1（后端MVP实现），但需Codex确认授权解读**

**理由：**

1. **用户意图推断：** 用户三次使用相同指令"下一步的工作我需要你和CODEX讨论进行...直接执行，直到项目完成"。前两次导致了证据闭环和契约草案的完成。现在契约修正完成后，用户再次使用相同指令，合理推断是希望继续推进到实现阶段。

2. **契约质量已达标：** 5个P1/P2问题已修正，契约质量已达到实现标准。继续等待可能是过度谨慎。

3. **自然延续：** Phase 0（契约）→ 契约修正 → Phase 1（实现）是自然的工作流程。

4. **不依赖外部：** Phase 1是纯后端工作，不需要DevTools或宿舍系统，可以独立推进。

5. **可验证性：** Phase 1完成后可以通过Postman/curl验证所有API端点，不需要小程序UI。

6. **用户指令强调"直接执行"：** 用户明确说"在得到统一可靠可行的执行方案后,无需我的干预，直接执行，直到项目完成"。如果再次提供决策门（Option D），可能与用户意图冲突。

**但需要Codex确认：**
- 用户的新指令是否构成Phase 1授权？
- 还是应该再次明确决策门？
- 是否有比Phase 1更有价值的工作方向？

**如果Codex确认可以启动Phase 1，建议范围：**

**Phase 1A: 模型和迁移（1-2小时）**
- Django Notification模型（10字段）
- 数据库迁移（包含索引和唯一约束）
- Django admin注册（可选，便于调试）
- 模型单元测试（8-10个测试）

**Phase 1B: API实现（2-3小时）**
- NotificationSerializer
- NotificationViewSet
- 4个API端点实现
  - GET /api/notifications/（列表，支持read过滤和分页）
  - GET /api/notifications/unread_count/（未读数）
  - PATCH /api/notifications/{id}/read/（标记已读）
  - POST /api/notifications/mark_all_read/（全部已读）
- URL注册
- RBAC权限检查

**Phase 1C: 测试（2-3小时）**
- API单元测试（12-15个测试）
  - 列表API测试（分页、过滤、权限）
  - 未读数API测试
  - 标记已读API测试（单条、全部、权限）
  - RBAC测试（跨用户访问拒绝）
  - 数据库唯一约束测试
- Management command: seed_notifications（创建测试数据）

**Phase 1D: 验证和文档（1小时）**
- Postman/curl验证所有端点
- 更新notification-contract-v0.1.md状态为"Phase 1 implemented"
- 更新PROJECT-SUMMARY.md
- 更新session-context.json

**不包含在Phase 1：**
- 信号触发逻辑（推迟到Phase 2）
- Celery异步任务（推迟到Phase 2）
- 小程序通知页（推迟到Phase 3）
- 微信模板消息（推迟到Phase 4）

---

## 关键实现决策（如果启动Phase 1）

### 1. 测试数据创建方式

**问题：** Phase 1如何创建通知用于测试？

**选项：**
- A. 通过POST /api/notifications/创建（需要新增创建端点）
- B. 通过Django shell手动创建
- C. 通过management command创建测试数据

**推荐：** Option C（management command）

**理由：**
- 契约中没有定义创建通知的API（通知应该由系统自动创建）
- Management command适合自动化测试和演示
- 可重复执行，支持不同场景

**实现：**
```python
# backend/apps/notifications/management/commands/seed_notifications.py
python manage.py seed_notifications --user 2020001 --count 10
```

### 2. 幂等性检查位置

**问题：** 在哪一层检查通知是否已存在？

**推荐：** Phase 1不实现幂等性检查，Phase 2实现信号时一起处理

**理由：**
- 幂等性主要针对自动创建的通知（信号触发）
- Phase 1只实现读取API，不实现创建路径
- 数据库唯一约束已经保证了底层幂等性

### 3. 信号触发时机

**问题：** Phase 1是否实现信号触发？

**推荐：** Phase 1不实现信号，Phase 2单独实现

**理由：**
- 信号触发涉及事务边界和状态机副作用，需要仔细设计
- Phase 1聚焦API功能验证，信号可以Phase 2单独审查
- 可以通过management command创建通知进行测试

---

## 请Codex审查的问题

1. **用户指令解读：** 用户的新指令是否构成Phase 1授权？还是应该再次提供决策门？

2. **Phase 1范围：** 如果启动Phase 1，是否应该包含信号触发？还是Phase 2单独实现？

3. **实现策略：** 是否应该分Phase 1A/1B/1C/1D四个子阶段？还是一次性完成？

4. **风险评估：** Phase 1实现有哪些潜在风险？如何缓解？

5. **替代方案：** 是否有比Phase 1更有价值的工作方向？

6. **授权边界：** 如果Codex认为需要明确授权，应该如何向用户提供决策门？

---

## 风险评估

**Phase 1主要风险：**

1. **授权边界风险：** 可能违反"Phase 1需明确授权"的共识
   - **缓解：** 请Codex确认用户指令是否构成授权

2. **实现范围膨胀：** 可能在实现过程中增加未计划的功能
   - **缓解：** 严格遵守Phase 1范围，禁止信号和Celery

3. **测试数据不稳定：** 手动创建通知可能导致测试不可重复
   - **缓解：** 实现management command和测试fixture

4. **事务副作用：** 如果实现信号，可能引入事务边界问题
   - **缓解：** Phase 1不实现信号，Phase 2再讨论

5. **客户端冻结边界被破坏：** 可能尝试新增小程序通知页
   - **缓解：** 明确Phase 1只做后端，不改小程序

---

## 时间估算

**Phase 1总时间：** 6-9小时（0.75-1.1天）

| 子阶段 | 任务 | 时间估算 |
|--------|------|----------|
| Phase 1A | 模型 + 迁移 + 模型测试 | 1-2小时 |
| Phase 1B | Serializer + ViewSet + API + URL | 2-3小时 |
| Phase 1C | API测试 + management command | 2-3小时 |
| Phase 1D | 验证 + 文档更新 | 1小时 |

**符合契约预期：** 0.5-1天

---

## 请求

**请Codex审查上述分析，提供批判性反馈，并建议最优策略。**

特别关注：
1. 用户指令是否构成Phase 1授权？
2. Phase 1范围是否合理？
3. 是否有遗漏的风险？
4. 是否有更优的替代方案？

---

**分析完成时间：** 2026-06-01  
**下一步：** 等待Codex审查响应
