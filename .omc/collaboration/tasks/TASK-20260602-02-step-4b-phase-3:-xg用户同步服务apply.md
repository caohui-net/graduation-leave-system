---
task_id: TASK-20260602-02
owner: claude
assignee: none
status: open
created_at: 2026-06-02T18:45:51.925438+00:00
updated_at: 2026-06-02T18:45:51.925453+00:00
priority: normal
---

# Task: Step 4B Phase 3: XG用户同步服务apply模式实现 - 8个验收场景测试

**Task ID:** TASK-20260602-02
**Status:** open

## Objective

实现XG用户同步服务的apply模式，在plan模式基础上增加实际DB写入能力。

## Background

**已完成：**
- Step 4B Phase 1: User模型扩展(phone/email/department字段) + migration 0002
- Step 4B Phase 2: mapper增加email提取
- 当前`plan_xg_user_sync()`只做计划分析，不写DB

**本Phase目标：**
实现`apply_xg_user_sync()`函数，实际更新已存在学生用户的phone/email/department字段。

## Implementation Requirements

**新增函数：** `apply_xg_user_sync(xg_users: List[dict], dry_run: bool = True) -> Dict`

**功能：**
- dry_run=True: 行为同plan模式，返回统计
- dry_run=False: 实际更新DB中已存在的student用户

**更新规则：**
- 仅更新role='student'的已存在用户
- 更新字段：phone, email, department (来自mapper输出)
- 跳过：mapper返回skip_reason的用户
- 跳过：role冲突的用户
- 跳过：本地不存在的用户(不创建新用户)

## Acceptance Criteria (8 Scenarios)

- [ ] Scenario 1: 成功更新已存在student的3个字段
- [ ] Scenario 2: 跳过mapper标记skip_reason的用户
- [ ] Scenario 3: 检测并跳过role冲突(local非student)
- [ ] Scenario 4: 跳过本地不存在的用户
- [ ] Scenario 5: dry_run=True不写DB，返回would_update统计
- [ ] Scenario 6: 批量同步多个用户
- [ ] Scenario 7: 返回详细统计(updated_count, skipped_count, conflicts)
- [ ] Scenario 8: 不影响其他用户(非student/未匹配用户)
