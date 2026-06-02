---
task_id: TASK-20260602-03
owner: claude
assignee: none
status: open
created_at: 2026-06-02T18:51:20.595201+00:00
updated_at: 2026-06-02T18:51:20.595217+00:00
priority: normal
---

# Task: Step 4B Phase 4: 回归验证 - 运行完整测试套件确保Phase 3无破坏性变更

**Task ID:** TASK-20260602-03
**Status:** open

## Objective

运行完整测试套件，验证Step 4B Phase 3的apply模式实现不破坏现有功能。

## Requirements

**环境前置：** 需要Django虚拟环境 (venv) 激活

**测试范围：**
1. 运行所有XG集成相关测试
2. 运行用户模块测试
3. 运行申请和审批模块测试（确保同步服务不影响业务逻辑）

**命令：**
```bash
cd backend
source venv/bin/activate  # 激活虚拟环境
python3 manage.py test apps.users.tests
python3 manage.py test apps.applications.tests  
python3 manage.py test apps.approvals.tests
```

## Acceptance Criteria

- [ ] XG用户同步测试全部通过（包括新增的8个apply场景测试）
- [ ] 用户模块其他测试全部通过
- [ ] 申请模块测试全部通过
- [ ] 审批模块测试全部通过
- [ ] 无新增测试失败或错误

## Blocker

当前环境Django未安装/venv未激活，无法执行测试。需要环境配置后才能完成此任务。
