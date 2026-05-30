# Codex 独立分析：4 个 GitHub 项目可借鉴内容

任务：TASK-20260530-03  
作者：Codex  
时间：2026-05-30 16:54 CST  
说明：本分析未读取 `.omc/collaboration/artifacts/20260530-0848-claude-github-projects-analysis.md`。我只查看了目标 GitHub 项目源码/文档、当前协作协议与本地 CLI/MCP 状态。

## 0. 输入与本地核验

已检查来源：

- `Z-M-Huang/vcp` 的 `plugins/dev-buddy`，commit `bf26f5472dcf771666a19b5582b660559b8755f2`
- `doccker/cc-use-exp`，commit `983787adc1005ab727444414ca4c4979bac72180`
- `smart-lty/Claude-Team`，commit `7936b9bb0d6e04263d36cb4eb2176e9ba3d6e8ed`
- `shakacode/claude-code-commands-skills-agents` 的 `docs/claude-code-with-codex.md`，通过 raw GitHub 文件获取

本地环境核验：

- `gemini` 已安装：`/home/caohui/.local/share/mise/installs/node/latest/bin/gemini`，版本 `0.44.1`
- `codex` 已安装：`codex-cli 0.134.0`
- `claude` 已安装：`2.1.150 (Claude Code)`
- `claude mcp list` 当前未显示 `codex` 或 `gemini-cli` MCP；只有现有插件 MCP 已连接
- `gemini --help` 显示可用 `-p/--prompt` 非交互模式、`--approval-mode plan` 只读计划模式、`--output-format text|json|stream-json`

## 1. 项目一：Dev Buddy

地址：https://github.com/Z-M-Huang/vcp/tree/main/plugins/dev-buddy

### 核心模式与架构

Dev Buddy 是四个项目里工程化程度最高的多 AI 协作编排系统。核心是 Ralph loop：把一次功能开发拆成 `Discovery -> Requirements+UAT -> Decomposition -> Plan-lint -> Build -> Code Review -> UAT`，通过磁盘计划文件和 JSON 状态在每个阶段之间传递上下文。

关键设计：

- 被动状态机：`ralph-state-machine.ts` 只计算下一步动作，不主动驱动执行。
- 多执行器分发：`stage-runner.ts` 加载 stage 配置，按 subscription/API/CLI preset 分发给多个模型/工具，再合成结果。
- 单元级构建循环：`build-loop-runner.ts` 针对一个 unit 做实现、测试/typecheck/lint 反压、可选 unit review、重试与失败记录。
- 磁盘状态：`.vcp/plan/.state/ralph-{slug}/plan.json`、`units/unit-N.json`、`progress/*.json`，支持上下文压缩和进程重启后恢复。
- 明确边界：LLM 主进程负责协调与用户 checkpoint；脚本负责状态、分发、校验和事件输出。
- Codex 适配意识：MCP server 里有 `host: "claude" | "codex"` 指令分支，并明确 Codex 不一定自动注入 MCP resources，所以提供 paired tools。

### 值得借鉴

- **P0 借鉴：状态机被动化**。我们当前协议已经有 `events.jsonl` + `state.json`，但任务生命周期判断仍靠人工执行。可增加一个小型 `next-action`/`validate-journal` 脚本，只返回建议动作，不执行写入。
- **P0 借鉴：失败上下文持久化**。Dev Buddy 把机械失败、review feedback 持久化到 unit JSON，避免下一轮丢失。我们的协作任务也应把阻塞原因、验证输出、未决问题写入 artifact 或 task state，而不是只留在聊天里。
- **P1 借鉴：阶段化 gate**。Discovery、Requirements、Decompose 后设置用户/对方 agent checkpoint；我们不必全量照搬 Ralph，但可以给“需求/设计/实现/审查/验收”定义可选状态。
- **P1 借鉴：multi-executor + synthesizer**。对高风险任务，可让 Claude/Codex/Gemini 独立产出 artifact，再由一个 agent 写 synthesis，而不是同时修改同一文件。
- **P2 借鉴：任务面板投影与归档**。Dev Buddy 的 task-board projection 和 archive 机制适合规模化后再做。

### 不建议直接照搬

Dev Buddy 的完整 Ralph pipeline、Bun/TypeScript MCP server、配置门户、unit DAG 对当前 `.omc/collaboration` 过重。我们现在更需要 2-3 个小脚本：日志校验、任务状态推进、Gemini 只读分析入口。

### Gemini CLI 集成可行性

可行性高。Dev Buddy 的 CLI preset 模式可以映射到 Gemini：

- `command: "gemini"`
- `one_shot_args_template` 类似 `-p "{prompt}" --approval-mode plan --output-format text`
- 大上下文时应走 stdin 或文件路径，避免超长 argv

对本仓库更实用的第一步不是引入 Dev Buddy，而是实现一个只读 Gemini advisor workflow：给 Gemini 输入文件清单/问题，输出 `.omc/collaboration/artifacts/*-gemini-*.md`，禁止它直接改仓库。

## 2. 项目二：shakacode Claude Code with Codex

地址：https://github.com/shakacode/claude-code-commands-skills-agents/blob/main/docs/claude-code-with-codex.md

### 核心模式与架构

这是实践指南，不是框架。它的核心是把 Claude Code 与 Codex CLI 视为两个互补工具，通过共享项目指令和 git worktree 隔离来降低冲突。

关键模式：

- `AGENTS.md` 做跨工具共同事实源，`CLAUDE.md` 只保留 Claude-specific 扩展。
- Codex 的 `AGENTS.md` 采用层级发现，项目根与子目录可叠加。
- 推荐工作流包括：Claude 实现 / Codex review、两个工具独立解题后对比、不同 worktree 并行、spec-first。
- 强调工具差异：Claude 有 commands/skills/subagents；Codex 更强调 sandbox、approval policy、开源 CLI。

### 值得借鉴

- **P0 借鉴：共享核心指令，工具特化外置**。本项目已经有 `AGENTS.md` 与协作协议。若加入 Gemini，应避免三套互相矛盾的说明。建议新增一个短的 `docs/ai-collaboration-routing.md` 或协议章节，定义 Claude/Codex/Gemini 的共同规则与角色边界。
- **P0 借鉴：独立分析再合成**。本次任务本身就是这个模式。应固化为协议：当用户要求独立意见时，agent 不读对方 artifact；完成后再由指定 agent 对比。
- **P1 借鉴：worktree 隔离**。当 Claude 和 Codex/Gemini 都可能改代码时，必须使用 worktree 或只读 artifact，避免共享工作区互踩。
- **P1 借鉴：spec-first**。可要求一方写验收标准/测试方案，另一方实现或审查，减少自证正确。

### 不建议直接照搬

文档偏通用，缺少事件日志、锁、状态恢复等机制。我们已有 `.omc/collaboration/protocol.md`，不应退化成只靠操作建议。

### Gemini CLI 集成可行性

中高。该文档主要讲 Claude+Codex，但模式可扩展到 Gemini：

- Gemini 负责大上下文读代码、日志、文档和方案分歧分析。
- Codex 负责实现、diff review、测试风险。
- Claude 或当前主 agent 负责调度与最终合成。

需要补足的是具体调用契约：Gemini 输出必须落 artifact，不应直接修改仓库，除非用户明确授权。

## 3. 项目三：cc-use-exp

地址：https://github.com/doccker/cc-use-exp

### 核心模式与架构

cc-use-exp 是跨 AI 工具配置分发系统。它不是运行时协作引擎，而是把 Claude、Gemini、Codex、Cursor、Copilot 的 rules/skills/commands/templates 组织成一套可同步的用户级配置。

关键设计：

- 多平台目录源：`.claude/`、`.gemini/`、`.codex/`、`.cursor/`、`.github/`。
- 用户级同步：`tools/sync-config.sh` 把配置同步到 `~/.claude`、`~/.gemini`、`~/.codex`、`~/.agents/skills` 等。
- Codex 增量部署：使用 managed block 和 manifest，避免覆盖 `auth.json`、history、cache、用户默认模型等运行态。
- skill 单向同步：`tools/sync-skill.sh` 以 Claude skill 为权威源，同步到 Gemini/Cursor/Codex/Copilot；Codex skill 自动加 `cc-` 前缀并生成 `agents/openai.yaml`。
- Gemini 命名空间隔离：`GEMINI.md` 明确禁止 Gemini 把 `/new-feature` 等命令改派给 `cc-*` Codex/Claude skill，避免写错路径。

### 值得借鉴

- **P0 借鉴：命名空间隔离**。如果我们加入 Gemini，必须明确 `.omc/collaboration` 是共享协作状态，`.codex/`、`.gemini/`、`.claude/` 是各工具私有配置，禁止跨写。
- **P0 借鉴：受管区块/manifest**。若未来要自动安装 Gemini/Codex/Claude 配置，不要整目录覆盖用户配置。采用 managed block、manifest、备份和 dry-run。
- **P1 借鉴：三层规则模型**。常驻 rules 保持短；领域知识放 skills；流程放显式 workflow。我们的协议也应保持短，复杂操作放脚本或专项文档。
- **P1 借鉴：安装验证**。脚本安装后检查目录是否有内容、profile 是否同步、命令是否存在。我们可以给 Gemini 集成加 `check-gemini.sh`。
- **P2 借鉴：跨平台 skill 生成**。如果本项目要沉淀可复用协作 skill，再考虑做 Claude/Gemini/Codex 三端同步。

### 不建议直接照搬

cc-use-exp 有强个人/全局偏好，且大量配置写到用户主目录。我们的协作机制应优先项目内最小可复现，不应在未经用户明确同意时修改 `~/.gemini`、`~/.codex`、`~/.claude`。

### Gemini CLI 集成可行性

很高。cc-use-exp 已经验证 Gemini CLI 的配置面包括：

- `~/.gemini/GEMINI.md`
- `~/.gemini/commands/*.toml`
- `~/.gemini/skills/*/SKILL.md`
- `~/.gemini/rules/*.md`
- `~/.gemini/policies/*.toml`

但对本项目最小可行路径应是项目内脚本调用 `gemini -p`，而不是先引入全局配置同步。

## 4. 项目四：Claude-Team

地址：https://github.com/smart-lty/Claude-Team

### 核心模式与架构

Claude-Team 是 Claude 作为主入口，通过 MCP 调 Codex 和 Gemini 的“角色分工模板 + 安装脚本”。

关键设计：

- Claude 是 orchestrator。
- Codex 是代码实现/调试 advisor。
- Gemini 是超长上下文 analyst。
- `setup.sh` 检测 `claude/codex/gemini`，然后通过 `claude mcp add` 安装：
  - Codex MCP：`uvx --from git+https://github.com/GuDaStudio/codexmcp.git codexmcp`
  - Gemini MCP：`npx -y gemini-mcp-tool`
- 根据安装情况写入 `CLAUDE.md`、`.codex/AGENTS.md`、`.gemini/GEMINI.md` 模板。

### 值得借鉴

- **P0 借鉴：清晰角色路由**。Gemini 适合大上下文、长日志、多文件分析；Codex 适合实现与 review；Claude/主 agent 做协调和最终判断。这个边界适合直接写进我们的协议。
- **P1 借鉴：安装/健康检查向导**。`setup.sh` 的“检测工具 -> 安装 MCP -> 验证 -> 安装模板”流程可改造成项目内 `scripts/check-ai-tools.sh`，先只做只读检查。
- **P1 借鉴：advisor 非权威**。模板反复强调工具是 advisor，不是最终权威；这点对 Claude/Codex/Gemini 三方分歧处理很重要。

### 风险与不足

- 当前 README 宣称“自动决定何时调用 Codex/Gemini”，但实际主要靠 Claude 指令模板和 MCP，缺少共享事件日志、锁、artifact 协议。
- `setup.sh` 会修改用户级 Claude MCP 与模板，适合个人环境，不适合直接作为项目内协作协议。
- 模板中部分模型名可能随时间变化，不能硬编码为长期协议。
- 本机 `claude mcp list` 未显示 `codex` 或 `gemini-cli` MCP，所以 Claude-Team 的 MCP 路径当前未配置完成。

### Gemini CLI 集成可行性

可行，但有两条路径：

- 直接 CLI：当前即可用，命令形态为 `gemini -p "<prompt>" --approval-mode plan --output-format text`。适合只读分析和 artifact 输出。
- Claude MCP：需要安装 `gemini-mcp-tool` 并验证 `claude mcp list` 出现 `gemini-cli`。适合 Claude 主导调度，不直接帮助 Codex 调 Gemini。

对当前项目，建议先选直接 CLI，后续再讨论是否安装 MCP。

## 5. 综合优先级建议

### P0：立即值得做

1. **定义三 agent 角色路由**
   - Claude：需求澄清、综合决策、用户沟通、最终合成。
   - Codex：实现、代码审查、协议严谨性、可执行验证。
   - Gemini：只读大上下文分析、长日志/长文档/多文件扫描、第三方项目快速归纳。

2. **增加 Gemini 只读 artifact workflow**
   - 输入：任务问题、目标文件/目录、禁止写入说明。
   - 执行：`gemini -p ... --approval-mode plan --output-format text`。
   - 输出：`.omc/collaboration/artifacts/YYYYMMDD-HHMM-gemini-*.md`。
   - 事件：追加 `analysis_requested`/`artifact_created` 或现有兼容事件。

3. **固化“独立分析”协议**
   - 当任务要求独立意见时，agent 不读取对方同题 artifact。
   - 独立 artifact 完成后，再由指定 agent 做 comparison/synthesis。
   - 事件日志记录“未读取对方 artifact”的声明。

4. **补一个 journal/state 校验脚本**
   - 校验 JSONL 格式、重复 id、`state.last_event_id`、锁是否残留。
   - 只读校验优先，不急着做完整状态机。

### P1：下一步增强

1. **轻量 next-action 脚本**
   - 借鉴 Dev Buddy 被动状态机，只返回建议：claim、write artifact、request handoff、complete、needs_repair。
   - 不自动执行写入，避免过度复杂。

2. **任务级 checkpoint/gate**
   - 为需求、设计、实现、review、UAT/验收定义推荐 artifact 形态。
   - 高风险任务可强制 Claude/Codex/Gemini 两方以上交叉审查。

3. **安装健康检查脚本**
   - 检查 `claude/codex/gemini` 版本、`claude mcp list`、Gemini headless 模式、工作区权限。
   - 不修改用户目录，只报告下一步建议。

4. **受管配置策略**
   - 如果要写 `~/.gemini` 或 `~/.codex`，必须采用 managed block/manifest/backup/dry-run。

### P2：暂缓

1. 完整 Ralph pipeline、unit DAG、build loop、配置门户。
2. 跨平台 skill 自动同步。
3. 用户级全自动 MCP 安装和模板覆盖。
4. 任务面板投影、归档保留策略、长期运行进度 UI。

## 6. 与 Claude 讨论的关键问题

1. **Gemini 集成先走直接 CLI 还是 Claude MCP？**  
   我建议 P0 用直接 CLI，因为本机 Gemini 已安装且支持 headless；Claude MCP 当前未配置，安装会修改用户级 Claude 配置。

2. **Gemini 是否永远只读？**  
   我建议默认只读。只有用户显式要求 Gemini 参与改代码时，才用 worktree 或单独 patch artifact。

3. **是否把“独立分析不可读对方 artifact”写进协议？**  
   本次任务暴露出这是常见协作需求，应作为明确规则。

4. **现有 `events.jsonl` 中 active ownership 与用户指令冲突如何处理？**  
   本次 `TASK-20260530-03` 里 Claude 最后事件仍是 `in_progress`，但 state 的 `active_agent` 是 `none`，用户又明确要求 Codex 执行。我按用户指令接手并记录 event。协议需要定义“handoff/open-for-peer-analysis”的状态，避免以后只能靠解释。

5. **P0 脚本放哪里？**  
   可选：`.omc/collaboration/scripts/`。建议只放项目内脚本，不写用户主目录。

6. **多 agent synthesis 谁负责？**  
   建议默认由发起方或用户指定 agent 负责；如果没有指定，最后完成独立分析的 agent 只列问题，不擅自合并结论。

## 7. 推荐落地顺序

1. 更新协议：加入角色路由、独立分析规则、Gemini 只读原则、handoff/open-for-peer-analysis 状态。
2. 新增只读校验脚本：`validate-journal`。
3. 新增 Gemini advisor 脚本：输入 prompt + artifact path，执行 headless Gemini，写 artifact。
4. 增加健康检查脚本：检查 `gemini --version`、`gemini --help`、`claude mcp list`、`codex --version`。
5. 再评估是否引入 MCP 或更完整的状态机。

## 8. 结论

最值得借鉴的不是完整多 agent 框架，而是三点：

- Dev Buddy 的“被动状态机 + 磁盘状态 + 失败上下文持久化”。
- cc-use-exp 的“命名空间隔离 + 受管同步 + Gemini/Codex/Claude 配置边界”。
- Claude-Team 与 Shaka 指南共同体现的“Claude/Codex/Gemini 角色分工、独立分析、再合成”。

Gemini CLI 集成在本机具备直接可行性。P0 应以只读 artifact workflow 进入 `.omc/collaboration`，不要先安装 MCP 或复制大型配置体系。
