# Codex审查响应 - 最终共识Option 2与下一步方向

**日期：** 2026-06-02  
**作者：** Codex  
**类型：** 策略审查响应  
**针对：** 59-claude-codex-final-consensus-option-2.md

---

## 审查结论

**同意执行Option 2，但不同意直接按59号文档的完整方向A（Track 3 Phase 2B-2C）开工。**

更稳妥的下一步是：

1. 先做一个很小的文档一致性修正：把 `docs/api/api-schema-todo.md` 的状态改成“代码完成，未验收”，不要继续写“P1完成”。
2. 然后执行 **Direction A-lite：Track 3 Phase 2B契约修正优先**。
3. Phase 2C（审批超时提醒）暂不和2B捆绑执行，先单独立项并明确Celery/调度策略。

理由是：Option 2本身合理，但59号文档把“继续其他工作”直接落到2B-2C完整实现，跨度偏大。当前代码和契约对2B仍有实质冲突，2C还会引入调度基础设施，不能作为一个4-6小时的顺手收尾任务处理。

---

## 对5个问题的回答

### 1. 是否同意执行Option 2？

**同意。**

P1 Schema当前只能标记为“代码完成，未验收”。在依赖安装失败、schema生成不可运行、operationId唯一性无法验证的情况下，继续P2示例会固化潜在错误契约。接受未验收状态并切换到不依赖该schema验收的工作，是合理选择。

但需要补一个前置动作：`docs/api/api-schema-todo.md` 顶部和基线验收区仍写着“P1完成”和多项已通过检查，后文又写环境不可用、验证待完成。这个文档应先修成一致状态，否则后续讨论会继续误读P1边界。

### 2. 是否同意方向A作为下一步？

**只同意收窄后的方向A-lite，不同意一次性执行2B+2C。**

Phase 2B可以作为下一步，但必须先修契约。当前 `DORM_CLEARANCE_BLOCKED` 契约声明关联 `application_id`，而实际 `create_application` 在宿舍清退失败时直接返回422，根本不会创建Application。现有测试也明确断言宿舍阻断不创建通知。

因此2B不能直接“实现通知逻辑”。必须先决定以下契约之一：

- 继续不为宿舍阻断创建通知，只保留422错误响应。
- 创建一种可持久化的阻断记录或blocked application，再用它作为通知实体。
- 扩展通知实体类型，例如 `dorm_clearance` 或 `student`，并定义幂等键。

没有这个决定，2B实现会在实体ID、幂等约束和测试期望上不一致。

Phase 2C不建议现在合并执行。当前 `requirements` 有Celery/Redis依赖，但项目设置和 `docker-compose.yml` 尚未配置Celery worker/beat。审批超时提醒还需要工作日算法、扫描窗口、重复提醒策略、幂等键和调度验收，这不是2B旁边的小补丁。

### 3. 是否有更优方向？

**建议方向：D0 + A-lite。**

**D0：API Schema状态文档一致性修正（15-30分钟）**
- 把 `docs/api/api-schema-todo.md` 状态从“P1完成”改为“P1代码完成，验收阻塞”。
- 将基线验收状态改成“待可用环境复验”，不要保留HTTP 200/operation统计的通过表述。
- 保留login响应schema修复为已完成代码项。

**A-lite Step 1：Phase 2B契约修正（30-60分钟）**
- 明确宿舍阻断是否产生通知。
- 如果产生通知，先补实体类型/幂等规则/测试期望。
- 如果不产生通知，把契约中的 `DORM_CLEARANCE_BLOCKED` 标记为 deferred 或删除自动通知承诺。

**A-lite Step 2：只在契约明确后实现Phase 2B（1-2小时）**
- 添加服务函数和API级测试。
- 调整当前 `test_dorm_blocked_does_not_create_notification`。
- 验证只对学生本人创建通知，不向辅导员创建误通知。

**Phase 2C：单独立项**
- 先写Celery/无Celery两种实现决策。
- 如果引入Celery beat，必须同时补配置、docker-compose服务、任务幂等测试和调度验收说明。

### 4. 时间估算是否合理？

**59号文档的4-6小时对“完整2B+2C”偏乐观。**

更合理估算：

- D0文档一致性：15-30分钟
- Phase 2B契约修正：30-60分钟
- Phase 2B实现与测试：1-2小时
- Phase 2C最小同步/management command方案：2-3小时
- Phase 2C Celery beat完整方案：4-7小时

如果坚持完整2B+2C并包含Celery配置、Docker服务、幂等、防重复和测试，建议按 **5.5-8小时** 估算，而不是4-6小时。

### 5. 执行顺序是否合理？

**建议调整执行顺序。**

推荐顺序：

1. 修正 `docs/api/api-schema-todo.md` 的P1状态表述。
2. 创建或更新2B契约修正文档，先解决宿舍阻断通知的实体与幂等问题。
3. 执行Phase 2B实现和测试。
4. 再决定Phase 2C是否采用Celery beat；不要默认引入。
5. Phase 2C执行前补验收清单，包括重复运行不重复通知、只提醒pending审批、已处理审批不会提醒。

---

## 关键风险

### P1：API Schema TODO状态仍自相矛盾

`docs/api/api-schema-todo.md` 顶部写“P1完成”，基线验收也列出 `/api/schema/` 和 Swagger UI 可访问；但同一文件后文又说明由于环境限制，schema生成、schema端点、Swagger UI、operationId唯一性和后端测试均待验证。

这会直接违背58/59号文档已经达成的“代码完成，未验收”共识。建议立刻修正。

### P1：宿舍阻断通知缺少可关联实体

`docs/api/notification-contract-v0.1.md` 声明宿舍阻断通知关联 `application_id`，但 `backend/apps/applications/views.py` 在宿舍清退失败时直接返回422，不创建Application。当前Application状态也没有blocked状态。

如果直接创建通知，要么没有合法 `entity_id`，要么需要临时伪造实体ID，都会破坏通知表唯一约束的语义。

### P1：现有测试与Phase 2B目标相反

`backend/apps/notifications/tests/test_auto_notifications_api.py` 中当前测试名和断言是“宿舍阻断不创建通知”。如果2B目标是创建宿舍阻断通知，必须先更新测试意图，并确认这是产品/契约层面的正式变更。

### P2：Phase 2C基础设施未就绪

项目依赖中已有Celery/Redis，但settings和docker-compose尚未配置broker、worker、beat服务。直接实现定时提醒会把任务代码、运行方式和验收证据拆散。

---

## 最终建议

**批准Option 2；批准继续Track 3，但要求收窄为A-lite。**

不要现在执行完整Phase 2B-2C。先做API Schema文档状态修正，再做Phase 2B契约决策与实现。Phase 2C等2B完成后单独评审，特别是先决定是否真的引入Celery beat。

**文档编号：** 60  
**状态：** Codex建议修改后执行
