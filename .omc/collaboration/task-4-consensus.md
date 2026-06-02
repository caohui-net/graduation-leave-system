# Task #4 共识：最小验证脚本 Phase 1a

**达成时间：** 2026-05-30  
**讨论轮次：** 2轮  
**参与方：** Claude, Codex

---

## 问题描述

**背景：** Task #1-#3 引入事件注册表、legacy/canonical 重建语义、repair 锁修复、Gemini 三方协作字段与权限模型。进入实施前需要一个最小验证脚本，防止新规则破坏既有协作日志，并证明关键新事件行为正确。

**核心风险：**

1. 硬编码既有事件数量会在日志增长后失效。
2. 纯 Bash 验证难以可靠处理 JSONL、状态重建和行为 smoke test。
3. 过早覆盖完整 repair、权限矩阵和性能测试会扩大 Phase 1a 范围。

---

## 最终方案

### 1. 架构

**共识：** 薄 Bash 入口 + Python 核心逻辑。

```text
.omc/collaboration/scripts/
  validate-phase1a.sh       # 薄入口
  validate_phase1a.py       # 主验证逻辑
  collab_schema.py          # 事件注册表和 schema 定义
  collab_journal.py         # JSONL 解析和状态重建
```

**原则：**

1. Bash 只负责定位目录、传参、退出码透传。
2. Python 负责 JSONL 解析、schema 校验、状态重建和 tempdir 行为测试。
3. 一个入口支持多个验证函数，可通过 `--check` 选择单项或组合执行。

### 2. 最小验证范围

Phase 1a 只包含 5 个 check：

```bash
1. journal-basic      # JSONL、id、必填字段、state.last_event_id
2. registry           # event type 分类完整性、无重叠、无未知类型
3. legacy-events      # 现有日志按 legacy/canonical 两种模式解释
4. state-schema       # 三方字段存在且权限值合法
5. behavioral-smoke   # tempdir测试：未知事件拒绝、INFO不改status、STATE_TRANSITION改status
```

### 3. legacy_cutoff 动态确定

**共识：** 不硬编码既有事件数量。

允许的动态来源：

1. 从 `events.jsonl` 读取最后一个旧规则事件的 id。
2. 或从 `state_rules_version_changed` / `state_rebuilt` 事件确定新规则生效点。

**当前约束：** 旧讨论中提到的 52 条事件已增长为 53 条，因此 Phase 1a 验证必须从日志和规则事件动态推导 cutoff，不能写死 `52`。

### 4. 失败处理分层

**只读汇总类 check：**

- 汇总所有发现的问题。
- 输出每项 check 的通过/失败状态。
- 最终用非零退出码表示整体失败。

**状态变更类行为：**

- 使用 tempdir 或隔离副本。
- 对写入、事件追加、状态更新失败采用 fail fast。
- 不在真实 `.omc/collaboration/` 上执行破坏性测试。

### 5. Phase 1a 边界

**包含：**

- 验证新事件注册表不会破坏现有日志。
- 验证 legacy/canonical 两种解释模式可运行。
- 验证三方协作 state schema 的基础字段和权限枚举。
- 验证关键事件行为：未知事件拒绝、INFO 不改 `status`、STATE_TRANSITION 改 `status`。

**不包含：**

- `repair()` 完整流程测试，放入 Phase 1b。
- 权限完整矩阵测试，放入 Phase 1b。
- 性能测试，后续阶段处理。

---

## 关键决策

### 为什么不用硬编码 cutoff？

协作日志是 append-only，事件数量会持续增长。硬编码 `LEGACY_CUTOFF_EVENT_ID = 52` 会在新增任何事件后产生歧义，尤其当前日志已达到 53 条。cutoff 必须由日志内容或规则切换事件动态确定。

### 为什么保留 Bash 入口？

Bash 入口方便人工运行和 CI 集成，也符合现有 `.omc/collaboration/scripts/validate-journal.sh` 的使用习惯；复杂逻辑放入 Python，避免在 Bash 中手写 JSON 解析。

### 为什么 Phase 1a 只做 5 个 check？

Phase 1a 的目标是为 Task #1-#3 的实施提供最小安全网：不破坏旧日志，并证明新事件分类的关键行为正确。repair 全流程、权限矩阵和性能都需要更多场景，纳入 Phase 1b 更合适。

---

## 验证要求

实施完成后至少运行：

```bash
.omc/collaboration/scripts/validate-phase1a.sh
.omc/collaboration/scripts/validate-phase1a.sh --check journal-basic
.omc/collaboration/scripts/validate-phase1a.sh --check behavioral-smoke
```

预期结果：

1. 现有协作日志通过 `journal-basic`。
2. 所有事件类型均能被注册表归类，分类无重叠。
3. legacy/canonical 两种重建模式都能解释现有日志。
4. `state.json` 包含三方协作字段，权限值属于允许枚举。
5. tempdir smoke test 不修改真实协作日志。

---

## 下一步

1. 创建 `collab_schema.py`，集中定义事件分类、状态和权限枚举。
2. 创建 `collab_journal.py`，实现 JSONL 严格/兼容解析和状态重建。
3. 创建 `validate_phase1a.py`，实现 5 个 check 和 `--check` 参数。
4. 创建 `validate-phase1a.sh`，作为薄 Bash 入口。
5. 运行现有 `validate-journal.sh` 和新 Phase 1a 验证脚本。

**状态：** ✅ 共识达成，待实施
