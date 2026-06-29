# 测试环境-用户登录后无数据

## Goal

在172.17.12.196:17788测试环境，用户2023045104054和2020220040131选择留校业务类型登录后无任何数据显示。需定位根因并修复。

## Problem Statement

**环境**: 172.17.12.196:17788
**受影响用户**: 2023045104054, 2020220040131
**操作流程**: 选择留校业务类型 → 登录
**现象**: 登录后无任何数据

## Investigation Plan

1. 确认"无数据"的具体含义
   - 审批列表为空？
   - 申请记录为空？
   - 页面加载失败？

2. 数据库验证
   - 检查用户是否存在
   - 检查用户的申请记录
   - 检查审批记录

3. 代码逻辑检查
   - 审批列表过滤逻辑
   - 用户角色判断
   - 业务类型过滤

4. 最近代码改动影响分析
   - applications/views.py
   - users/views.py

## Related Issues

- 可能与任务 `06-29-prod-bug-missing-approvals` 相关
- 最近有审批列表过滤相关的改动

## Root Cause

**文件**: `demo-web/index.html:2116-2118`

学生登录后错误执行：
```javascript
if (hasApplications) {
    showScreen(1);      // 审批列表页面
    loadApprovals();    // 审批API
}
```

学生角色无审批权限，审批列表为空。

## Fix

删除条件分支，学生始终显示申请表单：
```javascript
// Student: always show form (screen0)
showScreen(0);
```

## Acceptance Criteria

- [x] 定位根本原因 - 学生错误跳转到审批列表
- [x] 修复代码逻辑 - 学生始终显示screen-0
- [ ] 验证两个测试用户可以正常使用
- [x] 确保修复不影响其他用户 - 其他角色逻辑未改动
