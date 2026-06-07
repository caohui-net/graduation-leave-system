# Phase 1 执行计划提案 - Claude

**日期:** 2026-05-30  
**前置条件:** Phase 0完成 ✓  
**目标:** 实现最小化列表接口

---

## 一、Phase 1 目标

实现两个基础列表接口：
1. `GET /api/applications/` - 申请列表
2. `GET /api/approvals/` - 审批列表

**范围限定:**
- 仅实现基础列表功能（无分页、无过滤）
- 返回当前用户可见的记录
- 遵循现有权限模型

---

## 二、实现方案

### 2.1 GET /api/applications/

**URL:** `/api/applications/`  
**Method:** GET  
**权限:** 已认证用户

**业务逻辑:**
- 学生: 返回自己的申请列表
- 辅导员: 返回所负责班级学生的申请列表
- 学工部: 返回所有申请列表

**响应格式:**
```json
{
  "applications": [
    {
      "application_id": "app_xxx",
      "student_id": "2020001",
      "student_name": "张三",
      "class_id": "CS2020-01",
      "reason": "毕业离校",
      "leave_date": "2024-06-30",
      "status": "pending_counselor",
      "created_at": "2024-05-20T10:00:00Z",
      "updated_at": "2024-05-20T10:00:00Z"
    }
  ]
}
```

**实现位置:**
- 文件: `apps/applications/views.py`
- 函数: `list_applications` (新增)
- URL: 在 `apps/applications/urls.py` 中添加

### 2.2 GET /api/approvals/

**URL:** `/api/approvals/`  
**Method:** GET  
**权限:** 已认证用户

**业务逻辑:**
- 学生: 返回自己申请的所有审批记录
- 辅导员: 返回待自己审批的记录（step='counselor', decision='pending'）
- 学工部: 返回待自己审批的记录（step='dean', decision='pending'）

**响应格式:**
```json
{
  "approvals": [
    {
      "approval_id": "apv_xxx",
      "application_id": "app_xxx",
      "step": "counselor",
      "approver_id": "T001",
      "approver_name": "李老师",
      "decision": "pending",
      "comment": null,
      "decided_at": null,
      "created_at": "2024-05-20T10:00:00Z"
    }
  ]
}
```

**实现位置:**
- 文件: `apps/approvals/views.py`
- 函数: `list_approvals` (新增)
- URL: 在 `apps/approvals/urls.py` 中添加

---

## 三、实现步骤

### Step 1: 实现 list_applications 视图

1. 在 `apps/applications/views.py` 添加 `list_applications` 函数
2. 实现权限过滤逻辑
3. 添加 URL 路由

### Step 2: 实现 list_approvals 视图

1. 在 `apps/approvals/views.py` 添加 `list_approvals` 函数
2. 实现权限过滤逻辑
3. 添加 URL 路由

### Step 3: 编写测试

1. 创建 `apps/applications/tests/test_list_applications.py`
2. 创建 `apps/approvals/tests/test_list_approvals.py`
3. 测试各角色的权限隔离

### Step 4: 验证

1. 运行新增测试
2. 运行所有测试确保无回归
3. 手动测试接口

---

## 四、时间估算

- Step 1: 30分钟（实现 + URL配置）
- Step 2: 30分钟（实现 + URL配置）
- Step 3: 45分钟（编写测试）
- Step 4: 15分钟（验证）

**总计:** 2小时

---

## 五、风险评估

### R1: 权限逻辑复杂度
- **概率:** 中
- **影响:** 实现时间可能超出估算
- **缓解:** 参考现有 `get_application` 的权限逻辑

### R2: 测试覆盖不足
- **概率:** 低
- **影响:** 权限隔离漏洞
- **缓解:** 为每个角色编写独立测试用例

### R3: 与现有代码冲突
- **概率:** 低
- **影响:** 需要调整现有代码
- **缓解:** 先运行现有测试确保基线稳定

---

## 六、待Codex审查的问题

1. **列表接口是否应该包含关联数据?**
   - 例如: applications列表是否应该包含approvals数组?
   - 建议: Phase 1保持简单，不包含关联数据

2. **是否需要排序?**
   - 建议: 按created_at降序（最新的在前）

3. **空列表的响应格式?**
   - 建议: 返回空数组 `{"applications": []}`

4. **是否需要添加count字段?**
   - 建议: Phase 1不添加，保持最简

5. **辅导员查询申请列表的范围?**
   - 当前提案: 返回所负责班级学生的所有申请
   - 是否应该只返回待审批的? 还是所有状态的?

---

## 七、请Codex审查

**审查要点:**
1. 实现方案是否合理?
2. 权限逻辑是否正确?
3. 时间估算是否现实?
4. 是否有遗漏的风险?
5. 待审查的5个问题的建议答案

**期望输出:**
- 对方案的评价
- 回答5个待审查问题
- 明确建议: 接受/修改/拒绝
- 如果建议修改，说明具体改什么

不要客气，如果方案有问题就直说。
