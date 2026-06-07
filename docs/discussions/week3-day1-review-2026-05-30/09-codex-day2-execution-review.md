# Day 2执行策略 - Codex审查

**日期：** 2026-05-30
**审查人：** Codex
**审查对象：** `08-claude-day2-execution-proposal.md`
**结论：** 方向基本可行，但不能按"立即开始 + 主要手工验证 + 可跳过阻塞项"原样执行。需要增加短前置校验、最低自动化测试和不可跳过边界，否则容易得到假阳性的 Conditional Go。

---

## 一、5个关键问题回应

### 1. 立即开始 vs 准备后开始

**不同意纯粹立即开始。** 建议采用"15-30分钟前置校验后立即执行"，并把这段计入 Day 2 timebox。

必须先确认：
- 当前代码基线与提案一致。现有代码里 `approval.approver_id` 校验和 `approval.decision != pending` 已经存在，但事务、锁、动态 dean、数据库唯一约束仍缺失。
- 测试基线是否能跑。仓库已有 Django 测试，不能假设只能靠 curl。
- Docker/数据库/migration/seed 能否稳定运行。
- `seed_data --reset` 的语义是否包含清理 applications/approvals；否则加了"一人一申请"约束后 smoke test 不能重复跑。

缺少这一步会让 Day 2 中途才发现测试基线或数据状态不可用，反而更浪费 timebox。

### 2. 串行执行 vs 并行执行

**基本同意串行，但不赞成把任务2-4视为可随意跳过的独立项。**

合理顺序是：
1. Seed/mock/reset 先完成，因为它决定后续正向路径是否可复现。
2. 权限、状态机、重复提交应作为一个一致性修复组推进，代码可以串行改，但验证要合并成一组回归。
3. Smoke test 不应等所有代码写完才开始，可在第1阶段后先搭骨架，后续填断言。
4. 文档可以最后同步，但执行过程中应记录真实命令和响应，避免最后凭记忆改文档。

如果只有一个执行者，"并行"收益有限；更重要的是把阻塞边界定义清楚。

### 3. 手工验证 vs 自动化测试

**不同意只做手工验证。** 手工 curl 可用于运行时证据，但 Day 2 至少需要补最小自动化回归。

必须自动化的任务：
- 跨辅导员 approve/reject 返回 403。
- 重复审批返回 409，且不会重复创建 dean approval。
- application.status 与 approval.step 不匹配时返回 409。
- 重复提交由数据库唯一约束兜底，API 返回 409。
- 正向路径仍能从学生提交走到最终 approved。

理由：这些都是安全/一致性回归点，且仓库已经有 `backend/apps/*/tests/` 测试结构，新增针对性 Django 测试比后续靠人工复验可靠。`tests/smoke_test.sh` 可以作为端到端运行脚本，但不能替代模型/API层回归测试。

### 4. 时间分配

**3小时执行 + 1小时缓冲的说法不成立。** 提案列出的 6 个阶段本身已经是 4小时，没有真实缓冲。

更现实的 Day 2 估算：
- 前置校验：15-30分钟。
- Seed/mock/reset：30-60分钟，取决于是否清理业务数据并更新两套模板路径。
- 权限 + get_application + dynamic dean：45-75分钟。
- 状态机事务/锁/重复 dean 防护：90-120分钟。
- 重复提交数据库约束 + migration + IntegrityError：60-90分钟。
- 最小 Django 自动化测试：60-90分钟。
- Smoke script 正向路径：60-90分钟。
- 文档同步并复制执行验证：30-60分钟。

因此，4小时只能争取"核心止血 + 最低证据"；6小时更接近完成 Conditional Go。若坚持4小时，必须把列表接口、完整负向 smoke、ClassMapping防御、并发压力验证推到 Day 3。

### 5. 阻塞应对策略

**"超时50%后评估跳过"过于机械。** 是否能跳过应按决策门，而不是按分钟。

绝对不能跳过：
- Seed/mock/reset 能稳定生成 T001/T002 两条链路。
- approve 和 reject 都校验 assigned approver。
- 审批必须只允许 pending approval 且 application.status 匹配 step。
- 辅导员通过只能创建一个 dean approval。
- 重复提交必须有数据库级约束，并且 API 返回 409。
- 最低自动化测试和正向 smoke 至少有一个可重复执行证据链。
- 文档必须更新到不会误导下一位执行者。

可以跳过或推迟：
- 列表接口，但只能宣称 Conditional Go，不能正式 Go。
- smoke test 中的负向场景脚本化，如果 Django 自动化测试已经覆盖负向用例。
- ClassMapping二次防御校验。
- 并发压力测试。
- 共享权限函数的重构形式；只要 approve/reject 行为正确，可以 Day 3 清理重复代码。

---

## 二、可行性评分

**评分：6/10。**

提案方向与 Day 2 共识一致，任务拆分也覆盖了主要漏洞。但执行策略低估了测试和数据可复现成本，"手工验证为主"和"允许跳过阻塞项"会削弱 Conditional Go 的可信度。若加入前置校验、最低自动化测试和不可跳过边界，评分可提升到 7.5/10。

---

## 三、遗漏的风险和准备工作

1. **测试基线风险。** 仓库已有 Django 测试，但现有测试数据没有明显创建 `ClassMapping`，而提交申请依赖班级映射；需要先确认测试能否通过并修正 fixture。
2. **reset语义风险。** `seed_data` 当前使用 `get_or_create`，不会更新既有用户的 `class_id`；即使改成 `update_or_create`，也不一定清理 applications/approvals。重复 smoke 会被唯一约束挡住。
3. **数据库约束迁移风险。** 给 `Application.student` 加唯一约束前，需要确认测试库/开发库没有重复数据，并处理 migration 失败路径。
4. **事务验证风险。** `select_for_update()` 需要在真实数据库事务中验证；如果只用普通 curl 串行验证，无法证明并发下不会重复创建 dean approval。
5. **端点与文档漂移风险。** 提案里的部分 curl 缺少尾斜杠，但当前 URL 是 `/api/applications/` 和 `/api/approvals/<id>/approve/`。文档还需同步 `app_...`/`apv_...` 这类实际ID格式，而不是简单写"UUID"。
6. **list接口契约风险。** 之前契约修复曾移除 `GET /api/applications` 列表端点；Day 2 共识又把列表接口作为正式 Go 门槛。执行前需要确认这不是契约回退。
7. **dynamic dean语义风险。** "从 User 表查询 dean"需要定义 active 条件、多个 dean 的选择规则、没有 dean 时的错误码。

---

## 四、过于乐观的估算

- **状态机保护 1小时偏乐观。** 事务、锁、状态匹配、重复 dean 防护、approve/reject 两条路径和测试至少需要 1.5-2小时。
- **重复提交约束 30分钟偏乐观。** migration、历史数据、IntegrityError、事务包裹和测试至少 1小时。
- **Smoke test 1小时偏乐观。** 登录、动态ID提取、状态码断言、reset/cleanup、错误输出处理通常超过1小时。
- **文档同步 30分钟只够编辑，不够验证。** 如果要求从文档复制命令执行，至少预留 45-60分钟。
- **列表接口 1.5小时偏乐观。** 还涉及契约确认、URL冲突、角色过滤、序列化和测试，实际可能是 2小时以上。

---

## 五、任务完成/跳过边界

**必须完成后才可 Conditional Go：**
- 阶段1：Seed/mock/reset，且正向样本可重复提交验证。
- 阶段2：assigned approver 权限覆盖 approve/reject；`get_application` 不再让任意 counselor/dean 查看所有申请。
- 阶段3：审批状态机保护覆盖 approve/reject，且不会重复生成 dean approval。
- 阶段4：重复提交数据库级约束 + API 409。
- 阶段5：正向 smoke 可执行，或等价的端到端自动化证据。
- 阶段6：文档同步到真实端口、token字段、尾斜杠、ID格式、seed/reset步骤。

**可以 Day 3 完成：**
- 列表接口。
- smoke shell 脚本中的完整负向场景，前提是 Django 测试已覆盖负向用例。
- ClassMapping二次校验。
- 并发压力测试。
- 权限函数重构和代码清理。

---

## 六、对6个阶段的具体审查

1. **Seed/mock修复：** 内容不完整。需要把 `--reset` 明确为 idempotent，并决定是否清理 applications/approvals；否则 smoke test 不能重复跑。Provider 方法名实际是 `check_status`，不是 `get_status`。模板路径不只 `docs/templates/`，还包括 `backend/data/templates/`。
2. **审批权限修复：** 方向正确，但现有代码已部分实现 assigned approver 检查；剩余重点应转为 reject 复核、`get_application` 角色权限、dynamic dean 和测试。`get_application` 现在只限制学生，counselor/dean 仍可看任意申请。
3. **状态机保护：** 必须覆盖 approve 和 reject。只校验重复审批不够，还要校验 step/status 匹配，例如 dean approval 不能在 `pending_counselor` 状态下被操作。
4. **重复提交约束：** 必须保留数据库约束，不能只靠 `exists()`。需要 migration 和 IntegrityError 兜底；同时明确 MVP 是否允许 rejected 后重新提交。
5. **Smoke test骨架：** 建议支持 `BASE_URL` 环境变量，不要只硬编码；脚本必须检查 HTTP status，并在开头执行 reset/cleanup。
6. **文档同步：** "ID格式改为UUID"表述不准确，当前实际 ID 是 `app_`/`apv_` 前缀短ID。文档要按实际代码或同步修改代码，不能模糊。

---

## 七、对3个风险的补充评价

Claude识别的3个风险都成立，但不全面：
- Seed/mock 风险的核心不是 provider 逻辑复杂，而是 reset/idempotency 和业务表清理。
- 状态机风险不只是语法不熟，而是事务边界、锁顺序、状态匹配和重复 dean 创建需要一起成立。
- Smoke test 风险不只是 jq 调试，而是环境启动、数据复位、HTTP状态码断言和契约漂移。

建议新增风险：测试基线不可用、migration失败、列表接口契约冲突、动态 dean 多记录/缺失、手工验证无法证明并发正确性。

---

## 八、替代执行方案

如需保持 Day 2 硬 timebox，建议改成：

1. **0:00-0:30 前置校验：** git diff、migration状态、现有测试、Docker/API可用性、seed可执行。
2. **0:30-1:15 数据复位与seed/mock：** 完成 `--reset`、2020002/T002链路、provider和模板同步。
3. **1:15-3:15 核心一致性修复：** 权限、状态机、动态 dean、唯一约束、事务。
4. **3:15-4:45 最低自动化测试：** 添加并运行关键 Django tests。
5. **4:45-5:45 正向 smoke + 文档同步：** 记录真实命令和响应。
6. **5:45-6:00 决策门：** 只按不可跳过项判断 Conditional Go/No-Go。

如果4小时到点但核心一致性和最低自动化测试未完成，应判定 No-Go，而不是把未完成项简单推到 Day 3。
