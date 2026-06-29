# 多辅导员审批功能测试计划

**环境**: 196 Staging (http://172.17.12.196:17787)  
**测试时间**: 2026-06-29  
**测试人员**: Claude AI

## 前置条件

1. 数据库中需要有：
   - 学生账号（不同学院，部分有class_id，部分无）
   - 多个辅导员（同一学院至少2人）
2. Staging环境代码已同步
3. 数据库迁移已执行（0005_alter_approval_decision包含CANCELLED状态）

## 测试场景

### 场景1: class_id唯一匹配

**目标**: 验证当学生有class_id时，优先匹配唯一辅导员

**步骤**:
1. 查询一个有class_id的学生
2. 学生提交留校申请
3. 查询生成的审批记录
4. 验证只创建了1条辅导员审批记录
5. 验证审批记录的approver是class_id对应的辅导员

**预期结果**:
- 只创建1条COUNSELOR审批
- approver.user_id == student.class_id

---

### 场景2: 学院多辅导员匹配

**目标**: 验证当class_id匹配失败时，按学院匹配所有辅导员

**步骤**:
1. 找一个class_id为null或无效的学生，且该学生所在学院有多个辅导员
2. 学生提交留校申请
3. 查询生成的审批记录
4. 验证创建了多条辅导员审批记录（数量==该学院辅导员数）
5. 验证所有审批记录的approver都属于该学院

**预期结果**:
- 创建N条COUNSELOR审批（N==学院辅导员数）
- 所有approver.department == student.department
- 所有审批记录的decision == PENDING

---

### 场景3: 级联取消 - 审批通过

**目标**: 验证任一辅导员通过后，其他待审批自动取消

**步骤**:
1. 使用场景2的申请（多辅导员待审批）
2. 辅导员A审批通过
3. 查询该申请的所有辅导员审批记录
4. 验证辅导员A的审批为APPROVED
5. 验证其他辅导员的审批为CANCELLED

**预期结果**:
- 1条APPROVED（辅导员A）
- N-1条CANCELLED（其他辅导员）
- CANCELLED记录的comment包含"已由其他辅导员完成审批"

---

### 场景4: 级联取消 - 审批驳回

**目标**: 验证任一辅导员驳回后，其他待审批自动取消

**步骤**:
1. 创建新申请（多辅导员待审批）
2. 辅导员B驳回申请
3. 查询该申请的所有辅导员审批记录
4. 验证辅导员B的审批为REJECTED
5. 验证其他辅导员的审批为CANCELLED
6. 验证申请状态为REJECTED

**预期结果**:
- 1条REJECTED（辅导员B）
- N-1条CANCELLED（其他辅导员）
- CANCELLED记录的comment包含"申请已被驳回"
- application.status == REJECTED

---

### 场景5: 辅导员列表过滤

**目标**: 验证辅导员C看不到已取消的审批

**步骤**:
1. 使用场景3或4的申请（已有CANCELLED记录）
2. 以辅导员C身份调用GET /api/approvals/?decision=pending
3. 验证返回的列表中不包含该申请的审批记录

**预期结果**:
- 辅导员C的待审批列表不包含已CANCELLED的记录
- 只返回decision=PENDING的记录

---

### 场景6: 申请状态流转

**目标**: 验证审批完成后申请状态正确更新

**步骤**:
1. 学生提交留校申请（多辅导员）
2. 验证申请状态为PENDING_COUNSELOR
3. 任一辅导员审批通过
4. 验证申请状态为APPROVED

**预期结果**:
- 提交后: application.status == PENDING_COUNSELOR
- 审批通过后: application.status == APPROVED

---

## 执行方式

**方式1: browser-harness自动化测试** (推荐)
- 适合端到端业务流程测试
- 需要CDP端口：9222

**方式2: API直接测试**
- 适合快速验证后端逻辑
- 使用curl或Python脚本

**方式3: 手动UI测试**
- 适合最终验收
- 访问 http://172.17.12.196:17788

---

## 数据准备SQL

```sql
-- 查询测试数据
-- 1. 找一个有class_id的学生
SELECT user_id, name, class_id, department FROM users 
WHERE role='student' AND class_id IS NOT NULL LIMIT 1;

-- 2. 找一个学院有多个辅导员的学生
SELECT s.user_id, s.name, s.department, COUNT(c.user_id) as counselor_count
FROM users s
LEFT JOIN users c ON c.department = s.department AND c.role='counselor' AND c.active=true
WHERE s.role='student' AND s.class_id IS NULL
GROUP BY s.user_id, s.name, s.department
HAVING COUNT(c.user_id) >= 2
LIMIT 1;

-- 3. 查询某学院的所有辅导员
SELECT user_id, name, department FROM users
WHERE role='counselor' AND department='计算机学院' AND active=true;
```

---

## 验证清单

- [ ] 场景1: class_id唯一匹配
- [ ] 场景2: 学院多辅导员匹配
- [ ] 场景3: 级联取消 - 审批通过
- [ ] 场景4: 级联取消 - 审批驳回
- [ ] 场景5: 辅导员列表过滤
- [ ] 场景6: 申请状态流转

---

## 测试结果记录

测试执行完成后，在此记录结果和发现的问题。
