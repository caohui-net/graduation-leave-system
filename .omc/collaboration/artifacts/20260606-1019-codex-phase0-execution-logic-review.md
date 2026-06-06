# TASK-20260606-08 Phase 0数据验证后执行逻辑调整审查

**审查人:** Codex  
**日期:** 2026-06-06  
**审查范围:** Phase 2-3执行计划调整、兜底宿管员路由、271人学号更新、19人额外研究生处理  

## 总体结论

方案B（Fallback查询）作为短期方案合理，但当前落地版本不能直接验收：`backend/apps/applications/views.py` 已出现方案B式代码，却未导入 `User`，并且 fallback 条件过宽，可能掩盖非空楼栋的配置错误。

271人学号更新建议采用“源数据先修正 + 干净导入”为主策略；如果数据库已经产生申请/审批外键，则不能简单重导，也不能天真地修改 `User.user_id` 主键，必须走专用事务命令处理 FK 或在业务开启前重置导入。

19名额外研究生不应进入当前5946人主批次，建议先暂不处理，形成待确认清单；用户确认属于2026届且补齐班级/辅导员/楼栋策略后，再作为单独补充批次。

Phase 3需要前置“导入工具补齐/验收”任务。现有 `import_csv --students` 不消费 File5 表头，也不导入 `building_name`，且没有 `import_staff` 或 `update_tmp_ids...` 命令，任务清单不能只增加数据步骤。

## 1. 方案B是否合理

**问题**

方案B短期合理，但必须修正为“仅无楼栋学生 fallback”。当前方案文档和现有代码都倾向于“有楼栋但找不到宿管员也 fallback”，这会把真实配置错误静默路由到程婷。

代码现状：

- `backend/apps/applications/views.py:14` 只导入 `UserRole`，未导入 `User`。
- `backend/apps/applications/views.py:153`、`:162` 使用 `User.objects...`，会触发 `NameError`。
- `backend/apps/applications/views.py:153-157` 对非空楼栋找不到宿管员后继续 fallback。
- `backend/apps/applications/views.py:156-157` 多个宿管员时取 `.first()`，没有确定性约束。

**推荐方案**

短期采用方案B，但实现边界调整如下：

1. 导入 `User`，或使用 `get_user_model()`。
2. 只有 `user.building` 为空、NULL、纯空白时，路由到职工号 `92008149`。
3. 非空楼栋找不到宿管员时返回 404，并暴露 `building`，作为数据配置错误处理。
4. fallback 职工号不要散落硬编码，至少集中为常量；更好是放 settings，例如 `FALLBACK_DORM_MANAGER_USER_ID`。
5. 验证 fallback 用户必须 `role=dorm_manager` 且 `active=True`。

**理由**

这116人的业务问题是“无楼栋”，不是“所有楼栋路由失败”。非空楼栋失败通常意味着宿管员导入缺失、楼栋名称不一致或数据清洗错误，fallback 会让错误进入审批流，后期很难追溯。

方案B无需迁移，适合当前阶段快速恢复116人提交能力；相比方案A，不污染 `building` 语义；相比方案C，成本低。

**风险**

- 硬编码 `92008149` 可维护性弱。
- fallback 用户未导入时，116人仍会提交失败。
- 如果未来存在多个兜底宿管员，方案B无法表达分流策略。
- 当前测试无法验证，因本地执行 Django 测试时缺少 Django 依赖。

**调整建议**

Phase 2增加以下验收：

- 有楼栋且有宿管员：审批人是对应楼栋宿管员。
- 无楼栋/空白楼栋：审批人是 `92008149` 程婷。
- 非空楼栋但无宿管员：返回 404，不 fallback。
- fallback 用户不存在/非宿管/ inactive：返回 404。
- 多个 active 宿管员负责同一楼栋：导入或校验阶段失败，不在申请时随机 `.first()`。

长期在生产稳定后升级为方案C：增加 `is_fallback_dorm_manager` 或独立路由配置表，消除业务身份与职工号硬绑定。

## 2. 271人学号更新策略推荐

**问题**

271人当前是临时ID到真实学号的主键级修正。`User.user_id` 是主键，申请表通过 FK 引用学生；如果数据库已经有申请/审批数据，直接更新主键或全量重导都有外键和历史一致性风险。

现有导入工具也不支持直接重导 File5：

- `backend/apps/users/management/commands/import_csv.py:51` 要求 `student_id,name,class_id,is_graduating,graduation_year`。
- File5 表头是 `source_row_id,user_id,user_id_source,student_no,name,...,building_name,room_number,...`。
- `import_csv.py:93-101` 不写入 `building`、`department`、`phone`、`email`。
- 当前没有 `import_staff` 或 `update_tmp_ids_with_real_student_no` 命令。

**推荐方案**

推荐“双层策略”：

1. 生产正式导入前：采用方案B的“源数据修正”思路，先把271人的真实学号写回源数据/生成 `file5_students_merged_v2.csv`，再从干净库导入。不要把临时ID导入生产库。
2. 若数据库已导入临时ID且尚无申请/审批数据：可清空学生相关导入数据后，用 v2 File5 干净重导。
3. 若数据库已有申请/审批数据：不要全量重导；新增专用 management command，在事务内做 TMP->真实学号映射、冲突检测、FK处理和审计记录。

**理由**

在业务开启前，源数据修正最干净，可以消除临时ID残留；但一旦产生申请记录，`user_id` 作为主键会放大风险。此时“数据库直接更新”必须是 FK-aware 的专用命令，而不是简单 `user.user_id = real_id; save()` 或 `update_or_create(real_id)`。

**风险**

- 仅靠姓名精确匹配虽然当前271/271成功，但执行前仍需校验真实学号唯一、TMP唯一、真实学号未被现有用户占用。
- 重新导入如果在脏库运行，可能创建真实学号新用户并留下TMP旧用户。
- 修改主键可能破坏 `applications.student_id`、`approvals.approver_id` 等外键引用，具体取决于数据库约束，不应假设自动级联。
- 导入器不支持 File5 字段时，即使重导成功，也可能丢失楼栋数据，导致路由继续失败。

**调整建议**

Phase 3前新增“数据导入工具补齐”：

- 支持 File5 表头：`user_id`、`name`、`department`、`class_id`、`building_name -> User.building`、`phone`、`email`、`graduation_year=2026`、`is_graduating=True`。
- 提供 `--dry-run`，输出 created/updated/skipped/conflicts。
- 对271映射执行预检：271条、TMP唯一、真实学号唯一、姓名一致、真实学号不存在或只对应同一人。
- 明确禁止在已有 active applications 时执行破坏性重导；如必须更新，走 FK-aware 专用命令并备份。

## 3. 19名额外研究生处理建议

**问题**

19人来自290人研究生文件和“无入住信息”文件，但不在 File1/File2/File5 中。当前项目主批次权威范围是5946人，直接纳入会改变主批次边界，且缺少班级、辅导员、毕业状态确认和路由依据。

**推荐方案**

当前主批次暂不纳入；建立 `19人待确认补充清单`，请用户确认：

1. 是否属于2026届毕业离校范围。
2. 是否应进入本系统主批次。
3. 是否有班级/学院/辅导员映射。
4. 无楼栋时是否同样走程婷兜底。

用户确认后，作为单独补充批次导入，不回写污染 File1/File2 的原始口径。

**理由**

这19人说明数据源不一致，但不是当前 File5 的漏合并问题。贸然加入会让“5946主批次”的验收口径变成5965，并可能引入新的辅导员/宿管覆盖缺口。

**风险**

- 若这19人确实属于2026届且需要办理离校，暂不处理会导致遗漏服务对象。
- 若无班级映射，导入后辅导员审批无法路由。
- 若只补学生不补路由和宿舍状态，会制造新的提交失败或错误审批。

**调整建议**

将19人作为 Phase 3.5“可选补充批次”，进入条件是用户书面确认和字段补齐。验收标准：

- 19人是否纳入有明确决定。
- 纳入时每人有唯一学号、姓名、学院/班级、辅导员映射、宿管路由策略。
- 不纳入时保留差异报告和用户确认记录。

## 4. Phase 3任务调整评估

**问题**

当前任务调整只增加了数据动作，但缺少工具和前置校验。按现有代码，`import_staff`、`update_tmp_ids...` 不存在；`import_csv --students` 也不能导入 File5 楼栋字段。若直接进入 Phase 3，会出现命令不存在、楼栋丢失、管理员角色不完整等问题。

另一个迁移一致性风险：`UserRole.ADMIN` 已在模型中存在（`backend/apps/users/models.py:10`），但 `0003` 迁移的 role choices 只到 `student/dorm_manager/counselor/dean`（`backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:25-28`）。CharField choices通常不形成数据库约束，但应运行 `makemigrations --check`，避免迁移状态漂移。

**推荐方案**

调整后的优先级：

1. Phase 2.1：修正方案B路由实现和测试，导入 `User`，收窄 fallback 条件。
2. Phase 2.2：补齐数据导入命令能力：File5学生导入、staff/admin/dorm_manager导入、dry-run和冲突报告。
3. Phase 3.0：执行数据预检：File5 v2 5946人、271真实学号、116无楼栋、3名管理员、楼栋宿管覆盖、辅导员覆盖。
4. Phase 3.1：用修正后的 File5 v2 从干净库导入学生；若非干净库，先做数据库状态门禁。
5. Phase 3.2：导入/校验宿管员和辅导员路由数据。
6. Phase 3.3：导入3名新增管理员，尤其是 `92008149` 必须在申请开放前存在且 active。
7. Phase 3.4：跑端到端路由验收：有楼栋、无楼栋、非空楼栋无宿管员。
8. Phase 3.5：19人补充批次，等待用户确认后执行。

**理由**

申请创建依赖学生楼栋和兜底宿管员；学生导入又依赖导入器正确映射 File5 字段；271学号修正属于主键口径，必须在业务数据产生前处理。任务顺序应围绕依赖关系，而不是按文件类型机械导入。

**风险**

- 若先开放申请再处理271人，后续主键修正成本显著升高。
- 若先导入学生再导入程婷，116人申请会失败。
- 若导入器不写 `building`，5830人的楼栋路由也会退化。
- 若把非空楼栋失败 fallback 到程婷，会掩盖宿管员导入质量问题。

**调整建议**

Phase 3验收标准建议：

- 学生总数：5946，且无 `TMP2026_` 用户进入生产正式库。
- 271人真实学号全部存在，TMP不存在或已被安全迁移。
- 116名无楼栋学生允许存在，但提交申请路由到 `92008149`。
- 非空楼栋学生的宿管覆盖率达到100%，不能依赖 fallback。
- 辅导员路由覆盖率100%。
- 3名新增管理员存在、角色正确、手机号导入；程婷为 `dorm_manager`、active、building为空。
- 所有导入命令支持 dry-run，并在正式执行前输出0 conflict。
- 最小E2E测试通过：有楼栋学生提交、无楼栋学生提交、未知楼栋提交失败、程婷能看到待审批列表。

## 验证情况

已读取审查请求、协作协议、Codex审查协议、兜底路由方案、271人报告、无楼栋差异报告、相关模型/视图/导入命令和CSV表头。

尝试运行最小申请流程测试：

```bash
python3 manage.py test apps.applications.tests.test_application_flow.ApplicationFlowTestCase.test_complete_application_flow -v 2
```

结果：本地环境缺少 Django，测试未执行成功。该验证缺口应在依赖环境恢复后补跑。
