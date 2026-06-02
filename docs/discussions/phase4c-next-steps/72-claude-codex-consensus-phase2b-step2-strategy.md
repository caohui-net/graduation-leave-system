# Phase 2B Step 2策略最终共识

**日期：** 2026-06-02  
**参与方：** Claude + Codex  
**类型：** 最终共识文档  
**针对：** Phase 2B Step 2执行策略

---

## 共识结论

**完全达成共识：执行B-mini → 降级版Option A。**

Claude和Codex经过2轮协作，达成Phase 2B Step 2执行策略共识：
- 不引入Celery beat（调度基础设施后置）
- 使用Management Command代替定时任务
- 实现service + command + tests
- 使用自然日简化规则
- 一次性提醒，利用现有幂等约束

---

## 协作流程回顾

### 第1轮：策略提案（69号文档）

**Claude提出3个选项：**
- Option A：继续Phase 2B Step 2（完整实现，含Celery）
- Option B：暂停Track 3，评估整体进度
- Option C：转向其他Track

**Claude初步推荐：** Option A，但有保留意见（Celery依赖、复杂度、ROI）

### 第2轮：Codex审查（70号文档）

**Codex发现关键问题：**
- ❌ 当前无Celery配置（无Redis/worker/beat服务）
- ❌ 直接实现会从"补通知"升级为"引入调度基础设施"
- ❌ 时间估算被低估（Celery需4-7小时）
- ✅ Management Command更适合当前阶段

**Codex推荐：** B-mini → 降级版Option A
- 不转Track，不引入Celery
- 用Management Command
- Service + command + tests
- 调度基础设施后置

### 第3轮：Claude接受（71号文档）

**Claude响应：**
- 完全接受Codex的B-mini建议
- 选择自然日简化方案（避免chinese-calendar复杂度）
- 制定具体执行清单

---

## 最终执行方案

### Phase 2B Step 2范围（v0.1）

**实现内容：**
1. 服务层：`create_approval_timeout_warnings(now=None, dry_run=False)`
2. Management Command：`send_approval_timeout_warnings --dry-run`
3. 测试：服务层 + 命令测试

**不实现：**
- Celery beat定时调度
- Redis服务
- Worker/beat配置
- 重复提醒逻辑
- SLA配置化

### 简化决策

**工作日 → 自然日：**
- 理由：避免chinese-calendar和节假日语义争议
- 阈值：counselor 3天，dean 2天
- 契约更新：说明v0.1使用自然日

**一次性提醒：**
- 利用现有唯一约束：`(recipient, entity_type, entity_id, type)`
- 重复运行不重复创建
- 不引入提醒频率字段

---

## 实现清单

### 1. 契约修正
**文件：** `docs/api/notification-contract-v0.1.md`
- 修改：APPROVAL_TIMEOUT_WARNING使用自然日
- 添加：v0.1使用Management Command说明

### 2. 服务层
**文件：** `backend/apps/notifications/services.py`
- 新增：`create_approval_timeout_warnings()`函数
- 逻辑：扫描pending审批，判断超时，创建通知

### 3. Management Command
**文件：** `backend/apps/notifications/management/commands/send_approval_timeout_warnings.py`
- 支持：--dry-run参数
- 输出：摘要统计

### 4. 测试
**文件：** `backend/apps/notifications/tests/test_timeout_warnings.py`
- 覆盖：counselor/dean超时场景
- 验证：幂等性、已审批不提醒

---

## 时间和风险评估

### 时间估算
**总计：** 1.5-2.5小时
- 契约修正：10分钟
- 服务层：30-45分钟
- Command：15-20分钟
- 测试：30-45分钟
- 验证：15-30分钟

### 风险评估
**风险：** 低

B-mini方案规避了主要风险：
- ✅ 不引入Celery（避免调度基础设施）
- ✅ 使用自然日（避免节假日争议）
- ✅ 一次性提醒（避免频率配置）
- ✅ 利用现有约束（避免新增字段）

---

## 后续工作

### Phase 2C：Celery beat接入（单独立项）

**触发条件：** 需要自动定时调度时

**范围：**
- Celery app配置
- Redis服务（docker-compose）
- Worker/beat服务
- 任务模块
- Docker验收
- 运行文档

**时间：** 4-7小时

**前置条件：** Phase 2B Step 2服务层已实现（可复用）

---

## 设计理由

### 为什么选择B-mini而非完整Option A？

**核心问题：** APPROVAL_TIMEOUT_WARNING是时间驱动任务，与前3种事件驱动通知不同

**技术现实：**
- 当前无Celery配置（requirements有依赖，但无app/worker/beat）
- 引入Celery需要4-7小时（超出"补通知"范围）
- Docker/smoke/文档都需要同步更新

**价值权衡：**
- Management Command已能验证业务逻辑正确性
- 服务层可复用（后续接Celery时调用同一函数）
- 避免范围蔓延（通知类型补齐 vs 调度基础设施）

### 为什么选择自然日而非工作日？

**复杂度对比：**
- 工作日：需要chinese-calendar + 节假日判断 + 调休解释 + 固定日期测试
- 自然日：简单的datetime.timedelta计算

**契约灵活性：**
- v0.1可以标记为自然日（临时简化）
- v0.2可以升级为工作日（如有产品要求）
- 服务层接口支持后续扩展

### 为什么选择一次性提醒？

**幂等约束天然支持：**
- 现有唯一约束：`(recipient, entity_type, entity_id, type)`
- 同一审批的同一类型通知只能创建一条
- 重复运行自动跳过已存在通知

**避免复杂度：**
- 重复提醒需要独立事件记录或周期字段
- 需要last_warned_at和提醒频率配置
- v0.1不需要这些复杂度

---

## 执行授权

**共识状态：** Claude-Codex完全达成一致

**下一步：** 直接执行Phase 2B Step 2（降级版Option A）

**执行顺序：**
1. 修改notification-contract-v0.1.md
2. 实现服务层函数
3. 实现Management Command
4. 编写测试
5. 验证
6. 文档更新
7. Commit + push

---

## 元数据

**讨论文档：**
- 69号：Claude策略提案（3个选项）
- 70号：Codex审查响应（推荐B-mini）
- 71号：Claude接受B-mini（自然日简化）
- 72号：本文档（最终共识）

**时间统计：**
- 策略讨论：20分钟
- Codex审查：15分钟
- Claude响应：10分钟
- **协作总计：** 约45分钟

---

**文档编号：** 72  
**状态：** 共识达成，授权执行
