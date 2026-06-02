# Task #3 共识：添加active_agent支持gemini

**达成时间：** 2026-05-30  
**讨论轮次：** 2轮  
**参与方：** Claude, Codex

---

## 问题描述

**背景：** 当前协议只支持claude/codex作为active_agent，需要添加gemini支持以实现三方协作。

**当前限制：**
- protocol.md Line 63只列举claude/codex
- 缺少gemini的agent readiness检查
- 缺少三方协作的状态转换规则
- 缺少权限模型定义

---

## 最终方案

### 1. state.json字段扩展

**保留向后兼容 + 新增三方字段：**

```json
{
  "active_agent": "claude",
  "active_agents": ["claude", "codex"],
  "available_agents": ["claude", "codex", "gemini"],
  "agent_permissions": {
    "claude": "full",
    "codex": "full",
    "gemini": "read_only"
  }
}
```

**字段语义：**
- `active_agent`：兼容旧协议，表示当前owner/coordinator/last responsible agent（单个）
- `active_agents`：新字段，表示当前并行参与的agents（列表）
- `available_agents`：已ready，可被调度的agents（列表）
- `agent_permissions`：当前workflow下每个agent的权限

**向后兼容策略：** 保留active_agent字段，现有52条事件和脚本不受影响。

### 2. 权限模型

**三层权限定义：**

```python
# read_only权限
允许：
- 读取repo所有文件
- 读取state.json
- 写入.omc/collaboration/artifacts/{agent}/
- 追加INFO_EVENTS（不含status）

禁止：
- 修改repo源文件
- 修改state.json
- 追加STATE_TRANSITIONS或STATUS_OVERRIDE_EVENTS
- 写入.omc/collaboration/（除artifacts/{agent}/子目录）

# patch_proposal权限
允许：
- read_only的所有权限
- 生成patch/diff文件
- 提议代码修改

禁止：
- 直接应用patch到repo
- 需要claude/codex批准后才能应用

# isolated_write权限
允许：
- 在独立worktree/branch写入
- 修改隔离环境中的文件

禁止：
- 直接写主工作区
- 合入需claude/codex审核
```

**权限职责分层：**
- `protocol.md`：定义权限枚举和允许行为
- `state.json`：记录当前workflow的实际权限快照
- `events.jsonl`：每次权限变更必须有事件
- 执行脚本：在写入前检查权限

### 3. 新增事件类型

**agent_joined（INFO_EVENTS）：**

```json
{
  "id": 54,
  "type": "agent_joined",
  "agent": "claude",
  "timestamp": "2026-05-30T15:50:00.000Z",
  "summary": "Gemini joined collaboration",
  "details": {
    "joined_agent": "gemini",
    "permission": "read_only",
    "reason": "large context analysis requested"
  }
}
```

**agent_left（INFO_EVENTS）：**

```json
{
  "id": 55,
  "type": "agent_left",
  "agent": "gemini",
  "timestamp": "2026-05-30T15:55:00.000Z",
  "summary": "Gemini left collaboration",
  "details": {
    "reason": "analysis completed"
  }
}
```

**agent_permission_changed（INFO_EVENTS）：**

```json
{
  "id": 56,
  "type": "agent_permission_changed",
  "agent": "claude",
  "timestamp": "2026-05-30T15:52:00.000Z",
  "summary": "Escalated Gemini permission to patch_proposal",
  "details": {
    "target_agent": "gemini",
    "old_permission": "read_only",
    "new_permission": "patch_proposal",
    "reason": "escalate for code review task"
  }
}
```

**约束：**
- 只有full权限agent能修改权限
- 不能降级claude/codex
- 必须提供reason

### 4. 状态机设计

**不新增agent-specific状态，复用现有状态：**

- `open_for_collaboration`：多agent可并行分析
- `in_progress`：单agent或coordinator正在推进
- `waiting`：等待外部动作、handoff、用户或某agent响应
- `waiting_synthesis`：等待综合多方输入
- `blocked`：阻塞
- `completed`：完成

**等待特定agent的表达方式：** 放到事件details中

```json
{
  "type": "handoff_requested",
  "status": "waiting",
  "details": {
    "requested_agent": "gemini",
    "requested_action": "large_context_analysis"
  }
}
```

**原则：** 状态描述workflow阶段，不描述等待哪个agent。

### 5. gemini后加入流程

**gemini_ready事件（INFO_EVENTS）：**
- 只更新available_agents
- 不自动加入active_agents
- 不改变workflow status

**后加入流程：**
1. Gemini发`gemini_ready`
2. `available_agents`增加`gemini`
3. 当前任务不自动变化
4. 需要Claude/Codex/user显式发起：
   - `agent_joined`：加入当前协作
   - 或`analysis_requested`：一次性请求分析
5. Gemini完成后写artifact，发`independent_analysis_completed`或`artifact_created`
6. 若进入多方综合，状态转为`waiting_synthesis`

**原则：** 不等待所有agents ready才开始协作。核心双agent可先工作，Gemini可后加入。

---

## 事件注册表更新

**INFO_EVENTS新增：**
```python
INFO_EVENTS = {
    # ... 现有事件 ...
    'agent_joined',
    'agent_left',
    'agent_permission_changed',
}
```

---

## 实现位置

- **protocol.md：** 添加三方协作章节、权限模型定义
- **collab_event.py：** 更新事件注册表，添加权限检查
- **state.json schema：** 添加新字段
- **脚本：** 实现权限检查逻辑

---

## 关键决策

### 为什么保留active_agent？

**向后兼容：** 现有52条事件和脚本依赖active_agent字段。直接替换为active_agents会破坏兼容性。

**策略：** 新增字段，不删除旧字段。active_agent表示coordinator，active_agents表示并行参与者。

### 为什么不新增agent-specific状态？

**可扩展性：** 状态机不应随agent数量膨胀。`waiting_gemini_analysis`、`waiting_codex_review`等会导致状态爆炸。

**策略：** 状态描述workflow阶段，agent信息放details。

### 为什么read_only可写artifact？

**实用性：** 完全禁止写入会导致Gemini无法产出分析结果。

**策略：** 限制写入路径为`.omc/collaboration/artifacts/{agent}/`，不能修改repo源文件和共享状态。

---

## 下一步

1. 更新protocol.md添加三方协作章节
2. 更新Task #1共识的事件注册表
3. 实现权限检查逻辑
4. 添加agent_joined/agent_left/agent_permission_changed事件处理
5. 测试三方协作流程

**状态：** ✅ 共识达成，待实施
