# Day 2计划 - Codex批判性审查

**日期：** 2026-05-30  
**审查对象：** `03-day2-plan-review-request.md`  
**审查者：** Codex  
**结论：** 需要修改后执行

---

## 1. 评分

**5/10。**

计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。

---

## 2. 时间估算评估

**4小时不现实。** 更现实的估算：

| 工作项 | Claude估算 | 建议估算 | 原因 |
|---|---:|---:|---|
| 测试/数据基线修复 | 未单列 | 0.5-1h | 当前测试依赖`ClassMapping`，但部分测试setUp未创建映射；host环境也未安装Django，验证入口未稳定 |
| Seed/mock修复 | 0.5h | 0.5-1h | `get_or_create(defaults=...)`不会修复已有脏数据，还要同步CSV模板和负向样本 |
| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
| 状态机/事务保护 | 1h | 2-3h | 需要原子更新application+approval，防重复创建Dean approval，并补并发/重复测试 |
| 重复提交竞态 | 0.5h | 1.5-2h | 需要先决定被驳回后是否可重新提交，再设计约束、迁移和IntegrityError处理 |
| 列表接口 | 可选 | 1.5-2h | 可重复验收和真实审批入口都需要它 |
| smoke test | 1h | 1.5-2.5h | 动态token/ID、reset策略、负向场景、错误输出都要处理 |
| 文档同步 | 0.5h | 0.5-1h | 不止验收清单，seed要求、CSV模板、合同文档可能都漂移 |

**建议：**
- 如果Day 2是硬4小时，只能定义为“P1止血版”：seed/mock、审批权限、状态机基础保护、重复提交约束、最小smoke骨架。不能宣称全部P1完成。
- 如果目标是“Day 2后可重复验收”，应预留**8-12小时**，或者拆成Day 2核心修复 + Day 3验收固化。

---

## 3. 优先级调整建议

建议顺序调整为：

1. **先恢复测试与数据基线。** 修`2020002`、Mock、CSV模板、测试fixtures，让T001/T002两条链路可构造。否则后续权限和smoke都没有可靠样本。
2. **审批权限与状态机合并修。** 二者在同一个approve/reject事务里实现，不应分散修改。
3. **重复提交竞态。** 先做业务决策，再加数据库约束、迁移和异常处理。
4. **列表接口。** 至少实现待办列表；否则“可重复验收”仍靠内部ID传递。
5. **smoke test。** 可以先写骨架，但最终应在核心接口稳定后完成，且最好使用列表接口发现待审批记录。
6. **文档同步最后做。** 文档应由实际接口和smoke脚本反向校准。

---

## 4. 每个P1修复的改进方案

### P1-1 审批权限

Claude方案“只校验`approval.approver_id == request.user.user_id`”是必要但不完整。

应改为统一权限函数，同时用于approve和reject：
- `approval.step`与`user.role`匹配。
- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
- 对辅导员，额外校验申请班级当前仍映射给该辅导员：`ClassMapping(class_id=application.class_id, counselor=user, active=True)`。这能防止历史/篡改approval把错误辅导员写进去。
- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。

### P1-2 状态机/事务保护

只校验`status`匹配`step`不够。

应在`transaction.atomic()`内：
- 用`select_for_update()`锁定`Approval`和对应`Application`。
- 先验证`approval.decision == pending`。
- 再验证状态机：`counselor`只能处理`pending_counselor`；`dean`只能处理`pending_dean`。
- approval更新、application状态更新、Dean approval创建必须在同一事务内完成。
- counselor approve创建Dean approval前检查是否已经存在该application的Dean approval，避免并发重复创建。
- 建议给`Approval`加约束：同一`application + step`最多一个approval，至少MVP阶段如此。

并发测试不能只用普通`TestCase`。SQLite下`select_for_update()`基本不能证明锁语义，应至少用`TransactionTestCase`覆盖重复请求返回409；真正并发正确性最好在Docker/Postgres环境跑集成测试。

### P1-3 重复提交竞态

`unique_together = ['student']`不是无条件正确，它隐含“一个学生终身只能有一个申请”。这会阻止被驳回后重新提交。

必须先定业务规则：
- **若MVP规则是一人只能有一个申请记录：** 可加`UniqueConstraint(fields=['student'], name='uniq_application_student')`，并在`create_application`中捕获`IntegrityError`返回409。保留`exists()`只作为友好提示，不能作为并发保护。
- **若允许驳回后重新提交：** 应使用条件唯一约束，只限制`draft/pending_counselor/pending_dean/approved`等活跃或终态成功申请；`rejected`可再次提交。或者不新建申请，而是允许在原申请上“重新提交/更新材料”。

无论哪种，创建Application和首个Approval也应放进事务，否则可能出现Application创建成功但Approval缺失的半成品。

### P1-4 Seed/mock数据

只修`2020002`不够，且“改一行seed默认值”不能修复已有数据库。

应做：
- `2020001 -> CS2020-01 -> T001 -> completed`
- `2020002 -> CS2020-02 -> T002 -> completed`
- 保留至少一个宿舍未完成样本，例如`2020003 -> pending/not_started`，否则会破坏现有宿舍阻断测试。
- 更新`backend/data/templates/students_template.csv`，目前模板中`2020002`仍是`CS2020-01`。
- `seed_data`用`update_or_create`或提供显式`--reset`，否则已有错误seed不会被修复。
- 更新现有测试中`2020002`作为宿舍阻断样本的假设，改用新的负向学生。

### P1-5 Smoke test

smoke test不能只是happy path curl集合。最低要求：
- `BASE_URL`默认`http://localhost:8001`，可通过环境变量覆盖。
- 解析`access_token`，不要假设`token`字段。
- 从创建申请响应或列表接口动态提取`application_id`和`approval_id`。建议依赖`jq`，脚本启动时检查依赖；或使用Python解析JSON。
- 支持显式重置，例如`SMOKE_RESET=1`时执行`migrate + seed_data --reset`。默认不应破坏开发数据。
- 验证正向链路：`2020002`提交后由`T002`审批，再由`D001`审批，最终状态`approved`。
- 验证负向链路：`T001`不能审批`2020002`的approval；重复审批返回409；重复提交返回409；错误step/status返回409。
- 每一步失败应打印HTTP状态、响应体和当前步骤名。

### P1-6 验收文档同步

只修端口、token字段、UUID格式ID、URL斜杠不够。

还应同步：
- `docs/week3-day0-seed-data-requirements.md`的正向/负向样本。
- CSV模板与实际`seed_data`。
- 验收清单应引用`tests/smoke_test.sh`作为主验证入口，curl命令作为展开说明，而不是两套可能漂移的事实来源。
- 若新增列表接口，合同/API文档也要更新。

### P1-7 列表接口

列表接口不应是可选。没有它，审批人不知道有哪些申请需要处理，Day 2仍然依赖“学生提交响应里带出的approval_id”或查库，不能称为可重复验收。

建议实现最小版本：
- `GET /api/applications/`根据当前登录用户角色自动过滤，不依赖`role`查询参数授权。
- 学生：只看自己的申请。
- 辅导员：只看自己负责班级，默认返回`pending_counselor`待办，可支持`?status=`。
- 学工部：只看分配给自己的`pending_dean`待办。
- 返回字段包含`application_id`、`student_id/name`、`class_id`、`status`、当前待办`approval_id`。

---

## 5. 遗漏问题识别

1. **查看权限漏洞被遗漏。** `get_application`只限制学生，未限制辅导员/学工部访问范围。
2. **现有测试fixtures不完整。** 创建申请依赖`ClassMapping`，但部分测试未创建映射；Day 2新增测试前应先修基线。
3. **host测试环境不可用。** 当前直接运行`python3 backend/manage.py test`失败：未安装Django。若验收依赖Docker，计划需明确Docker命令。
4. **迁移成本未估算。** Application唯一约束、Approval唯一约束都需要migration，并要考虑已有重复数据如何处理。
5. **seed命令幂等但不纠错。** `get_or_create`不会更新已有错误数据，Day 2修复后旧环境仍可能失败。
6. **approve/reject重复逻辑风险。** 两个函数权限、状态机、事务应抽成共享处理路径，避免只修approve漏掉reject。
7. **D001硬编码没有治理方案。** 可以作为seed常量，但不应成为业务逻辑长期事实。

---

## 6. 决策门标准建议

Day 2不能用“完成4个P1”判定达标。**只要仍有未关闭P1，就不能进入Week 3扩展开发。**

建议决策门：

### Go

满足全部条件：
- `docker compose up`后可执行迁移和seed。
- `seed_data --reset`或等价流程能稳定生成T001/T002/D001和正负样本。
- 核心Django测试通过，至少覆盖申请、审批、驳回、权限、重复提交。
- smoke test从空/重置后的环境跑通正向闭环。
- smoke test覆盖至少三个负向场景：跨辅导员403、重复审批409、重复提交409。
- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
- 验收文档中的命令与实际脚本/API一致。

### Conditional Go

仅当列表接口或并发压力测试未完成，但有明确替代验证证据和Day 3首项任务时，允许进入“修复继续”状态；不允许进入扩展功能开发。

### No-Go

任一情况即No-Go：
- 跨辅导员审批仍可成功。
- 重复审批可改变状态或创建重复Dean approval。
- 重复提交仍可能创建多条Application。
- smoke test必须手工查数据库或硬编码ID。
- 只完成4个P1。

---

## 7. 关键风险点

1. **时间风险最高。** 4小时不足以同时完成代码、migration、测试、smoke和文档。
2. **并发验证风险。** SQLite/普通单元测试可能给出假安全，Postgres集成验证才有意义。
3. **业务规则未定。** 被驳回申请是否可重新提交会直接决定数据库约束设计。
4. **旧数据污染风险。** seed修复若不提供reset/update，Day 1环境可能继续沿用错误数据。
5. **权限面扩大风险。** 只修审批动作、不修列表和详情查看，会留下同等级的数据泄露问题。
6. **smoke destructive reset风险。** 自动flush会破坏开发数据，必须显式开关并限制环境。
7. **文档再次漂移风险。** 如果文档和脚本分别维护，Day 2后仍可能出现“文档通过、脚本失败”。

---

## 最终建议

Day 2计划应改成“先稳定验收基础，再修核心安全/一致性，再补可发现性和smoke”的执行方案。列表接口不应推迟；4小时只能做止血，不能作为P1关闭标准。真正的Day 2验收目标应是：**从重置环境开始，一条命令跑出正向闭环和关键负向断言，且不依赖人工查库或硬编码ID。**
