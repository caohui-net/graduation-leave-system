# Codex Implementation Plan Review

**Task ID:** TASK-20260605-03
**Review target:** `docs/用户需求最终确认与实施方案.md`
**Reviewer:** Codex
**Date:** 2026-06-05

## 审查结论

当前方案的业务方向基本正确：用 File1 作为学生基准、改为“楼栋宿管员 -> 学院辅导员”的 2 级审批、把学工管理员定位为只读角色，整体符合用户最新决策。

但文档不能按“所有 P0 已解除，可开始实施”执行。至少 3 个阻塞点仍未闭合：空学号/空 `user_id` 无法导入、楼栋多宿管员与当前单审批人模型冲突、`ClassMapping`/`dean`/`class_id` 的代码契约改造范围被明显低估。

评分：

| 维度 | 分数 |
|---|---:|
| 业务逻辑完整性 | 7/10 |
| 技术可行性 | 5/10 |
| 数据一致性 | 6/10 |
| 实施风险控制 | 4/10 |
| **总分** | **22/40** |

结论：需要修改后再实施。

## P0 问题清单

1. 空学号学生无法导入，与“全部 5830 行可导入”矛盾
   - 位置：`docs/用户需求最终确认与实施方案.md:33-42`, `docs/用户需求最终确认与实施方案.md:171-175`
   - 证据：现有 `User.user_id` 是主键且唯一；`UserManager.create_user()` 明确要求 `user_id` 非空。见 `backend/apps/users/models.py:12-17`, `backend/apps/users/models.py:28-31`。
   - 影响范围：File2 未匹配学生、研究生、登录账号、审批记录外键、通知和导入脚本。
   - 建议修正：实施前必须定义缺学号学生的稳定主键策略。推荐使用可追溯的临时账号，如 `TMP2026_{file1_row_no}` 或 `GRAD2026_{hash(name+college+building+room)}`，并在 File5 中增加 `source_row_id`、`user_id_source`、`student_no` 三类字段，避免把“登录账号主键”和“真实学号”混为一个字段。

2. “任一宿管员可审批”与当前审批模型不兼容
   - 位置：`docs/用户需求最终确认与实施方案.md:126-130`, `docs/用户需求最终确认与实施方案.md:248-255`, `docs/用户需求最终确认与实施方案.md:450-461`
   - 证据：当前 `Approval.approver` 是单个用户外键；创建申请时只创建一个宿管审批记录。见 `backend/apps/approvals/models.py:14-22`, `backend/apps/applications/views.py:172-179`。方案中的 `return dorm_managers` 没有定义如何落到审批记录、权限过滤、重复审批和通知。
   - 影响范围：提交申请、审批列表、详情权限、并发审批、通知、审计。
   - 建议修正：MVP 不要实现“任一人可审批”的组任务，除非增加 group approval 模型。更现实的 P0 修正是要求 File3 或映射表生成一个 `primary_dorm_manager_user_id`，每栋楼唯一主责宿管员；其他宿管员作为后续代理/备份扩展。

3. `ClassMapping` 移除工作量被低估，当前方案遗漏提交和流转入口
   - 位置：`docs/用户需求最终确认与实施方案.md:321-324`
   - 证据：现有提交申请直接查 `ClassMapping` 并用它创建宿管审批，见 `backend/apps/applications/views.py:147-179`；宿管审批通过后仍用 `ClassMapping` 创建辅导员审批，见 `backend/apps/approvals/views.py:149-174`；详情权限也按 `ClassMapping` 判断，见 `backend/apps/applications/permissions.py:11-23`。
   - 影响范围：后端接口、权限、数据库迁移、导入命令、前端类型、测试套件和文档契约。
   - 建议修正：把 Phase 2 拆成明确的改造清单：数据模型、提交路由、审批通过路由、列表过滤、详情权限、附件权限、导入命令、API schema、前端/miniprogram 类型、测试 fixture。未完成前不能导入真实数据并开放提交。

## P1 问题清单

1. 数据差异口径不一致
   - 位置：`docs/用户需求最终确认与实施方案.md:33-40`
   - 问题：文档同时写“File2 没有的 155 行”和“271 研究生 + 116 File2 独有”。这两个口径不能同时成立。按 5830 和 5675 的净差是 155，但若存在 271 个 File1 独有和 116 个 File2 独有，交集应为 5559。
   - 建议修正：File5 生成报告必须输出 `file1_only_count`、`file2_only_count`、`matched_count`、`ambiguous_match_count`、`duplicate_key_count`，并把 File2 独有 116 行明确列为“不导入但归档报告”或“追加导入”。

2. 状态机名称与现有代码不一致，迁移边界不清
   - 位置：`docs/用户需求最终确认与实施方案.md:218-234`, `docs/用户需求最终确认与实施方案.md:316-319`
   - 证据：现有状态是 `pending_dorm_manager / pending_counselor / pending_dean / approved / rejected`，不是文档里的 `PENDING / DORM_MANAGER_APPROVED / COUNSELOR_APPROVED / COMPLETED`。见 `backend/apps/applications/models.py:6-12`。
   - 建议修正：最终状态应继续使用 API 现有风格，例如 `pending_dorm_manager -> pending_counselor -> approved`。删除或迁移 `pending_dean`，并补充历史数据迁移规则。

3. 学工管理员与既有 `dean` 角色关系未定义
   - 位置：`docs/用户需求最终确认与实施方案.md:98-115`, `docs/用户需求最终确认与实施方案.md:326-329`
   - 证据：后端已有 `UserRole.DEAN`，前端类型也只有 `student | counselor | dean`，见 `backend/apps/users/models.py:5-9`, `frontend/types/api.ts:4-15`。
   - 建议修正：明确是复用并重命名 `dean` 为只读管理员，还是新增 `admin` 并迁移/废弃 `dean`。推荐短期复用 `dean` 的只读语义，文案改为“学工管理员(dean/admin display name)”，代码层是否改枚举放到单独 migration。

4. 路由键没有做申请时快照，后续人员/学院/楼栋变更会破坏审计
   - 位置：`docs/用户需求最终确认与实施方案.md:85-96`, `docs/用户需求最终确认与实施方案.md:178-182`
   - 问题：如果只从 `User.department/building_name` 动态读取，学生学院或宿管映射更新后，历史申请的可见范围和审批追溯会变化。
   - 建议修正：`Application` 增加申请时快照字段：`student_building_name`、`student_room_number`、`student_department`、可选 `route_version`。`Approval` 已保存审批人和姓名，可保留。

5. 学院/楼栋规范化缺少完整字典和阻断标准
   - 位置：`docs/用户需求最终确认与实施方案.md:285-293`, `docs/用户需求最终确认与实施方案.md:357-361`, `docs/用户需求最终确认与实施方案.md:438-448`
   - 问题：只给示例，没有说明 19 个学院、33 个楼栋的完整映射来源、冲突处理和失败阈值。
   - 建议修正：将 `college_normalization_map.json` 和 `building_normalization_map.json` 列为 Phase 1 必交付；导入门禁应是 100% 路由覆盖，任何未匹配、重复唯一键、空路由键都阻断。

6. 数据导入 Phase 缺少对现有导入命令的替换范围
   - 位置：`docs/用户需求最终确认与实施方案.md:336-355`
   - 证据：现有 `import_csv` 仍要求学生 `class_id`，并校验 `ClassMapping` 存在。见 `backend/apps/users/management/commands/import_csv.py`。
   - 建议修正：新增或重写导入命令，不要在文档里直接使用不存在的 `import_students/import_counselors/import_dorm_managers` 命令名，除非 Phase 2 明确包含这些命令实现。

7. 2.5-3 天估算偏乐观
   - 位置：`docs/用户需求最终确认与实施方案.md:314-388`
   - 问题：现有后端、前端、miniprogram、测试和 API 契约都依赖原 3 级/班级模型。1-1.5 天系统调整加 0.5 天前端不足以覆盖迁移、测试修复和回归。
   - 建议修正：按 4-6 天估算更现实；或切分为“后端闭环 MVP”和“前端/管理员视图完善”两个里程碑。

8. 缺少回滚策略
   - 位置：`docs/用户需求最终确认与实施方案.md:436-472`
   - 问题：风险章节只有缓解，没有数据库迁移失败、导入失败、上线后路由错误的回滚路径。
   - 建议修正：补充上线前备份、迁移可逆性、导入 dry-run、导入批次号、删除/回滚本批数据脚本、功能开关或维护窗口方案。

## P2 建议清单

1. 前端调整不要只写“4 类用户界面”，应明确小程序、frontend、demo-web 是否都要同步。
2. 测试用例应增加负向权限：宿管员不能看其他楼栋、辅导员不能看其他学院、管理员不能审批、学生不能访问审批列表。
3. 寝室号未来升级建议优先建独立映射表，不建议把 `room_numbers` JSONField 作为长期方案；独立表更容易做唯一约束和导入差异报告。
4. 通知文案需要随审批步骤更新，避免继续提示“学工部审批”。
5. API 文档和 TypeScript 类型应列入交付物，否则前后端状态枚举会漂移。

## 修正建议

1. 先把文档状态从“所有 P0 阻塞已解除”改为“业务方向确认，实施前仍需关闭 P0 技术/数据门禁”。
2. 增加 Phase 0：数据画像和路由门禁。
   - 输出 File1/File2 匹配报告。
   - 输出完整学院/楼栋规范化字典。
   - 输出缺学号学生账号生成策略。
   - 输出每名学生的宿管和辅导员路由结果。
3. 把楼栋多宿管员规则收敛为一个 MVP 决策。
   - 推荐：每栋楼唯一主责宿管员。
   - 后续再做多人队列或代理审批。
4. 重新设计数据模型变更。
   - `User` 增加学生楼栋、寝室、专业、年级字段。
   - `Application.class_id` 改可空或废弃展示依赖，并新增申请时路由快照字段。
   - 明确 `dean` 到 `admin` 的迁移或复用策略。
5. 重排实施顺序。
   - Phase 0 数据门禁。
   - Phase 1 后端模型和路由，带单元测试。
   - Phase 2 导入命令 dry-run 和真实导入。
   - Phase 3 前端/小程序/API 类型同步。
   - Phase 4 端到端和权限回归。
   - Phase 5 备份、上线、回滚演练。

## 最低通过条件

实施前至少满足以下条件：

1. 5830 行学生均有非空稳定 `user_id`。
2. 每个学生都能唯一确定一个宿管审批主体，或系统模型已支持多人待办。
3. 每个学生都能唯一确定一个学院辅导员。
4. `ClassMapping` 依赖清单已全部替换或兼容。
5. `pending_dean/dean` 的迁移策略明确。
6. 导入脚本支持 dry-run，并输出 100% 路由覆盖报告。
7. 有数据库备份和导入批次回滚方案。
