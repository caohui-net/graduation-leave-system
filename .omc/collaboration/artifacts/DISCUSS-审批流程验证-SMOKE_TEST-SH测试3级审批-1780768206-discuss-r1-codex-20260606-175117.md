./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:102:- ClassMapping校验防御的是"历史/篡改approval"场景
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:103:- 这个场景在MVP阶段不会发生（没有修改approval的接口）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:111:if approval.approver_id != request.user.user_id:
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:118:- 学工部D001硬编码应该修复（从User表查询唯一dean）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:128:- ✓ 验证`approval.decision == pending`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:130:- ✓ 防止重复创建Dean approval
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:148:- 防止重复创建Dean approval（exists检查）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:195:- ✓ 动态提取application_id/approval_id
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:326:- 位置：`backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:327:- 修复：校验`approval.approver_id == request.user.user_id`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:334:- 位置：`backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:337:- 修复：验证`approval.decision == pending`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:338:- 修复：验证`application.status`匹配`approval.step`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:339:- 修复：防止重复创建Dean approval（exists检查）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-revi
ew.md:354:- 实现：动态提取token/application_id/approval_id
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:24:-
 N2 Cross-counselor negative test: ✓ 通过
./docs/discussions/codex-review-2026-05-27/04-database-review.md:70:WHERE status
 = 'pending_counselor'
./docs/discussions/codex-review-2026-05-27/04-database-review.md:97:-- approvals
表
./docs/discussions/codex-review-2026-05-27/04-database-review.md:98:CREATE INDEX
 idx_app_time ON approvals(application_id, approval_time DESC);
./docs/discussions/codex-review-2026-05-27/04-database-review.md:164:- 无`counse
lor_id`（只有`current_approver_id`会变）
./docs/discussions/codex-review-2026-05-27/04-database-review.md:180:    counsel
or_id BIGINT COMMENT '辅导员ID',
./docs/discussions/codex-review-2026-05-27/04-database-review.md:190:    FOREIGN
 KEY (counselor_id) REFERENCES users(id),
./docs/discussions/codex-review-2026-05-27/04-database-review.md:192:    INDEX i
dx_counselor_id (counselor_id),
./docs/discussions/codex-review-2026-05-27/04-database-review.md:244:WHERE statu
s IN ('draft', 'pending_counselor', 'pending_admin')
./docs/discussions/codex-review-2026-05-27/04-database-review.md:251:        if
self.status in ['draft', 'pending_counselor', 'pending_admin']:
./docs/discussions/codex-review-2026-05-27/04-database-review.md:254:
     status__in=['draft', 'pending_counselor', 'pending_admin'],
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:41:-
 Attachment: `application.class_id == user.class_id` OR matching approval
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:42:-
 Application detail: `ClassMapping(counselor=user, class_id=application.class_id
, active=True)`
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:62:
           counselor=user,
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:68:
       # Must have pending dean approval
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:72:
           step=ApprovalStep.DEAN,
./docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.m
d:48:- backend/apps/approvals/views.py
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:72
:- `User.role`有明确值域：`student`/`counselor`/`advisor`/`dean`/`admin`
./docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:7
2:  - test_upload_forbidden_counselor ✅
./docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-
response.md:21:4. 明确幂等语义：同一 `approval`、同一接收者、同一 `approval_time
out_warning` 只创建一条通知。
./docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-
response.md:54:python manage.py send_approval_timeout_warnings --dry-run
./docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-
response.md:55:python manage.py send_approval_timeout_warnings
./docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-
response.md:61:create_approval_timeout_warnings(now=None, dry_run=False) -> summ
ary
./docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-
response.md:73:- counselor 阶段阈值为 3 天，dean 阶段阈值为 2 天。
./docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-
response.md:77:  - `recipient = approval.approver`
./docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-
response.md:79:  - `type = approval_timeout_warning`
./docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-
response.md:80:  - `entity_type = approval`
./docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-
response.md:81:  - `entity_id = approval.pk`
./docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-respons
e.md:60:契约写 `APPLICATION_SUBMITTED` 关联 `application`，但服务实际用 `entity_
type='approval'`、`entity_id=approval.pk` 创建通知。考虑接收者是辅导员，通知入口
要处理的是待审批记录，当前实现使用 `approval` 更合理。
./docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-respons
e.md:62:**建议：** 本次修订 `notification-contract-v0.1.md` 时一并把 `APPLICATIO
N_SUBMITTED` 的关联实体改为 `approval/{approval_id}`，避免后续 Phase 2B 文档只修
宿舍阻断而留下旧冲突。
./docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-respons
e.md:137:- 同步修正 `APPLICATION_SUBMITTED` 的实体为 `approval/{approval_id}`，
匹配现有服务实现。
./docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:78:
   - list权限 (RBAC: 学生own/辅导员class/学工部dean)
./docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:104
:3. **RBAC复杂度:** 辅导员/学工部权限检查依赖approval scope，是否会导致N+1查询？
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:46:2.
 辅导员通过后，学生收到一条`APPROVAL_APPROVED`通知，关联counselor approval
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:47:3.
 学工部通过后，学生收到一条`APPROVAL_APPROVED`通知，关联dean approval
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:52:8.
 自动通知测试与既有application/approval/notification tests全部通过
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:62:-
幂等通知创建函数：`notify_application_submitted()`, `notify_approval_decided()`
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:63:-
在业务视图中调用通知服务（`create_application`, `approve_approval`, `reject_appr
oval`）
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:79:-
实现`notify_application_submitted(application, approval)`
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:80:-
实现`notify_approval_decided(approval)`
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:85:-
`backend/apps/approvals/views.py:approve_approval`：决策后调用`notify_approval_d
ecided`
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:86:-
`backend/apps/approvals/views.py:reject_approval`：决策后调用`notify_approval_de
cided`
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:113:a
pprover_role = "辅导员" if approval.step == "counselor" else "学工部"
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:118:a
pprover_role = "辅导员" if approval.step == "counselor" else "学工部"
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:119:m
essage = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:65:
    counselor=user,
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:74:
    step=ApprovalStep.DEAN,
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:81:This mus
t include `ApprovalDecision.PENDING` for dean access, matching current applicati
on detail behavior. A dean with historical non-pending approval should not gain
attachment visibility unless Contract v0.3 deliberately changes the application-
detail contract too.
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:120:- assig
ned counselor allowed
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:121:- cross
-counselor forbidden
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:122:- dean
with pending approval allowed
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:123:- dean
with non-pending or unrelated approval forbidden
./docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:4
0:仓库已经有基础命令 `backend/apps/users/management/commands/import_csv.py`，支
持students、counselors、mappings三类CSV导入。但它目前仍是开发辅助级别，不是可验
收的数据导入工具：
./docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:4
3:- `import_csv.py:62-75`映射导入读取的是 `counselor_id`，而数据对接文档使用的是
 `counselor_employee_id`，字段命名存在契约漂移风险。
./docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:8
5:- 统一CSV字段名：students、counselors、class mappings与 `docs/数据对接说明文档
.md` 一致。
./docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:29:-
 同步修正APPLICATION_SUBMITTED实体为approval
./docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:42:
  - 改为 `entity_type: approval, entity_id: approval_id`
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-respon
se.md:33:- `approval_approved`
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-respon
se.md:34:- `approval_rejected`
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-respon
se.md:61:- `approve_approval`/`reject_approval`成功后学生通知是否通过API可见；
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-s
trategy-response.md:86:- 辅导员通知：`type=application_submitted`、`entity_type=
approval`、`message`包含学生姓名或学号。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-s
trategy-response.md:87:- 学生审批通过通知：`type=approval_approved`、`entity_typ
e=approval`、`message`包含`辅导员`或`学工部`。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-s
trategy-response.md:88:- 学生审批驳回通知：`type=approval_rejected`、`message`包
含本次提交的驳回原因。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-s
trategy-response.md:90:如果要断言`entity_id`，注意API当前返回的是数据库主键字符
串，而不是业务`approval_id`。这由通知服务用`approval.pk`写入决定。smoke脚本拿到
的是`approval_id`，所以不能直接拿`apv_xxx`和`entity_id`比较，除非先通过详情响应
或通知列表建立映射。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-s
trategy-response.md:102:- auth、applications、approvals、attachments、notificati
ons端点出现在schema中。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-s
trategy-response.md:130:这不是阻塞项，因为服务层测试已覆盖`entity_id=approval.pk
`，但若下一步smoke要验证`entity_id`，最好同步补1-2个API测试断言，避免脚本和API语
义漂移。
./docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy
.md:18:- ✅ 修正APPLICATION_SUBMITTED实体（approval）
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:3:**文档编号：** 06-approval-workflow-change-requirement
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:37:    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:38:    PENDING_DEAN = 'pending_dean', '待学工部审批'
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:45:    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:46:    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:51:**文件：** `backend/apps/approvals/models.py`
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:55:class ApprovalStep(models.TextChoices):
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:56:    COUNSELOR = 'counselor', '辅导员'
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:57:    DEAN = 'dean', '学工部'
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:60:class ApprovalStep(models.TextChoices):
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:61:    DORM_MANAGER = 'dorm_manager', '宿管员'
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:62:    COUNSELOR = 'counselor', '辅导员'
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:69:- `backend/apps/approvals/views.py` - 审批列表过滤、审批操作
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:70:- `backend/apps/approvals/providers.py` - 自动分配审批人逻辑
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:81:- `backend/apps/approvals/tests/test_state_machine.py`
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:82:- `backend/apps/approvals/tests/test_permissions.py`
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:83:- `backend/apps/approvals/tests/test_rejection_flow.py`
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:86:- 所有测试中的 `self.counselor` → `self.dorm_manager`（第一审批人）
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:87:- 所有测试中的 `self.dean` → `self.counselor`（第二审批人）
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:88:- 状态断言从 `pending_counselor` → `pending_dorm_manager`
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:89:- 状态断言从 `pending_dean` → `pending_counselor`
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:106:- 如果数据库中已有 `pending_counselor` 或 `pending_dean` 状态的申请，需要
数据迁移脚本
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:116:2. 更新 `ApprovalStep` 枚举
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:148:- 先检查数据库中是否有 `pending_counselor` 或 `pending_dean` 记录
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:166:- 检查 `User.role` 是否支持 `dorm_manager` 角色
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:174:- [ ] 后端模型枚举已更新（ApplicationStatus, ApprovalStep）
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:194:- 实施时需要确认 `User.role` 是否支持 `dorm_manager` 角色
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.
md:201:   - 检查 `User` 模型是否支持 `dorm_manager` 角色
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decis
ion.md:6:**回应：** 08-codex-dean-filing-ui-decision
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decis
ion.md:59:- 列表页标题：`role === 'dean' ? '备案查询' : '审批列表'`
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decis
ion.md:60:- 空状态文案：`role === 'dean' ? '暂无已通过备案申请' : '暂无待审批申
请'`
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decis
ion.md:61:- 详情页操作区：`if (role === 'dean') { hide approval buttons }`
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decis
ion.md:63:**miniprogram/pages/approvals/approvals.wxml:**
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decis
ion.md:68:- 审批按钮显示逻辑：`canApprove && userInfo.role !== 'dean'`
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decis
ion.md:73:- `backend/apps/applications/views.py:list_applications` - dean 返回 `
status=approved` 申请
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decis
ion.md:74:- `backend/apps/approvals/views.py:list_approvals` - dean 返回所有审批
记录
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decis
ion.md:117:1. 修改 `pages/approvals/approvals.wxml` 页面标题
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:3:**
文档编号：** 08-codex-dean-filing-ui-decision
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:17:-
 数据仍使用后端已支持的 dean 角色查询逻辑，只展示 `status=approved` 的申请。
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:36:-
 **选项 B**通过“备案查询”Tab 明确语义，但 dean 角色天然只看 approved 数据时，“全
部 / 待审批 / 已审批 / 备案查询”这些 Tab 对学工部并没有真实业务意义，反而暗示还
有审批过滤。
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:48:
  - 后端已支持 dean 查看 approved 申请。
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:93:>
 复用现有审批列表和详情页，按 dean/学工部角色把页面语义改为“备案查询”，列表只展
示已通过申请，详情页保持只读。
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:125:
   - 当前 dean API 已固定返回 approved。
./docs/discussions/ui-design-2026-06-02/01-ui-requirements-analysis.md:10:- 审批
列表页面骨架（miniprogram/pages/approvals/）
./docs/discussions/ui-design-2026-06-02/02-gemini-review-request.md:29:   - mini
program/pages/approvals/（审批列表）
./docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md:3:*
*文档编号：** 10-final-consensus-dean-filing-ui
./docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md:39:
- `miniprogram/pages/approvals/approvals.wxml` - 页面标题
./docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md:42:
**后端改动：** 无（已支持 dean 查看 status=approved）
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:20:**Codex指出：** 文档写 `password123/counselor/dean/dorm_manager`，实际
学生密码=学号，辅导员=`T001/T002`，学工部=`D001`，宿管员账号未创建
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:26:- seed_data.py 未创建任何 dorm_manager 角色用户
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:27:- class_mapping.py:7 需要 dorm_manager 外键，当前映射表无法完成
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:50:- config/urls.py:8 实际路径 `/api/auth/`, `/api/applications/`, `/api/
approvals/`
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:67:- GET /api/approvals/ - 查询审批列表（支持decision参数）
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:68:- POST /api/approvals/{id}/approve/ - 通过审批
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:69:- POST /api/approvals/{id}/reject/ - 驳回审批
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:86:**Codex指出：** 文档说宿管员登录后进入审批列表，但 approvals.ts:19 只
允许 `['counselor', 'dean']`
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:89:- miniprogram/pages/approvals/approvals.ts:19 `checkRoleAndRedirect(ap
p.globalData.userInfo, ['counselor', 'dean'])`
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:108:// miniprogram/pages/approvals/approvals.ts:19
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:109:if (checkRoleAndRedirect(app.globalData.userInfo, ['counselor', 'dean
', 'dorm_manager'])) return;
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:186:- approvals/views.py:72 `decision_param = request.query_params.get('d
ecision', 'pending')`
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-rev
iew.md:187:- approvals.ts:15 `currentTab: 'pending' as 'all' | 'pending' | 'appr
oved'`
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:35:- C
ounselor access checks `application.class_id == user.class_id` or matching appro
val.
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:36:- A
pplication detail checks `ClassMapping(counselor=user, class_id=application.clas
s_id, active=True)`.
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:37:- D
ean attachment access allows any matching dean approval.
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:38:- A
pplication detail currently allows only own pending dean approval.
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:73:- U
pload forbidden: student cannot upload to another student's application; counsel
or/dean cannot upload.
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:75:- L
ist visibility: student own positive, student other negative, assigned counselor
 positive, cross-counselor negative, assigned dean positive or negative accordin
g to the final RBAC decision.
./docs/discussions/ui-design-2026-06-02/02-gemini-review-response.md:100:3.  重
构 `approvals.wxml` 和 `approvals.wxss` 中的列表项，实现卡片化和状态标签。
./docs/discussions/ui-design-2026-06-02/02-gemini-review-response.md:125:*   **
时间线数据支持：** 详情页中的审批历史时间线需要后端提供数组格式的审批节点记录。
当前 `detail.approvals` 已有这个结构，但需要确认其是否包含按时间正序/倒序排列的
完整节点。
./docs/discussions/ui-design-2026-06-02/02-gemini-review-response.md:132:*   当
前 `approvals.ts`, `detail.ts`, `student-application.ts` 的业务逻辑（如网络请求
、数据绑定）无需修改。
./docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md:81:|
 `/pages/approvals/` | 审批列表页 | 查看待审批/已审批列表 | ✅ 已实现（待优化）
|
./docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md:96:|
 学生功能 | 我的申请列表页 | P2 | 学生查看历史申请（可选，可复用approvals页） |
./docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md:110:
#### 审批列表页 (`approvals`)
./docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md:141:
| 4 | `/pages/approvals/` | 审批列表页 | 待审批/已审批列表 | ✅ 已有 |
./docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md:149:
| 7 | `/pages/my-applications/` | 我的申请（学生） | 学生查看历史申请列表 | ❌
缺失（可复用approvals） |
./docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md:266:
- 我的申请页（学生专用，或复用approvals）
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:
170:权限矩阵只有3个角色（student/counselor/admin），但：
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:
180:counselor        # 辅导员（只能查看本年级）
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:
181:counselor_lead   # 年级组长（可查看本学院所有年级）
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:35
:1. `TRUNCATE users` 会触发外键约束冲突（applications.student_id、applications.c
ounselor_id、applications.admin_id都引用users.id）
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:49
:    role ENUM('student', 'counselor', 'admin') NOT NULL,
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:84
:- 历史申请记录中的 `student_id`、`counselor_id`、`admin_id` 仍然有效
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:12
0:    role ENUM('student', 'counselor', 'admin') NOT NULL,
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:13
8:        (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND studen
t_id IS NULL)
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:15
5:    else:  # counselor or admin
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:18
4:CREATE TABLE class_counselor_mapping (
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:18
6:    counselor_employee_id VARCHAR(50) NOT NULL,
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:19
2:1. 学生提交申请时，系统需要根据 `users.class_id` 查询 `class_counselor_mapping
` 确定辅导员
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:24
5:    counselor = User.query.filter_by(
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:24
6:        employee_id=mapping.counselor_employee_id,
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:24
7:        role='counselor'
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:24
9:    if not counselor or not counselor.is_active:
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:25
5:        counselor_id=counselor.id,  # 快照，不受后续映射变更影响
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:30
5:    import_type ENUM('student', 'counselor', 'class_mapping') NOT NULL,
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:33:- back
end/apps/approvals/tests/test_rejection_flow.py
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:70:
: '/pages/approvals/approvals';
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:162:4. ba
ckend/apps/approvals/tests/test_rejection_flow.py - 动态日期
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:170:4. mi
niprogram/pages/approvals/approvals.ts - 使用role-guard
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:172:6. mi
niprogram/pages/approvals/approvals.wxml - 快速修复列表显示
./docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-revie
w.md:136:- paginated approval list response if not inferred correctly
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:28:| 辅导
员 | counselor | ~50人 | 一级审批 | 人事系统 + 教务系统 |
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:118:- 辅导
员工号（counselor_employee_id）
./docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-st
rategy.md:62:1. 服务层：`create_approval_timeout_warnings(now=None, dry_run=Fals
e)`
./docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-st
rategy.md:63:2. Management Command：`send_approval_timeout_warnings --dry-run`
./docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-st
rategy.md:77:- 阈值：counselor 3天，dean 2天
./docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-st
rategy.md:96:- 新增：`create_approval_timeout_warnings()`函数
./docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-st
rategy.md:100:**文件：** `backend/apps/notifications/management/commands/send_ap
proval_timeout_warnings.py`
./docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-st
rategy.md:106:- 覆盖：counselor/dean超时场景
./docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:38:
**Rework risk: medium-high.** This spreads the same unverified miniprogram assum
ptions across more screens. The detail page needs improvement, but doing history
 pages and approval detail pages before validating current page patterns increas
es future cleanup.
./docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:40:
**Technical risk: medium.** These pages are less exposed to file API quirks, but
 they still depend on unverified navigation, role routing, WXML binding, and app
roval action behavior.
./docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:119
:- Counselor/dean can view/download according to backend RBAC.
./docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:130
:- Do not start broad history pages or new approval-detail pages until the attac
hment detail-page pattern has been validated.
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-
review.md:57:**注意：** entity_id是数据库pk，不是业务approval_id，断言时需注意。
./docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:3
1:**Codex正确。** `backend/apps/users/management/commands/import_csv.py`已存在，
支持students/counselors/mappings导入。但当前实现缺少：
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response
.md:28:- smoke 覆盖 H1 happy path、H2 counselor reject、N2 cross-counselor 403。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response
.md:34:- 46 号共识中的验收项写了“通知断言按本次实体过滤，不受旧数据干扰”。当前 s
moke 主要通过 message 内容过滤通知，例如包含 `2020001`、`辅导员`、`材料不齐全`，
不是通过当前 `approval_id` 或 `application_id` 过滤。由于推荐运行方式是 `SMOKE_R
ESET=1`，这不是本轮阻塞项，但应避免在总结中声称已经完全实现“按实体 id 过滤”。
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:75
:- 测试覆盖良好（applications/approvals/attachments/notifications）
./docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy
.md:164:- 按模块分组（auth/applications/approvals/notifications/attachments）
./docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy
.md:187:**任务2.3：approvals模块（30分钟）**
./docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy
.md:188:- /api/approvals/ - 列表端点
./docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy
.md:189:- /api/approvals/{approval_id}/approve/ - 审批通过
./docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy
.md:190:- /api/approvals/{approval_id}/reject/ - 审批驳回
./docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:170
:- `test_list_assigned_counselor_positive` ✅
./docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:171
:- `test_list_cross_counselor_negative` ✅
./docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:172
:- `test_list_dean_pending_approval_positive` ✅
./docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.
md:56:- 修改：`application/{application_id}` → `approval/{approval_id}`
./docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.
md:98:- ✅ APPLICATION_SUBMITTED实体：approval/{approval_id}
./docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.
md:137:### APPLICATION_SUBMITTED为什么用approval实体？
./docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.
md:140:1. 辅导员收到通知时approval已创建
./docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.
md:145:- 正常路径不存在"通知已创建但approval不存在"的情况
./docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.
md:146:- 服务层`notify_application_submitted(application, counselor_approval)`保
证approval存在
./docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md:30:1.
服务层：`create_approval_timeout_warnings(now=None, dry_run=False)`
./docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md:31:2.
Management Command：`send_approval_timeout_warnings --dry-run`
./docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md:38:-
阈值：counselor 3天，dean 2天
./docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md:61:def
 create_approval_timeout_warnings(now=None, dry_run=False):
./docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md:75:**
文件：** `backend/apps/notifications/management/commands/send_approval_timeout_w
arnings.py`
./docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md:86:- c
ounselor超时3天触发提醒
./docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md:87:- d
ean超时2天触发提醒
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:33:| 5. 学工
部最终审批 | ⚠ 部分达标 | 主路径达标，但缺列表接口，dean硬编码 |
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:45:**位置：**
 `backend/apps/approvals/views.py:22`
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:46:**问题：**
 只按role放行，不按`approval.approver_id == request.user.user_id`校验
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:50:**位置：**
 `backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:51:**问题：**
 审批时未校验application当前状态是否匹配approval step，且没有事务/锁
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:117:5. **写真
实smoke脚本**：动态读取`access_token`、`application_id`、`approval_id`，不要写死
`1/2`
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:29:-
核心漏洞是"任何辅导员都能审批任意approval"
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:32:-
当前没有approval修改接口，Day 2不该当阻塞项
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:68:-
位置：`backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:69:-
修复：校验`approval.approver_id == request.user.user_id`
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:76:-
位置：`backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:79:-
修复：验证`approval.decision == pending`
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:80:-
修复：验证`application.status`匹配`approval.step`
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:81:-
修复：防止重复创建Dean approval（exists检查）
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:96:-
实现：动态提取token/application_id/approval_id
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:3
7:4. `POST /api/approvals/{approval_id}/approve`
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:3
8:5. `POST /api/approvals/{approval_id}/reject`
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:
35:| 班级-辅导员对应关系 | 完整且必要 | 是自动分配 `counselor_id` 和权限边界的关
键数据。 |
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:
103:3. **历史一致性规则。** 班级映射变更后，不应自动改写已提交申请中的 `counselo
r_id`；已提交申请如需改派，应由管理员显式操作并记录审计日志。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:
277:1. `employee_id` 必须全校唯一，并与班级映射中的 `counselor_employee_id` 完全
一致。
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:87:`g
et_students(filters) -> List[Student]`、`get_counselors()`、`get_class_mapping()
 -> Dict[str, str]` 太粗，缺少：
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:229:│
  - approvals表                              │
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md
:53:    def fetch_counselors(self) -> ImportResult[CounselorDTO]:
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md
:224:    counselors = [
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md
:236:    return students, counselors, dorm_statuses
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus
.md:174:FROM counselors
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus
.md:180:GET /api/counselors?is_active=true
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus
.md:184:- 文件名：`counselors_YYYYMMDD.csv`
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus
.md:209:| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T2020001
 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus
.md:210:| 辅导员姓名 | counselor_name | 文本 | 否 | 辅导员姓名（用于展示） | 李
老师 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus
.md:223:    counselor_employee_id,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus
.md:224:    counselor_name,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus
.md:228:FROM class_counselor_mapping
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus
.md:234:GET /api/class-counselor-mapping?grade=2020
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus
.md:238:- 文件名：`class_counselor_mapping_YYYYMMDD.csv`
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus
.md:386:- 班级-辅导员映射表中的counselor_employee_id必须在辅导员表中存在
./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:74:-
状态枚举（UserRole、ApplicationStatus、ApprovalStep、ApprovalDecision、DormCheck
outStatus）
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.
md:33:- 状态枚举（draft/pending_counselor/pending_dean/approved/rejected）
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.m
d:57:| 班级/辅导员 | class_id、counselor_id、counselor_active | 组织树、多辅导员
复杂分配 |
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:45:
 def fetch_counselors(self) -> List[CounselorDTO]:
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:252:
  counselors = [
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:264:
  return students, counselors, dorm_statuses
./docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:107:
  - entity_type（关联实体类型：application/approval）
./docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:124:
  - 例：同一approval_id的APPROVAL_APPROVED只创建一次
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-int
egration.md:35:def check_approval_timeout():
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-int
egration.md:37:        status__in=['pending_counselor', 'pending_admin']
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-int
egration.md:54:`check_approval_timeout()`每小时执行一次，扫描所有待审批申请。
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-int
egration.md:74:def check_approval_timeout():
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-int
egration.md:77:        status__in=['pending_counselor', 'pending_admin'],
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-int
egration.md:91:    'draft': ['pending_counselor'],
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-int
egration.md:92:    'pending_counselor': ['pending_admin', 'rejected'],
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-int
egration.md:115:        if app.status == 'pending_counselor':
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:3
1:  4. POST /api/approvals/{id}/approve
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:3
2:  5. POST /api/approvals/{id}/reject
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-pla
n.md:57:- 重复审批仍能改变状态或重复创建dean approval
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-pla
n.md:113:- application.status与approval.step匹配
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-pla
n.md:114:- pending approval限制
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-pla
n.md:115:- 防重复dean approval
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-pla
n.md:132:docker exec backend python manage.py test apps.approvals.tests apps.app
lications.tests
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-pla
n.md:189:3. `get_application`不再让任意counselor/dean查看所有申请
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-pla
n.md:190:4. 审批状态机保护覆盖approve/reject，且不会重复生成dean approval
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-reque
st.md:70:    def get_counselors(self) -> List[Counselor]:
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-reque
st.md:109:    def get_counselors(self):

exec
/bin/bash -lc "rtk sed -n '260,330p' tests/smoke_test.sh" in /home/caohui/projec
ts/graduation-leave-system
exec
/bin/bash -lc "rtk rg --files backend/apps | rtk rg 'models.py|views.py|serializ
ers.py|tests'" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk rg -n \"pending_dean|dean|pending_counselor|pending_dorm_mana
ger|ApprovalStep|ApplicationStatus\" backend miniprogram tests/smoke_test.sh -g
'"'!backend/data/routing_coverage_report.json'"'" in /home/caohui/projects/gradu
ation-leave-system
 succeeded in 123ms:

if [ -z "$STUDENT_APPROVE_NOTIF" ]; then
  echo "✗ Student APPROVAL_APPROVED notification not found"
  echo "Available notifications:"
  echo "$STUDENT_NOTIFS" | jq '.results[] | {type, message}'
  exit 1
fi

NOTIF_TYPE=$(echo "$STUDENT_APPROVE_NOTIF" | jq -r '.type')
NOTIF_ENTITY_TYPE=$(echo "$STUDENT_APPROVE_NOTIF" | jq -r '.entity_type')

if [ "$NOTIF_TYPE" != "approval_approved" ]; then
  echo "✗ Notification type wrong: $NOTIF_TYPE (expected: approval_approved)"
  exit 1
fi

if [ "$NOTIF_ENTITY_TYPE" != "approval" ]; then
  echo "✗ Notification entity_type wrong: $NOTIF_ENTITY_TYPE (expected: approval
)"
  exit 1
fi

echo "  ✓ Student received APPROVAL_APPROVED notification (type: $NOTIF_TYPE, en
tity_type: $NOTIF_ENTITY_TYPE)"

# Verify application status changed
APP_STATUS_AFTER=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.status')

if [ "$APP_STATUS_AFTER" != "pending_dean" ]; then
  echo "✗ Application status not updated: $APP_STATUS_AFTER (expected: pending_d
ean)"
  exit 1
fi

echo "  Application status: $APP_STATUS_AFTER"

# Extract dean approval ID
DEAN_APPROVAL_ID=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.approvals[] | select(.step=="dean") | .approval_id')

if [ -z "$DEAN_APPROVAL_ID" ] || [ "$DEAN_APPROVAL_ID" = "null" ]; then
  echo "✗ Dean approval not created"
  exit 1
fi

echo "  Dean approval: $DEAN_APPROVAL_ID"

# 9. Dean login
echo "9. Dean D001 login..."
DEAN_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"D001","password":"D001"}' \
  | jq -r '.access_token')

if [ -z "$DEAN_TOKEN" ] || [ "$DEAN_TOKEN" = "null" ]; then
  echo "✗ Dean login failed"
  exit 1
fi
echo "✓ Dean login success"

# 10. Dean approve
echo "10. Dean approve..."
DEAN_APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$DEAN_APPROVAL_
ID/approve/" \
  -H "Authorization: Bearer $DEAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"批准"}')

DEAN_DECISION=$(echo "$DEAN_APPROVE_RESPONSE" | jq -r '.decision')

if [ "$DEAN_DECISION" != "approved" ]; then
  echo "✗ Dean approve failed"

 succeeded in 125ms:
tests/smoke_test.sh:78:if [ "$APP_STATUS" != "pending_dorm_manager" ]; then
tests/smoke_test.sh:79:  echo "✗ Application status wrong: $APP_STATUS (expected
: pending_dorm_manager)"
tests/smoke_test.sh:125:# Verify application status changed to pending_counselor
tests/smoke_test.sh:130:if [ "$APP_STATUS_AFTER_DM" != "pending_counselor" ]; th
en
tests/smoke_test.sh:131:  echo "✗ Application status not updated: $APP_STATUS_AF
TER_DM (expected: pending_counselor)"
tests/smoke_test.sh:288:if [ "$APP_STATUS_AFTER" != "pending_dean" ]; then
tests/smoke_test.sh:289:  echo "✗ Application status not updated: $APP_STATUS_AF
TER (expected: pending_dean)"
tests/smoke_test.sh:295:# Extract dean approval ID
tests/smoke_test.sh:298:  | jq -r '.approvals[] | select(.step=="dean") | .appro
val_id')
miniprogram/pages/approvals/approvals.ts:19:    if (checkRoleAndRedirect(app.glo
balData.userInfo, ['dorm_manager', 'counselor', 'dean', 'admin'])) return;
miniprogram/pages/approvals/approvals.ts:26:      dean: '学工部',
miniprogram/pages/approvals/approvals.ts:39:    if (checkRoleAndRedirect(app.glo
balData.userInfo, ['dorm_manager', 'counselor', 'dean', 'admin'])) return;
miniprogram/pages/approvals/approvals.wxml:3:    <text class="title">{{userInfo.
role === 'dean' ? '备案查询' : '审批列表'}}</text>
miniprogram/pages/approvals/approvals.wxml:41:    <text>{{userInfo.role === 'dea
n' ? '暂无已通过备案申请' : '暂无待审批项'}}</text>
miniprogram/pages/login/login.ts:42:      } else if (res.user.role === 'counselo
r' || res.user.role === 'dean') {
miniprogram/types/api.ts:4:export type UserRole = 'student' | 'dorm_manager' | '
counselor' | 'dean' | 'admin';
miniprogram/types/api.ts:6:export type ApplicationStatus =
miniprogram/types/api.ts:8:  | 'pending_dorm_manager'
miniprogram/types/api.ts:9:  | 'pending_counselor'
miniprogram/types/api.ts:15:export type ApprovalStep = 'dorm_manager' | 'counsel
or';
miniprogram/types/api.ts:49:  status: ApplicationStatus;
miniprogram/types/api.ts:63:  step: ApprovalStep;
miniprogram/types/api.ts:74:  step: ApprovalStep;
miniprogram/pages/detail/detail.ts:57:        pending_dorm_manager: '待宿管员审
批',
miniprogram/pages/detail/detail.ts:58:        pending_counselor: '待辅导员审批',
miniprogram/pages/detail/detail.wxml:74:    <view class="actions" wx:if="{{canAp
prove && userInfo.role !== 'dean'}}">
miniprogram/pages/detail/detail.wxss:54:.status-pending_dorm_manager, .status-pe
nding_counselor {
backend/apps/approvals/validators.py:1:from apps.applications.models import Appl
icationStatus
backend/apps/approvals/validators.py:5:    'dorm_manager': ApplicationStatus.PEN
DING_DORM_MANAGER,
backend/apps/approvals/validators.py:6:    'counselor': ApplicationStatus.PENDIN
G_COUNSELOR,
backend/apps/approvals/models.py:6:class ApprovalStep(models.TextChoices):
backend/apps/approvals/models.py:9:    DEAN = 'dean', '学工部'
backend/apps/approvals/models.py:21:    step = models.CharField(max_length=20, c
hoices=ApprovalStep.choices)
backend/apps/approvals/migrations/0003_alter_approval_step.py:16:            fie
ld=models.CharField(choices=[('dorm_manager', '宿管员'), ('counselor', '辅导员')
, ('dean', '学工部')], max_length=20),
backend/apps/approvals/migrations/0001_initial.py:20:                ('step', mo
dels.CharField(choices=[('counselor', '辅导员'), ('dean', '学工部')], max_length
=20)),
backend/apps/applications/migrations/0001_initial.py:22:                ('status
', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员
审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '
已驳回')], default='draft', max_length=20)),
backend/apps/applications/migrations/0005_alter_application_status.py:16:
     field=models.CharField(choices=[('draft', '草稿'), ('pending_dorm_manager',
 '待宿管员审批'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学
工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', ma
x_length=20),
backend/apps/applications/permissions.py:3:from apps.approvals.models import App
roval, ApprovalStep, ApprovalDecision
backend/apps/applications/models.py:6:class ApplicationStatus(models.TextChoices
):
backend/apps/applications/models.py:8:    PENDING_DORM_MANAGER = 'pending_dorm_m
anager', '待宿管员审批'
backend/apps/applications/models.py:9:    PENDING_COUNSELOR = 'pending_counselor
', '待辅导员审批'
backend/apps/applications/models.py:28:    status = models.CharField(max_length=
20, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT)
backend/apps/applications/models.py:38:            ApplicationStatus.PENDING_DOR
M_MANAGER,
backend/apps/applications/models.py:39:            ApplicationStatus.PENDING_COU
NSELOR,
backend/apps/applications/models.py:40:            ApplicationStatus.APPROVED,
backend/apps/approvals/tests/test_rejection_flow.py:8:from apps.applications.mod
els import Application, ApplicationStatus
backend/apps/approvals/tests/test_rejection_flow.py:9:from apps.approvals.models
 import ApprovalDecision, ApprovalStep
backend/apps/approvals/tests/test_rejection_flow.py:73:        dorm_manager_appr
oval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/approvals/tests/test_rejection_flow.py:92:        dorm_manager_appr
oval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/approvals/tests/test_rejection_flow.py:102:        self.assertEqual
(application.status, ApplicationStatus.REJECTED)
backend/apps/approvals/tests/test_rejection_flow.py:118:        counselor_approv
al = application.approvals.get(step=ApprovalStep.COUNSELOR)
backend/apps/approvals/tests/test_rejection_flow.py:129:        self.assertEqual
(application.status, ApplicationStatus.REJECTED)
backend/apps/attachments/tests/test_list.py:7:from apps.applications.models impo
rt Application, ApplicationStatus
backend/apps/attachments/tests/test_list.py:51:        # Create dean
backend/apps/attachments/tests/test_list.py:52:        self.dean = User.objects.
create_user(
backend/apps/attachments/tests/test_list.py:82:            status=ApplicationSta
tus.APPROVED
backend/apps/attachments/tests/test_list.py:142:    def test_list_dean_archive_p
ositive(self):
backend/apps/attachments/tests/test_list.py:144:        self.client.force_authen
ticate(user=self.dean)
backend/apps/applications/tests/test_list_permissions.py:5:from apps.application
s.models import Application, ApplicationStatus
backend/apps/applications/tests/test_list_permissions.py:6:from apps.approvals.m
odels import Approval, ApprovalStep, ApprovalDecision
backend/apps/applications/tests/test_list_permissions.py:38:        self.dean =
User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
backend/apps/applications/tests/test_list_permissions.py:39:        self.dean.se
t_password('D001')
backend/apps/applications/tests/test_list_permissions.py:40:        self.dean.sa
ve()
backend/apps/applications/tests/test_list_permissions.py:54:            status=A
pplicationStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_list_permissions.py:64:            status=A
pplicationStatus.APPROVED
backend/apps/applications/tests/test_list_permissions.py:71:            step=App
rovalStep.COUNSELOR,
backend/apps/applications/tests/test_list_permissions.py:90:    def test_counsel
or_sees_only_pending_counselor_approvals(self):
backend/apps/applications/tests/test_list_permissions.py:102:    def test_dean_s
ees_only_approved_applications_for_archive(self):
backend/apps/applications/tests/test_list_permissions.py:103:        self.client
.force_authenticate(user=self.dean)
backend/apps/applications/tests/test_p0_fixes.py:3:from apps.applications.models
 import Application, ApplicationStatus
backend/apps/applications/tests/test_p0_fixes.py:4:from apps.approvals.models im
port Approval, ApprovalDecision, ApprovalStep
backend/apps/applications/tests/test_p0_fixes.py:39:            status=Applicati
onStatus.REJECTED
backend/apps/applications/tests/test_p0_fixes.py:50:            status=Applicati
onStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:54:        self.assertEqual(app
2.status, ApplicationStatus.PENDING_COUNSELOR)
backend/apps/applications/tests/test_p0_fixes.py:65:            status=Applicati
onStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:76:            status=Applicati
onStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:106:            status=Applicat
ionStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:116:            status=Applicat
ionStatus.APPROVED
backend/apps/applications/tests/test_p0_fixes.py:126:            status=Applicat
ionStatus.REJECTED
backend/apps/applications/tests/test_p0_fixes.py:133:            step=ApprovalSt
ep.COUNSELOR,
backend/apps/applications/tests/test_p0_fixes.py:142:            step=ApprovalSt
ep.COUNSELOR,
backend/apps/applications/tests/test_p0_fixes.py:151:            step=ApprovalSt
ep.COUNSELOR,
backend/apps/applications/tests/test_error_cases.py:8:from apps.applications.mod
els import Application, ApplicationStatus
backend/apps/applications/tests/test_error_cases.py:59:        self.dean = User.
objects.create_user(
backend/apps/attachments/tests/test_delete.py:7:from apps.applications.models im
port Application, ApplicationStatus
backend/apps/attachments/tests/test_delete.py:60:            status=ApplicationS
tatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_detail_permissions.py:5:from apps.applicati
ons.models import Application, ApplicationStatus
backend/apps/applications/tests/test_detail_permissions.py:6:from apps.approvals
.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/applications/tests/test_detail_permissions.py:41:        self.dean1
 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
backend/apps/applications/tests/test_detail_permissions.py:42:        self.dean1
.set_password('D001')
backend/apps/applications/tests/test_detail_permissions.py:43:        self.dean1
.save()
backend/apps/applications/tests/test_detail_permissions.py:45:        self.dean2
 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
backend/apps/applications/tests/test_detail_permissions.py:46:        self.dean2
.set_password('D002')
backend/apps/applications/tests/test_detail_permissions.py:47:        self.dean2
.save()
backend/apps/applications/tests/test_detail_permissions.py:85:    def test_dean_
cannot_access_in_progress_application(self):
backend/apps/applications/tests/test_detail_permissions.py:96:        self.clien
t.force_authenticate(user=self.dean2)
backend/apps/approvals/views.py:10:from .models import Approval, ApprovalDecisio
n, ApprovalStep
backend/apps/approvals/views.py:14:from apps.applications.models import Applicat
ion, ApplicationStatus
backend/apps/approvals/views.py:52:            step=ApprovalStep.DORM_MANAGER
backend/apps/approvals/views.py:59:            step=ApprovalStep.COUNSELOR
backend/apps/approvals/views.py:115:    if approval.step == ApprovalStep.DORM_MA
NAGER and user.role != UserRole.DORM_MANAGER:
backend/apps/approvals/views.py:118:    if approval.step == ApprovalStep.COUNSEL
OR and user.role != UserRole.COUNSELOR:
backend/apps/approvals/views.py:121:    if approval.step == ApprovalStep.DEAN an
d user.role != UserRole.DEAN:
backend/apps/approvals/views.py:150:    if approval.step == ApprovalStep.DORM_MA
NAGER:
backend/apps/approvals/views.py:154:            step=ApprovalStep.COUNSELOR
backend/apps/approvals/views.py:161:        application.status = ApplicationStat
us.PENDING_COUNSELOR
backend/apps/approvals/views.py:191:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/views.py:196:    elif approval.step == ApprovalStep.COUNS
ELOR:
backend/apps/approvals/views.py:198:        application.status = ApplicationStat
us.APPROVED
backend/apps/approvals/views.py:229:    if approval.step == ApprovalStep.DORM_MA
NAGER and user.role != UserRole.DORM_MANAGER:
backend/apps/approvals/views.py:232:    if approval.step == ApprovalStep.COUNSEL
OR and user.role != UserRole.COUNSELOR:
backend/apps/approvals/views.py:235:    if approval.step == ApprovalStep.DEAN an
d user.role != UserRole.DEAN:
backend/apps/approvals/views.py:264:    application.status = ApplicationStatus.R
EJECTED
backend/apps/approvals/tests/test_state_machine.py:5:from apps.applications.mode
ls import Application, ApplicationStatus
backend/apps/approvals/tests/test_state_machine.py:6:from apps.approvals.models
import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_state_machine.py:37:        # Create dean
backend/apps/approvals/tests/test_state_machine.py:38:        self.dean = User.o
bjects.create_user(
backend/apps/approvals/tests/test_state_machine.py:63:            status=Applica
tionStatus.PENDING_COUNSELOR
backend/apps/approvals/tests/test_state_machine.py:70:            step=ApprovalS
tep.COUNSELOR,
backend/apps/approvals/tests/test_state_machine.py:116:    def test_counselor_st
ep_requires_pending_counselor_status(self):
backend/apps/approvals/tests/test_state_machine.py:118:        self.application.
status = ApplicationStatus.PENDING_DORM_MANAGER
backend/apps/approvals/tests/test_state_machine.py:136:    def test_dorm_manager
_step_requires_pending_dorm_manager_status(self):
backend/apps/approvals/tests/test_state_machine.py:138:        self.application.
status = ApplicationStatus.APPROVED
backend/apps/approvals/tests/test_state_machine.py:143:            step=Approval
Step.DORM_MANAGER,
backend/apps/approvals/tests/test_permissions.py:5:from apps.applications.models
 import Application, ApplicationStatus
backend/apps/approvals/tests/test_permissions.py:6:from apps.approvals.models im
port Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_permissions.py:53:        self.dean1 = User.ob
jects.create_user(
backend/apps/approvals/tests/test_permissions.py:59:        self.dean2 = User.ob
jects.create_user(
backend/apps/approvals/tests/test_permissions.py:92:            status=Applicati
onStatus.PENDING_COUNSELOR
backend/apps/approvals/tests/test_permissions.py:99:            step=ApprovalSte
p.COUNSELOR,
backend/apps/approvals/tests/test_permissions.py:108:        self.application1.s
tatus = ApplicationStatus.PENDING_DORM_MANAGER
backend/apps/approvals/tests/test_permissions.py:113:            step=ApprovalSt
ep.DORM_MANAGER,
backend/apps/approvals/tests/test_permissions.py:137:    def test_dean_cannot_ac
t_on_counselor_step(self):
backend/apps/approvals/tests/test_permissions.py:139:        self.client.force_a
uthenticate(user=self.dean1)
backend/apps/attachments/tests/test_upload.py:7:from apps.applications.models im
port Application, ApplicationStatus
backend/apps/attachments/tests/test_upload.py:61:            status=ApplicationS
tatus.PENDING_COUNSELOR
backend/apps/attachments/tests/test_upload.py:72:            status=ApplicationS
tatus.PENDING_COUNSELOR
backend/apps/attachments/tests/test_download.py:7:from apps.applications.models
import Application, ApplicationStatus
backend/apps/attachments/tests/test_download.py:8:from apps.approvals.models imp
ort Approval, ApprovalStep, ApprovalDecision
backend/apps/attachments/tests/test_download.py:61:            status=Applicatio
nStatus.PENDING_COUNSELOR
backend/apps/users/migrations/0001_initial.py:25:                ('role', models
.CharField(choices=[('student', '学生'), ('counselor', '辅导员'), ('dean', '学工
部')], max_length=20)),
backend/apps/users/migrations/0006_add_admin_role.py:21:                    ('de
an', '学工部'),
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:28:
        field=models.CharField(choices=[('student', '学生'), ('dorm_manager', '
宿管员'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20),
backend/apps/users/models.py:9:    DEAN = 'dean', '学工部'
backend/apps/approvals/tests/test_list_permissions.py:4:from apps.applications.m
odels import Application, ApplicationStatus
backend/apps/approvals/tests/test_list_permissions.py:5:from apps.approvals.mode
ls import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_list_permissions.py:33:        self.dean1 = Us
er.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
backend/apps/approvals/tests/test_list_permissions.py:34:        self.dean1.set_
password('D001')
backend/apps/approvals/tests/test_list_permissions.py:35:        self.dean1.save
()
backend/apps/approvals/tests/test_list_permissions.py:37:        self.dean2 = Us
er.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
backend/apps/approvals/tests/test_list_permissions.py:38:        self.dean2.set_
password('D002')
backend/apps/approvals/tests/test_list_permissions.py:39:        self.dean2.save
()
backend/apps/approvals/tests/test_list_permissions.py:49:            status=Appl
icationStatus.PENDING_COUNSELOR
backend/apps/approvals/tests/test_list_permissions.py:56:            step=Approv
alStep.COUNSELOR,
backend/apps/approvals/tests/test_list_permissions.py:65:            step=Approv
alStep.DORM_MANAGER,
backend/apps/approvals/tests/test_list_permissions.py:101:    def test_dean_sees
_all_approvals_for_archive(self):
backend/apps/approvals/tests/test_list_permissions.py:102:        self.client.fo
rce_authenticate(user=self.dean1)
backend/apps/approvals/tests/test_list_permissions.py:124:            status=App
licationStatus.APPROVED
backend/apps/approvals/tests/test_list_permissions.py:129:            step=Appro
valStep.COUNSELOR,
backend/apps/approvals/tests/test_list_permissions.py:143:            status=App
licationStatus.PENDING_COUNSELOR
backend/apps/approvals/tests/test_list_permissions.py:148:            step=Appro
valStep.COUNSELOR,
backend/apps/applications/tests/test_constraints.py:7:from apps.applications.mod
els import Application, ApplicationStatus
backend/apps/applications/tests/test_application_flow.py:8:from apps.application
s.models import Application, ApplicationStatus
backend/apps/applications/tests/test_application_flow.py:9:from apps.approvals.m
odels import ApprovalDecision, ApprovalStep
backend/apps/applications/tests/test_application_flow.py:41:        self.dean =
User.objects.create_user(
backend/apps/applications/tests/test_application_flow.py:76:        self.assertE
qual(response.data['status'], ApplicationStatus.PENDING_DORM_MANAGER)
backend/apps/applications/tests/test_application_flow.py:88:        dorm_manager
_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/applications/tests/test_application_flow.py:98:        self.assertE
qual(application.status, ApplicationStatus.PENDING_COUNSELOR)
backend/apps/applications/tests/test_application_flow.py:108:        counselor_a
pproval = application.approvals.get(step=ApprovalStep.COUNSELOR)
backend/apps/applications/tests/test_application_flow.py:119:        self.assert
Equal(application.status, ApplicationStatus.APPROVED)
backend/apps/applications/tests/test_application_flow.py:125:        self.assert
Equal(response.data['status'], ApplicationStatus.APPROVED)
backend/apps/notifications/tests/test_auto_notifications.py:14:from apps.applica
tions.models import Application, ApplicationStatus
backend/apps/notifications/tests/test_auto_notifications.py:15:from apps.approva
ls.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/notifications/tests/test_auto_notifications.py:53:            statu
s=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications.py:59:            step=
ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:85:            statu
s=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications.py:91:            step=
ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:116:            stat
us=ApplicationStatus.PENDING_DORM_MANAGER
backend/apps/notifications/tests/test_auto_notifications.py:122:            step
=ApprovalStep.DORM_MANAGER,
backend/apps/notifications/tests/test_auto_notifications.py:145:            stat
us=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications.py:151:            step
=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:176:            stat
us=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications.py:182:            step
=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:211:            stat
us=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications.py:217:            step
=ApprovalStep.COUNSELOR,
backend/apps/applications/views.py:8:from .models import Application, Applicatio
nStatus, DormCheckoutStatus
backend/apps/applications/views.py:13:from apps.approvals.models import Approval
, ApprovalStep, ApprovalDecision
backend/apps/applications/views.py:73:            step=ApprovalStep.DORM_MANAGER
,
backend/apps/applications/views.py:82:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/views.py:89:        queryset = Application.objects.fil
ter(status=ApplicationStatus.APPROVED)
backend/apps/applications/views.py:125:        status__in=[ApplicationStatus.PEN
DING_DORM_MANAGER, ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.APPROV
ED]
backend/apps/applications/views.py:187:        status=ApplicationStatus.PENDING_
DORM_MANAGER,
backend/apps/applications/views.py:194:        step=ApprovalStep.DORM_MANAGER,
backend/apps/notifications/tests/test_auto_notifications_api.py:11:from apps.app
lications.models import Application, ApplicationStatus
backend/apps/notifications/tests/test_auto_notifications_api.py:12:from apps.app
rovals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/notifications/tests/test_auto_notifications_api.py:42:        self.
dean = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:45:            r
ole='dean'
backend/apps/notifications/tests/test_auto_notifications_api.py:88:            s
tatus=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications_api.py:94:            s
tep=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications_api.py:130:
status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications_api.py:136:
step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications_api.py:175:
status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications_api.py:181:
step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications_api.py:210:
status=ApplicationStatus.APPROVED
backend/apps/notifications/tests/test_auto_notifications_api.py:216:
step=ApprovalStep.COUNSELOR,
backend/apps/users/management/commands/seed_data.py:110:            self.stdout.
write(f'Created dean: {user.user_id}')
backend/apps/attachments/views.py:13:from apps.approvals.models import Approval,
 ApprovalStep

 succeeded in 147ms:
backend/apps/approvals/tests/__init__.py
backend/apps/approvals/tests/test_rejection_flow.py
backend/apps/approvals/tests/test_list_permissions.py
backend/apps/approvals/tests/test_permissions.py
backend/apps/approvals/tests/test_state_machine.py
backend/apps/approvals/views.py
backend/apps/approvals/serializers.py
backend/apps/approvals/models.py
backend/apps/applications/tests/__init__.py
backend/apps/applications/tests/test_p0_fixes.py
backend/apps/applications/tests/test_error_cases.py
backend/apps/applications/tests/test_detail_permissions.py
backend/apps/applications/tests/test_serializer_validation.py
backend/apps/applications/tests/test_list_permissions.py
backend/apps/applications/tests/test_constraints.py
backend/apps/applications/tests/test_application_flow.py
backend/apps/applications/views.py
backend/apps/applications/serializers.py
backend/apps/applications/models.py
backend/apps/users/serializers.py
backend/apps/users/models.py
backend/apps/users/views.py
backend/apps/notifications/tests/__init__.py
backend/apps/notifications/tests/test_auto_notifications_api.py
backend/apps/notifications/tests/test_timeout_warnings.py
backend/apps/notifications/tests/test_models.py
backend/apps/notifications/tests/test_api.py
backend/apps/notifications/tests/test_auto_notifications.py
backend/apps/notifications/views.py
backend/apps/notifications/serializers.py
backend/apps/notifications/models.py
backend/apps/attachments/views.py
backend/apps/attachments/serializers.py
backend/apps/attachments/models.py
backend/apps/attachments/tests/__init__.py
backend/apps/attachments/tests/test_list.py
backend/apps/attachments/tests/test_delete.py
backend/apps/attachments/tests/test_upload.py
backend/apps/attachments/tests/test_download.py
backend/apps/users/tests/test_xg_user_client.py
backend/apps/users/tests/test_xg_user_sync.py
backend/apps/users/tests/test_import_csv.py
backend/apps/users/tests/test_xg_user_mapper.py
backend/apps/users/tests/__init__.py

exec
/bin/bash -lc "rtk sed -n '1,120p' backend/apps/approvals/models.py" in /home/ca
ohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/approvals/views.py" in /home/cao
hui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,240p' backend/apps/applications/views.py" in /home/
caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,100p' backend/apps/applications/models.py" in /home
/caohui/projects/graduation-leave-system
 succeeded in 106ms:
 succeeded in 117ms:
from django.db import models
from django.core.exceptions import ValidationError
from apps.users.models import User


class ApplicationStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
    APPROVED = 'approved', '已通过'
    REJECTED = 'rejected', '已驳回'


class DormCheckoutStatus(models.TextChoices):
    COMPLETED = 'completed', '已清退'
    PENDING = 'pending', '清退中'
    NOT_STARTED = 'not_started', '未开始'
    UNKNOWN = 'unknown', '状态未知'


class Application(models.Model):
    application_id = models.CharField(max_length=50, primary_key=True)
    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ap
plications')
    student_name = models.CharField(max_length=100)
    class_id = models.CharField(max_length=50)
    reason = models.TextField()
    leave_date = models.DateField()
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices,
default=ApplicationStatus.DRAFT)
    dorm_checkout_status = models.CharField(max_length=20, choices=DormCheckoutS
tatus.choices, default=DormCheckoutStatus.NOT_STARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'applications'

    def clean(self):
        active_statuses = [
            ApplicationStatus.PENDING_DORM_MANAGER,
            ApplicationStatus.PENDING_COUNSELOR,
            ApplicationStatus.APPROVED,
        ]
        if self.status in active_statuses:
            existing = Application.objects.filter(
                student=self.student,
                status__in=active_statuses
            ).exclude(application_id=self.application_id).exists()
            if existing:
                raise ValidationError('该学生已有待审批或已通过的申请，不能重复
提交')

 succeeded in 127ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
import logging
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from drf_spectacular.types import OpenApiTypes as Types
from .models import Approval, ApprovalDecision, ApprovalStep
from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalL
istSerializer, ApprovalListResponseSerializer
from .pagination import ApprovalLimitOffsetPagination
from .validators import approval_step_matches_application_status
from apps.applications.models import Application, ApplicationStatus
from apps.users.models import User, UserRole
from apps.notifications.services import notify_approval_decided
from schema import ErrorResponseSerializer
import uuid


@extend_schema(
    operation_id='approvals_list',
    summary='获取审批列表',
    description='获取当前用户的待审批列表（辅导员或学工部）',
    parameters=[
        OpenApiParameter('decision', Types.STR, description='决策过滤：pending/a
pproved/rejected/all（默认pending）'),
        OpenApiParameter('limit', Types.INT, description='每页数量（默认20）'),
        OpenApiParameter('offset', Types.INT, description='偏移量（默认0）'),
    ],
    responses={
        200: ApprovalListResponseSerializer,
        403: ErrorResponseSerializer,
    },
    tags=['审批']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_approvals(request):
    user = request.user

    # 学生禁止访问
    if user.role == UserRole.STUDENT:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # 宿管员: 只看自己的dorm_manager审批
    if user.role == UserRole.DORM_MANAGER:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DORM_MANAGER
        ).select_related('application', 'approver')

    # 辅导员: 只看自己的counselor审批
    elif user.role == UserRole.COUNSELOR:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR
        ).select_related('application', 'approver')

    # 学工部: 查看所有审批（存档用）
    elif user.role == UserRole.DEAN:
        queryset = Approval.objects.all().select_related('application', 'approve
r')

    else:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # Decision filtering (default: pending)
    decision_param = request.query_params.get('decision', 'pending')
    if decision_param != 'all':
        queryset = queryset.filter(decision=decision_param)

    # 排序
    queryset = queryset.order_by('-created_at', '-approval_id')

    # 分页
    paginator = ApprovalLimitOffsetPagination()
    page = paginator.paginate_queryset(queryset, request)

    # 序列化
    serializer = ApprovalListSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


@extend_schema(
    operation_id='approvals_approve',
    summary='通过审批',
    description='审批人通过指定的审批申请',
    request=ApprovalActionSerializer,
    responses={
        200: ApprovalSerializer,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
    },
    tags=['审批']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def approve_approval(request, approval_id):
    try:
        approval = Approval.objects.select_for_update().get(approval_id=approval
_id)
    except Approval.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存
在'}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM
_MANAGER:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)
    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSEL
OR:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)
    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.approver_id != user.user_id:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.decision != ApprovalDecision.PENDING:
        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，
不能重复操作'}},
                        status=status.HTTP_409_CONFLICT)

    if not approval_step_matches_application_status(approval):
        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审
批步骤不匹配'}},
                        status=status.HTTP_409_CONFLICT)

    serializer = ApprovalActionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求
参数验证失败'}},
                        status=status.HTTP_400_BAD_REQUEST)

    approval.decision = ApprovalDecision.APPROVED
    approval.comment = serializer.validated_data.get('comment', '')
    approval.decided_at = timezone.now()
    approval.save()

    notify_approval_decided(approval)

    application = approval.application
    if approval.step == ApprovalStep.DORM_MANAGER:
        # Check for existing counselor approval to prevent duplicates
        existing_counselor_approval = Approval.objects.filter(
            application=application,
            step=ApprovalStep.COUNSELOR
        ).exists()

        if existing_counselor_approval:
            return Response({'error': {'code': 'CONFLICT', 'message': '辅导员审
批已存在，不能重复创建'}},
                            status=status.HTTP_409_CONFLICT)

        application.status = ApplicationStatus.PENDING_COUNSELOR
        application.save()

        # Get counselor by department (Phase 3 design: department-based routing)
        # Note: Original design used ClassMapping (class_id), but Phase 3 user r
equirements
        # changed to "按学院向辅导员审批" (approval by department/college).
        # Multiple counselors per department are allowed (different classes with
in department).
        # Selection: order_by('user_id') picks lowest ID for deterministic routi
ng.
        counselors = User.objects.filter(
            role=UserRole.COUNSELOR,
            department=application.student.department,
            active=True
        ).order_by('user_id')

        if counselors.count() > 1:
            logging.warning(
                f"Multiple counselors found for department {application.student.
department}: "
                f"{counselors.count()} matches. Selected {counselors.first().use
r_id} via order_by('user_id')"
            )

        counselor = counselors.first()

        if not counselor:
            return Response({'error': {'code': 'NOT_FOUND', 'message': '该学院辅
导员不存在',
                                        'details': {'department': application.st
udent.department}}},
                            status=status.HTTP_404_NOT_FOUND)

        Approval.objects.create(
            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=counselor,
            approver_name=counselor.name,
            decision=ApprovalDecision.PENDING
        )
    elif approval.step == ApprovalStep.COUNSELOR:
        # Counselor approval completes the process (2-level approval)
        application.status = ApplicationStatus.APPROVED
        application.save()

    return Response(ApprovalSerializer(approval).data)


@extend_schema(
    operation_id='approvals_reject',
    summary='驳回审批',
    description='审批人驳回指定的审批申请',
    request=ApprovalActionSerializer,
    responses={
        200: ApprovalSerializer,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
    },
    tags=['审批']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def reject_approval(request, approval_id):
    try:
        approval = Approval.objects.select_for_update().get(approval_id=approval
_id)
    except Approval.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存
在'}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM
_MANAGER:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)
    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSEL
OR:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)
    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.approver_id != user.user_id:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.decision != ApprovalDecision.PENDING:
        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，
不能重复操作'}},
                        status=status.HTTP_409_CONFLICT)

    if not approval_step_matches_application_status(approval):
        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审
批步骤不匹配'}},
                        status=status.HTTP_409_CONFLICT)

    serializer = ApprovalActionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求
参数验证失败'}},
                        status=status.HTTP_400_BAD_REQUEST)

    approval.decision = ApprovalDecision.REJECTED
    approval.comment = serializer.validated_data.get('comment', '')
    approval.decided_at = timezone.now()
    approval.save()


 succeeded in 127ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Application, ApplicationStatus, DormCheckoutStatus
from .serializers import ApplicationSerializer, ApplicationCreateSerializer, App
licationListSerializer, ApplicationListResponseSerializer
from .pagination import ApplicationLimitOffsetPagination
from .providers import MockDormCheckoutProvider
from .permissions import can_view_application
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.users.models import UserRole, User
from apps.notifications.services import notify_application_submitted
from schema import ErrorResponseSerializer
import uuid
import logging


@extend_schema(
    methods=['GET'],
    operation_id='applications_list',
    summary='获取申请列表',
    description='获取当前用户的申请列表（学生/辅导员/学工部）',
    parameters=[
        OpenApiParameter('status', OpenApiTypes.STR, description='状态过滤'),
        OpenApiParameter('limit', OpenApiTypes.INT, description='每页数量（默认2
0）'),
        OpenApiParameter('offset', OpenApiTypes.INT, description='偏移量（默认0
）'),
    ],
    responses={
        200: ApplicationListResponseSerializer,
        403: ErrorResponseSerializer,
    },
    tags=['申请']
)
@extend_schema(
    methods=['POST'],
    operation_id='applications_create',
    summary='提交离校申请',
    description='学生提交新的离校申请',
    request=ApplicationCreateSerializer,
    responses={
        201: ApplicationSerializer,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
        422: ErrorResponseSerializer,
    },
    tags=['申请']
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def applications_view(request):
    if request.method == 'GET':
        return list_applications(request)
    else:
        return create_application(request)


def list_applications(request):
    user = request.user

    # Student: own applications only
    if user.role == UserRole.STUDENT:
        queryset = Application.objects.filter(student=user)

    # Dorm Manager: applications with own pending dorm manager approvals
    elif user.role == UserRole.DORM_MANAGER:
        pending_approvals = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DORM_MANAGER,
            decision=ApprovalDecision.PENDING
        ).values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=pending_approvals)

    # Counselor: applications with own pending counselor approvals
    elif user.role == UserRole.COUNSELOR:
        pending_approvals = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR,
            decision=ApprovalDecision.PENDING
        ).values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=pending_approvals)

    # Dean: view all approved applications (archiving role)
    elif user.role == UserRole.DEAN:
        queryset = Application.objects.filter(status=ApplicationStatus.APPROVED)

    else:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # Status filtering
    status_param = request.query_params.get('status')
    if status_param:
        queryset = queryset.filter(status=status_param)

    # Sort by created_at DESC
    queryset = queryset.order_by('-created_at', '-application_id')

    # Paginate
    paginator = ApplicationLimitOffsetPagination()
    page = paginator.paginate_queryset(queryset, request)

    # Serialize
    serializer = ApplicationListSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


def create_application(request):
    user = request.user

    if user.role != UserRole.STUDENT:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以
提交申请'}},
                        status=status.HTTP_403_FORBIDDEN)

    # Check for existing pending/approved applications
    existing = Application.objects.filter(
        student=user,
        status__in=[ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatus.PE
NDING_COUNSELOR, ApplicationStatus.APPROVED]
    ).first()
    if existing:
        return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或
已通过的申请，不能重复提交',
                                    'details': {'student_id': user.user_id, 'exi
sting_application_id': existing.application_id, 'status': existing.status}}},
                        status=status.HTTP_409_CONFLICT)

    serializer = ApplicationCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求
参数验证失败',
                                    'details': serializer.errors}},
                        status=status.HTTP_400_BAD_REQUEST)

    provider = MockDormCheckoutProvider()
    dorm_status = provider.check_status(user.user_id)

    if dorm_status.status != DormCheckoutStatus.COMPLETED:
        return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退
未完成，无法提交申请',
                                    'details': {'student_id': user.user_id, 'dor
m_status': dorm_status.status,
                                                'blocking_reason': dorm_status.b
locking_reason}}},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Find dorm manager with fallback mechanism
    dorm_manager = None
    building = user.building

    # Try to find dorm manager by building
    if building and building.strip():
        dorm_managers = User.objects.filter(
            role=UserRole.DORM_MANAGER,
            building=building,
            active=True
        ).order_by('user_id')

        if dorm_managers.exists():
            if dorm_managers.count() > 1:
                logging.warning(
                    f"Multiple dorm managers found for building {building}: "
                    f"{dorm_managers.count()} matches. Selected {dorm_managers.f
irst().user_id} via order_by('user_id')"
                )
            dorm_manager = dorm_managers.first()

    # Fallback: use default dorm manager for students without building
    if not dorm_manager:
        from django.conf import settings
        fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '920081
49')
        try:
            dorm_manager = User.objects.get(role=UserRole.DORM_MANAGER, user_id=
fallback_id, active=True)
        except User.DoesNotExist:
            return Response({'error': {'code': 'NOT_FOUND', 'message': '无可用宿
管员',
                                        'details': {'building': building or '未
分配', 'fallback_id': fallback_id}}},
                            status=status.HTTP_404_NOT_FOUND)

    dorm_manager_name = dorm_manager.name

    application = Application.objects.create(
        application_id=f'app_{uuid.uuid4().hex[:8]}',
        student=user,
        student_name=user.name,
        class_id=user.class_id,
        reason=serializer.validated_data['reason'],
        leave_date=serializer.validated_data['leave_date'],
        status=ApplicationStatus.PENDING_DORM_MANAGER,
        dorm_checkout_status=dorm_status.status
    )

    dorm_manager_approval = Approval.objects.create(
        approval_id=f'apv_{uuid.uuid4().hex[:8]}',
        application=application,
        step=ApprovalStep.DORM_MANAGER,
        approver=dorm_manager,
        approver_name=dorm_manager_name,
        decision=ApprovalDecision.PENDING
    )

    notify_application_submitted(application, dorm_manager_approval)

    return Response(ApplicationSerializer(application).data, status=status.HTTP_
201_CREATED)


@extend_schema(
    operation_id='applications_get',
    summary='获取申请详情',
    description='获取指定申请的详细信息（包括审批记录）',
    responses={
        200: ApplicationSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
    tags=['申请']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_application(request, application_id):
    try:
        application = Application.objects.get(application_id=application_id)
    except Application.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在',
                                    'details': {'application_id': application_id
}}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user

    # Check permission using shared helper
    if not can_view_application(user, application):
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此
资源'}},
                        status=status.HTTP_403_FORBIDDEN)

    return Response(ApplicationSerializer(application).data)

exec
/bin/bash -lc "rtk sed -n '260,340p' backend/apps/approvals/views.py" in /home/c
aohui/projects/graduation-leave-system
 succeeded in 0ms:

    notify_approval_decided(approval)

    application = approval.application
    application.status = ApplicationStatus.REJECTED
    application.save()

    return Response(ApprovalSerializer(approval).data)

exec
/bin/bash -lc "rtk sed -n '60,135p' backend/apps/applications/tests/test_applica
tion_flow.py" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,130p' backend/apps/approvals/serializers.py" in /ho
me/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,140p' backend/apps/approvals/validators.py" in /hom
e/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,120p' backend/apps/applications/serializers.py" in
/home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import serializers
from .models import Application


class ApplicationListSerializer(serializers.ModelSerializer):
    """Lean serializer for application lists - no nested approvals"""
    student_id = serializers.CharField(source='student.user_id', read_only=True)

    class Meta:
        model = Application
        fields = ['application_id', 'student_id', 'student_name', 'class_id',
                  'reason', 'leave_date', 'status', 'created_at', 'updated_at']
        read_only_fields = ['application_id', 'student_id', 'student_name',
                            'class_id', 'status', 'created_at', 'updated_at']


class ApplicationSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(source='student.user_id', read_only=True)
    approvals = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['application_id', 'student_id', 'student_name', 'class_id',
                  'reason', 'leave_date', 'status', 'dorm_checkout_status',
                  'approvals', 'created_at', 'updated_at']
        read_only_fields = ['application_id', 'student_id', 'student_name',
                            'class_id', 'status', 'dorm_checkout_status',
                            'created_at', 'updated_at']

    def get_approvals(self, obj):
        from apps.approvals.serializers import ApprovalSerializer
        return ApprovalSerializer(obj.approvals.all(), many=True).data


class ApplicationCreateSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=500, trim_whitespace=True)
    leave_date = serializers.DateField()

    def validate_reason(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('离校原因不能为空')
        return value

    def validate_leave_date(self, value):
        from django.utils import timezone
        today = timezone.now().date()
        if value < today:
            raise serializers.ValidationError('离校日期不能早于今天')
        return value


class ApplicationListResponseSerializer(serializers.Serializer):
    """Schema-only: application list response with pagination"""
    count = serializers.IntegerField()
    results = ApplicationListSerializer(many=True)

 succeeded in 105ms:
 succeeded in 110ms:
from rest_framework import serializers
from .models import Approval


class ApprovalListSerializer(serializers.ModelSerializer):
    """Lean serializer for approval lists - includes created_at"""
    application_id = serializers.CharField(source='application.application_id',
read_only=True)
    approver_id = serializers.CharField(source='approver.user_id', read_only=Tru
e)

    class Meta:
        model = Approval
        fields = ['approval_id', 'application_id', 'step', 'approver_id',
                  'approver_name', 'decision', 'created_at']
        read_only_fields = ['approval_id', 'application_id', 'step',
                            'approver_id', 'approver_name', 'decision', 'created
_at']


class ApprovalSerializer(serializers.ModelSerializer):
    application_id = serializers.CharField(source='application.application_id',
read_only=True)
    approver_id = serializers.CharField(source='approver.user_id', read_only=Tru
e)

    class Meta:
        model = Approval
        fields = ['approval_id', 'application_id', 'step', 'approver_id',
                  'approver_name', 'decision', 'comment', 'decided_at']
        read_only_fields = ['approval_id', 'application_id', 'step',
                            'approver_id', 'approver_name', 'decision', 'decided
_at']


class ApprovalActionSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False, allow_blank=True)


class ApprovalListResponseSerializer(serializers.Serializer):
    """Schema-only: approval list response with pagination"""
    count = serializers.IntegerField()
    results = ApprovalListSerializer(many=True)

 succeeded in 110ms:

        # Step 1: 学生登录
        response = self.client.post('/api/auth/login', {
            'user_id': '2020001',
            'password': '2020001'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        student_token = response.data['access_token']

        # Step 2: 学生提交申请
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.post('/api/applications/', {
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat(
)
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], ApplicationStatus.PENDING_DORM
_MANAGER)
        application_id = response.data['application_id']

        # Step 3: 宿管员登录
        response = self.client.post('/api/auth/login', {
            'user_id': 'M001',
            'password': 'M001'
        }, format='json')
        dorm_manager_token = response.data['access_token']

        # Step 4: 宿管员审批通过
        application = Application.objects.get(application_id=application_id)
        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM
_MANAGER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dorm_manager_token}
')
        response = self.client.post(f'/api/approvals/{dorm_manager_approval.appr
oval_id}/approve/', {
            'comment': '宿舍清退通过'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)

        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.PENDING_COUNSELOR
)

        # Step 5: 辅导员登录
        response = self.client.post('/api/auth/login', {
            'user_id': 'T001',
            'password': 'T001'
        }, format='json')
        counselor_token = response.data['access_token']

        # Step 6: 辅导员审批通过
        counselor_approval = application.approvals.get(step=ApprovalStep.COUNSEL
OR)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {counselor_token}')
        response = self.client.post(f'/api/approvals/{counselor_approval.approva
l_id}/approve/', {
            'comment': '同意离校'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)

        # Step 7: 查询申请状态 - 辅导员审批后直接完成（2级审批）
        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.APPROVED)

        # Step 8: 最终状态查询
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.get(f'/api/applications/{application_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], ApplicationStatus.APPROVED)
        self.assertEqual(len(response.data['approvals']), 2)  # 2-level approval

codex
[RESPONSE_START]
{
  "consensus": true,
  "decision": "后端当前实际审批流程是2级：dorm_manager -> counselor，辅导员通过
后直接进入 approved。应更新 tests/smoke_test.sh，移除 pending_dean/dean approval
/dean approve 断言；Phase 4 前端类型 ApplicationStatus/ApprovalStep 与当前后端实
际流程一致，不应为 smoke 的3级预期去扩展 pending_dean/dean。",
  "blocking_issues": [],
  "reasoning": "当前 backend/apps/applications/models.py 的 ApplicationStatus 已
无 pending_dean；backend/apps/approvals/views.py 在 counselor approve 分支明确将
 application.status 置为 approved，并注释为 2-level approval；backend/apps/appro
vals/validators.py 只映射 dorm_manager 和 counselor，dean step 不会匹配任何申请
状态；backend/apps/applications/tests/test_application_flow.py 也断言最终 approv
als 数量为2。虽然 ApprovalStep 模型仍保留 dean 枚举、历史 migration/文档中有 pen
ding_dean 痕迹，但运行时主流程不会创建 dean approval，因此 smoke_test.sh 第288行
后期待 pending_dean 是过期的3级流程假设。"
}
[RESPONSE_END]
tokens used
37,652

