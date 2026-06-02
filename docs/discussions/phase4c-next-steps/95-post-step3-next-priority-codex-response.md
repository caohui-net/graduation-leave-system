# Phase 4C Step 3后续优先级讨论 - Codex响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对：** `94-post-step3-next-priority-request.md`  
**文档编号：** 95

---

## 审查结论

**推荐：B-prime - 进入 Step 4，但先做“同步计划/变更摘要服务”，把 dry-run 作为 Step 4 的第一验收面，而不是单独做 Step 3.5 演示命令。**

不建议选择 C。Step 4+5 组合会把服务层、数据库写入、命令入口、输出格式、错误处理一次性耦合，风险和返工面都偏大。

也不建议把 A 作为独立优先级。原因不是 dry-run 没价值，而是仅做 `sync_xg_users --dry-run` 命令容易把核心逻辑写在命令层，随后 Step 4 还要搬迁到服务层。更好的切分是：

1. **Step 4A：纯服务层 sync plan / dry-run summary，不写 DB**
2. **Step 4B：在服务层实现受限真实写入**
3. **Step 5：management command 只作为薄入口调用服务层**

---

## 关键发现

### P1：当前模型没有 mapper 输出的主要补充字段

当前 `map_xg_user_to_internal()` 输出 `phone` 和 `department`，字段覆盖契约也把 `phone`、`email`、`department`定义为 API 补充字段。

但当前 `User` 模型只有：

- `user_id`
- `name`
- `role`
- `active`
- `class_id`
- `is_graduating`
- `graduation_year`

没有 `phone`、`email`、`department` 持久化字段。

这意味着如果 Step 4 现在直接做“幂等 upsert 并写库”，实际可安全写入的 API 字段非常有限。`class_id`、`is_graduating`、`graduation_year`按共识不由 API 覆盖；`role`仅用于过滤学生；`user_id`是主键；剩下只有 `name` 可能可更新，但它属于 CSV 主导核心字段，不应在没有明确策略时被 API 静默覆盖。

**结论：Step 4 不能直接实现完整 API 补充字段 upsert。必须先做同步计划/报告，或先做模型字段扩展决策。**

### P1：字段契约与 mapper 对“新用户是否可创建”的边界需要由 Step 4 承担

字段契约明确 Phase 1 中学工 API 不创建新学生，因为缺少 `class_id`、`is_graduating`、`graduation_year`。

当前 mapper 对一个合法学生返回：

- `class_id=None`
- `is_graduating=None`
- `graduation_year=None`
- `skip_reason=None`

这对只读 mapper 是合理的，因为 mapper 只负责 API 字段标准化。但 Step 4 必须显式执行以下规则：

- 本地不存在的 API 用户：不创建，计入 `missing_local_user` 或 `would_create_but_blocked`
- 本地存在但核心字段缺失：不覆盖核心字段，计入冲突或跳过
- 本地存在且 API 字段可比对：只生成变更摘要，是否写入由后续 schema/策略决定

---

## Step 3.5价值评估

dry-run 有价值，但不应作为独立命令优先实现。

它的真正价值是：

- 让团队看到 API 返回数据经过 mapper 后的分类结果
- 统计 `skip_reason`
- 对比本地用户是否存在
- 暴露“能写什么、不能写什么”

但这些都属于同步服务层的核心计划能力，不属于 management command 的独有能力。没有真实凭证时，单独做命令也无法完成端到端 live 演示，只能在 mock 数据上输出报告；这更适合用服务测试固定下来。

**建议：把 Step 3.5 吸收到 Step 4A，而不是先做一个可能被重写的命令。**

---

## Step 4依赖检查

Step 4 不依赖 Step 3.5 命令。

Step 4 依赖的是：

1. mapper 输出契约稳定：已基本满足，8/8 测试通过。
2. API/CSV 并存策略清晰：已明确 API 不替代 CSV，不自动停用。
3. 写入字段范围清晰：**目前不满足**，因为模型缺少 `phone`/`department`/`email`。

因此可以进入 Step 4，但 Step 4 的第一个交付必须是“计划和报告”，不能直接上真实 upsert。

---

## 推荐实现范围

### Step 4A：同步计划服务（推荐立即做）

新增服务层，例如：

`backend/apps/users/services/xg_user_sync.py`

最小能力：

- 输入：`xg_users: list[dict]`
- 调用：`map_xg_user_to_internal()`
- 查询：本地 `User` 是否存在
- 输出结构化 summary，不写 DB

建议 summary 至少包含：

- `total_fetched`
- `mapped_count`
- `skipped_count`
- `skipped_by_reason`
- `existing_count`
- `missing_local_count`
- `would_update_count`
- `conflicts`
- `warnings`

最小判定规则：

- mapper 有 `skip_reason`：计入 skipped，不查写库。
- mapper 成功但本地用户不存在：不创建，计入 `missing_local_user`。
- 本地用户存在但不是 `student`：计入 conflict，不更新。
- 本地用户存在且是学生：生成可比对字段摘要。
- 当前没有模型字段承接 `phone`/`department`：输出 warning，不能声明可写入。

测试重点：

- mapper skip 透传统计
- 已存在学生进入 existing/update candidate
- 不存在学生不创建
- 本地角色冲突
- 不覆盖 `class_id`、`is_graduating`、`graduation_year`
- 无 phone/department 模型字段时输出明确 warning

### Step 4B：受限真实写入（需 Step 4A 后再决定）

只有在以下二选一决策明确后再做：

1. **模型扩展路线**：给 `User` 增加 `phone`、`email`、`department` 等 API 补充字段，再实现幂等更新。
2. **只更新姓名路线**：明确允许 API 更新已有用户 `name`，并定义 CSV 与 API 冲突优先级。

没有这个决策前，不应实现真实 DB upsert。

### Step 5：命令入口

Step 5 再新增：

`sync_xg_users --dry-run`

命令只负责：

- 创建 `XGUserAPIConfig` / `XGUserAPIClient`
- 调用 `fetch_all_users()`
- 调用 Step 4 服务
- 格式化输出 summary

命令不应承载同步规则。

---

## 风险评估

### 跳过 Step 3.5 的风险

风险较低，前提是 Step 4A 包含 dry-run summary 并有服务测试。

如果直接跳到真实写库，风险很高；但本建议不是直接写库，而是先做服务层计划报告。

### Step 4关键风险点

1. **无可写补充字段**
   - 当前模型与字段契约不一致，不能假装 `phone`/`department` 可 upsert。

2. **创建新用户边界**
   - API 缺少学生核心字段，Phase 1 不应创建新学生。

3. **核心字段覆盖策略**
   - `name`、`class_id`、毕业字段由 CSV 主导，API 覆盖必须有明确规则。

4. **停用策略**
   - 现在不实现自动停用，只输出差异报告。

5. **命令层膨胀**
   - 如果先写命令，后续服务层容易重复实现同步判断。

---

## 遗漏检查

mapper 对 Step 3 的目标基本完整，但有两个后续注意点：

1. mapper 返回 `phone`/`department` 是合理的，但 Step 4 不能把它们视为可持久化字段，除非模型扩展。
2. 字段契约中提到 `email`，但 mapper 当前不提取 `email`；如果未来模型扩展包含邮箱，需要补 mapper 和测试。

测试覆盖对只读 mapper 足够；对 Step 4 还缺服务级测试，尤其是本地存在性、角色冲突、不可创建、不可覆盖核心字段、summary 结构稳定性。

---

## 最终建议

选择 **B-prime**：

1. 立即执行 **Step 4A 同步计划服务**，内置 dry-run summary，不写 DB。
2. 暂不单独做 Step 3.5 命令。
3. 暂不做 Step 4B 真实 upsert，先由 Step 4A 暴露“当前无可写补充字段”的事实。
4. Step 4A 完成后，再决策是扩展 `User` 模型字段，还是只做报告/命令入口。

一句话结论：**dry-run 是必须的，但应先成为服务层能力；真实 upsert 需要先解决可写字段目标。**
