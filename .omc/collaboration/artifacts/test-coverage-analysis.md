# 后端测试覆盖分析

**创建时间：** 2026-06-01  
**目的：** 分析现有测试覆盖，识别gap，补充关键测试

## Codex建议的5个重点测试领域

1. **请假申请状态流转**
2. **角色权限边界**
3. **审批人/学生数据隔离**
4. **时区与日期边界**
5. **附件即将引入后的权限模型预留**

## 现有测试文件（10个）

### Applications App (6个测试文件)

1. **test_application_flow.py** - ApplicationFlowTestCase
   - 覆盖：基本申请流程
   - 可能gap：完整状态流转路径

2. **test_constraints.py** - ApplicationConstraintsTestCase
   - 覆盖：约束条件
   - 可能gap：边界条件

3. **test_error_cases.py** - ErrorCasesTestCase
   - 覆盖：错误场景
   - 可能gap：特定错误组合

4. **test_list_permissions.py** - ApplicationListPermissionTest
   - 覆盖：列表权限
   - 可能gap：数据隔离验证

5. **test_p0_fixes.py** - ResubmissionAfterRejectionTest + ApprovalDecisionFilterTest
   - 覆盖：P0修复（重新提交 + 审批过滤）
   - 可能gap：其他P0场景

6. **test_serializer_validation.py** - ApplicationCreateSerializerTest
   - 覆盖：序列化器验证
   - 可能gap：时区边界

### Approvals App (4个测试文件)

7. **test_list_permissions.py** - ApprovalListPermissionTest
   - 覆盖：审批列表权限
   - 可能gap：跨班级数据隔离

8. **test_permissions.py** - ApprovalPermissionsTestCase
   - 覆盖：审批权限
   - 可能gap：边界场景

9. **test_rejection_flow.py** - RejectionFlowTestCase
   - 覆盖：驳回流程
   - 可能gap：驳回后状态

10. **test_state_machine.py** - ApprovalStateMachineTestCase
    - 覆盖：状态机
    - 可能gap：所有状态转换路径

## 初步Gap识别

### 高优先级Gap

1. **数据隔离测试不足**
   - 辅导员A不能看到辅导员B的学生申请
   - 学生A不能看到学生B的申请详情
   - 跨班级审批隔离

2. **时区边界测试不足**
   - 午夜边界（23:59 vs 00:00）
   - 跨时区提交（虽然系统用Asia/Shanghai，但需验证）
   - 日期比较边界

3. **状态流转完整性测试不足**
   - 所有可能的状态转换路径
   - 非法状态转换拒绝
   - 并发状态更新

### 中优先级Gap

4. **附件权限模型预留**
   - 虽然Phase 4C未开始，但可以预留测试框架
   - 附件上传权限（仅学生）
   - 附件查看权限（学生+审批人）

5. **边界条件测试**
   - 最大字段长度
   - 空值处理
   - 特殊字符

## 建议补充测试

### 立即补充（0.5天）

1. **test_data_isolation.py** - 数据隔离测试
   - 学生只能看自己的申请
   - 辅导员只能看自己班级的审批
   - 学工部可以看所有审批

2. **test_timezone_boundaries.py** - 时区边界测试
   - 午夜边界测试
   - 日期比较边界
   - 动态日期生成验证

3. **test_state_transitions.py** - 完整状态转换测试
   - 所有合法路径
   - 所有非法路径拒绝
   - 并发更新处理

### Phase 4C前补充

4. **test_attachment_permissions.py** - 附件权限预留测试
   - 框架测试（当前skip）
   - Phase 4C时取消skip并实现

## 下一步

1. 与Codex讨论补充测试方案
2. 确认优先级和范围
3. 实施测试补充
4. 验证测试通过
