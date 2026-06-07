---
task_id: TASK-20260606-20
owner: claude
assignee: none
status: open
created_at: 2026-06-06T17:00:45.054077+00:00
updated_at: 2026-06-06T17:00:45.054082+00:00
priority: normal
---

# Task: Phase 4前端实施策略讨论

**问题背景：**
Phase 4任务要求进行前端UI调整（用户需求最终确认与实施方案.md）：
- 任务4.1：用户界面区分（学生/宿管员/辅导员/学工管理员4个角色）
- 任务4.2：审批流程UI更新（2级审批进度条，移除学工部步骤）

**发现的问题：**
检查frontend/目录，只发现3个文件：
- frontend/services/api.ts
- frontend/services/mock.ts  
- frontend/types/api.ts

没有任何UI组件、页面或应用代码。miniprogram/目录为空。

**需要讨论的问题：**
1. 前端是否从未实现？还是在其他位置？
2. 原设计是微信小程序，现在应该用什么技术栈？
3. Phase 4是调整现有UI还是从零构建前端？
4. 如果要构建，推荐的实施路径是什么？

**相关证据：**
- 后端API已完整实现（审批流程已验证通过smoke test）
- 存在API契约文档：docs/api/contract-v0.3.md
- frontend/services/api.ts已定义API调用接口
- 项目文档提到微信小程序但无实际代码

**建议讨论参与者：** Codex（架构视角）, Gemini（实施建议）

**Task ID:** TASK-20260606-20
**Status:** open

## Objective

Phase 4前端实施策略讨论

**问题背景：**
Phase 4任务要求进行前端UI调整（用户需求最终确认与实施方案.md）：
- 任务4.1：用户界面区分（学生/宿管员/辅导员/学工管理员4个角色）
- 任务4.2：审批流程UI更新（2级审批进度条，移除学工部步骤）

**发现的问题：**
检查frontend/目录，只发现3个文件：
- frontend/services/api.ts
- frontend/services/mock.ts  
- frontend/types/api.ts

没有任何UI组件、页面或应用代码。miniprogram/目录为空。

**需要讨论的问题：**
1. 前端是否从未实现？还是在其他位置？
2. 原设计是微信小程序，现在应该用什么技术栈？
3. Phase 4是调整现有UI还是从零构建前端？
4. 如果要构建，推荐的实施路径是什么？

**相关证据：**
- 后端API已完整实现（审批流程已验证通过smoke test）
- 存在API契约文档：docs/api/contract-v0.3.md
- frontend/services/api.ts已定义API调用接口
- 项目文档提到微信小程序但无实际代码

**建议讨论参与者：** Codex（架构视角）, Gemini（实施建议）

## Acceptance Criteria

- [ ] Task completed as described
