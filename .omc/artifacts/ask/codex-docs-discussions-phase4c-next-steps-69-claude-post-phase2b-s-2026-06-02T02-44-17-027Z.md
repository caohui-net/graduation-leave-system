# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-02T02:44:17.028Z

## Original task

docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md

## Final prompt

docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md

## Raw output

```text
已审查 [69-claude-post-phase2b-step1-next-strategy.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md)，并确认现有 [70-codex-post-phase2b-step1-next-strategy-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md) 可以作为 Codex 审查响应使用，无需改写。

核心结论：推荐 **B-mini -> 降级版 Option A**。先不要直接上 Celery/beat，也不要切换 Track；下一步应把审批超时提醒收窄为 `service + management command + tests`，实现一次性、幂等的 `APPROVAL_TIMEOUT_WARNING`，调度基础设施后置。

我验证了代码证据：`celery`/`redis` 只是依赖存在于 [base.txt](/home/caohui/projects/graduation-leave-system/backend/requirements/base.txt:15)，但 [docker-compose.yml](/home/caohui/projects/graduation-leave-system/docker-compose.yml:3) 只有 `db` 和 `backend`，settings 中也没有 Celery 配置；同时 `Notification` 已有超时枚举和幂等唯一约束，适合 Management Command 方案：[models.py](/home/caohui/projects/graduation-leave-system/backend/apps/notifications/models.py:14)、[models.py](/home/caohui/projects/graduation-leave-system/backend/apps/notifications/models.py:88)。


Reading additional input from stdin...
OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e8636-bdd8-7b63-9645-d5724ccccb92
--------
user
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md
codex
I’ll inspect the referenced document first, along with the project command rules, so I can understand what you want me to act on without guessing past the file content.
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
/bin/bash -lc "sed -n '1,260p' docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Post Phase 2B Step 1策略提案

**日期：** 2026-06-02  
**作者：** Claude  
**类型：** 下一步策略提案  
**状态：** 待Codex审查

---

## 当前状态

**已完成：** A-lite Step 1（Phase 2B契约修正）

**完成时间：** 约30分钟（2026-06-02 02:00-02:35）

**成果：**
- ✅ 删除DORM_CLEARANCE_BLOCKED（契约+代码+migration）
- ✅ 修正APPLICATION_SUBMITTED实体（approval）
- ✅ 强化测试断言（3个验证点）
- ✅ 文档同步（PROJECT-SUMMARY + session-context）
- ✅ Claude-Codex协作（65-68号文档，3轮共识）

---

## 待选策略

### Option A：继续A-lite Step 2（Phase 2B实现）

**范围：** 实现APPROVAL_TIMEOUT_WARNING通知（审批超时提醒）

**工作内容：**
1. 设计超时检测机制（Celery定时任务 vs Management Command）
2. 实现超时提醒服务层
3. 集成到现有审批流程
4. 编写测试（服务层 + API层）
5. 验证和文档

**预估时间：** 1-2小时

**优先级评估：**
- **业务价值：** 中（防止审批拖延，但非核心流程）
- **技术风险：** 中（需要定时任务基础设施）
- **复杂度：** 中高（涉及时间计算、工作日判断）

**问题：**
1. 超时提醒依赖定时任务（Celery或cron），但当前环境是否配置Celery？
2. 工作日计算需要节假日数据吗？
3. 提醒频率是单次还是重复？
4. 是否需要提醒历史记录？

---

### Option B：暂停Track 3，评估整体进度

**理由：**
1. Track 3已完成Phase 0（契约）、Phase 1（后端MVP）、Phase 2A（3种通知自动化）、Phase 2B Step 1（契约修正）
2. Phase 2B Step 2（审批超时）和Phase 2C需要定时任务基础设施
3. 可能值得评估是否优先解决其他阻塞问题

**评估点：**
- API Schema P1验证仍被环境阻塞（psycopg2-binary编译错误）
- WeChat DevTools仍未安装（Phase 4A/4C验收门控）
- 宿舍系统真实集成仍缺失联系人和API文档

**问题：**
- 这些阻塞是否比Phase 2B更优先？
- 还是应该继续完成Track 3的契约承诺（4种通知类型全部实现）？

---

### Option C：转向其他Track

**可选方向：**
1. **Track 1硬化：** CSV导入已完成，但可能有边界情况未覆盖
2. **Track 2硬化：** Docker/media/smoke已完成，但可能需要补充场景
3. **前端增强：** miniprogram可能有UX改进空间
4. **技术债：** backend.schema导入问题仍未根治

**评估：**
- 这些是否比完成Track 3通知系统更重要？

---

## 推荐策略

### Claude初步推荐：Option A（继续Phase 2B Step 2）

**理由：**
1. **契约承诺完整性：** notification-contract-v0.1.md定义了4种通知类型，目前已实现3种，只剩APPROVAL_TIMEOUT_WARNING
2. **最小化上下文切换：** 当前对通知系统的理解最深，切换到其他Track会损失上下文
3. **渐进式交付：** 即使审批超时提醒暂时无法在生产使用（缺定时任务），代码和测试仍有价值

**但有保留意见：**
1. **定时任务依赖：** 需要先调研当前环境Celery配置状态
2. **复杂度估算：** 1-2小时可能过于乐观，如果涉及工作日计算和节假日数据
3. **ROI疑问：** 审批超时提醒的业务价值是否足以支撑1-2小时投入？

---

## 审查要点

**请Codex审查以下问题：**

### 1. 优先级判断
- Option A（Phase 2B Step 2）vs Option B（暂停评估）vs Option C（转向其他Track），哪个更合理？
- 完成Track 3通知系统的完整性是否重要？
- 还是应该优先解决外部阻塞（DevTools/宿舍系统/环境问题）？

### 2. 技术可行性
- 当前环境是否配置Celery？如果没有，是否应该用Management Command代替？
- 审批超时提醒的实现复杂度是否被低估？
- 工作日计算是否需要节假日数据？如果需要，数据源在哪里？

### 3. 范围控制
- 如果选择Option A，Phase 2B Step 2的最小可行范围是什么？
- 是否可以简化为"N天后自动提醒一次"，不涉及工作日计算？
- 测试覆盖的最小标准是什么？

### 4. 替代方案
- 是否有其他更高价值的工作应该优先执行？
- 如果暂停Track 3，应该转向哪个方向？

### 5. 退出条件
- 如果Phase 2B Step 2遇到技术阻塞（如Celery未配置），是否应该果断暂停？
- 还是应该降级到"仅实现服务层+测试，不部署定时任务"？

---

## 期望输出

**Codex审查应包含：**
1. 推荐策略选择及理由
2. 技术可行性评估（Celery/定时任务）
3. 范围建议（最小可行vs完整实现）
4. 风险识别
5. 时间估算调整（如果需要）
6. 替代方案建议（如适用）

---

**文档编号：** 69  
**状态：** 待Codex审查

codex
The document is explicitly asking for a Codex review, so I need to follow the project’s review protocol before giving a recommendation. I’m reading that contract now and will then check the repo state relevant to Celery, notifications, and timeout feasibility.
exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .omc/collaboration/events.jsonl
 M .omc/collaboration/state.json
 M .omc/state/hud-stdin-cache.json
 M backend/apps/applications/providers.py
 M backend/apps/applications/tests/test_application_flow.py
 M backend/apps/applications/tests/test_constraints.py
 M backend/apps/applications/tests/test_error_cases.py
 M backend/apps/approvals/tests/test_permissions.py
 M backend/apps/approvals/tests/test_rejection_flow.py
 M backend/apps/approvals/tests/test_state_machine.py
 M frontend/services/api.ts
 M frontend/services/mock.ts
 M frontend/types/api.ts
 M tests/test_p0_fixes.sh
?? .claude/scheduled_tasks.json
?? .claude/scheduled_tasks.lock
?? .omc/artifacts/api-samples-v0.2.sh
?? .omc/artifacts/api-samples/
?? .omc/artifacts/ask/claude-response-phase2-approach-2026-05-31.md
?? .omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md
?? .omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md
?? .omc/artifacts/ask/codex-claude-docs-discussions-codex-review-2026-05-27-35-claude-re-2026-06-01T01-59-52-222Z.md
?? .omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md
?? .omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-implementation-o-2026-06-01T01-50-38-091Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-01-claude-phase4c-strate-2026-06-01T07-04-35-149Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-03-claude-response-to-co-2026-06-01T07-08-03-331Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-05-claude-next-steps-str-2026-06-01T07-43-59-071Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-08-claude-phase2-impleme-2026-06-01T08-18-49-202Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-11-claude-p1-fixes-revie-2026-06-01T09-07-37-351Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-14-claude-p1-implementat-2026-06-01T09-18-42-163Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-17-claude-p0-fix-verific-2026-06-01T09-57-25-216Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-17-18-356Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-34-claude-authorization--2026-06-01T15-56-02-973Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-48-37-499Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-47-claude-post-step2-nex-2026-06-01T17-43-18-137Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-47-claude-post-step2-nex-2026-06-01T17-57-59-267Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-47-claude-post-step2-nex-2026-06-01T18-03-30-703Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-50-claude-post-option-e--2026-06-01T18-13-55-411Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-52-claude-response-optio-2026-06-01T18-20-09-573Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-55-claude-post-api-schem-2026-06-01T18-53-35-201Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-58-claude-codex-consensu-2026-06-01T19-03-31-790Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md
?? .omc/artifacts/ask/codex-final-wording-fixes-complete-and-pushed-phase-4a-prep-docs-f-2026-05-31T03-34-09-147Z.md
?? .omc/artifacts/ask/codex-i-reviewed-your-phase-4a-readiness-repair-recommendation-com-2026-05-31T03-13-17-070Z.md
?? .omc/artifacts/ask/codex-i-reviewed-your-week-4-prep-bundle-recommendation-event-63-c-2026-05-30T20-55-24-390Z.md
?? .omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md
?? .omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md
?? .omc/artifacts/ask/codex-phase-1-a-skeleton-miniprogram-wechat-devtools-b-p0-1-applic-2026-05-30T18-57-33-443Z.md
?? .omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md
?? .omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md
?? .omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-43-29-691Z.md
?? .omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md
?? .omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md
?? .omc/artifacts/ask/codex-phase-4a-blocked-on-phase4a-waiting-for-devtools-phase-4b-ph-2026-06-01T01-33-23-790Z.md
?? .omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md
?? .omc/artifacts/ask/codex-phase-4b-prep-note-complete-and-pushed-you-said-hard-stop-on-2026-05-31T03-47-21-588Z.md
?? .omc/artifacts/ask/codex-phase-4b-role-guard-ts-date-ts-p0-ui-phase-4a-wechat-devtool-2026-06-01T03-32-12-743Z.md
?? .omc/artifacts/ask/codex-phase-4b-student-application-miniprogram-pages-student-appli-2026-06-01T02-23-37-379Z.md
?? .omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md
?? .omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-27-45-286Z.md
?? .omc/artifacts/ask/codex-student-application-api-createdefaultapiclient-reason-leave--2026-06-01T01-42-06-938Z.md
?? .omc/artifacts/ask/codex-user-instruction-repeated-continue-discussing-next-steps-fin-2026-05-31T03-57-31-643Z.md
?? .omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md
?? .omc/artifacts/ask/codex-week-3-complete-need-next-phase-strategy-discussion-complete-2026-05-30T20-23-08-920Z.md
?? .omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md
?? .omc/artifacts/ask/codex-week-4-consensus-reached-but-execution-blocked-on-external-d-2026-05-30T20-33-00-011Z.md
?? .omc/artifacts/ask/codex-week-4-consensus-reached-but-execution-blocked-on-external-d-2026-05-30T20-42-36-193Z.md
?? .omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md
?? .omc/collaboration/artifacts/20260601-1817-codex-events-jsonl-repair.md
?? .omc/collaboration/task-2-consensus.md
?? .omc/collaboration/task-3-consensus.md
?? .omc/collaboration/task-4-consensus.md
?? .omc/project-memory.json
?? .omc/sessions/
?? .omc/state/agent-replay-1975d66f-d9f9-404a-aee5-c702658630c2.jsonl
?? .omc/state/checkpoints/
?? .omc/state/last-tool-error.json
?? .omc/state/mission-state.json
?? .omc/state/sessions/1975d66f-d9f9-404a-aee5-c702658630c2/
?? .omc/state/sessions/4aad264e-c3a4-460a-9be1-61247202bad3/
?? .omc/state/sessions/7afec07d-3b40-4e4c-8f86-86e9dc0e791c/
?? .omc/state/sessions/97c93024-a4c1-4e03-93bf-7522ce3517ff/
?? .omc/state/sessions/c8f47bca-464c-4b8c-bab5-42ba59354101/
?? .omc/state/sessions/dcf39a3e-1b72-449a-9897-852c3c7f1253/
?? .omc/state/sessions/e2566739-aaa7-4701-9354-a710639ac308/
?? .omc/state/sessions/f91e1567-b1b2-4cc2-bd9b-355702bc1ec4/
?? .omc/state/subagent-tracking.json
?? backend/.omc/
?? backend/app
?? backend/apps/approvals/validators.py
?? backend/docs/
?? "docs/api\350\257\264\346\230\216.txt"
?? docs/contracts/contract-v0.2.md
?? docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md
?? docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md
?? docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md
?? docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md
?? docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md
?? docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md
?? docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md
?? docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md
?? docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md
?? docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md
?? docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md
?? docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md
?? docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md
?? docs/discussions/codex-review-2026-05-27/21-final-consensus.md
?? docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md
?? docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
?? docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md
?? docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
?? docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md
?? docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md
?? docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md
?? docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md
?? docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md
?? docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
?? docs/discussions/phase4c-next-steps/19-claude-next-phase-strategy-request.md
?? docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md
?? docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md
?? docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md
?? docs/discussions/phase4c-next-steps/30-claude-consensus-contract-revision-gate.md
?? docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md
?? docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md
?? docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md
?? docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md
?? docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md
?? docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md
?? docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md
?? docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md
?? docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md
?? docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md
?? docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md
?? docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md
?? docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md
?? docs/discussions/phase4c-next-steps/53-codex-confirmation-option-a-corrected.md
?? docs/discussions/phase4c-next-steps/54-claude-codex-consensus-option-a-execution.md
?? docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/59-claude-codex-final-consensus-option-2.md
?? docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md
?? docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md
?? docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md
?? docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
?? docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md
?? docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md
?? docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md
?? docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md
?? docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md
?? docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md
?? docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md
?? docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md
?? docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md
?? docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md
?? docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md
?? docs/discussions/week3-day1-review-2026-05-30/09-codex-execution-review.md
?? docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md
?? docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md
?? docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md
?? docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md
?? docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md
?? docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md
?? docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md
?? docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md
?? docs/discussions/week3-day1-review-2026-05-30/19-claude-deadlock-analysis.md
?? docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md
?? docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md
?? docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md
?? docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md
?? docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md
?? docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260528210617_553_47.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260528210618_554_47.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260528210619_555_47.jpg"
?? findings.md
?? miniprogram/.omc/
?? progress.md
?? task_plan.md
?? "\346\257\225\344\270\232\347\246\273\346\240\241\347\263\273\347\273\237\347\224\250\346\210\267\346\226\207\346\241\243.zip"
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Codex审查流程指南

**版本：** v2.0  
**更新日期：** 2026-05-28  
**适用范围：** 使用 `/oh-my-claudecode:ask codex` 进行文档审查

---

## Load Trigger (懒加载条件)

Read this file when ANY of these occur:
- 技术文档审查（Technical design documents）
- 数据库变更（Database schema changes）
- API设计（API interface design）
- 数据对接方案（Data integration plans）
- 系统架构调整（System architecture updates）
- 用户要求与Codex对话（User requests Codex review）

---

## 一、流程概述

本指南定义了与Codex进行对话式审查的标准流程，使用OMC内置的`/oh-my-claudecode:ask`技能。

**核心原则：**
- 使用统一的`/oh-my-claudecode:ask codex`方式
- 结构化的审查请求
- 批判性分析Codex建议
- 迭代式达成共识

---

## 二、完整流程（7步）

### 第1步：创建审查请求文档

**文件命名：** `XX-[主题]-review-request.md`

**文档结构：**
```markdown
# [主题] - Codex审查请求

**审查日期：** YYYY-MM-DD
**审查类型：** [类型]
**审查范围：** [范围]

## 一、背景/需求
[说明审查背景和目的]

## 二、已完成的工作
[列出已完成的修改]

## 三、审查要点
[列出需要Codex关注的具体问题]

## 四、潜在问题
[列出已知的潜在问题]

## 五、期望输出
1. 审查结论：通过/需要修改/不建议
2. 问题清单
3. 修复建议
4. 最终方案
```

---

### 第2步：调用Codex审查

**使用OMC内置技能：**
```
/oh-my-claudecode:ask codex "审查 docs/discussions/[路径]/XX-[主题]-review-request.md - [具体审查要求]"
```

**示例：**
```
/oh-my-claudecode:ask codex "审查 docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md - 这是我们对你第二轮审查的回应。请确认：1) 3个关键修正方案是否可行 2) 5个补充细节是否完整 3) 数据库模型调整方案是否有遗漏 4) 是否可以基于此创建v2共识文档"
```

**优点：**
- 自动保存结果为artifact：`.omc/artifacts/ask/codex-*.md`
- 统一的调用接口
- 更好的错误处理

---

### 第3步：保存Codex审查结果

**文件命名：** `XX+1-[主题]-codex-response.md`

**从artifact中提取关键内容：**
- 审查结论
- 发现的问题（按优先级分类）
- 具体修复建议
- 代码示例

**文档结构：**
```markdown
# [主题] - Codex审查响应

**审查日期：** YYYY-MM-DD
**审查人：** Codex
**Artifact路径：** .omc/artifacts/ask/codex-[timestamp].md

## 审查结论
[总体评价]

## 发现的问题

### 问题1：[标题] [优先级]
**位置：** 文件:行号
**问题描述：** [详细说明]
**影响：** [影响分析]
**修复建议：** [具体方案]

[重复其他问题]

## 审查通过的部分
[列出做得好的地方]
```

---

### 第4步：Claude响应Codex审查

**文件命名：** `XX+2-[主题]-claude-response.md`

**文档结构：**
```markdown
# [主题] - Claude响应

**响应日期：** YYYY-MM-DD
**针对：** Codex审查响应

## 对Codex审查的回应
[总体回应]

## 问题确认与修复方案

### 问题1：[标题]
**Codex指出：** [问题描述]
**Claude确认：** [确认分析]
**修复方案：** [具体方案]

[重复其他问题]

## 修改清单
[列出立即执行的修改]
```

---

### 第5步：执行修复

**按优先级修复：**
1. P0/CRITICAL问题 - 必须立即修复
2. P1/MAJOR问题 - 应该修复
3. P2/MINOR问题 - 可选修复

**修复后验证：**
- 使用Read工具验证修改正确
- 检查所有相关文档一致性

---

### 第6步：创建共识文档

**文件命名：** `XX+3-[主题]-consensus.md`

**文档结构：**
```markdown
# [主题] - 最终共识

**日期：** YYYY-MM-DD
**参与方：** Codex + Claude

## 审查结论
**状态：** 已修复/通过

## 已完成的修复
[列出所有修复，包含修改前后对比]

## 最终方案
[总结最终达成的方案]

## 文档一致性确认
[确认所有相关文档已更新]
```

---

### 第7步：归档到项目文档

**更新以下文件：**
1. `docs/PROJECT-SUMMARY.md` - 添加审查记录
2. `.omc/session-context.json` - 更新completed和artifacts
3. Git commit + push

---

## 三、讨论原则

### 1. 批判性思维
- **不要急于认同：** 收到Codex审查后，仔细分析每个问题
- **合理质疑：** 如果Codex建议不合理，在Claude响应中说明理由
- **深入分析：** 不只看表面问题，分析根本原因和影响范围

### 2. 迭代式讨论
- **不局限一次：** 如果修复后发现新问题，可再次提交Codex审查
- **及时发现问题：** 修复过程中发现不一致，立即记录
- **多轮达成共识：** 复杂问题可能需要2-3轮讨论才能完全解决

### 3. 分段处理
- **大篇幅分章节：** 超过500行的文档，按章节分别审查
- **分批修复：** 问题多时，按优先级分批修复和验证
- **渐进式共识：** 每个章节达成共识后再进入下一章节

---

## 四、文件编号规则

**连续编号：**
- XX号：审查请求
- XX+1号：Codex响应
- XX+2号：Claude响应
- XX+3号：最终共识

**示例：**
- 34-codex-second-review-response.md（审查请求）
- 35-response-to-codex-critical-issues.md（Claude响应）
- 36-data-confirmation-and-implementation.md（共识文档）

---

## 五、验证清单

**审查前：**
- [ ] 审查请求文档结构完整
- [ ] 审查范围明确
- [ ] 期望输出清晰

**审查中：**
- [ ] `/oh-my-claudecode:ask codex`调用成功
- [ ] Artifact已生成
- [ ] 问题优先级明确

**审查后：**
- [ ] 所有问题已修复
- [ ] 文档一致性已验证
- [ ] 项目文档已更新
- [ ] Git已提交推送

---

## 六、关键要点

### ✓ 成功要素
- 审查请求文档要详细、结构化
- 使用`/oh-my-claudecode:ask codex`（不是直接调用CLI）
- Claude响应要具体、可执行、有批判性分析

exec
/bin/bash -lc "rtk sed -n '1,260p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Claude-Codex Collaboration Protocol

Version: 0.3
Status: active
Owner: Claude + Codex

## 1. Purpose

This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.

Agents must read this file before participating in the collaboration workflow.

## 2. Directory Layout

All collaboration files live under `.omc/collaboration/`.

- `protocol.md`: this protocol.
- `state.json`: current shared workflow state.
- `events.jsonl`: append-only event log.
- `tasks/`: task specifications and task handoff documents.
- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
- `locks/`: lock files or directories for serialized work.
- `codex-ready.md`: Codex readiness signal.

Filesystem requirements:

- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
- Local filesystems and NFSv4 are acceptable for this workflow.
- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
- Production testing MUST NOT proceed on an unsupported filesystem.

## 3. Authority And Conflicts

This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.

If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.

Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.

## 4. Shared State

`state.json` is the latest compact state snapshot. It must remain valid JSON.

`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.

Recommended schema:

```json
{
  "workflow_id": "claude-codex-collab-mvp",
  "current_task": null,
  "active_agent": "none",
  "status": "initialized",
  "last_event_id": 0,
  "updated_at": "2026-05-30T00:00:00.000Z"
}
```

Field meanings:

- `workflow_id`: stable collaboration workflow identifier.
- `current_task`: active task id or `null`.
- `active_agent`: `claude`, `codex`, or `none`.
- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
- `last_event_id`: numeric id of the last event written to `events.jsonl`.
- `updated_at`: UTC ISO-8601 timestamp for the state update.

State updates should be minimal and should not replace durable task or artifact content.

State write rules:

- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
- Agents MUST validate the temporary file as well-formed JSON before publishing it.
- Agents MUST atomically rename the validated temporary file into place with `mv`.
- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.

## 5. Event Log

`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.

Required event fields:

```json
{
  "id": 1,
  "type": "codex_ready",
  "agent": "codex",
  "timestamp": "2026-05-30T00:00:00.000Z",
  "summary": "Short event summary."
}
```

Recommended optional fields:

- `task_id`: related task id.
- `artifacts`: array of artifact paths.
- `status`: resulting workflow status.
- `details`: compact structured metadata.

Event id rules:

- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
- New event ids MUST be allocated while holding `locks/journal.lock`.
- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.

Common event types:

- `claude_ready`
- `codex_ready`
- `task_created`
- `task_claimed`
- `artifact_created`
- `handoff_requested`
- `review_requested`
- `blocked`
- `completed`

## 6. Tasks

Task documents belong in `.omc/collaboration/tasks/`.

Recommended task filename:

```text
TASK-YYYYMMDD-NN-short-name.md
```

Recommended task content:

- Task id.
- Owner or requesting agent.
- Objective.
- Scope.
- Inputs and relevant files.
- Expected outputs.
- Constraints and mandatory rules.
- Acceptance criteria.
- Current status.

When claiming a task, the agent MUST use this atomic claim procedure:

1. Acquire `locks/journal.lock`.
2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.

## 7. Artifacts

Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.

Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.

Recommended artifact filenames:

```text
YYYYMMDD-HHMM-agent-topic.md
```

For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.

## 8. Locks

Locks are files or directories under `.omc/collaboration/locks/`.

Use a lock when two agents might modify the same shared collaboration file at the same time.

Recommended lock filename:

```text
resource-name.lock
```

Recommended lock content:

```json
{
  "agent": "codex",
  "resource": "state.json",
  "created_at": "2026-05-30T00:00:00.000Z",
  "reason": "Updating state after event append."
}
```

Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.

### Required Journal Lock

Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.

Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:

```bash
mkdir .omc/collaboration/locks/journal.lock
```

The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.

The lock directory MUST contain `owner.json`:

```json
{
  "agent": "codex",
  "task_id": "TASK-20260530-01",
  "created_at": "2026-05-30T08:00:00.000Z",
  "heartbeat_at": "2026-05-30T08:00:00.000Z",
  "reason": "append event and update state"
}
```

The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.

## 9. Failure Recovery

Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.

If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.

If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.

If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.

Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.

## 10. Handoff Rules

When handing work to the other agent:

1. Write or update the task document.
2. Write any supporting artifact needed for context.
3. Append a `handoff_requested` event.
4. Update `state.json` with the current task, status, active agent, and last event id.
5. State the handoff clearly in the user-facing response when applicable.

Handoffs should include concrete next actions, relevant file paths, and any known blockers.

## 11. Completion Rules

A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.

Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.

## 12. Readiness Signal

Codex readiness is represented by both:

- A `codex_ready` event in `events.jsonl`.
- `.omc/collaboration/codex-ready.md`.

Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.

## 13. Minimal Operating Checklist

Before collaboration work:

codex
There is already an untracked `70-codex-post-phase2b-step1-next-strategy-response.md`, so I’m checking whether the requested review was already drafted before I create or change anything. After that I’ll verify the technical claims against the backend code.
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Post Phase 2B Step 1策略 - Codex审查响应

**日期：** 2026-06-02  
**审查人：** Codex  
**类型：** 策略审查响应  
**针对：** 69-claude-post-phase2b-step1-next-strategy.md

---

## 审查结论

**不建议直接执行 Option A 的完整 Phase 2B Step 2。建议采用 Option B-mini：暂停实现，先做一个很窄的超时提醒可行性决策门。**

当前 Track 3 的完整性诉求是合理的，但 `APPROVAL_TIMEOUT_WARNING` 和前三类通知不同：前三类都是同步业务事件触发，审批超时提醒是时间驱动扫描任务。仓库里虽然已有 `celery` 和 `redis` 依赖，但没有 Celery app、没有 worker/beat 服务、没有任务模块，也没有 Docker 调度服务。因此现在直接实现会把“通知类型补齐”升级成“引入调度基础设施”。

建议下一步不是转向其他 Track，也不是马上写 Celery，而是先把 Phase 2B Step 2 收窄为决策与最小服务层准备：

1. 明确 v0.1 是否接受 Management Command + 手动/cron 调度，而不是 Celery beat。
2. 明确超时规则采用自然日还是工作日；若坚持工作日，确认是否使用已有 `chinese-calendar` 依赖。
3. 明确提醒是一次性还是重复提醒；v0.1 建议一次性。
4. 明确幂等语义：同一 `approval`、同一接收者、同一 `approval_timeout_warning` 只创建一条通知。

---

## 技术可行性评估

### Celery/定时任务状态

当前不能把 Celery 视为已配置基础设施。

证据：

- `backend/requirements/base.txt:15-17` 只有 `celery==5.3.6` 和 `redis==5.0.3` 依赖。
- `docker-compose.yml:3-34` 只有 `db` 和 `backend` 服务，没有 Redis、worker、beat。
- `backend` 下未发现 `celery.py` 或 `tasks.py`。
- `backend/config/settings/base.py` 中未发现 `CELERY_*` / broker 配置。

所以，如果 Phase 2B Step 2 选择 Celery beat，真实范围至少包含：Celery app、Redis 服务、worker、beat、任务发现、运行文档、Docker/smoke 验收。这已经超出“补第4类通知”的小任务边界。

### Management Command可行性

Management Command 更适合当前阶段。

理由：

- 不需要新增常驻进程。
- 可以在测试中直接调用命令或服务函数。
- 后续如果引入 Celery beat，可以让 Celery task 调用同一个服务函数，避免重写业务逻辑。
- 当前通知模型已有唯一约束 `(recipient, entity_type, entity_id, type)`，适合做一次性幂等提醒。

建议命令形态：

```text
python manage.py send_approval_timeout_warnings --dry-run
python manage.py send_approval_timeout_warnings
```

服务层形态：

```text
create_approval_timeout_warnings(now=None, dry_run=False) -> summary
```

---

## 推荐范围

### 最小可行范围

建议 Phase 2B Step 2 的 v0.1 范围如下：

- 只扫描 `Approval.decision == pending`。
- counselor 阶段阈值为 3 天，dean 阶段阈值为 2 天。
- v0.1 使用工作日需要明确采用 `chinese-calendar`；如果不想引入节假日语义争议，就把契约临时改成自然日。
- 只创建一次提醒，不做重复提醒。
- 通知使用：
  - `recipient = approval.approver`
  - `actor = null`
  - `type = approval_timeout_warning`
  - `entity_type = approval`
  - `entity_id = approval.pk`
- 已审批记录不提醒。
- 已存在同类通知不重复创建。
- 不接入 Celery beat；只提供 service + management command + tests。

这能完成“业务逻辑可用、幂等可验证、后续可调度”的核心价值，同时不把项目拖进调度基础设施。

### 暂不纳入范围

- Celery worker/beat 配置。
- Docker 增加 Redis/worker/beat。
- 重复提醒频率，例如每天提醒一次。
- 节假日数据源治理。
- 审批 SLA 配置化后台。
- 通知历史单独表；当前 `Notification` 已能表达一次性历史。

---

## 风险识别

### P1：Option A当前范围被低估

69号文档估计 1-2 小时，但如果包含 Celery/beat 和工作日语义，风险明显偏高。调度基础设施、重复运行幂等、Docker 验收、环境变量、日志和失败重试都不是通知服务层的小改动。

### P1：工作日规则需要先降级或明确

契约写“辅导员3工作日，学工部2工作日”。仓库依赖里已有 `chinese-calendar`，但这会引入节假日判断、调休解释和测试固定日期选择。若没有产品要求必须精确到中国法定节假日，v0.1 可以先改为自然日；若坚持工作日，则必须把算法和测试日期固定下来。

### P1：提醒频率不能留空

当前通知唯一约束会让同一审批的同一类型通知只创建一条。这个约束天然支持“一次性提醒”，不支持“每天提醒一次”。如果产品要重复提醒，需要新增周期字段或独立事件记录，否则会和幂等约束冲突。

### P2：当前审批模型可做阈值扫描，但缺少 SLA 字段

`Approval` 已有 `created_at`、`decision`、`step`、`approver`，足够做初版扫描。但没有 `due_at`、`first_warned_at` 或 SLA 配置字段。不要为了 v0.1 增加这些字段，除非要做重复提醒或配置化 SLA。

---

## 时间估算调整

建议按以下估算：

- B-mini 决策门文档：20-40分钟。
- Management Command 方案实现：1.5-2.5小时。
- 若坚持工作日并使用 `chinese-calendar`：额外 0.5-1小时。
- Celery beat 完整方案：4-7小时，且应单独立项。

因此，69号文档的 1-2 小时只适用于“服务层 + management command + 一次性提醒 + 简化日期规则”，不适用于 Celery/beat 完整接入。

---

## 对选项的判断

### Option A

**有条件支持，但必须降级。**

不要按“Celery定时任务 vs Management Command”开放式实现。当前应直接选 Management Command，并把 Celery beat 标记为后续调度接入。

### Option B

**推荐采用 B-mini，而不是大范围整体暂停。**

不需要重新评估所有 Track，但需要在超时提醒前加一个小决策门。外部阻塞如 WeChat DevTools、宿舍系统真实集成仍然重要，但它们目前不是 Codex/Claude 在仓库内可以直接消除的阻塞。当前可推进的最高价值工作，是把 Track 3 的第4类通知定义为“可运行但不调度”的窄实现。

### Option C

**暂不推荐。**

切到 Track 1/2/前端会增加上下文切换，而且 Track 3 只剩一个明确缺口。但如果用户目标已经从通知完整性转为验收发布，则应优先回到 DevTools/验收证据，而不是继续补通知。

---

## 最终建议

执行顺序建议：

1. 创建 71 号 Claude 响应/共识文档，接受 B-mini。
2. 明确 Phase 2B Step 2 的 v0.1 退出条件：service + management command + tests；不接 Celery。
3. 如果契约仍坚持“工作日”，用 `chinese-calendar` 并写固定日期测试；否则先把契约改为“自然日”。
4. 实现一次性超时提醒，验证重复运行不重复创建通知。
5. Celery beat 单独作为后续 Phase 2C/调度基础设施任务。

**结论：** 推荐 **B-mini -> 降级版 Option A**。不要转向其他 Track，也不要现在引入 Celery beat。

**文档编号：** 70  
**状态：** Codex建议先决策门，再执行Management Command版最小实现

exec
/bin/bash -lc 'rtk rg -n "Celery|celery|beat|crontab|periodic|APScheduler|django-celery|APPROVAL_TIMEOUT|TIMEOUT|timeout|Notification|notification|APPLICATION_SUBMITTED|DORM_CLEARANCE" backend docs -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/api/notification-contract-v0.1.md:33:| 申请提交 | APPLICATION_SUBMITTED | 学生提交离校申请 | 辅导员 |
docs/api/notification-contract-v0.1.md:36:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
docs/api/notification-contract-v0.1.md:40:#### APPLICATION_SUBMITTED（申请提交）
docs/api/notification-contract-v0.1.md:88:#### APPROVAL_TIMEOUT_WARNING（审批超时提醒）
docs/api/notification-contract-v0.1.md:106:### 3.1 Notification字段草案
docs/api/notification-contract-v0.1.md:110:| notification_id | String | 是 | 通知ID，格式：not_xxxxxxxx（8位随机字符） |
docs/api/notification-contract-v0.1.md:125:PRIMARY KEY (notification_id)
docs/api/notification-contract-v0.1.md:134:UNIQUE INDEX idx_notification_idempotency (recipient_id, entity_type, entity_id, type)
docs/api/notification-contract-v0.1.md:143:**端点：** `GET /api/notifications/`
docs/api/notification-contract-v0.1.md:154:GET /api/notifications/?read=false&limit=20&offset=0
docs/api/notification-contract-v0.1.md:164:      "notification_id": "not_a1b2c3d4",
docs/api/notification-contract-v0.1.md:189:**端点：** `GET /api/notifications/unread_count/`
docs/api/notification-contract-v0.1.md:195:GET /api/notifications/unread_count/
docs/api/notification-contract-v0.1.md:210:**端点：** `PATCH /api/notifications/{notification_id}/read/`
docs/api/notification-contract-v0.1.md:212:**权限：** 认证用户，且notification.recipient_id = request.user.user_id
docs/api/notification-contract-v0.1.md:216:PATCH /api/notifications/not_a1b2c3d4/read/
docs/api/notification-contract-v0.1.md:223:  "notification_id": "not_a1b2c3d4",
docs/api/notification-contract-v0.1.md:242:**端点：** `POST /api/notifications/mark_all_read/`
docs/api/notification-contract-v0.1.md:248:POST /api/notifications/mark_all_read/
docs/api/notification-contract-v0.1.md:275:existing = Notification.objects.filter(
docs/api/notification-contract-v0.1.md:283:    Notification.objects.create(...)
docs/api/notification-contract-v0.1.md:341:- Django Notification模型
docs/api/notification-contract-v0.1.md:363:1. **Management Command（推荐）：** `python manage.py seed_notifications`
docs/api/notification-contract-v0.1.md:371:   from apps.notifications.models import Notification
docs/api/notification-contract-v0.1.md:372:   Notification.objects.create(
docs/api/notification-contract-v0.1.md:383:   - `apps/notifications/fixtures/test_notifications.json`
docs/api/notification-contract-v0.1.md:426:- Celery异步任务
docs/api/notification-contract-v0.1.md:450:- 建议使用异步任务（Celery）创建通知，但v0.1可以同步创建
docs/api/api-schema-todo.md:58:- 创建ApplicationListResponseSerializer、ApprovalListResponseSerializer、NotificationListResponseSerializer
docs/superpowers/plans/2026-05-27-implementation-plan.md:98:│   │   └── celery.py
docs/superpowers/plans/2026-05-27-implementation-plan.md:124:│   │   ├── notifications/      # 通知模块
docs/superpowers/plans/2026-05-27-implementation-plan.md:197:4. **配置Celery**
docs/superpowers/plans/2026-05-27-implementation-plan.md:198:   - 安装Celery
docs/superpowers/plans/2026-05-27-implementation-plan.md:199:   - 配置Celery应用
docs/superpowers/plans/2026-05-27-implementation-plan.md:200:   - 配置Celery worker
docs/superpowers/plans/2026-05-27-implementation-plan.md:201:   - 配置Celery beat
docs/superpowers/plans/2026-05-27-implementation-plan.md:214:- ✓ Celery worker正常运行
docs/superpowers/plans/2026-05-27-implementation-plan.md:335:   - 创建Celery定时任务
docs/superpowers/plans/2026-05-27-implementation-plan.md:404:   - 定义Notification模型
docs/superpowers/plans/2026-05-27-implementation-plan.md:415:3. **实现Celery异步任务**
backend/requirements/base.txt:15:# Celery
backend/requirements/base.txt:16:celery==5.3.6
backend/config/urls.py:12:    path('api/notifications/', include('apps.notifications.urls')),
backend/config/settings/base.py:38:    'apps.notifications',
docs/contracts/contract-v0.1.md:555:      "error": "Connection timeout"
backend/apps/applications/views.py:16:from apps.notifications.services import notify_application_submitted
docs/discussions/phase4c-next-steps/55-claude-post-api-schema-p1-next-strategy.md:81:- 审批超时提醒（需要Celery定时任务）
docs/discussions/phase4c-next-steps/55-claude-post-api-schema-p1-next-strategy.md:88:- 需要Celery配置（新依赖）
docs/discussions/phase4c-next-steps/55-claude-post-api-schema-p1-next-strategy.md:145:   - Notification list: 响应示例
docs/discussions/phase4c-next-steps/55-claude-post-api-schema-p1-next-strategy.md:153:- Celery配置需要时间
docs/discussions/phase4c-next-steps/55-claude-post-api-schema-p1-next-strategy.md:172:- 但需要Celery配置，增加复杂度
backend/apps/notifications/services.py:2:Notification service layer for idempotent notification creation.
backend/apps/notifications/services.py:4:This module provides business logic for creating notifications automatically
backend/apps/notifications/services.py:9:from .models import Notification, NotificationType
backend/apps/notifications/services.py:17:    Create notification for counselor when student submits application.
backend/apps/notifications/services.py:24:        tuple: (Notification instance, created boolean)
backend/apps/notifications/services.py:29:    return Notification.objects.get_or_create(
backend/apps/notifications/services.py:33:        type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/services.py:44:    Create notification for student when approval is approved or rejected.
backend/apps/notifications/services.py:50:        tuple: (Notification instance, created boolean)
backend/apps/notifications/services.py:57:        notification_type = NotificationType.APPROVAL_APPROVED
backend/apps/notifications/services.py:61:        notification_type = NotificationType.APPROVAL_REJECTED
backend/apps/notifications/services.py:63:    return Notification.objects.get_or_create(
backend/apps/notifications/services.py:67:        type=notification_type,
backend/apps/notifications/__init__.py:1:default_app_config = 'apps.notifications.apps.NotificationsConfig'
backend/apps/approvals/views.py:15:from apps.notifications.services import notify_approval_decided
backend/apps/notifications/admin.py:2:from .models import Notification
backend/apps/notifications/admin.py:5:@admin.register(Notification)
backend/apps/notifications/admin.py:6:class NotificationAdmin(admin.ModelAdmin):
backend/apps/notifications/admin.py:7:    list_display = ['notification_id', 'recipient', 'type', 'title', 'read_at', 'created_at']
backend/apps/notifications/admin.py:9:    search_fields = ['notification_id', 'title', 'message', 'recipient__user_id']
backend/apps/notifications/admin.py:10:    readonly_fields = ['notification_id', 'created_at']
backend/apps/notifications/urls.py:5:    path('', views.list_notifications, name='notification-list'),
backend/apps/notifications/urls.py:6:    path('unread_count/', views.unread_count, name='notification-unread-count'),
backend/apps/notifications/urls.py:7:    path('<str:notification_id>/read/', views.mark_as_read, name='notification-mark-read'),
backend/apps/notifications/urls.py:8:    path('mark_all_read/', views.mark_all_read, name='notification-mark-all-read'),
docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md:79:   范围：Django Notification模型、迁移、4个读取/已读API、RBAC测试、seed命令；不含 signals、Celery、小程序通知页、微信模板。
docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md:97:- `backend/apps/notifications/`；
docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md:98:- `Notification` model + migration；
docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md:105:- `seed_notifications` management command。
docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md:110:- Celery；
docs/PROJECT-SUMMARY.md:24:- **任务队列：** Celery
docs/PROJECT-SUMMARY.md:167:- ⏸ 配置Celery（待继续）
docs/PROJECT-SUMMARY.md:554:5. **notifications** - 通知表
docs/PROJECT-SUMMARY.md:571:- Celery配置
docs/PROJECT-SUMMARY.md:600:- Celery异步任务
docs/PROJECT-SUMMARY.md:1240:- M3: Notification Contract Ready（0.5天，可选）
docs/PROJECT-SUMMARY.md:1326:  - Redis/Celery配置（可选，未来使用）
docs/PROJECT-SUMMARY.md:1494:- ✓ 创建通知契约v0.1文档（docs/api/notification-contract-v0.1.md）
docs/PROJECT-SUMMARY.md:1496:  - APPLICATION_SUBMITTED（申请提交）
docs/PROJECT-SUMMARY.md:1499:  - APPROVAL_TIMEOUT_WARNING（审批超时提醒）
docs/PROJECT-SUMMARY.md:1501:- ✓ 设计Notification数据结构（10个字段）
docs/PROJECT-SUMMARY.md:1503:  - GET /api/notifications/（列表）
docs/PROJECT-SUMMARY.md:1504:  - GET /api/notifications/unread_count/（未读数）
docs/PROJECT-SUMMARY.md:1505:  - PATCH /api/notifications/{id}/read/（标记已读）
docs/PROJECT-SUMMARY.md:1506:  - POST /api/notifications/mark_all_read/（全部已读）
docs/PROJECT-SUMMARY.md:1512:- docs/api/notification-contract-v0.1.md（通知契约草案）
docs/PROJECT-SUMMARY.md:1547:- docs/api/notification-contract-v0.1.md（已修正）
docs/PROJECT-SUMMARY.md:1573:- ✓ 创建Notification模型（10个字段）
docs/PROJECT-SUMMARY.md:1574:  - notification_id（PK，not_xxxxxxxx格式）
docs/PROJECT-SUMMARY.md:1587:  - create_notification
docs/PROJECT-SUMMARY.md:1588:  - notification_id_auto_generated
docs/PROJECT-SUMMARY.md:1594:- ✓ NotificationSerializer（8个字段）
docs/PROJECT-SUMMARY.md:1596:  - GET /api/notifications/（列表，支持read过滤和limit/offset分页）
docs/PROJECT-SUMMARY.md:1597:  - GET /api/notifications/unread_count/（未读数）
docs/PROJECT-SUMMARY.md:1598:  - PATCH /api/notifications/{id}/read/（标记已读，幂等）
docs/PROJECT-SUMMARY.md:1599:  - POST /api/notifications/mark_all_read/（全部已读）
docs/PROJECT-SUMMARY.md:1607:  - test_list_notifications
docs/PROJECT-SUMMARY.md:1617:- ✓ seed_notifications管理命令
docs/PROJECT-SUMMARY.md:1624:  - GET /api/notifications/：返回2条通知 ✓
docs/PROJECT-SUMMARY.md:1625:  - GET /api/notifications/unread_count/：返回1条未读 ✓
docs/PROJECT-SUMMARY.md:1626:  - PATCH /api/notifications/{id}/read/：标记已读成功 ✓
docs/PROJECT-SUMMARY.md:1627:  - POST /api/notifications/mark_all_read/：返回marked_count=0 ✓
docs/PROJECT-SUMMARY.md:1633:- backend/apps/notifications/models.py（Notification模型）
docs/PROJECT-SUMMARY.md:1634:- backend/apps/notifications/serializers.py（NotificationSerializer）
docs/PROJECT-SUMMARY.md:1635:- backend/apps/notifications/views.py（4个API端点）
docs/PROJECT-SUMMARY.md:1636:- backend/apps/notifications/urls.py（URL路由）
docs/PROJECT-SUMMARY.md:1637:- backend/apps/notifications/admin.py（Django admin）
docs/PROJECT-SUMMARY.md:1638:- backend/apps/notifications/migrations/0001_initial.py（数据库迁移）
docs/PROJECT-SUMMARY.md:1639:- backend/apps/notifications/tests/test_models.py（5个模型测试）
docs/PROJECT-SUMMARY.md:1640:- backend/apps/notifications/tests/test_api.py（10个API测试）
docs/PROJECT-SUMMARY.md:1641:- backend/apps/notifications/management/commands/seed_notifications.py（seed命令）
docs/PROJECT-SUMMARY.md:1670:- 范围收窄：排除宿舍阻断通知（架构约束）和审批超时提醒（需Celery）
docs/PROJECT-SUMMARY.md:1674:2. ✓ Codex审查识别架构约束（DORM_CLEARANCE_BLOCKED无法实现，失败在Application.objects.create()之前）
docs/PROJECT-SUMMARY.md:1680:- ✓ 创建backend/apps/notifications/services.py
docs/PROJECT-SUMMARY.md:1690:  - 申请创建后调用通知服务（辅导员收到APPLICATION_SUBMITTED通知）
docs/PROJECT-SUMMARY.md:1698:- ✓ 创建backend/apps/notifications/tests/test_auto_notifications.py
docs/PROJECT-SUMMARY.md:1700:  - test_application_submitted_notification（申请提交通知创建）
docs/PROJECT-SUMMARY.md:1701:  - test_approval_approved_notification_counselor（辅导员审批通过通知）
docs/PROJECT-SUMMARY.md:1702:  - test_approval_approved_notification_dean（学工部审批通过通知）
docs/PROJECT-SUMMARY.md:1703:  - test_approval_rejected_notification（审批驳回通知）
docs/PROJECT-SUMMARY.md:1712:  - 辅导员登录后验证收到APPLICATION_SUBMITTED通知
docs/PROJECT-SUMMARY.md:1717:- backend/apps/notifications/services.py（通知服务层）
docs/PROJECT-SUMMARY.md:1720:- backend/apps/notifications/tests/test_auto_notifications.py（6个测试）
docs/PROJECT-SUMMARY.md:1742:- ⏸ Phase 2C推迟（审批超时提醒，需Celery）
docs/PROJECT-SUMMARY.md:1755:   - 修改services.py使用NotificationType枚举值
docs/PROJECT-SUMMARY.md:1759:   - 修改test_auto_notifications.py断言小写枚举值
docs/PROJECT-SUMMARY.md:1763:   - 创建test_auto_notifications_api.py
docs/PROJECT-SUMMARY.md:1774:- backend/apps/notifications/services.py（修复枚举值）
docs/PROJECT-SUMMARY.md:1775:- backend/apps/notifications/tests/test_auto_notifications.py（修正断言）
docs/PROJECT-SUMMARY.md:1776:- backend/apps/notifications/tests/test_auto_notifications_api.py（新增6个API测试）
docs/PROJECT-SUMMARY.md:1792:**目标：** 修正notification-contract-v0.1.md与代码实现的不一致问题
docs/PROJECT-SUMMARY.md:1802:   - 删除DORM_CLEARANCE_BLOCKED事件枚举（保持4个事件类型）
docs/PROJECT-SUMMARY.md:1803:   - 修正APPLICATION_SUBMITTED关联实体（application→approval）
docs/PROJECT-SUMMARY.md:1804:   - 删除DORM_CLEARANCE_BLOCKED详细说明章节
docs/PROJECT-SUMMARY.md:1807:   - backend/apps/notifications/models.py：删除DORM_CLEARANCE_BLOCKED枚举
docs/PROJECT-SUMMARY.md:1808:   - backend/apps/notifications/tests/test_auto_notifications_api.py：强化宿舍阻断测试断言
docs/PROJECT-SUMMARY.md:1811:   - 生成backend/apps/notifications/migrations/0002_alter_notification_type.py
docs/PROJECT-SUMMARY.md:1812:   - 更新Notification.type字段choices（4个枚举值）
docs/PROJECT-SUMMARY.md:1819:- docs/api/notification-contract-v0.1.md（契约修正）
docs/PROJECT-SUMMARY.md:1820:- backend/apps/notifications/models.py（删除枚举）
docs/PROJECT-SUMMARY.md:1821:- backend/apps/notifications/migrations/0002_alter_notification_type.py（新增）
docs/PROJECT-SUMMARY.md:1822:- backend/apps/notifications/tests/test_auto_notifications_api.py（强化断言）
docs/PROJECT-SUMMARY.md:1940:- ✓ 确认login路径（无尾斜杠）、notification分页（count+results）、attachment wrapper
docs/PROJECT-SUMMARY.md:1944:- ✓ 创建NotificationListResponseSerializer（notifications/serializers.py）
backend/apps/notifications/views.py:8:from .models import Notification
backend/apps/notifications/views.py:9:from .serializers import NotificationSerializer, NotificationListResponseSerializer
backend/apps/notifications/views.py:14:    operation_id='notifications_list',
backend/apps/notifications/views.py:23:        200: NotificationListResponseSerializer,
backend/apps/notifications/views.py:29:def list_notifications(request):
backend/apps/notifications/views.py:31:    GET /api/notifications/
backend/apps/notifications/views.py:43:    queryset = Notification.objects.filter(recipient=user)
backend/apps/notifications/views.py:51:    notifications = queryset[offset:offset + limit]
backend/apps/notifications/views.py:52:    serializer = NotificationSerializer(notifications, many=True)
backend/apps/notifications/views.py:61:    operation_id='notifications_unread_count',
backend/apps/notifications/views.py:76:    GET /api/notifications/unread_count/
backend/apps/notifications/views.py:80:    count = Notification.objects.filter(recipient=user, read_at__isnull=True).count()
backend/apps/notifications/views.py:85:    operation_id='notifications_mark_as_read',
backend/apps/notifications/views.py:89:        200: NotificationSerializer,
backend/apps/notifications/views.py:97:def mark_as_read(request, notification_id):
backend/apps/notifications/views.py:99:    PATCH /api/notifications/{notification_id}/read/
backend/apps/notifications/views.py:105:        notification = Notification.objects.get(notification_id=notification_id)
backend/apps/notifications/views.py:106:    except Notification.DoesNotExist:
backend/apps/notifications/views.py:112:    if notification.recipient != user:
backend/apps/notifications/views.py:118:    if notification.read_at is None:
backend/apps/notifications/views.py:119:        notification.read_at = timezone.now()
backend/apps/notifications/views.py:120:        notification.save(update_fields=['read_at'])
backend/apps/notifications/views.py:122:    serializer = NotificationSerializer(notification)
backend/apps/notifications/views.py:127:    operation_id='notifications_mark_all_read',
backend/apps/notifications/views.py:143:    POST /api/notifications/mark_all_read/
backend/apps/notifications/views.py:148:    updated_count = Notification.objects.filter(
backend/apps/notifications/serializers.py:2:from .models import Notification
backend/apps/notifications/serializers.py:5:class NotificationSerializer(serializers.ModelSerializer):
backend/apps/notifications/serializers.py:7:        model = Notification
backend/apps/notifications/serializers.py:9:            'notification_id',
backend/apps/notifications/serializers.py:20:        read_only_fields = ['notification_id', 'created_at']
backend/apps/notifications/serializers.py:26:class NotificationListResponseSerializer(serializers.Serializer):
backend/apps/notifications/serializers.py:27:    """Schema-only: notification list response with custom pagination"""
backend/apps/notifications/serializers.py:29:    results = NotificationSerializer(many=True)
backend/apps/notifications/apps.py:4:class NotificationsConfig(AppConfig):
backend/apps/notifications/apps.py:6:    name = 'apps.notifications'
backend/apps/notifications/models.py:7:def generate_notification_id():
backend/apps/notifications/models.py:14:class NotificationType(models.TextChoices):
backend/apps/notifications/models.py:15:    APPLICATION_SUBMITTED = 'application_submitted', '申请已提交'
backend/apps/notifications/models.py:18:    APPROVAL_TIMEOUT_WARNING = 'approval_timeout_warning', '审批超时提醒'
backend/apps/notifications/models.py:26:class Notification(models.Model):
backend/apps/notifications/models.py:27:    notification_id = models.CharField(
backend/apps/notifications/models.py:30:        default=generate_notification_id,
backend/apps/notifications/models.py:37:        related_name='notifications_received',
backend/apps/notifications/models.py:43:        related_name='notifications_triggered',
backend/apps/notifications/models.py:50:        choices=NotificationType.choices,
backend/apps/notifications/models.py:80:        db_table = 'notifications'
backend/apps/notifications/models.py:91:                name='unique_notification_per_recipient_entity'
backend/apps/notifications/models.py:96:        return f'{self.notification_id}: {self.title}'
backend/apps/notifications/migrations/0001_initial.py:3:import apps.notifications.models
backend/apps/notifications/migrations/0001_initial.py:19:            name='Notification',
backend/apps/notifications/migrations/0001_initial.py:21:                ('notification_id', models.CharField(default=apps.notifications.models.generate_notification_id, editable=False, max_length=12, primary_key=True, serialize=False, verbose_name='通知ID')),
backend/apps/notifications/migrations/0001_initial.py:22:                ('type', models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('dorm_clearance_blocked', '宿舍清退阻断'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型')),
backend/apps/notifications/migrations/0001_initial.py:29:                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='notifications_triggered', to=settings.AUTH_USER_MODEL, verbose_name='触发者')),
backend/apps/notifications/migrations/0001_initial.py:30:                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='notifications_received', to=settings.AUTH_USER_MODEL, verbose_name='接收者')),
backend/apps/notifications/migrations/0001_initial.py:35:                'db_table': 'notifications',
backend/apps/notifications/migrations/0001_initial.py:41:            model_name='notification',
backend/apps/notifications/migrations/0001_initial.py:42:            constraint=models.UniqueConstraint(fields=('recipient', 'entity_type', 'entity_id', 'type'), name='unique_notification_per_recipient_entity'),
docs/design/2026-05-27-system-design.md:94:        │                   │  Celery      │
docs/design/2026-05-27-system-design.md:127:- Celery 5.3（异步任务）
docs/design/2026-05-27-system-design.md:162:│   ├── notifications/     # 通知模块
docs/design/2026-05-27-system-design.md:164:│   │   ├── tasks.py       # Celery异步任务
docs/design/2026-05-27-system-design.md:215:5. **notifications（通知模块）**
docs/design/2026-05-27-system-design.md:220:   - 异步任务队列（Celery）
docs/design/2026-05-27-system-design.md:250:5. notifications - 通知表
docs/design/2026-05-27-system-design.md:374:    is_timeout BOOLEAN DEFAULT FALSE COMMENT '是否超时',
docs/design/2026-05-27-system-design.md:390:- `is_timeout`: 超过时限标记为超时
docs/design/2026-05-27-system-design.md:426:### 2.6 通知表（notifications）
docs/design/2026-05-27-system-design.md:429:CREATE TABLE notifications (
docs/design/2026-05-27-system-design.md:433:    notification_type VARCHAR(50) NOT NULL COMMENT '通知类型',
docs/design/2026-05-27-system-design.md:453:**通知类型（notification_type）：**
docs/design/2026-05-27-system-design.md:458:- `approval_timeout` - 审批超时提醒
docs/design/2026-05-27-system-design.md:487:- `notification` - 通知配置
docs/design/2026-05-27-system-design.md:594:  └─1:N─→ notifications (用户接收多个通知)
docs/design/2026-05-27-system-design.md:603:  ├─1:N─→ notifications (一个申请多条通知)
docs/design/2026-05-27-system-design.md:605:  └─1:N─→ notifications (一个申请触发多个通知)
docs/design/2026-05-27-system-design.md:614:notifications (通知表)
docs/design/2026-05-27-system-design.md:1142:GET /api/v1/notifications?is_read=false&page=1
docs/design/2026-05-27-system-design.md:1165:PUT /api/v1/notifications/{id}/read
docs/design/2026-05-27-system-design.md:1226:- `notification` - 通知配置
docs/design/2026-05-27-system-design.md:1501:# Celery定时任务，每小时执行一次
docs/design/2026-05-27-system-design.md:1505:@celery.task
docs/design/2026-05-27-system-design.md:1506:def check_approval_timeout():
docs/design/2026-05-27-system-design.md:1535:                action='timeout',
docs/design/2026-05-27-system-design.md:1536:                is_timeout=True,
docs/design/2026-05-27-system-design.md:1540:            send_timeout_notification(app)
docs/design/2026-05-27-system-design.md:1661:            timeout=5
docs/design/2026-05-27-system-design.md:1688:                timeout=5
docs/design/2026-05-27-system-design.md:1750:  celery-worker:  # 异步任务
docs/design/2026-05-27-system-design.md:1751:  celery-beat:    # 定时任务
docs/design/2026-05-27-system-design.md:1764:    ├─ celery-worker
docs/design/2026-05-27-system-design.md:1765:    └─ celery-beat
docs/design/2026-05-27-system-design.md:1792:    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 9 --max-requests 1000 --timeout 30
docs/design/2026-05-27-system-design.md:1819:  celery-worker:
docs/design/2026-05-27-system-design.md:1821:    command: celery -A config worker -l info
docs/design/2026-05-27-system-design.md:1832:  celery-beat:
docs/design/2026-05-27-system-design.md:1834:    command: celery -A config beat -l info
docs/design/2026-05-27-system-design.md:2266:@celery.task
docs/design/2026-05-27-system-design.md:2368:-- notifications表索引
docs/design/2026-05-27-system-design.md:2369:CREATE INDEX idx_user_id ON notifications(user_id);
docs/design/2026-05-27-system-design.md:2370:CREATE INDEX idx_is_read ON notifications(is_read);
docs/design/2026-05-27-system-design.md:2371:CREATE INDEX idx_send_status ON notifications(send_status);
docs/design/2026-05-27-system-design.md:2372:CREATE INDEX idx_user_read_time ON notifications(user_id, is_read, created_at DESC);
docs/design/2026-05-27-system-design.md:2500:**Celery任务队列：**
docs/design/2026-05-27-system-design.md:2503:@celery.task
docs/design/2026-05-27-system-design.md:2509:@celery.task
docs/design/2026-05-27-system-design.md:2510:def send_notification(user_id, message):
docs/design/2026-05-27-system-design.md:2515:@celery.task
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:136:不需要额外实现前端超时。微信API层已有网络失败回调；MVP阶段不建议自己包复杂timeout。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:14:理由很直接：上一轮共识已经把通知契约草案定义为纯文档任务，并明确“完成后硬停止”。`docs/api/notification-contract-v0.1.md` 自身也写明 Phase 1 “需单独授权”。因此，“继续讨论下一步”或再次要求 Claude/Codex 讨论，只能覆盖“可以重新评估”，不能自动覆盖“可以落库、加 API、加测试”。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:51:**位置：** `docs/api/notification-contract-v0.1.md:164-181`
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:59:**位置：** `docs/api/notification-contract-v0.1.md:150-151`, `docs/api/notification-contract-v0.1.md:280-299`
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:71:**位置：** `docs/api/notification-contract-v0.1.md:356-368`, `28-claude-post-phase0-next-strategy.md:175-177`
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:79:**位置：** `docs/api/notification-contract-v0.1.md:247-252`, `docs/api/notification-contract-v0.1.md:327-334`
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:111:- `Notification` model + migration；
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:136:- **实现范围膨胀：** Phase 1禁止 signals 和 Celery。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:160:   - B. 先修正 `notification-contract-v0.1.md` 中的分页、错误结构、幂等键和 Phase 1验收边界；
docs/discussions/phase4c-next-steps/59-claude-codex-final-consensus-option-2.md:65:- Phase 2C：审批超时提醒（需Celery定时任务）
docs/discussions/phase4c-next-steps/59-claude-codex-final-consensus-option-2.md:73:- 需要Celery配置（新依赖）
docs/discussions/phase4c-next-steps/59-claude-codex-final-consensus-option-2.md:146:4. **技术挑战适中：** Celery配置 + 契约修正 + 测试
docs/discussions/phase4c-next-steps/59-claude-codex-final-consensus-option-2.md:154:   - 配置Celery Beat
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:19:5. ✅ APPLICATION_SUBMITTED实体不一致需要同步修正
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:28:- 从notification-contract-v0.1.md删除DORM_CLEARANCE_BLOCKED
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:29:- 同步修正APPLICATION_SUBMITTED实体为approval
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:35:### 1. 修改notification-contract-v0.1.md
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:38:1. 事件枚举表：删除DORM_CLEARANCE_BLOCKED行
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:39:2. 删除DORM_CLEARANCE_BLOCKED详细说明章节
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:40:3. 修正APPLICATION_SUBMITTED关联实体：
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:46:- Line 36: 删除DORM_CLEARANCE_BLOCKED行
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:47:- Line 51-53: 修正APPLICATION_SUBMITTED实体
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:48:- Line 89-102: 删除DORM_CLEARANCE_BLOCKED详细说明
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:52:### 2. 修改backend/apps/notifications/models.py
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:55:删除NotificationType.DORM_CLEARANCE_BLOCKED枚举值
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:58:- Line 18: 删除DORM_CLEARANCE_BLOCKED枚举
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:62:### 3. 修改backend/apps/notifications/tests/test_auto_notifications_api.py
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:65:强化test_dorm_blocked_does_not_create_notification测试断言
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:70:- 添加断言：Notification.objects.filter(recipient=blocked_student).count() == 0
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:80:1. 修改notification-contract-v0.1.md（契约修正）
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:81:2. 修改backend/apps/notifications/models.py（删除枚举）
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:82:3. 修改backend/apps/notifications/tests/test_auto_notifications_api.py（强化测试）
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:30:docker compose exec backend python manage.py test apps.notifications.tests.test_auto_notifications apps.notifications.tests.test_auto_notifications_api
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:42:- `backend/apps/notifications/services.py`
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:43:- `backend/apps/notifications/tests/test_auto_notifications.py`
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:44:- `backend/apps/notifications/tests/test_auto_notifications_api.py`
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:82:当前smoke只查`/api/notifications/unread_count/`。下一步计划提出验证`type/entity_type/entity_id/message`是正确方向，但实现时必须从`/api/notifications/`中过滤本次流程产生的通知。
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:102:- auth、applications、approvals、attachments、notifications端点出现在schema中。
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:126:**位置：** `backend/apps/notifications/tests/test_auto_notifications_api.py:50-149`
backend/apps/notifications/management/commands/seed_notifications.py:4:from apps.notifications.models import Notification, NotificationType, EntityType
backend/apps/notifications/management/commands/seed_notifications.py:20:            Notification.objects.create(
backend/apps/notifications/management/commands/seed_notifications.py:22:                type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/management/commands/seed_notifications.py:31:                Notification.objects.create(
backend/apps/notifications/management/commands/seed_notifications.py:33:                    type=NotificationType.APPROVAL_APPROVED,
docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:62:- 设计Notification模型（通知ID、用户、类型、内容、已读状态）
docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:167:- 设计Notification模型
docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:168:- 定义API契约（GET /api/notifications/, PATCH /api/notifications/{id}/read/）
docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:173:- 实现Notification模型和迁移
docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:187:- 实现Celery异步任务
backend/apps/notifications/migrations/0002_alter_notification_type.py:9:        ('notifications', '0001_initial'),
backend/apps/notifications/migrations/0002_alter_notification_type.py:14:            model_name='notification',
backend/apps/notifications/migrations/0002_alter_notification_type.py:16:            field=models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型'),
docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:69:- 创建Notification模型草案
docs/discussions/phase4c-next-steps/34-claude-authorization-interpretation-request.md:34:- 范围：Django Notification模型 + 迁移 + 4 API + RBAC测试 + seed命令
docs/discussions/phase4c-next-steps/34-claude-authorization-interpretation-request.md:35:- 排除：signals、Celery、小程序页、微信模板
docs/discussions/phase4c-next-steps/54-claude-codex-consensus-option-a-execution.md:29:- 重点：login路径/响应、notification分页、attachment wrapper、错误envelope
docs/discussions/phase4c-next-steps/54-claude-codex-consensus-option-a-execution.md:34:- Notification list响应（count + results）
docs/discussions/phase4c-next-steps/54-claude-codex-consensus-option-a-execution.md:61:✓ Login/notification/attachment schema以当前代码为准  
docs/discussions/phase4c-next-steps/54-claude-codex-consensus-option-a-execution.md:64:✓ 不修改notification分页行为
docs/discussions/phase4c-next-steps/54-claude-codex-consensus-option-a-execution.md:76:7. ✓ Login/notification/attachment schema与实际匹配
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:49:- Celery beat/worker部署复杂度未准备好
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:79:- 修改`backend/apps/notifications/services.py`
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:80:- 使用`NotificationType.APPLICATION_SUBMITTED.value`等枚举值
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:81:- 不使用裸字符串`'APPLICATION_SUBMITTED'`
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:84:- 修改`backend/apps/notifications/tests/test_auto_notifications.py`
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:89:- 在`test_auto_notifications.py`或新建`test_auto_notifications_api.py`
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:179:- Phase 2C（审批超时提醒）- 推迟到Celery方案确定后
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:106:### P2-5: Notification分页schema不符
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:154:- 对齐`docs/api/notification-contract-v0.1.md`
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:158:- Notification分页
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:169:- 创建notification list响应（`count` + `results`）
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:222:7. ✓ Login/notification/attachment schema与实际行为匹配
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:70:- Track 3 Phase 2B-2C：4-6小时（包含Celery + 测试）
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:18:1. `APPLICATION_SUBMITTED`
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:24:1. `DORM_CLEARANCE_BLOCKED`
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:25:2. `APPROVAL_TIMEOUT_WARNING`
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:33:### P1：`DORM_CLEARANCE_BLOCKED` 不能由当前模型 signals 可靠触发
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:42:- 如果强行用学生 ID 或固定占位 ID，会破坏当前 `Notification` 唯一约束的业务含义。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:44:**裁决：** 本轮不要把 `DORM_CLEARANCE_BLOCKED` 纳入 signals Phase 2验收标准。可作为后续独立小任务处理：要么调整契约允许 `entity_type=student/application_attempt`，要么在阻断时创建可追踪的申请尝试记录。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:57:**裁决：** 先建立 `apps.notifications.services`，提供幂等创建函数；业务入口或 signals 都调用该服务。不要把拼装和幂等逻辑散落在 receiver 里。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:61:**位置：** `backend/apps/notifications/models.py:89-93`
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:67:1. 同一申请重复保存不重复创建 `APPLICATION_SUBMITTED`。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:71:### P2：`APPLICATION_SUBMITTED` 接收者解析需要定义失败策略
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:81:**位置：** `docs/api/notification-contract-v0.1.md:57-70`
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:97:- Phase 2C：超时提醒任务设计，等 Celery/调度方案确定后再做。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:105:- `DORM_CLEARANCE_BLOCKED`：当前失败路径没有实体落库；
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:106:- `APPROVAL_TIMEOUT_WARNING`：需要定时任务，不是状态保存触发。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:128:1. signals receiver 未在 `NotificationsConfig.ready()` 中加载，Django 不会自动注册。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:129:2. Django 4下 `default_app_config` 不可靠，当前 `INSTALLED_APPS` 使用的是 `'apps.notifications'`，若要在 notifications app 注册 signals，应改用 `'apps.notifications.apps.NotificationsConfig'` 或确认自动 config 发现行为。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:138:1. `backend/apps/notifications/services.py`
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:154:- 成功提交申请后创建 `APPLICATION_SUBMITTED` 给辅导员；
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:162:- `DORM_CLEARANCE_BLOCKED`；
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:163:- `APPROVAL_TIMEOUT_WARNING`；
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:166:- Celery/定时任务；
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:173:1. 学生提交申请成功后，辅导员收到一条 `APPLICATION_SUBMITTED` 通知。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:180:8. 自动通知测试与既有 application/approval/notification tests 全部通过。
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:41:**Location:** `backend/apps/applications/views.py:79`, `backend/apps/applications/views.py:93`, `backend/apps/attachments/views.py:43`, `backend/apps/notifications/views.py:67`, `backend/apps/users/views.py:14`
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:85:### P2 - Notification pagination schema in the plan is not the current response
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:87:**Location:** `backend/apps/notifications/views.py:22`, `backend/apps/notifications/views.py:23`, `backend/apps/notifications/views.py:37`
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:89:Notifications use custom `limit`/`offset` parsing and return only:
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:126:- `docs/api/notification-contract-v0.1.md`
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:128:Pay special attention to login path/response, notification pagination, attachment wrapper shape, and error envelopes.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:137:- notification list response with `count` and `results`
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:178:   Yes, after a small B-mini cleanup. Option A is the best internal, non-blocked work. Track 3 Phase 2B/2C should remain deferred because dorm-blocked notification semantics and Celery introduction are larger architectural decisions.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:184:   Yes: login schema mismatch, raw login errors, framework `401` error shape, multi-method dispatcher schemas, notification pagination shape, attachment module ownership, and imprecise warning acceptance.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:187:   Execute **B-mini + A-corrected**. Fix the smoke typo first, then do a schema-fidelity pass. Do not broaden into new notification features or Celery work until external blockers and explicit user authorization are resolved.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:198:- Document auth/login and notification pagination accurately.
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:14:Claude 推荐的技术方向基本合理：Phase 1 可以作为下一步内部工作，且应限定为后端通知读取 MVP，不包含信号触发、小程序页面、微信模板消息。但授权解释不能跳过前一轮共识里的硬边界：`docs/api/notification-contract-v0.1.md` 已明确写明 Phase 1 的前置条件是“用户明确授权启动 Track 3 实现”。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:55:- 新增 `notifications` Django app。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:56:- 新增 `Notification` 模型和迁移。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:65:- Celery/异步任务。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:91:**P1 - `notification_id` 生成规则需要落地。**  
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:101:Phase 1 测试数据可以通过 factory、fixtures、management command 或 admin/shell 创建，不应新增公开 POST `/api/notifications/`。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:118:> Track 3 Phase 0 通知契约已完成。下一步是否授权启动 Phase 1 后端通知 MVP？范围限定为 Django Notification 模型、迁移、4 个读取/已读 API、权限隔离测试和 curl 验证；不包含信号触发、小程序通知页、微信模板消息。回复“授权 Phase 1”后开始实现。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:126:若用户授权 Phase 1，建议先对 `docs/api/notification-contract-v0.1.md` 做最小修正后再编码：
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:36:| 设计 Notification 数据结构 | 有条件同意 | 只写字段草案，不创建 model/migration |
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:37:| 实现 Notification 模型 | 暂缓 | 需要用户明确授权进入 Track 3 实现 |
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:62:建议把当前 Phase 1 改名为 **Phase 0/1: Notification Contract Draft**，交付物限定为一个文档，例如：
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:64:- `docs/contracts/notification-contract-v0.1.md` 或 `docs/api/notification-contract-v0.1.md`
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:80:- Celery 任务；
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:30:- notification 断言覆盖 `type`、`entity_type`、`message`。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:50:- `docs/api/api-schema-todo.md` 中 notification mark-as-read 路径写成 `/api/notifications/mark_as_read/`，实际路由和 schema 是 `/api/notifications/{notification_id}/read/`。Step 3 或收尾时应修正这个清单。
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md:95:- Phase 2C：审批超时提醒（需Celery）
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md:104:- 需要架构决策（引入Celery）
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md:109:- Celery引入可能带来新的复杂度
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md:146:3. **无外部依赖：** 不需要WeChat DevTools、宿舍系统或Celery
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md:164:- 按模块分组（auth/applications/approvals/notifications/attachments）
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md:193:**任务2.4：notifications模块（15分钟）**
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md:194:- /api/notifications/ - 列表端点
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md:195:- /api/notifications/{notification_id}/read/ - 标记已读
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md:196:- /api/notifications/mark_all_read/ - 全部已读
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md:197:- /api/notifications/unread_count/ - 未读数
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:59:   - Track 3 Phase 2B-2C涉及Celery、定时任务、契约修正和幂等策略，应该单独立项。
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:67:- **Track 3 Phase 2B-2C：** 3-4小时偏紧。审批超时提醒如果包含Celery beat、幂等、防重复、测试和文档，建议按4-6小时估算。
docs/discussions/phase4c-next-steps/36-claude-consensus-minimal-confirmation.md:48:- backend/apps/notifications/ (model/migration/serializer/views/urls/admin/tests/seed)
docs/discussions/phase4c-next-steps/36-claude-consensus-minimal-confirmation.md:54:- signals、Celery、审批挂钩、超时提醒
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:52:**接受裁决：** 通知系统排在CSV导入和Docker硬化之后，仅做通知事件契约或后端`Notification`模型草案，不承诺完整通知中心。
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:128:### M3：Notification Contract Ready（0.5天，可选）
docs/discussions/phase4c-next-steps/49-claude-consensus-option-e-lite-complete.md:47:- 修正前：`/api/notifications/mark_as_read/`
docs/discussions/phase4c-next-steps/49-claude-consensus-option-e-lite-complete.md:48:- 修正后：`/api/notifications/{notification_id}/read/`
docs/discussions/phase4c-next-steps/49-claude-consensus-option-e-lite-complete.md:59:2. ✓ 修正api-schema-todo.md路径（{notification_id}/read/）
docs/discussions/phase4c-next-steps/49-claude-consensus-option-e-lite-complete.md:121:- 审批超时提醒（需Celery）
docs/discussions/phase4c-next-steps/67-claude-response-accept-codex-fixes.md:18:4. ✅ APPLICATION_SUBMITTED实体修正合理性分析准确
docs/discussions/phase4c-next-steps/67-claude-response-accept-codex-fixes.md:29:- 命令：`rtk docker compose exec -T backend python manage.py makemigrations notifications`
docs/discussions/phase4c-next-steps/67-claude-response-accept-codex-fixes.md:30:- 预期：生成`backend/apps/notifications/migrations/0002_alter_notification_type.py`
docs/discussions/phase4c-next-steps/67-claude-response-accept-codex-fixes.md:37:  - 删除DORM_CLEARANCE_BLOCKED相关描述
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:110:- 从`/api/notifications/`获取通知列表
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:96:需要fixture matrix：无班级、重复学号、辅导员停用、多班级、非毕业生、延期、宿舍API 401/404/429/500/timeout。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:14:当前 Track 3 的完整性诉求是合理的，但 `APPROVAL_TIMEOUT_WARNING` 和前三类通知不同：前三类都是同步业务事件触发，审批超时提醒是时间驱动扫描任务。仓库里虽然已有 `celery` 和 `redis` 依赖，但没有 Celery app、没有 worker/beat 服务、没有任务模块，也没有 Docker 调度服务。因此现在直接实现会把“通知类型补齐”升级成“引入调度基础设施”。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:16:建议下一步不是转向其他 Track，也不是马上写 Celery，而是先把 Phase 2B Step 2 收窄为决策与最小服务层准备：
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:18:1. 明确 v0.1 是否接受 Management Command + 手动/cron 调度，而不是 Celery beat。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:21:4. 明确幂等语义：同一 `approval`、同一接收者、同一 `approval_timeout_warning` 只创建一条通知。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:27:### Celery/定时任务状态
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:29:当前不能把 Celery 视为已配置基础设施。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:33:- `backend/requirements/base.txt:15-17` 只有 `celery==5.3.6` 和 `redis==5.0.3` 依赖。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:34:- `docker-compose.yml:3-34` 只有 `db` 和 `backend` 服务，没有 Redis、worker、beat。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:35:- `backend` 下未发现 `celery.py` 或 `tasks.py`。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:38:所以，如果 Phase 2B Step 2 选择 Celery beat，真实范围至少包含：Celery app、Redis 服务、worker、beat、任务发现、运行文档、Docker/smoke 验收。这已经超出“补第4类通知”的小任务边界。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:48:- 后续如果引入 Celery beat，可以让 Celery task 调用同一个服务函数，避免重写业务逻辑。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:54:python manage.py send_approval_timeout_warnings --dry-run
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:55:python manage.py send_approval_timeout_warnings
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:61:create_approval_timeout_warnings(now=None, dry_run=False) -> summary
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:79:  - `type = approval_timeout_warning`
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:84:- 不接入 Celery beat；只提供 service + management command + tests。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:90:- Celery worker/beat 配置。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:91:- Docker 增加 Redis/worker/beat。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:95:- 通知历史单独表；当前 `Notification` 已能表达一次性历史。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:103:69号文档估计 1-2 小时，但如果包含 Celery/beat 和工作日语义，风险明显偏高。调度基础设施、重复运行幂等、Docker 验收、环境变量、日志和失败重试都不是通知服务层的小改动。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:126:- Celery beat 完整方案：4-7小时，且应单独立项。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:128:因此，69号文档的 1-2 小时只适用于“服务层 + management command + 一次性提醒 + 简化日期规则”，不适用于 Celery/beat 完整接入。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:138:不要按“Celery定时任务 vs Management Command”开放式实现。当前应直接选 Management Command，并把 Celery beat 标记为后续调度接入。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:159:2. 明确 Phase 2B Step 2 的 v0.1 退出条件：service + management command + tests；不接 Celery。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:162:5. Celery beat 单独作为后续 Phase 2C/调度基础设施任务。
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:164:**结论：** 推荐 **B-mini -> 降级版 Option A**。不要转向其他 Track，也不要现在引入 Celery beat。
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:64:- Phase 1A: Django Notification模型 + migration（1-2小时）
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:136:**描述：** 只实现Notification模型和迁移，不实现API，用于验证数据结构设计
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:150:- Django Notification模型
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:182:- Django Notification模型（10字段）
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:188:- NotificationSerializer
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:189:- NotificationViewSet
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:191:  - GET /api/notifications/（列表，支持read过滤和分页）
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:192:  - GET /api/notifications/unread_count/（未读数）
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:193:  - PATCH /api/notifications/{id}/read/（标记已读）
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:194:  - POST /api/notifications/mark_all_read/（全部已读）
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:205:- Management command: seed_notifications（创建测试数据）
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:209:- 更新notification-contract-v0.1.md状态为"Phase 1 implemented"
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:215:- Celery异步任务（推迟到Phase 2）
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:228:- A. 通过POST /api/notifications/创建（需要新增创建端点）
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:241:# backend/apps/notifications/management/commands/seed_notifications.py
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:242:python manage.py seed_notifications --user 2020001 --count 10
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:293:   - **缓解：** 严格遵守Phase 1范围，禁止信号和Celery
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:28:**契约声明（notification-contract-v0.1.md）：**
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:30:DORM_CLEARANCE_BLOCKED:
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:42:        'error': 'DORM_CLEARANCE_BLOCKED',
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:48:**测试期望（test_auto_notifications_api.py）：**
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:50:def test_dorm_blocked_does_not_create_notification(self):
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:52:    assert Notification.objects.count() == 0
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:71:- 从契约中删除DORM_CLEARANCE_BLOCKED或标记为deferred
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:108:- 修改幂等键定义（recipient_id + entity_type + entity_id + notification_type）
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:117:- 幂等键变复杂（需要加notification_type）
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:129:4. **测试调整：** 如果创建通知，test_dorm_blocked_does_not_create_notification需要如何修改？
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:130:5. **契约修正：** notification-contract-v0.1.md需要如何更新？
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:138:- docs/api/notification-contract-v0.1.md（通知契约）
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:143:- backend/apps/notifications/models.py（Notification模型）
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:144:- backend/apps/notifications/services.py（通知服务）
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:147:- backend/apps/notifications/tests/test_auto_notifications_api.py（自动通知测试）
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:12:**建议当前采用 Option 1：不为宿舍阻断创建通知，将 `DORM_CLEARANCE_BLOCKED` 从 v0.1 自动通知契约中删除或标记为 deferred。**
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:25:- `docs/api/notification-contract-v0.1.md:89`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:26:- `docs/api/notification-contract-v0.1.md:99`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:30:契约要求 `DORM_CLEARANCE_BLOCKED` 关联 `application_id`，但代码在宿舍状态非 `completed` 时直接返回 `422`，`Application.objects.create(...)` 在后续分支才执行。也就是说阻断路径没有合法 `application_id`。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:48:- `backend/apps/notifications/models.py:89`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:57:- `docs/api/notification-contract-v0.1.md:51`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:58:- `backend/apps/notifications/services.py:29`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:60:契约写 `APPLICATION_SUBMITTED` 关联 `application`，但服务实际用 `entity_type='approval'`、`entity_id=approval.pk` 创建通知。考虑接收者是辅导员，通知入口要处理的是待审批记录，当前实现使用 `approval` 更合理。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:62:**建议：** 本次修订 `notification-contract-v0.1.md` 时一并把 `APPLICATION_SUBMITTED` 的关联实体改为 `approval/{approval_id}`，避免后续 Phase 2B 文档只修宿舍阻断而留下旧冲突。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:74:- `notification-contract-v0.1.md` 删除 `DORM_CLEARANCE_BLOCKED`，或保留在“Deferred / 后续版本”章节。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:75:- 当前测试 `test_dorm_blocked_does_not_create_notification` 的方向保持正确，但断言应强化为“学生和辅导员都没有宿舍阻断/申请提交通知”。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:117:- 保留并改名为 `test_dorm_blocked_returns_422_without_notification`。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:120:- 断言 `Notification.objects.filter(recipient=blocked_student).count() == 0`。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:134:- 事件枚举移除 `DORM_CLEARANCE_BLOCKED`，或移动到 `Deferred events`。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:137:- 同步修正 `APPLICATION_SUBMITTED` 的实体为 `approval/{approval_id}`，匹配现有服务实现。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:143:- `docs/api/notification-contract-v0.1.md`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:144:- `backend/apps/notifications/tests/test_auto_notifications_api.py`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:151:- `backend/apps/notifications/models.py`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:152:- `backend/apps/notifications/services.py`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:153:- `backend/apps/notifications/tests/test_auto_notifications_api.py`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:154:- `docs/api/notification-contract-v0.1.md`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:159:- `backend/apps/notifications/models.py`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:161:- `backend/apps/notifications/services.py`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:163:- `backend/apps/notifications/tests/test_auto_notifications_api.py`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:164:- `docs/api/notification-contract-v0.1.md`
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:178:Phase 2B不要直接实现宿舍阻断通知。当前应把 Phase 2B 定义为“契约修正优先”：从 v0.1 自动通知范围中移除或 defer `DORM_CLEARANCE_BLOCKED`，保持同步 `422` 阻断行为，并加强现有负路径测试。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:55:      "error": "Connection timeout"
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:39:- 执行P1修复：生成migration（0002_alter_notification_type.py）
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:48:**文件：** `docs/api/notification-contract-v0.1.md`
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:50:**修改1：** 删除DORM_CLEARANCE_BLOCKED事件枚举行
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:54:**修改2：** 修正APPLICATION_SUBMITTED关联实体
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:59:**修改3：** 删除DORM_CLEARANCE_BLOCKED详细说明章节
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:66:**文件1：** `backend/apps/notifications/models.py`
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:67:- 删除：`NotificationType.DORM_CLEARANCE_BLOCKED`枚举
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:68:- 结果：NotificationType现有4个枚举值
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:70:**文件2：** `backend/apps/notifications/tests/test_auto_notifications_api.py`
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:71:- 强化：`test_dorm_blocked_does_not_create_notification`断言
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:79:**文件：** `backend/apps/notifications/migrations/0002_alter_notification_type.py`
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:80:- 生成原因：删除DORM_CLEARANCE_BLOCKED后Notification.type的choices变更
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:89:- 删除：DORM_CLEARANCE_BLOCKED列表项
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:97:- ✅ notification-contract-v0.1.md事件枚举：4个类型
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:98:- ✅ APPLICATION_SUBMITTED实体：approval/{approval_id}
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:99:- ✅ 无DORM_CLEARANCE_BLOCKED详细章节
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:102:- ✅ models.py NotificationType：4个枚举值
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:103:- ✅ test_auto_notifications_api.py：3个断言覆盖核心语义
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:104:- ✅ 全仓库搜索：无活跃代码引用DORM_CLEARANCE_BLOCKED
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:107:- ✅ 生成0002_alter_notification_type.py（Django 4.2.13）
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:137:### APPLICATION_SUBMITTED为什么用approval实体？
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:153:- backend/apps/notifications/models.py（枚举删除）
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:154:- backend/apps/notifications/migrations/0002_alter_notification_type.py（新增）
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:155:- backend/apps/notifications/tests/test_auto_notifications_api.py（断言强化）
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:158:- docs/api/notification-contract-v0.1.md（3处修改）
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:172:**范围：** 实现APPROVAL_TIMEOUT_WARNING通知（审批超时提醒）
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:14:Codex识别的`DORM_CLEARANCE_BLOCKED`架构约束是正确的：当前失败路径在`backend/apps/applications/views.py:98-105`直接返回422，在`Application.objects.create()`之前，没有可关联的实体。这是我在原策略分析中遗漏的关键约束。
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:23:- `APPLICATION_SUBMITTED`（申请提交）
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:28:- `DORM_CLEARANCE_BLOCKED`：需要先修正契约或增加申请尝试实体
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:29:- `APPROVAL_TIMEOUT_WARNING`：需要Celery定时任务
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:33:**接受：** 先创建`backend/apps/notifications/services.py`，提供幂等创建函数，而不是直接在signals receiver中实现业务逻辑。
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:45:1. 学生提交申请成功后，辅导员收到一条`APPLICATION_SUBMITTED`通知
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:52:8. 自动通知测试与既有application/approval/notification tests全部通过
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:61:- 新增`backend/apps/notifications/services.py`
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:69:- `DORM_CLEARANCE_BLOCKED`通知
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:70:- `APPROVAL_TIMEOUT_WARNING`通知
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:73:- Celery/定时任务
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:78:- 创建`backend/apps/notifications/services.py`
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:89:- 创建`backend/apps/notifications/tests/test_auto_notifications.py`
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:107:# APPLICATION_SUBMITTED
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:125:def create_notification_idempotent(recipient, actor, type, entity_type, entity_id, title, message):
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:126:    notification, created = Notification.objects.get_or_create(
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:137:    return notification, created
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:147:- `DORM_CLEARANCE_BLOCKED`通知（推迟到契约修正后）
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:148:- `APPROVAL_TIMEOUT_WARNING`通知（推迟到Celery方案确定后）
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:159:- 需要Celery定时任务
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:125:3. **后端骨架**：1天（Django项目、Docker、Celery基础配置）
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:21:- ⏸ Track 3 Phase 2C: 审批超时提醒（需Celery定时任务）
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:42:- 需要Celery定时任务基础设施
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:75:- 测试覆盖良好（applications/approvals/attachments/notifications）
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:86:- Phase 2C: Celery基础设施 + 审批超时提醒
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:94:- Phase 2C需要引入Celery（新依赖，增加复杂度）
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:100:- Phase 2C: 3-4小时（Celery配置 + 定时任务 + 工作日计算 + 测试）
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:104:- Celery引入可能带来部署复杂度
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:252:- 需要Celery基础设施（复杂度高）
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:267:   - 不引入新依赖（无Celery）
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:271:   - Celery引入复杂度高
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:295:1. 宿舍阻断时学生收到DORM_CLEARANCE_BLOCKED通知
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:61:**建议裁决：** 通知系统排在CSV导入和Docker硬化之后。短期只做通知事件契约或后端`Notification`模型草案，最多实现"审批动作后创建站内通知记录"的无前端骨架；不要承诺完整通知中心。
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:185:### M3：Notification Contract Ready（可选）
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:18:3. Phase 2C（审批超时提醒）暂不和2B捆绑执行，先单独立项并明确Celery/调度策略。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:38:Phase 2B可以作为下一步，但必须先修契约。当前 `DORM_CLEARANCE_BLOCKED` 契约声明关联 `application_id`，而实际 `create_application` 在宿舍清退失败时直接返回422，根本不会创建Application。现有测试也明确断言宿舍阻断不创建通知。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:48:Phase 2C不建议现在合并执行。当前 `requirements` 有Celery/Redis依赖，但项目设置和 `docker-compose.yml` 尚未配置Celery worker/beat。审批超时提醒还需要工作日算法、扫描窗口、重复提醒策略、幂等键和调度验收，这不是2B旁边的小补丁。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:62:- 如果不产生通知，把契约中的 `DORM_CLEARANCE_BLOCKED` 标记为 deferred 或删除自动通知承诺。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:66:- 调整当前 `test_dorm_blocked_does_not_create_notification`。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:70:- 先写Celery/无Celery两种实现决策。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:71:- 如果引入Celery beat，必须同时补配置、docker-compose服务、任务幂等测试和调度验收说明。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:83:- Phase 2C Celery beat完整方案：4-7小时
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:85:如果坚持完整2B+2C并包含Celery配置、Docker服务、幂等、防重复和测试，建议按 **5.5-8小时** 估算，而不是4-6小时。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:96:4. 再决定Phase 2C是否采用Celery beat；不要默认引入。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:111:`docs/api/notification-contract-v0.1.md` 声明宿舍阻断通知关联 `application_id`，但 `backend/apps/applications/views.py` 在宿舍清退失败时直接返回422，不创建Application。当前Application状态也没有blocked状态。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:117:`backend/apps/notifications/tests/test_auto_notifications_api.py` 中当前测试名和断言是“宿舍阻断不创建通知”。如果2B目标是创建宿舍阻断通知，必须先更新测试意图，并确认这是产品/契约层面的正式变更。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:121:项目依赖中已有Celery/Redis，但settings和docker-compose尚未配置broker、worker、beat服务。直接实现定时提醒会把任务代码、运行方式和验收证据拆散。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:129:不要现在执行完整Phase 2B-2C。先做API Schema文档状态修正，再做Phase 2B契约决策与实现。Phase 2C等2B完成后单独评审，特别是先决定是否真的引入Celery beat。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:59:- timeout细节
docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md:13:- ✅ Task 1: 修复通知type枚举值（services.py使用NotificationType枚举）
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:14:契约修正已经完成，`docs/api/notification-contract-v0.1.md` 中上一轮指出的分页、错误结构、幂等键、验收边界、测试数据路径问题已经修正到可实现状态。但这只移除了"契约质量"阻塞项，没有移除"实现授权"阻塞项。
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:21:4. **Phase 1不得包含 signals、Celery、小程序通知页、微信模板消息。**
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:63:- Notification model + migration；
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:93:`PATCH /api/notifications/{id}/read/` 建议做成幂等操作：已读通知再次标记已读仍返回 200 和当前 `read_at`。如果把"已读"当作 `VALIDATION_ERROR`，小程序重试和重复点击会变脆。
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:102:`seed_notifications` 应是 management command，不开放 `POST /api/notifications/` 给客户端。命令需要幂等或支持清理/限定用户，避免重复运行撞唯一约束导致演示失败。
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:119:   范围：Notification model/migration/API/tests/seed command，不含 signals、小程序通知页、微信模板消息。
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:133:- 新建 `backend/apps/notifications/`；
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:135:- `Notification` model，使用 `recipient`/`actor` 外键到 `AUTH_USER_MODEL`；
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:136:- `notification_id` 主键，格式 `not_` + 8位随机字符；
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:145:- `seed_notifications` 或 fixture。
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:149:- Celery；
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:164:> 通知契约已经修正到可实现状态。建议授权启动 Track 3 Phase 1 后端MVP实现，范围仅限 Django Notification模型、迁移、读取/已读API、RBAC测试和测试造数命令；不包含 signals、小程序通知页、微信模板消息。请确认是否授权启动 Phase 1。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:28:**位置：** `backend/apps/notifications/services.py:33`、`backend/apps/notifications/services.py:57-61`、`backend/apps/notifications/models.py:14-18`
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:30:`NotificationType`模型枚举值是小写字符串：
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:38:- `APPLICATION_SUBMITTED`
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:42:Django不会在普通`save()`/`get_or_create()`时自动校验`choices`，所以这类非法枚举值可以落库，并通过通知API返回。现有`test_auto_notifications.py`也断言大写值，等于把错误行为写进测试。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:52:先修正服务层使用`NotificationType.APPLICATION_SUBMITTED`等枚举值，而不是裸字符串常量名；同步修正测试断言为枚举值/小写值。这个修复应作为所有文档工作的前置门禁。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:56:**位置：** `backend/apps/notifications/tests/test_auto_notifications.py`
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:156:审批超时提醒需要定时调度、工作日计算、重复提醒窗口、幂等键或提醒周期字段。即使`celery`依赖已经在`requirements`中，生产运行的Celery beat/worker、监控和部署复杂度仍然没有准备好。当前阶段不应引入。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:186:- 修正`test_auto_notifications.py`中错误的大写断言。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:213:1. 自动通知落库`type`与`NotificationType`枚举/契约一致。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:227:> 下一步不要启动Phase 2B/2C，也不要硬停止。先修复Phase 2A自动通知的契约一致性和测试缺口，再推进Option E-lite：smoke增强、OpenAPI基线、部署文档补漏。Phase 2B只有在需要审计阻断历史时再以`application_attempt`或明确幂等语义重新设计；Phase 2C继续推迟到Celery运行方案确定后。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:235:- 尝试运行通知测试：`python3 manage.py test apps.notifications...`，本地环境缺少Django依赖，未能执行。
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:42:- Phase 1: 项目初始化（Django、Docker、Celery）
docs/discussions/phase4c-next-steps/30-claude-consensus-contract-revision-gate.md:150:   - 添加management command说明：seed_notifications
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:17:- ✅ 删除DORM_CLEARANCE_BLOCKED（契约+代码+migration）
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:18:- ✅ 修正APPLICATION_SUBMITTED实体（approval）
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:29:**范围：** 实现APPROVAL_TIMEOUT_WARNING通知（审批超时提醒）
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:32:1. 设计超时检测机制（Celery定时任务 vs Management Command）
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:46:1. 超时提醒依赖定时任务（Celery或cron），但当前环境是否配置Celery？
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:89:1. **契约承诺完整性：** notification-contract-v0.1.md定义了4种通知类型，目前已实现3种，只剩APPROVAL_TIMEOUT_WARNING
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:94:1. **定时任务依赖：** 需要先调研当前环境Celery配置状态
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:110:- 当前环境是否配置Celery？如果没有，是否应该用Management Command代替？
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:124:- 如果Phase 2B Step 2遇到技术阻塞（如Celery未配置），是否应该果断暂停？
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:133:2. 技术可行性评估（Celery/定时任务）
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:28:- 包含：定义事件类型 + 设计Notification模型 + 定义API契约
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:31:- Phase 0/1: Notification Contract Draft（2-3小时）
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:90:**交付物：** `docs/api/notification-contract-v0.1.md`
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:94:   - APPLICATION_SUBMITTED（申请提交）
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:97:   - DORM_CLEARANCE_BLOCKED（宿舍清退阻断）
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:98:   - APPROVAL_TIMEOUT_WARNING（审批超时提醒）
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:101:   - notification_id（通知ID，not_xxxxxxxx格式）
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:113:   - GET /api/notifications/（列表，分页，过滤read/unread）
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:114:   - GET /api/notifications/unread_count/（未读数）
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:115:   - PATCH /api/notifications/{id}/read/（标记单条已读）
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:116:   - POST /api/notifications/mark_all_read/（全部已读）
docs/discussions/phase4c-next-steps/23-codex-post-execution-next-steps-response.md:56:如果直接做 `Notification` 模型或 API，容易把当前阶段从“验收准备”重新带回“功能开发”。这会模糊 Phase 4C 的完成边界。
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:14:- ✅ Notification模型 + 迁移（5/5测试通过）
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:17:- ✅ seed_notifications管理命令
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:51:- 自动创建Notification记录
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:52:- 5种通知类型全覆盖（APPLICATION_SUBMITTED、APPROVAL_APPROVED、APPROVAL_REJECTED、DORM_CLEARANCE_BLOCKED、APPROVAL_TIMEOUT_WARNING）
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:61:- 超时提醒需要Celery定时任务（Phase 4推迟范围）
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:74:- 实现miniprogram/pages/notifications/列表页
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:75:- 实现miniprogram/pages/notifications/detail详情页
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:203:- 仅实现4种立即可触发的通知类型（排除APPROVAL_TIMEOUT_WARNING，需要Celery）
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:209:1. 提交申请→自动创建APPLICATION_SUBMITTED通知
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:212:4. 宿舍清退阻断→自动创建DORM_CLEARANCE_BLOCKED通知
docs/discussions/phase4c-next-steps/53-codex-confirmation-option-a-corrected.md:40:- Login、notification分页、attachment list/upload/download/delete schema必须以当前代码行为为准。
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:14:Option 1方向正确：v0.1契约删除`DORM_CLEARANCE_BLOCKED`，代码枚举删除该类型，宿舍阻断路径保持422同步失败且不创建通知。`APPLICATION_SUBMITTED`改为关联`approval/{approval_id}`也与当前实现一致。
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:27:**位置：** `backend/apps/notifications/migrations/0001_initial.py:22`
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:30:`NotificationType`模型已删除`DORM_CLEARANCE_BLOCKED`，当前模型只有4个枚举值：
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:35:- `approval_timeout_warning`
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:52:Migrations for 'notifications':
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:53:  backend/apps/notifications/migrations/0002_alter_notification_type.py
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:54:    - Alter field type on notification
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:65:如果当前迁移尚未作为稳定生产基线发布，直接同步修改`0001_initial.py`移除该choice最干净；如果迁移历史需要保持不可变，则生成并提交`0002_alter_notification_type.py`。
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:81:- `docs/api/notification-contract-v0.1.md:165`
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:82:- `docs/api/notification-contract-v0.1.md:279`
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:83:- `docs/api/notification-contract-v0.1.md:374`
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:86:契约事件表使用符号名`APPLICATION_SUBMITTED`等可以接受，但API响应示例和伪代码/ shell示例中的实际`type`值仍写成`APPROVAL_APPROVED`。当前模型和测试均使用小写落库值，例如`approval_approved`、`application_submitted`。
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:98:- `APPLICATION_SUBMITTED` -> `application_submitted`
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:107:### 1. `DORM_CLEARANCE_BLOCKED`契约删除基本完整
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:109:`docs/api/notification-contract-v0.1.md`事件枚举表已只剩4类通知，详细说明章节也不再包含宿舍阻断通知。对v0.1自动通知契约而言，这符合Option 1。
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:113:### 2. `APPLICATION_SUBMITTED`关联`approval`语义合理
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:125:- `type=NotificationType.APPLICATION_SUBMITTED`
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:127:对应位置：`backend/apps/notifications/services.py:29-33`。
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:133:`backend/apps/notifications/tests/test_auto_notifications_api.py:245-257`覆盖了三点：
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:149:rg -n "DORM_CLEARANCE_BLOCKED|dorm_clearance_blocked|宿舍清退阻断|APPLICATION_SUBMITTED|application_submitted|NotificationType" docs backend -S
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:154:- 业务代码未发现`DORM_CLEARANCE_BLOCKED`残留引用。
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:155:- `backend/apps/notifications/migrations/0001_initial.py:22`仍保留`dorm_clearance_blocked`。
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:164:结果：失败，提示会生成`0002_alter_notification_type.py`。
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:169:PYTHONPATH=. python backend/manage.py test apps.notifications.tests.test_auto_notifications apps.notifications.tests.test_auto_notifications_api --keepdb --noinput
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:183:2. 修正`notification-contract-v0.1.md`中API示例/伪代码的type实际值为小写snake_case。
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:14:- ✅ Track 3 Phase 0: Notification Contract Draft v0.1
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:60:- Django Notification模型（30分钟）
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:119:**描述：** 只实现Notification模型和迁移，不实现API，用于验证数据结构设计
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:133:- Django Notification模型
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:160:- Django Notification模型
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:177:- Celery异步任务（推迟到Phase 2）
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:222:- A. 通过POST /api/notifications/创建（需要新增创建端点）
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:25:### 1. docs/api/notification-contract-v0.1.md
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:27:**修改1：删除DORM_CLEARANCE_BLOCKED枚举行**
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:32:**修改2：修正APPLICATION_SUBMITTED关联实体**
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:38:**修改3：删除DORM_CLEARANCE_BLOCKED详细说明章节**
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:41:- 结果：APPROVAL_REJECTED和APPROVAL_TIMEOUT_WARNING之间只有一个分隔符
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:45:### 2. backend/apps/notifications/models.py
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:47:**修改：删除DORM_CLEARANCE_BLOCKED枚举**
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:49:- 操作：删除 `DORM_CLEARANCE_BLOCKED = 'dorm_clearance_blocked', '宿舍清退阻断'`
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:50:- 结果：NotificationType现在有4个枚举值
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:54:### 3. backend/apps/notifications/tests/test_auto_notifications_api.py
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:56:**修改：强化test_dorm_blocked_does_not_create_notification断言**
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:60:- 新增断言2：`Notification.objects.filter(recipient=blocked_student).count() == 0`
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:71:- notification-contract-v0.1.md的修改是否完整？
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:72:- 是否还有其他章节引用了DORM_CLEARANCE_BLOCKED需要同步修正？
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:73:- APPLICATION_SUBMITTED实体修正是否与代码实现一致？
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:78:- 是否需要检查其他文件对DORM_CLEARANCE_BLOCKED的引用？
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:81:- APPLICATION_SUBMITTED使用approval作实体是否合理？
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:91:- 是否有其他文件引用DORM_CLEARANCE_BLOCKED？
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:102:- ✅ notification-contract-v0.1.md枚举表无DORM_CLEARANCE_BLOCKED
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:103:- ✅ APPLICATION_SUBMITTED实体为approval/approval_id
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:104:- ✅ DORM_CLEARANCE_BLOCKED详细章节已删除
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:105:- ✅ models.py NotificationType只有4个枚举
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:109:- 是否有其他文件引用DORM_CLEARANCE_BLOCKED（需要grep搜索）
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:120:3. 语义合理性分析（APPLICATION_SUBMITTED实体）
backend/apps/notifications/tests/test_models.py:4:from apps.notifications.models import Notification, NotificationType, EntityType
backend/apps/notifications/tests/test_models.py:7:class NotificationModelTest(TestCase):
backend/apps/notifications/tests/test_models.py:21:    def test_create_notification(self):
backend/apps/notifications/tests/test_models.py:23:        notification = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:26:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:32:        self.assertIsNotNone(notification.notification_id)
backend/apps/notifications/tests/test_models.py:33:        self.assertTrue(notification.notification_id.startswith('not_'))
backend/apps/notifications/tests/test_models.py:34:        self.assertEqual(len(notification.notification_id), 12)
backend/apps/notifications/tests/test_models.py:35:        self.assertEqual(notification.recipient, self.student)
backend/apps/notifications/tests/test_models.py:36:        self.assertIsNone(notification.read_at)
backend/apps/notifications/tests/test_models.py:38:    def test_notification_id_auto_generated(self):
backend/apps/notifications/tests/test_models.py:39:        """测试notification_id自动生成"""
backend/apps/notifications/tests/test_models.py:40:        n1 = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:42:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_models.py:48:        n2 = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:50:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_models.py:56:        self.assertNotEqual(n1.notification_id, n2.notification_id)
backend/apps/notifications/tests/test_models.py:60:        Notification.objects.create(
backend/apps/notifications/tests/test_models.py:62:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:69:            Notification.objects.create(
backend/apps/notifications/tests/test_models.py:71:                type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:86:        n1 = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:88:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:94:        n2 = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:96:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:102:        self.assertNotEqual(n1.notification_id, n2.notification_id)
backend/apps/notifications/tests/test_models.py:106:        n1 = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:108:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_models.py:114:        n2 = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:116:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:122:        notifications = list(Notification.objects.all())
backend/apps/notifications/tests/test_models.py:123:        self.assertEqual(notifications[0].notification_id, n2.notification_id)
backend/apps/notifications/tests/test_models.py:124:        self.assertEqual(notifications[1].notification_id, n1.notification_id)
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md:28:4. Phase 2C基础设施未就绪（Celery/Redis依赖存在，但未配置）
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md:66:3. 更新`notification-contract-v0.1.md`
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md:69:**产出：** notification-contract-v0.1.md修订 + 契约决策文档
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md:81:4. 调整现有测试（test_dorm_blocked_does_not_create_notification）
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md:91:- 需要Celery beat配置（docker-compose服务、settings、broker）
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md:94:- 时间估算：2-7小时（取决于Celery vs 同步方案）
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md:126:- docs/api/notification-contract-v0.1.md（修订）
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md:130:- backend/apps/notifications/services.py（修改）
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md:131:- backend/apps/notifications/tests/（修改）
backend/apps/notifications/tests/test_auto_notifications_api.py:2:API-level tests for automatic notification creation.
backend/apps/notifications/tests/test_auto_notifications_api.py:4:Verifies that notifications created by business logic are visible through the API
backend/apps/notifications/tests/test_auto_notifications_api.py:5:and that negative paths (permission denied, status conflicts) don't create notifications.
backend/apps/notifications/tests/test_auto_notifications_api.py:13:from apps.notifications.models import Notification
backend/apps/notifications/tests/test_auto_notifications_api.py:19:class AutoNotificationAPITest(TestCase):
backend/apps/notifications/tests/test_auto_notifications_api.py:20:    """Test automatic notifications are visible through API."""
backend/apps/notifications/tests/test_auto_notifications_api.py:50:    def test_application_submitted_notification_visible_via_api(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:51:        """Test counselor can see APPLICATION_SUBMITTED notification via API after student submits."""
backend/apps/notifications/tests/test_auto_notifications_api.py:52:        # Student submits application (triggers notification)
backend/apps/notifications/tests/test_auto_notifications_api.py:60:        # Counselor checks notifications via API
backend/apps/notifications/tests/test_auto_notifications_api.py:62:        response = self.client.get('/api/notifications/')
backend/apps/notifications/tests/test_auto_notifications_api.py:65:        notifications = response.json()['results']
backend/apps/notifications/tests/test_auto_notifications_api.py:66:        self.assertEqual(len(notifications), 1)
backend/apps/notifications/tests/test_auto_notifications_api.py:67:        self.assertEqual(notifications[0]['type'], 'application_submitted')
backend/apps/notifications/tests/test_auto_notifications_api.py:68:        self.assertEqual(notifications[0]['entity_type'], 'approval')
backend/apps/notifications/tests/test_auto_notifications_api.py:69:        self.assertIn('测试学生', notifications[0]['message'])
backend/apps/notifications/tests/test_auto_notifications_api.py:71:    def test_approval_approved_notification_visible_via_api(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:72:        """Test student can see APPROVAL_APPROVED notification via API after counselor approves."""
backend/apps/notifications/tests/test_auto_notifications_api.py:93:        # Counselor approves (triggers notification)
backend/apps/notifications/tests/test_auto_notifications_api.py:100:        # Student checks notifications via API
backend/apps/notifications/tests/test_auto_notifications_api.py:102:        response = self.client.get('/api/notifications/')
backend/apps/notifications/tests/test_auto_notifications_api.py:105:        notifications = response.json()['results']
backend/apps/notifications/tests/test_auto_notifications_api.py:106:        self.assertGreaterEqual(len(notifications), 1)
backend/apps/notifications/tests/test_auto_notifications_api.py:108:        # Find the approval notification
backend/apps/notifications/tests/test_auto_notifications_api.py:109:        approval_notif = [n for n in notifications if n['type'] == 'approval_approved'][0]
backend/apps/notifications/tests/test_auto_notifications_api.py:113:    def test_approval_rejected_notification_includes_reason(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:114:        """Test APPROVAL_REJECTED notification includes rejection reason in message."""
backend/apps/notifications/tests/test_auto_notifications_api.py:142:        # Student checks notification
backend/apps/notifications/tests/test_auto_notifications_api.py:144:        response = self.client.get('/api/notifications/')
backend/apps/notifications/tests/test_auto_notifications_api.py:147:        notifications = response.json()['results']
backend/apps/notifications/tests/test_auto_notifications_api.py:148:        reject_notif = [n for n in notifications if n['type'] == 'approval_rejected'][0]
backend/apps/notifications/tests/test_auto_notifications_api.py:151:    def test_permission_denied_does_not_create_notification(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:152:        """Test that permission denied does not create spurious notifications."""
backend/apps/notifications/tests/test_auto_notifications_api.py:187:        # Verify no notification was created
backend/apps/notifications/tests/test_auto_notifications_api.py:188:        self.assertEqual(Notification.objects.filter(
backend/apps/notifications/tests/test_auto_notifications_api.py:193:    def test_status_conflict_does_not_create_notification(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:194:        """Test that status conflict (e.g., re-approving) does not create duplicate notifications."""
backend/apps/notifications/tests/test_auto_notifications_api.py:222:        # Verify only one notification exists (from initial approval, not from failed re-approval)
backend/apps/notifications/tests/test_auto_notifications_api.py:223:        self.assertEqual(Notification.objects.filter(
backend/apps/notifications/tests/test_auto_notifications_api.py:227:        ).count(), 0)  # No notification because we created approval directly, not through API
backend/apps/notifications/tests/test_auto_notifications_api.py:229:    def test_dorm_blocked_does_not_create_notification(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:230:        """Test that dorm checkout blockage does not create notifications."""
backend/apps/notifications/tests/test_auto_notifications_api.py:250:        # Verify no notification was created for the blocked student
backend/apps/notifications/tests/test_auto_notifications_api.py:251:        self.assertEqual(Notification.objects.filter(recipient=blocked_student).count(), 0)
backend/apps/notifications/tests/test_auto_notifications_api.py:253:        # Verify no notification was created for counselor
backend/apps/notifications/tests/test_auto_notifications_api.py:254:        self.assertEqual(Notification.objects.filter(
backend/apps/notifications/tests/__init__.py:1:# Notifications app tests
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:44:> - 范围：Django Notification模型、迁移、读取/已读API、RBAC测试、测试造数命令
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:60:- backend/apps/notifications/models.py（Notification模型）
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:61:- backend/apps/notifications/migrations/0001_initial.py（数据库迁移）
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:62:- backend/apps/notifications/serializers.py（NotificationSerializer）
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:63:- backend/apps/notifications/views.py（4个API端点）
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:64:- backend/apps/notifications/urls.py（URL注册）
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:65:- backend/apps/notifications/admin.py（Django admin）
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:66:- backend/apps/notifications/tests/（单元测试）
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:67:- backend/apps/notifications/management/commands/seed_notifications.py（测试造数）
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:71:- Celery异步任务（推迟到Phase 2）
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:92:4. **Seed命令隔离** - seed_notifications必须是management command，不是生产API
backend/apps/notifications/tests/test_api.py:5:from apps.notifications.models import Notification, NotificationType, EntityType
backend/apps/notifications/tests/test_api.py:8:class NotificationAPITest(TestCase):
backend/apps/notifications/tests/test_api.py:29:    def test_list_notifications(self):
backend/apps/notifications/tests/test_api.py:31:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:33:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:39:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:41:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_api.py:49:        response = self.client.get('/api/notifications/')
backend/apps/notifications/tests/test_api.py:57:        n1 = Notification.objects.create(
backend/apps/notifications/tests/test_api.py:59:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:65:        n2 = Notification.objects.create(
backend/apps/notifications/tests/test_api.py:67:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_api.py:77:        response = self.client.get('/api/notifications/?read=unread')
backend/apps/notifications/tests/test_api.py:80:        response = self.client.get('/api/notifications/?read=read')
backend/apps/notifications/tests/test_api.py:83:        response = self.client.get('/api/notifications/?read=all')
backend/apps/notifications/tests/test_api.py:89:            Notification.objects.create(
backend/apps/notifications/tests/test_api.py:91:                type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:100:        response = self.client.get('/api/notifications/?limit=2&offset=0')
backend/apps/notifications/tests/test_api.py:104:        response = self.client.get('/api/notifications/?limit=2&offset=2')
backend/apps/notifications/tests/test_api.py:109:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:111:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:117:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:119:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:127:        response = self.client.get('/api/notifications/')
backend/apps/notifications/tests/test_api.py:132:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:134:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:140:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:142:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_api.py:151:        response = self.client.get('/api/notifications/unread_count/')
backend/apps/notifications/tests/test_api.py:158:        notification = Notification.objects.create(
backend/apps/notifications/tests/test_api.py:160:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:168:        response = self.client.patch(f'/api/notifications/{notification.notification_id}/read/')
backend/apps/notifications/tests/test_api.py:173:        notification.refresh_from_db()
backend/apps/notifications/tests/test_api.py:174:        self.assertIsNotNone(notification.read_at)
backend/apps/notifications/tests/test_api.py:178:        notification = Notification.objects.create(
backend/apps/notifications/tests/test_api.py:180:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:189:        response1 = self.client.patch(f'/api/notifications/{notification.notification_id}/read/')
backend/apps/notifications/tests/test_api.py:193:        response2 = self.client.patch(f'/api/notifications/{notification.notification_id}/read/')
backend/apps/notifications/tests/test_api.py:199:        notification = Notification.objects.create(
backend/apps/notifications/tests/test_api.py:201:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:209:        response = self.client.patch(f'/api/notifications/{notification.notification_id}/read/')
backend/apps/notifications/tests/test_api.py:217:        response = self.client.patch('/api/notifications/not_99999999/read/')
backend/apps/notifications/tests/test_api.py:224:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:226:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:232:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:234:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_api.py:242:        response = self.client.post('/api/notifications/mark_all_read/')
backend/apps/notifications/tests/test_api.py:247:        unread_count = Notification.objects.filter(
backend/apps/notifications/tests/test_auto_notifications.py:2:Tests for automatic notification creation.
backend/apps/notifications/tests/test_auto_notifications.py:4:Verifies that notifications are created automatically when:
backend/apps/notifications/tests/test_auto_notifications.py:5:- Student submits application (APPLICATION_SUBMITTED)
backend/apps/notifications/tests/test_auto_notifications.py:16:from apps.notifications.models import Notification
backend/apps/notifications/tests/test_auto_notifications.py:17:from apps.notifications.services import notify_application_submitted, notify_approval_decided
backend/apps/notifications/tests/test_auto_notifications.py:22:class AutoNotificationTest(TestCase):
backend/apps/notifications/tests/test_auto_notifications.py:23:    """Test automatic notification creation."""
backend/apps/notifications/tests/test_auto_notifications.py:44:    def test_application_submitted_notification(self):
backend/apps/notifications/tests/test_auto_notifications.py:45:        """Test APPLICATION_SUBMITTED notification creation."""
backend/apps/notifications/tests/test_auto_notifications.py:65:        notification, created = notify_application_submitted(application, approval)
backend/apps/notifications/tests/test_auto_notifications.py:68:        self.assertEqual(notification.recipient, self.counselor)
backend/apps/notifications/tests/test_auto_notifications.py:69:        self.assertEqual(notification.actor, self.student)
backend/apps/notifications/tests/test_auto_notifications.py:70:        self.assertEqual(notification.type, 'application_submitted')
backend/apps/notifications/tests/test_auto_notifications.py:71:        self.assertEqual(notification.entity_type, 'approval')
backend/apps/notifications/tests/test_auto_notifications.py:72:        self.assertEqual(notification.entity_id, approval.pk)
backend/apps/notifications/tests/test_auto_notifications.py:73:        self.assertIn('测试学生', notification.message)
backend/apps/notifications/tests/test_auto_notifications.py:74:        self.assertIn('2021001', notification.message)
backend/apps/notifications/tests/test_auto_notifications.py:76:    def test_approval_approved_notification_counselor(self):
backend/apps/notifications/tests/test_auto_notifications.py:77:        """Test APPROVAL_APPROVED notification for counselor approval."""
backend/apps/notifications/tests/test_auto_notifications.py:97:        notification, created = notify_approval_decided(approval)
backend/apps/notifications/tests/test_auto_notifications.py:100:        self.assertEqual(notification.recipient, self.student)
backend/apps/notifications/tests/test_auto_notifications.py:101:        self.assertEqual(notification.actor, self.counselor)
backend/apps/notifications/tests/test_auto_notifications.py:102:        self.assertEqual(notification.type, 'approval_approved')
backend/apps/notifications/tests/test_auto_notifications.py:103:        self.assertEqual(notification.entity_type, 'approval')
backend/apps/notifications/tests/test_auto_notifications.py:104:        self.assertEqual(notification.entity_id, approval.pk)
backend/apps/notifications/tests/test_auto_notifications.py:105:        self.assertIn('辅导员', notification.message)
backend/apps/notifications/tests/test_auto_notifications.py:107:    def test_approval_approved_notification_dean(self):
backend/apps/notifications/tests/test_auto_notifications.py:108:        """Test APPROVAL_APPROVED notification for dean approval."""
backend/apps/notifications/tests/test_auto_notifications.py:128:        notification, created = notify_approval_decided(approval)
backend/apps/notifications/tests/test_auto_notifications.py:131:        self.assertEqual(notification.recipient, self.student)
backend/apps/notifications/tests/test_auto_notifications.py:132:        self.assertEqual(notification.actor, self.dean)
backend/apps/notifications/tests/test_auto_notifications.py:133:        self.assertEqual(notification.type, 'approval_approved')
backend/apps/notifications/tests/test_auto_notifications.py:134:        self.assertIn('学工部', notification.message)
backend/apps/notifications/tests/test_auto_notifications.py:136:    def test_approval_rejected_notification(self):
backend/apps/notifications/tests/test_auto_notifications.py:137:        """Test APPROVAL_REJECTED notification creation."""
backend/apps/notifications/tests/test_auto_notifications.py:158:        notification, created = notify_approval_decided(approval)
backend/apps/notifications/tests/test_auto_notifications.py:161:        self.assertEqual(notification.recipient, self.student)
backend/apps/notifications/tests/test_auto_notifications.py:162:        self.assertEqual(notification.actor, self.counselor)
backend/apps/notifications/tests/test_auto_notifications.py:163:        self.assertEqual(notification.type, 'approval_rejected')
backend/apps/notifications/tests/test_auto_notifications.py:164:        self.assertIn('驳回', notification.message)
backend/apps/notifications/tests/test_auto_notifications.py:165:        self.assertIn('材料不齐全', notification.message)
backend/apps/notifications/tests/test_auto_notifications.py:168:        """Test that repeated calls don't create duplicate notifications."""
backend/apps/notifications/tests/test_auto_notifications.py:188:        notification1, created1 = notify_application_submitted(application, approval)
backend/apps/notifications/tests/test_auto_notifications.py:191:        notification2, created2 = notify_application_submitted(application, approval)
backend/apps/notifications/tests/test_auto_notifications.py:193:        self.assertEqual(notification1.pk, notification2.pk)
backend/apps/notifications/tests/test_auto_notifications.py:195:        self.assertEqual(Notification.objects.filter(
backend/apps/notifications/tests/test_auto_notifications.py:203:        """Test that repeated approval decisions don't create duplicate notifications."""
backend/apps/notifications/tests/test_auto_notifications.py:223:        notification1, created1 = notify_approval_decided(approval)
backend/apps/notifications/tests/test_auto_notifications.py:226:        notification2, created2 = notify_approval_decided(approval)
backend/apps/notifications/tests/test_auto_notifications.py:228:        self.assertEqual(notification1.pk, notification2.pk)
backend/apps/notifications/tests/test_auto_notifications.py:230:        self.assertEqual(Notification.objects.filter(
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:72:            timeout=5
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:81:- notification_preferences（初期所有用户收到所有通知）
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:77:2. ✅ **MAJOR - is_timeout字段位置错误**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:78:   - 同意。`is_timeout`在`approvals`表，不在`applications`表
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:102:- 修正is_timeout字段位置
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:133:- 完全重写docker-compose.yml（postgres、单实例django-app、redis、celery）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:19:- 技术栈：Django 4.2 + PostgreSQL + Redis + Celery + Docker
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:35:- 6个核心模块（accounts, applications, approvals, attachments, notifications, integrations）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:38:- Celery异步任务的必要性
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:111:- PostgreSQL + Redis + Celery容器化
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:143:- Celery异步任务（通知发送、外部系统调用）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:189:+ command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 9 --max-requests 1000 --timeout 30
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:298:### 争议3：Celery异步任务
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:300:**设计文档：** 已包含Celery  
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:308:def send_notification(user_id, message):
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:328:- 如果通知发送成为瓶颈（>500ms），Phase 2引入Celery
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:364:@celery.task
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:365:def check_approval_timeout():
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:373:        send_timeout_notification(app)
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:455:- ✓ 推迟Celery实施
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:464:- 同步实现（不引入Celery）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:476:- 如果通知慢 → 引入Celery
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:35:2. Celery任务队列必要性存疑
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:143:- ❌ Celery异步任务（Phase 1同步实现）
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:163:- 如果通知发送成为瓶颈 → 引入Celery
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:284:3. **简化Phase 1设计**（推迟Celery、乐观锁、复杂工作日计算）
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:37:  --timeout 30
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:74:      timeout: 10s
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:82:      timeout: 5s
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:79:2. **MAJOR**: `app.is_timeout = True`（lines 1306-1308）与最终数据库不匹配
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:80:   - `is_timeout`字段在`approvals`表，不在`applications`表（lines 371-372）
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:133:- 重写第7章围绕：`nginx`、单个`django-app`（Gunicorn 4 workers）、`postgres`、`redis`、`celery-worker`、`celery-beat`
docs/discussions/codex-review-2026-05-27/04-database-review.md:81:SELECT * FROM notifications
docs/discussions/codex-review-2026-05-27/04-database-review.md:100:-- notifications表
docs/discussions/codex-review-2026-05-27/04-database-review.md:101:CREATE INDEX idx_user_read_time ON notifications(user_id, is_read, created_at DESC);
docs/discussions/codex-review-2026-05-27/04-database-review.md:278:### 9. notifications表缺少retry_count
docs/discussions/codex-review-2026-05-27/04-database-review.md:290:- 无`user_notification_preferences`表（所有用户收到所有通知）
docs/discussions/codex-review-2026-05-27/04-database-review.md:302:- notifications应该软删除还是90天后硬删除？
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:34:#### MAJOR - Celery任务队列必要性存疑
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:37:设计中Celery用于：通知发送、文件上传、凭证生成。但单实例部署场景下，这些任务是否真的需要异步？
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:38:- 微信通知：HTTP请求通常<500ms，是否值得引入Celery复杂度？
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:43:- 增加系统复杂度（Redis、Celery Worker、Celery Beat）
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:49:2. **性能测试后决策**：如果通知发送成为瓶颈，再引入Celery
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:76:1. **简化初期架构**：Phase 1不引入Celery，先用同步实现
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:77:2. **明确扩展路径**：文档化何时需要MinIO、何时需要Celery
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:205:部分表有`is_deleted`字段（users, applications, attachments），部分表没有（approvals, notifications）。不一致的设计增加理解成本。
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:34:@celery.task
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:35:def check_approval_timeout():
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:43:            send_timeout_notification(app)
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:51:#### MAJOR - 超时监控Celery任务每小时执行浪费资源
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:54:`check_approval_timeout()`每小时执行一次，扫描所有待审批申请。
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:66:    timeout_at = models.DateTimeField(null=True)  # 到期时间
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:69:    app.timeout_at = datetime.now() + timedelta(hours=24)
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:73:@celery.task
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:74:def check_approval_timeout():
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:76:    soon_timeout = Application.objects.filter(
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:78:        timeout_at__lte=datetime.now() + timedelta(hours=1),
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:79:        timeout_at__gt=datetime.now()
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:81:    for app in soon_timeout:
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:82:        send_timeout_notification(app)
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:179:    result = dorm_api.check_status(student_id, timeout=2)
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:186:@celery.task(max_retries=10, retry_backoff=60)
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:217:@celery.task
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:64:| MAJOR | Celery必要性存疑 | 增加复杂度 |
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:125:### 3. Celery异步任务
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:169:18. 推迟Celery实施
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:212:### 争议3：Celery是否Phase 1引入？
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:214:**设计文档：** 已包含Celery
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:221:- 如果成为瓶颈，Phase 2引入Celery
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:238:  - Celery是否Phase 1引入？
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:60:- 修正is_timeout字段位置
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:44:### 9. notifications表缺少retry_count - **同意**
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:49:class Notification(models.Model):
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:93:# Celery定时任务
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:94:@celery.task
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:108:### Q3: notifications应该软删除还是硬删除？
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:148:4. ⚠️ `user_notification_preferences` - 暂不添加（Phase 2考虑）
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:174:9. ✅ notifications添加retry_count
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:102:class Notification(models.Model):
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:5:**不在范围内：** 安装依赖、创建 Django 项目、settings 分层、Docker/Celery/开发工具配置、后端业务实现、前端实现、测试实现、部署落地等尚未完成事项
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:27:- Celery
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:64:- 缓存/队列：Redis + Celery
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:169:   Phase 1 同时包含 Django 初始化、Docker、Celery、开发工具等任务。作为计划本身没有问题，但当前已完成部分只覆盖了目录、`.gitignore`、requirements。项目总结中已经正确标注其余任务为暂停/待继续。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:250:- Celery pid/schedule
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:335:- Celery 任务实现
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:152:# notifications表
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:230:### 3.9 notifications表新增retry_count
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:311:- ⏸ user_notification_preferences表
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:11:当前仓库已经完成较完整的需求、系统设计、实施计划和多轮评审共识，核心方向基本清晰：Django + DRF 单体后端、PostgreSQL 单数据库、Redis + Celery、本地文件存储、微信登录/通知、宿舍系统优先 API 对接。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:141:- Celery/Redis
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:208:- `idx_notifications_user_id`
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:242:approvals 表字段说明写 `action: approve/reject`，但超时任务会创建 `action='timeout'`。需要把 `timeout` 加入枚举，或把超时记录拆成独立 `approval_timeouts`/notification 事件，避免审批记录语义混乱。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:555:   - base：Django/DRF/PostgreSQL/Redis/Celery/SimpleJWT/requests/python-magic/chinese-calendar/cryptography/django-redis

exec
/bin/bash -lc "rtk rg --files backend | rg 'notification|approval|application|settings|manage.py|requirements|pyproject|Pipfile|poetry|celery|task'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/requirements/base.txt
backend/requirements/dev.txt
backend/requirements/prod.txt
backend/config/settings/__init__.py
backend/config/settings/base.py
backend/config/settings/prod.py
backend/config/settings/dev.py
backend/manage.py
backend/apps/approvals/validators.py
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
backend/apps/approvals/serializers.py
backend/apps/approvals/views.py
backend/apps/approvals/models.py
backend/apps/notifications/services.py
backend/apps/applications/__init__.py
backend/apps/notifications/__init__.py
backend/apps/notifications/admin.py
backend/apps/notifications/urls.py
backend/apps/notifications/migrations/__init__.py
backend/apps/notifications/migrations/0001_initial.py
backend/apps/notifications/migrations/0002_alter_notification_type.py
backend/apps/notifications/apps.py
backend/apps/notifications/tests/__init__.py
backend/apps/notifications/tests/test_auto_notifications_api.py
backend/apps/notifications/tests/test_models.py
backend/apps/notifications/tests/test_api.py
backend/apps/notifications/tests/test_auto_notifications.py
backend/apps/notifications/views.py
backend/apps/notifications/serializers.py
backend/apps/notifications/models.py
backend/apps/notifications/management/__init__.py
backend/apps/applications/serializers.py
backend/apps/applications/models.py
backend/apps/applications/permissions.py
backend/apps/applications/views.py
backend/apps/applications/pagination.py
backend/apps/applications/urls.py
backend/apps/notifications/management/commands/seed_notifications.py
backend/apps/notifications/management/commands/__init__.py
backend/apps/applications/providers.py
backend/apps/applications/admin.py
backend/apps/applications/migrations/0003_application_unique_student_application.py
backend/apps/applications/migrations/__init__.py
backend/apps/applications/migrations/0002_initial.py
backend/apps/applications/migrations/0001_initial.py
backend/apps/applications/migrations/0004_remove_unique_student_constraint.py
backend/apps/applications/tests/test_serializer_validation.py
backend/apps/applications/tests/test_list_permissions.py
backend/apps/applications/tests/test_constraints.py
backend/apps/applications/tests/test_application_flow.py
backend/apps/applications/tests/test_error_cases.py
backend/apps/applications/tests/test_detail_permissions.py
backend/apps/applications/tests/test_p0_fixes.py
backend/apps/applications/tests/__init__.py

codex
The existing 70 response already matches the expected review artifact shape. I’m doing a quick code-level verification now so the final answer can state whether it is usable as-is or needs correction.
exec
/bin/bash -lc "rtk nl -ba backend/apps/notifications/services.py | sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""
     2	Notification service layer for idempotent notification creation.
     3	
     4	This module provides business logic for creating notifications automatically
     5	when key events occur (application submission, approval decisions).
     6	"""
     7	
     8	from django.contrib.auth import get_user_model
     9	from .models import Notification, NotificationType
    10	from apps.approvals.models import ApprovalDecision
    11	
    12	User = get_user_model()
    13	
    14	
    15	def notify_application_submitted(application, approval):
    16	    """
    17	    Create notification for counselor when student submits application.
    18	
    19	    Args:
    20	        application: Application instance
    21	        approval: Counselor approval instance
    22	
    23	    Returns:
    24	        tuple: (Notification instance, created boolean)
    25	    """
    26	    title = "新的离校申请"
    27	    message = f"学生{application.student_name}（{application.student.user_id}）提交了离校申请，请及时审批。"
    28	
    29	    return Notification.objects.get_or_create(
    30	        recipient=approval.approver,
    31	        entity_type='approval',
    32	        entity_id=approval.pk,
    33	        type=NotificationType.APPLICATION_SUBMITTED,
    34	        defaults={
    35	            'actor': application.student,
    36	            'title': title,
    37	            'message': message
    38	        }
    39	    )
    40	
    41	
    42	def notify_approval_decided(approval):
    43	    """
    44	    Create notification for student when approval is approved or rejected.
    45	
    46	    Args:
    47	        approval: Approval instance with decision
    48	
    49	    Returns:
    50	        tuple: (Notification instance, created boolean)
    51	    """
    52	    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
    53	
    54	    if approval.decision == ApprovalDecision.APPROVED:
    55	        title = "审批通过"
    56	        message = f"您的离校申请已通过{approver_role}审批。"
    57	        notification_type = NotificationType.APPROVAL_APPROVED
    58	    else:  # rejected
    59	        title = "审批驳回"
    60	        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
    61	        notification_type = NotificationType.APPROVAL_REJECTED
    62	
    63	    return Notification.objects.get_or_create(
    64	        recipient=approval.application.student,
    65	        entity_type='approval',
    66	        entity_id=approval.pk,
    67	        type=notification_type,
    68	        defaults={
    69	            'actor': approval.approver,
    70	            'title': title,
    71	            'message': message
    72	        }
    73	    )

exec
/bin/bash -lc "rtk nl -ba docker-compose.yml | sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	version: '3.8'
     2	
     3	services:
     4	  db:
     5	    image: postgres:15-alpine
     6	    environment:
     7	      POSTGRES_DB: graduation_leave
     8	      POSTGRES_USER: postgres
     9	      POSTGRES_PASSWORD: postgres
    10	    ports:
    11	      - "5432:5432"
    12	    volumes:
    13	      - postgres_data:/var/lib/postgresql/data
    14	    healthcheck:
    15	      test: ["CMD-SHELL", "pg_isready -U postgres"]
    16	      interval: 5s
    17	      timeout: 5s
    18	      retries: 5
    19	
    20	  backend:
    21	    build:
    22	      context: ./backend
    23	      dockerfile: Dockerfile
    24	    command: python manage.py runserver 0.0.0.0:8000
    25	    volumes:
    26	      - ./backend:/app
    27	      - media_data:/app/media
    28	    ports:
    29	      - "8001:8000"
    30	    env_file:
    31	      - .env.docker
    32	    depends_on:
    33	      db:
    34	        condition: service_healthy
    35	
    36	volumes:
    37	  postgres_data:
    38	  media_data:

exec
/bin/bash -lc "rtk nl -ba backend/apps/notifications/models.py | sed -n '1,140p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	import string
     2	import random
     3	from django.db import models
     4	from django.conf import settings
     5	
     6	
     7	def generate_notification_id():
     8	    """生成格式为 not_xxxxxxxx 的通知ID"""
     9	    chars = string.ascii_lowercase + string.digits
    10	    random_str = ''.join(random.choices(chars, k=8))
    11	    return f'not_{random_str}'
    12	
    13	
    14	class NotificationType(models.TextChoices):
    15	    APPLICATION_SUBMITTED = 'application_submitted', '申请已提交'
    16	    APPROVAL_APPROVED = 'approval_approved', '审批通过'
    17	    APPROVAL_REJECTED = 'approval_rejected', '审批驳回'
    18	    APPROVAL_TIMEOUT_WARNING = 'approval_timeout_warning', '审批超时提醒'
    19	
    20	
    21	class EntityType(models.TextChoices):
    22	    APPLICATION = 'application', '离校申请'
    23	    APPROVAL = 'approval', '审批记录'
    24	
    25	
    26	class Notification(models.Model):
    27	    notification_id = models.CharField(
    28	        max_length=12,
    29	        primary_key=True,
    30	        default=generate_notification_id,
    31	        editable=False,
    32	        verbose_name='通知ID'
    33	    )
    34	    recipient = models.ForeignKey(
    35	        settings.AUTH_USER_MODEL,
    36	        on_delete=models.PROTECT,
    37	        related_name='notifications_received',
    38	        verbose_name='接收者'
    39	    )
    40	    actor = models.ForeignKey(
    41	        settings.AUTH_USER_MODEL,
    42	        on_delete=models.PROTECT,
    43	        related_name='notifications_triggered',
    44	        null=True,
    45	        blank=True,
    46	        verbose_name='触发者'
    47	    )
    48	    type = models.CharField(
    49	        max_length=50,
    50	        choices=NotificationType.choices,
    51	        verbose_name='通知类型'
    52	    )
    53	    entity_type = models.CharField(
    54	        max_length=50,
    55	        choices=EntityType.choices,
    56	        verbose_name='实体类型'
    57	    )
    58	    entity_id = models.CharField(
    59	        max_length=50,
    60	        verbose_name='实体ID'
    61	    )
    62	    title = models.CharField(
    63	        max_length=200,
    64	        verbose_name='标题'
    65	    )
    66	    message = models.TextField(
    67	        verbose_name='消息内容'
    68	    )
    69	    read_at = models.DateTimeField(
    70	        null=True,
    71	        blank=True,
    72	        verbose_name='已读时间'
    73	    )
    74	    created_at = models.DateTimeField(
    75	        auto_now_add=True,
    76	        verbose_name='创建时间'
    77	    )
    78	
    79	    class Meta:
    80	        db_table = 'notifications'
    81	        verbose_name = '通知'
    82	        verbose_name_plural = '通知'
    83	        ordering = ['-created_at']
    84	        indexes = [
    85	            models.Index(fields=['recipient', 'created_at']),
    86	            models.Index(fields=['recipient', 'read_at']),
    87	        ]
    88	        constraints = [
    89	            models.UniqueConstraint(
    90	                fields=['recipient', 'entity_type', 'entity_id', 'type'],
    91	                name='unique_notification_per_recipient_entity'
    92	            )
    93	        ]
    94	
    95	    def __str__(self):
    96	        return f'{self.notification_id}: {self.title}'

exec
/bin/bash -lc "rtk nl -ba backend/config/settings/base.py | sed -n '1,160p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""
     2	Django settings for graduation leave system project.
     3	Base settings shared across all environments.
     4	"""
     5	from pathlib import Path
     6	from decouple import config
     7	from datetime import timedelta
     8	
     9	BASE_DIR = Path(__file__).resolve().parent.parent.parent
    10	
    11	SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
    12	
    13	DEBUG = config('DEBUG', default=True, cast=bool)
    14	
    15	ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])
    16	
    17	# Application definition
    18	INSTALLED_APPS = [
    19	    'django.contrib.admin',
    20	    'django.contrib.auth',
    21	    'django.contrib.contenttypes',
    22	    'django.contrib.sessions',
    23	    'django.contrib.messages',
    24	    'django.contrib.staticfiles',
    25	
    26	    # Third party
    27	    'rest_framework',
    28	    'rest_framework_simplejwt',
    29	    'corsheaders',
    30	    'django_filters',
    31	    'drf_spectacular',
    32	
    33	    # Local apps
    34	    'apps.users',
    35	    'apps.applications',
    36	    'apps.approvals',
    37	    'apps.attachments',
    38	    'apps.notifications',
    39	]
    40	
    41	MIDDLEWARE = [
    42	    'django.middleware.security.SecurityMiddleware',
    43	    'corsheaders.middleware.CorsMiddleware',
    44	    'django.contrib.sessions.middleware.SessionMiddleware',
    45	    'django.middleware.common.CommonMiddleware',
    46	    'django.middleware.csrf.CsrfViewMiddleware',
    47	    'django.contrib.auth.middleware.AuthenticationMiddleware',
    48	    'django.contrib.messages.middleware.MessageMiddleware',
    49	    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    50	]
    51	
    52	ROOT_URLCONF = 'config.urls'
    53	
    54	TEMPLATES = [
    55	    {
    56	        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    57	        'DIRS': [],
    58	        'APP_DIRS': True,
    59	        'OPTIONS': {
    60	            'context_processors': [
    61	                'django.template.context_processors.debug',
    62	                'django.template.context_processors.request',
    63	                'django.contrib.auth.context_processors.auth',
    64	                'django.contrib.messages.context_processors.messages',
    65	            ],
    66	        },
    67	    },
    68	]
    69	
    70	WSGI_APPLICATION = 'config.wsgi.application'
    71	
    72	# Database
    73	DATABASES = {
    74	    'default': {
    75	        'ENGINE': 'django.db.backends.postgresql',
    76	        'NAME': config('DB_NAME', default='graduation_leave'),
    77	        'USER': config('DB_USER', default='postgres'),
    78	        'PASSWORD': config('DB_PASSWORD', default='postgres'),
    79	        'HOST': config('DB_HOST', default='localhost'),
    80	        'PORT': config('DB_PORT', default='5432'),
    81	    }
    82	}
    83	
    84	# Custom user model
    85	AUTH_USER_MODEL = 'users.User'
    86	
    87	# Password validation
    88	AUTH_PASSWORD_VALIDATORS = [
    89	    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    90	    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    91	    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    92	    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    93	]
    94	
    95	# Internationalization
    96	LANGUAGE_CODE = 'zh-hans'
    97	TIME_ZONE = 'Asia/Shanghai'
    98	USE_I18N = True
    99	USE_TZ = True
   100	
   101	# Static files
   102	STATIC_URL = 'static/'
   103	STATIC_ROOT = BASE_DIR / 'staticfiles'
   104	
   105	# Media files
   106	MEDIA_URL = '/media/'
   107	MEDIA_ROOT = BASE_DIR / 'media'
   108	
   109	# Default primary key field type
   110	DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
   111	
   112	# REST Framework
   113	REST_FRAMEWORK = {
   114	    'DEFAULT_AUTHENTICATION_CLASSES': (
   115	        'rest_framework_simplejwt.authentication.JWTAuthentication',
   116	    ),
   117	    'DEFAULT_PERMISSION_CLASSES': (
   118	        'rest_framework.permissions.IsAuthenticated',
   119	    ),
   120	    'DEFAULT_RENDERER_CLASSES': (
   121	        'rest_framework.renderers.JSONRenderer',
   122	    ),
   123	    'DEFAULT_PARSER_CLASSES': (
   124	        'rest_framework.parsers.JSONParser',
   125	    ),
   126	    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
   127	    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
   128	}
   129	
   130	# API Documentation
   131	SPECTACULAR_SETTINGS = {
   132	    'TITLE': '毕业生离校申请审批系统 API',
   133	    'DESCRIPTION': '毕业生离校申请审批系统后端API文档',
   134	    'VERSION': '1.0.0',
   135	    'SERVE_INCLUDE_SCHEMA': False,
   136	    'COMPONENT_SPLIT_REQUEST': True,
   137	}
   138	
   139	# JWT Settings
   140	SIMPLE_JWT = {
   141	    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
   142	    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
   143	    'ROTATE_REFRESH_TOKENS': False,
   144	    'BLACKLIST_AFTER_ROTATION': False,
   145	    'ALGORITHM': 'HS256',
   146	    'SIGNING_KEY': SECRET_KEY,
   147	    'AUTH_HEADER_TYPES': ('Bearer',),
   148	    'USER_ID_FIELD': 'user_id',
   149	    'USER_ID_CLAIM': 'user_id',
   150	}
   151	
   152	# CORS Settings
   153	CORS_ALLOWED_ORIGINS = config(
   154	    'CORS_ALLOWED_ORIGINS',
   155	    default='http://localhost:3000,http://127.0.0.1:3000',
   156	    cast=lambda v: [s.strip() for s in v.split(',')]
   157	)

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/models.py | sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.db import models
     2	from apps.users.models import User
     3	from apps.applications.models import Application
     4	
     5	
     6	class ApprovalStep(models.TextChoices):
     7	    COUNSELOR = 'counselor', '辅导员'
     8	    DEAN = 'dean', '学工部'
     9	
    10	
    11	class ApprovalDecision(models.TextChoices):
    12	    PENDING = 'pending', '待审批'
    13	    APPROVED = 'approved', '已通过'
    14	    REJECTED = 'rejected', '已驳回'
    15	
    16	
    17	class Approval(models.Model):
    18	    approval_id = models.CharField(max_length=50, primary_key=True)
    19	    application = models.ForeignKey(Application, on_delete=models.PROTECT, related_name='approvals')
    20	    step = models.CharField(max_length=20, choices=ApprovalStep.choices)
    21	    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals')
    22	    approver_name = models.CharField(max_length=100)
    23	    decision = models.CharField(max_length=20, choices=ApprovalDecision.choices, default=ApprovalDecision.PENDING)
    24	    comment = models.TextField(null=True, blank=True)
    25	    decided_at = models.DateTimeField(null=True, blank=True)
    26	    created_at = models.DateTimeField(auto_now_add=True)
    27	    updated_at = models.DateTimeField(auto_now=True)
    28	
    29	    class Meta:
    30	        db_table = 'approvals'

exec
/bin/bash -lc "rtk nl -ba backend/requirements/base.txt | sed -n '1,80p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# Django Core
     2	Django==4.2.13
     3	djangorestframework==3.14.0
     4	djangorestframework-simplejwt==5.3.1
     5	django-cors-headers==4.3.1
     6	django-filter==23.5
     7	drf-spectacular==0.27.1
     8	
     9	# Database
    10	psycopg2-binary==2.9.9
    11	
    12	# State Machine
    13	django-fsm==2.8.1
    14	
    15	# Celery
    16	celery==5.3.6
    17	redis==5.0.3
    18	
    19	# WeChat
    20	wechatpy==1.8.18
    21	
    22	# Retry
    23	tenacity==8.2.3
    24	
    25	# Password
    26	bcrypt==4.1.2
    27	
    28	# Environment
    29	python-decouple==3.8
    30	
    31	# Utils
    32	python-dateutil==2.9.0
    33	pytz==2024.1
    34	
    35	# File Processing
    36	python-magic==0.4.27
    37	
    38	# Work Day Calculation
    39	chinese-calendar==1.9.0
    40	
    41	# HTTP Client
    42	requests==2.31.0
    43	
    44	# Encryption
    45	cryptography==42.0.5
    46	
    47	# Cache
    48	django-redis==5.4.0

codex
已审查 [69-claude-post-phase2b-step1-next-strategy.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md)，并确认现有 [70-codex-post-phase2b-step1-next-strategy-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md) 可以作为 Codex 审查响应使用，无需改写。

核心结论：推荐 **B-mini -> 降级版 Option A**。先不要直接上 Celery/beat，也不要切换 Track；下一步应把审批超时提醒收窄为 `service + management command + tests`，实现一次性、幂等的 `APPROVAL_TIMEOUT_WARNING`，调度基础设施后置。

我验证了代码证据：`celery`/`redis` 只是依赖存在于 [base.txt](/home/caohui/projects/graduation-leave-system/backend/requirements/base.txt:15)，但 [docker-compose.yml](/home/caohui/projects/graduation-leave-system/docker-compose.yml:3) 只有 `db` 和 `backend`，settings 中也没有 Celery 配置；同时 `Notification` 已有超时枚举和幂等唯一约束，适合 Management Command 方案：[models.py](/home/caohui/projects/graduation-leave-system/backend/apps/notifications/models.py:14)、[models.py](/home/caohui/projects/graduation-leave-system/backend/apps/notifications/models.py:88)。
tokens used
36,408

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
