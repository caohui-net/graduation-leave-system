# Phase 4C 下一步优先级讨论 - Codex响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对：** `90-next-priority-discussion-request.md`  
**文档编号：** 91

---

## 审查结论

**推荐优先级：选择 A，但收窄为“Step 2C-lite 字段映射契约”，随后进入 Step 3 的只读 Provider/映射测试。**

不建议直接执行选项 B 或 C 中的“学生数据同步命令并入库”。当前 `fetch_all_users()` 已经解决分页读取问题，但数据库写入不是下一个最低风险动作。下一步应先把学工字段、内部 `User` 字段、CSV补充字段、缺失字段处理规则固定下来。

建议顺序：

1. **Step 2C-lite：字段覆盖与映射契约**
2. **Step 3：只读 mapper / `UserInfoProvider` 设计与测试**
3. **Step 4：同步服务与幂等 upsert**
4. **Step 5：management command 运维入口**

这也与 doc 85 的阶段划分一致：doc 85 中 Step 3 是“字段映射与 Provider 设计”，Step 4 才是“同步服务与数据库写入”，Step 5 才是“管理命令或后台任务入口”。本次请求中的选项 B 实际上把 Step 3、Step 4、Step 5 合并了，风险偏高。

---

## 依赖关系分析

### Step 3是否强依赖Step 2C？

**强依赖，但不是依赖真实凭证；依赖的是字段映射决策。**

没有真实凭证时，仍然可以基于以下材料完成 Step 2C-lite：

- 学工文档样例字段：`name`、`number`、`phone`、`identity_id`、`department`、`user_identity`、`updated_at` 等
- 当前内部 `User` 模型字段：`user_id`、`name`、`role`、`active`、`class_id`、`is_graduating`、`graduation_year`
- 当前 CSV 导入命令的业务要求：学生导入要求 `student_id`、`name`、`class_id`、`is_graduating`、`graduation_year`
- 现有 `ClassMapping` 约束：学生 `class_id` 需要能匹配辅导员映射

因此 Step 2C 不是“等 live probe 才能做”的硬阻塞项，而是一个必须先落地的同步契约。

### 能否在实现Step 3时增量确定字段覆盖？

可以增量修正字段覆盖，但不应在入库同步命令里首次确定字段覆盖。

合理边界是：

- mapper / provider 测试阶段可以增量调整字段映射；
- DB upsert 阶段不应再临时决定必填字段、默认值、缺失字段策略；
- management command 阶段只负责执行已确认的同步计划，不应承载字段决策。

---

## 风险评估

### 直接跳到Step 3/同步命令的主要风险

1. **误写入风险**
   - 如果 `number` 是否等同 `student_id` 未确认，可能把错误字段作为 `User.user_id` 主键。
   - 主键一旦写错，后续修复会涉及用户、申请、审批、通知等关联数据。

2. **权限链风险**
   - 当前业务依赖 `class_id` 和 `ClassMapping` 做辅导员可见性控制。
   - 学工API文档样例没有明确稳定的 `class_id` 字段；如果用院系/专业/班级名称临时拼接，可能导致辅导员看不到学生或看到错误班级。

3. **毕业生范围风险**
   - CSV 导入要求 `is_graduating` 和 `graduation_year`。
   - 学工API样例字段未证明能提供这两个字段。若默认所有学生都是毕业生，会扩大系统范围；若默认否，会导致毕业生缺失。

4. **角色识别风险**
   - `user_identity` 可能能区分学生/老师，但值域未确认。
   - 未定义值域映射前，直接入库可能把辅导员、学生或其他人员角色写错。

5. **回滚成本风险**
   - 只读 mapper 的错误可通过测试修正。
   - 入库命令的错误需要数据清理、关联检查和审计摘要，成本更高。

### 缺失字段覆盖文档会导致什么问题？

最直接的问题是同步命令无法判断“成功”是什么意思。它只能证明 API 返回了用户列表，不能证明这些用户足以支撑本系统的毕业离校业务。

尤其需要提前写清：

- `number -> User.user_id` 是否成立；
- `name -> User.name` 是否必填；
- `user_identity -> User.role` 的值域；
- `class_id` 从哪里来，学工API没有时是否继续依赖 CSV；
- `is_graduating`、`graduation_year` 从哪里来，缺失时是否禁止入库；
- API 缺失用户时是否停用本地用户，还是仅报告差异。

---

## 效率考量

**最快达到可工作状态的方式不是直接写同步命令，而是先做一个短平快的字段契约。**

推荐 Step 2C-lite 控制在一个小交付内：

1. 创建字段覆盖表，不追求真实字段全集，只覆盖“同步写库必需字段”。
2. 把字段分为四类：
   - API可直接提供
   - API可能提供但需 live probe 确认
   - 必须由 CSV/手工配置提供
   - 暂不支持或禁止默认推断
3. 明确同步门槛：
   - 没有 `number/name`：不可创建用户
   - 没有 `class_id`：不可替代当前学生 CSV 主路径
   - 没有 `is_graduating/graduation_year`：不可声明毕业生筛选可用
   - 没有辅导员映射：不可自动创建 `ClassMapping`
4. 产出 mapper 测试用例输入/输出样例。

完成这个文档后，Step 3 的 mapper/provider 可以很快实现，而且测试目标明确。反过来，如果直接写 DB 同步命令，测试会被迫同时覆盖字段猜测、数据转换、幂等 upsert、事务和命令输出，反馈周期会变慢。

---

## 遗漏检查

Step 2系列还有一个关键遗漏：**字段覆盖报告不能只列 API 字段，还必须列内部写库字段和缺失字段策略。**

建议 Step 2C-lite 至少包含以下表：

| 内部目标 | 来源字段 | 状态 | 处理规则 |
| --- | --- | --- | --- |
| `User.user_id` | `number` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
| `User.name` | `name` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
| `User.role` | `user_identity` | 值域未知 | 只接受明确学生值；未知值跳过并报告 |
| `User.class_id` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
| `User.is_graduating` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
| `User.graduation_year` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
| `ClassMapping` | 未确认 | 缺失 | 不由学工用户API自动生成 |

还建议补充两个基础设施决策，放入 Step 2C 或 Step 3：

1. **API 与 CSV 并存策略**
   - 在字段未完全覆盖前，API 只能补充或更新可确定字段，不能替代 CSV 导入。

2. **缺失/停用策略**
   - 初期不要因为 API 本次未返回某用户就自动停用本地用户；先输出差异报告，等 live 数据稳定后再决定停用规则。

---

## 推荐执行方案

### 下一步：Step 2C-lite

产出文件建议：

`docs/phase4c-xg-field-coverage.md`

内容建议：

1. 学工API文档样例字段清单
2. 内部 `User` / `ClassMapping` 写库字段清单
3. 字段映射表
4. 缺失字段处理规则
5. API/CSV 并存策略
6. Step 3 mapper 测试样例

验收标准：

- 能明确哪些字段允许 API 写入，哪些字段仍由 CSV/手工来源维护；
- 能明确什么情况下跳过记录、报告错误、禁止同步；
- 能为下一步 mapper/provider 测试提供固定输入输出。

### 随后：Step 3

实现范围建议收窄为：

- 新增纯转换函数或 `UserInfoProvider`；
- 输入为 `fetch_all_users()` 返回的用户列表；
- 输出为内部标准化用户 DTO / dict；
- 不写数据库；
- 单元测试覆盖字段缺失、角色未知、班级缺失、毕业字段缺失等场景。

### 再后：Step 4/5

等 mapper 通过测试后再做：

- 幂等 upsert；
- dry-run 变更摘要；
- 冲突报告；
- 不自动停用本地缺失用户；
- management command 入口。

---

## 替代方案

如果团队非常希望马上看到可执行命令，可以采用折中方案：

**创建 `sync_xg_users --dry-run`，但只做读取和映射报告，不写数据库。**

这本质上仍然是 Step 2C-lite + Step 3 的组合，不是完整同步命令。它可以提高可见性，同时避免未确认字段导致误写库。

---

## 最终建议

**不要跳过 Step 2C。**

但 Step 2C 不应拖成大文档任务，而应作为一个短周期、可执行的字段映射契约。完成后进入只读 mapper/provider；再进入 DB upsert；最后再封装 management command。

本轮推荐决策：

**A-prime：Step 2C-lite 字段映射契约优先，禁止直接实现写库同步命令。**
