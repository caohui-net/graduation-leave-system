---
task_id: TASK-20260602-04
owner: claude
assignee: none
status: open
created_at: 2026-06-02T18:52:03.429982+00:00
updated_at: 2026-06-02T18:52:03.429998+00:00
priority: normal
---

# Task: Step 5: XG用户同步管理命令 - sync_xg_users命令实现

**Task ID:** TASK-20260602-04
**Status:** open

## Objective

实现Django管理命令`sync_xg_users`，提供命令行接口调用XG用户同步服务。

## Background

**已完成：**
- Step 4B Phase 3: apply_xg_user_sync()函数实现（支持dry_run参数）
- XG API客户端（支持分页获取用户列表）
- 用户映射器（map_xg_user_to_internal）

**本Step目标：**
创建Django management command，封装完整同步流程。

## Implementation Requirements

**文件位置：** `backend/apps/users/management/commands/sync_xg_users.py`

**命令功能：**
1. 调用XG API客户端获取用户列表（分页处理）
2. 调用apply_xg_user_sync()执行同步
3. 支持--dry-run模式（默认dry_run=True）
4. 输出同步统计信息
5. 错误处理和日志记录

**命令参数：**
- `--apply`: 实际写入DB（不提供则dry_run=True）
- `--limit N`: 限制获取用户数（可选，用于测试）

**输出示例：**
```
Fetching users from XG API...
Fetched 100 users
Running sync (dry-run mode)...
Results:
  - Total fetched: 100
  - Mapped: 95
  - Skipped: 5
  - Updated: 50
  - Conflicts: 0
  - Missing local: 45
```

## Acceptance Criteria

- [ ] 创建management command文件
- [ ] 实现--apply和--dry-run模式切换
- [ ] 调用XG API客户端获取用户
- [ ] 调用apply_xg_user_sync()执行同步
- [ ] 输出清晰的统计信息
- [ ] 错误处理完善
