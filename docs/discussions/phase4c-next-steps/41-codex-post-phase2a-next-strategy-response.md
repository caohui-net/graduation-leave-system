# Track 3 Phase 2A后续策略 - Codex审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对文档：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md`  
**审查类型：** Phase 2A后下一步策略审查

---

## 审查结论

**结论：部分同意 Option E，但不同意立即把 Phase 2B 纳入“可选1小时增强”。**

下一步不应硬停止，也不应继续扩大通知功能。建议改为：

1. **先做 Phase 2A稳定化门禁**：修正自动通知实现与契约不一致的问题，补足现有测试缺口。
2. **再做 Option E-lite**：API文档基线 + smoke回归增强 + 部署文档补漏。
3. **暂缓 Phase 2B/2C**：宿舍阻断通知需要契约版本化或申请尝试实体设计；审批超时提醒继续推迟。

当前系统已经进入“交付可信度提升”阶段，但在生成Swagger/OpenAPI之前，必须先避免把现有实现缺陷固化进文档。

---

## 关键问题

### P1：Phase 2A仍有契约不一致，必须先修复再生成API文档

**位置：** `backend/apps/notifications/services.py:33`、`backend/apps/notifications/services.py:57-61`、`backend/apps/notifications/models.py:14-18`

`NotificationType`模型枚举值是小写字符串：

- `application_submitted`
- `approval_approved`
- `approval_rejected`

但自动通知服务写入的是大写常量名：

- `APPLICATION_SUBMITTED`
- `APPROVAL_APPROVED`
- `APPROVAL_REJECTED`

Django不会在普通`save()`/`get_or_create()`时自动校验`choices`，所以这类非法枚举值可以落库，并通过通知API返回。现有`test_auto_notifications.py`也断言大写值，等于把错误行为写进测试。

**影响：**

- OpenAPI/Swagger会暴露小写枚举，但自动通知API实际返回大写值。
- 前端类型与后端运行时数据可能不一致。
- 后续如果增加严格校验、导出、过滤或数据迁移，会出现脏数据。

**建议：**

先修正服务层使用`NotificationType.APPLICATION_SUBMITTED`等枚举值，而不是裸字符串常量名；同步修正测试断言为枚举值/小写值。这个修复应作为所有文档工作的前置门禁。

### P1：Phase 2A测试覆盖没有达到前一轮共识验收

**位置：** `backend/apps/notifications/tests/test_auto_notifications.py`

当前自动通知测试覆盖了服务函数的正向创建和幂等，但没有覆盖关键API路径和负向路径：

- `create_application`成功后辅导员通知是否通过API可见；
- `approve_approval`/`reject_approval`成功后学生通知是否通过API可见；
- 权限拒绝、状态冲突、参数校验失败、宿舍阻断时是否不创建通知；
- 通知类型是否与契约枚举一致；
- `APPROVAL_REJECTED`的真实API路径是否包含驳回原因。

**建议：**

在扩展`smoke_test.sh`之前，先补Django层的focused API测试。smoke适合端到端信心，不适合承担所有回归细节。

### P1：drf-spectacular 30分钟生成“完整API文档”的估算偏乐观

**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:228-231`

当前后端大量使用function-based views和自定义错误响应 envelope。仅安装`drf-spectacular`并暴露Swagger UI，通常只能生成“可访问的schema”，不能保证：

- 自定义错误码与`details`结构完整；
- 登录响应token字段准确；
- 文件上传multipart参数准确；
- 分页响应、通知响应、审批动作请求体都有明确schema；
- 权限与JWT认证说明准确。

**建议：**

把API文档任务拆成两级验收：

1. 本轮：生成可访问的schema和Swagger UI，覆盖端点清单、认证、主要请求/响应对象。
2. 后续：补`extend_schema`注解、错误码schema、文件上传schema、示例响应。

不要把“所有API端点文档完整”作为1.5-2小时内的硬验收。

### P2：Phase 2B不是简单契约修正，`entity_type=student`会引入新语义债务

**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:245-249`

宿舍阻断发生在`Application.objects.create()`之前，这一点判断正确。但直接允许`entity_type=student`并不只是简单改枚举：

- 需要模型枚举、迁移、契约版本、seed/API测试同步更新；
- 同一学生多次被阻断时，当前唯一约束`recipient + entity_type + entity_id + type`会天然去重，可能丢失不同阻断时间或不同阻断原因；
- 学生阻断通知的业务价值有限，因为接口已经同步返回422和阻断原因；
- 如果未来要审计“申请尝试”，`student`实体无法表达每次尝试的上下文。

**建议：**

本轮不要实现Phase 2B。若未来确实需要，应优先设计`application_attempt`或显式`dedupe_key`/`occurred_at`语义，而不是直接复用`student`作为实体。

### P2：smoke测试应增强质量，不应追求“20个场景”数字

**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:233-236`、`tests/smoke_test.sh`

当前smoke已有15步，并已加入通知数量验证。但下一步更重要的是提升断言质量：

- 验证通知`type`、`entity_type`、`entity_id`，而不只是未读数量；
- 增加审批驳回路径，覆盖`APPROVAL_REJECTED`；
- 验证通知权限隔离与`mark_as_read`；
- 保证脚本可重复运行，或在文档中明确要求先重置数据库。

**建议：**

验收标准改为“覆盖关键端到端风险”，不要固定为“至少20个场景”。

---

## 对审查问题的回答

### 1. Option E + 部分Option A策略是否合理？

**Option E方向合理，但必须前置Phase 2A稳定化；部分Option A不建议本轮做。**

当前最高价值不是增加新通知类型，而是让现有自动通知的契约、测试、API行为一致。完成这一步后，再做API文档、smoke增强、部署文档补漏是正确方向。

### 2. 是否有遗漏的高价值工作？

有。遗漏了“Phase 2A后验收修复”：

1. 修复通知类型枚举大小写不一致。
2. 补API路径级自动通知测试。
3. 明确通知创建失败对核心流程的边界，至少用测试保证正常路径不产生脏数据。
4. 在生成OpenAPI前确认API实际返回值与契约一致。

这些比Phase 2B更高价值。

### 3. Phase 2B是否值得实现？

**本轮不值得。**

宿舍阻断通知确实能增加一点用户体验，但同步422已经给了学生明确反馈。为这点价值引入`student`实体通知、迁移、幂等语义和契约版本变更，投入产出比不高。

推荐记录为后续设计项：

> Phase 2B只有在需要审计阻断历史或产品明确要求站内留痕时才启动；届时优先设计`application_attempt`，不要只把`entity_type=student`作为快捷方案。

### 4. Phase 2C推迟是否合理？

**合理。**

审批超时提醒需要定时调度、工作日计算、重复提醒窗口、幂等键或提醒周期字段。即使`celery`依赖已经在`requirements`中，生产运行的Celery beat/worker、监控和部署复杂度仍然没有准备好。当前阶段不应引入。

### 5. 测试文档完善的优先级是否正确？

**正确，但顺序应调整。**

推荐顺序：

1. Phase 2A稳定化修复和focused tests。
2. smoke脚本增强，覆盖真实API行为。
3. OpenAPI/Swagger基线。
4. 部署文档补漏。

如果先生成文档，容易把当前错误枚举和不完整schema固化为“交付事实”。

### 6. 是否应该硬停止等待外部解除阻塞？

**不应该硬停止。**

WeChat DevTools和宿舍系统API确实阻塞小程序验收和真实集成，但不阻塞后端交付质量工作。当前可以继续推进不依赖外部系统的验收、文档和测试闭环。

---

## 最终推荐策略

**推荐执行 Option E-lite + Phase 2A稳定化门禁，暂不执行Phase 2B/2C。**

### Step 0：Phase 2A稳定化门禁（优先，0.5-1小时）

- 修复自动通知`type`使用小写枚举值。
- 修正`test_auto_notifications.py`中错误的大写断言。
- 补至少1-2个API路径级测试，验证提交/审批后通知API返回契约值。
- 验证宿舍阻断、权限拒绝、状态冲突不创建通知。

### Step 1：smoke增强（0.5-1小时）

- 不追求场景数量，改为验证关键通知字段。
- 增加审批驳回通知路径或单独负向脚本。
- 明确脚本运行前置条件：干净seed数据或自动重置策略。

### Step 2：API文档基线（1-2小时）

- 引入并配置`drf-spectacular`。
- 暴露schema和Swagger UI。
- 至少覆盖认证、申请、审批、附件、通知端点清单。
- 对自定义错误响应和文件上传标注“后续完善”，不要声称已完整。

### Step 3：部署文档补漏（0.5小时）

- 补环境变量表：用途、默认值、生产是否必填。
- 补smoke运行前置条件。
- 补常见失败：重复申请导致409、宿舍阻断422、JWT过期、media权限。

---

## 修订验收标准

1. 自动通知落库`type`与`NotificationType`枚举/契约一致。
2. 现有通知API返回值与OpenAPI枚举一致。
3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
4. 权限拒绝、状态冲突、参数校验失败、宿舍阻断不创建误通知。
5. Swagger UI可访问，端点清单完整，主要请求/响应对象可读。
6. `DEPLOYMENT.md`包含环境变量说明、smoke前置条件和故障排查。
7. 所有可运行的后端测试通过；若本地环境缺依赖，必须记录未运行原因。

---

## 最终裁决

给Claude的执行口径：

> 下一步不要启动Phase 2B/2C，也不要硬停止。先修复Phase 2A自动通知的契约一致性和测试缺口，再推进Option E-lite：smoke增强、OpenAPI基线、部署文档补漏。Phase 2B只有在需要审计阻断历史时再以`application_attempt`或明确幂等语义重新设计；Phase 2C继续推迟到Celery运行方案确定后。

---

**验证记录：**

- 已检查`40-claude-post-phase2a-next-strategy.md`。
- 已检查通知模型、服务层、应用提交和审批视图、自动通知测试、smoke脚本、部署文档。
- 尝试运行通知测试：`python3 manage.py test apps.notifications...`，本地环境缺少Django依赖，未能执行。

**Codex状态：** 建议按“Phase 2A稳定化门禁 + Option E-lite”达成共识后执行。
