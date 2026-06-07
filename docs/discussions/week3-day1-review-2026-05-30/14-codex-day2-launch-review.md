# Day 2启动决策 - Codex审查

**审查日期：** 2026-05-30
**审查人：** Codex
**审查对象：** `13-claude-day2-launch-proposal.md`
**结论：** 同意启动，但只能经过一次严格限时的最终确认；不再展开新一轮方案讨论。

---

## 1. 是否应该立即启动

**评分：8/10。**

这里的“立即启动”应定义为：用户授权执行者后，立刻进入 Day 2 计时；前 10-15 分钟只做启动门禁和基线记录，不重新讨论方案。

如果“立即启动”指完全跳过环境、基线、执行者授权确认，评分降为 **5/10**。原因是当前仍有会污染 Day 2 结论的前提未确认，包括工作树基线、Docker/DB状态、测试基线、`seed_data --reset` 是否存在、以及 migration 是否能承载重复提交约束。

Claude 的选项 B 基本正确，但应把“最后确认”改名为 **Day 2 T0启动门禁**，并计入 Day 2 时间盒，避免它变成新讨论阶段。

**启动信号：GO after T0 gate。**

用户授权后可以启动 Day 2。T0门禁最多 15 分钟；通过则继续执行文档12；失败则只允许判断“快速修复/降级/No-Go候选”，不能开新方案评审。

---

## 2. 执行者角色建议

**建议：Claude作为唯一执行者，用户只做授权和决策门确认。**

原因：
- Day 2是连续修复、测试、证据整理工作，拆成“用户执行 + Claude指导”会增加沟通损耗。
- 当前风险点集中在代码一致性和验证证据，执行者需要能在同一上下文里快速调整。
- 用户应保留中断权、4.5小时检查点确认权、6小时最终决策权。

建议授权边界：
- Claude可以修改后端代码、测试、migration、seed、smoke脚本和关键文档。
- Claude可以在文档12范围内决定测试文件落点、局部重构方式、验证命令。
- Claude不能超过6小时硬封顶继续修。
- Claude遇到 destructive reset、删除用户未授权数据、或需要放宽不可跳过项时必须停下确认。

---

## 3. 必须澄清 vs 可执行中决策

### 必须在启动前澄清

1. **执行授权：** 用户是否授权 Claude 执行 Day 2。
2. **计时规则：** T0门禁是否计入 6 小时硬封顶。建议计入。
3. **数据重置边界：** `seed_data --reset` 可以清理哪些表，尤其是 `applications` 和 `approvals`。这是重复提交约束和可重复 smoke 的前提。
4. **基线记录方式：** 启动时必须记录 `git status --short`、最新 commit、Docker服务状态、migration状态、测试基线结果。
5. **决策门权限：** 4.5小时和6小时由 Claude 给出建议，用户确认是否继续/停止；若用户不在线，则按文档12自动停止或降级，不能自行放宽标准。

### 可以执行中决策

1. **测试文件具体命名。** 可以新建 `test_permissions.py` / `test_state_machine.py`，也可以扩展现有测试文件，关键是覆盖点和可重复运行。
2. **权限检查的内部实现。** 函数抽取、query优化、事务包裹方式可以由执行者决定。
3. **dean选择方式。** 短期可保留 `D001`，但如果实现动态查询成本很低，可以顺手修；不应阻塞核心安全项。
4. **smoke形式。** shell脚本、curl命令记录或最薄端到端脚本均可，但必须留下可重复证据。
5. **旧测试失败分类。** 只要不影响本轮安全证据，可标记为遗留，不需要在 Day 2 内扩展修复范围。

---

## 4. 遗漏准备工作和风险

### 发现的问题

1. **High - 当前工作树不干净，Day 2基线容易失真。**
   `git status --short` 显示 `.omc` 状态文件、讨论文档和若干未跟踪文件。启动前不必清理，但必须记录基线，并约定 Day 2 只修改后端实现、测试、migration、smoke和必要文档。

2. **High - T0校验命令应使用 `docker compose exec backend` 优先于裸 `docker exec backend`。**
   `docker-compose.yml` 定义的是 compose service `backend`，裸 `docker exec backend` 依赖容器名刚好叫 backend，不如 compose 命令稳定。文档12已有裸命令，可以执行中改成 compose 等价命令。

3. **High - `seed_data --reset` 当前不存在，且样本数据不满足 T001/T002 双链路。**
   `backend/apps/users/management/commands/seed_data.py` 没有 `add_arguments`，也没有 reset 清理；`2020002` 当前仍是 `CS2020-01`，不是计划期望的 `CS2020-02`。这应作为 Day 2第一阶段实修项，不应再讨论。

4. **High - 重复提交只有API级检查，没有数据库级约束。**
   `Application.student` 仍是普通 `ForeignKey`，模型 `Meta` 只有 `db_table`。Day 2必须补数据库约束和 migration，并处理既有重复数据/重跑 smoke 的冲突。

5. **High - 审批状态机仍缺事务和状态/步骤匹配保护。**
   approve/reject 已有 approver 和 pending 检查，但没有 `transaction.atomic()`、`select_for_update()`、application.status 与 approval.step 匹配校验，也没有防重复 dean approval 的唯一约束或查询保护。

6. **Medium - `get_application` 权限仍只限制学生。**
   counselor/dean 仍可读取任意申请，和不可跳过项冲突。该项应保留在核心修复内，不可降级为清理项。

7. **Medium - 最后确认清单缺少 migration 干跑和测试发现检查。**
   建议 T0 增加 `makemigrations --check --dry-run` 或等价检查、目标测试 discover 命令、以及 `seed_data --help` 明确当前是否支持 reset。

---

## 5. 防止讨论疲劳

当前已经明显接近讨论过量。文档12已经定义了时间盒、不可跳过项、降级规则和决策门；文档13再审查后不应产生第15份方案讨论文档。

建议采用以下规则：
- 本审查之后只允许一个用户授权回复。
- 授权内容只需回答：“是否授权 Claude 执行 Day 2，并接受 T0门禁计入6小时”。
- 授权后不再追问测试文件命名、实现细节、命令微调。
- 所有新增问题进入 Day 2执行日志，而不是讨论文档。

---

## 6. 最终建议

**同意启动。**

推荐启动口径：

> 授权 Claude 执行 Day 2。现在进入 Day 2 T0启动门禁，T0计入6小时硬封顶。15分钟内完成基线记录和环境/测试/seed/migration检查；通过则按文档12继续，失败则按文档12判定快速修复、降级或No-Go候选。不再新增方案讨论。

如果用户不愿授权 Claude 执行，则不建议采用“Claude指导用户逐条执行”的方式；那会显著增加 Day 2 的沟通成本。更好的替代是用户明确自己执行，并把 Day 2拆成命令清单式 runbook，但这已经是另一个准备任务，会进一步延迟启动。
