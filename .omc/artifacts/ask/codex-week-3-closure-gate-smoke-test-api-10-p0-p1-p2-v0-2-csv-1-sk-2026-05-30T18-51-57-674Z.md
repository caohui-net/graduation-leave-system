# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-30T18:51:57.675Z

## Original task

Week 3 closure gate已完成：
- ✓ Smoke test通过
- ✓ API样例收集（10个真实响应）
- ✓ 已知风险文档（P0/P1/P2）
- ✓ v0.2前端契约快照
- ✓ CSV导入验证

下一步：启动小程序窄切片开发

问题：
1. 窄切片应该包含哪些最小功能？（skeleton/API client/login/lists/detail）
2. 优先级顺序？先做什么后做什么？
3. 技术选型建议？（原生小程序 vs uni-app vs Taro）
4. 开发环境配置要点？（dev tools/域名白名单/mock数据）
5. 有哪些前置准备工作？

请批判性分析并给出具体可执行的建议。

## Final prompt

Week 3 closure gate已完成：
- ✓ Smoke test通过
- ✓ API样例收集（10个真实响应）
- ✓ 已知风险文档（P0/P1/P2）
- ✓ v0.2前端契约快照
- ✓ CSV导入验证

下一步：启动小程序窄切片开发

问题：
1. 窄切片应该包含哪些最小功能？（skeleton/API client/login/lists/detail）
2. 优先级顺序？先做什么后做什么？
3. 技术选型建议？（原生小程序 vs uni-app vs Taro）
4. 开发环境配置要点？（dev tools/域名白名单/mock数据）
5. 有哪些前置准备工作？

请批判性分析并给出具体可执行的建议。

## Raw output

```text
结论：小程序窄切片不要只做“能打开页面”的 skeleton。最小闭环应消费真实后端 API，证明 `登录 -> 列表发现 -> 详情查看 -> 关键动作 -> 状态刷新` 能跑通。

**1. 最小功能范围**

建议 Week 4 起步窄切片包含：

1. 小程序工程骨架  
   `app`、路由、基础布局、环境配置、构建脚本、类型约束。

2. API client  
   封装 `baseUrl`、JWT token 注入、401 处理、统一错误格式、loading/重试边界。不要让页面直接写 `wx.request`。

3. 登录页  
   先做账号密码登录：`POST /api/auth/login`。微信 OAuth 暂不进首个窄切片，否则会被小程序主体、备案、openid 绑定拖住。

4. 角色化首页  
   根据 `user.role` 分流：
   - student：我的申请
   - counselor：待我审批
   - dean：待我审批

5. 列表页  
   - student 调 `GET /api/applications/`
   - counselor/dean 调 `GET /api/approvals/`
   - 只做默认分页和空态，不做复杂筛选、搜索、统计。

6. 详情页  
   调 `GET /api/applications/{application_id}/`，展示申请状态、宿舍清退状态、审批记录。

7. 一个核心写动作  
   建议第一版加上审批通过：`POST /api/approvals/{approval_id}/approve/`。  
   驳回、学生提交申请可以放到第二小步，但不能拖太久，因为它们是核心流程。

我会把首个可验收目标定为：辅导员或学工部登录后，能从待审批列表进入详情并完成通过操作，状态刷新正确。

**2. 优先级顺序**

按这个顺序做：

1. 固定 API 契约快照  
   把 Week 3 的 10 个真实响应整理成前端 mock fixtures/type samples。先锁字段，再写 UI。

2. 搭工程 skeleton  
   只保留必要目录：`pages/login`、`pages/applications`、`pages/approvals`、`pages/detail`、`services/api`、`stores/auth`、`types/api`。

3. API client + auth store  
   这是地基。先完成 token 存储、请求头、错误归一化。

4. 登录页  
   用真实后端账号登录，不接微信 OAuth。

5. 待审批列表  
   优先做 `GET /api/approvals/`，因为它能支撑审批人员真实工作流。

6. 申请详情页  
   从审批列表拿 `application_id` 后进入详情。

7. 审批通过动作  
   完成后回到列表并刷新，验证 pending 项消失或状态变化。

8. 学生侧列表/详情  
   再补 student 视角，避免一开始同时做三套页面逻辑。

9. 学生提交、驳回、错误态完善  
   作为第二个窄切片。

**3. 技术选型**

建议：**原生微信小程序 + TypeScript**。

原因很直接：当前首版已经明确微信小程序优先，而且没有现成 React/Vue 前端代码可复用。原生小程序在登录、调试、上传、审核、微信能力接入上阻力最小。

不建议首版用 uni-app，除非已经确定后续必须多端复用。现在引入 uni-app 会多一层框架语义和构建问题，但短期收益不大。

不建议 Taro，除非团队已有 React/Taro 经验并且后续明确要复用到 H5/RN。否则它会把小程序窄切片变成前端框架工程。

**4. 开发环境配置要点**

开发工具：
- 微信开发者工具稳定版
- 启用 TypeScript
- 本地调试勾选“不校验合法域名”
- 后端本地服务保持固定地址，例如 `http://localhost:8001`

环境配置：
- `dev`：本地后端
- `mock`：使用 fixtures，不依赖后端
- `prod`：正式 HTTPS 域名

域名：
- 真机预览和体验版必须配置合法 HTTPS 域名。
- 本地 `localhost` 只适合开发者工具。
- 如果近期没有正式域名，先准备内网穿透或测试 HTTPS 域名，但不要把它写死在页面里。

mock 数据：
- 直接使用 Week 3 收集的真实响应。
- mock 要覆盖：登录成功、401、403、空列表、待审批列表、详情、审批成功、审批冲突。
- mock 字段必须和真实响应同名，不要为了前端方便另造模型。

**5. 前置准备工作**

启动前先完成这些，不然小程序会反复返工：

1. 冻结 v0.2 前端 API 表  
   至少列清楚：URL、method、请求体、响应体、错误码、分页格式、是否带尾斜杠。

2. 确认登录策略  
   首个切片用账号密码。微信登录/openid 绑定单独排期。

3. 明确测试账号  
   固定至少 4 个：`2020001`、`T001`、`T002`、`D001`，并保证 seed 可重复。

4. 明确列表语义  
   `GET /api/approvals/` 默认只返回 pending，这是小程序审批列表最需要的行为。

5. 建立前端验收脚本或手测清单  
   不需要一开始自动化很重，但必须能复现：
   登录 T001 -> 看待审批 -> 进详情 -> 通过 -> 列表刷新。

6. 记录已知风险  
   微信 OAuth、正式 HTTPS 域名、主体备案、真机网络、接口尾斜杠、分页字段、权限 403 展示，都要作为前端风险项管理。

我的建议是：第一天不要做漂亮 UI，先做“真实 API 可跑通的小程序壳”。只要 `登录 + 审批列表 + 详情 + 通过` 走通，小程序开发就从不确定性阶段进入可迭代阶段。


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e7a38-cbfc-7123-af74-7e13e1bb1c93
--------
user
Week 3 closure gate已完成：
- ✓ Smoke test通过
- ✓ API样例收集（10个真实响应）
- ✓ 已知风险文档（P0/P1/P2）
- ✓ v0.2前端契约快照
- ✓ CSV导入验证

下一步：启动小程序窄切片开发

问题：
1. 窄切片应该包含哪些最小功能？（skeleton/API client/login/lists/detail）
2. 优先级顺序？先做什么后做什么？
3. 技术选型建议？（原生小程序 vs uni-app vs Taro）
4. 开发环境配置要点？（dev tools/域名白名单/mock数据）
5. 有哪些前置准备工作？

请批判性分析并给出具体可执行的建议。
codex
我会先看项目本地规则和已有契约/风险文档，避免给出脱离当前仓库状态的建议。
exec
/bin/bash -lc "pwd && sed -n '1,220p' /home/caohui/.codex/RTK.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
/home/caohui/projects/graduation-leave-system
# RTK - Rust Token Killer (Codex CLI)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Always prefix shell commands with `rtk`.

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

## Meta Commands

```bash
rtk gain            # Token savings analytics
rtk gain --history  # Recent command savings history
rtk proxy <cmd>     # Run raw command without filtering
```

## Verification

```bash
rtk --version
rtk gain
which rtk
```

exec
/bin/bash -lc 'rg --files' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
task_plan.md
progress.md
CLAUDE.md
AGENTS.md
docs/week3-day0-seed-data-requirements.md
docs/week3-day0-acceptance-checklist.md
docs/templates/宿舍清退数据模板.csv
docs/templates/学生基本信息导入模板.csv
docs/templates/班级辅导员对应关系导入模板.csv
docs/templates/辅导员基本信息导入模板.csv
docs/微信小程序申请说明.md
毕业离校系统用户文档.zip
docker-compose.yml
findings.md
docs/superpowers/plans/2026-05-27-implementation-plan.md
docs/数据对接说明文档.md
docs/微信小程序备案说明.md
docs/Codex审查流程指南.md
docs/plans/week-0-1-execution-plan.md
docs/codex-review-protocol.md
docs/week3-day0-environment-strategy.md
docs/用户设计说明书.md
docs/PROJECT-SUMMARY.md
docs/contracts/contract-v0.1.md
docs/design/2026-05-27-system-design.md
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md
docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md
docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md
docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md
backend/manage.py
backend/Dockerfile
backend/data/templates/counselors_template.csv
backend/data/templates/class_mappings_template.csv
backend/data/templates/students_template.csv
backend/requirements/base.txt
backend/requirements/dev.txt
backend/requirements/prod.txt
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md
backend/config/__init__.py
backend/config/urls.py
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md
docs/discussions/week3-day1-review-2026-05-30/19-claude-deadlock-analysis.md
docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md
docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md
docs/discussions/week3-day1-review-2026-05-30/09-codex-execution-review.md
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md
docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md
backend/config/wsgi.py
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md
tests/smoke_test.sh
docs/数据确认清单.md
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md
docs/discussions/week3-direction-2026-05-30/06-consensus.md
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md
docs/discussions/week3-direction-2026-05-30/03-claude-response.md
docs/discussions/week3-direction-2026-05-30/02-codex-review.md
docs/discussions/codex-review-2026-05-27/21-final-consensus.md
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md
docs/discussions/codex-review-2026-05-27/01-architecture-review.md
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md
docs/discussions/codex-review-2026-05-27/04-database-review.md
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md
docs/discussions/codex-review-2026-05-27/02-architecture-response.md
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md
backend/config/settings/__init__.py
backend/config/settings/base.py
backend/config/settings/prod.py
backend/config/settings/dev.py
backend/apps/approvals/__init__.py
backend/apps/approvals/admin.py
backend/apps/approvals/pagination.py
backend/apps/approvals/urls.py
backend/apps/approvals/migrations/__init__.py
backend/apps/approvals/migrations/0002_initial.py
backend/apps/approvals/migrations/0001_initial.py
backend/apps/approvals/tests/__init__.py
backend/apps/approvals/tests/test_rejection_flow.py
backend/apps/approvals/tests/test_list_permissions.py
backend/apps/approvals/tests/test_permissions.py
backend/apps/approvals/tests/test_state_machine.py
backend/apps/approvals/views.py
backend/apps/approvals/serializers.py
backend/apps/approvals/models.py
backend/apps/applications/__init__.py
backend/apps/applications/admin.py
backend/apps/applications/providers.py
backend/apps/applications/pagination.py
backend/apps/applications/urls.py
backend/apps/applications/migrations/0003_application_unique_student_application.py
backend/apps/applications/migrations/__init__.py
backend/apps/applications/migrations/0002_initial.py
backend/apps/applications/migrations/0001_initial.py
backend/apps/applications/tests/__init__.py
backend/apps/applications/tests/test_error_cases.py
backend/apps/applications/tests/test_list_permissions.py
backend/apps/applications/tests/test_constraints.py
backend/apps/applications/tests/test_application_flow.py
backend/apps/applications/views.py
backend/apps/applications/serializers.py
backend/apps/applications/models.py
backend/apps/users/__init__.py
backend/apps/users/admin.py
backend/apps/users/urls.py
backend/apps/users/migrations/__init__.py
backend/apps/users/migrations/0001_initial.py
backend/apps/users/apps.py
backend/apps/users/class_mapping.py
backend/apps/users/views.py
backend/apps/users/serializers.py
backend/apps/users/models.py
backend/apps/users/management/__init__.py
backend/apps/users/management/commands/import_csv.py
backend/apps/users/management/commands/__init__.py
backend/apps/users/management/commands/seed_data.py

codex
我确认到这个仓库要求所有 shell 命令走 `rtk`。接下来只抓和小程序窄切片直接相关的契约、闭环结论和风险，不展开无关历史讨论。
exec
/bin/bash -lc "rtk rg -n \"v0\\.2|contract|契约|小程序|风险|P0|P1|P2|Smoke|smoke|API样例|真实响应|CSV|导入\" docs backend task_plan.md progress.md findings.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 2ms:
task_plan.md:21:| `.codex-plugin/plugin.json` missing in skill project | Checked whether skill was a full plugin | Treated cross-tool/plugin distribution as premature P2 rather than current capability. |
docs/week3-day0-seed-data-requirements.md:98:**Mock规则（contract-v0.1.md Section 6.2）：**
docs/week3-day0-seed-data-requirements.md:112:## 数据导入方式
docs/week3-day0-seed-data-requirements.md:121:- 一键导入
docs/week3-day0-acceptance-checklist.md:345:- 如果返回200：权限校验缺失，P0阻塞问题
docs/week3-day0-acceptance-checklist.md:411:### 方式1：Smoke Test脚本（推荐）
docs/week3-day0-acceptance-checklist.md:413:**创建：** `tests/smoke_test.sh`
docs/week3-day0-acceptance-checklist.md:419:echo "=== 最小闭环Smoke Test ==="
docs/week3-day0-acceptance-checklist.md:481:chmod +x tests/smoke_test.sh
docs/week3-day0-acceptance-checklist.md:482:./tests/smoke_test.sh
docs/week3-day0-acceptance-checklist.md:513:### P0（阻塞闭环）
docs/week3-day0-acceptance-checklist.md:521:### P1（影响验收）
docs/week3-day0-acceptance-checklist.md:527:### P2（不影响闭环）
docs/week3-day0-acceptance-checklist.md:538:1. **可复现验证脚本**（smoke_test.sh或Postman集合）
docs/week3-day0-acceptance-checklist.md:539:2. **P0问题清单**（如果有）
docs/week3-day0-acceptance-checklist.md:540:3. **P1/P2问题清单**
docs/week3-day0-acceptance-checklist.md:544:- **继续Week 3扩展开发**：最小闭环通过，仅剩P1/P2问题
docs/week3-day0-acceptance-checklist.md:545:- **Day 3修复P0**：闭环接近通过，剩余明确局部P0缺陷
docs/week3-day0-acceptance-checklist.md:546:- **停止并重设计**：发现架构级阻塞（状态机错误、数据模型缺陷、契约冲突）
docs/微信小程序申请说明.md:1:# 微信小程序申请说明
docs/微信小程序申请说明.md:9:## 一、小程序主体选择建议
docs/微信小程序申请说明.md:11:**建议使用学校主体申请小程序**
docs/微信小程序申请说明.md:15:如果使用校友会主体申请小程序，会有以下限制：
docs/微信小程序申请说明.md:20:- **限制：** 只有学校主体的小程序才可以开通人脸核身功能
docs/微信小程序申请说明.md:25:- **收费说明：** 每次用户登录小程序都会调用一次该接口，每次登录都要收费
docs/微信小程序申请说明.md:27:- **学校主体优势：** 学校主体的小程序使用该接口时，微信不收取费用
docs/微信小程序申请说明.md:31:- 同一个主体可以注册多个小程序
docs/微信小程序申请说明.md:32:- 一个学校注册校友会小程序之后，不影响该学校注册其它小程序
docs/微信小程序申请说明.md:36:## 二、小程序注册流程
docs/微信小程序申请说明.md:45:进入小程序注册页面，依次填写：
docs/微信小程序申请说明.md:69:#### c. 填写小程序管理员信息
docs/微信小程序申请说明.md:71:按照页面提示填写小程序管理员的相关信息。
docs/微信小程序申请说明.md:77:1. **邮箱要求：** 注册邮箱不能与其他微信公众号或小程序重复使用
docs/微信小程序申请说明.md:86:- [微信小程序备案说明](./微信小程序备案说明.md)
findings.md:16:- Existing local artifact `.omc/collaboration/artifacts/20260530-1654-codex-github-projects-analysis.md` already reached similar P0 conclusions: role routing, Gemini read-only artifact workflow, independent analysis protocol, journal validation, and defer full Ralph/MCP/global sync.
docs/superpowers/plans/2026-05-27-implementation-plan.md:24:- 前端开发（React Native + 微信小程序）
docs/superpowers/plans/2026-05-27-implementation-plan.md:52:- 微信小程序开发经验
docs/superpowers/plans/2026-05-27-implementation-plan.md:153:│   └── miniprogram/            # 微信小程序
docs/superpowers/plans/2026-05-27-implementation-plan.md:488:**目标：** 实现React Native应用和微信小程序
docs/superpowers/plans/2026-05-27-implementation-plan.md:528:#### 8.2 微信小程序
docs/superpowers/plans/2026-05-27-implementation-plan.md:533:   - 创建小程序项目
docs/superpowers/plans/2026-05-27-implementation-plan.md:558:- ✓ 微信小程序运行正常
docs/superpowers/plans/2026-05-27-implementation-plan.md:582:   - 编写小程序测试用例
docs/superpowers/plans/2026-05-27-implementation-plan.md:610:## 风险和缓解措施
docs/superpowers/plans/2026-05-27-implementation-plan.md:612:**风险1：外部系统API不稳定**
docs/superpowers/plans/2026-05-27-implementation-plan.md:616:**风险2：微信公众平台审核延迟**
docs/superpowers/plans/2026-05-27-implementation-plan.md:620:**风险3：数据库性能问题**
docs/superpowers/plans/2026-05-27-implementation-plan.md:624:**风险4：前端开发延期**
docs/superpowers/plans/2026-05-27-implementation-plan.md:628:**风险5：测试覆盖不足**
docs/superpowers/plans/2026-05-27-implementation-plan.md:638:- ✓ 完整的前端代码（React Native + 小程序）
docs/数据对接说明文档.md:26:| 学生基本信息 | **CSV/Excel文件导入** | 首版推荐，快速上线 |
docs/数据对接说明文档.md:27:| 辅导员基本信息 | **CSV/Excel文件导入** | 首版推荐，快速上线 |
docs/数据对接说明文档.md:28:| 班级-辅导员对应关系 | **CSV/Excel文件导入** | 首版推荐，需强校验 |
docs/数据对接说明文档.md:31:**为什么推荐CSV/Excel导入？**
docs/数据对接说明文档.md:33:- 风险可控：可以先验证、再导入、可回滚
docs/数据对接说明文档.md:41:| 数据确认 | 第1周 | 确认数据可用性、字段定义、CSV模板 |
docs/数据对接说明文档.md:42:| CSV导入开发 | 第2-3周 | 开发CSV导入功能、校验逻辑、审计日志 |
docs/数据对接说明文档.md:44:| 上线验收 | 第5周 | 全量导入演练、功能测试、正式上线 |
docs/数据对接说明文档.md:48:## 二、学生基本信息（CSV导入）
docs/数据对接说明文档.md:82:- 只需导入当届毕业生（约1000人），不需要全部学生
docs/数据对接说明文档.md:84:### 2.3 CSV模板
docs/数据对接说明文档.md:86:**文件名：** `学生基本信息导入模板.csv`
docs/数据对接说明文档.md:101:- 不要使用Excel的"另存为CSV"，建议使用专业工具导出UTF-8编码
docs/数据对接说明文档.md:103:### 2.4 导入流程
docs/数据对接说明文档.md:105:**步骤1：准备CSV文件**
docs/数据对接说明文档.md:110:**步骤2：上传CSV文件**
docs/数据对接说明文档.md:112:- 进入"数据导入"模块
docs/数据对接说明文档.md:113:- 选择"学生基本信息导入"
docs/数据对接说明文档.md:114:- 上传CSV文件
docs/数据对接说明文档.md:119:- 班级ID存在性校验（需要先导入班级映射）
docs/数据对接说明文档.md:125:- 如有错误，修改CSV后重新上传
docs/数据对接说明文档.md:127:**步骤5：确认导入**
docs/数据对接说明文档.md:128:- 校验通过后，点击"确认导入"
docs/数据对接说明文档.md:129:- 系统执行导入操作
docs/数据对接说明文档.md:130:- 导入完成后，生成导入日志
docs/数据对接说明文档.md:132:### 2.5 导入策略
docs/数据对接说明文档.md:134:**首次导入：**
docs/数据对接说明文档.md:138:**后续导入：**
docs/数据对接说明文档.md:141:- 本次未导入的学号：自动标记为"停用"状态
docs/数据对接说明文档.md:147:- 下次导入重新出现时，自动激活
docs/数据对接说明文档.md:151:## 三、辅导员基本信息（CSV导入）
docs/数据对接说明文档.md:174:### 3.3 CSV模板
docs/数据对接说明文档.md:176:**文件名：** `辅导员基本信息导入模板.csv`
docs/数据对接说明文档.md:185:### 3.4 导入流程
docs/数据对接说明文档.md:187:与学生导入流程相同，参考第二章2.4节。
docs/数据对接说明文档.md:191:## 四、班级-辅导员对应关系（CSV导入）
docs/数据对接说明文档.md:210:### 4.3 CSV模板
docs/数据对接说明文档.md:212:**文件名：** `班级辅导员对应关系导入模板.csv`
docs/数据对接说明文档.md:221:### 4.4 导入顺序
docs/数据对接说明文档.md:223:**重要：必须按以下顺序导入**
docs/数据对接说明文档.md:224:1. 先导入辅导员基本信息
docs/数据对接说明文档.md:225:2. 再导入班级-辅导员对应关系
docs/数据对接说明文档.md:226:3. 最后导入学生基本信息
docs/数据对接说明文档.md:230:- 学生导入需要验证班级ID是否有对应的辅导员
docs/数据对接说明文档.md:239:**导入后输出校验报告：**
docs/数据对接说明文档.md:361:### 6.1 CSV文件要求
docs/数据对接说明文档.md:365:- 格式：CSV或Excel（.xlsx）
docs/数据对接说明文档.md:376:### 6.2 导入审计
docs/数据对接说明文档.md:378:系统会记录每次导入操作：
docs/数据对接说明文档.md:379:- 导入类型（学生/辅导员/班级映射）
docs/数据对接说明文档.md:382:- 导入结果（成功数、失败数、新增数、更新数、停用数）
docs/数据对接说明文档.md:395:- 导入日志保留3个月
docs/数据对接说明文档.md:401:### 7.1 CSV导入相关
docs/数据对接说明文档.md:403:**Q1：CSV文件中文乱码怎么办？**
docs/数据对接说明文档.md:405:A：确保文件编码为UTF-8。如果使用Excel编辑，保存时选择"CSV UTF-8（逗号分隔）"格式。
docs/数据对接说明文档.md:407:**Q2：导入时提示"学号重复"怎么办？**
docs/数据对接说明文档.md:409:A：检查CSV文件中是否有重复的学号。系统要求学号必须唯一。
docs/数据对接说明文档.md:411:**Q3：导入时提示"班级ID不存在"怎么办？**
docs/数据对接说明文档.md:413:A：需要先导入班级-辅导员对应关系，再导入学生信息。
docs/数据对接说明文档.md:417:A：在下次导入时，不包含需要停用的账号即可。系统会自动将本次未导入的账号标记为停用。
docs/数据对接说明文档.md:441:A：可以通过系统管理后台手动修改，或者重新导入包含该学生的CSV文件。
docs/数据对接说明文档.md:445:A：更新班级-辅导员对应关系，重新导入CSV文件。已提交的申请不受影响，新提交的申请使用新辅导员。
docs/微信小程序备案说明.md:1:# 微信小程序备案说明
docs/微信小程序备案说明.md:25:   - 未做过其他小程序或公众号备案的手机号
docs/微信小程序备案说明.md:31:   - 未做过其他小程序或公众号备案的手机号
docs/微信小程序备案说明.md:34:   - 未做过其他小程序或公众号备案的邮箱
docs/微信小程序备案说明.md:48:   - 模板下载：小程序备案-主体负责人授权书.doc
docs/微信小程序备案说明.md:51:   - 未做过其他小程序或公众号备案的手机号
docs/微信小程序备案说明.md:56:   - 未做过其他小程序或公众号备案的手机号
docs/微信小程序备案说明.md:58:   - 未做过其他小程序或公众号备案的邮箱
docs/微信小程序备案说明.md:62:### 1.3 小程序负责人资料
docs/微信小程序备案说明.md:66:1. **小程序负责人（小程序管理员）身份证正反面照片**（照片要求请见下文）
docs/微信小程序备案说明.md:67:2. **《小程序负责人授权书》**
docs/微信小程序备案说明.md:72:   - 模板下载：小程序备案-小程序负责人授权书.doc
docs/微信小程序备案说明.md:74:   - 未做过其他小程序或公众号备案的手机号
docs/微信小程序备案说明.md:79:   - 未做过其他小程序或公众号备案的手机号
docs/微信小程序备案说明.md:81:   - 未做过其他小程序或公众号备案的邮箱
docs/微信小程序备案说明.md:83:**重要提示：** 地区不同，小程序负责人要求不同（详见原文档图表）
docs/微信小程序备案说明.md:87:## 二、小程序备案整体流程
docs/微信小程序备案说明.md:101:### 3.1 登录微信小程序后台
docs/微信小程序备案说明.md:103:1. 申请小程序之后，访问微信公众平台
docs/微信小程序备案说明.md:106:4. 用微信小程序管理员的微信扫码登录小程序
docs/微信小程序备案说明.md:122:1. **手机号要求：** 所有手机号必须未做过其他小程序或公众号备案
docs/微信小程序备案说明.md:123:2. **邮箱要求：** 邮箱必须未做过其他小程序或公众号备案
docs/微信小程序备案说明.md:126:5. **地区差异：** 不同地区对主体负责人和小程序负责人的要求不同，请提前确认
docs/微信小程序备案说明.md:132:- [微信小程序申请说明](./微信小程序申请说明.md)
docs/Codex审查流程指南.md:156:1. P0/CRITICAL问题 - 必须立即修复
docs/Codex审查流程指南.md:157:2. P1/MAJOR问题 - 应该修复
docs/Codex审查流程指南.md:158:3. P2/MINOR问题 - 可选修复
docs/plans/week-0-1-execution-plan.md:10:## Week 0：契约冻结（1-2工作日）
docs/plans/week-0-1-execution-plan.md:13:冻结v0.1最小可执行契约，为Week 1纵向切片提供稳定基础。
docs/plans/week-0-1-execution-plan.md:24:**交付物：** contract-v0.1.md初稿
docs/plans/week-0-1-execution-plan.md:42:**交付物：** contract-v0.1.md冻结版
docs/plans/week-0-1-execution-plan.md:63:- [ ] Seed命令实现（加载contract-v0.1.md中的样例数据）
docs/plans/week-0-1-execution-plan.md:124:- [ ] 契约测试（API响应格式符合contract-v0.1.md）
docs/plans/week-0-1-execution-plan.md:136:- [ ] 无P0/P1阻断bug
docs/plans/week-0-1-execution-plan.md:140:- 如Day 5结束仍有P0 bug → 推到Week 2 Day 1修复，或砍掉触发bug的边界场景
docs/plans/week-0-1-execution-plan.md:149:- [ ] 技术栈选型确认（微信小程序框架）
docs/plans/week-0-1-execution-plan.md:151:- [ ] Mock Server配置（基于contract-v0.1.md）
docs/plans/week-0-1-execution-plan.md:159:- 微信小程序项目可运行
docs/plans/week-0-1-execution-plan.md:168:## 风险和降级
docs/plans/week-0-1-execution-plan.md:170:### 风险1：Week 0契约定义延期
docs/plans/week-0-1-execution-plan.md:176:### 风险2：Week 1 Day 3申请提交API未完成
docs/plans/week-0-1-execution-plan.md:182:### 风险3：Week 1 Day 4学工部审批未完成
docs/plans/week-0-1-execution-plan.md:188:### 风险4：Week 1 Day 5测试未通过
docs/plans/week-0-1-execution-plan.md:200:- [ ] contract-v0.1.md冻结
docs/plans/week-0-1-execution-plan.md:211:- [ ] 无P0/P1阻断bug
docs/plans/week-0-1-execution-plan.md:217:**目标：** CSV导入v1
docs/plans/week-0-1-execution-plan.md:224:- 导入审计基础
docs/codex-review-protocol.md:156:1. P0/CRITICAL问题 - 必须立即修复
docs/codex-review-protocol.md:157:2. P1/MAJOR问题 - 应该修复
docs/codex-review-protocol.md:158:3. P2/MINOR问题 - 可选修复
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:117:2. **遗漏风险预警:** 指出手动添加format='json'容易遗漏且无法防止回归
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:128:- 风险：容易遗漏，未来回归
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:135:- 风险：低，根因修复
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:165:4. **Codex审查价值高:** 及时发现了手动方案的遗漏风险
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:16:2. **遗漏风险评估准确:** 20个POST调用，手动修复容易遗漏，未来新增测试会继续踩坑
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:23:### 发现1: 遗漏风险高 ✓ 确认
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:120:## 五、风险评估
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:122:### 新方案风险
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:139:### 原方案风险（对比）
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:178:5. 风险可控且已有缓解措施
docs/PROJECT-SUMMARY.md:6:**项目状态：** Week 0契约已冻结，准备启动Week 1 Day 1  
docs/PROJECT-SUMMARY.md:7:**当前阶段：** contract-v0.1.md已冻结为v0.1 Final（可执行契约标准）  
docs/PROJECT-SUMMARY.md:17:- **平台：** iOS/Android + 微信小程序
docs/PROJECT-SUMMARY.md:18:- **前端：** React Native + 小程序原生
docs/PROJECT-SUMMARY.md:53:- ✓ 识别风险和缓解措施
docs/PROJECT-SUMMARY.md:75:**Round 3 - P0修改（2026-05-27完成）：**
docs/PROJECT-SUMMARY.md:87:- ✓ Codex审查发现3个P2问题并修复
docs/PROJECT-SUMMARY.md:92:- ✓ 修正CSV模板文件扩展名（.xlsx → .csv）
docs/PROJECT-SUMMARY.md:96:- ✓ P0修复：初始密码改为学号+强制修改（安全风险）
docs/PROJECT-SUMMARY.md:97:- ✓ P1修复：HTTPS改为双模式（HTTP内网+HTTPS公网）、删除id_card参数
docs/PROJECT-SUMMARY.md:98:- ✓ P2修复：删除Postman引用、明确认证方式、统一审批时限、修改辅导员权限范围、统一性能指标
docs/PROJECT-SUMMARY.md:104:- ✓ 更新CSV模板（学生、辅导员、班级映射）
docs/PROJECT-SUMMARY.md:111:  - 风险和应对措施
docs/PROJECT-SUMMARY.md:113:  - 包含3个文档+4个CSV模板
docs/PROJECT-SUMMARY.md:142:**微信小程序文档整理：**
docs/PROJECT-SUMMARY.md:143:- ✓ 整理微信小程序申请说明（docs/微信小程序申请说明.md）
docs/PROJECT-SUMMARY.md:147:- ✓ 整理微信小程序备案说明（docs/微信小程序备案说明.md）
docs/PROJECT-SUMMARY.md:148:  - 备案所需材料汇总（法人证书、主体负责人、小程序负责人）
docs/PROJECT-SUMMARY.md:177:- ✓ 达成最终共识：Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配（文档40）
docs/PROJECT-SUMMARY.md:179:  - 用户主数据通过CSV导入到本地数据库（非运行时API查询）
docs/PROJECT-SUMMARY.md:180:  - ImportSource接口用于数据导入（非运行时查询）
docs/PROJECT-SUMMARY.md:184:  - Week 1提前做数据契约和接口设计（避免返工）
docs/PROJECT-SUMMARY.md:187:- ✓ Claude提出方案A：更新实施计划 + Week 1数据契约（文档41）
docs/PROJECT-SUMMARY.md:194:  - Week 0（1-2工作日）：冻结v0.1最小可执行契约
docs/PROJECT-SUMMARY.md:196:  - Week 2：CSV导入v1
docs/PROJECT-SUMMARY.md:197:  - Week 3：核心流程补强 + v0.2契约
docs/PROJECT-SUMMARY.md:198:  - Week 4-6：微信小程序并行开发
docs/PROJECT-SUMMARY.md:202:  - 单端交付（微信小程序优先）
docs/PROJECT-SUMMARY.md:206:  - 从双端到单端（微信小程序优先）
docs/PROJECT-SUMMARY.md:207:  - 从Week 1数据契约到Week 0（1-2工作日timebox）
docs/PROJECT-SUMMARY.md:210:**Week 0 契约冻结工作（进行中）：**
docs/PROJECT-SUMMARY.md:211:- ✓ 创建contract-v0.1.md初稿（核心DTO、状态枚举、错误码、API端点、样例数据、Mock响应）
docs/PROJECT-SUMMARY.md:212:- ✓ 创建week-0-1-execution-plan.md初稿（Week 0契约冻结 + Week 1后端纵向切片）
docs/PROJECT-SUMMARY.md:215:  - 缺少状态机契约表
docs/PROJECT-SUMMARY.md:224:  - API端点数量仍不一致（契约6个，计划说5个/4个）
docs/PROJECT-SUMMARY.md:231:- ✓ Codex第三轮审查：尚未达标，2个P1阻塞问题
docs/PROJECT-SUMMARY.md:232:  - P1-1：错误样例覆盖不完整（Section 3定义8个错误码，Section 6.2只有4个样例）
docs/PROJECT-SUMMARY.md:233:  - P1-2：降级方案逻辑矛盾（风险2说"砍学工部审批"又说"Day 4补学工部审批"）
docs/PROJECT-SUMMARY.md:234:  - P2-1：术语不一致（"5个HTTP路由" vs "4个API端点"）
docs/PROJECT-SUMMARY.md:235:  - P2-2：AuthUserDTO未正式定义
docs/PROJECT-SUMMARY.md:236:- ✓ 修复全部2个P1阻塞问题：
docs/PROJECT-SUMMARY.md:237:  - P1-1修复：补齐4个缺失错误样例（400 VALIDATION_ERROR, 404 NOT_FOUND, 409 CONFLICT, 500 INTERNAL_ERROR）
docs/PROJECT-SUMMARY.md:238:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
docs/PROJECT-SUMMARY.md:239:- ✓ Codex第四轮审查确认：达到可执行契约标准
docs/PROJECT-SUMMARY.md:242:  - 剩余3个P2问题不阻塞Week 1启动
docs/PROJECT-SUMMARY.md:243:- ✓ 冻结contract-v0.1.md为v0.1 Final（可执行契约标准）
docs/PROJECT-SUMMARY.md:245:- ✓ Week 0契约冻结工作完成，准备启动Week 1 Day 1
docs/PROJECT-SUMMARY.md:318:- ✓ CSV导入命令（import_csv）
docs/PROJECT-SUMMARY.md:319:  - 支持导入students CSV（student_id、name、class_id等）
docs/PROJECT-SUMMARY.md:320:  - 支持导入counselors CSV（employee_id、name等）
docs/PROJECT-SUMMARY.md:321:  - 支持导入mappings CSV（class_id、counselor_id）
docs/PROJECT-SUMMARY.md:330:- ⏳ CSV模板文件（待创建）
docs/PROJECT-SUMMARY.md:334:- ✓ 最终方案：Plan D（2天硬timebox + 决策门 + 可选P0修复日）
docs/PROJECT-SUMMARY.md:352:- ✓ Seed数据导入：10学生+2辅导员+1学工部+2班级映射
docs/PROJECT-SUMMARY.md:362:- ✓ P0问题修复：
docs/PROJECT-SUMMARY.md:369:- ✓ Codex审查识别7个P1 + 5个P2问题（文档01）
docs/PROJECT-SUMMARY.md:372:  - P1-1：跨辅导员审批漏洞（任何辅导员都能审批任意approval）
docs/PROJECT-SUMMARY.md:373:  - P1-2：重复审批漏洞（缺少事务保护和状态机验证）
docs/PROJECT-SUMMARY.md:374:  - P1-3：重复提交竞态（缺少数据库约束）
docs/PROJECT-SUMMARY.md:375:  - P1-4：Seed/mock数据错误（2020002班级不匹配，宿舍清退状态错误）
docs/PROJECT-SUMMARY.md:376:  - P1-5：缺少smoke test（无可复现验证脚本）
docs/PROJECT-SUMMARY.md:377:  - P1-6：验收文档与实际不一致（端口、字段名、ID格式）
docs/PROJECT-SUMMARY.md:378:  - P1-7：缺少列表接口（审批人无法发现待审批申请）
docs/PROJECT-SUMMARY.md:385:  - 决策门标准：Codex要求全部P1完成才Go，Claude建议Conditional Go
docs/PROJECT-SUMMARY.md:390:  - 8-12小时是完整P1关闭的真实成本，但分摊到Day 2-3
docs/PROJECT-SUMMARY.md:409:  6. 正向smoke与证据整理（60分钟）：可重复证据链
docs/PROJECT-SUMMARY.md:411:  8. 决策门（10分钟）：Conditional Go / No-Go / Day 3 P0
docs/PROJECT-SUMMARY.md:439:- ✓ Phase 6: Smoke测试与证据收集（完成）
docs/PROJECT-SUMMARY.md:443:  - 证据文档：.omc/artifacts/day2-smoke-test-evidence.md
docs/PROJECT-SUMMARY.md:453:  - Gap 3: smoke test负向测试逻辑错误（测试T002审批自己的approval而非T001的）
docs/PROJECT-SUMMARY.md:458:  - 修复smoke test使用正确的approval ID（$COUNSELOR_APPROVAL_ID而非$TEST_COUNSELOR_APPROVAL）
docs/PROJECT-SUMMARY.md:459:- ✓ Smoke test验证通过
docs/PROJECT-SUMMARY.md:471:- ✓ Smoke测试：3个关键场景验证通过
docs/PROJECT-SUMMARY.md:611:- 微信小程序
docs/PROJECT-SUMMARY.md:636:## 风险和挑战
docs/week3-day0-environment-strategy.md:77:# 4. 导入seed数据
docs/week3-day0-environment-strategy.md:92:- [ ] seed数据导入成功
docs/week3-day0-environment-strategy.md:97:## 风险和缓解
docs/week3-day0-environment-strategy.md:99:### 风险1：Docker镜像构建失败
docs/week3-day0-environment-strategy.md:102:### 风险2：数据库连接失败
docs/week3-day0-environment-strategy.md:105:### 风险3：端口冲突
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:84:### 错误4: URL路由导入问题
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:17:### 1. Day 2 Evidence Drift (P0 Blocker)
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:30:### 2. Mock Data Inconsistency (P0 Blocker)
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:40:### 3. Smoke Script Broken (P0 Blocker)
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:42:**Problem:** smoke_test.sh line 175 tries to create second application with same student `2020001`.
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:50:### 4. Scope Too Broad (P1 Risk)
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:65:### 5. Dean Scope Unclear (P2 Inconsistency)
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:93:- Fix Day 2 drift (login URL, mock, smoke): 30-60 min
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:96:- Smoke test update: 30-60 min
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:120:**Reason:** Current tests and smoke script are already broken.
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:129:3. Fix smoke script duplicate submission issue
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:147:### Phase 4: Smoke Test Update (30-60 min)
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:148:- Update smoke test to discover approvals via `/api/approvals/`
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:174:- Repeatable smoke test
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:27:- ✓ Day 1问题识别（7个P1 + 5个P2）
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:46:风险：
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:54:- 降低执行风险
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:58:风险：
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:68:- 降低Phase 1风险
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:70:风险：
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:163:2. **Assigned approver权限**（最高优先级，P1-1核心漏洞）
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:243:## 风险和应对
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:245:### 风险1：讨论疲劳导致执行延迟
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:256:### 风险2：执行者不明确导致责任模糊
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:267:### 风险3：环境状态不符合预期
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:60:### 3. Smoke Script Broken: ✓ ACCEPT
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:62:**Codex claim:** smoke_test.sh tries to create duplicate application, violating unique constraint.
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:64:**My response:** This is a valid point. The smoke script was created before the unique constraint, so it needs updating.
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:66:**Action:** Fix smoke script to handle unique constraint properly.
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:101:3. Fix smoke_test.sh duplicate submission issue
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:104:**Acceptance:** All 12 tests passing + smoke script runs without errors
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:158:### Phase 3: Smoke Test Update (PRIORITY 4)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:170:**Acceptance:** Smoke test passes using list endpoints for discovery
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:194:- Phase 3 (smoke update): 30-60 min
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:249:5. **Smoke test verification** - Verify T002 cannot see T001's data
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:267:4. **Then:** Update smoke test (Phase 3)
docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:3:**Context:** Day 2 achieved CONDITIONAL GO (6/7 P1s resolved, ~2h used vs 6h budget)
docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:5:**Remaining P1:** P1-7 列表接口 (deferred from Day 2)
docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:31:7. Add smoke test verification
docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:66:3. **Testing Question:** Are automated tests sufficient, or do we need manual smoke tests for list endpoints?
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:14:计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:25:| Seed/mock修复 | 0.5h | 0.5-1h | `get_or_create(defaults=...)`不会修复已有脏数据，还要同步CSV模板和负向样本 |
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:30:| smoke test | 1h | 1.5-2.5h | 动态token/ID、reset策略、负向场景、错误输出都要处理 |
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:31:| 文档同步 | 0.5h | 0.5-1h | 不止验收清单，seed要求、CSV模板、合同文档可能都漂移 |
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:34:- 如果Day 2是硬4小时，只能定义为“P1止血版”：seed/mock、审批权限、状态机基础保护、重复提交约束、最小smoke骨架。不能宣称全部P1完成。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:43:1. **先恢复测试与数据基线。** 修`2020002`、Mock、CSV模板、测试fixtures，让T001/T002两条链路可构造。否则后续权限和smoke都没有可靠样本。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:47:5. **smoke test。** 可以先写骨架，但最终应在核心接口稳定后完成，且最好使用列表接口发现待审批记录。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:48:6. **文档同步最后做。** 文档应由实际接口和smoke脚本反向校准。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:52:## 4. 每个P1修复的改进方案
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:54:### P1-1 审批权限
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:65:### P1-2 状态机/事务保护
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:79:### P1-3 重复提交竞态
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:89:### P1-4 Seed/mock数据
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:101:### P1-5 Smoke test
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:103:smoke test不能只是happy path curl集合。最低要求：
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:112:### P1-6 验收文档同步
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:118:- CSV模板与实际`seed_data`。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:119:- 验收清单应引用`tests/smoke_test.sh`作为主验证入口，curl命令作为展开说明，而不是两套可能漂移的事实来源。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:122:### P1-7 列表接口
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:142:6. **approve/reject重复逻辑风险。** 两个函数权限、状态机、事务应抽成共享处理路径，避免只修approve漏掉reject。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:149:Day 2不能用“完成4个P1”判定达标。**只要仍有未关闭P1，就不能进入Week 3扩展开发。**
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:159:- smoke test从空/重置后的环境跑通正向闭环。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:160:- smoke test覆盖至少三个负向场景：跨辅导员403、重复审批409、重复提交409。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:174:- smoke test必须手工查数据库或硬编码ID。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:175:- 只完成4个P1。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:179:## 7. 关键风险点
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:181:1. **时间风险最高。** 4小时不足以同时完成代码、migration、测试、smoke和文档。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:182:2. **并发验证风险。** SQLite/普通单元测试可能给出假安全，Postgres集成验证才有意义。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:184:4. **旧数据污染风险。** seed修复若不提供reset/update，Day 1环境可能继续沿用错误数据。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:185:5. **权限面扩大风险。** 只修审批动作、不修列表和详情查看，会留下同等级的数据泄露问题。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:186:6. **smoke destructive reset风险。** 自动flush会破坏开发数据，必须显式开关并限制环境。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:187:7. **文档再次漂移风险。** 如果文档和脚本分别维护，Day 2后仍可能出现“文档通过、脚本失败”。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:193:Day 2计划应改成“先稳定验收基础，再修核心安全/一致性，再补可发现性和smoke”的执行方案。列表接口不应推迟；4小时只能做止血，不能作为P1关闭标准。真正的Day 2验收目标应是：**从重置环境开始，一条命令跑出正向闭环和关键负向断言，且不依赖人工查库或硬编码ID。**
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:20:- `seed_data --reset` 的语义是否包含清理 applications/approvals；否则加了"一人一申请"约束后 smoke test 不能重复跑。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:31:3. Smoke test 不应等所有代码写完才开始，可在第1阶段后先搭骨架，后续填断言。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:47:理由：这些都是安全/一致性回归点，且仓库已经有 `backend/apps/*/tests/` 测试结构，新增针对性 Django 测试比后续靠人工复验可靠。`tests/smoke_test.sh` 可以作为端到端运行脚本，但不能替代模型/API层回归测试。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:60:- Smoke script 正向路径：60-90分钟。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:63:因此，4小时只能争取"核心止血 + 最低证据"；6小时更接近完成 Conditional Go。若坚持4小时，必须把列表接口、完整负向 smoke、ClassMapping防御、并发压力验证推到 Day 3。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:75:- 最低自动化测试和正向 smoke 至少有一个可重复执行证据链。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:80:- smoke test 中的负向场景脚本化，如果 Django 自动化测试已经覆盖负向用例。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:95:## 三、遗漏的风险和准备工作
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:97:1. **测试基线风险。** 仓库已有 Django 测试，但现有测试数据没有明显创建 `ClassMapping`，而提交申请依赖班级映射；需要先确认测试能否通过并修正 fixture。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:98:2. **reset语义风险。** `seed_data` 当前使用 `get_or_create`，不会更新既有用户的 `class_id`；即使改成 `update_or_create`，也不一定清理 applications/approvals。重复 smoke 会被唯一约束挡住。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:99:3. **数据库约束迁移风险。** 给 `Application.student` 加唯一约束前，需要确认测试库/开发库没有重复数据，并处理 migration 失败路径。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:100:4. **事务验证风险。** `select_for_update()` 需要在真实数据库事务中验证；如果只用普通 curl 串行验证，无法证明并发下不会重复创建 dean approval。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:101:5. **端点与文档漂移风险。** 提案里的部分 curl 缺少尾斜杠，但当前 URL 是 `/api/applications/` 和 `/api/approvals/<id>/approve/`。文档还需同步 `app_...`/`apv_...` 这类实际ID格式，而不是简单写"UUID"。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:102:6. **list接口契约风险。** 之前契约修复曾移除 `GET /api/applications` 列表端点；Day 2 共识又把列表接口作为正式 Go 门槛。执行前需要确认这不是契约回退。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:103:7. **dynamic dean语义风险。** "从 User 表查询 dean"需要定义 active 条件、多个 dean 的选择规则、没有 dean 时的错误码。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:111:- **Smoke test 1小时偏乐观。** 登录、动态ID提取、状态码断言、reset/cleanup、错误输出处理通常超过1小时。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:113:- **列表接口 1.5小时偏乐观。** 还涉及契约确认、URL冲突、角色过滤、序列化和测试，实际可能是 2小时以上。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:124:- 阶段5：正向 smoke 可执行，或等价的端到端自动化证据。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:129:- smoke shell 脚本中的完整负向场景，前提是 Django 测试已覆盖负向用例。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:138:1. **Seed/mock修复：** 内容不完整。需要把 `--reset` 明确为 idempotent，并决定是否清理 applications/approvals；否则 smoke test 不能重复跑。Provider 方法名实际是 `check_status`，不是 `get_status`。模板路径不只 `docs/templates/`，还包括 `backend/data/templates/`。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:142:5. **Smoke test骨架：** 建议支持 `BASE_URL` 环境变量，不要只硬编码；脚本必须检查 HTTP status，并在开头执行 reset/cleanup。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:147:## 七、对3个风险的补充评价
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:149:Claude识别的3个风险都成立，但不全面：
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:150:- Seed/mock 风险的核心不是 provider 逻辑复杂，而是 reset/idempotency 和业务表清理。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:151:- 状态机风险不只是语法不熟，而是事务边界、锁顺序、状态匹配和重复 dean 创建需要一起成立。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:152:- Smoke test 风险不只是 jq 调试，而是环境启动、数据复位、HTTP状态码断言和契约漂移。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:154:建议新增风险：测试基线不可用、migration失败、列表接口契约冲突、动态 dean 多记录/缺失、手工验证无法证明并发正确性。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:166:5. **4:45-5:45 正向 smoke + 文档同步：** 记录真实命令和响应。
docs/discussions/week3-day1-review-2026-05-30/19-claude-deadlock-analysis.md:67:- 避免误判授权的风险
docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md:15:- Day 2会修改代码、migration、seed、测试与smoke
docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md:27:**风险最高**：Day 2涉及数据库、迁移、reset、代码修改和时间盒决策。
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:44:### 4. 风险识别偏泛（Medium）
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:46:17号列了环境、seed、测试等通用问题，但没有吸收14号已明确指出的具体风险：
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:55:### 5. "最关键3项"有降级风险（Medium）
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:69:- 识别的是通用执行风险，没有把前几轮已确认的具体缺陷转化为T0检查项、修复优先级和停止条件
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:79:- 选项2的"选择性执行/跳过阶段"有风险（Day 2各阶段强依赖）
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:97:- 只提供"停止/记录为No-Go/转Day 3 P0"的路径
docs/design/2026-05-27-system-design.md:47:- **平台：** iOS/Android + 微信小程序
docs/design/2026-05-27-system-design.md:48:- **前端：** React Native + 小程序原生
docs/design/2026-05-27-system-design.md:64:│ React Native │ React Native │  微信小程序    │
docs/design/2026-05-27-system-design.md:1275:**理由：** 本系统为内部系统，用户由管理员导入，学号枚举风险低。Phase 1采用核心措施，根据实际需求渐进式引入其他措施。
docs/design/2026-05-27-system-design.md:1305:- 小程序：存储在wx.storage
docs/design/2026-05-27-system-design.md:2534:**小程序优化：**
docs/design/2026-05-27-system-design.md:2708:- 微信开发者工具（小程序测试）
docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md:11:**Plan D的timebox仍然有效，但它约束的是Day 2的"止血 + 证据"，不是"把所有P1关完"。**
docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md:21:**是，timebox仍然有效，但只能作为范围约束，不能作为"完成全部P1"的承诺。**
docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md:23:- 8-12小时对应的是"完整关闭P1 + 可重复验收"
docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md:48:**决策门可以调整，但不能降成"部分P1完成也算Go"。**
docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md:63:**作为Day 2全部交付，偏乐观**，尤其是migration、测试基线、smoke、文档同步会吃掉缓冲。
docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md:72:- **坚持8-12小时作为"完整关闭P1"的真实成本**
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:26:- 风险：可能遗漏准备工作，中途卡住
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:29:- 优势：降低执行风险，提高成功率
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:30:- 风险：准备工作可能吃掉timebox时间
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:47:5. Smoke test骨架（1小时）
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:52:- 风险：前面卡住会阻塞后面
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:55:- 优势：提高效率，降低阻塞风险
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:56:- 风险：可能引入集成问题
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:63:3. 任务5（smoke test）依赖任务1-4全部完成
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:69:- 第三阶段：任务5（smoke test）- 验证前面的修复
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:78:- 风险：不可重复，容易遗漏
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:82:- 风险：写测试吃时间
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:86:- 风险：需要判断哪些手工、哪些自动
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:92:2. 任务5（smoke test）本身就是自动化验证脚本
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:93:3. 手工验证命令可以作为smoke test的基础
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:101:- 任务5：执行smoke_test.sh，期望全部通过
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:110:- 风险：打破timebox
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:114:- 风险：后续任务可能依赖
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:118:- 风险：需要判断力
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:125:3. 任务5（smoke test）可以降级为部分验证
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:143:- 2:30-3:30：任务5（smoke test）
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:162:4. 更新CSV模板（docs/templates/）
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:255:### 阶段5：Smoke test骨架（1小时）
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:257:**位置：** `tests/smoke_test.sh`
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:267:chmod +x tests/smoke_test.sh
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:268:./tests/smoke_test.sh
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:287:6. 更新CSV模板路径
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:319:### 阶段8：Smoke test负向场景（30分钟）
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:337:- ✓ 有smoke test骨架（正向路径可验证）
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:348:- ✓ Smoke test覆盖负向场景
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:352:## 风险和应对
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:354:### 风险1：Seed/mock修复遇到阻塞
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:358:- CSV模板格式问题
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:365:### 风险2：状态机保护实现复杂
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:376:### 风险3：Smoke test脚本调试耗时
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:402:- 不写自动化测试（smoke test骨架即可）
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:19:我不坚持“必须跑满6小时”。我坚持的是：**如果目标是可信的Conditional Go，4.5小时方案里的几个压缩项风险过高；如果坚持4.5小时，到点只能作为决策检查点，不能预设一定能Conditional Go。**
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:35:- 6小时后仍未满足不可跳过项：No-Go或进入Day 3 P0收尾，不能继续消耗Day 2。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:47:- smoke脚本调试不被登录字段、token字段、ID格式、尾斜杠问题打断。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:54:> 4.5小时内争取完成核心代码修复和至少一种可重复证据；到点检查是否值得继续使用剩余1.5小时补测试、smoke和文档。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:64:Claude提出“核心安全项完成但测试/smoke未完成：Conditional Go with Day 3 plan”，我不同意。没有最小自动化测试或等价端到端证据时，只能说“核心修复候选已完成”，不能说Conditional Go。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:72:   - 剩余工作主要是测试、smoke、文档证据。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:78:   - 最低自动化测试或正向smoke至少一个可重复证据链通过；
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:80:   - 未完成项只剩列表接口、完整负向smoke、ClassMapping、并发压力和清理类任务。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:96:- **历史遗留但可绕过的问题**：部分旧测试失败、非本轮路径的fixture缺失、列表接口契约冲突。这些记录为Day 0/Day 1遗留，但只要不影响核心证据，可以推Day 3。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:105:原因很直接：Day 2修的是权限、状态机、唯一约束，这些是最容易被后续开发再次破坏的契约。如果没有自动化测试，Week 3继续开发时没有回归刹车。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:109:- 如果Django测试基线可用：必须写最小自动化测试，smoke可只做正向骨架。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:111:- 如果Django测试基线在30-45分钟内无法恢复：允许用手工验证加命令记录支撑Day 2阶段性结论，但决策只能是“Day 3 P0补测试后再Conditional Go”，不能直接进入Week 3扩展。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:123:- 3:15-4:00 正向smoke
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:129:### 不现实或高风险的压缩
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:151:**正向smoke 45分钟偏紧。**
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:153:登录、token解析、application_id/approval_id提取、HTTP状态码判断、reset/cleanup、错误输出，任何一个字段与文档不一致都会吃时间。45分钟能搭骨架，但不一定能形成可信证据。可接受的压缩方式是：如果Django测试已经覆盖正向路径，smoke只保留最薄的端到端脚本。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:172:这不是完美主义，而是避免假阳性。一个没有可重复证据的Conditional Go，会把风险转移到Week 3，并让Day 3变成隐性返工。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:218:若不满足：停止，No-Go或Day 3 P0修复，不进入Week 3。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:220:### 4:30-5:30 正向smoke与证据整理
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:222:- smoke脚本或等价命令序列必须跑通至少一条正向链路。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:231:- 满足不可跳过项：Conditional Go，Day 3只做列表接口、完整负向smoke、ClassMapping/并发/清理。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:232:- 不满足不可跳过项：No-Go或Day 3 P0，禁止进入Week 3扩展。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:243:4. **Day 3只允许收尾明确项目。** 如果Day 2剩余的是核心权限、状态机、重复提交这些未闭合问题，Day 3是P0修复日，不是进入Week 3前的普通补充。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:254:Claude说“测试/smoke未完成但核心安全项完成，可Conditional Go with Day 3 plan”，我的回答是：**这应改名为Day 3 P0 Follow-up，不应叫Conditional Go。Conditional Go至少需要一个可重复证据链。**
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:56:- Smoke test可以在阶段1后先搭骨架
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:72:Codex正确指出手工curl不足以支撑安全/一致性修复。我的"手工验证为主"低估了回归风险。
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:98:- 状态机、唯一约束、smoke test、文档验证都需要更多时间
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:111:- 正向smoke + 文档：45分钟
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:126:- 最低自动化测试或正向smoke至少有一个可重复证据
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:131:- Smoke test负向场景脚本化（如果Django测试已覆盖）
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:144:  - 核心安全项完成但测试/smoke未完成：Conditional Go with Day 3 plan
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:149:## 对Codex遗漏风险的回应
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:151:**完全接受Codex识别的7个遗漏风险。**
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:153:1. **测试基线风险** - 接受，前置校验必须检查
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:154:2. **reset语义风险** - 接受，必须明确是否清理业务表
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:155:3. **数据库约束迁移风险** - 接受，必须处理历史数据
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:156:4. **事务验证风险** - 接受，但Day 2只做基础验证，并发压力测试推Day 3
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:157:5. **端点与文档漂移风险** - 接受，文档必须同步实际ID格式
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:158:6. **list接口契约风险** - 接受，必须确认不是契约回退
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:159:7. **dynamic dean语义风险** - 接受，必须定义多记录/缺失规则
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:161:这些风险都是我遗漏的，Codex的识别非常准确。
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:172:3. **Smoke test 1小时 → 超过1小时** - 部分接受，骨架版本可以1小时，完整版本需要更多
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:179:- Smoke test：先做骨架（1小时），完整版本Day 3
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:205:5. **Smoke test骨架** - 接受，支持BASE_URL环境变量，检查HTTP status
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:221:- 4:45-5:45 正向smoke + 文档同步
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:233:- 3:15-4:00 正向smoke（45分钟，骨架版本）
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:238:- 核心安全项完成：Conditional Go，Day 3补测试/smoke/文档
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:278:   - 哪些压缩（前置20分钟、测试45分钟、smoke 45分钟）是不现实的？
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:304:5. 所有7个遗漏风险
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:313:4. **Smoke test超过1小时** - 骨架版本可以1小时
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:318:- 4.5小时：前置校验 + 核心修复 + 最小测试 + 骨架smoke + 关键文档
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:16:- 方向正确，识别了所有关键P1问题
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:30:- **Day 2（4小时）：** 核心P1止血 + 暴露剩余问题
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:32:- **不是：** Day 2必须完成所有P1
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:45:- +2小时：如果进展顺利，补列表接口或smoke骨架
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:46:- 决策门：评估剩余P1是否需要Day 3
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:64:   - 合并修复会增加单次修改的复杂度和风险
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:75:5. Smoke test骨架（1小时）- 只覆盖正向路径
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:80:8. Smoke test负向场景（30分钟）
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:84:## 对P1修复方案的批判性回应
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:86:### P1-1 审批权限
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:121:### P1-2 状态机/事务保护
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:152:### P1-3 重复提交竞态
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:174:### P1-4 Seed/mock数据
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:182:- 更新CSV模板
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:188:### P1-5 Smoke test
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:192:Codex建议的完整smoke test包括：
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:202:完整smoke test需要2.5小时，Day 2做不完。
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:215:### P1-6 验收文档同步
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:225:- CSV模板
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:229:### P1-7 列表接口
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:274:- smoke test跑通正向闭环
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:275:- smoke test覆盖三个负向场景
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:281:这个标准要求**Day 2完成所有P1 + 完整验证**，这不是timebox，这是瀑布式开发。
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:285:- **Conditional Go：** 部分P1未完成，但有Day 3计划，不阻塞Week 3准备
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:295:- ✓ 有smoke test骨架（正向路径可验证）
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:322:- 修复：更新CSV模板
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:350:**5. Smoke test骨架（1小时）**
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:351:- 位置：`tests/smoke_test.sh`
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:361:- 修复：CSV模板
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:375:**8. Smoke test负向场景（30分钟）**
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:388:**Codex：** 8-12小时完整关闭P1  
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:395:**Codex：** ClassMapping校验、并发测试、完整smoke test  
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:402:**Codex：** 全部P1完成 + 完整验证才能Go  
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:424:   - Codex的Go标准要求"全部P1完成 + 完整验证"
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:426:   - Plan D的决策门是否应该允许"部分P1完成 + 有Day 3计划"的Conditional Go？
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:448:4. **完整smoke test** - Day 2做不完
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:454:- 4小时：核心P1止血（6项任务）
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:458:**不应该是8-12小时的完整P1关闭。**
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:38:## 对P1问题的完全接受
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:40:Codex识别的7个P1问题全部准确，且都是阻塞性问题：
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:42:### 最严重的3个P1
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:51:- 重复审批、并发审批都有风险
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:54:**3. 重复提交有竞态风险**
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:59:### 其他4个P1
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:62:**5. 可复现验证缺失**：没有smoke_test.sh  
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:70:## 对P2问题的认同
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:72:5个P2问题都准确，但优先级低于P1：
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:84:## 对P0根因判断的认同
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:86:Codex对4个P0问题的根因分析准确：
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:113:#### P1修复（必须完成）
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:136:**5. 创建smoke test脚本**
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:137:- 位置：`tests/smoke_test.sh`
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:146:#### P1修复（可选）
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:153:#### P2修复（可选）
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:173:Day 1暴露的4个P0问题都是Week 1-2质量问题的体现。
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:179:**P1修复（6个必须项）：**
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:184:5. 创建smoke test脚本：1小时
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:189:**P2修复（可选）：**
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:190:- 如果时间允许，可以修复部分P2问题
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:201:- P1问题：7个（全部阻塞）
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:202:- P2问题：5个（不阻塞）
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:206:- ✓ 必须Day 2修复P1问题
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:207:- ⚠ 如果Day 2修复后仍有P1问题，需要Day 3或调整Week 3计划
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:234:Day 2必须修复7个P1问题，把"手工跑通"固化为"可重复验收"。
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:47:- 剩余工作主要是测试、smoke、文档证据
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:51:- 最低自动化测试或正向smoke至少一个可重复证据链通过
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:53:- 未完成项只剩列表接口、完整负向smoke、ClassMapping、并发压力和清理类任务
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:77:- 测试基线30-45分钟内无法恢复：允许用手工验证加命令记录，但决策只能是"Day 3 P0补测试后再Conditional Go"
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:142:**若不满足：** 停止，No-Go或Day 3 P0修复，不进入Week 3
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:144:### 4:30-5:30 正向smoke与证据整理（60分钟）
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:147:- smoke脚本或等价命令序列必须跑通至少一条正向链路
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:152:chmod +x tests/smoke_test.sh
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:153:./tests/smoke_test.sh
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:179:- Conditional Go：Day 3只做列表接口、完整负向smoke、ClassMapping/并发/清理
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:180:- No-Go或Day 3 P0：禁止进入Week 3扩展
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:192:6. 正向smoke可执行，或等价的端到端自动化证据
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:197:2. Smoke shell脚本中的完整负向场景（前提是Django测试已覆盖负向用例）
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:204:## 风险和应对（最终版本）
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:206:### 风险1：前置校验发现环境问题
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:212:### 风险2：核心修复超时
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:219:### 风险3：测试基线不可用
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:224:- 降级后决策只能是"Day 3 P0补测试"
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:226:### 风险4：Smoke test调试耗时
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:229:- 如果Django测试已覆盖正向路径，smoke只保留最薄的端到端脚本
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:240:- ✓ 最低自动化测试或正向smoke至少一个可重复证据链通过
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:249:### Day 3 P0 Follow-up
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:252:- 核心安全项完成但测试/smoke未完成
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:258:- Day 3必须补全smoke或等价证据
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:278:5. **Day 3只允许收尾明确项目。** 如果Day 2剩余的是核心权限、状态机、重复提交这些未闭合问题，Day 3是P0修复日，不是进入Week 3前的普通补充。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:32:- 当前风险点集中在代码一致性和验证证据，执行者需要能在同一上下文里快速调整。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:36:- Claude可以修改后端代码、测试、migration、seed、smoke脚本和关键文档。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:49:3. **数据重置边界：** `seed_data --reset` 可以清理哪些表，尤其是 `applications` 和 `approvals`。这是重复提交约束和可重复 smoke 的前提。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:58:4. **smoke形式。** shell脚本、curl命令记录或最薄端到端脚本均可，但必须留下可重复证据。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:63:## 4. 遗漏准备工作和风险
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:68:   `git status --short` 显示 `.omc` 状态文件、讨论文档和若干未跟踪文件。启动前不必清理，但必须记录基线，并约定 Day 2 只修改后端实现、测试、migration、smoke和必要文档。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:77:   `Application.student` 仍是普通 `ForeignKey`，模型 `Meta` 只有 `db_table`。Day 2必须补数据库约束和 migration，并处理既有重复数据/重跑 smoke 的冲突。
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:19:**共识：有效，但约束的是Day 2的"止血+证据"，不是"完整关闭P1"。**
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:22:- 8-12小时对应"完整关闭P1 + 可重复验收"
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:64:- 修复：更新CSV模板
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:92:**5. Smoke test骨架（1小时）**
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:93:- 位置：`tests/smoke_test.sh`
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:103:- 修复：CSV模板
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:117:**8. Smoke test负向场景（30分钟）**
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:129:2. **负向验证（30分钟）** - smoke test负向场景
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:145:- ✓ 有smoke test骨架（正向路径可验证）
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:158:- ✓ Smoke test覆盖负向场景
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:172:- 8-12小时是"完整关闭P1 + 可重复验收"的真实成本
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:183:- 8-12小时是完整P1关闭的真实成本，但分摊到Day 2-3
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:190:- ClassMapping校验、并发测试、完整smoke test是工程完整性要求
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:198:- 完整smoke test分两阶段：Day 2骨架，Day 3负向场景
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:213:- 接受8-12小时是完整P1关闭的真实成本
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:12:Day 1完成后，Codex给出6/10评分，识别出7个P1问题和5个P2问题。
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:27:### P1修复（必须完成，6个）
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:50:**5. 创建smoke test脚本 - 1小时**
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:51:- 位置：`tests/smoke_test.sh`
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:62:### P1修复（可选）
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:69:### P2修复（可选）
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:81:**问题：** 4小时完成6个P1修复是否现实？
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:85:- smoke_test.sh需要从零编写，1小时够吗？
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:91:**问题：** 6个P1修复的顺序是否合理？
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:98:5. Smoke test脚本（可复现验证）
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:103:- Smoke test脚本是否应该在所有修复完成后再写？
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:127:**问题5：Smoke test脚本**
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:138:**Codex识别的7个P1问题：**
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:141:3. ✓ 重复提交有竞态风险
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:158:- ✓ 必须Day 2修复P1问题
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:159:- ⚠ 如果Day 2修复后仍有P1问题，需要Day 3或调整Week 3计划
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:162:- "修复P1问题"的验收标准是什么？
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:164:- 如果Day 2只完成4个P1修复，是否算达标？
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:172:3. **优先级调整建议：** 是否需要调整6个P1修复的顺序？
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:173:4. **修复方案改进：** 每个P1修复是否有更好的方案？
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:176:7. **关键风险点：** Day 2执行中可能遇到的风险
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:18:- Seed数据已导入
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:42:## P1问题清单（7个）
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:52:**影响：** 重复或并发审批有风险
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:54:### 3. 重复提交有竞态风险
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:57:**影响：** 重复提交有竞态风险
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:64:**问题：** 仓库里没找到`smoke_test.sh` / Postman / manual verification文档  
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:77:## P2问题清单（5个）
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:87:## P0问题根因判断
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:99:**判断：** 改8001合理，但文档和smoke脚本必须同步
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:117:5. **写真实smoke脚本**：动态读取`access_token`、`application_id`、`approval_id`，不要写死`1/2`
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:122:## 关键风险
docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md:28:"继续讨论"不能推导成"授权修改后端代码、测试、migration、seed、smoke脚本并开始6小时计时"。
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:35:6. 正向smoke与证据整理（4:30-5:30，60分钟）
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:47:**风险：** 如果T0门禁失败，需要快速判断是否No-Go，可能浪费25分钟。
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:54:**风险：** 如果seed/reset不稳定，后续所有验证都不可重复。
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:61:**风险：** 如果任何一项修复遇到意外复杂度，可能导致4.5h检查点时核心代码未落地。
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:68:**风险：** 如果测试基线不可用，只能降级为手工验证，结论等级降低。
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:75:**风险：** 可能在4.5h时错误判断"继续"，导致6h时仍未达标。
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:125:- 列出7个P1问题的根本原因和解决方案
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:153:   - 是否有遗漏的关键风险？
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:162:   - 是否应该提前做某些低风险的准备？
docs/数据确认清单.md:56:- C. CSV/Excel文件导入（最快，首版推荐）
docs/数据确认清单.md:62:**问题11：** CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/数据确认清单.md:64:**背景说明：** 系统采用"staging + upsert + 软停用"策略，本次未导入的账号自动标记为停用。
docs/数据确认清单.md:76:**背景说明：** 系统支持密码登录和微信登录，CSV导入的账号需要首次登录设置密码。
docs/数据确认清单.md:78:**问题14：** 是否需要导入手机号/邮箱用于找回密码或二次验证？
docs/数据确认清单.md:96:首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：
docs/数据确认清单.md:100:| 学生基本信息 | CSV/Excel导入 | 变更频率低（学期级），快速上线 |
docs/数据确认清单.md:101:| 辅导员基本信息 | CSV/Excel导入 | 约50人，变更频率低 |
docs/数据确认清单.md:102:| 班级-辅导员映射 | CSV/Excel导入 | 变更频率低，需强校验 |
docs/数据确认清单.md:129:**阶段2：CSV导入实现（2周）**
docs/数据确认清单.md:131:**目标：** 实现CSV批量导入功能
docs/数据确认清单.md:134:1. 设计三份CSV模板（学生、辅导员、班级映射）
docs/数据确认清单.md:135:2. 实现CSV导入功能（文件上传、解析、校验）
docs/数据确认清单.md:138:5. 实现导入审计日志
docs/数据确认清单.md:139:6. 生成导入校验报告
docs/数据确认清单.md:142:- CSV导入功能模块
docs/数据确认清单.md:143:- 三份CSV模板文件
docs/数据确认清单.md:144:- 导入校验报告示例
docs/数据确认清单.md:145:- 导入操作手册
docs/数据确认清单.md:174:2. 完成一次全量导入演练
docs/数据确认清单.md:180:- 全量导入演练报告
docs/数据确认清单.md:212:| 阶段2 | 第2-3周 | CSV导入功能上线 | 成功导入测试数据，校验报告无异常 |
docs/数据确认清单.md:214:| 阶段4 | 第5周 | 上线前验收通过 | 全量导入成功，异常清单为空，功能测试通过 |
docs/数据确认清单.md:221:## 四、风险和应对
docs/数据确认清单.md:223:| 风险 | 影响 | 应对措施 |
docs/数据确认清单.md:226:| 班级映射数据不完整 | 高 | 导入时强校验，输出未映射班级清单，人工补充 |
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:135:## 五、风险评估
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:181:4. 是否有遗漏的风险?
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:57:- 风险：可能陷入"永远等待"循环
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:62:- 风险：可能被视为"过度讨论"
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:67:- 风险：可能误解用户意图
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:120:2. **Day 2会修改代码，风险高**
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:122:   - 这是高风险操作，需要明确授权
backend/apps/users/management/commands/import_csv.py:8:    help = 'Import users and class mappings from CSV files'
backend/apps/users/management/commands/import_csv.py:11:        parser.add_argument('--students', type=str, help='Path to students CSV file')
backend/apps/users/management/commands/import_csv.py:12:        parser.add_argument('--counselors', type=str, help='Path to counselors CSV file')
backend/apps/users/management/commands/import_csv.py:13:        parser.add_argument('--mappings', type=str, help='Path to class mappings CSV file')
docs/用户设计说明书.md:25:- **微信小程序：** 微信内使用，无需安装
docs/用户设计说明书.md:83:- 学号由学校统一导入
docs/用户设计说明书.md:237:**Q1：如何批量导入学生用户？**
docs/用户设计说明书.md:293:**方式一：Excel文件导入（推荐，最简单）**
docs/用户设计说明书.md:300:3. 系统自动导入数据，生成账号
docs/用户设计说明书.md:301:4. 导入完成后，学生和辅导员就可以登录了
docs/用户设计说明书.md:306:- 数据可以先检查再导入，出错了可以重新导入
docs/用户设计说明书.md:309:- 每学期导入1-2次即可
docs/用户设计说明书.md:381:### 6.4 数据导入顺序（重要）
docs/用户设计说明书.md:383:**必须按以下顺序导入：**
docs/用户设计说明书.md:384:1. 先导入辅导员信息
docs/用户设计说明书.md:385:2. 再导入班级-辅导员对应关系
docs/用户设计说明书.md:386:3. 最后导入学生信息
docs/用户设计说明书.md:390:- 学生导入需要验证班级是否有对应的辅导员
docs/用户设计说明书.md:393:### 6.5 首次导入后的效果
docs/用户设计说明书.md:412:**Q1：数据导入会不会覆盖原有数据？**
docs/用户设计说明书.md:417:- 本次未导入的学号/工号：标记为停用（不删除）
docs/用户设计说明书.md:419:**Q2：导入错误了怎么办？**
docs/用户设计说明书.md:421:A：可以重新导入。系统会先校验数据，发现错误会提示，不会直接导入。
docs/用户设计说明书.md:423:**Q3：如何知道导入是否成功？**
docs/用户设计说明书.md:425:A：系统会生成导入报告，显示：
docs/用户设计说明书.md:426:- 成功导入多少条
docs/用户设计说明书.md:438:A：Excel导入不需要技术人员，管理员就能操作。API接口需要技术人员配合开发。
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:14:Codex正确指出了方案的核心问题：**偏离了已达成的首版共识**。原方案错误地将用户主数据API化，而共识明确规定学生、辅导员、班级映射应采用CSV导入。
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:18:## 对P0问题的响应
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:20:### P0-1：RealUserDataProvider不应成为运行时依赖
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:29:1. 用户主数据通过CSV导入到本地数据库
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:31:3. Provider抽象层保留，但用途改为：**数据导入的输入源**，而非运行时查询
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:36:# Provider用于数据导入（非运行时查询）
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:38:    """用户数据导入源接口"""
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:41:        """获取学生数据用于导入"""
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:46:        """获取辅导员数据用于导入"""
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:49:# CSV实现
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:50:class CSVUserDataImportSource(IUserDataImportSource):
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:52:        # 读取CSV文件
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:60:# 导入服务
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:69:        # 2. 导入到staging表
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:72:        # 5. 软停用未导入的账号
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:89:### P0-2：+3天生产就绪评估过于乐观
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:102:| 宿舍清退API集成 | 1-2周 | API契约明确、字段覆盖、认证跑通 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:111:## 对P1问题的响应
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:113:### P1-1：接口设计粒度不够
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:191:### P1-2：USE_MOCK_DATA太粗且有生产风险
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:209:USER_DATA_SOURCE = 'csv'  # 生产环境使用CSV导入
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:233:### P1-3：Mock数据真实性不足
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:277:| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:278:| Week 2-3 | CSV导入功能、staging表、upsert逻辑、审计日志 | CSV导入模块、导入校验报告 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:281:| Week 8-9 | 前端开发 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:286:- 用户主数据API替换CSV（如需）：另计2-4周
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:299:外部数据源 (CSV/API/Mock)
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:301:ImportSource (数据导入源)
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:303:ImportService (导入服务：校验、staging、upsert、软停用)
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:313:1. **用户主数据落库：** 学生、辅导员、班级映射通过CSV导入到本地数据库
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:314:2. **Provider用于导入：** ImportSource接口用于数据导入，不是运行时查询
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:324:**"Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配"**
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:330:| RealUserDataProvider运行时查询 | CSV导入到本地数据库 | 用户主数据是基础数据，不应依赖外部API |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:333:| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:334:| Provider用于运行时查询 | ImportSource用于数据导入 | 明确职责边界 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:338:1. **Week 1：** 数据契约、DTO、ImportSource接口
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:339:2. **Week 2-3：** CSV导入功能（staging + upsert + 审计）
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:348:- 稳定的数据契约
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:349:- CSV导入功能和校验逻辑
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:352:- 契约测试
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:364:3. Provider抽象层的用途是数据导入，不是运行时查询
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:371:3. 开始Week 1工作：数据契约和接口设计
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:16:1. **Week 0（1-2工作日）：** 冻结v0.1最小可执行契约
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:18:3. **Week 2：** CSV导入v1
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:19:4. **Week 3：** 核心流程补强 + v0.2契约
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:20:5. **Week 4-6：** 微信小程序并行开发
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:29:### 决策1：数据契约v0.1现在冻结（1-2工作日）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:31:**范围：** 最小可执行契约（不是极简字段，也不是完整模型）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:43:- 后端负责人owns契约包
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:64:- 完整CSV导入
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:77:1. 单端范围确认（只做微信小程序）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:78:2. OpenAPI/DTO达到v0.2（有changelog）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:91:- 完整CSV导入后台
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:93:### 决策4：单端交付（微信小程序优先）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:96:- 微信小程序（覆盖主要用户群）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:115:| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:117:| **Week 2** | CSV导入v1 | Staging表、校验报告、upsert、软停用基础、导入审计基础 | 可导入10学生+2辅导员，生成校验报告，软停用未导入账号 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:118:| **Week 3** | 核心流程补强 + v0.2契约 | 权限细化、异常流、API mock更新、前端启动检查 | v0.2契约冻结，前端mock可用，核心API稳定 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:119:| **Week 4-6** | 微信小程序并行开发 | 登录、申请、审批、查询主流程 | 小程序可用mock跑通完整流程，逐步联调真实后端 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:121:| **Week 8-9** | UAT和完善 | 通知、附件最小可用、异常流修复、导入演练 | UAT通过，主要缺陷修复 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:128:### 行动1：创建contract-v0.1.md
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:130:**文件路径：** `docs/contracts/contract-v0.1.md`
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:144:**时间限制：** 与contract-v0.1.md同步完成
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:172:**原因：** 降低前端集成风险，提前发现问题
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:176:**原方案A：** React Native + 微信小程序同时开发
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:178:**修正后：** 微信小程序优先，React Native后续迭代
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:182:### 修正4：从Week 1数据契约到Week 0
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:184:**原方案A：** Week 1做数据契约和接口设计
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:188:**原因：** 避免Week 1前半定义契约，后半只剩2-3天开发
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:200:## 六、风险缓解
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:202:### 风险1：Week 0契约定义延期
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:206:### 风险2：Week 1纵向切片未完成
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:212:### 风险3：前端Week 4启动条件不满足
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:217:- 如果v0.2契约仍没有确定状态枚举、角色和核心路径，先用1-2天补契约
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:219:### 风险4：Week 10过载
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:241:- 达成共识：Week 0-1拆分、v0.1最小可执行契约、保留最小权限校验、前端Week 4并行
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:246:2. **前端并行优于前端后置** - 降低集成风险
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:248:4. **数据契约提前冻结** - 避免Week 1前半定义后半开发
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:255:- CSV导入v1的详细设计（Week 2开始前）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:256:- 微信小程序技术栈选择（Week 3开始前）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:263:**下一步：** 创建contract-v0.1.md和week-0-1-execution-plan.md
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:15:它比旧计划好，但仍然是"先后端模块、后前端、最后联调"的瀑布排期。最大风险不是数据契约，而是到Week 8-10才发现端到端流程、微信小程序、附件、审批权限、宿舍降级和通知串不起来。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:23:### 问题1：前端后置风险高
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:26:- Week 8-9前端、Week 10联调风险很高
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:28:- 原计划同时要求React Native和微信小程序
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:48:若演示还包含双端、真实微信、完整附件、通知、导入审计、宿舍降级，那不现实。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:50:### 问题4：CSV导入前置过重
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:53:方案A仍然把CSV导入当成前置大模块。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:56:更好的做法是先做`seed/import minimal path`，让认证和审批用同一套落库数据跑起来，再完善CSV校验、staging、审计。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:58:### 问题5：数据契约"冻结"危险
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:61:"数据契约冻结"这个词危险。契约需要版本化和变更机制，不是一次冻结后假装不会变。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:64:40号文档已有DTO和ImportResult雏形，现在要做的是契约测试和样例数据包。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:70:### 问题1：Week 1做数据契约太晚吗？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:75:现在就应冻结v0.1：字段、枚举、样例CSV、错误码、前端API mock。Week 1用它跑纵向切片。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:84:### 问题3：CSV导入是否应该更早？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:86:**回答：** 不应Week 1完整完成，但Week 1必须完成最小导入路径。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:89:seed/CSV二选一落库到真实users/class mapping表。完整staging、审计、软停用放Week 2。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:107:**回答：** Mock Provider和契约测试必须Week 1进入提交申请流程。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:117:优先微信小程序或一个Web/RN壳，不要默认双端完整交付。生产就绪不现实，尤其原计划还要求80%覆盖率、P95、1000并发。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:124:Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:131:契约v0.1 + 纵向切片 → CSV导入硬化 → 核心流程扩展 → 前端并行 → 外部集成 → 验收硬化
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:146:**Week 0-1：契约 + 纵向切片**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:147:- 契约v0.1（字段、枚举、样例CSV、错误码、前端API mock）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:154:**Week 2：CSV导入v1**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:168:- 先做微信小程序主流程
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:179:- 导入演练
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:195:明确演示范围：单端（微信小程序优先）+ 核心流程 + Mock数据。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:200:React Native和微信小程序同时开发，资源不足。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:203:优先微信小程序，React Native作为可选项或后续迭代。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:213:### 4. 导入失败后的人工处理流程不明确
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:216:CSV导入失败后，如何人工修复？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:219:设计导入失败处理流程：校验报告 → 人工修正 → 重新导入。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:221:### 5. 数据契约缺少版本管理
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:224:数据契约如何演进？如何处理字段变更？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:227:建立契约版本管理机制：v0.1 → v0.2 → v1.0，每次变更记录在changelog。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:244:1. 立即冻结数据契约v0.1（现在，不是Week 1）
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:12:Claude的质疑是必要的，尤其是把"Week 0准备"和"Week 1纵向切片"拆开这一点，有助于避免把契约、数据、实现全塞进同一个5天窗口。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:16:1. 把v0.1契约理解成"字段清单"，而不是可执行契约包。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:23:**采用Week 0-1拆分，但Week 0必须是1-2个工作日的timebox；v0.1应现在冻结最小可执行契约，不等到Week 1前半；Week 1只承诺后端端到端最小闭环；前端Week 4启动不要求后端完全稳定，只要求契约、mock和核心路径达到可消费状态。**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:27:## 一、数据契约v0.1：现在冻结还是Week 1前半？
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:38:- 样例CSV或seed fixture
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:41:- 契约变更记录
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:43:如果拖到Week 1前半才冻结，Week 1后半只剩2-3天，很难完成后端骨架、认证、申请、审批、状态查询和集成测试。Claude把这个拆法描述成"Week 1前半冻结，Week 1后半纵向切片"，本质上还是把Week 1压缩成半周开发，风险比Codex原建议更高。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:52:建议采用**最小可执行契约**：
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:54:| 契约块 | v0.1必须包含 | v0.1不必完整包含 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:63:| CSV/seed | 正常样本 + 边界样本 | 完整生产导入模板 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:65:也就是说，v0.1的范围应是**能跑通纵向切片且为v0.2留扩展点**，不是"最小字段"和"完整模型"二选一。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:71:- 后端负责人 owns 契约包：OpenAPI/DTO/错误码/seed schema。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:72:- 前端负责人 reviews 契约可消费性：字段命名、状态展示、错误展示、登录态。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:74:- 样例CSV/fixture先用合成数据，不等待真实样本；真实样本只用于v0.2/v1.0校准。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:75:- 前端API mock由契约生成或从后端mock server导出，不能由前端手写一套与后端脱节的mock。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:85:如果团队是2-3人，且Week 0已经完成v0.1契约，Week 1用5个工作日交付最小后端闭环是有机会的。但前提是严格砍范围，并且明确并行路径。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:110:- 完整CSV staging、upsert、软停用、导入审计
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:121:**Week 0 / Day 0-1：契约timebox**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:123:- 冻结v0.1最小可执行契约
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:145:- 契约测试
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:159:Claude列出的前提条件里，"核心流程后端API已实现"和"认证机制已确定"是对的；但"API契约稳定至少v0.2"如果理解成后端字段不再变化，就太重了。前端并行开发需要的是可消费契约，不是生产级冻结。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:163:Week 4开始微信小程序主流程开发前，必须满足：
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:165:1. 单端范围已确认：首版只做微信小程序，不并行React Native。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:166:2. OpenAPI/DTO达到v0.2，破坏性变更需要changelog。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:182:- 完整CSV导入后台
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:190:- 如果v0.2契约仍没有确定状态枚举、角色和核心路径，则不能启动页面开发，应先用1-2天补契约，否则前端会做成静态原型。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:200:- Week 0做契约和fixture
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:205:这比文档40的"Week 1只做数据契约、Week 8-9才做前端"更好。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:211:如果Week 0花3天定义契约，再Week 1花5天做切片，总体变成8个工作日。不是不可以，但这应被明确计入计划，而不是把"现在"当免费缓冲。建议Week 0限制为1-2个工作日，超过就冻结当前假设继续做，后续进入v0.2。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:215:Claude的Week 0列了StudentDTO、ApplicationDTO、ApprovalDTO，但缺少错误码、状态机、样例请求响应、mock、契约测试和变更规则。前端和测试真正依赖的是这些可执行产物，不只是字段名。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:223:Claude前面说"前端Week 4并行"，后面修正建议又写"Week 2：CSV导入 + 前端开始"。这两个说法需要统一。我的建议是：Week 2可以开始前端技术预研和API client封装，但微信小程序主流程页面开发以Week 4为正式启动点。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:225:**问题5：CSV导入仍可能挤压Week 2。**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:227:Claude建议Week 2做CSV导入并让前端开始，但CSV staging、校验报告、upsert、软停用、审计日志本身就是一周以上风险项。Week 2的目标应定义为"CSV导入v1可用"，前端只做轻量准备；不要让Week 2同时承诺完整导入和主流程前端。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:231:Week 1可以交Postman集合，但必须有自动化端到端测试。否则每次契约变化都靠人工点接口，后续Week 2-4会快速失控。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:241:| Week 0 / 1-2工作日 | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:243:| Week 2 | CSV导入v1 | staging、校验报告、upsert、软停用基础、导入审计基础 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:244:| Week 3 | 核心流程补强 + v0.2契约 | 权限细化、异常流、API mock更新、前端启动检查 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:245:| Week 4-6 | 微信小程序并行开发 | 登录、申请、审批、查询主流程，使用mock并逐步联调真实后端 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:247:| Week 8-9 | UAT和完善 | 通知、附件最小可用、异常流修复、导入演练 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:254:1. **数据契约v0.1应该现在冻结还是Week 1前半？范围最小还是完整？**  
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:255:   现在冻结，限制在1-2个工作日内完成。范围是"最小可执行契约"，不是极简字段，也不是完整未来模型。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:258:   如果指7-10人日，在2-3人团队下现实；如果指7-10日历天，不现实。调整方式是Week 0先完成契约，Week 1只做后端最小闭环，推迟CSV完整导入、附件、通知、微信OAuth、真实宿舍API。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:261:   v0.2可消费契约、mock可用、核心API可跑、认证策略固定为演示期薄认证、状态枚举/错误码稳定、API owner和变更机制明确。不要求附件、通知、真实OAuth、真实宿舍API完成。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:264:   方向可行，但必须修正：Week 0要timebox，v0.1要可执行而非字段清单，Week 1不能砍掉最小权限校验，前端启动时间要统一，Week 2不要同时塞满CSV和主流程前端。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:270:**接受Claude的拆分方向，但不接受把契约冻结推迟到Week 1前半，也不接受Week 1无权限校验的纵向切片。**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:274:1. `contract-v0.1.md`或OpenAPI草案：字段、状态、错误码、样例、mock、changelog。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:277:这两个文件完成后，再更新总实施计划。否则直接改10周排期仍然会停留在计划层，不能降低真正的集成风险。
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:1:# P1 Fixes Summary
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:11:基于Codex审查（文档49）指出的2个P1阻塞问题，已完成全部修复：
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:13:### ✅ P1修复1：补齐缺失错误样例
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:17:**修改文件：** docs/contracts/contract-v0.1.md
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:80:### ✅ P1修复2：修复降级方案矛盾
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:82:**问题：** 风险2降级方案说"砍学工部审批，Day 4补学工部审批"，逻辑矛盾
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:100:## P2问题（未修复，优先级较低）
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:102:### P2-1：术语不一致
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:110:### P2-2：AuthUserDTO未正式定义
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:123:1. P1修复是否解决了阻塞问题
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:124:2. 契约是否达到"可执行契约"标准
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:125:3. 是否可以冻结contract-v0.1.md并开始Week 1 Day 1工作
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:128:1. 冻结contract-v0.1.md（标记为v0.1 Final）
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:136:3. 直到达到"可执行契约"标准
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:16:**核心问题：** 方案把"用户主数据 API 化"当成默认终局，偏离了此前已达成的首版共识：学生、辅导员、班级映射应优先走 CSV/Excel 导入，宿舍清退才是实时 API。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:24:## P0问题（必须修复）
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:26:### P0-1：RealUserDataProvider不应成为运行时依赖
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:34:应落入本地数据库，通过 CSV/API Provider 输入到 staging，再校验、upsert、软停用。此前设计已经定义了 staging + upsert + 软停用、导入审计和校验报告：[31-data-source-requirements-consensus-v2.md](../codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md) 第282行。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:36:**风险：**
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:39:- 外部 API 可用性风险
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:47:1. 用户主数据（学生、辅导员、班级映射）通过CSV导入到本地数据库
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:49:3. 保留Provider抽象层，但明确其用途：数据导入（非运行时查询）
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:53:### P0-2：+3天生产就绪评估过于乐观
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:57:3天只适用于"API 契约已冻结、测试环境可用、认证已跑通、字段完全覆盖、只写一个薄适配器"的场景。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:73:- **用户主数据API（如果坚持）：** 2-4周（牵涉数据模型、导入/同步策略、账号状态、审批人映射和验收演练）
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:81:## P1问题（重要改进）
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:83:### P1-1：接口设计粒度不够
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:113:### P1-2：USE_MOCK_DATA太粗且有生产风险
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:131:- 支持"用户主数据 CSV + 宿舍清退 API"的混合模式
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:135:### P1-3：Mock数据真实性不足
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:139:100学生、10辅导员可以支撑演示，但不足以覆盖风险。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:167:Provider 契约、DTO、种子数据、导入接口应在 Week 1-2 完成，否则认证、审批、前端都会先绑定临时模型，后续返工。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:175:| Week 1 | 数据契约、DTO、Provider接口、种子数据、导入模型 | 数据契约文档、DTO定义、Provider接口 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:176:| Week 2-3 | CSV/staging/upsert/审计和核心账号数据 | CSV导入功能、staging表、审计日志 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:179:| Week 8-9 | 前端 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:184:- 用户主数据 API 替换 CSV：另计 2-4周
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:192:若外部 API 字段继续缺失，首版应坚持 CSV/Excel 主数据导入，不等待 API。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:203:│  CSV / API / DB View / Mock                │
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:216:│    Import/Sync Service（导入/同步服务）      │
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:221:│  - 导入审计                                 │
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:241:1. **外部数据源：** CSV/API/DB view/Mock
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:296:**"Seed/Mock + Provider 抽象 + CSV 主数据导入 + 宿舍清退 API 适配"**
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:303:   - 稳定的数据契约
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:304:   - 导入校验
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:306:   - 契约测试
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:311:1. **Week 1-3：** CSV导入 + 种子数据
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:320:如果数据变更频率高，可升级为API/DB同步。但首版应坚持CSV导入，快速上线。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:4:**审查类型：** 契约修复验证  
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:12:在上一轮审查中（文档46），Codex指出contract-v0.1.md和week-0-1-execution-plan.md存在3-4个问题，导致契约"接近可执行契约"但未达到标准。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:15:> "结论：**还没有完全达到"可执行契约"标准，不建议直接开始 Week 1 的完整实施**。可以先启动不受争议影响的 Day 1 骨架、模型、seed、认证准备，但应先用半天把下面几个契约不一致点修掉再冻结。"
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:23:**问题：** 契约列出6个HTTP路由，计划说"5个核心API端点"（Week 0 Day 1）和"4个API端点"（Week 1 Day 3-4），口径不一致。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:26:- 从contract-v0.1.md移除Section 4.4 GET /api/applications（列表端点）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:36:**文件：** docs/contracts/contract-v0.1.md（Section 4.4已删除）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:45:- 在contract-v0.1.md Section 6.2添加503错误样例
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:61:**文件：** docs/contracts/contract-v0.1.md（Section 6.2新增503样例）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:70:- 在contract-v0.1.md Section 4.1 POST /api/auth/login添加说明
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:74:**文件：** docs/contracts/contract-v0.1.md（Section 4.1新增说明）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:80:**问题：** 风险表中"申请提交API未完成 → 只做查询API"与纵向切片目标矛盾（无法先查询后提交）。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:83:- 修改week-0-1-execution-plan.md风险2降级方案：
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:86:- 同步修改Day 3-4降级条件，移除"列表API"引用（已从契约删除）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:88:**文件：** docs/plans/week-0-1-execution-plan.md（风险2和Day 3-4降级条件已修改）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:101:- [ ] 契约和计划的API端点数量现在是否一致？
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:118:- [ ] 契约现在是否达到"可执行契约"标准？
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:119:- [ ] 是否可以冻结契约并开始Week 1 Day 1工作？
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:128:3. **可执行性判断：** 明确回答"是否达到可执行契约标准"
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:129:4. **下一步建议：** 如果达标，建议冻结契约；如果未达标，建议优先修复哪些点
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:136:- docs/contracts/contract-v0.1.md（已修改）
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:17:4. ✗ Serializer风险（N+1查询，暴露过多数据）
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:42:**承认:** 忽略了N+1查询和数据暴露风险
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md:12:- Week 0: contract-v0.1.md冻结（可执行契约标准）
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md:14:- Week 2: ClassMapping模型、CSV导入命令、动态辅导员分配、CSV模板
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md:35:- 准备v0.2契约（附件管理、通知系统）
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md:45:- 风险增加（可能存在大量隐藏bug）
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md:75:- 降低风险
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md:90:1. **技术债务临界点：** Week 1-2已经积累了25个未测试文件，继续累积风险过高
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md:93:4. **契约精神：** contract-v0.1.md定义了验收标准，但我们无法验证是否达标
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md:103:**风险：**
docs/discussions/week3-direction-2026-05-30/03-claude-response.md:35:**潜在风险：**
docs/discussions/week3-direction-2026-05-30/03-claude-response.md:66:### 质疑4：P0-P3优先级可能需要调整
docs/discussions/week3-direction-2026-05-30/03-claude-response.md:68:**Codex的P2包括"Docker Compose覆盖必要依赖"，但：**
docs/discussions/week3-direction-2026-05-30/03-claude-response.md:70:- 应该把"环境搭建"降级到P1或P2，把"代码验证"提升到P0
docs/discussions/week3-direction-2026-05-30/03-claude-response.md:73:- **P0**：跑通最小闭环（无论用什么环境）
docs/discussions/week3-direction-2026-05-30/03-claude-response.md:74:- **P1**：修复闭环中暴露的问题
docs/discussions/week3-direction-2026-05-30/03-claude-response.md:75:- **P2**：环境自动化（Docker或脚本）
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:17:2. **弹性timebox的风险**：Codex指出"2-3天弹性timebox容易滑成小型修复周"，这个批评成立。我的C-Modified方案确实存在范围蔓延风险。
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:23:### Codex遗漏风险的价值
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:28:- **可验证证据标准**：不能只说"手动跑通"，必须有smoke test或命令记录
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:30:- **权限不是边界条件**：权限验证是核心安全契约，必须包含在最小闭环
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:48:这个设计避免了我方案中的"延期掩盖问题性质"风险。
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:73:- **成功**：最小闭环可复现，或仅剩少量明确P0缺陷
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:89:- 补充了我遗漏的7个关键风险点
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:109:- 导入seed数据
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:113:**Day 2：只修P0并固化证据**
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:115:- 保留可复现验证入口（smoke脚本/API请求集合）
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:120:- 条件：最小闭环已接近跑通，且剩余问题是明确局部P0缺陷
docs/contracts/contract-v0.1.md:1:# 数据契约 v0.1 Final - 最小可执行契约
docs/contracts/contract-v0.1.md:4:**状态：** ✅ 已冻结（可执行契约标准）  
docs/contracts/contract-v0.1.md:7:**下一版本：** v0.2（Week 3）  
docs/contracts/contract-v0.1.md:127:### 2.6 状态机契约
docs/contracts/contract-v0.1.md:567:**初始版本 - 最小可执行契约**
docs/contracts/contract-v0.1.md:577:**不包含内容（v0.2）：**
docs/contracts/contract-v0.1.md:646:**契约负责人：** Claude Opus 4.7  
docs/contracts/contract-v0.1.md:650:**下一版本：** v0.2（Week 3）
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:1:# P1 Fixes - Codex Confirmation Response
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:6:**审查类型：** P1修复确认
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:12:**可执行契约标准：** 是
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:16:**结论：** 可以冻结 `docs/contracts/contract-v0.1.md` 为 v0.1 Final，并开始 Week 1 Day 1 工作。
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:20:## P1修复验证
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:26:`docs/contracts/contract-v0.1.md` Section 3定义的8个错误码为：
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:62:其中401和403省略 `details`，这对v0.1可接受；如果后续要生成严格schema，可在v0.2明确 `details` 为可选字段。
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:68:风险2当前表述为：
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:87:### P0/P1问题
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:91:当前没有继续阻塞契约冻结或Week 1 Day 1启动的问题。
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:93:### P2问题
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:95:1. `week-0-1-execution-plan.md` 仍有“4个API端点可用”的表述，和契约“5个HTTP路由”容易产生术语混淆。建议后续改为“4个业务HTTP路由可用，不含Day 1-2登录路由”，或在Week 1验收处统一写“5个HTTP路由覆盖4个核心能力”。
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:96:2. `AuthUserDTO` 仍未在Section 1正式定义。Section 4.1已有解释，对v0.1实现不构成阻塞；建议v0.2或冻结前顺手补充正式DTO定义。
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:97:3. Day 3-4局部降级条件中“如Day 3结束申请提交API未完成 -> 保留最短闭环”的一句仍较压缩。风险表已给出清晰版本，因此不再构成P1；建议后续同步成同一口径，减少计划文档内重复表达的维护成本。
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:103:1. 冻结 `docs/contracts/contract-v0.1.md` 为 v0.1 Final。
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:105:3. 将上述P2作为非阻塞清理项处理，不应继续阻塞Week 1启动。
docs/discussions/week3-direction-2026-05-30/02-codex-review.md:15:- Week 0-2代码未经验证，继续盲写功能风险高
docs/discussions/week3-direction-2026-05-30/02-codex-review.md:26:先把当前Week 0-2代码跑通一条最小链路，补齐会阻塞演示的契约/环境问题，然后立刻回到Week 3核心流程补强。
docs/discussions/week3-direction-2026-05-30/02-codex-review.md:30:**P0（必须完成）：**
docs/discussions/week3-direction-2026-05-30/02-codex-review.md:33:- 验证contract-v0.1.md定义的核心流程可执行
docs/discussions/week3-direction-2026-05-30/02-codex-review.md:35:**P1（发现问题立即修复）：**
docs/discussions/week3-direction-2026-05-30/02-codex-review.md:36:- 修复闭环中暴露的契约问题（字段缺失、类型不匹配）
docs/discussions/week3-direction-2026-05-30/02-codex-review.md:40:**P2（最小化环境脚手架）：**
docs/discussions/week3-direction-2026-05-30/02-codex-review.md:60:| **风险** | 开发节奏中断 | 平衡速度和质量 |
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:13:- **P0问题（问题7）**：初始密码安全风险必须立即修复
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:14:- **P1问题（问题1、3、5）**：已部分修复，需继续完善
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:15:- **P2问题（问题2、4、6、8、9）**：影响对接和用户体验，应修复
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:23:### 问题1：引用不存在的 Excel 模板文件 [P1]
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:27:**Claude确认：** ✓ 已在前一轮修复（commit: docs: 修正CSV模板文件扩展名引用）
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:33:### 问题2：引用不存在的 Postman 文件 [P2]
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:51:### 问题3：API 示例使用 HTTP 但安全要求 HTTPS [P1]
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:63:4. **安全平衡**：内网环境下 HTTP 风险可控，可通过 IP 白名单 + API Key 补偿
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:72:### 问题4：认证方式描述不够收敛 [P2]
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:92:### 问题5：数据脱敏与请求参数冲突 [P1]
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:111:### 问题6：审批时限口径不一致 [P2]
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:129:### 问题7：初始密码为身份证后 6 位有安全风险 [P0]
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:131:**Codex指出：** 弱口令风险高，扩大身份证信息依赖
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:133:**Claude确认：** ✓ 严重安全风险
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:150:### 问题8：辅导员权限按"本年级"过粗 [P2]
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:169:### 问题9：容量指标不一致 [P2]
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:200:   - 风险评估：内网环境风险可控
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:221:**P0（立即修复）：**
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:224:**P1（应该修复）：**
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:229:**P2（建议修复）：**
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:26:3. **[Codex addition]** Sync CSV template: Update students_template.csv line 3 to `CS2020-02`
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:27:4. Fix smoke_test.sh duplicate submission issue
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:29:**Acceptance:** All 12 tests passing + smoke script runs without errors
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:88:### Phase 3: Smoke Test Update (30-60 min) - PRIORITY 4
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:98:**Acceptance:** Smoke test passes using list endpoints for discovery
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:133:**Issue:** `2020002` is `CS2020-02` in seed_data but `CS2020-01` in CSV template.
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:184:- Smoke script issue confirmed: Line 175 creates duplicate application
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:197:5. Smoke test verification (T002 cannot see T001 data)
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:61:### 2. 是否还有其他安全风险？
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:63:**是的 - 发现3个额外风险：**
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:65:#### 风险A: 学号枚举攻击（HIGH严重性）
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:85:#### 风险B: 微信绑定的竞态条件（MEDIUM严重性）
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:102:#### 风险C: 绑定操作无审计追踪（MEDIUM严重性）
docs/discussions/week3-direction-2026-05-30/06-consensus.md:11:**采用方案D：2天硬timebox + 明确闭环范围 + 决策门 + 可选P0修复日**
docs/discussions/week3-direction-2026-05-30/06-consensus.md:42:3. 导入或创建seed数据
docs/discussions/week3-direction-2026-05-30/06-consensus.md:52:- 问题清单（按P0/P1/P2分类）
docs/discussions/week3-direction-2026-05-30/06-consensus.md:55:### Day 2：只修P0并固化证据
docs/discussions/week3-direction-2026-05-30/06-consensus.md:60:1. 修复阻塞闭环的P0问题
docs/discussions/week3-direction-2026-05-30/06-consensus.md:62:   - smoke test脚本，或
docs/discussions/week3-direction-2026-05-30/06-consensus.md:70:- P1/P2问题清单
docs/discussions/week3-direction-2026-05-30/06-consensus.md:77:- 剩余问题是明确局部P0缺陷（非架构级）
docs/discussions/week3-direction-2026-05-30/06-consensus.md:80:- 发现状态机、数据模型、契约冲突等架构级问题
docs/discussions/week3-direction-2026-05-30/06-consensus.md:121:   - 接口契约、失败分支、超时策略有占位定义
docs/discussions/week3-direction-2026-05-30/06-consensus.md:131:2. 仅剩少量明确P0缺陷（已识别、已分类、有修复计划）
docs/discussions/week3-direction-2026-05-30/06-consensus.md:136:- 发现架构级阻塞（状态机设计错误、数据模型根本缺陷、契约冲突）
docs/discussions/week3-direction-2026-05-30/06-consensus.md:168:**而是**：问题性质（是否阻塞演示、是否需要改契约、是否影响核心数据模型）
docs/discussions/week3-direction-2026-05-30/06-consensus.md:172:## Codex补充的7个关键风险
docs/discussions/week3-direction-2026-05-30/06-consensus.md:176:1. **可验证证据标准**：不能只说"手动跑通"，必须有smoke test或命令记录
docs/discussions/week3-direction-2026-05-30/06-consensus.md:178:3. **权限不是边界条件**：权限验证是核心安全契约，必须包含在最小闭环
docs/discussions/week3-direction-2026-05-30/06-consensus.md:179:4. **架构级问题处置门槛**：发现状态机或模型错误时，先判断是局部补丁还是契约重开
docs/discussions/week3-direction-2026-05-30/06-consensus.md:181:6. **宿舍清退mock风险**：Mock可以固定返回，但接口边界必须有占位定义
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:15:**修改文件：** docs/contracts/contract-v0.1.md
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:30:**修改文件：** docs/contracts/contract-v0.1.md
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:43:**修改文件：** docs/contracts/contract-v0.1.md
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:59:- 风险2降级方案：改为"保留提交→辅导员审批→查询闭环，砍学工部审批"
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:71:2. **Codex审查：** 需要Codex确认修复是否达到"可执行契约"标准
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:72:3. **契约冻结：** 如果Codex确认达标，可以冻结contract-v0.1.md
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:79:1. 冻结contract-v0.1.md（标记为v0.1 Final）
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:87:3. 直到达到"可执行契约"标准
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:31:- React Native 和小程序
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:151:计划中包含任务清单、验证标准、风险和缓解措施、交付物和协作建议。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:230:目录结构与实施计划基本一致，能够承接 Django 后端、移动端、小程序、Docker 配置等后续工作。当前为空目录是正常状态，因为只完成了结构创建。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:11:Claude的响应抓住了两个真实问题：最小闭环范围需要明确，Docker不应压过功能验证。但Claude也误读了timebox的核心目的：timebox不是承诺在1-2天内修完所有问题，而是在有限时间内暴露风险、建立可复现证据，并决定继续修、降范围还是停下来重设计。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:13:因此我不建议直接采用Claude的C-Modified。它比原方案更完整，但把1-2天硬timebox改成2-3天弹性timebox后，存在范围滑移风险，也把“问题分类”设计成独立半天，容易消耗掉真正验证和修复的时间。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:15:更优方案是第三种：**2天硬timebox + 明确范围 + 决策门 + 可选第3天只处理已确认的P0阻塞项**。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:30:- 成功：最小闭环可复现，或仅剩少量明确P0缺陷。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:69:### 质疑4：P0-P3优先级需要调整
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:73:Claude把“跑通最小闭环”提升为P0是正确的。Docker不应作为P0本身。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:75:但“环境搭建”不能整体降到P2，因为没有一个可复现环境，就无法证明闭环真的跑通。应拆分为：
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:76:- P0：获得一个能稳定执行闭环的环境，无论本地还是容器。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:77:- P1：修复闭环阻塞缺陷。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:78:- P2：把已验证的启动方式自动化为脚本或Docker Compose。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:102:## 3. Claude遗漏的风险和盲点
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:105:   不能只说“手动跑通”。应输出命令记录、测试账号、API请求样例、响应结果，至少保留一个smoke test脚本或可复现步骤。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:110:3. **权限被当成可选边界风险。**  
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:111:   学生只能查自己的申请不是边界条件，而是核心安全契约。最小闭环至少要覆盖一条负向权限验证。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:114:   发现状态机或模型关系错误时，不能自动进入修复阶段。应先判断是局部补丁、迁移调整，还是契约需要重开。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:117:   如果Day 2修复了P0 bug，但没有脚本化最小闭环，后续Week 3继续开发可能再次破坏同一链路。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:119:6. **对宿舍清退mock的风险描述不足。**  
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:120:   Mock可以固定返回，但接口契约、失败分支、超时/不可用策略至少要有占位定义，否则后续接真实系统时会返工。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:123:   Week 1-2代码未经运行，首次迁移可能暴露默认值、nullable、外键约束、枚举状态不一致等问题。这类问题应作为P0验证项。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:132:   原方案的价值在于尽快逼出“能跑/不能跑/为什么不能跑”的事实。把默认时间改成2-3天，会让团队倾向继续修小问题，而不是及时承认设计风险。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:141:   延不延期应看问题性质：是否阻塞演示、是否需要改契约、是否影响核心数据模型，而不是数量阈值。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:147:### 方案D：2天硬timebox + 决策门 + 可选P0修复日
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:157:- 导入或创建seed数据。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:161:**Day 2：只修P0并固化证据**
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:163:- 保留至少一个可复现验证入口：smoke脚本、API请求集合、或清晰命令序列。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:168:- 仅当最小闭环已接近跑通，且剩余问题是明确局部P0缺陷时使用。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:169:- 如果发现状态机、数据模型、契约冲突等架构级问题，不启用Day 3修补，改为暂停Week 3扩展开发并重做设计决策。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:194:不建议完全回到Codex原始1-2天方案，因为它确实需要更清晰的闭环范围和失败处理。也不建议直接采用Claude的2-3天弹性方案，因为它削弱了timebox的风险控制作用。
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:196:建议采用方案D：**2天硬timebox验证最小闭环，可选第3天只处理明确P0阻塞；一旦发现架构级问题，停止扩展开发并重开设计讨论。**
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:16:2. ✓ 定义v0.1为"最小可执行契约"（不是字段清单）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:19:5. ✓ 明确Week 2只做CSV导入v1（不塞前端主流程）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:27:### 1. 数据契约v0.1：现在冻结（1-2工作日）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:31:**v0.1范围：最小可执行契约**
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:41:- 后端负责人owns契约包
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:64:- 完整CSV导入
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:79:1. 单端范围确认（只做微信小程序）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:80:2. OpenAPI/DTO达到v0.2（有changelog）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:93:- 完整CSV导入后台
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:107:**修正5：** Week 2只做CSV导入v1（不塞前端主流程）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:116:| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:118:| **Week 2** | CSV导入v1 | Staging表、校验报告、upsert、软停用基础、导入审计基础 | 可导入10学生+2辅导员，生成校验报告，软停用未导入账号 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:119:| **Week 3** | 核心流程补强 + v0.2契约 | 权限细化、异常流、API mock更新、前端启动检查 | v0.2契约冻结，前端mock可用，核心API稳定 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:120:| **Week 4-6** | 微信小程序并行开发 | 登录、申请、审批、查询主流程 | 小程序可用mock跑通完整流程，逐步联调真实后端 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:122:| **Week 8-9** | UAT和完善 | 通知、附件最小可用、异常流修复、导入演练 | UAT通过，主要缺陷修复 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:129:### 行动1：创建contract-v0.1.md
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:131:**文件路径：** `docs/contracts/contract-v0.1.md`
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:135:# 数据契约 v0.1 - 最小可执行契约
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:221:- [ ] 契约测试
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:232:**时间限制：** 与contract-v0.1.md同步完成
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:241:1. ✓ Week 0是1-2工作日timebox，冻结v0.1最小可执行契约
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:246:6. ✓ Week 2只做CSV导入v1，不塞前端主流程
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:248:8. ✓ 单端交付（微信小程序优先）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:252:1. 创建`docs/contracts/contract-v0.1.md`
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:258:- CSV导入v1的详细设计（Week 2开始前）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:259:- 微信小程序技术栈选择（Week 3开始前）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:268:> 1. `contract-v0.1.md`或OpenAPI草案
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:274:> 这两个文件完成后，再更新总实施计划。否则直接改10周排期仍然会停留在计划层，不能降低真正的集成风险。
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:285:- Week 0（1-2工作日）：冻结v0.1最小可执行契约
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:287:- Week 2：CSV导入v1
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:288:- Week 3：核心流程补强 + v0.2契约
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:289:- Week 4-6：微信小程序并行开发
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:295:1. 创建contract-v0.1.md（1-2工作日）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:300:- 瀑布式排期风险
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:301:- 前端后置风险
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:302:- Week 10过载风险
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:303:- 数据契约延迟风险
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:304:- 权限校验缺失风险
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:6:**优先级：** P0（阻塞开发进度）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:20:- 原设计采用CSV导入用户数据（学生、辅导员、班级）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:201:| Week 8-9 | 前端开发 | React Native、微信小程序（测试AppID） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:221:4. **低风险切换** - 配置开关，无需改代码
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:227:3. **风险隔离** - API问题不影响核心功能
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:230:### 2.5 风险评估
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:232:**低风险：**
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:236:**中风险：**
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:266:### 3.2 风险评估
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:268:**问题4：真实API到位后的集成风险有多大？**
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:271:- 如何降低集成风险？
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:324:- 是否可以考虑Contract Testing（契约测试）？
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:340:3. 是否有致命缺陷或重大风险
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:343:### 4.2 风险识别
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:346:1. 方案中可能遗漏的风险点
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:347:2. 风险等级评估（P0/P1/P2）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:348:3. 风险缓解措施建议
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:378:2. ✓ 风险识别和缓解措施
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:395:- **技术栈：** Python Django + PostgreSQL + Redis + React Native + 微信小程序
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:404:- Round 3: P0修复、字段补充、用户文档（20+问题修复）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:417:**优先级：** P0（阻塞开发进度）
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:1:# P1 Fixes - Final Consensus
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:11:**状态：** ✅ 达到可执行契约标准
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:13:**Codex确认：** 2个P1阻塞问题已全部解决，可以冻结contract-v0.1.md并开始Week 1 Day 1工作。
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:19:### 修复1：补齐错误样例（P1-1）
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:31:### 修复2：修复降级方案矛盾（P1-2）
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:33:**问题：** 风险2说"砍学工部审批"又说"Day 4补学工部审批"
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:49:## 剩余P2问题（非阻塞）
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:51:Codex指出3个P2问题，不阻塞Week 1启动：
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:53:1. **术语不一致：** 执行计划"4个API端点" vs 契约"5个HTTP路由"
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:57:   - 建议：v0.2或冻结前补充正式定义
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:60:   - 建议：后续同步成风险表同一口径
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:66:### 契约冻结
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:68:**文件：** docs/contracts/contract-v0.1.md
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:70:**状态：** v0.1 Final（可执行契约标准）
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:98:- ✅ docs/contracts/contract-v0.1.md - P1修复完成
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:99:- ✅ docs/plans/week-0-1-execution-plan.md - P1修复完成
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:110:1. ✅ 冻结contract-v0.1.md（标记为v0.1 Final）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:6:**优先级：** P0（决定实施路径）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:17:- ✓ 达成最终共识：Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:22:外部数据源 (CSV/API/Mock)
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:24:ImportSource (数据导入源接口)
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:26:ImportService (导入服务：校验、staging、upsert、软停用)
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:38:2. 开始Week 1工作：数据契约、DTO、ImportSource接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:46:2. **发现问题** - 识别可能遗漏的风险和问题
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:65:   - 将数据契约和接口设计提前到Week 1
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:68:2. **Week 1启动：** 数据契约和接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:74:3. **Week 2-3：** CSV导入功能开发
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:78:   - 导入审计日志
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:82:- 路径清晰，风险可控
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:89:- 数据契约是否应该更早确定？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:97:**问题1：Week 1做数据契约是否太晚？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:98:- 数据契约影响认证、审批、前端所有模块
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:99:- 是否应该在Week 1之前（现在）就冻结数据契约？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:107:**问题3：CSV导入功能是否应该更早？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:108:- 当前计划Week 2-3做CSV导入
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:110:- 是否应该Week 1就完成CSV导入？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:112:### 4.2 关于技术风险
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:121:- 对于首版（CSV导入）是否过于复杂？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:122:- 是否应该先实现CSV导入，后续再抽象？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:132:- Week 1: 数据契约和接口
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:133:- Week 2-3: CSV导入
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:142:- 数据契约、DTO、接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:144:- 导入模型设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:151:- 当前：数据契约→CSV导入→核心业务→API集成→前端→联调
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:159:- 哪种顺序风险更低？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:169:2. 识别的风险和遗漏点
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:186:- 风险缓解措施
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:197:4. ✓ 技术风险的识别
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:219:- **数据对接文档：** CSV模板、API规范
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:224:- CSV导入是首版主数据来源
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:226:- 微信小程序测试AppID可用
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:237:4. 指出可能遗漏的风险
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:250:**优先级：** P0（决定实施路径）
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:1:# P1 Fixes Confirmation Request
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:11:请Codex批判性审查P1修复完成情况，并明确回答是否达到"可执行契约"标准。
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:17:上一轮审查（文档49）指出2个P1阻塞问题：
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:19:1. **P1-1：错误样例覆盖不完整** - Section 3定义8个错误码，Section 6.2只有4个样例
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:20:2. **P1-2：降级方案逻辑矛盾** - 风险2说"砍学工部审批"又说"Day 4补学工部审批"
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:30:**文件：** docs/contracts/contract-v0.1.md Section 6.2
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:60:### 1. P1修复验证
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:63:- [ ] 错误样例格式是否符合契约规范？
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:67:### 2. 可执行契约标准
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:71:**Q1：契约是否达到"可执行契约"标准？**
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:72:- [ ] 是 - 可以冻结contract-v0.1.md并开始Week 1 Day 1
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:76:- 按优先级列出（P0/P1/P2）
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:94:**可执行契约标准：** [是/否]
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:98:## P1修复验证
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:110:### P0/P1问题
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:113:### P2问题
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:125:- **契约文档：** docs/contracts/contract-v0.1.md
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:128:- **上轮审查：** docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:133:**优先级：** P0（阻塞Week 1启动）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:166:- [ ] 风险识别是否充分？
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:217:- 是否有技术风险？
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:17:2. **设计层面**：部分设计过度复杂，实施风险高（微信绑定、性能目标、冗余表）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:20:- P0（立即修改）：11项
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:21:- P1（强烈建议）：6项
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:22:- P2（可选优化）：6项
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:26:## 第一部分：无争议修改项（P0）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:161:**理由：** 直连数据库安全风险高，违反服务边界原则
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:293:- 本系统是内部系统，用户由管理员导入
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:294:- 学号枚举风险低（学号在校内公开）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:342:## 第三部分：P1修改项（强烈建议）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:500:### 立即修改（P0）- 11项
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:518:### 强烈建议（P1）- 6项
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:546:### 风险评估
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:548:| 风险 | 修改前 | 修改后 | 缓解措施 |
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:560:1. 完成P0修改（11项，1.5天）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:561:2. 完成P1修改（6项，0.5天）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:574:**下一步：** 执行P0+P1修改，更新设计文档
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:25:#### 3. SQLAlchemy备选方案安全风险高
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:27:- **问题：** 直连外部数据库存在严重安全风险
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:130:**必须修改（P0）：**
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:269:### 实施风险评估
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:271:| 风险 | 等级 | 缓解措施 |
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:297:4. **批量修改**：应用所有P0和P1修改
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:305:**建议修改项：** 15个P0/P1优先级
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:14:1. **CSV导入策略**：从"全量覆盖"改为"staging表 + upsert + 软停用"
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:19:   - 新增`import_logs`表（导入审计）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:21:3. **认证约束调整**：增加`password_setup_required`支持CSV预导入账号
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:22:4. **对接方式调整**：学生/辅导员/班级映射改为"CSV/Excel首版优先"
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:37:| 学生基本信息 | P0 | 创建学生账号、身份识别、班级映射 | **CSV/Excel首版优先** / API或DB增强 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:38:| 宿舍清退数据 | P0 | 验证学生是否完成宿舍清退 | API优先 / DB备选 / CSV降级 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:39:| 辅导员基本信息 | P0 | 创建辅导员账号、审批权限 | **CSV/Excel首版优先** / 人事或统一身份API增强 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:41:| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:44:- **CSV/Excel首版优先**：首版采用CSV/Excel批量导入，快速上线，后续根据数据变更频率决定是否升级为API/DB
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:47:- **CSV降级**：当无法提供API或DB时，通过CSV文件导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:50:1. **实施周期**：CSV/Excel导入最快，DB直连需要安全审批和网络配置
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:52:3. **风险控制**：CSV导入可以先验证、再导入、可回滚；DB直连风险更高
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:56:## 二、P0数据源详细要求
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:93:**CSV模板示例：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:102:- 只导入当届毕业生（`is_graduating=true` 且 `graduation_year=2026`）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:169:**CSV模板示例：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:217:**CSV模板示例：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:228:- 导入后输出校验报告：未匹配班级、未匹配辅导员、重复映射、无审批人的学生数
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:255:- 首版采用手动创建，不参与批量导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:267:### 3.1 CSV/Excel导入（首版推荐）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:278:- 格式：CSV或Excel（.xlsx）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:282:**导入策略（v2修订）：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:286:1. CSV导入到临时staging表（按类型拆分）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:288:3. 本次未导入的账号标记为 `is_active=false`
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:289:4. 下次导入重新出现时自动激活
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:294:-- 学生导入staging表
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:309:-- 辅导员导入staging表
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:318:-- 班级映射导入staging表
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:325:**导入流程：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:331:-- 2. 导入CSV到staging表
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:345:-- 4. 软停用：本次未导入的学生（使用NOT EXISTS避免NULL问题）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:362:**导入审计（v2新增）：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:474:| 学生账号 | 当届毕业生 | 1000人/届 | 只导入当届（`is_graduating=true` 且 `graduation_year=2026`） |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:500:**学生导入时只导入当前批次：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:531:9. 优先推荐的对接方式是什么？（DB直连 / API / CSV导入）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:533:11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:539:14. 是否需要导入手机号/邮箱用于找回密码或二次验证？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:551:首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:552:- 学生、辅导员、班级映射：CSV/Excel批量导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:564:**阶段2：CSV导入实现（2周）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:565:1. 设计三份CSV模板：学生、辅导员、班级-辅导员映射
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:566:2. 实现CSV导入功能和校验逻辑
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:569:5. 实现导入审计日志（v2新增）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:570:6. 生成导入校验报告（成功数、失败数、错误明细）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:580:2. 完成一次全量导入演练
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:612:**1. students_staging - 学生导入临时表**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:629:**2. counselors_staging - 辅导员导入临时表**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:640:**3. class_mapping_staging - 班级映射导入临时表**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:686:**6. import_logs - 导入审计日志表**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:722:1. ✅ CSV导入策略从"全量覆盖"改为"staging + upsert + 软停用"
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:725:4. ✅ 认证约束调整：支持CSV预导入账号（password_setup_required）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:726:5. ✅ 对接方式调整：学生/辅导员/班级映射改为CSV首版优先
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:13:1. ✓ P0 - 初始密码安全风险（学号+强制修改）
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:14:2. ✓ P1 - HTTPS要求改为双模式（HTTP内网 + HTTPS公网）
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:15:3. ✓ P1 - 删除id_card参数（避免身份证号传输）
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:16:4. ✓ P2 - 删除Postman引用（文件不存在）
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:17:5. ✓ P2 - 明确认证方式（API Key + IP白名单）
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:18:6. ✓ P2 - 统一审批时限（1个工作日）
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:19:7. ✓ P2 - 修改辅导员权限范围（负责的班级）
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:20:8. ✓ P2 - 统一性能指标（P95 < 200ms）
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:26:### 修复1：初始密码安全策略 [P0]
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:45:### 修复2：HTTPS要求改为双模式 [P1]
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:64:### 修复3：删除id_card参数 [P1]
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:80:### 修复4：删除Postman引用 [P2]
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:98:### 修复5：明确认证方式 [P2]
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:124:### 修复6：统一审批时限 [P2]
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:144:### 修复7：修改辅导员权限范围 [P2]
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:168:### 修复8：统一性能指标 [P2]
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:197:- 内网环境：HTTP + IP白名单 + API Key（风险可控）
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:11:**总体评价：** 字段补充方向合理，但当前文档之间仍存在必填性和字段命名不一致，并且 Excel 示例表格有列错位问题。修正这些问题后再作为最终对接契约会更安全。
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:19:### 问题1：class_name字段必填性不一致 [P2]
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:24:当宿舍系统不一定提供班级信息时，文件导入字段表已把 `class_name` 标为"否"（非必填），但 API 响应字段表只给 `bed_number` 标注了"可选"，会让接口实现方把 `class_name` 误认为必返字段。
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:35:### 问题2：Excel示例表格列错位 [P2]
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:40:在"李四"这一行，表头只有 10 列，但当前内容在 `否` 后面放了两个空单元格，导致该行变成 11 列，`未开始` 和备注列会错位；这也与下面的 CSV 示例不一致。
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:44:- 导入系统时可能解析失败或数据错位
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:51:### 问题3：系统设计文档字段命名不一致 [P2]
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:83:- ✓ 数据对接说明文档（文件导入部分）
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:84:- ✓ CSV模板文件
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:96:**P2级问题（必须修复）：**
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:103:2. 再修复问题1（必填性标注），确保接口契约清晰
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:129:1. 修复上述3个P2级问题
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:17:- **数据获取方式：** 通过宿管系统提供的数据库、API或CSV文件
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:67:**Codex意见：** 学生、辅导员、班级映射的"DB优先"改为"CSV/Excel优先，API/DB增强"。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:73:1. **实施周期：** CSV/Excel导入最快，DB直连需要安全审批和网络配置
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:75:3. **风险控制：** CSV导入可以先验证、再导入、可回滚；DB直连风险更高
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:76:4. **首版策略：** 先用CSV快速上线，后续根据数据变更频率决定是否升级为API/DB
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:82:| 学生基本信息 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先** / API或DB视图增强 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:83:| 辅导员基本信息 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先** / 人事或统一身份API增强 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:84:| 班级-辅导员对应关系 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:85:| 宿舍清退数据 | API优先 / DB备选 / CSV降级 | **保持不变**（API优先合理） |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:89:- 账号数据采用CSV首版，上线后根据实际变更频率决定是否升级
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:140:**后续增强方案（P1）：**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:173:**数据导入映射：**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:174:- 学生CSV：`student_id` → `users.student_id`
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:175:- 辅导员CSV：`employee_id` → `users.employee_id`
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:176:- 班级映射CSV：`counselor_employee_id` → 查询 `users` 表中 `employee_id` 匹配的记录
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:238:3. CSV导入时强校验：同一 `class_id` 不能出现多次
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:244:| 一班多辅导员 | 只导入主辅导员，其他辅导员不导入 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:248:**后续扩展方案（P1）：**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:264:**Codex结论：** P0数据源覆盖完整，未遗漏关键数据。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:269:- 图书馆清书、财务结清、学籍状态不列为P0是合理的
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:298:3. CSV需补充导入覆盖策略、重复数据处理、失败回滚
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:329:**CSV技术要求：**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:330:- 导入策略：首版采用**全量覆盖**（清空后重新导入）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:332:- 失败处理：导入前备份，失败后回滚到备份
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:333:- 校验报告：导入后生成校验报告（成功数、失败数、错误明细）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:353:| 学生账号 | 当届毕业生 | 1000人/届 | 只导入当届，历史届别不保留 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:390:9. 优先推荐的对接方式是什么？（DB直连 / API / CSV导入）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:392:11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:397:14. 是否需要导入手机号/邮箱用于找回密码或二次验证？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:411:2. 先落地CSV模板
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:412:3. 实现导入校验报告
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:427:**阶段2：CSV导入实现（2周）**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:428:1. 设计三份CSV模板：学生、辅导员、班级-辅导员映射
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:429:2. 实现CSV导入功能和校验逻辑
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:430:3. 生成导入校验报告（成功数、失败数、错误明细）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:440:2. 完成一次全量导入演练
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:455:1. 对接方式从"DB优先"改为"CSV/Excel首版优先，API/DB增强"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:461:7. 补充DB/API/CSV的技术要求细节
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:464:10. 调整实施路径（CSV优先，分阶段实施）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:479:- 调整对接方式优先级：学生/辅导员/班级映射改为"CSV/Excel首版优先"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:500:- 补充DB/API/CSV的具体技术要求
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:511:- 调整推荐方案：CSV首版优先
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:546:4. **实施路径：** 我们接受了CSV首版优先的建议，并补充了5阶段实施路径。Codex是否认同这个路径？是否有需要调整的地方？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:557:- **接受建议：** CSV首版优先、字段定义统一、补充实施细节
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:23:**Codex意见：** `PRIMARY KEY (student_id, employee_id, role)` 会让可空字段隐式非空，学生没有employee_id、辅导员没有student_id，导入会冲突。
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:41:1. 学生导入：`student_id='2022001', employee_id=NULL, role='student'` → 主键包含NULL，插入失败
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:42:2. 辅导员导入：`student_id=NULL, employee_id='T001', role='counselor'` → 主键包含NULL，插入失败
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:44:**修正方案：按导入类型拆分staging表**
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:47:-- 学生导入staging表
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:62:-- 辅导员导入staging表
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:71:-- 班级映射导入staging表
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:78:**导入流程调整：**
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:81:-- 1. 学生导入
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:96:-- 3. 软停用：本次未导入的学生
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:218:**Codex意见：** 主设计中 `users` 表有 `chk_auth_method` 约束，要求 `password_hash` 或 `wechat_openid` 非空；CSV预导入账号通常还没有密码或微信绑定，会被约束挡住。
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:231:CSV导入场景：
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:232:1. 学生CSV导入：只有学号、姓名等基本信息，没有密码或微信openid
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:235:**修正方案：调整认证约束，允许预导入账号**
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:259:    -- 修正后的认证约束：允许预导入账号
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:279:3. `password_setup_required = true`：预导入账号，待设置密码
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:281:**CSV导入时的处理：**
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:384:        raise ValueError(f"CSV校验失败，共 {len(errors)} 个错误")
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:450:1. **students_staging** - 学生导入临时表
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:451:2. **counselors_staging** - 辅导员导入临时表
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:452:3. **class_mapping_staging** - 班级映射导入临时表
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:455:6. **import_logs** - 导入审计日志表
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:469:3. ✅ 调整认证约束，增加password_setup_required支持CSV导入
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:37:- 系统崩溃风险
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:91:- 小程序：`<image lazy-load="true">`（原生懒加载）
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:136:P0: 核心业务逻辑（认证、审批、状态机）
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:137:P1: API端点（集成测试）
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:138:P2: 边界条件和异常处理
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:253:### P0 - 必须修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:256:### P1 - 强烈建议（影响质量）
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:261:### P2 - 可选优化
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:12:**方案名称：** Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:15:1. 用户主数据（学生、辅导员、班级映射）通过CSV导入到本地数据库
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:16:2. ImportSource接口用于数据导入，不是运行时查询
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:29:外部数据源 (CSV/API/Mock)
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:31:ImportSource (数据导入源接口)
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:33:ImportService (导入服务：校验、staging、upsert、软停用)
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:44:# 1. 数据导入源接口（用于导入，非运行时查询）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:46:    """用户数据导入源接口"""
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:49:        """获取学生数据用于导入"""
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:54:        """获取辅导员数据用于导入"""
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:59:        """获取班级映射数据用于导入"""
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:75:# 3. 导入服务
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:84:        # 2. 导入到staging表
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:93:        # 5. 软停用未导入的账号
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:149:USER_DATA_SOURCE = 'csv'  # 生产环境使用CSV导入
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:184:| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:185:| Week 2-3 | CSV导入功能、staging表、upsert逻辑、审计日志 | CSV导入模块、导入校验报告 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:188:| Week 8-9 | 前端开发 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:193:- 用户主数据API替换CSV（如需）：另计2-4周
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:199:1. **Week 1结束：** 数据契约冻结，接口定义完成
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:200:2. **Week 3结束：** CSV导入功能可用，种子数据就绪
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:254:- **更新策略：** 导入后清空缓存
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:306:| RealUserDataProvider运行时查询 | CSV导入到本地数据库 | 用户主数据是基础数据，不应依赖外部API |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:309:| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:310:| Provider用于运行时查询 | ImportSource用于数据导入 | 明确职责边界 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:314:1. **不要偏离已达成的共识** - 原方案错误地将用户主数据API化，偏离了CSV导入的共识
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:316:3. **Provider抽象层的用途是数据导入** - 不是运行时查询
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:327:- [ ] 数据契约文档
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:328:- [ ] CSV导入功能和校验逻辑
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:331:- [ ] 契约测试
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:340:- [ ] 数据导入审计日志完整
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:345:## 十、风险管理
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:347:### 10.1 已识别风险
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:349:| 风险 | 等级 | 缓解措施 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:351:| 真实API字段与Mock不一致 | P1 | Week 1冻结数据契约，预留扩展字段 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:352:| 真实API性能问题 | P1 | 缓存和重试机制 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:353:| 真实API数据结构差异大 | P2 | DTO适配层，预留2-3天调整时间 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:354:| API认证复杂度超预期 | P2 | 预留1-2天调试时间 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:358:- **API延期：** 首版坚持CSV导入，不等待API
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:360:- **数据质量问题：** 导入校验报告，人工审核
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:378:2. **Week 1启动：** 数据契约和接口设计
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:379:3. **Week 2-3：** CSV导入功能开发
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:15:最大风险不是“功能缺少”，而是设计文档和实施计划中仍存在多处与既定共识冲突的细节。如果直接按当前计划开工，容易把已经达成的 PostgreSQL 单数据库、单实例部署、文件安全、工作日计算、测试目标等决策重新做偏。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:168:## 6. 数据库设计风险
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:258:## 7. API 与业务流程风险
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:305:## 8. 认证与安全风险
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:314:- 小程序端结合静默刷新
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:352:## 9. 外部系统集成风险
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:377:### 9.3 宿舍系统字段契约不足
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:389:## 10. 部署设计风险
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:448:## 11. 性能与缓存风险
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:509:当前前端仅有空目录。设计计划同时做 React Native 和微信小程序，但需求里明确“挂在微信公众号”，小程序很可能是首要交付端。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:511:建议降低初期交付风险：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:513:1. 先确认首发端：微信小程序优先，React Native 后续。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:514:2. 先产出 OpenAPI/接口契约，避免两个前端各自猜接口。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:516:4. React Native 与小程序不要在第 8-9 周才开始完全介入，至少要在后端 API 定稿时同步验证登录和上传能力。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:522:### P0：开工前必须修正
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:531:### P1：Phase 1 应完成
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:539:### P2：业务模块实施前应定稿
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:545:5. 宿舍系统集成契约：状态码、超时、降级、人工跳过责任。
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:248:### P0 - 必须修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:251:### P1 - 强烈建议（影响质量）
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:252:2. 添加病毒扫描（安全风险）
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:256:### P2 - 可选优化
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:11:感谢Codex的详细审查。同意所有3个P2问题都需要修复，这些不一致会导致实际集成时出现问题。
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:19:**Codex指出：** API字段表未标注class_name为可选，与文件导入表不一致。
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:28:- 保持与文件导入字段表一致
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:103:   - [ ] 检查Excel/CSV示例格式正确
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:127:1. 立即修复3个P2问题
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:105:- 路径遍历风险
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:181:## 歧义风险
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:194:- 为什么需要React Native？微信小程序不够？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:57:- C. CSV/Excel文件导入（最快，首版推荐）
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:63:**问题11：** CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:65:**背景说明：** 系统采用"staging + upsert + 软停用"策略，本次未导入的账号自动标记为停用。
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:77:**背景说明：** 系统支持密码登录和微信登录，CSV导入的账号需要首次登录设置密码。
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:79:**问题14：** 是否需要导入手机号/邮箱用于找回密码或二次验证？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:97:首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:101:| 学生基本信息 | CSV/Excel导入 | 变更频率低（学期级），快速上线 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:102:| 辅导员基本信息 | CSV/Excel导入 | 约50人，变更频率低 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:103:| 班级-辅导员映射 | CSV/Excel导入 | 变更频率低，需强校验 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:130:**阶段2：CSV导入实现（2周）**
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:132:**目标：** 实现CSV批量导入功能
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:135:1. 设计三份CSV模板：
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:139:2. 实现CSV导入功能：
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:144:3. 实现导入审计日志
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:145:4. 生成导入校验报告：
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:156:- CSV导入功能模块
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:157:- 三份CSV模板文件
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:158:- 导入校验报告示例
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:159:- 导入操作手册
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:202:2. 完成一次全量导入演练：
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:203:   - 导入学生数据（约1000人）
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:204:   - 导入辅导员数据（约50人）
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:205:   - 导入班级映射数据（约50-100条）
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:223:- 全量导入演练报告
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:242:   - 如果变更频率低（每学期1-2次），保持CSV导入
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:251:   - 导入流程优化
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:268:| 阶段2 | 第2-3周 | CSV导入功能上线 | 成功导入测试数据，校验报告无异常 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:270:| 阶段4 | 第5周 | 上线前验收通过 | 全量导入成功，异常清单为空，功能测试通过 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:277:## 四、风险和应对
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:279:| 风险 | 影响 | 应对措施 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:282:| 班级映射数据不完整 | 高 | 导入时强校验，输出未映射班级清单，人工补充 |
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:55:**修改位置4：数据文件导入 - 字段定义表（第220-229行）**
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:67:**修改位置6：CSV格式示例**
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:69:CSV添加班级和床号列：
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:74:### 2.2 CSV模板文件（`docs/templates/宿舍清退数据模板.csv`）
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:76:更新CSV模板，添加班级和床号列，包含示例数据。
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:159:- ✓ CSV模板文件
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:231:### P0 - 必须修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:235:### P1 - 强烈建议（影响质量）
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:239:### P2 - 可选优化
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:15:| 学生基本信息 | P0 | 创建学生账号、身份识别、班级映射 | DB优先 / API备选 / CSV降级 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:16:| 宿舍清退数据 | P0 | 验证学生是否完成宿舍清退 | API优先 / DB备选 / CSV降级 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:17:| 辅导员基本信息 | P0 | 创建辅导员账号、审批权限 | DB优先 / API备选 / CSV降级 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:18:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | DB优先 / API备选 / CSV降级 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:19:| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:24:- **CSV降级**：当无法提供DB访问或API时，通过CSV文件导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:28:## 二、P0数据源详细要求
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:86:**对接方式3：CSV文件导入（降级）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:89:- 模板文件：`docs/templates/学生基本信息导入模板.csv`
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:137:**对接方式3：CSV文件导入（降级）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:183:**对接方式3：CSV文件导入（降级）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:186:- 模板文件：`docs/templates/辅导员基本信息导入模板.csv`
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:237:**对接方式3：CSV文件导入（降级）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:240:- 模板文件：`docs/templates/班级辅导员对应关系导入模板.csv`
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:243:- 导入后必须输出校验报告：
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:252:## 三、P1数据源（可选）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:266:**如需导入，字段要求：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:336:### 4.3 方式3：CSV文件导入（降级）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:353:1. 宿管系统方按模板导出CSV文件
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:355:3. 本系统导入并校验
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:356:4. 生成导入报告
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:360:- 文件格式：CSV
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:382:- CSV导入：建议每日更新，延迟不超过24小时
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:401:2. 学生基本信息：数据库直连或CSV导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:402:3. 辅导员信息：CSV导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:403:4. 班级-辅导员映射：CSV导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:409:2. 学生基本信息：CSV导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:410:3. 辅导员基本信息：CSV导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:411:4. 班级-辅导员对应关系：CSV导入（必须100%覆盖）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:434:### 7.3 CSV导入情况
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:435:1. 如果使用CSV导入，是否可以按模板定期导出数据？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:448:1. **宿管系统方**：反馈上述问题，提供数据库/API/CSV的可行性
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:451:4. **本系统方**：更新数据对接说明文档，提供CSV模板文件
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:141:#### CRITICAL - SQLAlchemy备选方案安全风险高
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:144:设计中提供SQLAlchemy直连外部数据库作为备选方案，但存在严重安全风险：
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:146:2. **SQL注入风险**：直接执行SQL语句
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:147:3. **数据一致性风险**：只读用户权限可能被滥用
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:151:- 安全风险极高
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:162:- 安全风险远大于便利性
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:242:### P0 - 必须修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:243:1. 删除SQLAlchemy备选方案（安全风险）
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:245:### P1 - 强烈建议（影响质量）
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:250:### P2 - 可选优化
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:55:这些是**设计方案本身**的实施风险：
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:61:| CRITICAL | SQLAlchemy备选方案安全风险 | 凭证泄露、SQL注入 |
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:141:### P0 - 立即修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:158:### P1 - 强烈建议（影响质量）
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:167:### P2 - 可选优化
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:230:- 优先级：P0
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:242:- 明确所有P0/P1修改项
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:250:**待修改文档项：** 7个（P0）+ 6个（P1）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:21:### 2.1 问题1：CSV导入策略错误（行329）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:23:**Codex意见：** "全量覆盖（清空后重新导入）"会导致外键约束冲突，必须改为"staging表 + upsert + 软停用"。
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:31:导入策略：首版采用**全量覆盖**（清空后重新导入）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:37:3. 无法区分"本次未导入"和"已停用"
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:44:-- 1. 创建staging表（临时表，每次导入前清空）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:54:-- 2. 导入CSV到staging表
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:67:-- 4. 软停用：本次未导入的账号标记为停用
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:78:- 学生账号：本次未导入 → `is_active=false`
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:79:- 辅导员账号：本次未导入 → `is_active=false`
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:80:- 管理员账号：不参与批量导入，手动管理
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:214:**CSV导入映射：**
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:216:学生CSV模板：
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:222:导入时：
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:287:学生导入时只导入当前批次：
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:289:-- 只导入is_graduating=true且graduation_year=2026的学生
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:295:### 3.2 导入审计
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:297:**问题：** 原文档提到"导入校验报告"，但未明确格式和存储。
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:301:导入日志表：
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:348:- 学生：本次CSV导入中未出现
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:349:- 辅导员：本次CSV导入中未出现
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:350:- 管理员：手动停用（不参与批量导入）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:353:- 下次CSV导入中重新出现 → 自动激活（`is_active=true`）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:413:   - `users_staging`：CSV导入临时表
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:415:   - `import_logs`：导入审计日志表
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:418:### 4.2 CSV导入策略修改（第三章3.3节）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:422:导入策略：首版采用**全量覆盖**（清空后重新导入）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:427:导入策略：**staging表 + upsert + 软停用**
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:428:1. CSV导入到临时staging表
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:430:3. 本次未导入的账号标记为 `is_active=false`
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:431:4. 下次导入重新出现时自动激活
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:446:**CSV技术要求：**
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:449:- 新增导入审计日志要求
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:453:**阶段2：CSV导入实现（2周）**
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:456:- 新增：实现导入审计日志
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:464:1. ✅ CSV导入从"全量覆盖"改为"staging + upsert + 软停用"
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:470:- 导入审计日志
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:138:- ❌ 学生身份验证：Phase 1不实施，依赖管理员导入用户
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:144:- 本系统是**内部系统**，用户由管理员导入，不是公开注册
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:145:- 学号枚举风险低（学号本就在校内公开）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:154:- 安全风险高
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:230:### P0 - 必须修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:233:### P1 - 强烈建议（影响质量）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:237:### P2 - 可选优化
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:45:- 确实存在账户接管风险
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:13:   - 对接方式：API接口 或 CSV文件导入
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:33:## 三、必需数据源（P0）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:56:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:78:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:102:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:124:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:151:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:161:## 四、可选数据源（P1）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:179:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:205:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:256:### P0（必需，系统无法运行）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:260:| 学生基本信息 | 教务系统 | API/CSV | ❌ 缺失 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:261:| 宿舍清退数据 | 宿管系统 | API/CSV | ✅ 已有 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:262:| 辅导员基本信息 | 人事系统 | API/CSV | ❌ 缺失 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:263:| 班级-辅导员对应关系 | 教务系统 | API/CSV | ❌ 缺失 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:265:### P1（可选，影响用户体验）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:270:| 图书馆清书状态 | 图书馆系统 | API/CSV | 手动上传截图 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:271:| 财务结清状态 | 财务系统 | API/CSV | 手动上传截图 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:291:- 🟡 **后果：** 需要学生自行注册，或手动导入
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:309:   - API接口 vs CSV文件导入
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:11:**结论：文档方向正确，P0 数据源基本完整；但不建议原样提交给用户。**
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:15:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:16:2. 对接方式里对学生、辅导员、班级映射默认写“DB 优先”偏激进。首版更合理的路径是：账号与映射数据优先 CSV/Excel 批量导入，宿舍清退优先 API。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:26:### 2.1 P0 数据源覆盖情况
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:28:当前 P0 数据源覆盖了系统运行所需的核心闭环：
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:36:| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:40:图书馆清书状态、财务结清状态、独立学籍状态没有列为 P0 是合理的。当前用户设计和系统设计仍保留截图上传、人工审核和宿舍系统异常时人工降级的方案，因此这三类不应阻塞首版上线。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:48:3. **账号标识映射。** 当前系统设计中的 `users.student_id` 被用作唯一登录标识，但共识文档给辅导员和管理员使用 `employee_id`。需要明确导入时 `employee_id` 映射到哪个内部字段，或后续模型是否新增统一的 `external_id/employee_id`。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:67:   如果登录只依赖学号密码和微信 OAuth，手机号可选合理；如果要支持短信验证、密码找回或紧急联系，手机号应至少在导入模板中强烈建议提供。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:83:   对 API 或 CSV 数据都建议记录外部系统数据更新时间，便于区分“未完成清退”和“数据过期/未同步”。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:87:字段基本可用，但有两个风险点：
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:90:   如果通知主要走微信，手机号可作为推荐字段而非硬性 P0。若学校确实要求短信/电话通知，则保留必填也合理。建议在文档中说明依据。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:102:2. **有效期字段。** `effective_term` 可选略弱，建议至少支持 `effective_start_date` / `effective_end_date` 或说明同一届首版只按当前有效映射导入。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:121:| 学生基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 首版优先，DB/API 作为条件成熟后的增强。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:122:| 宿舍清退数据 | API 优先 / DB 备选 / CSV 降级 | 合理。提交前置校验对实时性要求更高，API 价值最大。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:123:| 辅导员基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 或手动批量维护优先，人数少且变化低频。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:124:| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:129:DB、API、CSV 三种方式的技术要求整体清晰，但建议补充：
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:134:4. CSV 需补充导入覆盖策略：全量覆盖、增量更新、软删除/停用、重复数据处理、失败回滚。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:141:2. CSV 通过 SFTP 或后台上传时应限制权限，并记录上传人、文件哈希、导入批次和导入结果。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:160:1. 若系统只导入当届毕业生，1000 人规模合理。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:161:2. 若系统保留多届历史或提前导入低年级学生，容量应按 10,000 学生账号设计。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:168:当前问题覆盖了数据库、API、CSV 和数据范围，基本可用，但建议扩展为面向多方的数据确认清单。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:188:9. CSV 导入时是否采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:190:11. 是否有统一身份认证或微信绑定前置要求？是否需要导入手机号/邮箱用于找回密码或二次验证？
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:203:1. 宿舍清退：优先使用宿管系统 API；若不可用，使用每日 CSV 导入；异常时保留人工证明。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:204:2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:205:3. 辅导员信息：首版优先 CSV/Excel 或后台批量维护；若有统一身份或人事 API，再对接。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:206:4. 班级-辅导员映射：首版优先 CSV/Excel 强校验，上线前必须 100% 覆盖当届学生。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:221:2. 先落地三份基础 CSV/Excel 模板：学生、辅导员、班级-辅导员映射。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:222:3. 实现导入校验报告，重点校验学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:224:5. 上线前冻结当届数据批次，完成一次全量导入演练和异常清单清零。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:247:| 学生基本信息 | CSV/Excel 首版优先 / API 或 DB 视图增强 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:248:| 辅导员基本信息 | CSV/Excel 或后台批量维护首版优先 / 人事或统一身份 API 增强 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:249:| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:250:| 宿舍清退数据 | API 优先 / DB 只读视图备选 / CSV 降级 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:305:`31-data-source-requirements-consensus.md` 已经覆盖首版上线所需的主要 P0 数据源，字段设计也基本能支撑业务。它可以作为对接需求基础稿。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:310:2. 将学生、辅导员、班级映射的首版推荐方式从“DB 优先”调整为“CSV/Excel 优先，API/DB 增强”。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:14:1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:15:2. **首版不应追求所有数据源 API 化。** 对约 1000 名学生、约 50 名辅导员、约 5 名管理员的规模，CSV/Excel 批量导入加严格校验更现实；API 更适合作为后续自动化增强。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:21:### P0：上线必须具备
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:23:| 数据源 | 来源系统 | P0 判定 | 原因 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:25:| 学生基本信息 | 教务系统 | P0 | 用于创建学生账号、身份识别、展示院系专业班级、限定毕业离校申请人范围。用户设计说明书已出现“学号、姓名、专业、班级”和“批量导入学生用户”的要求，因此必须写入数据对接文档。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:26:| 辅导员基本信息 | 人事系统或人工台账 | P0 | 用于创建 counselor 账号和审批权限主体。实时同步不是 P0，但账号数据本身是 P0。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:28:| 宿舍清退数据 | 宿管系统 | P0 | 当前业务把宿舍清退作为提交前校验项，现有对接文档已覆盖。即使保留人工证明降级，正式流程仍应具备自动校验或批量数据导入能力。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:29:| 毕业资格/离校资格字段 | 教务系统 | P0 字段，非 P0 独立接口 | 如果系统只导入当届毕业生，可通过导入范围满足；如果导入全量学生，则必须在学生基本信息中带 `graduation_year`、`graduation_status` 或 `eligible_for_leave`。不建议首版单独建设学籍 API。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:31:### P1：可选增强
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:33:| 数据源 | 来源系统 | P1 判定 | 原因 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:35:| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:36:| 图书馆清书状态 | 图书馆系统 | P1 | 当前已有上传截图的人工方案。接口集成能降低审核成本和伪造风险，但不应阻塞首版上线。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:37:| 财务结清状态 | 财务系统 | P1 | 当前已有上传截图的人工方案。由于财务状态更敏感，若后续接口条件成熟，优先级可高于图书馆，但仍不是首版 P0。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:38:| 独立学籍状态接口 | 教务系统 | P1 | 只有在多届学生并行、延期毕业、结业/退学实时变化等需求明确时，才需要独立 API。首版可并入学生基础数据。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:46:| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:47:| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:48:| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:49:| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入、人工证明降级 | 当前文档策略合理。提交申请时实时性较强，API 价值高；若宿管系统暂不支持 API，则每日文件导入加人工证明降级。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:50:| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:51:| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 后续对接时只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，不要引入借阅明细。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:52:| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 后续对接时只返回是否结清和结清日期，不同步欠费明细；外部系统失败时保留人工审核通道。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:53:| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 首版不要单独拆接口。若后续存在延期毕业、结业、退学状态的实时变更，再建设独立同步。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:61:需要，且应列为 P0。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:67:首版推荐 CSV/Excel 批量导入，不推荐一开始就要求人事系统 API。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:71:### 3. 班级-辅导员对应关系是否应为 P0？
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:73:应为 P0，而且是当前缺口中风险最高的数据源。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:82:建议数据对接文档单独增加“审批关系数据”章节，并把导入覆盖率 100% 作为上线验收条件之一。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:88:约 5 人的规模下，真正重要的是权限授予、停用、密码重置、操作审计，而不是与人事系统同步。文档应说明由系统管理员在后台维护，不应把它列为 P0 数据接口。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:92:图书馆和财务可保持 P1。首版延续截图上传和人工审核，后续按审核量、造假风险、外部系统接口成熟度决定是否对接。若只能先选一个，建议先评估财务结清状态，因为财务数据的业务风险通常高于图书馆清书。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:102:2. **组织架构数据。** 院系、专业、年级不仅用于展示，也用于权限过滤、统计导出、异常排查。首版可随学生和辅导员数据导入，不必单独做组织架构接口。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:106:4. **导入校验和差异报告。** P0 数据导入不能只要求字段格式，还应要求失败明细、重复数据处理、覆盖策略、回滚策略和导入审计日志。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:116:9. **通知联系方式。** `phone`、`email` 对提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:128:2. **定义学生基本信息导入模板。** 先支持 CSV/Excel 导入当届毕业生，包含毕业资格字段和班级唯一标识。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:130:3. **定义辅导员基本信息导入模板。** 先确保 counselor 账号存在，且 `employee_id` 可被映射数据引用。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:132:4. **实现班级-辅导员映射导入。** 这是最关键步骤。上线前必须校验当届学生 100% 能解析到有效辅导员，否则不应开放提交。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:142:9. **补齐运营治理能力。** 包括导入审计、失败重试、差异报表、外部数据更新时间展示、人工改派、人工审核日志。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:150:1. 新增“学生基本信息导入”章节，提供 CSV/Excel 模板字段。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:151:2. 新增“辅导员基本信息导入”章节，明确 `employee_id`、联系方式和账号状态。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:152:3. 新增“班级-辅导员对应关系导入”章节，列为 P0，并写明覆盖率和异常报告要求。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:162:- **P0 数据：** 学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据、毕业资格字段。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:163:- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:164:- **首版策略：** 账号和映射数据用 CSV/Excel 批量导入，宿舍清退优先 API，管理员手动维护，图书馆/财务继续截图上传。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:165:- **最高优先级行动：** 立即补充班级-辅导员映射的数据规范和导入校验，这是自动审批闭环的关键缺口。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:17:1. 数据契约v0.1"现在"冻结的可行性
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:29:原方案A确实是"认证→申请→审批→附件→通知→前端→联调"的横向模块堆叠，风险在Week 8-10才暴露。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:33:- Week 2：CSV导入硬化
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:44:2-3人10周同时交付React Native和微信小程序不现实。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:47:- 首版：微信小程序（覆盖主要用户群）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:71:## 分歧点1：数据契约v0.1"现在"冻结
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:75:> 现在就应冻结v0.1：字段、枚举、样例CSV、错误码、前端API mock。Week 1用它跑纵向切片。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:79:**"现在"冻结数据契约v0.1的前提是什么？**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:84:3. 样例CSV从哪里来？是Mock数据还是需要真实样本？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:106:> Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:113:- 契约v0.1
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:123:1. **契约v0.1**：1-2天（定义字段、枚举、DTO）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:128:6. **Dorm Mock**：0.5天（Mock Provider、契约测试）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:140:  - 契约v0.1 + seed数据
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:160:> Week 4-6：前端并行开发，不等后端全完，先做微信小程序主流程，使用前端API mock。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:167:1. 后端API契约稳定（至少v0.2）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:179:- Week 3：后端API契约冻结v0.2，提供前端mock
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:193:Week 0-1：契约v0.1 + 纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:194:- 契约v0.1
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:205:- 定义数据契约v0.1范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:241:### 问题1：Week 1做数据契约太晚吗？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:252:- 单端（微信小程序）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:271:- Week 0（2-3天）：契约v0.1
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:278:### 1. 数据契约v0.1的范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:287:**我的倾向：** 选项A，Week 2扩展到v0.2。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:307:- API契约冻结v0.2
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:310:**我的倾向：** Week 4开始，但Week 3必须完成API契约冻结。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:323:1. 数据契约v0.1"现在"冻结的可行性和范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:328:- Week 0（2-3天）：定义并冻结契约v0.1
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:330:- Week 2（5天）：CSV导入 + 前端开始
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:97:- ⚠️ 安全风险 - 存储数据库凭证
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:167:### Option 2 (SQLAlchemy) - 有风险 ⚠️
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:35:**理由：** 与文件导入字段表保持一致，宿舍系统可能无法提供班级信息。
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:147:- ✓ `docs/数据对接说明文档.md` - 文件导入字段表
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:148:- ✓ `docs/templates/宿舍清退数据模板.csv` - CSV模板
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:160:**Codex审查：** 3个P2问题已全部修复  
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:5:**针对文档：** 47-contract-fixes-review-request.md  
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:6:**审查类型：** 契约修复验证
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:12:**结论：尚未完全达到可执行契约标准，但已经非常接近。**
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:14:4个修复方向都正确，且主要阻塞点已经明显收敛：契约正文现在只有5个HTTP路由，列表端点已移除；503 `PROVIDER_UNAVAILABLE`样例已补；登录响应的DTO子集问题已说明；原先“申请未完成却只做查询”的降级方向已被替换。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:18:1. **P1：错误样例未覆盖Section 3定义的全部错误码。**
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:19:2. **P1：降级方案仍有一句口径冲突，且Day 3提交未完成时的措辞不够可执行。**
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:20:3. **P2：计划文档仍混用“5个HTTP路由”和“4个API端点/能力”的口径；AuthUserDTO最好正式纳入Section 1。**
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:22:完成这些收尾后，可以冻结契约并开始Week 1工作。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:32:契约Section 4现在实际列出5个HTTP路由：
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:40:列表端点 `GET /api/applications` 已不在契约中。移除列表端点是合理的，因为v0.1纵向切片只需要“登录 -> 提交 -> 审批 -> 查询单个申请”，不需要审批队列或学生申请列表。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:54:契约已经新增503样例，且与宿舍清退外部服务不可用场景匹配：
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:70:如果v0.1目标是“前端可用mock跑通并处理错误态”，错误样例应至少覆盖Section 3列出的全部错误码。否则前端mock、契约测试和后端异常处理仍会自行发挥。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:90:原因是契约已经命名了 `AuthUserDTO`，但核心DTO章节没有定义它。对后端实现、前端类型生成、契约测试来说，正式定义比正文说明更可靠。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:94:**验证结果：方向正确，但风险表还需要改一句。**
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:98:但风险表仍写：
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:112:### P1：错误样例覆盖不完整
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:114:**位置：** `docs/contracts/contract-v0.1.md` Section 3和Section 6.2
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:118:**影响：** 前端mock、后端异常格式、契约测试无法完整对齐。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:135:### P1：降级条件仍有口径冲突
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:137:**位置：** `docs/plans/week-0-1-execution-plan.md` 风险2
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:141:**影响：** Day 3风险触发后团队不知道是保闭环，还是继续追两级审批。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:145:### P2：API端点术语仍不够统一
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:149:**问题：** 计划中“4个API端点”实际指4个核心能力或Day 3-4新增HTTP路由，不等于契约的5个HTTP路由。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:159:### P2：AuthUserDTO应正式定义
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:161:**位置：** `docs/contracts/contract-v0.1.md` Section 1
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:165:**影响：** 对人工阅读影响小，对类型生成和契约测试有轻微歧义。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:173:**当前状态：未完全达到可执行契约标准。**
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:175:不是因为方向错，而是因为仍有两个会影响执行验收的P1口径缺口：错误样例未全覆盖，降级风险表仍有冲突措辞。它们都属于半天内可以修完的收尾问题。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:177:**修完上述P1后：可以冻结contract-v0.1.md，并开始Week 1 Day 1工作。**
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:179:如果团队已经要启动Week 1，也可以先启动不受这些问题影响的Day 1-2工作：Django骨架、基础模型、seed、登录认证。但不建议在P1修完前把契约标记为Final并全面进入Day 3-4业务API实现。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:186:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:5:**审查范围：** 用户设计说明书、数据对接说明文档、CSV模板
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:13:发现 9 个主要问题，涉及文档一致性、安全设计、对接契约。CSV 格式本身无误。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:19:### 问题1：引用不存在的 Excel 模板文件 [P1]
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:36:### 问题2：引用不存在的 Postman 文件 [P2]
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:52:### 问题3：API 示例使用 HTTP 但安全要求 HTTPS [P1]
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:69:### 问题4：认证方式描述不够收敛 [P2]
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:84:### 问题5：数据脱敏与请求参数冲突 [P1]
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:94:对接方不清楚是否应该支持身份证号查询，可能导致隐私泄露风险。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:101:### 问题6：审批时限口径不一致 [P2]
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:118:### 问题7：初始密码为身份证后 6 位有安全风险 [P0]
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:123:初始密码为身份证后 6 位，弱口令风险高，且扩大身份证信息依赖。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:126:严重安全风险，容易被暴力破解。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:136:### 问题8：辅导员权限按"本年级"过粗 [P2]
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:153:### 问题9：容量指标与既有设计口径不一致 [P2]
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:175:## CSV 模板检查
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:187:- 明确 CSV 文件名规则
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:188:- 如果实际模板是 CSV，确保文档引用一致（已修复）

exec
/bin/bash -lc "rtk sed -n '1,240p' progress.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# TASK-20260530-07 Multi-Project Collaboration Pattern Progress

## 2026-05-30
- Loaded RTK rule, planning-with-files skill, collaboration protocol, Codex review protocol, current planning files, recent collaboration events, and state snapshot.
- Created fresh planning files for the four-project architecture and pattern analysis.
- Verified local Gemini CLI presence/version and read the existing Gemini invocation script.
- Loaded previous local Claude/Codex analyses and upstream GitHub pages for Dev Buddy, Claude-Team, cc-use-exp, and ShakaCode Claude+Codex guidance.
- Inspected `/home/caohui/projects/claude-codex-gemini-collab` skill project, protocol template, task/event/validate scripts, and confirmed missing `.codex-plugin/plugin.json`.
- Wrote `.omc/collaboration/artifacts/20260530-2251-codex-four-project-pattern-analysis.md`.
- Ran `.omc/collaboration/scripts/validate-journal.sh`; validation passed for 51 events, no duplicate IDs, matching `state.last_event_id`, and no residual locks.
- Did not append a collaboration event for this artifact because the current event logger would mark `artifact_created` as `in_progress` and risk misleading state during the existing TASK-20260530-06 ambiguity.

exec
/bin/bash -lc "rtk sed -n '1,220p' findings.md" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,220p' docs/contracts/contract-v0.1.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 数据契约 v0.1 Final - 最小可执行契约

**版本：** v0.1 Final  
**状态：** ✅ 已冻结（可执行契约标准）  
**冻结日期：** 2026-05-30  
**适用范围：** Week 1纵向切片  
**下一版本：** v0.2（Week 3）  
**Codex审查：** 通过（文档52）

---

## 1. 核心DTO

### 1.1 UserDTO

```python
@dataclass
class UserDTO:
    """用户数据传输对象"""
    user_id: str                      # 学号/工号
    name: str                         # 姓名
    role: UserRole                    # 角色：student/counselor/dean
    active: bool                      # 账号是否激活
    class_id: Optional[str] = None    # 班级ID（学生必填，教师为None）
    is_graduating: Optional[bool] = None  # 是否毕业生（仅学生）
    graduation_year: Optional[int] = None # 毕业年份（仅学生）
```

### 1.2 ApplicationDTO

```python
@dataclass
class ApplicationDTO:
    """离校申请数据传输对象"""
    application_id: str
    student_id: str
    student_name: str
    class_id: str
    reason: str                      # 申请理由
    leave_date: str                  # 计划离校日期 (YYYY-MM-DD)
    status: ApplicationStatus
    dorm_checkout_status: DormCheckoutStatus
    created_at: str                  # ISO8601
    updated_at: str
```

### 1.3 ApprovalDTO

```python
@dataclass
class ApprovalDTO:
    """审批记录数据传输对象"""
    approval_id: str
    application_id: str
    step: ApprovalStep           # counselor/dean
    approver_id: str
    approver_name: str
    decision: ApprovalDecision   # approved/rejected/pending
    comment: Optional[str]
    decided_at: Optional[str]    # ISO8601
```

### 1.4 DormCheckoutStatusDTO

```python
@dataclass
class DormCheckoutStatusDTO:
    """宿舍清退状态数据传输对象"""
    student_id: str
    status: DormCheckoutStatus   # completed/pending/not_started/unknown
    checked_at: Optional[str]    # ISO8601
    blocking_reason: Optional[str]
    provider_error_code: Optional[str]
```

---

## 2. 状态枚举

### 2.1 UserRole

```python
class UserRole(str, Enum):
    STUDENT = "student"
    COUNSELOR = "counselor"
    DEAN = "dean"
```

### 2.2 ApplicationStatus

```python
class ApplicationStatus(str, Enum):
    DRAFT = "draft"                      # 草稿
    PENDING_COUNSELOR = "pending_counselor"  # 待辅导员审批
    PENDING_DEAN = "pending_dean"        # 待学工部审批
    APPROVED = "approved"                # 已通过
    REJECTED = "rejected"                # 已驳回
```

### 2.3 ApprovalStep

```python
class ApprovalStep(str, Enum):
    COUNSELOR = "counselor"
    DEAN = "dean"
```

### 2.4 ApprovalDecision

```python
class ApprovalDecision(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
```

### 2.5 DormCheckoutStatus

```python
class DormCheckoutStatus(str, Enum):
    COMPLETED = "completed"          # 已清退
    PENDING = "pending"              # 清退中
    NOT_STARTED = "not_started"      # 未开始
    UNKNOWN = "unknown"              # 状态未知（API失败）
```

### 2.6 状态机契约

**申请状态流转规则：**

| 当前状态 | 触发动作 | 角色 | 下一状态 | 副作用 |
|---------|---------|------|---------|--------|
| - | 学生提交申请 | student | pending_counselor | 创建辅导员审批记录 |
| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
| pending_counselor | 辅导员驳回 | counselor | rejected | 无 |
| pending_dean | 学工部通过 | dean | approved | 无 |
| pending_dean | 学工部驳回 | dean | rejected | 无 |

**宿舍清退状态处理规则：**

| 宿舍状态 | 提交申请行为 | HTTP状态 | 错误码 |
|---------|------------|---------|--------|
| completed | 允许提交 | 201 | - |
| pending | 阻断提交 | 422 | DORM_BLOCKED |
| not_started | 阻断提交 | 422 | DORM_BLOCKED |
| unknown | 阻断提交 | 422 | DORM_BLOCKED |
| provider_unavailable | 阻断提交 | 503 | PROVIDER_UNAVAILABLE |

**角色权限矩阵：**

| 操作 | student | counselor | dean |
|------|---------|-----------|------|
| 提交申请 | ✓（仅自己） | ✗ | ✗ |
| 查看申请 | ✓（仅自己） | ✓（本班级） | ✓（所有） |
| 辅导员审批 | ✗ | ✓（本班级） | ✗ |
| 学工部审批 | ✗ | ✗ | ✓（所有） |

---

## 3. 错误码

### 3.1 业务错误 (4xx)

| 错误码 | HTTP状态 | 说明 | 示例场景 |
|--------|---------|------|---------|
| VALIDATION_ERROR | 400 | 请求参数校验失败 | 必填字段缺失、格式错误 |
| AUTH_REQUIRED | 401 | 未认证 | Token缺失或过期 |
| FORBIDDEN | 403 | 无权限 | 学生访问他人申请 |
| NOT_FOUND | 404 | 资源不存在 | 申请ID不存在 |
| CONFLICT | 409 | 资源冲突 | 重复提交申请 |
| DORM_BLOCKED | 422 | 宿舍清退未完成 | 提交申请时宿舍未清退 |

### 3.2 系统错误 (5xx)

| 错误码 | HTTP状态 | 说明 | 示例场景 |
|--------|---------|------|---------|
| PROVIDER_UNAVAILABLE | 503 | 外部服务不可用 | 宿舍清退API超时 |
| INTERNAL_ERROR | 500 | 内部错误 | 数据库连接失败 |

### 3.3 错误响应格式

```json
{
  "error": {
    "code": "DORM_BLOCKED",
    "message": "宿舍清退未完成，无法提交申请",
    "details": {
      "student_id": "2020001",
      "dorm_status": "pending"
    }
  }
}
```

---

## 4. API端点

### 4.1 认证

#### POST /api/auth/login

**请求：**
```json
{
  "user_id": "2020001",
  "password": "password123"
}
```

**响应：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "user": {
    "user_id": "2020001",
    "name": "张三",
    "role": "student",
    "class_id": "CS2020-01"

 succeeded in 129ms:
exec
/bin/bash -lc "rtk sed -n '220,520p' docs/contracts/contract-v0.1.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    "class_id": "CS2020-01"
  }
}
```

**说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。

### 4.2 申请

#### POST /api/applications

**请求：**
```json
{
  "reason": "毕业离校",
  "leave_date": "2024-06-30"
}
```

**响应：**
```json
{
  "application_id": "app_001",
  "student_id": "2020001",
  "student_name": "张三",
  "class_id": "CS2020-01",
  "reason": "毕业离校",
  "leave_date": "2024-06-30",
  "status": "pending_counselor",
  "dorm_checkout_status": "completed",
  "created_at": "2024-05-30T10:00:00Z",
  "updated_at": "2024-05-30T10:00:00Z"
}
```

#### GET /api/applications/{application_id}

**响应：**
```json
{
  "application_id": "app_001",
  "student_id": "2020001",
  "student_name": "张三",
  "class_id": "CS2020-01",
  "reason": "毕业离校",
  "leave_date": "2024-06-30",
  "status": "pending_counselor",
  "dorm_checkout_status": "completed",
  "approvals": [
    {
      "approval_id": "apv_001",
      "step": "counselor",
      "approver_id": "T001",
      "approver_name": "李老师",
      "decision": "pending",
      "comment": null,
      "decided_at": null
    }
  ],
  "created_at": "2024-05-30T10:00:00Z",
  "updated_at": "2024-05-30T10:00:00Z"
}
```

### 4.3 审批

#### POST /api/approvals/{approval_id}/approve

**请求：**
```json
{
  "comment": "同意离校"
}
```

**响应：**
```json
{
  "approval_id": "apv_001",
  "application_id": "app_001",
  "step": "counselor",
  "approver_id": "T001",
  "approver_name": "李老师",
  "decision": "approved",
  "comment": "同意离校",
  "decided_at": "2024-05-30T11:00:00Z"
}
```

#### POST /api/approvals/{approval_id}/reject

**请求：**
```json
{
  "comment": "材料不齐全"
}
```

**响应：**
```json
{
  "approval_id": "apv_001",
  "application_id": "app_001",
  "step": "counselor",
  "approver_id": "T001",
  "approver_name": "李老师",
  "decision": "rejected",
  "comment": "材料不齐全",
  "decided_at": "2024-05-30T11:00:00Z"
}
```

---

## 5. 样例数据

### 5.1 正常样本

**默认密码：** 所有账号默认密码为 `password123`

**学生（10人）：**
```python
students = [
    {"user_id": "2020001", "name": "张三", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020002", "name": "李四", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020003", "name": "王五", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020004", "name": "赵六", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020005", "name": "钱七", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020006", "name": "孙八", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020007", "name": "周九", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020008", "name": "吴十", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020009", "name": "郑十一", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020010", "name": "王十二", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
]
```

**辅导员（2人）：**
```python
counselors = [
    {"user_id": "T001", "name": "李老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
    {"user_id": "T002", "name": "王老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
]
```

**学工部（1人）：**
```python
deans = [
    {"user_id": "D001", "name": "赵主任", "role": "dean", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
]
```

**班级映射：**
```python
class_mappings = [
    {"class_id": "CS2020-01", "counselor_id": "T001"},
    {"class_id": "CS2020-02", "counselor_id": "T002"},
]
```

### 5.2 边界样本

**无班级映射：**
```python
{"user_id": "2020099", "name": "边界1", "role": "student", "class_id": "INVALID", "is_graduating": True, "graduation_year": 2024, "active": True}
```

**辅导员停用：**
```python
{"user_id": "T099", "name": "停用老师", "role": "counselor", "class_id": None, "active": False}
```

**非毕业生：**
```python
{"user_id": "2021001", "name": "边界2", "role": "student", "class_id": "CS2021-01", "is_graduating": False, "graduation_year": 2025, "active": True}
```

**延期毕业：**
```python
{"user_id": "2019001", "name": "边界3", "role": "student", "class_id": "CS2019-01", "is_graduating": True, "graduation_year": 2024, "active": True}
```

---

## 6. Mock响应

### 6.1 宿舍清退Mock

**DormCheckoutProvider Mock实现：**

```python
class MockDormCheckoutProvider:
    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
        # 固定返回规则（覆盖所有状态）
        mock_data = {
            "2020001": DormCheckoutStatusDTO(
                student_id="2020001",
                status=DormCheckoutStatus.COMPLETED,
                checked_at="2024-05-15T10:00:00Z",
                blocking_reason=None,
                provider_error_code=None
            ),
            "2020002": DormCheckoutStatusDTO(
                student_id="2020002",
                status=DormCheckoutStatus.PENDING,
                checked_at=None,
                blocking_reason="宿舍物品未清理",
                provider_error_code=None
            ),
            "2020003": DormCheckoutStatusDTO(
                student_id="2020003",
                status=DormCheckoutStatus.NOT_STARTED,
                checked_at=None,
                blocking_reason="未提交清退申请",
                provider_error_code=None
            ),
            "2020099": DormCheckoutStatusDTO(
                student_id="2020099",
                status=DormCheckoutStatus.UNKNOWN,
                checked_at=None,
                blocking_reason="学生信息不存在",
                provider_error_code="STUDENT_NOT_FOUND"
            ),
        }
        
        # 默认返回NOT_STARTED（而非completed，避免掩盖失败路径）
        return mock_data.get(student_id, DormCheckoutStatusDTO(
            student_id=student_id,
            status=DormCheckoutStatus.NOT_STARTED,
            checked_at=None,
            blocking_reason="未在宿舍系统中找到记录",
            provider_error_code=None
        ))
```

### 6.2 错误Mock

**400 Validation Error：**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": {
      "field": "leave_date",
      "reason": "离校日期不能早于今天"
    }
  }
}
```

**401 Unauthorized：**
```json
{
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "Token缺失或过期"
  }
}
```

**403 Forbidden：**
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "无权限访问此资源"
  }
}
```

**404 Not Found：**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "申请不存在",
    "details": {
      "application_id": "app_999"
    }
  }
}
```

**409 Conflict：**
```json
{
  "error": {
    "code": "CONFLICT",
    "message": "申请已存在，不能重复提交",
    "details": {
      "student_id": "2020001",
      "existing_application_id": "app_001"
    }
  }
}
```

**422 Dorm Blocked：**
```json
{
  "error": {

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/approvals/urls.py" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/urls.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
]

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/applications/urls.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.urls import path
from . import views

urlpatterns = [
    path('', views.applications_view, name='applications'),
    path('<str:application_id>/', views.get_application, name='get_application'),
]

 succeeded in 149ms:
exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/views.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import LoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

exec
/bin/bash -lc "rtk sed -n '1,320p' backend/apps/applications/views.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Application, ApplicationStatus, DormCheckoutStatus
from .serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationListSerializer
from .pagination import ApplicationLimitOffsetPagination
from .providers import MockDormCheckoutProvider
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.users.models import UserRole
from apps.users.class_mapping import ClassMapping
import uuid


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

    # Counselor: applications with own pending counselor approvals
    elif user.role == UserRole.COUNSELOR:
        pending_approvals = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR,
            decision=ApprovalDecision.PENDING
        ).values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=pending_approvals)

    # Dean: applications with own pending dean approvals
    elif user.role == UserRole.DEAN:
        pending_approvals = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DEAN,
            decision=ApprovalDecision.PENDING
        ).values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=pending_approvals)

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
        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以提交申请'}},
                        status=status.HTTP_403_FORBIDDEN)

    if Application.objects.filter(student=user).exists():
        existing = Application.objects.filter(student=user).first()
        return Response({'error': {'code': 'CONFLICT', 'message': '申请已存在，不能重复提交',
                                    'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id}}},
                        status=status.HTTP_409_CONFLICT)

    serializer = ApplicationCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
                                    'details': serializer.errors}},
                        status=status.HTTP_400_BAD_REQUEST)

    provider = MockDormCheckoutProvider()
    dorm_status = provider.check_status(user.user_id)

    if dorm_status.status != DormCheckoutStatus.COMPLETED:
        return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
                                    'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
                                                'blocking_reason': dorm_status.blocking_reason}}},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    try:
        class_mapping = ClassMapping.objects.get(class_id=user.class_id, active=True)
    except ClassMapping.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '班级映射不存在',
                                    'details': {'class_id': user.class_id}}},
                        status=status.HTTP_404_NOT_FOUND)

    application = Application.objects.create(
        application_id=f'app_{uuid.uuid4().hex[:8]}',
        student=user,
        student_name=user.name,
        class_id=user.class_id,
        reason=serializer.validated_data['reason'],
        leave_date=serializer.validated_data['leave_date'],
        status=ApplicationStatus.PENDING_COUNSELOR,
        dorm_checkout_status=dorm_status.status
    )

    Approval.objects.create(
        approval_id=f'apv_{uuid.uuid4().hex[:8]}',
        application=application,
        step=ApprovalStep.COUNSELOR,
        approver=class_mapping.counselor,
        approver_name=class_mapping.counselor_name,
        decision=ApprovalDecision.PENDING
    )

    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_application(request, application_id):
    try:
        application = Application.objects.get(application_id=application_id)
    except Application.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在',
                                    'details': {'application_id': application_id}}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user

    # Student: can only view own application
    if user.role == UserRole.STUDENT and application.student.user_id != user.user_id:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
                        status=status.HTTP_403_FORBIDDEN)

    # Counselor: can only view applications from assigned classes
    if user.role == UserRole.COUNSELOR:
        try:
            class_mapping = ClassMapping.objects.get(counselor=user, class_id=application.class_id, active=True)
        except ClassMapping.DoesNotExist:
            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
                            status=status.HTTP_403_FORBIDDEN)

    # Dean: can only view applications with own pending dean approvals
    if user.role == UserRole.DEAN:
        has_pending_approval = Approval.objects.filter(
            application=application,
            approver=user,
            step=ApprovalStep.DEAN,
            decision=ApprovalDecision.PENDING
        ).exists()
        if not has_pending_approval:
            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
                            status=status.HTTP_403_FORBIDDEN)

    return Response(ApplicationSerializer(application).data)

exec
/bin/bash -lc "rtk sed -n '1,360p' backend/apps/approvals/views.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from .models import Approval, ApprovalDecision, ApprovalStep
from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalListSerializer
from .pagination import ApprovalLimitOffsetPagination
from apps.applications.models import Application, ApplicationStatus
from apps.users.models import UserRole
import uuid


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

    # 辅导员: 只看自己的pending counselor审批
    if user.role == UserRole.COUNSELOR:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR,
            decision=ApprovalDecision.PENDING
        ).select_related('application', 'approver')

    # 学工部: 只看自己的pending dean审批
    elif user.role == UserRole.DEAN:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DEAN,
            decision=ApprovalDecision.PENDING
        ).select_related('application', 'approver')

    else:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # 排序
    queryset = queryset.order_by('-created_at', '-approval_id')

    # 分页
    paginator = ApprovalLimitOffsetPagination()
    page = paginator.paginate_queryset(queryset, request)

    # 序列化
    serializer = ApprovalListSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def approve_approval(request, approval_id):
    try:
        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
    except Approval.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)
    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.approver_id != user.user_id:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.decision != ApprovalDecision.PENDING:
        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
                        status=status.HTTP_409_CONFLICT)

    # Validate status/step matching
    application = approval.application
    if approval.step == ApprovalStep.COUNSELOR and application.status != ApplicationStatus.PENDING_COUNSELOR:
        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
                        status=status.HTTP_409_CONFLICT)
    if approval.step == ApprovalStep.DEAN and application.status != ApplicationStatus.PENDING_DEAN:
        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
                        status=status.HTTP_409_CONFLICT)

    serializer = ApprovalActionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
                        status=status.HTTP_400_BAD_REQUEST)

    approval.decision = ApprovalDecision.APPROVED
    approval.comment = serializer.validated_data.get('comment', '')
    approval.decided_at = timezone.now()
    approval.save()

    application = approval.application
    if approval.step == ApprovalStep.COUNSELOR:
        # Check for existing dean approval to prevent duplicates
        existing_dean_approval = Approval.objects.filter(
            application=application,
            step=ApprovalStep.DEAN
        ).exists()

        if existing_dean_approval:
            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
                            status=status.HTTP_409_CONFLICT)

        application.status = ApplicationStatus.PENDING_DEAN
        application.save()
        Approval.objects.create(
            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
            application=application,
            step=ApprovalStep.DEAN,
            approver_id='D001',
            approver_name='赵主任',
            decision=ApprovalDecision.PENDING
        )
    elif approval.step == ApprovalStep.DEAN:
        application.status = ApplicationStatus.APPROVED
        application.save()

    return Response(ApprovalSerializer(approval).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def reject_approval(request, approval_id):
    try:
        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
    except Approval.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)
    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.approver_id != user.user_id:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.decision != ApprovalDecision.PENDING:
        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
                        status=status.HTTP_409_CONFLICT)

    # Validate status/step matching
    application = approval.application
    if approval.step == ApprovalStep.COUNSELOR and application.status != ApplicationStatus.PENDING_COUNSELOR:
        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
                        status=status.HTTP_409_CONFLICT)
    if approval.step == ApprovalStep.DEAN and application.status != ApplicationStatus.PENDING_DEAN:
        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
                        status=status.HTTP_409_CONFLICT)

    serializer = ApprovalActionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
                        status=status.HTTP_400_BAD_REQUEST)

    approval.decision = ApprovalDecision.REJECTED
    approval.comment = serializer.validated_data.get('comment', '')
    approval.decided_at = timezone.now()
    approval.save()

    application = approval.application
    application.status = ApplicationStatus.REJECTED
    application.save()

    return Response(ApprovalSerializer(approval).data)

exec
/bin/bash -lc "rtk sed -n '520,760p' docs/contracts/contract-v0.1.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
  "error": {
    "code": "DORM_BLOCKED",
    "message": "宿舍清退未完成，无法提交申请",
    "details": {
      "student_id": "2020002",
      "dorm_status": "pending",
      "blocking_reason": "宿舍物品未清理"
    }
  }
}
```

**500 Internal Error：**
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "服务器内部错误",
    "details": {
      "error_id": "err_20240530_001",
      "message": "数据库连接失败"
    }
  }
}
```

**503 Provider Unavailable：**
```json
{
  "error": {
    "code": "PROVIDER_UNAVAILABLE",
    "message": "宿舍清退服务暂时不可用，请稍后重试",
    "details": {
      "student_id": "2020503",
      "provider": "dorm_checkout",
      "error": "Connection timeout"
    }
  }
}
```

---

## 7. 变更日志

### v0.1 (2026-05-30)

**初始版本 - 最小可执行契约**

**包含内容：**
- 核心DTO（User、Application、Approval、DormCheckoutStatus）
- 状态枚举（UserRole、ApplicationStatus、ApprovalStep、ApprovalDecision、DormCheckoutStatus）
- 错误码（8个核心错误码）
- API端点（认证、申请、审批、查询）
- 样例数据（正常样本 + 边界样本）
- Mock响应（宿舍清退Mock + 错误Mock）

**不包含内容（v0.2）：**
- 附件相关DTO和API
- 通知相关DTO和API
- 微信OAuth相关API
- 完整RBAC权限矩阵
- 审批转办、撤回、驳回重提

**验收标准：**
- 前端可用mock跑通登录→提交→审批→查询流程
- 后端可用seed数据跑通端到端测试

---

## 8. 使用说明

### 8.1 前端使用

**Mock Server配置：**
```javascript
// mock/handlers.js
export const handlers = [
  rest.post('/api/auth/login', (req, res, ctx) => {
    return res(ctx.json({
      access_token: 'mock_token',
      token_type: 'Bearer',
      user: {
        user_id: '2020001',
        name: '张三',
        role: 'student',
        class_id: 'CS2020-01'
      }
    }))
  }),
  // ... 其他端点
]
```

### 8.2 后端使用

**Seed数据加载：**
```bash
python manage.py seed_users
python manage.py seed_class_mappings
```

**端到端测试：**
```python
def test_application_flow():
    # 1. 学生登录
    response = client.post('/api/auth/login', {
        'user_id': '2020001',
        'password': 'password123'
    })
    token = response.json()['access_token']
    
    # 2. 提交申请
    response = client.post('/api/applications', 
        headers={'Authorization': f'Bearer {token}'},
        json={'reason': '毕业离校', 'leave_date': '2024-06-30'}
    )
    app_id = response.json()['application_id']
    
    # 3. 辅导员审批
    # 4. 学工部审批
    # 5. 查询状态
```

---

**契约负责人：** Claude Opus 4.7  
**前端Review：** 待确认  
**业务确认：** 待确认  
**冻结日期：** 2026-05-30  
**下一版本：** v0.2（Week 3）

codex
后端现在已经比 v0.1 契约多出列表能力：`GET /api/applications` 和 `GET /api/approvals` 都存在。这会影响窄切片范围，我会把“列表”纳入最小可用面，但控制成只读队列，不扩展复杂筛选。
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/week3-direction-2026-05-30/06-consensus.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Week 3工作方向 - 最终共识

**日期：** 2026-05-30  
**参与方：** Claude + Codex  
**状态：** 已达成共识

---

## 共识结论

**采用方案D：2天硬timebox + 明确闭环范围 + 决策门 + 可选P0修复日**

经过4轮讨论（Claude提案 → Codex审查 → Claude响应 → Codex反驳 → Claude认同），双方达成一致。

---

## 方案D详细内容

### Day 0：准备（不超过1小时）

**目标：** 明确环境策略和验收标准

**任务：**
1. 确认运行方式：
   - 优先级1：本机已有依赖，直接本地跑
   - 优先级2：数据库瓶颈，用Docker只起PostgreSQL，Django本地运行
   - 优先级3：Python/Django依赖瓶颈，补完整Docker Compose
2. 明确测试账号和seed数据需求：
   - 学生账号（至少2个，不同班级）
   - 辅导员账号（至少2个，对应不同班级）
   - 院长账号（1个）
   - 班级映射数据
3. 写下最小闭环验收清单（见下文验收标准）

### Day 1：跑通环境和最小闭环

**目标：** 暴露问题，建立可复现证据

**任务：**
1. 启动Django和数据库
2. 执行迁移（`python manage.py migrate`）
3. 导入或创建seed数据
4. 跑通完整闭环：
   - 学生登录
   - 学生提交申请
   - 辅导员审批
   - 院长审批
   - 学生查询状态
5. 记录所有阻塞项（不展开修非阻塞问题）

**输出：**
- 问题清单（按P0/P1/P2分类）
- 初步可复现步骤

### Day 2：只修P0并固化证据

**目标：** 修复阻塞问题，建立回归保护

**任务：**
1. 修复阻塞闭环的P0问题
2. 保留至少一个可复现验证入口：
   - smoke test脚本，或
   - API请求集合（Postman/curl），或
   - 清晰命令序列文档
3. 做一条负向权限验证（学生不能操作他人申请）
4. 输出问题清单和Week 3后续开发顺序

**输出：**
- 可复现验证脚本/文档
- P1/P2问题清单
- Week 3开发优先级

### 可选Day 3：仅在满足条件时启用

**启用条件：**
- 最小闭环已接近跑通
- 剩余问题是明确局部P0缺陷（非架构级）

**禁止条件：**
- 发现状态机、数据模型、契约冲突等架构级问题
- 此时应停止修补，暂停Week 3扩展开发，重做设计决策

---

## 最小闭环验收标准

**必须证明以下8项：**

1. **迁移成功执行**
   - `python manage.py migrate` 无错误
   - 所有表创建成功

2. **seed数据足以支持两级审批**
   - 至少2个学生（不同班级）
   - 至少2个辅导员（对应不同班级）
   - 1个院长
   - 班级映射关系正确

3. **登录后学生能提交申请**
   - JWT认证或项目实际使用的认证方式
   - 提交成功返回application_id

4. **辅导员能审批对应学生申请**
   - 辅导员只能看到自己班级的申请
   - 审批操作成功，状态转换正确

5. **院长能进行最终审批**
   - 院长能看到所有待审批申请
   - 审批操作成功，状态转换正确

6. **学生能查询最终状态**
   - 学生能查询自己的申请
   - 状态显示正确（draft/pending/approved/rejected）

7. **学生不能查询或操作他人申请**（负向权限验证）
   - 学生A尝试查询学生B的申请 → 403 Forbidden
   - 学生A尝试修改学生B的申请 → 403 Forbidden

8. **宿舍清退可用mock通过，但接口边界有记录**
   - MockDormCheckoutProvider返回固定值
   - 接口契约、失败分支、超时策略有占位定义

---

## 成功/失败标准

### 成功标准

**满足以下任一条件即为成功：**
1. 最小闭环可复现（8项验收标准全部通过）
2. 仅剩少量明确P0缺陷（已识别、已分类、有修复计划）

### 失败标准

**满足以下条件即为失败：**
- 发现架构级阻塞（状态机设计错误、数据模型根本缺陷、契约冲突）
- 此时应停止扩展开发，转入设计修正

### 禁止行为

**不允许：**
- 用"再延长一天"掩盖问题性质不清
- 把架构问题当作局部bug修补
- 跳过可复现验证直接进入Week 3

---

## 关键决策记录

### 1. Timebox目的

**不是**：保证在1-2天内修完所有问题  
**而是**：快速暴露事实、建立可复现证据、做出继续/降范围/重设计的决策

### 2. 环境策略

**不是**：Docker vs 本地二选一  
**而是**：渐进策略（本地 → Docker PostgreSQL → 完整Compose），目标是可复现运行

### 3. 问题分类

**不是**：独立半天做分类  
**而是**：伴随验证实时记录，Day 2结束时集中决策

### 4. 延期依据

**不是**：致命问题数量（>5个就延长）  
**而是**：问题性质（是否阻塞演示、是否需要改契约、是否影响核心数据模型）

---

## Codex补充的7个关键风险

**Claude原方案遗漏，Codex补充：**

1. **可验证证据标准**：不能只说"手动跑通"，必须有smoke test或命令记录
2. **测试数据/角色矩阵**：seed数据必须明确，否则卡在外键和角色上
3. **权限不是边界条件**：权限验证是核心安全契约，必须包含在最小闭环
4. **架构级问题处置门槛**：发现状态机或模型错误时，先判断是局部补丁还是契约重开
5. **回归保护**：Day 2修复后必须脚本化最小闭环，避免Week 3再次破坏
6. **宿舍清退mock风险**：Mock可以固定返回，但接口边界必须有占位定义
7. **迁移兼容性**：首次迁移可能暴露nullable、外键约束、枚举状态不一致

---

## 下一步行动

**立即执行：**
1. 开始Day 0准备（预计1小时内完成）
2. 检查本地环境（Python、PostgreSQL、Django）
3. 决定环境策略（本地/Docker PostgreSQL/完整Compose）
4. 列出seed数据需求
5. 创建最小闭环验收清单文档

**预期时间线：**
- Day 0：2026-05-30（今天）
- Day 1：2026-05-31
- Day 2：2026-06-01
- 决策点：Day 2结束时评估是否需要Day 3

---

## 讨论历史

1. **01-claude-proposal.md**：Claude提出3个方案（A继续开发/B暂停搭环境/C混合），倾向方案B
2. **02-codex-review.md**：Codex指出Claude过度简化问题，提出1-2天timebox稳定化冲刺
3. **03-claude-response.md**：Claude质疑timebox可行性，提出C-Modified（2-3天弹性timebox）
4. **04-codex-review-of-claude-response.md**：Codex指出Claude误读timebox目的，提出方案D（2天硬timebox + 决策门）
5. **05-claude-final-response.md**：Claude完全认同方案D，无需进一步修正
6. **06-consensus.md**（本文档）：双方达成最终共识

---

**共识状态：已确认**  
**执行状态：待开始Day 0**

exec
/bin/bash -lc "rtk sed -n '1,220p' tests/smoke_test.sh" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
#!/bin/bash
# Week 3 Day 1 Smoke Test - Minimum Viable Loop
# Base URL: http://localhost:8001 (Docker Compose)

set -e

BASE_URL="http://localhost:8001"

echo "=== Week 3 Day 1 Smoke Test ==="
echo "Base URL: $BASE_URL"
echo ""

# H1: Happy path (Class A)
echo "--- H1: Happy Path (2020001 → T001 → D001) ---"

# 1. Student login
echo "1. Student 2020001 login..."
STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020001","password":"2020001"}' \
  | jq -r '.access_token')

if [ -z "$STUDENT_TOKEN" ] || [ "$STUDENT_TOKEN" = "null" ]; then
  echo "✗ Student login failed"
  exit 1
fi
echo "✓ Student login success"

# 2. Submit application
echo "2. Submit application..."
APP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason":"毕业离校","leave_date":"2024-06-30"}')

APP_ID=$(echo "$APP_RESPONSE" | jq -r '.application_id')
APP_STATUS=$(echo "$APP_RESPONSE" | jq -r '.status')

if [ -z "$APP_ID" ] || [ "$APP_ID" = "null" ]; then
  echo "✗ Application submit failed"
  echo "$APP_RESPONSE" | jq '.'
  exit 1
fi

if [ "$APP_STATUS" != "pending_counselor" ]; then
  echo "✗ Application status wrong: $APP_STATUS (expected: pending_counselor)"
  exit 1
fi

echo "✓ Application submitted: $APP_ID (status: $APP_STATUS)"

# Extract counselor approval ID
COUNSELOR_APPROVAL_ID=$(echo "$APP_RESPONSE" | jq -r '.approvals[] | select(.step=="counselor") | .approval_id')

if [ -z "$COUNSELOR_APPROVAL_ID" ] || [ "$COUNSELOR_APPROVAL_ID" = "null" ]; then
  echo "✗ Counselor approval not created"
  exit 1
fi

echo "  Counselor approval: $COUNSELOR_APPROVAL_ID"

# 3. Counselor login
echo "3. Counselor T001 login..."
T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T001","password":"T001"}' \
  | jq -r '.access_token')

if [ -z "$T001_TOKEN" ] || [ "$T001_TOKEN" = "null" ]; then
  echo "✗ Counselor login failed"
  exit 1
fi
echo "✓ Counselor login success"

# 4. Counselor approve
echo "4. Counselor approve..."
APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$COUNSELOR_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $T001_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"同意"}')

APPROVE_DECISION=$(echo "$APPROVE_RESPONSE" | jq -r '.decision')

if [ "$APPROVE_DECISION" != "approved" ]; then
  echo "✗ Counselor approve failed"
  echo "$APPROVE_RESPONSE" | jq '.'
  exit 1
fi

echo "✓ Counselor approved"

# Verify application status changed
APP_STATUS_AFTER=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.status')

if [ "$APP_STATUS_AFTER" != "pending_dean" ]; then
  echo "✗ Application status not updated: $APP_STATUS_AFTER (expected: pending_dean)"
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

# 5. Dean login
echo "5. Dean D001 login..."
DEAN_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"D001","password":"D001"}' \
  | jq -r '.access_token')

if [ -z "$DEAN_TOKEN" ] || [ "$DEAN_TOKEN" = "null" ]; then
  echo "✗ Dean login failed"
  exit 1
fi
echo "✓ Dean login success"

# 6. Dean approve
echo "6. Dean approve..."
DEAN_APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$DEAN_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $DEAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"批准"}')

DEAN_DECISION=$(echo "$DEAN_APPROVE_RESPONSE" | jq -r '.decision')

if [ "$DEAN_DECISION" != "approved" ]; then
  echo "✗ Dean approve failed"
  echo "$DEAN_APPROVE_RESPONSE" | jq '.'
  exit 1
fi

echo "✓ Dean approved"

# 7. Verify final status
echo "7. Verify final status..."
FINAL_STATUS=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.status')

if [ "$FINAL_STATUS" != "approved" ]; then
  echo "✗ Final status wrong: $FINAL_STATUS (expected: approved)"
  exit 1
fi

echo "✓ Final status: $FINAL_STATUS"

echo ""
echo "--- N2: Cross-counselor approval (negative test) ---"

# N2: T002 tries to approve T001's approval (should fail)
echo "8. T002 login..."
T002_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T002","password":"T002"}' \
  | jq -r '.access_token')

if [ -z "$T002_TOKEN" ] || [ "$T002_TOKEN" = "null" ]; then
  echo "✗ T002 login failed"
  exit 1
fi
echo "✓ T002 login success"

# Login as student 2020002 (CS2020-02, counselor T002)
echo "9. Student 2020002 login..."
STUDENT2_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020002","password":"2020002"}' \
  | jq -r '.access_token')

if [ -z "$STUDENT2_TOKEN" ] || [ "$STUDENT2_TOKEN" = "null" ]; then
  echo "✗ Student 2020002 login failed"
  exit 1
fi
echo "✓ Student 2020002 login success"

# Create application for 2020002 (will be assigned to T002)
echo "10. Create application for 2020002..."
TEST_APP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $STUDENT2_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason":"测试跨班级审批","leave_date":"2024-06-30"}')

TEST_APP_ID=$(echo "$TEST_APP_RESPONSE" | jq -r '.application_id')
TEST_COUNSELOR_APPROVAL=$(echo "$TEST_APP_RESPONSE" | jq -r '.approvals[] | select(.step=="counselor") | .approval_id')

echo "  Test application: $TEST_APP_ID"
echo "  Test approval (T002): $TEST_COUNSELOR_APPROVAL"

# T002 tries to approve T001's approval
echo "10. T002 tries to approve T001's approval (should fail)..."
CROSS_APPROVE_STATUS=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/approvals/$COUNSELOR_APPROVAL_ID/approve/" \
  -H "Authorization: Bearer $T002_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"尝试跨班级审批"}' \
  | tail -1)

if [ "$CROSS_APPROVE_STATUS" != "403" ]; then
  echo "✗ Cross-counselor approve should return 403, got: $CROSS_APPROVE_STATUS"
  exit 1
fi

echo "✓ Cross-counselor approve blocked (403)"

echo ""
echo "=== All tests passed ==="

exec
/bin/bash -lc "rtk sed -n '1,220p' docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Week 3 Day 3 Planning Consensus

**Date:** 2026-05-30
**Participants:** Claude + Codex
**Status:** ✓ CONSENSUS REACHED

---

## Consensus Statement

**达成共识，可以执行。**

Claude's revised Day 3 plan is accepted. Claude has demonstrated true understanding of the core problems (Day 2 evidence drift, scope creep, permission risks). The revised plan addresses all critical issues raised in Codex's initial critique.

---

## Agreed Execution Plan

### Phase 0: Fix Day 2 Evidence Drift (30-60 min) - PRIORITY 1

**Tasks:**
1. Fix login URL in all Week 1 Day 5 tests
   - Change `/api/auth/login/` to `/api/auth/login` (remove trailing slash)
   - Files: test_application_flow.py, test_error_cases.py, test_rejection_flow.py
2. Fix `2020002` mock data to `completed` in providers.py
3. **[Codex addition]** Sync CSV template: Update students_template.csv line 3 to `CS2020-02`
4. Fix smoke_test.sh duplicate submission issue

**Acceptance:** All 12 tests passing + smoke script runs without errors

---

### Phase 1: Minimal List Endpoints (60-90 min) - PRIORITY 2

**Endpoints:**

1. `GET /api/approvals/` (PRIORITY 1)
   - Student: 403 Forbidden
   - Counselor: filter by `approver=user` **AND `decision=pending`** (Codex constraint)
   - Dean: filter by `approver=user` **AND `decision=pending`** (Codex constraint)
   
2. `GET /api/applications/` (PRIORITY 2)
   - Student: filter by `student=user`
   - Counselor: filter by `class_id` via ClassMapping
   - Dean: applications with own pending approvals (NOT all applications)
   - **[Codex constraint]** Sync Dean detail endpoint strategy or document as known risk

**Filtering:**
- Support `?status=` parameter
- **[Codex constraint]** Define `?status=pending` to map to both `pending_counselor` AND `pending_dean`
- Or use real enum values: `pending_counselor`, `pending_dean`, `approved`, `rejected`
- NO date range filtering
- NO sorting (default: created_at desc)

**Pagination:**
- Simple limit/offset (DRF default)
- Fixed limit: 20 items per page

**Serializers:**
- **[Codex constraint]** Use lean list serializer for applications
- Do NOT use full ApplicationSerializer with nested approvals
- Avoid expanding approval records exposure surface

**Response Format:**
```json
{
  "count": 10,
  "results": [...]
}
```

---

### Phase 2: Permission Isolation Tests (45-75 min) - PRIORITY 3

**Test Scenarios:**
1. Student cannot list others' applications
2. Counselor cannot list other counselors' approvals
3. Counselor cannot list applications from non-assigned classes
4. Dean cannot list other deans' approvals
5. List endpoints respect role-based filtering
6. **[Codex constraint]** Verify approvals list filters by decision=pending by default

**Acceptance:** All permission tests passing

---

### Phase 3: Smoke Test Update (30-60 min) - PRIORITY 4

**Changes:**
- Student submits application
- Counselor discovers approval via `GET /api/approvals/` (not from creation response)
- Counselor approves
- Dean discovers approval via `GET /api/approvals/` (not from creation response)
- Dean approves
- Student verifies final status

**Acceptance:** Smoke test passes using list endpoints for discovery

---

### Phase 4: Documentation (20-30 min) - PRIORITY 5

**Updates:**
- PROJECT-SUMMARY.md: Document Day 3 completion
- session-context.json: Update with Day 3 status
- Document remaining work: ClassMapping validation, advanced filtering, cursor pagination
- **[Codex constraint]** Document Dean detail endpoint permission as known risk if not fixed

---

## Time Estimate

**Codex-adjusted estimate:** 3-5 hours (not 3-4 hours)

**Breakdown:**
- Phase 0: 30-60 min
- Phase 1: 60-90 min
- Phase 2: 45-75 min
- Phase 3: 30-60 min
- Phase 4: 20-30 min

**Total:** 185-305 minutes (3-5 hours)

**Decision Gate:** After Phase 0, verify all 12 tests passing before proceeding to Phase 1

---

## Codex's 5 Implementation Constraints

### 1. Phase 0 Data Consistency

**Issue:** `2020002` is `CS2020-02` in seed_data but `CS2020-01` in CSV template.

**Action:** Sync students_template.csv line 3 to `CS2020-02`, or declare seed_data as sole acceptance source.

---

### 2. Status Filtering Semantics

**Issue:** `Application.status` values are `pending_counselor`/`pending_dean`/`approved`/`rejected`, not single `pending`.

**Action:** 
- Option A: Map `?status=pending` to both `pending_counselor` AND `pending_dean`
- Option B: Use real enum values directly

**Recommendation:** Option B (use real enum values) for clarity.

---

### 3. Permission Strategy Defenses

**Issue 1:** `GET /api/approvals/` should filter by `approver=user` AND `decision=pending` by default.

**Issue 2:** Dean detail endpoint (`GET /api/applications/{id}`) has no restrictions - falls through to return any application.

**Action:**
- Add `decision=pending` filter to approvals list
- Either fix Dean detail endpoint or document as known risk

---

### 4. Lean List Serializer

**Issue:** Current `ApplicationSerializer` includes nested approvals, expanding exposure surface.

**Action:** Create separate list serializer without nested approvals for `GET /api/applications/`.

---

### 5. Realistic Time Estimate

**Issue:** Claude's breakdown totals 185-305 minutes (3-5 hours), not 3-4 hours.

**Action:** Use 3-5 hour estimate. After Phase 0, decide whether to continue based on time remaining.

---

## Verification Evidence

Codex independently verified Claude's claims:
- Ran 12 tests in Docker: 1 failure, 7 errors (matches Claude's report)
- Root cause: Tests use `/api/auth/login/` but route is `/api/auth/login`
- Smoke script issue confirmed: Line 175 creates duplicate application

---

## Risk Mitigation

**Biggest Risk:** List endpoints reopening permission vulnerabilities.

**Mitigation Strategy:**
1. Queryset-level filtering (not Python filtering)
2. Explicit role checks (no default "show all")
3. Permission isolation tests
4. Never use `.all()` without immediate `.filter()`
5. Smoke test verification (T002 cannot see T001 data)
6. **[Codex addition]** Default filter approvals by `decision=pending`
7. **[Codex addition]** Use lean serializers to minimize exposure

---

## Next Steps

1. **Immediate:** Execute Phase 0 (fix Day 2 drift)
2. **Decision Gate:** Verify all 12 tests passing
3. **Then:** Execute Phase 1-4 per plan
4. **Final:** Document completion and remaining work

---

## Consensus Confirmation

**Claude:** Accepts Codex's 5 constraints and revised time estimate.

**Codex:** Accepts revised plan. No need for another planning round.

**Status:** Ready to execute.

---

exec
/bin/bash -lc 'rtk find . -maxdepth 4 -type f | rtk sort | rtk rg "(sample|response|响应|snapshot|contract-v0.2|v0.2|risk|风险|closure|闭环|known)"' in /home/caohui/projects/graduation-leave-system
 exited 1 in 109ms:
exec
/bin/bash -lc "rtk find . -maxdepth 3 -type f -name 'package.json' -o -name 'project.config.json' -o -name 'app.json' -o -name 'app.ts' -o -name 'app.js'" in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
rtk: rtk find does not support compound predicates or actions (e.g. -not, -exec). Use `find` directly.

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/approvals/serializers.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import serializers
from .models import Approval


class ApprovalListSerializer(serializers.ModelSerializer):
    """Lean serializer for approval lists - includes created_at"""
    application_id = serializers.CharField(source='application.application_id', read_only=True)
    approver_id = serializers.CharField(source='approver.user_id', read_only=True)

    class Meta:
        model = Approval
        fields = ['approval_id', 'application_id', 'step', 'approver_id',
                  'approver_name', 'decision', 'created_at']
        read_only_fields = ['approval_id', 'application_id', 'step',
                            'approver_id', 'approver_name', 'decision', 'created_at']


class ApprovalSerializer(serializers.ModelSerializer):
    application_id = serializers.CharField(source='application.application_id', read_only=True)
    approver_id = serializers.CharField(source='approver.user_id', read_only=True)

    class Meta:
        model = Approval
        fields = ['approval_id', 'application_id', 'step', 'approver_id',
                  'approver_name', 'decision', 'comment', 'decided_at']
        read_only_fields = ['approval_id', 'application_id', 'step',
                            'approver_id', 'approver_name', 'decision', 'decided_at']


class ApprovalActionSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False, allow_blank=True)

exec
/bin/bash -lc "rtk sed -n '220,360p' tests/smoke_test.sh" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/applications/serializers.py" in /home/caohui/projects/graduation-leave-system
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
    reason = serializers.CharField()
    leave_date = serializers.DateField()

exec
/bin/bash -lc "rtk rg --files | rtk rg '("'^|/)(package'"\\.json|project\\.config\\.json|app\\.(json|js|ts|vue)|pages\\.json)"'$|(''^|/)(frontend|miniprogram|mobile|web)(/|$)'"'" in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
codex
结论：小程序窄切片不要只做“能打开页面”的 skeleton。最小闭环应消费真实后端 API，证明 `登录 -> 列表发现 -> 详情查看 -> 关键动作 -> 状态刷新` 能跑通。

**1. 最小功能范围**

建议 Week 4 起步窄切片包含：

1. 小程序工程骨架  
   `app`、路由、基础布局、环境配置、构建脚本、类型约束。

2. API client  
   封装 `baseUrl`、JWT token 注入、401 处理、统一错误格式、loading/重试边界。不要让页面直接写 `wx.request`。

3. 登录页  
   先做账号密码登录：`POST /api/auth/login`。微信 OAuth 暂不进首个窄切片，否则会被小程序主体、备案、openid 绑定拖住。

4. 角色化首页  
   根据 `user.role` 分流：
   - student：我的申请
   - counselor：待我审批
   - dean：待我审批

5. 列表页  
   - student 调 `GET /api/applications/`
   - counselor/dean 调 `GET /api/approvals/`
   - 只做默认分页和空态，不做复杂筛选、搜索、统计。

6. 详情页  
   调 `GET /api/applications/{application_id}/`，展示申请状态、宿舍清退状态、审批记录。

7. 一个核心写动作  
   建议第一版加上审批通过：`POST /api/approvals/{approval_id}/approve/`。  
   驳回、学生提交申请可以放到第二小步，但不能拖太久，因为它们是核心流程。

我会把首个可验收目标定为：辅导员或学工部登录后，能从待审批列表进入详情并完成通过操作，状态刷新正确。

**2. 优先级顺序**

按这个顺序做：

1. 固定 API 契约快照  
   把 Week 3 的 10 个真实响应整理成前端 mock fixtures/type samples。先锁字段，再写 UI。

2. 搭工程 skeleton  
   只保留必要目录：`pages/login`、`pages/applications`、`pages/approvals`、`pages/detail`、`services/api`、`stores/auth`、`types/api`。

3. API client + auth store  
   这是地基。先完成 token 存储、请求头、错误归一化。

4. 登录页  
   用真实后端账号登录，不接微信 OAuth。

5. 待审批列表  
   优先做 `GET /api/approvals/`，因为它能支撑审批人员真实工作流。

6. 申请详情页  
   从审批列表拿 `application_id` 后进入详情。

7. 审批通过动作  
   完成后回到列表并刷新，验证 pending 项消失或状态变化。

8. 学生侧列表/详情  
   再补 student 视角，避免一开始同时做三套页面逻辑。

9. 学生提交、驳回、错误态完善  
   作为第二个窄切片。

**3. 技术选型**

建议：**原生微信小程序 + TypeScript**。

原因很直接：当前首版已经明确微信小程序优先，而且没有现成 React/Vue 前端代码可复用。原生小程序在登录、调试、上传、审核、微信能力接入上阻力最小。

不建议首版用 uni-app，除非已经确定后续必须多端复用。现在引入 uni-app 会多一层框架语义和构建问题，但短期收益不大。

不建议 Taro，除非团队已有 React/Taro 经验并且后续明确要复用到 H5/RN。否则它会把小程序窄切片变成前端框架工程。

**4. 开发环境配置要点**

开发工具：
- 微信开发者工具稳定版
- 启用 TypeScript
- 本地调试勾选“不校验合法域名”
- 后端本地服务保持固定地址，例如 `http://localhost:8001`

环境配置：
- `dev`：本地后端
- `mock`：使用 fixtures，不依赖后端
- `prod`：正式 HTTPS 域名

域名：
- 真机预览和体验版必须配置合法 HTTPS 域名。
- 本地 `localhost` 只适合开发者工具。
- 如果近期没有正式域名，先准备内网穿透或测试 HTTPS 域名，但不要把它写死在页面里。

mock 数据：
- 直接使用 Week 3 收集的真实响应。
- mock 要覆盖：登录成功、401、403、空列表、待审批列表、详情、审批成功、审批冲突。
- mock 字段必须和真实响应同名，不要为了前端方便另造模型。

**5. 前置准备工作**

启动前先完成这些，不然小程序会反复返工：

1. 冻结 v0.2 前端 API 表  
   至少列清楚：URL、method、请求体、响应体、错误码、分页格式、是否带尾斜杠。

2. 确认登录策略  
   首个切片用账号密码。微信登录/openid 绑定单独排期。

3. 明确测试账号  
   固定至少 4 个：`2020001`、`T001`、`T002`、`D001`，并保证 seed 可重复。

4. 明确列表语义  
   `GET /api/approvals/` 默认只返回 pending，这是小程序审批列表最需要的行为。

5. 建立前端验收脚本或手测清单  
   不需要一开始自动化很重，但必须能复现：
   登录 T001 -> 看待审批 -> 进详情 -> 通过 -> 列表刷新。

6. 记录已知风险  
   微信 OAuth、正式 HTTPS 域名、主体备案、真机网络、接口尾斜杠、分页字段、权限 403 展示，都要作为前端风险项管理。

我的建议是：第一天不要做漂亮 UI，先做“真实 API 可跑通的小程序壳”。只要 `登录 + 审批列表 + 详情 + 通过` 走通，小程序开发就从不确定性阶段进入可迭代阶段。
tokens used
77,085

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
