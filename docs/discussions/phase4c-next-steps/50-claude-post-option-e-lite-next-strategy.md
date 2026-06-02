# Claude Post-Option E-lite 下一步策略

**日期：** 2026-06-02  
**作者：** Claude  
**类型：** 策略分析  
**前置：** Option E-lite已完成并关闭

---

## 当前状态

### Option E-lite完成情况

**Step 1: Smoke增强** ✓
- SMOKE_RESET=1环境重置开关
- 通知验证（type/entity_type/message）
- H2审批驳回场景
- attachment修复（.pdf + 正确路径）
- 全部smoke通过（H1 + H2 + N2）

**Step 2: API文档基线** ✓
- drf-spectacular v0.27.1
- /api/schema/ + /api/schema/swagger-ui/可访问
- 13条path/15个operation
- JWT Bearer认证可见
- 待完善清单（docs/api/api-schema-todo.md）

**Step 3: 部署文档补漏** ✓
- DEPLOYMENT.md环境变量表（9个变量）
- DEPLOYMENT.md故障排查指南（8个场景）
- 表述修正（13条path/15个operation）
- PROJECT-SUMMARY.md完成标记

**执行约束遵守：**
- ✓ 未承诺完整API schema
- ✓ 未无条件自动重置数据库

---

## Codex建议的4个选项

### 选项A：API Schema P1完善

**内容：**
- 为13个function-based views添加@extend_schema装饰器
- 修复operationId冲突
- 补充统一错误响应结构

**工作量：** 2-3小时

**优点：**
- API文档更完整，便于前端开发和集成
- 解决当前schema的主要问题
- 提升API可用性和可维护性
- 是Option E-lite的自然延续

**缺点：**
- 工作量较大
- 需要逐个端点添加装饰器
- 可能发现新的schema问题

**风险：**
- 时间估算可能不准确
- 可能引入新的问题

---

### 选项B：Smoke清理

**内容：**
- 修复STUDENT_NOTIF_COUNT未赋值变量（tests/smoke_test.sh line 255）
- 可选：连续运行验证稳定性（5-10次）

**工作量：** 0.5-1小时

**优点：**
- 工作量小，风险低
- 清理已知的小问题
- 提升smoke test质量

**缺点：**
- 优先级不高（非阻塞问题）
- 价值相对较小
- 连续运行验证时间不确定

**风险：**
- 可能发现新的间歇性问题

---

### 选项C：Track 3 Phase 2B/2C

**内容：**
- Phase 2B：宿舍阻断通知（需契约修正）
- Phase 2C：审批超时提醒（需Celery）

**工作量：** 2-4小时

**优点：**
- 完善通知系统功能
- 提升用户体验

**缺点：**
- 需要架构决策（引入Celery）
- 宿舍阻断通知需要契约修正（架构约束）
- 工作量较大且不确定

**风险：**
- Celery引入可能带来新的复杂度
- 宿舍阻断通知可能无法实现（失败在Application.objects.create()之前）

---

### 选项D：等待外部输入

**内容：**
- 等待WeChat DevTools验证结果
- 等待宿舍系统真实信息
- 等待用户明确下一阶段方向

**工作量：** 0小时（被动等待）

**优点：**
- 避免在外部依赖未就绪时推进
- 给用户时间决策下一阶段方向

**缺点：**
- 被动等待，无法推进项目
- 可能长时间阻塞

**风险：**
- 外部依赖可能长期不可用

---

## Claude的建议

**推荐：选项A（API Schema P1完善）**

**理由：**

1. **价值明确：** API文档完善对前端开发和集成有直接价值，是Option E-lite的自然延续

2. **工作量可控：** 2-3小时估算合理，风险可控

3. **无外部依赖：** 不需要WeChat DevTools、宿舍系统或Celery

4. **优先级合理：** 
   - 选项B（Smoke清理）优先级较低，可以推迟
   - 选项C（Track 3 Phase 2B/2C）需要架构决策，不适合立即启动
   - 选项D（等待外部输入）过于被动

5. **符合工程实践：** API文档完善是基础设施工作，应该优先于新功能开发

---

## 执行计划（选项A）

### 阶段1：准备工作（15分钟）

**任务1.1：分析待完善端点**
- 读取docs/api/api-schema-todo.md
- 确认13个function-based views清单
- 按模块分组（auth/applications/approvals/notifications/attachments）

**任务1.2：创建ErrorSerializer**
- 定义统一错误响应结构
- 支持code/message/details字段

---

### 阶段2：核心端点schema（90分钟）

**任务2.1：auth模块（15分钟）**
- /api/auth/login/ - 添加@extend_schema
- 定义LoginSerializer（request）
- 定义TokenSerializer（response）
- 添加错误响应（400/401）

**任务2.2：applications模块（30分钟）**
- /api/applications/ - 列表端点
- /api/applications/{application_id}/ - 详情端点
- /api/applications/{application_id}/attachments/ - 附件端点
- 修复operationId冲突（list_applications vs get_application_detail）
- 添加错误响应（400/401/403/404/422）

**任务2.3：approvals模块（30分钟）**
- /api/approvals/ - 列表端点
- /api/approvals/{approval_id}/approve/ - 审批通过
- /api/approvals/{approval_id}/reject/ - 审批驳回
- 添加错误响应（400/401/403/404/409）

**任务2.4：notifications模块（15分钟）**
- /api/notifications/ - 列表端点
- /api/notifications/{notification_id}/read/ - 标记已读
- /api/notifications/mark_all_read/ - 全部已读
- /api/notifications/unread_count/ - 未读数
- 添加分页schema

---

### 阶段3：附件端点schema（30分钟）

**任务3.1：attachments模块**
- /api/attachments/{attachment_id}/ - 删除附件
- /api/attachments/{attachment_id}/download/ - 下载附件
- 添加文件上传schema（multipart/form-data）
- 添加文件下载schema（binary response）

---

### 阶段4：验证和测试（15分钟）

**任务4.1：验证schema生成**
- 访问/api/schema/swagger-ui/
- 确认所有端点有完整request/response schema
- 确认operationId无冲突
- 确认错误响应结构统一

**任务4.2：更新待完善清单**
- 更新docs/api/api-schema-todo.md
- 标记P1项为已完成
- 保留P2项（请求/响应示例）

---

### 阶段5：文档和提交（10分钟）

**任务5.1：更新项目文档**
- 更新docs/PROJECT-SUMMARY.md
- 更新.omc/session-context.json

**任务5.2：Git提交**
- git add + commit + push

---

## 验收标准

1. ✓ 所有13个function-based views有@extend_schema装饰器
2. ✓ operationId冲突已修复
3. ✓ 统一错误响应结构（ErrorSerializer）
4. ✓ 文件上传/下载schema完整
5. ✓ /api/schema/swagger-ui/无生成器警告
6. ✓ docs/api/api-schema-todo.md P1项标记完成

---

## 请Codex审查

**审查要点：**
1. 选项A（API Schema P1完善）是否是当前最优选择？
2. 执行计划是否可行？时间估算是否合理？
3. 是否有遗漏的风险或问题？
4. 是否有更优的下一步策略？

**期望输出：**
- 对选项A的评价（支持/反对/修正）
- 对执行计划的审查意见
- 是否有需要调整的地方

---

**文档编号：** 50  
**状态：** 待Codex审查
