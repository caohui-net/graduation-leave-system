# 审批流程变更需求

**文档编号：** 06-approval-workflow-change-requirement  
**创建时间：** 2026-06-02  
**优先级：** 高（影响业务逻辑）

---

## 1. 需求说明

**用户要求：** "第一审批人学校要求是宿管员，第二审批人是辅导员"

### 当前审批流程

```
学生提交申请 → 辅导员审批 → 院长/学工部审批 → 完成
```

### 目标审批流程

```
学生提交申请 → 宿管员审批 → 辅导员审批 → 完成
```

---

## 2. 影响范围

### 2.1 后端模型（Backend Models）

**文件：** `backend/apps/applications/models.py`

```python
# 当前
class ApplicationStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
    PENDING_DEAN = 'pending_dean', '待学工部审批'
    APPROVED = 'approved', '已通过'
    REJECTED = 'rejected', '已驳回'

# 需要改为
class ApplicationStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
    APPROVED = 'approved', '已通过'
    REJECTED = 'rejected', '已驳回'
```

**文件：** `backend/apps/approvals/models.py`

```python
# 当前
class ApprovalStep(models.TextChoices):
    COUNSELOR = 'counselor', '辅导员'
    DEAN = 'dean', '学工部'

# 需要改为
class ApprovalStep(models.TextChoices):
    DORM_MANAGER = 'dorm_manager', '宿管员'
    COUNSELOR = 'counselor', '辅导员'
```

### 2.2 后端视图和逻辑

**影响文件：**
- `backend/apps/applications/views.py` - 申请提交逻辑（创建第一个审批记录）
- `backend/apps/approvals/views.py` - 审批列表过滤、审批操作
- `backend/apps/approvals/providers.py` - 自动分配审批人逻辑

**关键变更点：**
- 申请提交后创建宿管员审批记录（不是辅导员）
- 宿管员审批通过后创建辅导员审批记录（不是院长）
- 辅导员审批通过后直接完成（不再有第三级审批）

### 2.3 测试代码

**影响文件（至少）：**
- `backend/apps/applications/tests/test_application_flow.py`
- `backend/apps/approvals/tests/test_state_machine.py`
- `backend/apps/approvals/tests/test_permissions.py`
- `backend/apps/approvals/tests/test_rejection_flow.py`

**变更内容：**
- 所有测试中的 `self.counselor` → `self.dorm_manager`（第一审批人）
- 所有测试中的 `self.dean` → `self.counselor`（第二审批人）
- 状态断言从 `pending_counselor` → `pending_dorm_manager`
- 状态断言从 `pending_dean` → `pending_counselor`

### 2.4 前端UI标签

**影响文件：**
- `miniprogram/pages/detail/detail.ts` - 状态文本映射
- `demo-web/index.html` - 硬编码的UI文本
- 所有显示审批步骤、状态的组件

**变更内容：**
- "待辅导员审批" → "待宿管员审批"
- "待院长审批" / "待学工部审批" → "待辅导员审批"
- 审批人角色显示调整

### 2.5 数据库迁移

**潜在影响：**
- 如果数据库中已有 `pending_counselor` 或 `pending_dean` 状态的申请，需要数据迁移脚本
- 如果有现有的审批记录（Approval表），需要更新 `step` 字段

---

## 3. 实施方案

### 3.1 Phase 1: 后端模型和逻辑（必须）

1. 更新 `ApplicationStatus` 枚举
2. 更新 `ApprovalStep` 枚举
3. 更新申请提交逻辑（创建宿管员审批）
4. 更新审批通过逻辑（宿管员→辅导员，辅导员→完成）
5. 更新审批人自动分配逻辑

### 3.2 Phase 2: 测试更新（必须）

1. 更新所有测试用例
2. 验证状态转换正确
3. 验证权限检查正确

### 3.3 Phase 3: 前端UI更新（必须）

1. 更新状态文本映射
2. 更新所有硬编码的审批步骤文本
3. 验证UI显示正确

### 3.4 Phase 4: 数据迁移（如需要）

1. 检查现有数据库是否有待审批记录
2. 编写数据迁移脚本（如需要）
3. 执行迁移

---

## 4. 风险和注意事项

### 4.1 数据一致性

**风险：** 如果数据库中已有待审批记录，状态值可能不匹配

**缓解：**
- 先检查数据库中是否有 `pending_counselor` 或 `pending_dean` 记录
- 如果有，需要数据迁移或清理
- 如果是测试环境，可以直接清理数据库

### 4.2 向后兼容性

**风险：** 旧的状态值可能仍然存在于某些地方

**缓解：**
- 全局搜索所有 `PENDING_COUNSELOR` 和 `PENDING_DEAN` 引用
- 确保所有引用都已更新
- 运行完整测试套件

### 4.3 角色权限

**风险：** 需要确保宿管员角色在系统中存在且配置正确

**缓解：**
- 检查 `User.role` 是否支持 `dorm_manager` 角色
- 更新角色相关的权限检查逻辑
- 创建测试数据时包含宿管员角色

---

## 5. 验收标准

- [ ] 后端模型枚举已更新（ApplicationStatus, ApprovalStep）
- [ ] 申请提交后创建宿管员审批记录
- [ ] 宿管员审批通过后创建辅导员审批记录
- [ ] 辅导员审批通过后申请状态为 `approved`
- [ ] 所有测试通过
- [ ] 前端UI显示正确的审批步骤名称
- [ ] 数据库迁移完成（如需要）

---

## 6. 用户确认（2026-06-02）

**用户反馈：**
1. ✅ 两级审批足够（宿管员→辅导员）
2. ✅ 审批完成后汇总到学工部学生科备案（存档+查询功能，非审批环节）
3. ⚠️ 宿管员角色需要在系统中添加/确认

**关键理解：**
- 审批流程：学生提交 → 宿管员审批 → 辅导员审批 → **完成**
- 学工部角色：不参与审批，仅负责已完成申请的存档和查询
- 实施时需要确认 `User.role` 是否支持 `dorm_manager` 角色

---

## 7. 下一步行动

1. **技术确认：**
   - 检查 `User` 模型是否支持 `dorm_manager` 角色
   - 检查现有数据库是否有待审批记录需要迁移

2. **技术实施：**
   - 阅读当前实现代码，理解状态转换逻辑
   - 制定详细的修改清单
   - 分阶段实施（后端→测试→前端）

3. **测试验证：**
   - 运行完整测试套件
   - 手动测试审批流程
   - 验证UI显示正确

---

**协作模式：** 建议与Codex讨论技术实施方案，确保向后兼容性和数据一致性。
