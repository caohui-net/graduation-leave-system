# Phase 1b实施共识：实施顺序和风险控制

**达成时间：** 2026-05-30  
**讨论轮次：** 3轮  
**参与方：** Claude, Codex  
**Artifact来源：**
- Claude: `.omc/collaboration/artifacts/20260530-1625-claude-phase1b-response.md`
- Codex: `.omc/artifacts/ask/codex-omc-collaboration-artifacts-20260530-1625-claude-phase1b-res-2026-05-30T16-28-00-114Z.md`

---

## 一、核心共识

### 1. 实施顺序：Phase A-E分层门禁

**拒绝方案：** Claude原始的"Task #4先行"顺序（依赖倒置）

**采纳方案：** Codex的Phase A-E分层，但明确为门禁式推进：

- **Phase A：只读基础层**
  - 新增 `collab_schema.py`、`collab_journal.py`、`collab_lock.py`
  - 新增验证脚本框架（只跑 journal-basic、registry、legacy-events）
  - 不改真实 events.jsonl 行为，不启用 enforcement
  - **门禁：** 验证脚本通过，旧日志可读

- **Phase B：规则激活**
  - 修改 `collab_event.py` 使用注册表
  - 追加 `state_rules_version_changed` 事件作为新规则生效点
  - `legacy_cutoff` 动态取 activation_id - 1，不能写死52或54
  - 在 tempdir 跑 behavioral-smoke 后，再对真实协作目录启用
  - **门禁：** tempdir smoke通过，activation事件成功追加

- **Phase C：状态分叉处理**
  - 在 Phase B 激活前做"状态分叉决策"
  - 若只做只读验证：允许 legacy=waiting、canonical=blocked 同时存在，报告为 known divergence
  - 若启用写入规则：必须选择一个 operational state（建议 blocked）
  - 修正事件在 activation 之后追加，不在 Phase A/C 只读阶段追加
  - **门禁：** 状态决策明确，canonical/legacy 解释一致或显式声明分歧

- **Phase D：Task #2 repair锁**
  - 依赖 Phase A 的 collab_journal.py 和 collab_lock.py
  - repair 内部不能调用会再次获取 journal lock 的高层 append_event()
  - 使用"已持锁的低层 append"
  - **门禁：** repair-smoke 在 tempdir 通过

- **Phase E：Task #3 Gemini**
  - 先加 passive schema 字段：active_agents、available_agents、agent_permissions
  - 完整权限 enforcement、Gemini lifecycle、artifact 子目录限制放最后
  - **门禁：** Gemini dry-run 通过，不依赖 Gemini CLI 安装

### 2. 双实现漂移问题（P0优先级）

**Claude原始判断：** 旧路径已废弃，直接删除

**Codex纠正（已验证）：**
- `.claude/skills/claude-codex-collab/SKILL.md` 的 task/status/handoff/repair 都调用 `.claude/skills/.../scripts/`
- `.omc/collaboration/scripts/invoke-gemini-analysis.sh` 三处调用 `.claude/skills/.../collab_event.py`
- `.omc/collaboration/scripts/` 目前只有 validate-journal.sh 和 invoke-gemini-analysis.sh，**没有 collab_event.py**

**最终方案：**
1. 把核心 Python 写入脚本迁到 `.omc/collaboration/scripts/`
2. `.claude/skills/.../scripts/` 只保留薄 wrapper，转调 `.omc` 下的脚本
3. 更新 SKILL.md 和 invoke-gemini-analysis.sh 的调用点
4. 验证没有调用旧核心实现后，再考虑删除旧实现文件

**禁止方案：** 两边都保留完整实现（会让 validator 和 writer 相信不同状态机）

### 3. state_rules_version_changed事件时机

**Claude原始方案：**
- B.1: 修改 collab_event.py，添加 state_rules_version_changed 到 INFO_EVENTS
- B.2: 部署新代码
- B.3: 追加 state_rules_version_changed 事件（id=55），标记 legacy_cutoff=54
- B.4: 从 id=56 开始强制执行新规则

**Codex纠正：**
- ✅ 方向正确，但不能手写假定 id=55
- ✅ 必须在持有 journal.lock 时从 events.jsonl 计算 max(id)+1
- ✅ state_rules_version_changed 应该作为新代码支持后的第一条真实 activation event

**最终方案：**
1. 先改代码和 schema，让旧日志可读、新事件类型可识别
2. 在 tempdir 用复制的 events.jsonl/state.json 跑 behavioral smoke
3. 真实目录加锁追加 state_rules_version_changed
4. 事件 details 写：
   - `old_version: 1`
   - `new_version: 2`
   - `legacy_cutoff_event_id: <activation_id - 1>`（动态计算）
   - `effective_from_event_id: <activation_id + 1>`（动态计算）
5. 从 effective_from_event_id 开始拒绝 unknown event，INFO 事件禁止顶层 status

---

## 二、共识文档矛盾优先级

**P0（立即修复）：**
1. LEGACY_CUTOFF_EVENT_ID 硬编码 - 修复 Task #1 文档，改为动态推导
2. 双实现漂移 - Phase A 第一步验证调用点，迁移写入口

**P1（Phase A/B 修复）：**
3. INFO_EVENTS 历史 status - 文档澄清"只对 cutoff 后强制"
4. state_rebuilt vs state_corrected 约束 - 放宽 state_rebuilt 要求

**P2（Phase E 修复）：**
5. INFO 更新 metadata vs 不更新 state - 文档澄清"不更新 status，允许更新非状态字段"
6. state-schema check 依赖 - Phase A 加默认三方字段

---

## 三、最大风险识别

**Codex 最担心：** 双实现漂移

**风险场景：**
- 当前写入入口在 `.claude/skills/...`
- 验证和新设计在 `.omc/collaboration/scripts/`
- 如果先实现 validator/schema，却没有迁移真实写入口
- 测试会通过，但生产写入仍会把未知事件映射成 in_progress
- 继续污染 state.json

**缓解措施：**
- Phase A 第一步：grep 确认所有调用点
- 统一脚本入口后再实施新规则
- 每个 Phase 都有明确的验证门禁

---

## 四、回滚策略

**基线标记：**
```bash
rtk git tag phase1b-baseline-20260531
```

**回滚方式：**
- 代码回滚：`git revert` 到 tag
- 状态回滚：不直接重写 events.jsonl，通过追加 state_corrected 或锁保护下重建 state.json

**Emergency 开关：**
- 不使用长期 feature flag 控制规则
- 保留 emergency 开关用于"拒绝所有写入"（只读验证模式）

---

## 五、最终实施顺序（7步）

### Step 1: 基线检查和回滚点

```bash
rtk git status --short
rtk .omc/collaboration/scripts/validate-journal.sh
rtk git tag phase1b-baseline-20260531
```

### Step 2: 统一脚本入口（P0）

**重要：** 迁移入口但保持旧行为兼容，**不启用新规则 enforcement**。否则 Step 2 可能意外变成规则激活。

**修改文件：**
- `.omc/collaboration/scripts/collab_schema.py` 新增（定义注册表，但不强制）
- `.omc/collaboration/scripts/collab_journal.py` 新增（解析器，但不拒绝）
- `.omc/collaboration/scripts/collab_lock.py` 新增
- `.omc/collaboration/scripts/collab_event.py` 从旧路径迁入，**保持旧行为**（unknown→in_progress）
- `.claude/skills/claude-codex-collab/scripts/collab_event.py` 改成 wrapper
- `.claude/skills/claude-codex-collab/SKILL.md` 更新调用点
- `.omc/collaboration/scripts/invoke-gemini-analysis.sh` 更新调用点

**验证：**
```bash
rtk rg -n "\\.claude/skills/claude-codex-collab/scripts/collab_event.py|collab_event.py" .claude .omc docs
rtk .omc/collaboration/scripts/validate-journal.sh
```

### Step 3: Phase A 只读基础层

**新增文件：**
- `.omc/collaboration/scripts/validate-phase1a.sh`
- `.omc/collaboration/scripts/validate_phase1a.py`

**验证：**
```bash
rtk .omc/collaboration/scripts/validate-phase1a.sh --check journal-basic
rtk .omc/collaboration/scripts/validate-phase1a.sh --check registry
rtk .omc/collaboration/scripts/validate-phase1a.sh --check legacy-events
```

### Step 4: Phase B 激活规则

**修改文件：**
- `.omc/collaboration/protocol.md`
- `.omc/collaboration/task-1-consensus.md`
- `.omc/collaboration/task-4-consensus.md`
- `.omc/collaboration/scripts/collab_event.py`（启用新规则enforcement）

**验证和激活：**
```bash
rtk .omc/collaboration/scripts/validate-phase1a.sh --check behavioral-smoke --tempdir
# 注意：activation命令必须支持动态写入details，包含：
# - old_version: 1
# - new_version: 2
# - legacy_cutoff_event_id: <activation_id - 1>（动态计算）
# - effective_from_event_id: <activation_id + 1>（动态计算）
# 实现时由脚本在持锁期间动态写入，或命令支持 --details-json
rtk python3 .omc/collaboration/scripts/collab_event.py state_rules_version_changed codex none "Activated collaboration state rules v2" --details-json '{"old_version":1,"new_version":2}'
rtk .omc/collaboration/scripts/validate-journal.sh
```

### Step 5: Phase C 状态分叉处理

**条件：** 若 activation 后 canonical 仍为 blocked、state 仍为 waiting

**操作：**
```bash
rtk python3 .omc/collaboration/scripts/collab_event.py state_corrected codex TASK-20260530-06 "Restored canonical blocked status after state rules v2 activation"
rtk .omc/collaboration/scripts/validate-journal.sh
```

### Step 6: Phase D repair 锁修复

**修改文件：**
- `.omc/collaboration/scripts/collab_validate.py` 或迁移后的 repair 实现
- `.omc/collaboration/scripts/collab_lock.py`
- `.omc/collaboration/scripts/collab_journal.py`

**验证：**
```bash
rtk .omc/collaboration/scripts/validate-phase1a.sh --check repair-smoke --tempdir
rtk .omc/collaboration/scripts/validate-journal.sh
```

### Step 7: Phase E Gemini/passive agent schema

**修改文件：**
- `.omc/collaboration/scripts/collab_schema.py`
- `.omc/collaboration/scripts/invoke-gemini-analysis.sh`
- `.omc/collaboration/protocol.md`

**验证：**
```bash
rtk .omc/collaboration/scripts/invoke-gemini-analysis.sh --dry-run -t TASK-20260530-06 -p "Gemini workflow dry run"
rtk .omc/collaboration/scripts/validate-journal.sh
```

---

## 六、关键决策记录

### Q1: Phase C 状态校正时机

**Claude 质疑：** Phase C 强制要求现在就追加 state_corrected 会污染事件日志

**Codex 回应：** 同意"不要过早修日志"，但不能推迟状态决策到 Phase 2

**最终决策：**
- Phase A 不修日志
- Phase B 激活前做"状态分叉决策"
- Phase B 激活后立即用明确事件修正（如果需要）
- 或明确声明 legacy state 被保留且 canonical 检查不作为 gate

### Q2: 双实现漂移

**Claude 判断：** 旧路径已废弃，直接删除

**Codex 纠正：** 旧路径仍在使用，不能删除

**最终决策：**
- Phase A 第一步：grep 确认所有调用点
- 先迁移核心实现到 `.omc/collaboration/scripts/`
- 旧路径改为薄 wrapper
- 验证后再删除旧实现

### Q3: state_rules_version_changed 事件时机

**Claude 方案：** B.1-B.4 顺序，但写死 id=55

**Codex 纠正：** 方向对，但必须动态计算 ID

**最终决策：**
- 不能手写假定 id=55
- 必须在持有 journal.lock 时从 events.jsonl 计算 max(id)+1
- activation event 本身是边界标记，不受"后续事件禁止 status"规则约束

---

## 七、追加共识事件的正确方法

**重要警告：** 不要使用当前旧的 `.claude/skills/.../collab_event.py` 追加 consensus_reached 事件。

**原因：**
- 旧脚本对未知事件默认写 `status=in_progress`（line 102）
- 并会覆盖 `state.status`（line 112）
- 这会错误地将当前 `waiting` 状态改为 `in_progress`

**正确方法：** 手动持锁追加，保持当前 workflow status 为 `waiting`

```bash
# 1. 获取锁
mkdir .omc/collaboration/locks/journal.lock

# 2. 写入 owner.json
cat > .omc/collaboration/locks/journal.lock/owner.json <<EOF
{
  "agent": "claude",
  "task_id": "TASK-20260530-06",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)",
  "heartbeat_at": "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)",
  "reason": "append consensus_reached event"
}
EOF

# 3. 计算下一个事件ID
NEXT_ID=$(tail -1 .omc/collaboration/events.jsonl | jq '.id + 1')

# 4. 追加事件（不含status字段，保持state.status不变）
cat >> .omc/collaboration/events.jsonl <<EOF
{"id":${NEXT_ID},"type":"consensus_reached","agent":"claude","timestamp":"$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)","summary":"Phase 1b implementation consensus reached","task_id":"TASK-20260530-06","artifacts":[".omc/collaboration/phase1b-implementation-consensus.md"],"details":{"discussion_rounds":3,"key_decisions":["Phase A-E layered gates","Unify script entry first","Dynamic cutoff calculation","State fork decision before Phase B"]}}
EOF

# 5. 更新 state.json（只更新 last_event_id，不改 status）
jq ".last_event_id = ${NEXT_ID} | .updated_at = \"$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)\"" .omc/collaboration/state.json > .omc/collaboration/state.json.tmp.claude
mv .omc/collaboration/state.json.tmp.claude .omc/collaboration/state.json

# 6. 释放锁
rm -rf .omc/collaboration/locks/journal.lock
```

## 八、下一步

1. 立即修复 Task #1 共识文档（移除 LEGACY_CUTOFF_EVENT_ID=52）
2. 追加 consensus_reached 事件（使用上述正确方法）
3. 执行 Step 1: 基线检查和回滚点
4. 执行 Step 2: 统一脚本入口（P0 优先级）
5. 按顺序执行 Step 3-7，每步验证通过后再进入下一步

**状态：** ✅ 共识达成，已补充3处澄清，待实施
