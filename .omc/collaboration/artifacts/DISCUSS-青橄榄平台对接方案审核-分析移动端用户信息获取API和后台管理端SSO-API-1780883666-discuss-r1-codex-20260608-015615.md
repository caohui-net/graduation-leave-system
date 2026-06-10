docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:171:-
 `test_list_cross_counselor_negative` ✅
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:172:-
 `test_list_dean_pending_approval_positive` ✅
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:15:1. ✅
**P1准确**：User模型缺失phone/email/department字段，mapper输出无法安全持久化
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:28:**Code
x指出：** mapper输出phone/department，但User模型只到graduation_year，缺这些字段
。
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:39:    cl
ass_id = CharField(max_length=50, null=True, blank=True)
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:42:    #
缺失: phone, email, department
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:46:- 字段
契约定义phone/email/department为"API补充字段"
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:57:**Code
x指出：** 字段契约说Phase 1不创建新用户，但mapper对合法学生返回class_id=None且sk
ip_reason=None。
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:61:- 但cl
ass_id/is_graduating/graduation_year都是None
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:71:
  result['warnings'].append('would_create_but_blocked: API lacks class_id')
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:112:5. ph
one/department无模型字段 → 输出warning
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:121:5. 不
覆盖class_id/is_graduating/graduation_year
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:122:6. ph
one/department无模型字段warning
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:135:- 给U
ser增加phone/email/department字段
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:145:- 字
段契约已定义phone/email/department为API补充字段
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:184:- 当
前提取：number, name, user_identity, phone, department
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:201:5. ✅
 识别User模型缺phone/email/department
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:214:- 选
项1：增加phone/email/department字段（推荐）
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.m
d:28:- smoke 覆盖 H1 happy path、H2 counselor reject、N2 cross-counselor 403。
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md:14:- Week 2: C
lassMapping模型、CSV导入命令、动态辅导员分配、CSV模板
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:35:- Cou
nselor access checks `application.class_id == user.class_id` or matching approva
l.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:36:- App
lication detail checks `ClassMapping(counselor=user, class_id=application.class_
id, active=True)`.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:37:- Dea
n attachment access allows any matching dean approval.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:38:- App
lication detail currently allows only own pending dean approval.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:73:- Upl
oad forbidden: student cannot upload to another student's application; counselor
/dean cannot upload.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:75:- Lis
t visibility: student own positive, student other negative, assigned counselor p
ositive, cross-counselor negative, assigned dean positive or negative according
to the final RBAC decision.
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:24:- dep
artment: CharField(max_length=100, null=True, blank=True)
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:31:- CSV
主导：user_id/name/role/class_id/is_graduating/graduation_year
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:32:- API
补充：phone/email/department
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:38:**当
前状态：** mapper只提取phone/department，缺email
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:72:- 只
更新已存在学生的phone/email/department
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:91:1. ✅
 migration只包含phone/email/department
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:171:
for field in ['phone', 'email', 'department']:
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.m
d:76:- 验证服务执行后DB中class_id/is_graduating/graduation_year不变
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.m
d:124:**质疑：** 是否需要验证warning提示缺少class_id等核心字段？
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:1
4:但有一个必须先澄清并落地的小问题：`would_update_count`现在按"本地存在且role=st
udent"计数。若该字段表示"真实可写更新数"，当前User模型没有`phone/email/departmen
t`，`name`是否允许API覆盖也未决，因此真实可更新字段数应为0。若该字段表示"未来可
更新候选数"，则字段名有误导性，测试必须明确锁定这个语义。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:2
4:**问题描述：** 当前实现只要本地用户存在且角色为`student`，就执行`would_update_
count += 1`。这符合文档97第4条"已存在学生计入would_update_count"，但与字段覆盖文
档的Phase 1事实存在张力：User模型当前没有`phone/email/department`字段，`name`是
否允许由API覆盖仍未决。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:3
0:- 保留当前计数也可以，但warning文本应更强：`would_update_count` candidates exi
st, but no supplemental API fields can be persisted until User model adds phone/
email/department or name overwrite policy is approved。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:3
7:**问题描述：** 当前只有`would_update_count > 0`时才输出模型字段gap warning。若
输入中只有missing_local用户，但mapper已经产出`phone/department`，仍然存在同一个
字段gap和Phase 1创建阻塞问题，只是现在只有逐用户`would_create_but_blocked` warni
ng。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:4
2:- 至少在`mapped_count > 0`且任一mapped结果包含`phone`或`department`时输出字段g
ap warning。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:6
5:7. 服务没有写DB，不会覆盖`class_id/is_graduating/graduation_year`。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:7
7:如果`would_update_count`表示"现有学生同步候选"，当前实现正确。如果表示"当前真
实可写更新"，当前实现不准确，因为可安全写入字段未成立：`phone/email/department`
不存在，`name`覆盖策略未决。建议在Step 4A把它定义为候选数，并用warning明确真实写
入仍不可执行。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:9
1:- 服务执行后本地User的`class_id/is_graduating/graduation_year`保持不变；
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:1
00:2. "不覆盖class_id/is_graduating/graduation_year"：断言服务只读后DB原值不变，
不要模拟Step 4B写入行为。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:1
01:3. "phone/department无模型字段warning"：断言warning文本明确说明不能持久化补充
字段，并且不会影响`existing_count`。
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md
:61:- **Option 3：** 扩展通知实体类型（dorm_clearance或student），定义幂等键
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md
:81:4. 调整现有测试（test_dorm_blocked_does_not_create_notification）
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:95:**问题1：是
否新增phone/email/department字段？**
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:115:1. 评估pho
ne/email/department字段业务价值
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:3
5:5. phone/department无模型字段 → 输出warning
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:7
5:5. 不覆盖class_id/is_graduating/graduation_year
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:7
6:6. phone/department无模型字段warning
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:9
0:- API不创建新用户（缺class_id/is_graduating/graduation_year）
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:9
1:- mapper返回class_id=None但skip_reason=None的情况必须处理
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:1
02:- mapper输出phone/department
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:1
35:- phone/department（模型无字段，不能写）
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:1
62:文档97要求测试"不覆盖class_id/is_graduating/graduation_year"。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:28:当前 `map_xg_user_to_internal()` 输出 `phone` 和 `department`，字段覆盖契约
也把 `phone`、`email`、`department`定义为 API 补充字段。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:36:- `class_id`
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:40:没有 `phone`、`email`、`department` 持久化字段。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:42:这意味着如果 Step 4 现在直接做“幂等 upsert 并写库”，实际可安全写入的 API 字
段非常有限。`class_id`、`is_graduating`、`graduation_year`按共识不由 API 覆盖；`
role`仅用于过滤学生；`user_id`是主键；剩下只有 `name` 可能可更新，但它属于 CSV
主导核心字段，不应在没有明确策略时被 API 静默覆盖。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:48:字段契约明确 Phase 1 中学工 API 不创建新学生，因为缺少 `class_id`、`is_grad
uating`、`graduation_year`。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:52:- `class_id=None`
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:90:3. 写入字段范围清晰：**目前不满足**，因为模型缺少 `phone`/`department`/`ema
il`。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:129:- 当前没有模型字段承接 `phone`/`department`：输出 warning，不能声明可写入
。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:137:- 不覆盖 `class_id`、`is_graduating`、`graduation_year`
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:138:- 无 phone/department 模型字段时输出明确 warning
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:144:1. **模型扩展路线**：给 `User` 增加 `phone`、`email`、`department` 等 API
补充字段，再实现幂等更新。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:177:   - 当前模型与字段契约不一致，不能假装 `phone`/`department` 可 upsert。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:183:   - `name`、`class_id`、毕业字段由 CSV 主导，API 覆盖必须有明确规则。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.m
d:197:1. mapper 返回 `phone`/`department` 是合理的，但 Step 4 不能把它们视为可持
久化字段，除非模型扩展。
docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-stra
tegy.md:77:- 阈值：counselor 3天，dean 2天
docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-stra
tegy.md:106:- 覆盖：counselor/dean超时场景
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:247:
- 实现`notify_dorm_clearance_blocked(student, dorm_status)`
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.
md:40:if not dorm_response.get('cleared'):
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.
md:50:def test_dorm_blocked_does_not_create_notification(self):
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.
md:106:- 允许entity_type为dorm_clearance或student
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.
md:129:4. **测试调整：** 如果创建通知，test_dorm_blocked_does_not_create_notific
ation需要如何修改？
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:1
40:5. 字段采样：仅检查人员记录是否包含 `name/number/phone/identity_id/department
/user_identity/updated_at` 等文档字段。
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:31:
**Codex正确。** `backend/apps/users/management/commands/import_csv.py`已存在，支
持students/counselors/mappings导入。但当前实现缺少：
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:74:
- 增加强校验：必填字段、重复主键、班级映射引用辅导员存在、学生class_id有映射
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md
:71:- 强化：`test_dorm_blocked_does_not_create_notification`断言
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md
:146:- 服务层`notify_application_submitted(application, counselor_approval)`保证
approval存在
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:119:-
 Counselor/dean can view/download according to backend RBAC.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:128:-
 Do dorm-system stakeholder/contact/document discovery now, because it is a prod
uction blocker and does not depend on DevTools.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:155:-
 dorm-system discovery in parallel.
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:33:| 5. 学工部
最终审批 | ⚠ 部分达标 | 主路径达标，但缺列表接口，dean硬编码 |
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.
md:159:1. 2020002的class_id改为CS2020-02（当前是CS2020-01）
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.
md:167:docker exec backend python manage.py shell -c "from apps.users.models imp
ort User; print(User.objects.get(user_id='2020002').class_id)"
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.
md:172:- 2020002的class_id为CS2020-02
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.
md:361:- 先修复2020002的class_id（5分钟）
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:65:
- 辅导员列表：GET /api/applications/?role=counselor
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:66:
- 学工部列表：GET /api/applications/?role=dean
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:109
:- 是否需要同时校验`class_id`？（辅导员只能审批自己班级）
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.
md:53:- 未完成项只剩列表接口、完整负向smoke、ClassMapping、并发压力和清理类任务
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.
md:57:- 重复审批仍能改变状态或重复创建dean approval
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.
md:104:docker exec backend python manage.py shell -c "from apps.users.models imp
ort User; print(User.objects.get(user_id='2020002').class_id)"
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.
md:115:- 防重复dean approval
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.
md:179:- Conditional Go：Day 3只做列表接口、完整负向smoke、ClassMapping/并发/清
理
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.
md:189:3. `get_application`不再让任意counselor/dean查看所有申请
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.
md:190:4. 审批状态机保护覆盖approve/reject，且不会重复生成dean approval
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.
md:198:3. ClassMapping二次校验
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.
md:246:- ⚠ ClassMapping二次校验
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review
.md:88:**部分接受Codex建议，但认为Day 2不应包含ClassMapping校验。**
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review
.md:93:- ✗ 辅导员额外校验`ClassMapping`当前映射
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review
.md:99:ClassMapping校验是**过度工程**：
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review
.md:102:- ClassMapping校验防御的是"历史/篡改approval"场景
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review
.md:115:ClassMapping校验推迟到Week 3或Day 3（如果有）。
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review
.md:118:- 学工部D001硬编码应该修复（从User表查询唯一dean）
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review
.md:395:**Codex：** ClassMapping校验、并发测试、完整smoke test
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review
.md:415:2. **ClassMapping校验是否Day 2必须？**
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review
.md:446:2. **ClassMapping校验** - Day 2过度工程
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review
.md:466:2. ClassMapping校验是否Day 2必须？
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:45:    d
ef fetch_counselors(self) -> List[CounselorDTO]:
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:132:clas
s ClassMappingImportSource(ABC):
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:134:
def fetch(self) -> ImportResult[ClassMappingDTO]:
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:151:
department: str
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:153:
class_id: str
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:243:
    Student(student_id="2020001", name="张三", class_id="CS2020-01", is_graduati
ng=True),
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:246:
    Student(student_id="2020002", name="李四", class_id="INVALID", is_graduating
=True),  # 无班级映射
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:247:
    Student(student_id="2020003", name="王五", class_id="CS2020-99", is_graduati
ng=True),  # 辅导员停用
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:248:
    Student(student_id="2020004", name="赵六", class_id="CS2020-01", is_graduati
ng=False),  # 非毕业生
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:249:
    Student(student_id="2020005", name="钱七", class_id="CS2020-01", is_graduati
ng=True, graduation_year=2027),  # 延期毕业
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:252:
counselors = [
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:257:
dorm_statuses = {
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:264:
return students, counselors, dorm_statuses
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:149:- 辅导员
列表：GET /api/applications/?role=counselor
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:150:- 学工部
列表：GET /api/applications/?role=dean
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:169:4. ✅
 applications表添加字段（counselor_id, admin_id, version, certificate_url）
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:
56:| 学生/用户 | student_id、name、role、class_id、is_graduating、graduation_yea
r、active | 微信openid、手机号、完整个人档案 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:
57:| 班级/辅导员 | class_id、counselor_id、counselor_active | 组织树、多辅导员复
杂分配 |
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execut
ion-review.md:124:- 辅导员通过只能创建一个dean approval
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execut
ion-review.md:132:- ClassMapping二次防御
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execut
ion-review.md:159:7. **dynamic dean语义风险** - 接受，必须定义多记录/缺失规则
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execut
ion-review.md:191:- 可以Day 3：列表接口、完整负向场景、ClassMapping、并发测试、
代码清理
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execut
ion-review.md:202:2. **审批权限修复** - 接受，重点转为reject复核、get_applicatio
n权限、dynamic dean
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:10:`29-d
ata-source-analysis.md` 的方向是正确的：当前数据对接文档只覆盖宿舍清退，无法完整
支撑 student、counselor、admin 三类角色的账号初始化、权限边界和自动审批分配。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:14:1. **
班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统
提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐
个配置或人工改派。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:26:| 辅
导员基本信息 | 人事系统或人工台账 | P0 | 用于创建 counselor 账号和审批权限主体。
实时同步不是 P0，但账号数据本身是 P0。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:46:| 学
生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。
字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_nam
e`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`ema
il` 可选。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:47:| 辅
导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批
量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、
`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。
 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:48:| 班
级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建
议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `cla
ss_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:100:1. *
*班级唯一标识。** 当前分析偏向 `class_name`，但班级名称可能重复、改名或跨届复用
。应要求 `class_id`，`class_name` 只用于展示。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:108:5. *
*审批人变更后的历史一致性。** 已提交申请中的 `counselor_id` 应保持历史一致，不应
因后续班级映射变更自动改写。若需改派，应由管理员显式操作并记录审计日志。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:130:3. *
*定义辅导员基本信息导入模板。** 先确保 counselor 账号存在，且 `employee_id` 可被
映射数据引用。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:87:`get
_students(filters) -> List[Student]`、`get_counselors()`、`get_class_mapping() -
> Dict[str, str]` 太粗，缺少：
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:100:- `
StudentSourceProvider` / `CounselorSourceProvider` / `ClassMappingSourceProvider
`
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:144:-
重复 class_id
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:211:│
- ClassMappingSourceProvider               │
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:175:- counselor
_id BIGINT（固定辅导员ID）
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:204:    if self
.status in ['draft', 'pending_counselor', 'pending_admin']:
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:207:
 status__in=['draft', 'pending_counselor', 'pending_admin'],
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:256:counselor =
 models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:276:('dorm_inte
gration_type', 'api', 'integration', FALSE)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:277:('dorm_api_
url', 'https://dorm.edu/api', 'integration', FALSE)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:278:('dorm_api_
key', 'encrypted_key', 'integration', TRUE)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:281:('dorm_inte
gration_type', 'database', 'integration', FALSE)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:282:('dorm_db_c
onfig', '{"type":"mysql",...}', 'integration', TRUE)
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:61:-
 添加字段更新逻辑（counselor_id、admin_id、current_approver_id、version）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:54:
      "provider": "dorm_checkout",
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:67:
**问题：** 登录响应返回部分UserDTO（只有user_id/name/role/class_id），未说明是完
整DTO还是子集。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:72:
> **说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必
需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduat
ion_year 等完整字段。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:235
:    condition=Q(status__in=["draft", "pending_counselor", "pending_admin"], is_
deleted=False),
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:293
:建议新增 `counselor_assignments` 或在用户/班级模型中维护负责关系，并在查询和审
批时同时校验 `current_approver_id`。
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:57:
      status__in=['pending_counselor', 'pending_admin']
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:69:counse
lor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # 允许为空
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:44:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:46:| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2020-01 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:67:    department,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:69:    class_id,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:105:| 宿舍楼栋 | dorm_building | 文本 | 否 | 宿舍楼栋名称 | 1号楼 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:106:| 宿舍房间号 | dorm_room | 文本 | 否 | 宿舍房间号 | 101 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:117:- 接口地址：`/api/dorm/checkout/status`
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:126:    dorm_building,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:127:    dorm_room,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:133:FROM dorm_checkout
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:138:- 文件名：`dorm_checkout_YYYYMMDD.csv`
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:159:| 院系 | department | 文本 | 否 | 所属院系 | 计算机学院 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:172:    department,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:174:FROM counselors
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:180:GET /api/counselors?is_active=true
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:184:- 文件名：`counselors_YYYYMMDD.csv`
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:207:| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2020-01 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:209:| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T2020001 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:210:| 辅导员姓名 | counselor_name | 文本 | 否 | 辅导员姓名（用于展示） | 李老
师 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:211:| 院系 | department | 文本 | 否 | 所属院系 | 计算机学院 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:221:    class_id,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:223:    counselor_employee_id,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:224:    counselor_name,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:225:    department,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:228:FROM class_counselor_mapping
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:234:GET /api/class-counselor-mapping?grade=2020
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:238:- 文件名：`class_counselor_mapping_YYYYMMDD.csv`
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:302:  "host": "dorm-db.example.com",
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:304:  "database": "dorm_system",
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:385:- 学生表中的class_id必须在班级-辅导员映射表中存在
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.m
d:386:- 班级-辅导员映射表中的counselor_employee_id必须在辅导员表中存在
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:57:
3. **dean选择方式。** 短期可保留 `D001`，但如果实现动态查询成本很低，可以顺手修
；不应阻塞核心安全项。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:80:
   approve/reject 已有 approver 和 pending 检查，但没有 `transaction.atomic()`、
`select_for_update()`、application.status 与 approval.step 匹配校验，也没有防重
复 dean approval 的唯一约束或查询保护。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:83:
   counselor/dean 仍可读取任意申请，和不可跳过项冲突。该项应保留在核心修复内，不
可降级为清理项。
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:28:| 辅导员
| counselor | ~50人 | 一级审批 | 人事系统 + 教务系统 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:47:- 院系（d
epartment）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:73:- 宿舍信
息（dorm_building, dorm_room, bed_number）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:97:- 院系（d
epartment，可选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:118:- 辅导员
工号（counselor_employee_id）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:119:- 院系（
department）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-reque
st.md:69:   - 定义StudentDTO、CounselorDTO、ClassMappingDTO
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:35:1
. `TRUNCATE users` 会触发外键约束冲突（applications.student_id、applications.cou
nselor_id、applications.admin_id都引用users.id）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:49:
   role ENUM('student', 'counselor', 'admin') NOT NULL,
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:58:I
NSERT INTO users (student_id, name, department, ...)
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:59:S
ELECT student_id, name, department, ...
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:63:
   department = VALUES(department),
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:84:-
 历史申请记录中的 `student_id`、`counselor_id`、`admin_id` 仍然有效
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:120:
    role ENUM('student', 'counselor', 'admin') NOT NULL,
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:121:
    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:123:
    class_id VARCHAR(50),        -- 新增（见问题3）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:138:
        (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND student_
id IS NULL)
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:155:
    else:  # counselor or admin
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:165:
### 2.3 问题3：class_id缺失（行381）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:167:
**Codex意见：** 班级-辅导员映射需要 `class_id` 作为核心键，但当前users表只有 `cl
ass_name`。
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:182:
班级-辅导员映射表使用 `class_id`：
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:184:
CREATE TABLE class_counselor_mapping (
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:185:
    class_id VARCHAR(50) PRIMARY KEY,
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:186:
    counselor_employee_id VARCHAR(50) NOT NULL,
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:192:
1. 学生提交申请时，系统需要根据 `users.class_id` 查询 `class_counselor_mapping`
确定辅导员
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:193:
2. 但当前 `users` 表没有 `class_id` 字段
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:198:
在 `users` 表中新增 `class_id` 字段：
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:202:
ADD COLUMN class_id VARCHAR(50) AFTER major;
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:204:
-- 为学生账号添加索引（辅导员/管理员的class_id为空）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:205:
CREATE INDEX idx_class_id ON users(class_id);
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:209:
- `class_id`：班级唯一标识（如 `CS2022-01`），全校唯一
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:211:
- 学生账号：`class_id` 必填，`class_name` 可选
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:212:
- 辅导员/管理员账号：`class_id` 和 `class_name` 都为空
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:218:
student_id,name,department,major,class_id,class_name,grade,graduation_year,is_gr
aduating
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:227:
    class_id=row['class_id'],      # 核心键
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:237:
    if not student or not student.class_id:
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:240:
    # 根据class_id查询辅导员
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:241:
    mapping = ClassCounselorMapping.query.filter_by(class_id=student.class_id).f
irst()
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:243:
        raise ValueError(f"班级 {student.class_id} 未配置辅导员")
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:245:
    counselor = User.query.filter_by(
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:246:
        employee_id=mapping.counselor_employee_id,
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:247:
        role='counselor'
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:249:
    if not counselor or not counselor.is_active:
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:255:
        counselor_id=counselor.id,  # 快照，不受后续映射变更影响
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:305:
    import_type ENUM('student', 'counselor', 'class_mapping') NOT NULL,
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:328:
    {"row": 12, "field": "class_id", "error": "班级ID不存在"}
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:409:
   - 新增 `class_id` 字段
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:437:
- 新增 `class_id` 字段（必填）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:438:
- 说明 `class_id` 是班级唯一标识，用于映射辅导员
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:466:
3. ✅ 新增 `class_id` 字段到users表
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:64:    co
unselor = models.ForeignKey(
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:68:
  related_name='counselor_applications',
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:107:
       models.Index(fields=['counselor_id']),
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:155:    d
epartment = models.CharField(max_length=100, null=True)
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:195:
   if self.status in ['draft', 'pending_counselor', 'pending_admin']:
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:198:
           status__in=['draft', 'pending_counselor', 'pending_admin'],
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:219:WHERE
 status IN ('draft', 'pending_counselor', 'pending_admin')
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:16:   - users表：`student_id`改为可空，新增`employee_id`和`class_id`字段
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:17:   - 新增`class_counselor_mapping`表（班级-辅导员映射）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:20:   - 拆分staging表：`students_staging`、`counselors_staging`、`class_map
ping_staging`
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:23:5. **约束增强**：学生必须有`class_id`，复用`system_configs`表
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:72:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:74:| 班级ID | class_id | 文本 | 是 | 班级唯一标识（核心键） | CS2022-01 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:88:- `class_id`：班级唯一标识，全校唯一，用于映射辅导员（**v2新增必填要求**
）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:96:student_id,name,department,major,class_id,class_name,grade,graduation_ye
ar,is_graduating,phone,email
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:160:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:172:employee_id,name,department,phone,email,is_active
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:200:| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2022-01 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:202:| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T202200
1 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:213:- `class_id`：班级唯一标识，必须全校唯一，不能重复、变更或跨届复用
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:214:- `counselor_employee_id`：必须在辅导员表中存在且 `is_active=true`
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:215:- 首版只支持一班一主辅导员，同一 `class_id` 不能出现多次
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:220:class_id,class_name,counselor_employee_id
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:226:- 学生表中的 `class_id` 必须在班级映射表中存在
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:227:- 班级映射表中的 `counselor_employee_id` 必须在辅导员表中存在
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:231:- 已提交申请的 `counselor_id` 不自动改写，保持历史一致性
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:249:| 部门 | department | 文本 | 是 | 所属部门 | 学工部 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:298:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:300:    class_id VARCHAR(50),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:310:CREATE TABLE counselors_staging (
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:313:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:320:    class_id VARCHAR(50) PRIMARY KEY,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:321:    counselor_employee_id VARCHAR(50) NOT NULL
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:335:INSERT INTO users (student_id, name, department, class_id, role, is_act
ive, password_setup_required, ...)
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:336:SELECT student_id, name, department, class_id, 'student', true, true, .
..
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:340:    department = VALUES(department),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:341:    class_id = VALUES(class_id),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:367:    import_type ENUM('student', 'counselor', 'class_mapping') NOT NULL,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:393:    {"row": 12, "field": "class_id", "error": "班级ID不存在"}
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:520:4. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:597:- 新增 `class_id VARCHAR(50)` 字段（可空）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:602:      (role = 'student' AND student_id IS NOT NULL AND employee_id IS N
ULL AND class_id IS NOT NULL) OR
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:603:      (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND s
tudent_id IS NULL AND class_id IS NULL)
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:617:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:619:    class_id VARCHAR(50),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:629:**2. counselors_staging - 辅导员导入临时表**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:631:CREATE TABLE counselors_staging (
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:634:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:643:    class_id VARCHAR(50) PRIMARY KEY,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:644:    counselor_employee_id VARCHAR(50) NOT NULL
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:648:**4. class_counselor_mapping - 班级-辅导员映射表（核心表）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:650:CREATE TABLE class_counselor_mapping (
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:652:    class_id VARCHAR(50) NOT NULL COMMENT '班级唯一标识',
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:653:    counselor_employee_id VARCHAR(50) NOT NULL COMMENT '辅导员工号',
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:662:    UNIQUE KEY uk_class_active (class_id, is_active),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:663:    FOREIGN KEY (counselor_employee_id) REFERENCES users(employee_id) O
N DELETE RESTRICT,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:666:    INDEX idx_class_id (class_id),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:667:    INDEX idx_counselor_employee_id (counselor_employee_id)
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:690:    import_type ENUM('student', 'counselor', 'class_mapping') NOT NULL,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:723:2. ✅ 数据库模型调整：users表增加employee_id和class_id，调整约束
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:724:3. ✅ 新增6个表：3个staging表、class_counselor_mapping、graduation_batc
hes、import_logs
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:727:6. ✅ 约束增强：学生必须有class_id，复用system_configs表
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:58:
- `provider: dorm_checkout`
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:76:
Section 4.1说明 `user` 是 `AuthUserDTO`，是 `UserDTO` 的子集，只包含 `user_id/na
me/role/class_id`。这解决了“登录响应到底是不是完整UserDTO”的歧义。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:87:
    class_id: Optional[str] = None
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:17
0:权限矩阵只有3个角色（student/counselor/admin），但：
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:18
0:counselor        # 辅导员（只能查看本年级）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:18
1:counselor_lead   # 年级组长（可查看本学院所有年级）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:19
5:            student__department=request.user.department
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation
.md:24:**问题4：** `class_id`（班级ID）是否全校唯一？班级名称是否可能重复、变更
或跨届复用？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation
.md:26:**背景说明：** 系统需要用 `class_id` 作为核心键映射辅导员，如果只有班级名
称，可能导致映射错误。
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation
.md:151:   - 班级映射覆盖率（所有学生的class_id都有对应辅导员）
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:61:# apps/
integrations/dorm_system.py
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:64:
 config = SystemConfig.objects.get(config_key='dorm_api_url')
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:66:
 self.api_key = SystemConfig.objects.get(config_key='dorm_api_key').config_value
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:80:('dorm_
api_url', 'https://dorm.university.edu', 'integration'),
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:81:('dorm_
api_key', 'encrypted_key_here', 'integration');
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:163:('dorm
_api_url', 'https://dorm.university.edu/api', 'integration', FALSE),
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:164:('dorm
_api_key', 'encrypted_api_key', 'integration', TRUE);
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:170:('dorm
_db_config', '{"type":"mysql","host":"10.0.1.50","port":3306,"database":"dorm","
user":"readonly","password":"P@ssw0rd"}', 'integration', TRUE);
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:101
:- 班级 `class_id`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:109
:2. **业务字段层：** 宽松采样，记录 `name/number/phone/identity_id/department/us
er_identity/user_auth_extra_field` 是否出现，不因业务字段缺失直接失败。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:134
:字段: name=yes number=yes phone=yes department=yes user_identity=yes
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:43
:  "dorm_building": "1号楼",
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:44
:  "dorm_room": "101",
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:13
3:student_id → name → class_name → dorm_building → dorm_room → bed_number → is_c
hecked_out → ...
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:13
8:- 宿舍信息：dorm_building、dorm_room、bed_number
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:20
4:- class_name vs class_id
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:87:
"dorm_building": "1号楼",
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:88:
"dorm_room": "101",
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:100:- `
room_no` → `dorm_building` + `dorm_room`
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:116:| d
orm_building | String | 宿舍楼栋 | 是 | "1号楼" |
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:117:| d
orm_room | String | 宿舍房间号 | 是 | "101" |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:176
:- 班级映射CSV：`counselor_employee_id` → 查询 `users` 表中 `employee_id` 匹配的
记录
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:182
:**问题：** 班级-辅导员映射变更后，已提交申请中的 `counselor_id` 是否自动改写？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:208
:| 申请提交时 | 根据当前班级-辅导员映射确定 `counselor_id` |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:209
:| 映射变更后，已提交申请 | `counselor_id` **不变**，保持原审批人 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:210
:| 映射变更后，新提交申请 | 使用新映射确定 `counselor_id` |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:214
:- `applications` 表的 `counselor_id` 是快照字段，不关联外键级联更新
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:237
:2. 班级-辅导员映射表中，`class_id` 必须唯一
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:238
:3. CSV导入时强校验：同一 `class_id` 不能出现多次
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:252
:2. 允许同一 `class_id` 有多条记录，但只能有一个 `is_primary=true`
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:253
:3. 申请提交时使用主辅导员作为 `counselor_id`
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:381
:4. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:496
:- 补充说明：`class_id` 必须唯一，不允许重复
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:4
8:**Codex指出：** 系统设计文档使用is_cleared/clearance_date/room_no，数据对接文
档使用is_checked_out/checkout_date/dorm_building/dorm_room。
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:6
0:  - `dorm_building` + `dorm_room`（而非room_no）
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:9
8:   - [ ] 第1638行：room_no → dorm_building（或拆分为dorm_building + dorm_room
）
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:1
16:| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:1
17:| dorm_room | String | 宿舍房间号 | 是 | "101" |
docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strat
egy.md:159:} else if (res.user.role === 'counselor' || res.user.role === 'dean')
 {
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:40:- ✅ 添
加counselor_id, admin_id, version, certificate_url, certificate_generated_at
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-d
atabase.md:27:├── dorm/            # 宿舍系统集成
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:62:- 替
换数据库配置示例为外部集成配置（`dorm_integration_type`、`dorm_api_url`、`dorm_d
b_config`）
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:83:   -
 `counselor_id`
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:35
:| 班级-辅导员对应关系 | 完整且必要 | 是自动分配 `counselor_id` 和权限边界的关键
数据。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:56
:字段整体合理，能支撑首版业务。`student_id`、`name`、`department`、`major`、`cla
ss_id`、`class_name`、`grade`、`graduation_year`、`is_graduating` 作为必填基本可
接受。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:80
:3. `dorm_building`、`dorm_room`、`bed_number` 可选是可接受的，但应说明这些字段
仅用于展示、核对和异常排查，业务判定不得依赖床位文本匹配。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:97
:该章节是文档中最关键、也最合理的部分。`class_id` 作为必填是正确的，避免只靠班级
名称匹配。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:10
3:3. **历史一致性规则。** 班级映射变更后，不应自动改写已提交申请中的 `counselor_
id`；已提交申请如需改派，应由管理员显式操作并记录审计日志。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:18
2:3. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:27
7:1. `employee_id` 必须全校唯一，并与班级映射中的 `counselor_employee_id` 完全一
致。
docs/discussions/codex-review-2026-05-27/04-database-review.md:70:WHERE status =
 'pending_counselor'
docs/discussions/codex-review-2026-05-27/04-database-review.md:164:- 无`counselo
r_id`（只有`current_approver_id`会变）
docs/discussions/codex-review-2026-05-27/04-database-review.md:180:    counselor
_id BIGINT COMMENT '辅导员ID',
docs/discussions/codex-review-2026-05-27/04-database-review.md:190:    FOREIGN K
EY (counselor_id) REFERENCES users(id),
docs/discussions/codex-review-2026-05-27/04-database-review.md:192:    INDEX idx
_counselor_id (counselor_id),
docs/discussions/codex-review-2026-05-27/04-database-review.md:244:WHERE status
IN ('draft', 'pending_counselor', 'pending_admin')
docs/discussions/codex-review-2026-05-27/04-database-review.md:251:        if se
lf.status in ['draft', 'pending_counselor', 'pending_admin']:
docs/discussions/codex-review-2026-05-27/04-database-review.md:254:
   status__in=['draft', 'pending_counselor', 'pending_admin'],
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:56
:系统设计文档中的响应仍使用 `is_cleared`、`clearance_date`、`room_no`，而数据对
接文档定义的是 `is_checked_out`、`checkout_date`、`dorm_building`、`dorm_room`
等字段；在补充 `class_name` 和 `bed_number` 后仍保留两套命名，会让实现方按不同文
档接出不兼容的 payload。
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:25:### 2
. ClassMapping校验是否Day 2必须？
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:31:- Cla
ssMapping防的是更弱、更后置的场景
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:130:3. *
*ClassMapping校验（可选）** - 如果业务需要
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:151:- ⚠
ClassMapping校验
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:190:- Cl
assMapping校验、并发测试、完整smoke test是工程完整性要求
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:197:- Cl
assMapping、并发测试推到Day 3或Week 3
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:206:- 接
受ClassMapping推迟到Day 3/Week 3
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integ
ration.md:37:        status__in=['pending_counselor', 'pending_admin']
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integ
ration.md:77:        status__in=['pending_counselor', 'pending_admin'],
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integ
ration.md:91:    'draft': ['pending_counselor'],
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integ
ration.md:92:    'pending_counselor': ['pending_admin', 'rejected'],
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integ
ration.md:115:        if app.status == 'pending_counselor':
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integ
ration.md:179:    result = dorm_api.check_status(student_id, timeout=2)
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integ
ration.md:187:def retry_dorm_check(student_id):
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integ
ration.md:188:    result = dorm_api.check_status(student_id)
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request
.md:70:    def get_counselors(self) -> List[Counselor]:
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request
.md:99:                department="计算机学院",
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request
.md:101:                class_id="CS2020-01",
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request
.md:109:    def get_counselors(self):
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request
.md:126:            dorm_building="1号楼",
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request
.md:127:            dorm_room="101"
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request
.md:167:def get_dorm_checkout_provider() -> IDormCheckoutProvider:
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:32:
 - 将替换为：外部系统集成配置（`dorm_integration_type`、`dorm_api_url`、`dorm_db
_config`）
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:83:
 - 将添加：提交时设置`counselor_id`、`admin_id`
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:103:-
 添加完整的字段更新逻辑（counselor_id、admin_id、current_approver_id、version）
docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.m
d:4:**Context:** Phase 4 regression testing blocker - missing dorm_manager field
s in ClassMapping migration
docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.m
d:18:1. Add `null=True` to dorm_manager fields temporarily
docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.m
d:47:   - `docker compose exec backend python manage.py shell -c "from apps.user
s.models import ClassMapping; print(ClassMapping.objects.count())"`
docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.m
d:50:   - Add `null=True, blank=True` to both dorm_manager fields
docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.m
d:61:- Test fixtures will provide complete ClassMapping objects
docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.m
d:67:- Model validation less strict (allows null dorm_manager)
docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.m
d:77:2. Make dorm_manager fields nullable
docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.m
d:91:1. Check ClassMapping table row count in Docker database
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:22:- Gene
rated migration 0003 - added nullable dorm_manager fields to ClassMapping
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:23:- Gene
rated migration 0004 - backfilled dorm_manager data (counselor as fallback)
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:27:- Adde
d `ApplicationStatus.PENDING_DEAN` for dean approval state
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:31:- Adde
d dean approval creation when counselor approves
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:42:- Test
s not creating dean users in setUp()
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:43:- Test
s expecting old 2-step workflow (counselor → admin)
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:48:- `tes
t_cross_counselor_approve_forbidden` - approval endpoint error
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:49:- `tes
t_dean_rejection` - likely missing dean user fixture
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:52:Tests
checking dean-specific permissions fail, likely due to:
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:53:- Test
 fixtures not creating dean approval records
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:58:- `tes
t_dean_sees_only_pending_dean_approvals`
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:59:- `tes
t_dean_cannot_access_non_assigned_application`
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:66:**Orig
inal design:** 2-step (counselor → admin/dean)
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:67:**Phas
e 3 addition:** Added dorm_manager without completing workflow
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:68:**Curr
ent state:** 3-step workflow implemented (dorm_manager → counselor → dean)
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:72:1. Upd
ate test fixtures to create dean users
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:75:4. Upd
ate permission checks for dean role
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:82:2. `ba
ckend/apps/users/class_mapping.py` (dorm_manager fields nullable)
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:83:3. `ba
ckend/apps/users/migrations/0003_*.py` (add dorm_manager fields)
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:84:4. `ba
ckend/apps/users/migrations/0004_*.py` (backfill dorm_manager data)
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:87:7. `ba
ckend/apps/approvals/views.py` (added dean approval creation)
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:94:1. Upd
ate test fixtures to create dean users
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:5:**Co
ntext:** Phase 4 regression testing after Step 4B Phase 3 (dorm_manager integrat
ion)
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:11:Pha
se 4 regression tests revealed **breaking changes** from adding dorm_manager ste
p to approval workflow. The 3-step workflow (counselor → dean) was expanded to 4
-step (counselor → dorm_manager → dean), but enum definitions and approval creat
ion logic were not updated consistently.
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:22:DET
AIL:  Failing row contains (apv_09824ea3, dorm_manager, null, pending, null, nul
l, ...)
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:28:Whe
n creating dorm_manager approval, code doesn't set `approver_name` field:
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:30:dor
m_manager_approval = Approval.objects.create(
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:32:
 approver=class_mapping.dorm_manager,
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:38:**I
mpact:** All application creation tests fail when trying to create dorm_manager
approval.
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:61:- T
ests assume 3-step workflow (counselor → dean) but code now has 4-step workflow
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:80:1.
✓ Added `dorm_manager` fields to ClassMapping model
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:83:4.
✓ Updated application creation logic to create dorm_manager approval
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:86:1.
✗ `approver_name` not set when creating dorm_manager approvals
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:96:
- Should we keep 3-step workflow (counselor → dean) and make dorm_manager option
al?
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:97:
- Or fully implement 4-step workflow (counselor → dorm_manager → dean)?
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:103:
 - How should `ApprovalStep.DEAN` be handled if dorm_manager comes before dean?
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:107:
 - Should we derive it from `approver.name` or from `ClassMapping.dorm_manager_n
ame`?
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:124:-
Application creation tests (IntegrityError on dorm_manager approval)
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:35:    role ENUM('student', 'counselor', 'admin') NOT NULL,
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:42:2. 辅导员导入：`student_id=NULL, employee_id='T001', role='counselor'` → 主
键包含NULL，插入失败
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:51:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:53:    class_id VARCHAR(50),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:63:CREATE TABLE counselors_staging (
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:66:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:73:    class_id VARCHAR(50) PRIMARY KEY,
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:74:    counselor_employee_id VARCHAR(50) NOT NULL
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:86:INSERT INTO users (student_id, name, department, major, class_id, role, is_a
ctive, ...)
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:87:SELECT student_id, name, department, major, class_id, 'student', true, ...
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:91:    department = VALUES(department),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:92:    class_id = VALUES(class_id),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:119:### 2.2 问题2：缺少class_counselor_mapping表定义（行412）
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:127:文档多处引用`class_counselor_mapping`表：
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:132:**修正方案：正式定义class_counselor_mapping表**
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:135:CREATE TABLE class_counselor_mapping (
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:137:    class_id VARCHAR(50) NOT NULL COMMENT '班级唯一标识',
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:138:    counselor_employee_id VARCHAR(50) NOT NULL COMMENT '辅导员工号',
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:152:    UNIQUE KEY uk_class_active (class_id, is_active),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:155:    FOREIGN KEY (counselor_employee_id) REFERENCES users(employee_id) ON DE
LETE RESTRICT,
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:160:    INDEX idx_class_id (class_id),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:161:    INDEX idx_counselor_employee_id (counselor_employee_id),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:170:| class_id | VARCHAR(50) | 班级唯一标识，如 `CS2022-01` |
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:171:| counselor_employee_id | VARCHAR(50) | 辅导员工号，引用 `users.employee_id
` |
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:179:`UNIQUE KEY uk_class_active (class_id, is_active)` 确保：
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:186:def get_counselor_for_class(class_id, graduation_batch_id=None):
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:189:        class_id=class_id,
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:202:        raise ValueError(f"班级 {class_id} 未配置辅导员")
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:207:        raise ValueError(f"班级 {class_id} 的辅导员映射尚未生效")
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:209:        raise ValueError(f"班级 {class_id} 的辅导员映射已失效")
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:250:    role ENUM('student', 'counselor', 'admin') NOT NULL,
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:269:        (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND stu
dent_id IS NULL)
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:352:### 2.4 问题4：class_id约束不完整（行135-139）
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:354:**Codex意见：** 检查约束只检查学生/员工标识互斥，没有检查学生必须有 `class_
id`。
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:360:当前约束只检查 `student_id` 和 `employee_id` 互斥，未检查学生必须有 `class_
id`。
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:365:-- 增强的检查约束：学生必须有student_id和class_id
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:367:    (role = 'student' AND student_id IS NOT NULL AND employee_id IS NULL AN
D class_id IS NOT NULL) OR
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:368:    (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND student
_id IS NULL AND class_id IS NULL)
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:380:        if not row.get('class_id'):
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:381:            errors.append({"row": row_num, "field": "class_id", "error": "
班级ID不能为空"})
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:441:- 新增 `class_id` 字段（可空）
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:443:- 修改 `chk_user_identity` 约束：增加 `class_id` 必填检查
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:451:2. **counselors_staging** - 辅导员导入临时表
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:453:4. **class_counselor_mapping** - 班级-辅导员映射表（核心表）
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:468:2. ✅ 补充class_counselor_mapping表完整定义
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:470:4. ✅ 增强class_id约束，确保学生必须有class_id
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:55
:- 实际影响：counselor/dean访问学生申请页被踢回登录
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:67
:  if (userInfo.role === 'counselor' || userInfo.role === 'dean') {
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:10
3:  // counselor/dean继续加载
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:10
6:    counselor: '辅导员',
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:10
7:    dean: '院长',
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:19
2:- 扩展ApprovalListSerializer添加student_name/class_id/leave_date
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:21
3:   - 手工验证角色保护：student不能进approvals，counselor/dean不能停留student-a
pplication
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:80:- 5个
状态（draft, pending_counselor, pending_admin, approved, rejected）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:5
3:    def fetch_counselors(self) -> ImportResult[CounselorDTO]:
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:5
8:    def fetch_class_mapping(self) -> ImportResult[ClassMappingDTO]:
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:1
07:    department: str
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:1
09:    class_id: str
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:2
15:        Student(student_id="2020001", name="张三", class_id="CS2020-01", is_g
raduating=True),
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:2
18:        Student(student_id="2020002", name="李四", class_id="INVALID", is_gra
duating=True),  # 无班级映射
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:2
19:        Student(student_id="2020003", name="王五", class_id="CS2020-99", is_g
raduating=True),  # 辅导员停用
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:2
20:        Student(student_id="2020004", name="赵六", class_id="CS2020-01", is_g
raduating=False),  # 非毕业生
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:2
21:        Student(student_id="2020005", name="钱七", class_id="CS2020-01", is_g
raduating=True, graduation_year=2027),  # 延期毕业
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:2
24:    counselors = [
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:2
29:    dorm_statuses = {
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:2
36:    return students, counselors, dorm_statuses
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md
:33:- 状态枚举（draft/pending_counselor/pending_dean/approved/rejected）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:368:        statu
s__in=['pending_counselor', 'pending_admin'],

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/class_mapping.py" in /home
/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.db import models
from apps.users.models import User


class ClassMapping(models.Model):
    class_id = models.CharField(max_length=50, primary_key=True)
    dorm_manager = models.ForeignKey(User, on_delete=models.PROTECT, related_nam
e='managed_dorms', null=True, blank=True)
    dorm_manager_name = models.CharField(max_length=100, null=True, blank=True)
    counselor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='
managed_classes')
    counselor_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'class_mappings'

exec
/bin/bash -lc "rtk rg -n \"class ClassMapping|class_mapping|ClassMapping\" backe
nd/apps/users backend/apps/applications backend/apps/approvals -g '"'!**/migrati
ons/**'"'" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,320p' backend/apps/approvals/views.py" in /home/cao
hui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
import logging
from drf_spectacular.utils import extend_schema, OpenApiParameter
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
        OpenApiParameter('decision', str, description='决策过滤：pending/approve
d/rejected/all（默认pending）'),
        OpenApiParameter('limit', int, description='每页数量（默认20）'),
        OpenApiParameter('offset', int, description='偏移量（默认0）'),
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
        ).select_related('application', 'application__student', 'approver')

    # 辅导员: 只看自己的counselor审批
    elif user.role == UserRole.COUNSELOR:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR
        ).select_related('application', 'application__student', 'approver')

    # 学工部: 查看所有审批（存档用）
    elif user.role == UserRole.DEAN:
        queryset = Approval.objects.all().select_related('application', 'applica
tion__student', 'approver')

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
    operation_id='approvals_get',
    summary='获取审批详情',
    description='获取指定审批的详细信息',
    responses={
        200: ApprovalSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
    tags=['审批']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_approval(request, approval_id):
    try:
        approval = Approval.objects.select_related('application', 'approver').ge
t(approval_id=approval_id)
    except Approval.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存
在'}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user

    # Permission check: only the approver or dean can view this approval
    if user.role == UserRole.DEAN or approval.approver_id == user.user_id:
        return Response(ApprovalSerializer(approval).data)

    return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源
'}},
                    status=status.HTTP_403_FORBIDDEN)


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
        # Auto-complete other pending dorm manager approvals for the same buildi
ng
        # (New requirement: any dorm manager in the building can approve, others
 see "already approved")
        other_dorm_approvals = Approval.objects.filter(
            application=application,
            step=ApprovalStep.DORM_MANAGER,
            decision=ApprovalDecision.PENDING
        ).exclude(approval_id=approval.approval_id)

        if other_dorm_approvals.exists():
            other_dorm_approvals.update(
                decision=ApprovalDecision.APPROVED,
                comment=f'已由{approval.approver_name}完成审批，无需重复操作',
                decided_at=timezone.now()
            )
            logging.info(
                f"Auto-completed {other_dorm_approvals.count()} other dorm manag
er approvals "
                f"for application {application.application_id} after approval by
 {approval.approver.user_id}"
            )

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

    notify_approval_decided(approval)

    application = approval.application
    application.status = ApplicationStatus.REJECTED
    application.save()

    return Response(ApprovalSerializer(approval).data)

exec
/bin/bash -lc "rtk sed -n '1,320p' backend/apps/applications/views.py" in /home/
caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_class
es
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
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
        OpenApiParameter('status', str, description='状态过滤'),
        OpenApiParameter('limit', int, description='每页数量（默认20）'),
        OpenApiParameter('offset', int, description='偏移量（默认0）'),
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
@parser_classes([JSONParser, MultiPartParser, FormParser])
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

    # Admin: view all applications
    elif user.role == UserRole.ADMIN:
        queryset = Application.objects.all()

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
    from django.db import transaction

    user = request.user

    if user.role != UserRole.STUDENT:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以
提交申请'}},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = ApplicationCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求
参数验证失败',
                                    'details': serializer.errors}},
                        status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        # Check for existing pending/approved applications
        existing = Application.objects.select_for_update().filter(
            student=user,
            status__in=[ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatu
s.PENDING_COUNSELOR, ApplicationStatus.APPROVED]
        ).first()
        if existing:
            return Response({'error': {'code': 'CONFLICT', 'message': '已有待审
批或已通过的申请，不能重复提交',
                                        'details': {'student_id': user.user_id,
'existing_application_id': existing.application_id, 'status': existing.status}}}
,
                            status=status.HTTP_409_CONFLICT)

        provider = MockDormCheckoutProvider()
        dorm_status = provider.check_status(user.user_id)

        if dorm_status.status != DormCheckoutStatus.COMPLETED:
            return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍
清退未完成，无法提交申请',
                                        'details': {'student_id': user.user_id,
'dorm_status': dorm_status.status,
                                                    'blocking_reason': dorm_stat
us.blocking_reason}}},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Find dorm managers
        dorm_managers = []
        building = user.building

        if building and building.strip():
            dorm_managers = list(User.objects.filter(
                role=UserRole.DORM_MANAGER,
                building=building,
                active=True
            ).order_by('user_id'))

        if not dorm_managers:
            from django.conf import settings
            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92
008149')
            try:
                fallback_manager = User.objects.get(role=UserRole.DORM_MANAGER,
user_id=fallback_id, active=True)
                dorm_managers = [fallback_manager]
            except User.DoesNotExist:
                return Response({'error': {'code': 'NOT_FOUND', 'message': '无可
用宿管员',
                                            'details': {'building': building or
'未分配', 'fallback_id': fallback_id}}},
                                status=status.HTTP_404_NOT_FOUND)

        # Check for existing draft, convert if exists
        draft = Application.objects.select_for_update().filter(student=user, sta
tus=ApplicationStatus.DRAFT).first()

        if draft:
            # Update draft to submitted application
            draft.contact_phone = serializer.validated_data['contact_phone']
            draft.reason = serializer.validated_data.get('reason', '')
            draft.leave_date = serializer.validated_data['leave_date']
            draft.status = ApplicationStatus.PENDING_DORM_MANAGER
            draft.dorm_checkout_status = dorm_status.status
            draft.save()
            application = draft
        else:
            # Create new application
            application = Application.objects.create(
                application_id=f'app_{uuid.uuid4().hex[:8]}',
                student=user,
                student_name=user.name,
                class_id=user.class_id,
                contact_phone=serializer.validated_data['contact_phone'],
                reason=serializer.validated_data.get('reason', ''),
                leave_date=serializer.validated_data['leave_date'],
                status=ApplicationStatus.PENDING_DORM_MANAGER,
                dorm_checkout_status=dorm_status.status
            )

        # Create approvals
        for dorm_manager in dorm_managers:
            dorm_manager_approval = Approval.objects.create(
                approval_id=f'apv_{uuid.uuid4().hex[:8]}',
                application=application,
                step=ApprovalStep.DORM_MANAGER,
                approver=dorm_manager,
                approver_name=dorm_manager.name,
                decision=ApprovalDecision.PENDING
            )
            notify_application_submitted(application, dorm_manager_approval)

        # Sync phone to User table
        if not user.phone:
            user.phone = serializer.validated_data['contact_phone']
            user.save()

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


@extend_schema(
    operation_id='applications_draft',
    summary='获取或创建草稿申请',
    description='学生获取或创建草稿申请，用于附件上传前置',
    responses={
        200: ApplicationSerializer,
        201: ApplicationSerializer,
        403: ErrorResponseSerializer,
    },
    tags=['申请']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_or_create_draft(request):
    from django.db import transaction

    user = request.user

    if user.role != UserRole.STUDENT:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以
创建草稿'}},
                        status=status.HTTP_403_FORBIDDEN)

    with transaction.atomic():
        # Get existing draft or create new one
        draft = Application.objects.select_for_update().filter(student=user, sta
tus=ApplicationStatus.DRAFT).first()

    if draft:
        return Response(ApplicationSerializer(draft).data, status=status.HTTP_20
0_OK)

    # Create new draft
    draft = Application.objects.create(
        application_id=f'app_{uuid.uuid4().hex[:8]}',
        student=user,
        student_name=user.name,
        class_id=user.class_id,
        status=ApplicationStatus.DRAFT
    )

    return Response(ApplicationSerializer(draft).data, status=status.HTTP_201_CR
EATED)

 succeeded in 105ms:
backend/apps/approvals/tests/test_state_machine.py:7:from apps.users.class_mappi
ng import ClassMapping
backend/apps/approvals/tests/test_state_machine.py:50:        ClassMapping.objec
ts.create(

codex
[RESPONSE_START]
{
  "consensus": false,
  "decision": "方案方向可行，但不能按 /tmp/integration-analysis.md 直接进入实现
；必须先收敛为“外部身份只做登录凭证，本地 User 与审批路由仍以现有数据模型为权威”
的对接方案，并补齐映射唯一性、角色白名单、token/签名安全和组织数据来源后再开发。
",
  "blocking_issues": [
    "GoliveUserMapping 以 golive_user_code 全局唯一不成立；后台 verify-user 返回
 username/role_id/role_name，移动端返回 user_code/user_type/user_id，两条链路的
外部主体标识不同，必须设计 tenant_code + source + external_subject 的复合唯一键
。",
    "首次登录自动创建本地用户风险过高。当前 User.user_id 是主键，学生提交和审批
路由依赖 class_id、department、building、active 等字段；青橄榄移动端 user-info
文档摘要未证明能提供完整路由字段。",
    "role_name/identity_name 不能直接映射本地权限。必须配置白名单映射，并对 staf
f 账号优先采用预绑定或人工审核，否则可能把外部角色误提升为 dorm_manager/counselo
r/dean/admin。",
    "SSO token 和 saas_wap_token 的生命周期、一次性使用语义、失败码、过期码未确
认；本系统不能缓存或信任第三方 token，只能校验后签发本地 JWT，并避免在日志、Refe
rer、错误响应中泄露 query token。",
    "签名方案只描述 appSecret/timestamp/randStr 排序后 sha1/md5，但未确认 timest
amp 单位、编码、大小写、参数拼接边界、encryptionType 兼容性以及 replay nonce 规
则；需要对照真实测试用例验签。",
    "组织结构同步来源不清。当前审批实际使用 building 匹配宿管、department 匹配辅
导员，ClassMapping 也存在历史/测试依赖；青橄榄用户信息接口不能替代批量组织/班级/
楼栋同步，除非提供权威字段和同步策略。"
  ],
  "reasoning": "我同意 DISCUSS-青橄榄平台对接方案审核-分析移动端用户信息获取API
和后台管理端SSO-API-1780883666-r0-claude 的基本框架：先澄清范围、兼容性和验证证
据。进一步看当前代码后，最大风险不是能否调用青橄榄 API，而是把外部身份结果直接转
成本地账号、角色和审批路由。现有系统的权限边界绑定在 User.role、Approval.approve
r_id、Application.student、department/building 路由上；任何自动创建或自动提权都
会绕开这些本地约束。建议的统一模块 golive_auth 可以保留，但它应只负责外部凭证校
验、账号绑定查询、审计记录和签发本地 JWT，不应成为角色和组织数据的权威来源。",
  "previous_responses": [
    "DISCUSS-青橄榄平台对接方案审核-分析移动端用户信息获取API和后台管理端SSO-API
-1780883666-r0-claude"
  ],
  "targeted_challenges": [
    {
      "target_agent": "claude",
      "target_response_id": "DISCUSS-青橄榄平台对接方案审核-分析移动端用户信息获
取API和后台管理端SSO-API-1780883666-r0-claude",
      "question": "请明确“兼容性合同”具体包括哪些现有接口和数据语义：是否必须保
持 /api/auth/login 返回 access_token/token_type/user，是否保留本地密码登录，SSO
登录成功是否复用同一 AuthUser DTO。",
      "rationale": "如果 SSO 返回结构或本地登录行为不一致，前端和现有 API 文档会
产生二义性，也会增加回归风险。"
    },
    {
      "target_agent": "claude",
      "target_response_id": "DISCUSS-青橄榄平台对接方案审核-分析移动端用户信息获
取API和后台管理端SSO-API-1780883666-r0-claude",
      "question": "请补充角色与组织映射的拒绝策略：当 role_name、identity_name、
department、building、class_id 缺失或不匹配时，是拒绝登录、降级为普通用户，还是
进入待绑定状态。",
      "rationale": "这是权限安全的核心分支，不能在实现阶段用默认角色或自动创建来
兜底。"
    }
  ],
  "dissent": "不同意“首次登录自动创建用户并建立映射”作为默认策略。学生账号可考虑
仅在能用学号/工号命中现有 User 时自动绑定；管理端账号应默认要求预绑定或管理员审
核。",
  "evidence": [
    "/tmp/integration-analysis.md 中后台 verify-user 返回 tenant_code、username
、name、phone、status、role_id、role_name；移动端链路返回 tenant_code、user_code
、user_type、user_id，并需再取 user-info，说明两类主体键不同。",
    "backend/apps/users/models.py 定义 User.user_id 为 primary_key，role 仅允许
student、dorm_manager、counselor、dean、admin，且 User 还保存 class_id、phone、d
epartment、building 等业务字段。",
    "backend/apps/users/serializers.py 当前登录成功响应为 access_token、token_ty
pe、user，使用 SimpleJWT RefreshToken.for_user(user) 签发本地 JWT。",
    "backend/apps/applications/views.py 学生提交时依赖 user.role == student、use
r.building 匹配宿管或 fallback、user.class_id 写入 Application。",
    "backend/apps/approvals/views.py 审批动作要求 approval.step 与 user.role 匹
配，并且 approval.approver_id == user.user_id；宿管通过后按 application.student.
department 选择辅导员。",
    "backend/config/settings/base.py INSTALLED_APPS 当前未包含 apps.golive_auth
，SIMPLE_JWT 使用 USER_ID_FIELD=user_id，新增模块必须显式纳入 settings 和路由。"
  ],
  "action_items": [
    {
      "owner": "Claude",
      "task": "把用户映射方案改为复合外部身份模型：tenant_code、source(mobile/ad
min)、external_subject、external_type、local_user、bind_status、last_verified_at
，并定义唯一约束和冲突处理。",
      "due": "下一轮讨论前",
      "verification": "设计文档中能分别覆盖后台 username、移动端 user_code/user_
type、同租户多端、跨租户冲突。"
    },
    {
      "owner": "Claude",
      "task": "补充角色映射白名单和拒绝策略，明确 staff 账号是否必须预绑定，禁止
 role_name/identity_name 直接落库为本地 role。",
      "due": "下一轮讨论前",
      "verification": "列出 role_id/role_name/identity_name 到 UserRole 的映射表
，以及未知、重复、降权、升权场景的返回码。"
    },
    {
      "owner": "Claude",
      "task": "向青橄榄确认签名与 token 细节：timestamp 单位、sign 输入样例、失
败码、token 有效期、是否一次性、生产域名、是否允许服务端回调重试。",
      "due": "开发前",
      "verification": "用官方样例生成 sign 并在测试环境完成 verify-user、user-co
de-by-token、user-info 三条 smoke test。"
    },
    {
      "owner": "Codex/Reviewer",
      "task": "下一轮重点审查新增 golive_auth 的安全边界：不记录 query token、不
缓存第三方 token、错误响应不泄露外部用户信息、本地 JWT 响应与现有登录 DTO 一致。
",
      "due": "方案修订后",
      "verification": "审查视图、service、日志语句、测试用例和 OpenAPI 文档。"
    },
    {
      "owner": "Implementation owner",
      "task": "为对接模块补测试：签名生成固定向量、token 校验失败、外部用户未绑
定、角色未知拒绝、username 冲突、已停用本地用户拒绝、成功签发本地 JWT。",
      "due": "首版实现完成时",
      "verification": "pytest/Django test 覆盖上述场景并通过。"
    }
  ]
}
[RESPONSE_END]
tokens used
57,353

