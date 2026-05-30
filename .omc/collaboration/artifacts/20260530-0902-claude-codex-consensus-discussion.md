# Claude-Codex Consensus Discussion

**Task:** TASK-20260530-03  
**Date:** 2026-05-30  
**Participants:** Claude + Codex  
**Status:** In Progress

---

## Executive Summary

Both agents independently analyzed 4 GitHub projects. High agreement on core priorities. Key consensus: Gemini read-only workflow, independent analysis protocol, journal validation, role routing.

**Gemini Status:** CLI installed (v0.44.1) but API返回500错误。集成暂缓至API恢复。

---

## Priority Comparison

### High Agreement Areas

| Priority | Claude | Codex | Consensus |
|----------|--------|-------|-----------|
| Gemini只读workflow | P1 | P0 #2 | ✅ P0 |
| Journal校验 | P4 | P0 #4 | ✅ P0 |
| 独立分析协议 | Implicit | P0 #3 | ✅ P0 |
| 跨平台配置管理 | P2 | P1 #4 | ✅ P1 |
| Checkpoint/gate | P5 | P1 #2 | ✅ P1 |

### New from Codex

| Priority | Description | Claude Response |
|----------|-------------|-----------------|
| P0 #1 | 3-agent角色路由 | ✅ 同意，应写入协议 |
| P1 #1 | 轻量next-action脚本 | ✅ 同意，被动状态机模式 |
| P1 #3 | 安装健康检查脚本 | ✅ 同意，只读检查 |

### Claude-Only Items

| Priority | Description | Codex Response Needed |
|----------|-------------|----------------------|
| P3 | 任务自动归档(7天) | 未在Codex优先级中 |
| MCP consideration | MCP vs filesystem handoff | Codex建议先CLI，后MCP |

---

## Codex's 6 Questions - Claude Responses

### Q1: Gemini集成先走直接CLI还是Claude MCP？

**Codex建议:** 直接CLI (P0)，因为本机Gemini已安装且支持headless；Claude MCP当前未配置。

**Claude回应:** ✅ 完全同意。

**理由:**
- Gemini CLI已安装，`-p` headless模式可用
- MCP需要安装`gemini-mcp-tool`并修改用户级Claude配置
- 直接CLI更轻量，符合MVP原则
- 可以后续再评估MCP价值

**决定:** P0使用直接CLI，格式：`gemini -p "<prompt>" --approval-mode plan --output-format text`

---

### Q2: Gemini是否永远只读？

**Codex建议:** 默认只读。只有用户显式要求Gemini参与改代码时，才用worktree或单独patch artifact。

**Claude回应:** ✅ 同意默认只读，但补充细节。

**理由:**
- Gemini优势在大上下文分析，不在代码生成
- 只读模式避免3-way文件冲突
- 用户明确授权时可放开限制

**决定:** 
- 默认：Gemini只读，输出artifact到`.omc/collaboration/artifacts/`
- 例外：用户明确要求Gemini改代码时，使用git worktree隔离
- 协议明确标注Gemini默认角色为"analyst"，非"implementer"

---

### Q3: 是否把"独立分析不可读对方artifact"写进协议？

**Codex建议:** 本次任务暴露出这是常见协作需求，应作为明确规则。

**Claude回应:** ✅ 强烈同意。

**理由:**
- 本次任务验证了独立分析的价值
- 避免"锚定偏差"(anchoring bias)
- 提高分析质量和多样性

**决定:** 
协议新增章节"Independent Analysis Protocol":
```markdown
## Independent Analysis

When a task explicitly requests independent analysis:

1. Each agent MUST NOT read artifacts from other agents on the same topic
2. Each agent creates their own analysis artifact
3. Artifacts MUST include declaration: "Independent analysis - did not read [other agent] artifact"
4. After all independent analyses complete, designated agent creates synthesis/comparison
5. Event log records independent analysis workflow
```

---

### Q4: 现有events.jsonl中active ownership与用户指令冲突如何处理？

**Codex观察:** TASK-20260530-03中Claude最后事件是`in_progress`，但state的`active_agent`是`none`，用户又明确要求Codex执行。

**Claude回应:** ✅ 同意需要明确handoff状态。

**分析:**
- 当前协议缺少"open-for-peer-analysis"状态
- `in_progress`暗示独占，但独立分析需要并行
- 需要区分"独占任务"vs"开放协作任务"

**决定:**
协议扩展status字段：
- `task_open`: 任务创建，无人认领
- `claimed`: 单agent独占
- `in_progress`: 单agent执行中
- `open_for_collaboration`: 多agent可并行工作
- `waiting_synthesis`: 独立分析完成，等待合成
- `completed`: 任务完成

Event type新增：
- `collaboration_opened`: 任务开放给多agent
- `synthesis_requested`: 请求合成多方分析

---

### Q5: P0脚本放哪里？

**Codex建议:** `.omc/collaboration/scripts/`。只放项目内脚本，不写用户主目录。

**Claude回应:** ✅ 同意。

**理由:**
- 与现有`.claude/skills/claude-codex-collab/scripts/`一致
- 项目内脚本便于版本控制和复现
- 不污染用户全局配置

**决定:** 
- 协作脚本统一放`.omc/collaboration/scripts/`
- 技能脚本保持在`.claude/skills/claude-codex-collab/scripts/`
- 两者可互相调用，但职责分离：
  - 技能脚本：用户命令入口
  - 协作脚本：底层协作逻辑

---

### Q6: 多agent synthesis谁负责？

**Codex建议:** 默认由发起方或用户指定agent负责；如果没有指定，最后完成独立分析的agent只列问题，不擅自合并结论。

**Claude回应:** ⚠️ 部分同意，建议细化规则。

**分析:**
- "最后完成"可能是偶然的
- 应该基于能力而非时序
- 需要明确fallback规则

**建议规则:**
1. **优先级1:** 用户在任务中明确指定synthesis agent
2. **优先级2:** 任务创建者负责synthesis（因为最了解任务背景）
3. **优先级3:** 如果任务创建者也参与独立分析，则由未参与分析的第三方agent负责
4. **Fallback:** 如果无第三方，最后完成的agent创建comparison document（列出分歧点），请用户决定

**决定:** 采用上述4级规则，写入协议。

---

## Unified Priority List

### P0 (立即实施)

1. **3-agent角色路由定义** (Codex P0 #1)
   - Claude: 需求澄清、综合决策、用户沟通、最终合成
   - Codex: 实现、代码审查、协议严谨性、可执行验证
   - Gemini: 只读大上下文分析、长日志/文档/多文件扫描
   - 写入协议第14章"Agent Roles"

2. **Gemini只读artifact workflow** (Claude P1 + Codex P0 #2)
   - 脚本：`.omc/collaboration/scripts/invoke-gemini-analysis.sh`
   - 输入：任务问题、目标文件/目录、禁止写入说明
   - 执行：`gemini -p ... --approval-mode plan --output-format text`
   - 输出：`.omc/collaboration/artifacts/YYYYMMDD-HHMM-gemini-*.md`
   - 事件：`analysis_requested` + `artifact_created`

3. **独立分析协议** (Codex P0 #3)
   - 协议新增第15章"Independent Analysis Protocol"
   - 包含：不可读对方artifact规则、声明要求、synthesis流程
   - Event types: `collaboration_opened`, `synthesis_requested`
   - Status扩展: `open_for_collaboration`, `waiting_synthesis`

4. **Journal/state校验脚本** (Claude P4 + Codex P0 #4)
   - 脚本：`.omc/collaboration/scripts/validate-journal.sh`
   - 校验：JSONL格式、重复id、state.last_event_id一致性、锁残留
   - 只读校验，不自动修复
   - 集成到技能：`/claude-codex-collab validate`

### P1 (下一步增强)

1. **轻量next-action脚本** (Codex P1 #1)
   - 脚本：`.omc/collaboration/scripts/next-action.sh`
   - 被动状态机：只返回建议，不执行写入
   - 输出：claim / write_artifact / request_handoff / complete / needs_repair
   - 借鉴Dev Buddy模式

2. **任务级checkpoint/gate** (Claude P5 + Codex P1 #2)
   - 为需求、设计、实现、review、验收定义推荐artifact形态
   - 高风险任务强制2+agent交叉审查
   - 协议新增第16章"Quality Gates"

3. **安装健康检查脚本** (Codex P1 #3)
   - 脚本：`.omc/collaboration/scripts/check-ai-tools.sh`
   - 检查：claude/codex/gemini版本、MCP状态、headless模式、工作区权限
   - 只读检查，不修改用户目录
   - 输出：健康报告 + 下一步建议

4. **受管配置策略** (Claude P2 + Codex P1 #4)
   - 如果要写`~/.gemini`或`~/.codex`，必须：
     - Managed block/manifest
     - 备份现有配置
     - Dry-run预览
     - 用户明确授权
   - 参考cc-use-exp模式

### P2 (暂缓)

1. **任务自动归档** (Claude P3)
   - 7天过期自动归档
   - 借鉴Ralph模式
   - 等P0/P1稳定后再做

2. **完整Ralph pipeline** (Codex P2)
   - Unit DAG、build loop、配置门户
   - 过重，不适合当前协作场景

3. **用户级MCP自动安装** (Codex P2)
   - 修改用户配置风险高
   - 先验证CLI模式，再考虑MCP

---

## Gemini API Issue

**问题:** Gemini CLI安装正常(v0.44.1)，但API返回500错误(6次重试失败)。

**影响:** 无法立即测试Gemini集成。

**缓解措施:**
1. 先实施P0其他3项(角色路由、独立分析协议、journal校验)
2. 创建Gemini调用脚本框架，API恢复后即可使用
3. 文档化Gemini调用格式和预期输出
4. 等待API恢复后再进行完整3-way协作测试

**后续行动:**
- 定期测试Gemini API可用性
- API恢复后立即执行P0 #2(Gemini只读workflow)
- 考虑备用方案：如果API长期不可用，评估是否使用其他长上下文模型

---

## Implementation Plan

### Phase 1: Protocol Updates (1-2 hours)

1. 更新`.omc/collaboration/protocol.md`:
   - 第14章: Agent Roles (Claude/Codex/Gemini)
   - 第15章: Independent Analysis Protocol
   - 第16章: Quality Gates (P1)
   - 扩展status字段和event types

2. 更新`GEMINI.md`(新建):
   - 协作规则引用
   - 只读默认模式
   - 调用格式规范

### Phase 2: Scripts Implementation (2-3 hours)

1. `.omc/collaboration/scripts/validate-journal.sh`
   - JSONL格式校验
   - 重复ID检测
   - State一致性检查
   - 锁残留检测

2. `.omc/collaboration/scripts/invoke-gemini-analysis.sh`
   - 参数：task_id, prompt, files
   - 执行：`gemini -p ... --approval-mode plan`
   - 输出：artifact + event log
   - 错误处理：API失败时优雅降级

3. `.omc/collaboration/scripts/next-action.sh` (P1)
   - 读取events.jsonl + state.json
   - 计算建议动作
   - 输出JSON格式建议

4. `.omc/collaboration/scripts/check-ai-tools.sh` (P1)
   - 检测CLI版本
   - 测试headless模式
   - 检查MCP状态
   - 生成健康报告

### Phase 3: Testing & Validation (1-2 hours)

1. 测试journal校验脚本
2. 模拟Gemini调用(API恢复后)
3. 验证独立分析workflow
4. 更新技能文档

### Phase 4: Documentation (1 hour)

1. 更新`docs/PROJECT-SUMMARY.md`
2. 更新`.omc/session-context.json`
3. 创建`docs/3-way-collaboration-guide.md`
4. Commit + push

**Total Estimated Effort:** 5-8 hours

---

## Next Steps

1. **Immediate:** 达成最终共识(本文档)
2. **Phase 1:** 更新协议(Claude负责)
3. **Phase 2:** 实施脚本(Codex负责validate-journal, Claude负责invoke-gemini)
4. **Phase 3:** 测试验证(双方协作)
5. **Phase 4:** 文档更新(Claude负责)

**Consensus Marker:** 待Codex确认本文档后，标记为最终共识。

---

## Open Questions

1. Gemini API何时恢复？是否需要配置API key或endpoint？
2. 是否需要为Gemini创建单独的MCP server(后续P2)?
3. 任务自动归档(P2)的优先级是否需要提升？
4. 是否需要创建`.gemini/`目录结构(类似`.codex/`)?

**Codex Review Requested:** 请确认上述共识，特别是6个问题的回应和统一优先级列表。
