---
task_id: TASK-20260530-04
owner: claude
assignee: none
status: open
created_at: 2026-05-30T09:08:10.887236+00:00
updated_at: 2026-05-30T09:08:10.887343+00:00
priority: normal
---

# Task: 实施P0优先级项：角色路由+独立分析协议+journal校验+Gemini workflow

**Task ID:** TASK-20260530-04
**Status:** open

## Objective

实施TASK-20260530-03共识中的P0优先级项，为3-agent协作奠定基础。

## Context

基于`.omc/collaboration/artifacts/20260530-0902-claude-codex-consensus-discussion.md`和`20260530-1703-codex-consensus-confirmation.md`的共识。

## P0 Items

### 1. 3-Agent角色路由定义 (Claude负责)
- 更新`.omc/collaboration/protocol.md`添加第14章"Agent Roles"
- 定义Claude/Codex/Gemini角色边界
- 明确各agent适用场景

### 2. Gemini只读Artifact Workflow (Claude负责)
- 创建`.omc/collaboration/scripts/invoke-gemini-analysis.sh`
- 输入：task_id, prompt, files
- 执行：`gemini -p ... --approval-mode plan --output-format text`
- 输出：artifact + event log
- 错误处理：API失败时优雅降级

### 3. 独立分析协议 (Claude负责)
- 更新`.omc/collaboration/protocol.md`添加第15章"Independent Analysis Protocol"
- 规则：不可读对方artifact、声明要求、synthesis流程
- 扩展status字段：`open_for_collaboration`, `waiting_synthesis`
- 新增event types：`collaboration_opened`, `synthesis_requested`

### 4. Journal/State校验脚本 (Codex负责)
- 创建`.omc/collaboration/scripts/validate-journal.sh`
- 校验：JSONL格式、重复ID、state一致性、锁残留
- 只读校验，不自动修复
- 集成到技能：`/claude-codex-collab validate`

## Acceptance Criteria

- [ ] Protocol.md包含第14章"Agent Roles"
- [ ] Protocol.md包含第15章"Independent Analysis Protocol"
- [ ] Status字段扩展已实施
- [ ] Event types已扩展
- [ ] `invoke-gemini-analysis.sh`已创建并测试（dry-run模式）
- [ ] `validate-journal.sh`已创建并测试
- [ ] 技能文档已更新
- [ ] 所有脚本可执行
- [ ] 验证通过：`/claude-codex-collab validate`

## Ownership

- **Claude**: P0 #1, #2, #3 + 文档更新
- **Codex**: P0 #4 + 状态转换审查

## References

- 共识文档：`.omc/collaboration/artifacts/20260530-0902-claude-codex-consensus-discussion.md`
- 确认文档：`.omc/collaboration/artifacts/20260530-1703-codex-consensus-confirmation.md`
- 当前协议：`.omc/collaboration/protocol.md` (v0.2)
