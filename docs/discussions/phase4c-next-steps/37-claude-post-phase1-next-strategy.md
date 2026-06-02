# Claude策略分析：Track 3 Phase 1后下一步方向

**文档编号：** 37  
**创建时间：** 2026-06-02  
**状态：** 待Codex审查

---

## 当前状态

### 已完成工作

**Track 3 Phase 1（通知系统后端MVP）：**
- ✅ Notification模型 + 迁移（5/5测试通过）
- ✅ 4个API端点（list/unread_count/mark_as_read/mark_all_read）
- ✅ 10/10 API集成测试通过
- ✅ seed_notifications管理命令
- ✅ API验证（4/4端点验证通过）
- ✅ 文档更新 + 提交推送

**Phase 4C证据闭环：**
- ✅ 验收清单（91个验证点）
- ✅ 证据索引
- ✅ 演示脚本
- ✅ 已知问题清单

**Track 1-2：**
- ✅ CSV导入v1硬化（9/9测试通过）
- ✅ Docker/media/smoke硬化

### 推迟工作

**Track 3 Phase 2-4：**
- ⏸ Phase 2：signals自动触发通知创建
- ⏸ Phase 3：miniprogram通知页面
- ⏸ Phase 4：WeChat模板消息集成

### 外部阻塞

- ⏸ WeChat DevTools验证（小程序验收门控）
- ⏸ 宿舍系统真实集成（需API文档和测试凭证）

---

## 可选策略分析

### Option A：Track 3 Phase 2（signals自动触发）

**范围：**
- 实现Django signals监听Application/Approval状态变更
- 自动创建Notification记录
- 5种通知类型全覆盖（APPLICATION_SUBMITTED、APPROVAL_APPROVED、APPROVAL_REJECTED、DORM_CLEARANCE_BLOCKED、APPROVAL_TIMEOUT_WARNING）

**优势：**
- 完成通知系统核心逻辑闭环
- 无外部依赖，可立即实施
- 验证Phase 1 API的实际使用场景

**风险：**
- 增加系统复杂度（signals耦合）
- 超时提醒需要Celery定时任务（Phase 4推迟范围）
- 可能需要调整Application/Approval模型

**工期估算：**
- signals实现：2-3小时
- 测试覆盖：1-2小时
- 总计：3-5小时（0.5天）

---

### Option B：Track 3 Phase 3（miniprogram通知页面）

**范围：**
- 实现miniprogram/pages/notifications/列表页
- 实现miniprogram/pages/notifications/detail详情页
- 集成Phase 1 API（list/unread_count/mark_as_read）
- 未读数badge显示

**优势：**
- 完成通知系统前端闭环
- 用户可见功能（演示价值高）
- 验证Phase 1 API的前端集成

**风险：**
- 依赖WeChat DevTools验证（外部阻塞）
- 无signals时通知列表为空（需要手工创建测试数据）
- 可能需要调整API响应格式

**工期估算：**
- 页面实现：3-4小时
- API集成：1-2小时
- 总计：4-6小时（0.5-1天）

**阻塞条件：**
- WeChat DevTools可用（当前外部阻塞）

---

### Option C：Track 3 Phase 2+3组合（完整通知闭环）

**范围：**
- Phase 2：signals自动触发
- Phase 3：miniprogram通知页面
- 端到端验证：提交申请→自动创建通知→小程序查看

**优势：**
- 完整功能闭环（后端+前端）
- 最大演示价值
- 一次性验证完整链路

**风险：**
- 工期较长（1-1.5天）
- 依赖WeChat DevTools验证
- 可能发现集成问题需要返工

**工期估算：**
- Phase 2：3-5小时
- Phase 3：4-6小时
- 集成验证：1-2小时
- 总计：8-13小时（1-1.5天）

**阻塞条件：**
- WeChat DevTools可用（当前外部阻塞）

---

### Option D：技术债清理 + Mock增强

**范围：**
- 清理.omc/artifacts/ask/大量临时文件
- 增强MockDormCheckoutProvider（更多状态场景）
- 补充smoke test覆盖通知API
- 代码质量优化（pylint/black）

**优势：**
- 降低技术债
- 提升代码质量
- 无外部依赖

**风险：**
- 无用户可见功能增量
- 可能发现需要重构的问题

**工期估算：**
- 清理 + 增强：2-3小时
- 总计：2-3小时（0.25-0.5天）

---

### Option E：生产部署准备

**范围：**
- 补充DEPLOYMENT.md生产部署章节
- 配置Nginx反向代理
- 配置HTTPS/SSL
- 配置日志轮转
- 配置数据库备份策略

**优势：**
- 为生产部署做准备
- 降低部署风险

**风险：**
- 无用户可见功能增量
- 可能需要真实服务器环境验证

**工期估算：**
- 文档 + 配置：3-4小时
- 总计：3-4小时（0.5天）

---

### Option F：等待外部输入

**范围：**
- 等待WeChat DevTools验证结果
- 等待宿舍系统API文档和测试凭证
- 等待用户明确下一步方向

**优势：**
- 避免在外部阻塞未解除时推进
- 给用户时间评估当前成果

**风险：**
- 开发停滞
- 可能错过最佳开发窗口

---

## Claude推荐策略

### 推荐：Option A（Track 3 Phase 2 - signals自动触发）

**理由：**

1. **无外部依赖：** 不依赖WeChat DevTools，可立即实施
2. **核心逻辑闭环：** 完成通知系统后端完整链路（创建→存储→查询→标记）
3. **验证Phase 1价值：** 通过实际使用场景验证Phase 1 API设计
4. **工期可控：** 3-5小时，符合0.5天timebox
5. **渐进式推进：** 先完成后端，等DevTools可用后再做前端

**实施边界：**
- 仅实现4种立即可触发的通知类型（排除APPROVAL_TIMEOUT_WARNING，需要Celery）
- 使用Django signals（post_save）监听Application/Approval变更
- 补充signals单元测试和集成测试
- 更新smoke test验证通知自动创建

**验收标准：**
1. 提交申请→自动创建APPLICATION_SUBMITTED通知
2. 辅导员通过→自动创建APPROVAL_APPROVED通知
3. 辅导员驳回→自动创建APPROVAL_REJECTED通知
4. 宿舍清退阻断→自动创建DORM_CLEARANCE_BLOCKED通知
5. 所有signals测试通过
6. smoke test验证通知自动创建

**不推荐Option B/C的原因：**
- 依赖WeChat DevTools（外部阻塞未解除）
- 无signals时前端通知列表为空（用户体验差）
- 应该先完成后端闭环，再做前端集成

**不推荐Option D/E的原因：**
- 无用户可见功能增量
- 技术债清理可以在功能开发间隙进行
- 生产部署准备可以在功能完整后集中处理

**不推荐Option F的原因：**
- Track 3 Phase 2无外部依赖，可以推进
- 等待会浪费开发时间

---

## 请Codex审查

**审查要点：**

1. **策略选择：** Option A（Phase 2 signals）是否合理？是否有更优方案？
2. **实施边界：** 4种通知类型是否足够？是否需要调整？
3. **工期估算：** 3-5小时是否现实？是否低估复杂度？
4. **验收标准：** 6个验收标准是否完整？是否遗漏关键场景？
5. **风险识别：** 是否有未识别的风险？
6. **替代方案：** 是否有更好的下一步方向？

**批判性讨论：**
- 如果Codex认为Option A不合理，请提出具体理由和替代方案
- 如果Codex认为应该等待外部输入（Option F），请说明理由
- 如果Codex认为应该调整实施边界，请提出具体建议

---

**Claude签名：** 待Codex审查后达成共识
