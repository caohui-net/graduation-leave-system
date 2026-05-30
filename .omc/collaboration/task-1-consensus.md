# Task #1 共识：修复collab_event.py事件映射bug

**达成时间：** 2026-05-30  
**讨论轮次：** 3轮  
**参与方：** Claude, Codex

---

## 问题描述

**Bug位置：** `collab_event.py:102`

```python
status_map = {...}
event['status'] = status_map.get(event_type, 'in_progress')  # BUG
```

**问题：** 未知事件类型默认映射为`in_progress`，导致信息事件（如`artifact_created`）错误覆盖任务状态（如`blocked`）。

**影响：** 现有52条事件中，7个`artifact_created`事件错误携带`status=in_progress`。

---

## 最终方案

### 1. 三类事件模型

```python
STATE_TRANSITIONS = {
    'task_created': 'task_open',
    'task_claimed': 'in_progress',
    'handoff_requested': 'waiting',
    'completed': 'completed',
    'blocked': 'blocked',
    'collaboration_opened': 'open_for_collaboration',
    'independent_analysis_completed': 'waiting_synthesis',
    'synthesis_completed': 'completed',
    'in_progress': 'in_progress',
}

INFO_EVENTS = {
    'artifact_created',
    'analysis_requested',
    'analysis_completed',
    'analysis_failed',
    'review_response',
    'consensus_reached',
    'skill_created',
    'synthesis_requested',
    'codex_ready',
    'claude_ready',
    'gemini_ready',
    'agent_joined',
    'agent_left',
    'agent_permission_changed',
}

STATUS_OVERRIDE_EVENTS = {
    'state_corrected',
    'state_rebuilt',
}

VALID_STATUSES = {
    'task_open',
    'in_progress',
    'waiting',
    'blocked',
    'completed',
    'open_for_collaboration',
    'waiting_synthesis',
}
```

### 2. 行为规则

1. **event_type验证：** 必须在注册表中，否则`ValueError`，事件不追加
2. **STATE_TRANSITIONS：** 自动设置`event['status']`和`state['status']`
3. **INFO_EVENTS：** 完全禁止顶层`status`，不更新`state['status']`
4. **STATUS_OVERRIDE_EVENTS：** 必须显式传入：
   - `status` (in VALID_STATUSES)
   - `reason` (必填)
   - `previous_status` (必填)
   - `corrected_event_ids` (列表，必填)
5. **所有成功事件：** 更新`last_event_id`和`updated_at`
6. **current_task更新：**
   - STATE_TRANSITIONS: 有task_id时默认更新
   - INFO_EVENTS: 默认不更新，允许显式`update_current_task=True`
   - STATUS_OVERRIDE_EVENTS: 允许修正，必须有reason

### 3. 验证顺序

```
1. 读取输入参数
2. 识别event_type属于三类之一，否则拒绝
3. 校验该类型允许/禁止的字段
4. 派生status或确认无status
5. 获取lock
6. 验证现有log/state
7. 分配id
8. 构造最终event
9. append到events.jsonl
10. 按规则更新state.json
```

**关键：** INFO_EVENTS禁止status的校验在写入前完成，失败则命令非0退出。

### 4. 历史迁移策略

```python
STATE_RULES_VERSION = 2
# LEGACY_CUTOFF_EVENT_ID 动态确定，不硬编码
# 从 state_rules_version_changed 事件的 details.legacy_cutoff_event_id 读取
# 或从 events.jsonl 查找最后一个旧规则事件
```

**两种重建模式：**
- **legacy_rebuild：** 按历史`event.status`重放（用于审计/回溯）
- **canonical_rebuild：** 按注册表解释（用于修复/未来一致性）

**迁移规则：** 
- cutoff 动态确定：从 `state_rules_version_changed` 事件的 `details.legacy_cutoff_event_id` 读取
- 或从 `events.jsonl` 查找规则切换点
- 新事件（id > cutoff）强制新规则，旧事件保持不变

### 5. 实现位置

- **protocol.md：** 规范来源，说明事件分类、状态语义、迁移策略
- **collab_event.py：** 强制执行来源
- **collab_schema.py：** 统一管理常量（建议新增）

---

## 关键决策

### agent_ready事件语义

**共识：** `codex_ready/claude_ready/gemini_ready`是agent readiness signal，不是workflow status。

- 归类：INFO_EVENTS
- 不改变task/workflow status
- 是否"所有agent ready"由协作开启前检查或readiness registry判断

### synthesis_requested分类

**共识：** 归INFO_EVENTS

**理由：** 是请求/调度信号，不代表任务状态自然迁移。真正状态变化来自：
- `independent_analysis_completed` → `waiting_synthesis`
- `synthesis_completed` → `completed`

### state_corrected的corrected_event_ids

**共识：** 使用列表字段，不是单数

```json
{
  "type": "state_corrected",
  "status": "blocked",
  "details": {
    "previous_status": "waiting",
    "corrected_event_ids": [43, 44, 45, 46, 47, 48, 49],
    "reason": "INFO_EVENTS incorrectly advanced workflow status"
  }
}
```

---

## 回归测试要求

最低限度4个测试：

1. **未知事件类型：** 命令失败，不追加事件，不更新state
2. **artifact_created：** 事件追加成功，但`state.status`保持原值
3. **analysis_requested：** 同上，尤其覆盖原状态为`blocked`的场景
4. **task_claimed/handoff_requested/completed：** 仍正确更新状态

---

## 下一步

1. 更新`protocol.md`添加事件注册表和迁移策略
2. 修改`collab_event.py`实现新规则
3. 创建`collab_schema.py`统一管理常量
4. 添加回归测试
5. 验证修复后行为

**状态：** ✅ 共识达成，待实施
