# 留校审批支持多辅导员匹配和级联取消

**创建时间：** 2026-06-29  
**完成时间：** 2026-06-29  
**状态：** completed

## 需求

留校审批流程改造，参考宿管员的多人审批逻辑：

1. **辅导员匹配逻辑**：
   - 优先通过 `class_id` 尝试唯一匹配
   - 失败则通过学院（`department`）匹配该学院所有辅导员

2. **多人审批支持**：
   - 一个申请可创建多个辅导员审批记录
   - 任一辅导员审批完成即可进入下一环节

3. **级联取消机制**：
   - 任一辅导员审批完成后，自动取消其他待审批的辅导员审批
   - 其他辅导员的列表中不再显示此申请

4. **与宿管员逻辑保持一致**

## 实施步骤

### 1. 修改辅导员匹配逻辑
**文件：** `backend/apps/applications/views.py`

- [ ] 优先通过 `class_id` 匹配（保留现有逻辑）
- [ ] 如果 `class_id` 匹配失败，通过 `student.department` 匹配所有该学院的辅导员
- [ ] 返回辅导员列表（而不是单个辅导员）

### 2. 修改审批创建逻辑
**文件：** `backend/apps/applications/views.py`

- [ ] 将辅导员审批创建改为循环创建（参考宿管员逻辑）
- [ ] 为每个匹配到的辅导员创建一条审批记录

### 3. 实现级联取消逻辑
**文件：** `backend/apps/approvals/views.py`

- [ ] 在 `approve_approval` 函数中，当辅导员审批完成时：
  - 查找同一申请的其他辅导员待审批记录
  - 将其状态设置为"已取消"或标记为不可见
- [ ] 在 `reject_approval` 函数中同样处理

### 4. 修改列表查询逻辑
**文件：** `backend/apps/approvals/views.py`

- [ ] `list_approvals` 函数中过滤掉已取消的审批记录
- [ ] 确保辅导员只能看到自己的待审批和已处理的记录

### 5. 测试验证

- [ ] 测试 `class_id` 唯一匹配场景
- [ ] 测试学院多辅导员匹配场景
- [ ] 测试任一辅导员审批后，其他辅导员看不到记录
- [ ] 测试审批流程完整性

## 技术细节

### 辅导员匹配逻辑（参考宿管员）

```python
# 当前宿管员匹配逻辑（lines 181-213）
dorm_managers = []
if building:
    dorm_managers = list(User.objects.filter(
        role=UserRole.DORM_MANAGER,
        building=building,
        active=True
    ))

# 新的辅导员匹配逻辑
counselors = []
if user.class_id:
    # 优先class_id匹配
    counselor = User.objects.filter(
        role=UserRole.COUNSELOR,
        user_id=user.class_id,
        active=True
    ).first()
    if counselor:
        counselors = [counselor]

if not counselors and user.department:
    # 失败则学院匹配
    counselors = list(User.objects.filter(
        role=UserRole.COUNSELOR,
        department=user.department,
        active=True
    ))
```

### 审批级联取消逻辑

```python
# 在approve_approval或reject_approval中
if approval.step == ApprovalStep.COUNSELOR:
    # 取消同一申请的其他辅导员待审批
    Approval.objects.filter(
        application=approval.application,
        step=ApprovalStep.COUNSELOR,
        decision=ApprovalDecision.PENDING
    ).exclude(
        approval_id=approval.approval_id
    ).update(
        decision=ApprovalDecision.CANCELLED,  # 需要添加CANCELLED状态
        decided_at=timezone.now()
    )
```

## 注意事项

1. 需要在 `ApprovalDecision` 枚举中添加 `CANCELLED` 状态
2. 列表查询需要过滤 `CANCELLED` 状态的审批
3. 保持与宿管员审批逻辑的一致性
4. 确保通知逻辑正确处理多辅导员场景

## 验证清单

- [ ] class_id唯一匹配正常工作
- [ ] 学院多辅导员匹配正常工作
- [ ] 任一审批完成后其他待审批自动取消
- [ ] 其他辅导员看不到已处理的申请
- [ ] 申请状态正确流转
- [ ] 通知正确发送
