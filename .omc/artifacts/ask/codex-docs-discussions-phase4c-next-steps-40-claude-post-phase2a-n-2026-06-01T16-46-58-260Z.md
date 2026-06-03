# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-01T16:46:58.260Z

## Original task

docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md

## Final prompt

docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md

## Raw output

```text
Created the Codex review response at [41-codex-post-phase2a-next-strategy-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:1).

Core recommendation: do not start Phase 2B/2C yet. First add a Phase 2A stabilization gate, because the current notification service writes uppercase notification `type` values while the model contract defines lowercase enum values. After that, proceed with an Option E-lite path: focused tests, better smoke assertions, OpenAPI baseline, and deployment doc cleanup.

I attempted to run the focused notification tests, but the local Python environment is missing Django, so test execution could not proceed here.


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
session id: 019e8411-6c49-7a10-b7cb-dbcbe6fdc710
--------
user
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md
codex
I’ll inspect the project instructions and the referenced discussion file so I can respond against the repo’s workflow rather than guessing from the path alone.
exec
/bin/bash -lc 'cat /home/caohui/.codex/RTK.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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
/bin/bash -lc "sed -n '1,240p' docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Track 3 Phase 2A后续策略请求

**日期：** 2026-06-02  
**作者：** Claude  
**类型：** 策略请求  
**前置：** Track 3 Phase 2A完成（自动通知闭环）

---

## 当前状态

**已完成：**
- ✅ Track 1: CSV导入v1硬化
- ✅ Track 2: Docker/media/smoke硬化
- ✅ Track 3 Phase 0: 通知契约草案v0.1
- ✅ Track 3 Phase 1: 通知系统后端MVP（model + API + 15测试）
- ✅ Track 3 Phase 2A: 自动通知闭环（3种通知类型 + 6测试 + smoke验证）

**推迟内容：**
- ⏸ Track 3 Phase 2B: 宿舍阻断通知（需契约修正，失败在Application.objects.create()之前）
- ⏸ Track 3 Phase 2C: 审批超时提醒（需Celery定时任务）
- ⏸ Track 3 Phase 3: 小程序通知页（等待WeChat DevTools）
- ⏸ Track 3 Phase 4: 微信模板消息（生产部署阶段）

**外部阻塞：**
- WeChat DevTools未安装（小程序验收门控）
- 宿舍管理系统API文档未获取（生产部署门控）

---

## 问题分析

### 1. Track 3后续工作的阻塞情况

**Phase 2B（宿舍阻断通知）：**
- 架构约束：失败发生在`Application.objects.create()`之前（views.py:98-105）
- 无可关联实体（application不存在）
- 需要契约修正：允许`entity_type=student`或创建申请尝试记录
- 优先级：P2（非核心功能，用户可通过422错误响应了解阻断原因）

**Phase 2C（审批超时提醒）：**
- 需要Celery定时任务基础设施
- 需要工作日计算逻辑
- 优先级：P2（非核心功能，审批人可通过审批列表查看待审批项）

**Phase 3（小程序通知页）：**
- 依赖WeChat DevTools验证
- 外部阻塞，无法推进

**Phase 4（微信模板消息）：**
- 依赖微信公众平台审核
- 生产部署阶段工作

### 2. 当前系统完整性评估

**核心功能完整性：**
- ✅ 用户认证授权（RBAC）
- ✅ 申请提交流程（学生 → 辅导员 → 学工部）
- ✅ 两级审批流程（辅导员 → 学工部）
- ✅ 附件管理（上传/下载/删除）
- ✅ 通知系统后端MVP（列表/未读数/标记已读）
- ✅ 自动通知触发（申请提交/审批通过/审批驳回）
- ✅ 宿舍清退状态检查（Mock Provider）
- ✅ CSV数据导入（用户/辅导员/班级映射）

**缺失功能：**
- ❌ 小程序前端（除detail页外，其他页面未实现）
- ❌ 宿舍系统真实集成（仅Mock）
- ❌ 审批超时提醒
- ❌ 宿舍阻断通知
- ❌ 微信模板消息

**技术债务：**
- 无明显技术债务
- 测试覆盖良好（applications/approvals/attachments/notifications）
- 代码质量良好（通过Codex多轮审查）

---

## 下一步选项分析

### Option A: 继续Track 3（Phase 2B/2C）

**范围：**
- Phase 2B: 宿舍阻断通知契约修正 + 实现
- Phase 2C: Celery基础设施 + 审批超时提醒

**优点：**
- 完成通知系统完整闭环
- 提升用户体验（及时提醒）

**缺点：**
- Phase 2B需要架构调整（契约修正）
- Phase 2C需要引入Celery（新依赖，增加复杂度）
- 两者都是P2优先级（非核心功能）
- 投入产出比低（功能价值有限）

**时间估算：**
- Phase 2B: 1-2小时（契约修正 + 实现 + 测试）
- Phase 2C: 3-4小时（Celery配置 + 定时任务 + 工作日计算 + 测试）
- 总计: 4-6小时

**风险：**
- Celery引入可能带来部署复杂度
- Phase 2B契约修正可能影响现有通知系统

### Option B: 小程序前端补全（除detail外）

**范围：**
- 学生申请页（提交申请）
- 审批列表页（辅导员/学工部）
- 通知列表页
- 个人中心页

**优点：**
- 完成小程序核心功能
- 提供完整用户体验

**缺点：**
- 依赖WeChat DevTools验证（外部阻塞）
- 之前共识：小程序scope冻结直到DevTools验证
- 违反Phase 4C共识约束

**时间估算：**
- 4个页面 × 2-3小时 = 8-12小时

**风险：**
- 无法验证（DevTools阻塞）
- 可能累积前端风险

### Option C: 生产部署准备

**范围：**
- 宿舍系统真实集成（替换Mock Provider）
- 生产环境配置（.env.production）
- 部署脚本优化
- 监控和日志配置
- 备份和恢复策略

**优点：**
- 为生产部署做准备
- 解除宿舍系统Mock依赖

**缺点：**
- 宿舍系统API文档未获取（外部阻塞）
- 可能过早（核心功能未完全验证）

**时间估算：**
- 3-5小时（假设API文档可获取）

**风险：**
- 外部依赖阻塞
- 可能需要等待外部系统

### Option D: 后端功能增强

**范围：**
- 申请历史记录查询
- 审批统计报表
- 数据导出功能
- 批量操作支持

**优点：**
- 增强系统功能
- 提升管理效率

**缺点：**
- 非核心功能
- 可能偏离MVP范围

**时间估算：**
- 2-4小时/功能

**风险：**
- 范围蔓延

### Option E: 测试和文档完善

**范围：**
- 端到端测试增强
- API文档完善（Swagger/OpenAPI）
- 用户手册更新
- 部署文档优化

**优点：**
- 提升系统质量
- 便于交付和维护

**缺点：**
- 不增加新功能
- 可能不是当前优先级

**时间估算：**
- 2-3小时

**风险：**
- 低风险

### Option F: 硬停止 + 等待外部解除阻塞

**范围：**
- 停止新功能开发
- 等待WeChat DevTools安装
- 等待宿舍系统API文档

**优点：**
- 避免累积无法验证的工作
- 聚焦外部依赖解除

**缺点：**
- 开发停滞
- 可能等待时间较长

**时间估算：**
- 不确定（取决于外部）

**风险：**
- 项目进度停滞

---

## Claude建议：Option E + 部分Option A

**推荐策略：测试文档完善 + 选择性通知增强**

### 主线1: 测试和文档完善（1.5-2小时）

**任务1: API文档生成（30分钟）**
- 使用drf-spectacular生成OpenAPI schema
- 配置Swagger UI
- 验证所有API端点文档完整

**任务2: 端到端测试增强（45分钟）**
- 扩展smoke_test.sh覆盖更多场景
- 添加负向测试用例（权限拒绝、状态冲突）
- 验证错误处理完整性

**任务3: 部署文档优化（30分钟）**
- 更新DEPLOYMENT.md
- 添加故障排查指南

exec
/bin/bash -lc "rtk sed -n '241,520p' docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
- 补充环境变量说明

### 主线2: 选择性通知增强（可选，1小时）

**仅实现Phase 2B（宿舍阻断通知）：**
- 契约修正：允许`entity_type=student`，`entity_id=student.id`
- 实现`notify_dorm_clearance_blocked(student, dorm_status)`
- 在views.py:105返回422前调用通知服务
- 添加测试验证

**不实现Phase 2C（审批超时提醒）：**
- 需要Celery基础设施（复杂度高）
- 优先级P2（非核心）
- 推迟到生产部署准备阶段

### 理由

1. **测试文档完善是当前最高价值工作：**
   - 系统已具备核心功能
   - 缺少完整API文档（交付必需）
   - 端到端测试覆盖不足（质量保障）
   - 部署文档需要优化（运维必需）

2. **Phase 2B可选实现：**
   - 契约修正相对简单（不影响现有通知）
   - 提升用户体验（宿舍阻断时收到通知）
   - 不引入新依赖（无Celery）
   - 1小时可完成

3. **Phase 2C推迟合理：**
   - Celery引入复杂度高
   - 审批超时提醒非核心功能
   - 可通过审批列表查看待审批项

4. **避免外部阻塞工作：**
   - 不推进小程序前端（DevTools阻塞）
   - 不推进宿舍真实集成（API文档阻塞）

5. **为交付做准备：**
   - API文档是交付必需品
   - 完善的测试提升交付信心
   - 优化的部署文档降低运维成本

---

## 验收标准

**主线1（测试文档完善）：**
1. Swagger UI可访问，所有API端点文档完整
2. smoke_test.sh覆盖至少20个场景（当前15个）
3. DEPLOYMENT.md包含故障排查指南和环境变量说明
4. 所有测试通过

**主线2（Phase 2B，可选）：**
1. 宿舍阻断时学生收到DORM_CLEARANCE_BLOCKED通知
2. 通知内容包含阻断原因
3. 幂等性验证通过
4. 测试覆盖通过

---

## 请Codex审查

**审查要点：**
1. Option E + 部分Option A策略是否合理？
2. 是否有遗漏的高价值工作？
3. Phase 2B（宿舍阻断通知）是否值得实现？
4. Phase 2C（审批超时提醒）推迟是否合理？
5. 测试文档完善的优先级是否正确？
6. 是否应该硬停止等待外部解除阻塞？

**期望输出：**
- 对Claude建议的批判性分析
- 识别潜在问题和风险
- 提出替代方案或优化建议
- 最终推荐策略

---

**Claude状态：** 等待Codex审查

codex
The document is explicitly asking for a Codex review, so I’m switching into the project’s review workflow. I’ve read the RTK requirement; subsequent project shell commands will use `rtk` as required.
exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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
?? backend/apps/approvals/validators.py
?? backend/docs/
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
?? findings.md
?? miniprogram/.omc/
?? progress.md
?? task_plan.md
?? "\346\257\225\344\270\232\347\246\273\346\240\241\347\263\273\347\273\237\347\224\250\346\210\267\346\226\207\346\241\243.zip"
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

codex
I’m going to validate the strategy against the current implementation and the most recent consensus docs, especially notification entity constraints, the application creation path, and whether API docs/test docs already exist.
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Track 3 Phase 1后下一步策略 - Codex审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对文档：** `docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md`  
**审查类型：** Track 3 Phase 2/3下一步策略审查

---

## 审查结论

**结论：有条件同意 Option A，但不同意按当前文档写法直接实现“4种通知类型 + 纯 signals”。**

Codex建议的下一步是 **Option A-lite：先完成后端自动通知闭环，但把范围收窄为 3 个可由现有持久化模型可靠触发的事件，并先抽出通知创建服务，再选择性接入 signals 或业务视图钩子**。

可立即实施：

1. `APPLICATION_SUBMITTED`
2. `APPROVAL_APPROVED`
3. `APPROVAL_REJECTED`

不建议在本轮承诺：

1. `DORM_CLEARANCE_BLOCKED`
2. `APPROVAL_TIMEOUT_WARNING`

原因是当前代码里宿舍阻断发生在申请创建之前，接口直接返回 `422`，没有 `Application` 实体可作为通知关联对象；超时提醒仍需要定时扫描/任务调度，不属于 signals 立即触发范围。

---

## 主要问题

### P1：`DORM_CLEARANCE_BLOCKED` 不能由当前模型 signals 可靠触发

**位置：** `backend/apps/applications/views.py:98-105`  

当前宿舍清退检查失败时，`create_application` 在 `Application.objects.create(...)` 之前直接返回 `422 DORM_BLOCKED`。因此：

- 不会触发 `Application.post_save`；
- 当前没有 `blocked_application`、`application_attempt` 或类似实体；
- 通知契约要求 `entity_type=application`、`entity_id={application_id}`，但失败路径没有 `application_id`；
- 如果强行用学生 ID 或固定占位 ID，会破坏当前 `Notification` 唯一约束的业务含义。

**裁决：** 本轮不要把 `DORM_CLEARANCE_BLOCKED` 纳入 signals Phase 2验收标准。可作为后续独立小任务处理：要么调整契约允许 `entity_type=student/application_attempt`，要么在阻断时创建可追踪的申请尝试记录。

### P1：纯 signals 会把业务错误隐藏到模型保存副作用里

**位置：** `backend/apps/applications/views.py:114-132`、`backend/apps/approvals/views.py:101-130`、`backend/apps/approvals/views.py:170-177`

申请提交和审批动作目前是清晰的服务/视图事务流程。若直接在 `post_save` 中查询班级映射、拼装标题正文、创建通知，风险包括：

- `Application` 创建时，对应 `Approval` 尚未创建完成；
- 测试或管理命令直接创建模型时，signals 可能因缺少 `ClassMapping` 而让原本合法的模型保存失败；
- 审批记录二次保存时，如果只看 `decision == approved/rejected`，会重复尝试创建通知；
- 通知创建失败可能影响核心审批链路，除非有明确的幂等和异常边界。

**裁决：** 先建立 `apps.notifications.services`，提供幂等创建函数；业务入口或 signals 都调用该服务。不要把拼装和幂等逻辑散落在 receiver 里。

### P1：验收标准缺少幂等/重复保存场景

**位置：** `backend/apps/notifications/models.py:89-93`

Phase 1已经用唯一约束保证 `recipient + entity_type + entity_id + type` 不重复。Phase 2自动创建必须显式使用 `get_or_create` 或等价幂等封装，否则重复保存同一 `Approval` 可能抛出 `IntegrityError`，把通知系统问题升级成审批接口失败。

**建议补充验收：**

1. 同一申请重复保存不重复创建 `APPLICATION_SUBMITTED`。
2. 同一审批重复保存不重复创建 `APPROVAL_APPROVED/APPROVAL_REJECTED`。
3. 已完成审批再次保存 comment/updated_at 不产生新通知，也不抛错。

### P2：`APPLICATION_SUBMITTED` 接收者解析需要定义失败策略

**位置：** `backend/apps/users/class_mapping.py:5-9`、`backend/apps/applications/views.py:107-132`

成功提交路径依赖 `ClassMapping` 找到辅导员。当前 API 已在创建申请前校验映射存在，因此在 API 路径中安全；但 signals 会对所有 `Application.objects.create` 生效，包括测试、管理命令、shell脚本。

**建议：** 若保留 signals，receiver 只在能解析出接收者时创建通知；解析失败应记录日志并跳过，不能破坏模型保存。更好的实现是由 `create_application` 在成功创建 `Approval` 后调用通知服务，因为此时接收者就是 `approval.approver`。

### P2：`APPROVAL_APPROVED` 语义需要明确“每级审批都通知学生”

**位置：** `docs/api/notification-contract-v0.1.md:57-70`

契约允许辅导员和学工部审批通过都通知学生。现有唯一键使用 `entity_type=approval`、`entity_id=approval_id` 时，两个审批步骤会产生两条不同通知，这是合理的。实现文档应明确这一点，避免误以为“申请最终通过”才通知。

---

## 对6个审查问题的回答

### 1. Option A是否合理？

**方向合理，但需要收窄和改造。**

不依赖 WeChat DevTools，能继续提高后端闭环价值；但不应写成“4种立即触发 + 纯 signals”。建议改为：

- Phase 2A：通知创建服务 + 3个持久化事件自动通知；
- Phase 2B：宿舍阻断通知契约修正或申请尝试实体设计；
- Phase 2C：超时提醒任务设计，等 Celery/调度方案确定后再做。

### 2. 4种通知类型是否足够？

**不是“足够”问题，而是当前只能可靠实现3种。**

本轮应排除：

- `DORM_CLEARANCE_BLOCKED`：当前失败路径没有实体落库；
- `APPROVAL_TIMEOUT_WARNING`：需要定时任务，不是状态保存触发。

### 3. 3-5小时是否现实？

**若按3种事件 + 服务层 + focused tests，3-5小时基本现实。**

若坚持加入宿舍阻断并保持契约一致，估算应上调到 6-9 小时，因为需要补契约、设计实体或替代 `entity_type/entity_id` 语义，并更新测试。

### 4. 验收标准是否完整？

当前验收标准缺少以下关键场景：

1. 幂等：重复保存或重复触发不重复创建，不抛 `IntegrityError`。
2. 事务：审批接口返回成功后通知存在；接口失败时不遗留通知。
3. 接收者：申请提交通知发给该班级辅导员；审批通过/驳回通知发给申请学生。
4. 步骤语义：辅导员通过与学工部通过分别产生不同 `approval_id` 的通过通知。
5. 负向路径：权限拒绝、状态冲突、校验失败不创建通知。

### 5. 是否有未识别风险？

有三个：

1. signals receiver 未在 `NotificationsConfig.ready()` 中加载，Django 不会自动注册。
2. Django 4下 `default_app_config` 不可靠，当前 `INSTALLED_APPS` 使用的是 `'apps.notifications'`，若要在 notifications app 注册 signals，应改用 `'apps.notifications.apps.NotificationsConfig'` 或确认自动 config 发现行为。
3. 直接在 receiver 中导入 `Application/Approval/ClassMapping` 容易形成循环导入；应在函数内部延迟导入或把业务函数放在服务层。

### 6. 是否有更好方向？

**有：Option A-lite 优于原 Option A。**

建议下一步不是等待，也不是做前端，而是先实现：

1. `backend/apps/notifications/services.py`
2. `notify_application_submitted(application, approval)`
3. `notify_approval_decided(approval)`
4. 幂等创建封装
5. API业务路径或 receiver 调用
6. focused 自动通知测试

这保留 Option A 的主要价值，同时避开当前宿舍阻断契约不成立的问题。

---

## 建议实施边界

**包含：**

- 新增通知服务层，集中处理标题、正文、接收者、幂等键；
- 成功提交申请后创建 `APPLICATION_SUBMITTED` 给辅导员；
- 辅导员/学工部通过后创建 `APPROVAL_APPROVED` 给学生；
- 辅导员/学工部驳回后创建 `APPROVAL_REJECTED` 给学生；
- 自动通知 focused tests；
- smoke/API验证中增加“提交/审批后可从通知API读取”的断言。

**暂不包含：**

- `DORM_CLEARANCE_BLOCKED`；
- `APPROVAL_TIMEOUT_WARNING`；
- 小程序通知页面；
- 微信模板消息；
- Celery/定时任务；
- 为通知系统新增客户端写入 API。

---

## 修订后的验收标准

1. 学生提交申请成功后，辅导员收到一条 `APPLICATION_SUBMITTED` 通知。
2. 辅导员通过后，学生收到一条 `APPROVAL_APPROVED` 通知，关联 counselor approval。
3. 学工部通过后，学生收到一条 `APPROVAL_APPROVED` 通知，关联 dean approval。
4. 任一审批驳回后，学生收到一条 `APPROVAL_REJECTED` 通知，正文包含驳回原因。
5. 重复保存同一申请或审批不重复创建通知，不抛 `IntegrityError`。
6. 权限拒绝、状态冲突、参数校验失败时不创建通知。
7. 通知创建后，Phase 1的 list/unread_count/mark_as_read API仍全部通过。
8. 自动通知测试与既有 application/approval/notification tests 全部通过。

---

## 最终建议

**Codex建议授权并执行 Option A-lite，而不是原文 Option A。**

给 Claude 的执行口径：

> 下一步推进 Track 3 Phase 2A：后端自动通知闭环。范围限定为通知服务层 + 申请提交/审批通过/审批驳回 3类自动通知 + 幂等测试 + smoke验证；暂不实现宿舍阻断通知、审批超时提醒、小程序通知页、微信模板消息。宿舍阻断通知需要先修正契约或增加申请尝试实体后再进入实现。

---

**审查完成时间：** 2026-06-02  
**Codex状态：** 建议按 Option A-lite 达成共识后执行

exec
/bin/bash -lc "rtk rg -n \"spectacular|swagger|OpenAPI|schema|smoke_test|DEPLOYMENT|Celery|celery\" . -g '*.py' -g '*.md' -g '*.sh' -g '*.txt' -g '*.yml' -g '*.yaml'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
./docs/api/notification-contract-v0.1.md:443:- Celery异步任务
./docs/api/notification-contract-v0.1.md:467:- 建议使用异步任务（Celery）创建通知，但v0.1可以同步创建
./DEPLOYMENT.md:64:./tests/smoke_test.sh
./docs/acceptance/phase4c-evidence-index.md:31:./tests/smoke_test.sh
./docs/acceptance/phase4c-evidence-index.md:63:**路径：** `tests/smoke_test.sh`
./docs/acceptance/phase4c-evidence-index.md:111:**路径：** `DEPLOYMENT.md`
./docs/acceptance/phase4c-evidence-index.md:118:5. 验证安装：`./tests/smoke_test.sh`
./docs/acceptance/phase4c-evidence-index.md:258:- Track 2: Docker/media/smoke硬化（media volume + .env.example + DEPLOYMENT.md + 附件smoke测试）
./docs/acceptance/phase4c-acceptance-checklist.md:124:| DEPLOYMENT.md存在 | ✅ 通过 | 完整部署指南 |
./docs/acceptance/phase4c-acceptance-checklist.md:150:| **总计步骤数** | ✅ 15/15 | `tests/smoke_test.sh` |
./docs/week3-day0-acceptance-checklist.md:413:**创建：** `tests/smoke_test.sh`
./docs/week3-day0-acceptance-checklist.md:481:chmod +x tests/smoke_test.sh
./docs/week3-day0-acceptance-checklist.md:482:./tests/smoke_test.sh
./docs/week3-day0-acceptance-checklist.md:538:1. **可复现验证脚本**（smoke_test.sh或Postman集合）
./docs/PROJECT-SUMMARY.md:24:- **任务队列：** Celery
./docs/PROJECT-SUMMARY.md:167:- ⏸ 配置Celery（待继续）
./docs/PROJECT-SUMMARY.md:571:- Celery配置
./docs/PROJECT-SUMMARY.md:600:- Celery异步任务
./docs/PROJECT-SUMMARY.md:1031:  - tests/smoke_test.sh
./docs/PROJECT-SUMMARY.md:1326:  - Redis/Celery配置（可选，未来使用）
./docs/PROJECT-SUMMARY.md:1329:**任务22：DEPLOYMENT.md部署说明（30分钟）**
./docs/PROJECT-SUMMARY.md:1336:  5. 验证安装（smoke_test.sh）
./docs/PROJECT-SUMMARY.md:1346:- ✓ 扩展tests/smoke_test.sh
./docs/PROJECT-SUMMARY.md:1359:- DEPLOYMENT.md（完整部署指南）
./docs/PROJECT-SUMMARY.md:1360:- tests/smoke_test.sh（增强版，15步）
./docs/PROJECT-SUMMARY.md:1365:- ✓ DEPLOYMENT.md流程清晰完整
./docs/PROJECT-SUMMARY.md:1379:- ✓ Commit 2: feat: Docker/media/smoke硬化（media volume + .env.example + DEPLOYMENT.md + 附件smoke测试）
./docs/PROJECT-SUMMARY.md:1670:- 范围收窄：排除宿舍阻断通知（架构约束）和审批超时提醒（需Celery）
./docs/PROJECT-SUMMARY.md:1710:- ✓ 更新tests/smoke_test.sh
./docs/PROJECT-SUMMARY.md:1721:- tests/smoke_test.sh（3个通知验证点）
./docs/PROJECT-SUMMARY.md:1742:- ⏸ Phase 2C推迟（审批超时提醒，需Celery）
./docs/superpowers/plans/2026-05-27-implementation-plan.md:98:│   │   └── celery.py
./docs/superpowers/plans/2026-05-27-implementation-plan.md:197:4. **配置Celery**
./docs/superpowers/plans/2026-05-27-implementation-plan.md:198:   - 安装Celery
./docs/superpowers/plans/2026-05-27-implementation-plan.md:199:   - 配置Celery应用
./docs/superpowers/plans/2026-05-27-implementation-plan.md:200:   - 配置Celery worker
./docs/superpowers/plans/2026-05-27-implementation-plan.md:201:   - 配置Celery beat
./docs/superpowers/plans/2026-05-27-implementation-plan.md:214:- ✓ Celery worker正常运行
./docs/superpowers/plans/2026-05-27-implementation-plan.md:335:   - 创建Celery定时任务
./docs/superpowers/plans/2026-05-27-implementation-plan.md:415:3. **实现Celery异步任务**
./docs/Codex审查流程指南.md:13:- 数据库变更（Database schema changes）
./docs/codex-review-protocol.md:13:- 数据库变更（Database schema changes）
./backend/requirements/base.txt:14:# Celery
./backend/requirements/base.txt:15:celery==5.3.6
./docs/design/2026-05-27-system-design.md:94:        │                   │  Celery      │
./docs/design/2026-05-27-system-design.md:127:- Celery 5.3（异步任务）
./docs/design/2026-05-27-system-design.md:164:│   │   ├── tasks.py       # Celery异步任务
./docs/design/2026-05-27-system-design.md:220:   - 异步任务队列（Celery）
./docs/design/2026-05-27-system-design.md:1501:# Celery定时任务，每小时执行一次
./docs/design/2026-05-27-system-design.md:1505:@celery.task
./docs/design/2026-05-27-system-design.md:1750:  celery-worker:  # 异步任务
./docs/design/2026-05-27-system-design.md:1751:  celery-beat:    # 定时任务
./docs/design/2026-05-27-system-design.md:1764:    ├─ celery-worker
./docs/design/2026-05-27-system-design.md:1765:    └─ celery-beat
./docs/design/2026-05-27-system-design.md:1819:  celery-worker:
./docs/design/2026-05-27-system-design.md:1821:    command: celery -A config worker -l info
./docs/design/2026-05-27-system-design.md:1832:  celery-beat:
./docs/design/2026-05-27-system-design.md:1834:    command: celery -A config beat -l info
./docs/design/2026-05-27-system-design.md:2266:@celery.task
./docs/design/2026-05-27-system-design.md:2500:**Celery任务队列：**
./docs/design/2026-05-27-system-design.md:2503:@celery.task
./docs/design/2026-05-27-system-design.md:2509:@celery.task
./docs/design/2026-05-27-system-design.md:2515:@celery.task
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:27:4. Fix smoke_test.sh duplicate submission issue
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:42:**Problem:** smoke_test.sh line 175 tries to create second application with same student `2020001`.
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:62:**Codex claim:** smoke_test.sh tries to create duplicate application, violating unique constraint.
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:101:3. Fix smoke_test.sh duplicate submission issue
./docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:22:- DEPLOYMENT.md完整部署指南（6步快速启动）
./docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md:79:   范围：Django Notification模型、迁移、4个读取/已读API、RBAC测试、seed命令；不含 signals、Celery、小程序通知页、微信模板。
./docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md:110:- Celery；
./docs/discussions/phase4c-next-steps/34-claude-authorization-interpretation-request.md:35:- 排除：signals、Celery、小程序页、微信模板
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:119:- 验收清单应引用`tests/smoke_test.sh`作为主验证入口，curl命令作为展开说明，而不是两套可能漂移的事实来源。
./docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:71:- Celery异步任务（推迟到Phase 2）
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:47:理由：这些都是安全/一致性回归点，且仓库已经有 `backend/apps/*/tests/` 测试结构，新增针对性 Django 测试比后续靠人工复验可靠。`tests/smoke_test.sh` 可以作为端到端运行脚本，但不能替代模型/API层回归测试。
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:35:2. Celery任务队列必要性存疑
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:143:- ❌ Celery异步任务（Phase 1同步实现）
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:163:- 如果通知发送成为瓶颈 → 引入Celery
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:284:3. **简化Phase 1设计**（推迟Celery、乐观锁、复杂工作日计算）
./docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:97:- Phase 2C：超时提醒任务设计，等 Celery/调度方案确定后再做。
./docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:166:- Celery/定时任务；
./docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:122:- 风险最小（只改数据库schema）
./docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:177:- Celery异步任务（推迟到Phase 2）
./docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:61:当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
./docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:136:- **实现范围膨胀：** Phase 1禁止 signals 和 Celery。
./docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:61:- 超时提醒需要Celery定时任务（Phase 4推迟范围）
./docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:153:- 补充DEPLOYMENT.md生产部署章节
./docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:203:- 仅实现4种立即可触发的通知类型（排除APPROVAL_TIMEOUT_WARNING，需要Celery）
./docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:187:- 实现Celery异步任务
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:62:**5. 可复现验证缺失**：没有smoke_test.sh  
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:137:- 位置：`tests/smoke_test.sh`
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:5:**不在范围内：** 安装依赖、创建 Django 项目、settings 分层、Docker/Celery/开发工具配置、后端业务实现、前端实现、测试实现、部署落地等尚未完成事项
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:27:- Celery
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:64:- 缓存/队列：Redis + Celery
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:169:   Phase 1 同时包含 Django 初始化、Docker、Celery、开发工具等任务。作为计划本身没有问题，但当前已完成部分只覆盖了目录、`.gitignore`、requirements。项目总结中已经正确标注其余任务为暂停/待继续。
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:250:- Celery pid/schedule
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:335:- Celery 任务实现
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:29:- `APPROVAL_TIMEOUT_WARNING`：需要Celery定时任务
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:73:- Celery/定时任务
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:95:- 更新`tests/smoke_test.sh`
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:148:- `APPROVAL_TIMEOUT_WARNING`通知（推迟到Celery方案确定后）
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:159:- 需要Celery定时任务
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:34:#### MAJOR - Celery任务队列必要性存疑
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:37:设计中Celery用于：通知发送、文件上传、凭证生成。但单实例部署场景下，这些任务是否真的需要异步？
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:38:- 微信通知：HTTP请求通常<500ms，是否值得引入Celery复杂度？
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:43:- 增加系统复杂度（Redis、Celery Worker、Celery Beat）
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:49:2. **性能测试后决策**：如果通知发送成为瓶颈，再引入Celery
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:76:1. **简化初期架构**：Phase 1不引入Celery，先用同步实现
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:77:2. **明确扩展路径**：文档化何时需要MinIO、何时需要Celery
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:51:- 位置：`tests/smoke_test.sh`
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:85:- smoke_test.sh需要从零编写，1小时够吗？
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:64:| MAJOR | Celery必要性存疑 | 增加复杂度 |
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:125:### 3. Celery异步任务
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:169:18. 推迟Celery实施
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:212:### 争议3：Celery是否Phase 1引入？
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:214:**设计文档：** 已包含Celery
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:221:- 如果成为瓶颈，Phase 2引入Celery
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:238:  - Celery是否Phase 1引入？
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:11:当前仓库已经完成较完整的需求、系统设计、实施计划和多轮评审共识，核心方向基本清晰：Django + DRF 单体后端、PostgreSQL 单数据库、Redis + Celery、本地文件存储、微信登录/通知、宿舍系统优先 API 对接。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:141:- Celery/Redis
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:203:设计文档多表重复使用 `idx_user_id`、`idx_application_id` 等索引名。PostgreSQL 中索引名在 schema 内需要唯一，不能像 MySQL 那样只在表内唯一。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:514:2. 先产出 OpenAPI/接口契约，避免两个前端各自猜接口。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:555:   - base：Django/DRF/PostgreSQL/Redis/Celery/SimpleJWT/requests/python-magic/chinese-calendar/cryptography/django-redis
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:101:- 任务5：执行smoke_test.sh，期望全部通过
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:257:**位置：** `tests/smoke_test.sh`
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:267:chmod +x tests/smoke_test.sh
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:268:./tests/smoke_test.sh
./docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:80:- Celery 任务；
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:25:- 但`tests/smoke_test.sh`和`tests/test_p0_fixes.sh`也有固定`2024-06-30`
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:34:- **tests/smoke_test.sh** (新增)
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:163:5. **tests/smoke_test.sh** - 动态日期（新增）
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:190:2. Smoke测试：tests/smoke_test.sh通过
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:133:- 完全重写docker-compose.yml（postgres、单实例django-app、redis、celery）
./docs/discussions/phase4c-next-steps/36-claude-consensus-minimal-confirmation.md:54:- signals、Celery、审批挂钩、超时提醒
./docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:98:- ⚠️ 紧耦合 - schema变更会破坏本系统
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:351:- 位置：`tests/smoke_test.sh`
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:152:chmod +x tests/smoke_test.sh
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:153:./tests/smoke_test.sh
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:19:- 技术栈：Django 4.2 + PostgreSQL + Redis + Celery + Docker
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:38:- Celery异步任务的必要性
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:111:- PostgreSQL + Redis + Celery容器化
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:143:- Celery异步任务（通知发送、外部系统调用）
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:93:- 位置：`tests/smoke_test.sh`
./docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:139:- 风险最小（只改数据库schema）
./docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:215:- Celery异步任务（推迟到Phase 2）
./docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:293:   - **缓解：** 严格遵守Phase 1范围，禁止信号和Celery
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:298:### 争议3：Celery异步任务
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:300:**设计文档：** 已包含Celery  
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:328:- 如果通知发送成为瓶颈（>500ms），Phase 2引入Celery
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:364:@celery.task
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:455:- ✓ 推迟Celery实施
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:464:- 同步实现（不引入Celery）
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:476:- 如果通知慢 → 引入Celery
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:64:**问题：** 仓库里没找到`smoke_test.sh` / Postman / manual verification文档  
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:133:- 重写第7章围绕：`nginx`、单个`django-app`（Gunicorn 4 workers）、`postgres`、`redis`、`celery-worker`、`celery-beat`
./docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:93:# Celery定时任务
./docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:94:@celery.task
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:21:- ⏸ Track 3 Phase 2C: 审批超时提醒（需Celery定时任务）
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:42:- 需要Celery定时任务基础设施
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:86:- Phase 2C: Celery基础设施 + 审批超时提醒
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:94:- Phase 2C需要引入Celery（新依赖，增加复杂度）
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:100:- Phase 2C: 3-4小时（Celery配置 + 定时任务 + 工作日计算 + 测试）
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:104:- Celery引入可能带来部署复杂度
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:181:- API文档完善（Swagger/OpenAPI）
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:229:- 使用drf-spectacular生成OpenAPI schema
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:234:- 扩展smoke_test.sh覆盖更多场景
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:239:- 更新DEPLOYMENT.md
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:252:- 需要Celery基础设施（复杂度高）
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:267:   - 不引入新依赖（无Celery）
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:271:   - Celery引入复杂度高
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:290:2. smoke_test.sh覆盖至少20个场景（当前15个）
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:291:3. DEPLOYMENT.md包含故障排查指南和环境变量说明
./docs/discussions/phase4c-next-steps/24-claude-consensus-evidence-closure.md:43:- Smoke脚本：`tests/smoke_test.sh`（15步）
./docs/discussions/phase4c-next-steps/24-claude-consensus-evidence-closure.md:46:- Docker部署：`DEPLOYMENT.md`（6步快速启动）
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:34:@celery.task
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:51:#### MAJOR - 超时监控Celery任务每小时执行浪费资源
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:73:@celery.task
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:186:@celery.task(max_retries=10, retry_backoff=60)
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:217:@celery.task
./docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:21:4. **Phase 1不得包含 signals、Celery、小程序通知页、微信模板消息。**
./docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:149:- Celery；
./docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:31:| Option D：只做模型和迁移 | 不建议 | 只落 schema 但无 API 验收价值低，且仍然属于实现 |
./docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:65:- Celery/异步任务。
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:34:- OpenAPI/DTO草案
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:78:2. OpenAPI/DTO达到v0.2（有changelog）
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:115:| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:32:- OpenAPI/DTO草案
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:80:2. OpenAPI/DTO达到v0.2（有changelog）
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:116:| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:242:2. ✓ v0.1包含OpenAPI/DTO、状态枚举、错误码、样例、mock、changelog
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:268:> 1. `contract-v0.1.md`或OpenAPI草案
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:42:- Phase 1: 项目初始化（Django、Docker、Celery）
./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:62:其中401和403省略 `details`，这对v0.1可接受；如果后续要生成严格schema，可在v0.2明确 `details` 为可选字段。
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:125:3. **后端骨架**：1天（Django项目、Docker、Celery基础配置）
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:35:- OpenAPI/接口草案
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:71:- 后端负责人 owns 契约包：OpenAPI/DTO/错误码/seed schema。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:166:2. OpenAPI/DTO达到v0.2，破坏性变更需要changelog。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:241:| Week 0 / 1-2工作日 | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog |
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:274:1. `contract-v0.1.md`或OpenAPI草案：字段、状态、错误码、样例、mock、changelog。
./docs/contracts/contract-v0.2.md:245:- 全量 OpenAPI schema。

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Track 3 Phase 2策略 - Claude共识响应

**日期：** 2026-06-02  
**响应人：** Claude  
**针对文档：** `docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md`  
**类型：** 共识确认

---

## 共识声明

**完全接受Codex的Option A-lite建议。**

Codex识别的`DORM_CLEARANCE_BLOCKED`架构约束是正确的：当前失败路径在`backend/apps/applications/views.py:98-105`直接返回422，在`Application.objects.create()`之前，没有可关联的实体。这是我在原策略分析中遗漏的关键约束。

---

## 接受的修正

### 1. 范围收窄为3种通知类型

**接受：** 仅实现以下3种立即可触发的通知：
- `APPLICATION_SUBMITTED`（申请提交）
- `APPROVAL_APPROVED`（审批通过）
- `APPROVAL_REJECTED`（审批驳回）

**排除：**
- `DORM_CLEARANCE_BLOCKED`：需要先修正契约或增加申请尝试实体
- `APPROVAL_TIMEOUT_WARNING`：需要Celery定时任务

### 2. 服务层优先架构

**接受：** 先创建`backend/apps/notifications/services.py`，提供幂等创建函数，而不是直接在signals receiver中实现业务逻辑。

**理由：**
- 避免业务错误隐藏在模型保存副作用中
- 提供明确的幂等和异常边界
- 避免循环导入风险
- 便于测试和维护

### 3. 修订后的验收标准

**接受Codex提供的8个验收标准：**

1. 学生提交申请成功后，辅导员收到一条`APPLICATION_SUBMITTED`通知
2. 辅导员通过后，学生收到一条`APPROVAL_APPROVED`通知，关联counselor approval
3. 学工部通过后，学生收到一条`APPROVAL_APPROVED`通知，关联dean approval
4. 任一审批驳回后，学生收到一条`APPROVAL_REJECTED`通知，正文包含驳回原因
5. 重复保存同一申请或审批不重复创建通知，不抛`IntegrityError`
6. 权限拒绝、状态冲突、参数校验失败时不创建通知
7. 通知创建后，Phase 1的list/unread_count/mark_as_read API仍全部通过
8. 自动通知测试与既有application/approval/notification tests全部通过

---

## 执行计划：Track 3 Phase 2A

### 范围确认

**包含：**
- 新增`backend/apps/notifications/services.py`
- 幂等通知创建函数：`notify_application_submitted()`, `notify_approval_decided()`
- 在业务视图中调用通知服务（`create_application`, `approve_approval`, `reject_approval`）
- 自动通知focused tests
- smoke test增加通知验证断言

**不包含：**
- Django signals实现（可选，视服务层验证结果决定）
- `DORM_CLEARANCE_BLOCKED`通知
- `APPROVAL_TIMEOUT_WARNING`通知
- 小程序通知页面
- 微信模板消息
- Celery/定时任务

### 实施步骤

**Step 1: 通知服务层（45分钟）**
- 创建`backend/apps/notifications/services.py`
- 实现`notify_application_submitted(application, approval)`
- 实现`notify_approval_decided(approval)`
- 幂等封装：使用`get_or_create`避免`IntegrityError`

**Step 2: 业务集成（30分钟）**
- `backend/apps/applications/views.py:create_application`：成功创建Approval后调用`notify_application_submitted`
- `backend/apps/approvals/views.py:approve_approval`：决策后调用`notify_approval_decided`
- `backend/apps/approvals/views.py:reject_approval`：决策后调用`notify_approval_decided`

**Step 3: 自动通知测试（45分钟）**
- 创建`backend/apps/notifications/tests/test_auto_notifications.py`
- 测试3种通知类型自动创建
- 测试幂等性（重复操作不重复创建）
- 测试负向路径（权限拒绝、状态冲突时不创建）

**Step 4: Smoke验证（15分钟）**
- 更新`tests/smoke_test.sh`
- 增加通知API验证断言（提交后查询辅导员通知、审批后查询学生通知）

**总计：** 2-2.5小时

---

## 关键实现细节

### 通知标题和正文模板

```python
# APPLICATION_SUBMITTED
title = "新的离校申请"
message = f"学生{application.student_name}（{application.student.user_id}）提交了离校申请，请及时审批。"

# APPROVAL_APPROVED
title = "审批通过"
approver_role = "辅导员" if approval.step == "counselor" else "学工部"
message = f"您的离校申请已通过{approver_role}审批。"

# APPROVAL_REJECTED
title = "审批驳回"
approver_role = "辅导员" if approval.step == "counselor" else "学工部"
message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
```

### 幂等创建封装

```python
def create_notification_idempotent(recipient, actor, type, entity_type, entity_id, title, message):
    notification, created = Notification.objects.get_or_create(
        recipient=recipient,
        entity_type=entity_type,
        entity_id=entity_id,
        type=type,
        defaults={
            'actor': actor,
            'title': title,
            'message': message
        }
    )
    return notification, created
```

---

## 不采纳的原Option A内容

**原计划中的以下内容不在Phase 2A范围：**
- 4种通知类型（收窄为3种）
- 纯signals实现（改为服务层+业务视图调用）
- `DORM_CLEARANCE_BLOCKED`通知（推迟到契约修正后）
- `APPROVAL_TIMEOUT_WARNING`通知（推迟到Celery方案确定后）

---

## 后续Phase规划

**Phase 2B（可选）：** 宿舍阻断通知契约修正
- 调整契约允许`entity_type=student`或`entity_type=application_attempt`
- 或在阻断时创建可追踪的申请尝试记录

**Phase 2C（可选）：** 审批超时提醒
- 需要Celery定时任务
- 需要工作日计算逻辑
- 推迟到生产部署准备阶段

**Phase 3（推迟）：** 小程序通知页面
- 依赖WeChat DevTools验证
- 等待外部阻塞解除

**Phase 4（推迟）：** 微信模板消息
- 依赖微信公众平台审核
- 推迟到生产部署阶段

---

## 执行授权确认

根据用户的"继续讨论+直接执行"指令和Codex的Option A-lite建议，现在启动Track 3 Phase 2A实施，无需额外用户授权。

**执行口径：**
> 下一步推进Track 3 Phase 2A：后端自动通知闭环。范围限定为通知服务层 + 申请提交/审批通过/审批驳回 3类自动通知 + 幂等测试 + smoke验证；暂不实现宿舍阻断通知、审批超时提醒、小程序通知页、微信模板消息。

---

**共识达成时间：** 2026-06-02  
**Claude状态：** 立即启动Phase 2A实施

exec
/bin/bash -lc "rtk rg -n \"Notification|entity_type|DORM|notify_|application_submitted|approved|rejected|clearance\" backend docs/contracts docs/discussions/phase4c-next-steps -g '*.py' -g '*.md'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md:79:   范围：Django Notification模型、迁移、4个读取/已读API、RBAC测试、seed命令；不含 signals、Celery、小程序通知页、微信模板。
docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md:98:- `Notification` model + migration；
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:44:> - 范围：Django Notification模型、迁移、读取/已读API、RBAC测试、测试造数命令
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:60:- backend/apps/notifications/models.py（Notification模型）
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:62:- backend/apps/notifications/serializers.py（NotificationSerializer）
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:14:- ✅ Track 3 Phase 0: Notification Contract Draft v0.1
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:60:- Django Notification模型（30分钟）
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:119:**描述：** 只实现Notification模型和迁移，不实现API，用于验证数据结构设计
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:133:- Django Notification模型
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md:160:- Django Notification模型
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:14:- ✅ Notification模型 + 迁移（5/5测试通过）
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:51:- 自动创建Notification记录
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:52:- 5种通知类型全覆盖（APPLICATION_SUBMITTED、APPROVAL_APPROVED、APPROVAL_REJECTED、DORM_CLEARANCE_BLOCKED、APPROVAL_TIMEOUT_WARNING）
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:212:4. 宿舍清退阻断→自动创建DORM_CLEARANCE_BLOCKED通知
docs/discussions/phase4c-next-steps/23-codex-post-execution-next-steps-response.md:56:如果直接做 `Notification` 模型或 API，容易把当前阶段从“验收准备”重新带回“功能开发”。这会模糊 Phase 4C 的完成边界。
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:14:Codex识别的`DORM_CLEARANCE_BLOCKED`架构约束是正确的：当前失败路径在`backend/apps/applications/views.py:98-105`直接返回422，在`Application.objects.create()`之前，没有可关联的实体。这是我在原策略分析中遗漏的关键约束。
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:28:- `DORM_CLEARANCE_BLOCKED`：需要先修正契约或增加申请尝试实体
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:62:- 幂等通知创建函数：`notify_application_submitted()`, `notify_approval_decided()`
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:69:- `DORM_CLEARANCE_BLOCKED`通知
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:79:- 实现`notify_application_submitted(application, approval)`
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:80:- 实现`notify_approval_decided(approval)`
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:84:- `backend/apps/applications/views.py:create_application`：成功创建Approval后调用`notify_application_submitted`
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:85:- `backend/apps/approvals/views.py:approve_approval`：决策后调用`notify_approval_decided`
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:86:- `backend/apps/approvals/views.py:reject_approval`：决策后调用`notify_approval_decided`
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:125:def create_notification_idempotent(recipient, actor, type, entity_type, entity_id, title, message):
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:126:    notification, created = Notification.objects.get_or_create(
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:128:        entity_type=entity_type,
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:147:- `DORM_CLEARANCE_BLOCKED`通知（推迟到契约修正后）
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:155:- 调整契约允许`entity_type=student`或`entity_type=application_attempt`
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:61:**建议裁决：** 通知系统排在CSV导入和Docker硬化之后。短期只做通知事件契约或后端`Notification`模型草案，最多实现"审批动作后创建站内通知记录"的无前端骨架；不要承诺完整通知中心。
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:185:### M3：Notification Contract Ready（可选）
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:28:- 包含：定义事件类型 + 设计Notification模型 + 定义API契约
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:31:- Phase 0/1: Notification Contract Draft（2-3小时）
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:97:   - DORM_CLEARANCE_BLOCKED（宿舍清退阻断）
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:107:   - entity_type（关联实体类型：application/approval）
docs/discussions/phase4c-next-steps/30-claude-consensus-contract-revision-gate.md:72:**问题：** 当前幂等键(entity_type, entity_id, type)无法支持多接收者
docs/discussions/phase4c-next-steps/30-claude-consensus-contract-revision-gate.md:74:**修正方案：** UNIQUE(recipient_id, entity_type, entity_id, type)
docs/discussions/phase4c-next-steps/30-claude-consensus-contract-revision-gate.md:137:   - 唯一约束：UNIQUE(recipient_id, entity_type, entity_id, type)
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:36:| 设计 Notification 数据结构 | 有条件同意 | 只写字段草案，不创建 model/migration |
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:37:| 实现 Notification 模型 | 暂缓 | 需要用户明确授权进入 Track 3 实现 |
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:62:建议把当前 Phase 1 改名为 **Phase 0/1: Notification Contract Draft**，交付物限定为一个文档，例如：
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:69:2. 最小字段草案：id、recipient、actor、type、title、body、entity_type、entity_id、read_at、created_at。
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:52:**接受裁决：** 通知系统排在CSV导入和Docker硬化之后，仅做通知事件契约或后端`Notification`模型草案，不承诺完整通知中心。
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:128:### M3：Notification Contract Ready（0.5天，可选）
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:64:- Phase 1A: Django Notification模型 + migration（1-2小时）
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:136:**描述：** 只实现Notification模型和迁移，不实现API，用于验证数据结构设计
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:150:- Django Notification模型
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:182:- Django Notification模型（10字段）
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:188:- NotificationSerializer
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:189:- NotificationViewSet
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:38:- 需要契约修正：允许`entity_type=student`或创建申请尝试记录
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:246:- 契约修正：允许`entity_type=student`，`entity_id=student.id`
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:247:- 实现`notify_dorm_clearance_blocked(student, dorm_status)`
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:295:1. 宿舍阻断时学生收到DORM_CLEARANCE_BLOCKED通知
docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:69:- 创建Notification模型草案
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:63:- Notification model + migration；
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:96:`UNIQUE(recipient_id, entity_type, entity_id, type)` 适合当前 v0.1，但 Phase 2接入超时提醒时要确认是否允许同一审批多次周期性提醒。如果需要周期性提醒，Phase 2应补充 `dedupe_key` 或提醒窗口字段，而不是强行复用当前唯一键。
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:119:   范围：Notification model/migration/API/tests/seed command，不含 signals、小程序通知页、微信模板消息。
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:135:- `Notification` model，使用 `recipient`/`actor` 外键到 `AUTH_USER_MODEL`；
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:137:- `type`、`entity_type` 使用 TextChoices；
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:140:- 唯一约束 `recipient, entity_type, entity_id, type`；
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:164:> 通知契约已经修正到可实现状态。建议授权启动 Track 3 Phase 1 后端MVP实现，范围仅限 Django Notification模型、迁移、读取/已读API、RBAC测试和测试造数命令；不包含 signals、小程序通知页、微信模板消息。请确认是否授权启动 Phase 1。
docs/discussions/phase4c-next-steps/34-claude-authorization-interpretation-request.md:34:- 范围：Django Notification模型 + 迁移 + 4 API + RBAC测试 + seed命令
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:42:Because global `DEFAULT_PARSER_CLASSES` only includes `JSONParser`, multipart upload requests are rejected before the helper-level parser configuration can take effect.
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:35:  | 'library_clearance'
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:36:  | 'finance_clearance'
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:119:    const types: AttachmentType[] = ['dorm_checkout', 'library_clearance', 'finance_clearance', 'other'];
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:56:- 新增 `Notification` 模型和迁移。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:89:契约现在用 `(entity_type, entity_id, type)` 做幂等检查，但如果同一审批事件需要通知多个接收者，会误杀不同 recipient 的通知。实现前应把唯一约束定义为 `(recipient, entity_type, entity_id, type)`，并把并发幂等交给数据库唯一约束，而不是只靠 `.exists()`。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:118:> Track 3 Phase 0 通知契约已完成。下一步是否授权启动 Phase 1 后端通知 MVP？范围限定为 Django Notification 模型、迁移、4 个读取/已读 API、权限隔离测试和 curl 验证；不包含信号触发、小程序通知页、微信模板消息。回复“授权 Phase 1”后开始实现。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:128:1. 将幂等键从 `(entity_type, entity_id, type)` 改为 `(recipient_id, entity_type, entity_id, type)`。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:24:1. `DORM_CLEARANCE_BLOCKED`
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:33:### P1：`DORM_CLEARANCE_BLOCKED` 不能由当前模型 signals 可靠触发
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:37:当前宿舍清退检查失败时，`create_application` 在 `Application.objects.create(...)` 之前直接返回 `422 DORM_BLOCKED`。因此：
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:41:- 通知契约要求 `entity_type=application`、`entity_id={application_id}`，但失败路径没有 `application_id`；
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:42:- 如果强行用学生 ID 或固定占位 ID，会破坏当前 `Notification` 唯一约束的业务含义。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:44:**裁决：** 本轮不要把 `DORM_CLEARANCE_BLOCKED` 纳入 signals Phase 2验收标准。可作为后续独立小任务处理：要么调整契约允许 `entity_type=student/application_attempt`，要么在阻断时创建可追踪的申请尝试记录。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:54:- 审批记录二次保存时，如果只看 `decision == approved/rejected`，会重复尝试创建通知；
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:63:Phase 1已经用唯一约束保证 `recipient + entity_type + entity_id + type` 不重复。Phase 2自动创建必须显式使用 `get_or_create` 或等价幂等封装，否则重复保存同一 `Approval` 可能抛出 `IntegrityError`，把通知系统问题升级成审批接口失败。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:83:契约允许辅导员和学工部审批通过都通知学生。现有唯一键使用 `entity_type=approval`、`entity_id=approval_id` 时，两个审批步骤会产生两条不同通知，这是合理的。实现文档应明确这一点，避免误以为“申请最终通过”才通知。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:105:- `DORM_CLEARANCE_BLOCKED`：当前失败路径没有实体落库；
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:112:若坚持加入宿舍阻断并保持契约一致，估算应上调到 6-9 小时，因为需要补契约、设计实体或替代 `entity_type/entity_id` 语义，并更新测试。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:128:1. signals receiver 未在 `NotificationsConfig.ready()` 中加载，Django 不会自动注册。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:129:2. Django 4下 `default_app_config` 不可靠，当前 `INSTALLED_APPS` 使用的是 `'apps.notifications'`，若要在 notifications app 注册 signals，应改用 `'apps.notifications.apps.NotificationsConfig'` 或确认自动 config 发现行为。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:139:2. `notify_application_submitted(application, approval)`
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:140:3. `notify_approval_decided(approval)`
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:162:- `DORM_CLEARANCE_BLOCKED`；
docs/contracts/contract-v0.1.md:58:    decision: ApprovalDecision   # approved/rejected/pending
docs/contracts/contract-v0.1.md:96:    APPROVED = "approved"                # 已通过
docs/contracts/contract-v0.1.md:97:    REJECTED = "rejected"                # 已驳回
docs/contracts/contract-v0.1.md:113:    APPROVED = "approved"
docs/contracts/contract-v0.1.md:114:    REJECTED = "rejected"
docs/contracts/contract-v0.1.md:135:| pending_counselor | 辅导员驳回 | counselor | rejected | 无 |
docs/contracts/contract-v0.1.md:136:| pending_dean | 学工部通过 | dean | approved | 无 |
docs/contracts/contract-v0.1.md:137:| pending_dean | 学工部驳回 | dean | rejected | 无 |
docs/contracts/contract-v0.1.md:144:| pending | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:145:| not_started | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:146:| unknown | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:171:| DORM_BLOCKED | 422 | 宿舍清退未完成 | 提交申请时宿舍未清退 |
docs/contracts/contract-v0.1.md:185:    "code": "DORM_BLOCKED",
docs/contracts/contract-v0.1.md:303:  "decision": "approved",
docs/contracts/contract-v0.1.md:326:  "decision": "rejected",
docs/contracts/contract-v0.1.md:521:    "code": "DORM_BLOCKED",
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:61:当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:66:UNIQUE(recipient_id, entity_type, entity_id, type)
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:111:- `Notification` model + migration；
docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:62:- 设计Notification模型（通知ID、用户、类型、内容、已读状态）
docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:167:- 设计Notification模型
docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:173:- 实现Notification模型和迁移
docs/contracts/contract-v0.2.md:13:ApplicationStatus: draft | pending_counselor | pending_dean | approved | rejected
docs/contracts/contract-v0.2.md:15:ApprovalDecision: pending | approved | rejected
docs/contracts/contract-v0.2.md:95:  "decision": "approved",
docs/contracts/contract-v0.2.md:120:| pending_counselor | 驳回 | counselor | counselor | rejected | 无 |
docs/contracts/contract-v0.2.md:121:| pending_dean | 通过 | dean | dean | approved | 无 |
docs/contracts/contract-v0.2.md:122:| pending_dean | 驳回 | dean | dean | rejected | 无 |
docs/contracts/contract-v0.2.md:130:- 已处于 `pending_counselor`、`pending_dean`、`approved` 的申请会阻断重复提交。
docs/contracts/contract-v0.2.md:189:`decision` 可取 `pending | approved | rejected | all`，默认 `pending`。
docs/contracts/contract-v0.2.md:238:| DORM_BLOCKED | 422 | 宿舍清退未完成 |
backend/apps/approvals/migrations/0001_initial.py:22:                ('decision', models.CharField(choices=[('pending', '待审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='pending', max_length=20)),
backend/apps/approvals/models.py:13:    APPROVED = 'approved', '已通过'
backend/apps/approvals/models.py:14:    REJECTED = 'rejected', '已驳回'
backend/apps/approvals/tests/test_list_permissions.py:102:        # Create second application and approval for counselor1 (approved)
backend/apps/approvals/tests/test_list_permissions.py:112:        approval_c1_approved = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:113:            approval_id='apv_c1_approved',
backend/apps/approvals/tests/test_list_permissions.py:149:        self.assertIn('apv_c1_approved', approval_ids)
backend/apps/approvals/views.py:13:from apps.notifications.services import notify_approval_decided
backend/apps/approvals/views.py:107:    notify_approval_decided(approval)
backend/apps/approvals/views.py:178:    notify_approval_decided(approval)
backend/apps/applications/models.py:10:    APPROVED = 'approved', '已通过'
backend/apps/applications/models.py:11:    REJECTED = 'rejected', '已驳回'
backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
backend/apps/applications/tests/test_p0_fixes.py:109:        self.app_approved = Application.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:110:            application_id='app_approved',
backend/apps/applications/tests/test_p0_fixes.py:119:        self.app_rejected = Application.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:120:            application_id='app_rejected',
backend/apps/applications/tests/test_p0_fixes.py:139:        self.approval_approved = Approval.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:140:            approval_id='apv_approved',
backend/apps/applications/tests/test_p0_fixes.py:141:            application=self.app_approved,
backend/apps/applications/tests/test_p0_fixes.py:148:        self.approval_rejected = Approval.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:149:            approval_id='apv_rejected',
backend/apps/applications/tests/test_p0_fixes.py:150:            application=self.app_rejected,
backend/apps/applications/tests/test_p0_fixes.py:165:    def test_filter_approved_approvals(self):
backend/apps/applications/tests/test_p0_fixes.py:171:        self.assertEqual(approvals.first().approval_id, 'apv_approved')
backend/apps/applications/tests/test_p0_fixes.py:173:    def test_filter_rejected_approvals(self):
backend/apps/applications/tests/test_p0_fixes.py:179:        self.assertEqual(approvals.first().approval_id, 'apv_rejected')
backend/apps/applications/tests/test_error_cases.py:75:        self.assertEqual(response.data['error']['code'], 'DORM_BLOCKED')
backend/apps/applications/views.py:14:from apps.notifications.services import notify_application_submitted
backend/apps/applications/views.py:83:    # Check for existing pending/approved applications
backend/apps/applications/views.py:103:        return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
backend/apps/applications/views.py:135:    notify_application_submitted(application, counselor_approval)
backend/apps/attachments/migrations/0001_initial.py:23:                ('attachment_type', models.CharField(choices=[('dorm_checkout', '宿舍清退证明'), ('library_clearance', '图书馆清书证明'), ('finance_clearance', '财务结清证明'), ('other', '其他')], max_length=50)),
backend/apps/attachments/models.py:7:    DORM_CHECKOUT = 'dorm_checkout', '宿舍清退证明'
backend/apps/attachments/models.py:8:    LIBRARY_CLEARANCE = 'library_clearance', '图书馆清书证明'
backend/apps/attachments/models.py:9:    FINANCE_CLEARANCE = 'finance_clearance', '财务结清证明'
backend/apps/attachments/tests/test_list.py:92:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_download.py:71:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_delete.py:70:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_upload.py:84:                'attachment_type': AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_upload.py:94:        self.assertEqual(response.data['attachment_type'], AttachmentType.DORM_CHECKOUT)
backend/apps/attachments/tests/test_upload.py:106:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:123:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:138:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/users/management/commands/import_csv.py:252:        for entity_type, stats in summary.items():
backend/apps/users/management/commands/import_csv.py:254:                self.stdout.write(f'\n{entity_type.upper()}:')
backend/apps/notifications/services.py:2:Notification service layer for idempotent notification creation.
backend/apps/notifications/services.py:9:from .models import Notification
backend/apps/notifications/services.py:15:def notify_application_submitted(application, approval):
backend/apps/notifications/services.py:24:        tuple: (Notification instance, created boolean)
backend/apps/notifications/services.py:29:    return Notification.objects.get_or_create(
backend/apps/notifications/services.py:31:        entity_type='approval',
backend/apps/notifications/services.py:42:def notify_approval_decided(approval):
backend/apps/notifications/services.py:44:    Create notification for student when approval is approved or rejected.
backend/apps/notifications/services.py:50:        tuple: (Notification instance, created boolean)
backend/apps/notifications/services.py:58:    else:  # rejected
backend/apps/notifications/services.py:63:    return Notification.objects.get_or_create(
backend/apps/notifications/services.py:65:        entity_type='approval',
backend/apps/notifications/apps.py:4:class NotificationsConfig(AppConfig):
backend/apps/notifications/tests/__init__.py:1:# Notifications app tests
backend/apps/notifications/tests/test_models.py:4:from apps.notifications.models import Notification, NotificationType, EntityType
backend/apps/notifications/tests/test_models.py:7:class NotificationModelTest(TestCase):
backend/apps/notifications/tests/test_models.py:23:        notification = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:26:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:27:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:40:        n1 = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:42:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_models.py:43:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:48:        n2 = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:50:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_models.py:51:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:60:        Notification.objects.create(
backend/apps/notifications/tests/test_models.py:62:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:63:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:69:            Notification.objects.create(
backend/apps/notifications/tests/test_models.py:71:                type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:72:                entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:86:        n1 = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:88:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:89:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:94:        n2 = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:96:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:97:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:106:        n1 = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:108:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_models.py:109:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:114:        n2 = Notification.objects.create(
backend/apps/notifications/tests/test_models.py:116:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:117:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:122:        notifications = list(Notification.objects.all())
backend/apps/notifications/tests/test_api.py:5:from apps.notifications.models import Notification, NotificationType, EntityType
backend/apps/notifications/tests/test_api.py:8:class NotificationAPITest(TestCase):
backend/apps/notifications/tests/test_api.py:31:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:33:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:34:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:39:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:41:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_api.py:42:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:57:        n1 = Notification.objects.create(
backend/apps/notifications/tests/test_api.py:59:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:60:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:65:        n2 = Notification.objects.create(
backend/apps/notifications/tests/test_api.py:67:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_api.py:68:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:89:            Notification.objects.create(
backend/apps/notifications/tests/test_api.py:91:                type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:92:                entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:109:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:111:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:112:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:117:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:119:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:120:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:132:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:134:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:135:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:140:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:142:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_api.py:143:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:158:        notification = Notification.objects.create(
backend/apps/notifications/tests/test_api.py:160:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:161:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:178:        notification = Notification.objects.create(
backend/apps/notifications/tests/test_api.py:180:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:181:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:199:        notification = Notification.objects.create(
backend/apps/notifications/tests/test_api.py:201:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:202:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:224:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:226:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:227:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:232:        Notification.objects.create(
backend/apps/notifications/tests/test_api.py:234:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_api.py:235:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:247:        unread_count = Notification.objects.filter(
backend/apps/notifications/tests/test_auto_notifications.py:6:- Approval is approved (APPROVAL_APPROVED)
backend/apps/notifications/tests/test_auto_notifications.py:7:- Approval is rejected (APPROVAL_REJECTED)
backend/apps/notifications/tests/test_auto_notifications.py:16:from apps.notifications.models import Notification
backend/apps/notifications/tests/test_auto_notifications.py:17:from apps.notifications.services import notify_application_submitted, notify_approval_decided
backend/apps/notifications/tests/test_auto_notifications.py:22:class AutoNotificationTest(TestCase):
backend/apps/notifications/tests/test_auto_notifications.py:44:    def test_application_submitted_notification(self):
backend/apps/notifications/tests/test_auto_notifications.py:65:        notification, created = notify_application_submitted(application, approval)
backend/apps/notifications/tests/test_auto_notifications.py:71:        self.assertEqual(notification.entity_type, 'approval')
backend/apps/notifications/tests/test_auto_notifications.py:76:    def test_approval_approved_notification_counselor(self):
backend/apps/notifications/tests/test_auto_notifications.py:97:        notification, created = notify_approval_decided(approval)
backend/apps/notifications/tests/test_auto_notifications.py:103:        self.assertEqual(notification.entity_type, 'approval')
backend/apps/notifications/tests/test_auto_notifications.py:107:    def test_approval_approved_notification_dean(self):
backend/apps/notifications/tests/test_auto_notifications.py:128:        notification, created = notify_approval_decided(approval)
backend/apps/notifications/tests/test_auto_notifications.py:136:    def test_approval_rejected_notification(self):
backend/apps/notifications/tests/test_auto_notifications.py:158:        notification, created = notify_approval_decided(approval)
backend/apps/notifications/tests/test_auto_notifications.py:167:    def test_idempotency_application_submitted(self):
backend/apps/notifications/tests/test_auto_notifications.py:188:        notification1, created1 = notify_application_submitted(application, approval)
backend/apps/notifications/tests/test_auto_notifications.py:191:        notification2, created2 = notify_application_submitted(application, approval)
backend/apps/notifications/tests/test_auto_notifications.py:195:        self.assertEqual(Notification.objects.filter(
backend/apps/notifications/tests/test_auto_notifications.py:197:            entity_type='approval',
backend/apps/notifications/tests/test_auto_notifications.py:223:        notification1, created1 = notify_approval_decided(approval)
backend/apps/notifications/tests/test_auto_notifications.py:226:        notification2, created2 = notify_approval_decided(approval)
backend/apps/notifications/tests/test_auto_notifications.py:230:        self.assertEqual(Notification.objects.filter(
backend/apps/notifications/tests/test_auto_notifications.py:232:            entity_type='approval',
backend/apps/notifications/serializers.py:2:from .models import Notification
backend/apps/notifications/serializers.py:5:class NotificationSerializer(serializers.ModelSerializer):
backend/apps/notifications/serializers.py:7:        model = Notification
backend/apps/notifications/serializers.py:13:            'entity_type',
backend/apps/notifications/views.py:6:from .models import Notification
backend/apps/notifications/views.py:7:from .serializers import NotificationSerializer
backend/apps/notifications/views.py:26:    queryset = Notification.objects.filter(recipient=user)
backend/apps/notifications/views.py:35:    serializer = NotificationSerializer(notifications, many=True)
backend/apps/notifications/views.py:51:    count = Notification.objects.filter(recipient=user, read_at__isnull=True).count()
backend/apps/notifications/views.py:65:        notification = Notification.objects.get(notification_id=notification_id)
backend/apps/notifications/views.py:66:    except Notification.DoesNotExist:
backend/apps/notifications/views.py:82:    serializer = NotificationSerializer(notification)
backend/apps/notifications/views.py:95:    updated_count = Notification.objects.filter(
backend/apps/notifications/admin.py:2:from .models import Notification
backend/apps/notifications/admin.py:5:@admin.register(Notification)
backend/apps/notifications/admin.py:6:class NotificationAdmin(admin.ModelAdmin):
backend/apps/notifications/admin.py:8:    list_filter = ['type', 'entity_type', 'read_at', 'created_at']
backend/apps/notifications/management/commands/seed_notifications.py:4:from apps.notifications.models import Notification, NotificationType, EntityType
backend/apps/notifications/management/commands/seed_notifications.py:20:            Notification.objects.create(
backend/apps/notifications/management/commands/seed_notifications.py:22:                type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/management/commands/seed_notifications.py:23:                entity_type=EntityType.APPLICATION,
backend/apps/notifications/management/commands/seed_notifications.py:31:                Notification.objects.create(
backend/apps/notifications/management/commands/seed_notifications.py:33:                    type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/management/commands/seed_notifications.py:34:                    entity_type=EntityType.APPLICATION,
backend/apps/notifications/__init__.py:1:default_app_config = 'apps.notifications.apps.NotificationsConfig'
backend/apps/notifications/models.py:14:class NotificationType(models.TextChoices):
backend/apps/notifications/models.py:15:    APPLICATION_SUBMITTED = 'application_submitted', '申请已提交'
backend/apps/notifications/models.py:16:    APPROVAL_APPROVED = 'approval_approved', '审批通过'
backend/apps/notifications/models.py:17:    APPROVAL_REJECTED = 'approval_rejected', '审批驳回'
backend/apps/notifications/models.py:18:    DORM_CLEARANCE_BLOCKED = 'dorm_clearance_blocked', '宿舍清退阻断'
backend/apps/notifications/models.py:27:class Notification(models.Model):
backend/apps/notifications/models.py:51:        choices=NotificationType.choices,
backend/apps/notifications/models.py:54:    entity_type = models.CharField(
backend/apps/notifications/models.py:91:                fields=['recipient', 'entity_type', 'entity_id', 'type'],
backend/apps/notifications/migrations/0001_initial.py:19:            name='Notification',
backend/apps/notifications/migrations/0001_initial.py:22:                ('type', models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('dorm_clearance_blocked', '宿舍清退阻断'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型')),
backend/apps/notifications/migrations/0001_initial.py:23:                ('entity_type', models.CharField(choices=[('application', '离校申请'), ('approval', '审批记录')], max_length=50, verbose_name='实体类型')),
backend/apps/notifications/migrations/0001_initial.py:42:            constraint=models.UniqueConstraint(fields=('recipient', 'entity_type', 'entity_id', 'type'), name='unique_notification_per_recipient_entity'),

codex
Phase 2A appears to have already landed in the working tree, so I’m checking the proposed next step against the actual post-Phase 2A state rather than only the strategy text. That matters because the value of Option E versus Phase 2B changes if smoke/doc work already moved.
exec
/bin/bash -lc "rtk sed -n '70,160p' backend/apps/applications/views.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    # Serialize
    serializer = ApplicationListSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


def create_application(request):
    user = request.user

    if user.role != UserRole.STUDENT:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以提交申请'}},
                        status=status.HTTP_403_FORBIDDEN)

    # Check for existing pending/approved applications
    existing = Application.objects.filter(
        student=user,
        status__in=[ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]
    ).first()
    if existing:
        return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
                                    'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
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

    counselor_approval = Approval.objects.create(
        approval_id=f'apv_{uuid.uuid4().hex[:8]}',
        application=application,
        step=ApprovalStep.COUNSELOR,
        approver=class_mapping.counselor,
        approver_name=class_mapping.counselor_name,
        decision=ApprovalDecision.PENDING
    )

    notify_application_submitted(application, counselor_approval)

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

    # Check permission using shared helper
    if not can_view_application(user, application):
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
                        status=status.HTTP_403_FORBIDDEN)

    return Response(ApplicationSerializer(application).data)

exec
/bin/bash -lc "rtk sed -n '1,220p' backend/apps/notifications/models.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
import string
import random
from django.db import models
from django.conf import settings


def generate_notification_id():
    """生成格式为 not_xxxxxxxx 的通知ID"""
    chars = string.ascii_lowercase + string.digits
    random_str = ''.join(random.choices(chars, k=8))
    return f'not_{random_str}'


class NotificationType(models.TextChoices):
    APPLICATION_SUBMITTED = 'application_submitted', '申请已提交'
    APPROVAL_APPROVED = 'approval_approved', '审批通过'
    APPROVAL_REJECTED = 'approval_rejected', '审批驳回'
    DORM_CLEARANCE_BLOCKED = 'dorm_clearance_blocked', '宿舍清退阻断'
    APPROVAL_TIMEOUT_WARNING = 'approval_timeout_warning', '审批超时提醒'


class EntityType(models.TextChoices):
    APPLICATION = 'application', '离校申请'
    APPROVAL = 'approval', '审批记录'


class Notification(models.Model):
    notification_id = models.CharField(
        max_length=12,
        primary_key=True,
        default=generate_notification_id,
        editable=False,
        verbose_name='通知ID'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='notifications_received',
        verbose_name='接收者'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='notifications_triggered',
        null=True,
        blank=True,
        verbose_name='触发者'
    )
    type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        verbose_name='通知类型'
    )
    entity_type = models.CharField(
        max_length=50,
        choices=EntityType.choices,
        verbose_name='实体类型'
    )
    entity_id = models.CharField(
        max_length=50,
        verbose_name='实体ID'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='标题'
    )
    message = models.TextField(
        verbose_name='消息内容'
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='已读时间'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )

    class Meta:
        db_table = 'notifications'
        verbose_name = '通知'
        verbose_name_plural = '通知'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'created_at']),
            models.Index(fields=['recipient', 'read_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['recipient', 'entity_type', 'entity_id', 'type'],
                name='unique_notification_per_recipient_entity'
            )
        ]

    def __str__(self):
        return f'{self.notification_id}: {self.title}'

exec
/bin/bash -lc "rtk sed -n '1,240p' backend/apps/approvals/views.py" in /home/caohui/projects/graduation-leave-system
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
from .validators import approval_step_matches_application_status
from apps.applications.models import Application, ApplicationStatus
from apps.users.models import UserRole
from apps.notifications.services import notify_approval_decided
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

    # 辅导员: 只看自己的counselor审批
    if user.role == UserRole.COUNSELOR:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR
        ).select_related('application', 'approver')

    # 学工部: 只看自己的dean审批
    elif user.role == UserRole.DEAN:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DEAN
        ).select_related('application', 'approver')

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

    if not approval_step_matches_application_status(approval):
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

    notify_approval_decided(approval)

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

    if not approval_step_matches_application_status(approval):
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

    notify_approval_decided(approval)

    application = approval.application
    application.status = ApplicationStatus.REJECTED
    application.save()

    return Response(ApprovalSerializer(approval).data)

exec
/bin/bash -lc "rtk sed -n '1,300p' tests/smoke_test.sh" in /home/caohui/projects/graduation-leave-system
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
LEAVE_DATE=$(date -d "+1 day" +%Y-%m-%d)
APP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"reason\":\"毕业离校\",\"leave_date\":\"$LEAVE_DATE\"}")

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

# 3. Upload attachment
echo "3. Upload attachment..."
echo "Test attachment content" > /tmp/test_attachment.txt
UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/$APP_ID/attachments/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -F "file=@/tmp/test_attachment.txt" \
  -F "attachment_type=other")

ATTACHMENT_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.attachment_id')

if [ -z "$ATTACHMENT_ID" ] || [ "$ATTACHMENT_ID" = "null" ]; then
  echo "✗ Attachment upload failed"
  echo "$UPLOAD_RESPONSE" | jq '.'
  exit 1
fi

echo "✓ Attachment uploaded: $ATTACHMENT_ID"

# 4. List attachments
echo "4. List attachments..."
LIST_RESPONSE=$(curl -s "$BASE_URL/api/applications/$APP_ID/attachments/" \
  -H "Authorization: Bearer $STUDENT_TOKEN")

ATTACHMENT_COUNT=$(echo "$LIST_RESPONSE" | jq -r '.attachments | length')

if [ "$ATTACHMENT_COUNT" != "1" ]; then
  echo "✗ Attachment list failed: expected 1, got $ATTACHMENT_COUNT"
  exit 1
fi

echo "✓ Attachment list success: $ATTACHMENT_COUNT attachment(s)"

# 5. Download attachment
echo "5. Download attachment..."
DOWNLOAD_STATUS=$(curl -s -w "\n%{http_code}" -o /tmp/downloaded_attachment.txt \
  "$BASE_URL/api/applications/$APP_ID/attachments/$ATTACHMENT_ID/download/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | tail -1)

if [ "$DOWNLOAD_STATUS" != "200" ]; then
  echo "✗ Attachment download failed: HTTP $DOWNLOAD_STATUS"
  exit 1
fi

echo "✓ Attachment download success"

# 6. Delete attachment
echo "6. Delete attachment..."
DELETE_STATUS=$(curl -s -w "\n%{http_code}" -X DELETE \
  "$BASE_URL/api/applications/$APP_ID/attachments/$ATTACHMENT_ID/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | tail -1)

if [ "$DELETE_STATUS" != "204" ]; then
  echo "✗ Attachment delete failed: HTTP $DELETE_STATUS"
  exit 1
fi

echo "✓ Attachment deleted"

# Verify attachment list is empty
FINAL_LIST=$(curl -s "$BASE_URL/api/applications/$APP_ID/attachments/" \
  -H "Authorization: Bearer $STUDENT_TOKEN")
FINAL_COUNT=$(echo "$FINAL_LIST" | jq -r '.attachments | length')

if [ "$FINAL_COUNT" != "0" ]; then
  echo "✗ Attachment still exists after delete"
  exit 1
fi

echo "  Verified: attachment list empty"

# 7. Counselor login
echo "7. Counselor T001 login..."
T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T001","password":"T001"}' \
  | jq -r '.access_token')

if [ -z "$T001_TOKEN" ] || [ "$T001_TOKEN" = "null" ]; then
  echo "✗ Counselor login failed"
  exit 1
fi
echo "✓ Counselor login success"

# Verify counselor received APPLICATION_SUBMITTED notification
echo "  Verifying counselor notification..."
COUNSELOR_NOTIF_COUNT=$(curl -s "$BASE_URL/api/notifications/unread_count/" \
  -H "Authorization: Bearer $T001_TOKEN" \
  | jq -r '.unread_count')

if [ "$COUNSELOR_NOTIF_COUNT" -lt "1" ]; then
  echo "✗ Counselor notification not created: expected ≥1, got $COUNSELOR_NOTIF_COUNT"
  exit 1
fi

echo "  ✓ Counselor has $COUNSELOR_NOTIF_COUNT unread notification(s)"

# 8. Counselor approve
echo "8. Counselor approve..."
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

# Verify student received APPROVAL_APPROVED notification
echo "  Verifying student notification..."
STUDENT_NOTIF_COUNT=$(curl -s "$BASE_URL/api/notifications/unread_count/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.unread_count')

if [ "$STUDENT_NOTIF_COUNT" -lt "1" ]; then
  echo "✗ Student notification not created: expected ≥1, got $STUDENT_NOTIF_COUNT"
  exit 1
fi

echo "  ✓ Student has $STUDENT_NOTIF_COUNT unread notification(s)"

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

# Verify student received second APPROVAL_APPROVED notification
echo "  Verifying student notification..."
STUDENT_NOTIF_COUNT_FINAL=$(curl -s "$BASE_URL/api/notifications/unread_count/" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  | jq -r '.unread_count')

if [ "$STUDENT_NOTIF_COUNT_FINAL" -lt "2" ]; then
  echo "✗ Student notification count wrong: expected ≥2, got $STUDENT_NOTIF_COUNT_FINAL"
  exit 1
fi

echo "  ✓ Student has $STUDENT_NOTIF_COUNT_FINAL unread notification(s)"

# 11. Verify final status
echo "11. Verify final status..."
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
echo "12. T002 login..."
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
echo "13. Student 2020002 login..."
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

exec
/bin/bash -lc "rtk sed -n '1,220p' backend/apps/notifications/services.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
"""
Notification service layer for idempotent notification creation.

This module provides business logic for creating notifications automatically
when key events occur (application submission, approval decisions).
"""

from django.contrib.auth import get_user_model
from .models import Notification
from apps.approvals.models import ApprovalDecision

User = get_user_model()


def notify_application_submitted(application, approval):
    """
    Create notification for counselor when student submits application.

    Args:
        application: Application instance
        approval: Counselor approval instance

    Returns:
        tuple: (Notification instance, created boolean)
    """
    title = "新的离校申请"
    message = f"学生{application.student_name}（{application.student.user_id}）提交了离校申请，请及时审批。"

    return Notification.objects.get_or_create(
        recipient=approval.approver,
        entity_type='approval',
        entity_id=approval.pk,
        type='APPLICATION_SUBMITTED',
        defaults={
            'actor': application.student,
            'title': title,
            'message': message
        }
    )


def notify_approval_decided(approval):
    """
    Create notification for student when approval is approved or rejected.

    Args:
        approval: Approval instance with decision

    Returns:
        tuple: (Notification instance, created boolean)
    """
    approver_role = "辅导员" if approval.step == "counselor" else "学工部"

    if approval.decision == ApprovalDecision.APPROVED:
        title = "审批通过"
        message = f"您的离校申请已通过{approver_role}审批。"
        notification_type = 'APPROVAL_APPROVED'
    else:  # rejected
        title = "审批驳回"
        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
        notification_type = 'APPROVAL_REJECTED'

    return Notification.objects.get_or_create(
        recipient=approval.application.student,
        entity_type='approval',
        entity_id=approval.pk,
        type=notification_type,
        defaults={
            'actor': approval.approver,
            'title': title,
            'message': message
        }
    )

exec
/bin/bash -lc "rtk sed -n '300,620p' tests/smoke_test.sh" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Create application for 2020002 (will be assigned to T002)
echo "14. Create application for 2020002..."
TEST_APP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/" \
  -H "Authorization: Bearer $STUDENT2_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"reason\":\"测试跨班级审批\",\"leave_date\":\"$LEAVE_DATE\"}")

TEST_APP_ID=$(echo "$TEST_APP_RESPONSE" | jq -r '.application_id')
TEST_COUNSELOR_APPROVAL=$(echo "$TEST_APP_RESPONSE" | jq -r '.approvals[] | select(.step=="counselor") | .approval_id')

echo "  Test application: $TEST_APP_ID"
echo "  Test approval (T002): $TEST_COUNSELOR_APPROVAL"

# T002 tries to approve T001's approval
echo "15. T002 tries to approve T001's approval (should fail)..."
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
/bin/bash -lc "rtk sed -n '1,280p' backend/apps/notifications/tests/test_auto_notifications.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
"""
Tests for automatic notification creation.

Verifies that notifications are created automatically when:
- Student submits application (APPLICATION_SUBMITTED)
- Approval is approved (APPROVAL_APPROVED)
- Approval is rejected (APPROVAL_REJECTED)

Also tests idempotency and negative paths.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.notifications.models import Notification
from apps.notifications.services import notify_application_submitted, notify_approval_decided

User = get_user_model()


class AutoNotificationTest(TestCase):
    """Test automatic notification creation."""

    def setUp(self):
        """Create test users and base data."""
        self.student = User.objects.create_user(
            user_id='2021001',
            name='测试学生',
            role='student',
            class_id='CS2021-1'
        )
        self.counselor = User.objects.create_user(
            user_id='T001',
            name='张老师',
            role='counselor'
        )
        self.dean = User.objects.create_user(
            user_id='D001',
            name='赵主任',
            role='dean'
        )

    def test_application_submitted_notification(self):
        """Test APPLICATION_SUBMITTED notification creation."""
        application = Application.objects.create(
            application_id='app_test001',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test001',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.PENDING
        )

        notification, created = notify_application_submitted(application, approval)

        self.assertTrue(created)
        self.assertEqual(notification.recipient, self.counselor)
        self.assertEqual(notification.actor, self.student)
        self.assertEqual(notification.type, 'APPLICATION_SUBMITTED')
        self.assertEqual(notification.entity_type, 'approval')
        self.assertEqual(notification.entity_id, approval.pk)
        self.assertIn('测试学生', notification.message)
        self.assertIn('2021001', notification.message)

    def test_approval_approved_notification_counselor(self):
        """Test APPROVAL_APPROVED notification for counselor approval."""
        application = Application.objects.create(
            application_id='app_test002',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test002',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.APPROVED
        )

        notification, created = notify_approval_decided(approval)

        self.assertTrue(created)
        self.assertEqual(notification.recipient, self.student)
        self.assertEqual(notification.actor, self.counselor)
        self.assertEqual(notification.type, 'APPROVAL_APPROVED')
        self.assertEqual(notification.entity_type, 'approval')
        self.assertEqual(notification.entity_id, approval.pk)
        self.assertIn('辅导员', notification.message)

    def test_approval_approved_notification_dean(self):
        """Test APPROVAL_APPROVED notification for dean approval."""
        application = Application.objects.create(
            application_id='app_test003',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_DEAN
        )

        approval = Approval.objects.create(
            approval_id='apv_test003',
            application=application,
            step=ApprovalStep.DEAN,
            approver=self.dean,
            approver_name=self.dean.name,
            decision=ApprovalDecision.APPROVED
        )

        notification, created = notify_approval_decided(approval)

        self.assertTrue(created)
        self.assertEqual(notification.recipient, self.student)
        self.assertEqual(notification.actor, self.dean)
        self.assertEqual(notification.type, 'APPROVAL_APPROVED')
        self.assertIn('学工部', notification.message)

    def test_approval_rejected_notification(self):
        """Test APPROVAL_REJECTED notification creation."""
        application = Application.objects.create(
            application_id='app_test004',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test004',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.REJECTED,
            comment='材料不齐全'
        )

        notification, created = notify_approval_decided(approval)

        self.assertTrue(created)
        self.assertEqual(notification.recipient, self.student)
        self.assertEqual(notification.actor, self.counselor)
        self.assertEqual(notification.type, 'APPROVAL_REJECTED')
        self.assertIn('驳回', notification.message)
        self.assertIn('材料不齐全', notification.message)

    def test_idempotency_application_submitted(self):
        """Test that repeated calls don't create duplicate notifications."""
        application = Application.objects.create(
            application_id='app_test005',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test005',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.PENDING
        )

        notification1, created1 = notify_application_submitted(application, approval)
        self.assertTrue(created1)

        notification2, created2 = notify_application_submitted(application, approval)
        self.assertFalse(created2)
        self.assertEqual(notification1.pk, notification2.pk)

        self.assertEqual(Notification.objects.filter(
            recipient=self.counselor,
            entity_type='approval',
            entity_id=approval.pk,
            type='APPLICATION_SUBMITTED'
        ).count(), 1)

    def test_idempotency_approval_decided(self):
        """Test that repeated approval decisions don't create duplicate notifications."""
        application = Application.objects.create(
            application_id='app_test006',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test006',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.APPROVED
        )

        notification1, created1 = notify_approval_decided(approval)
        self.assertTrue(created1)

        notification2, created2 = notify_approval_decided(approval)
        self.assertFalse(created2)
        self.assertEqual(notification1.pk, notification2.pk)

        self.assertEqual(Notification.objects.filter(
            recipient=self.student,
            entity_type='approval',
            entity_id=approval.pk,
            type='APPROVAL_APPROVED'
        ).count(), 1)

exec
/bin/bash -lc "rtk sed -n '1,220p' DEPLOYMENT.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Deployment Guide

## Quick Start

### 1. Environment Setup

Copy environment template:
```bash
cp .env.example .env.docker
```

Edit `.env.docker` and set:
- `SECRET_KEY` (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DB_PASSWORD` (secure password)
- `JWT_SECRET_KEY` (random string)
- `ALLOWED_HOSTS` (your domain)

### 2. Start Services

```bash
docker compose up -d
```

Wait for services to be healthy (~10 seconds).

### 3. Database Migration

```bash
docker compose exec backend python manage.py migrate
```

### 4. Load Initial Data

**Option A: Seed test data (development)**
```bash
docker compose exec backend python manage.py seed_data
```

**Option B: Import production data (production)**
```bash
# 1. Import counselors first
docker compose exec backend python manage.py import_csv \
  --counselors /path/to/counselors.csv \
  --dry-run  # Preview first

docker compose exec backend python manage.py import_csv \
  --counselors /path/to/counselors.csv  # Apply

# 2. Import class mappings
docker compose exec backend python manage.py import_csv \
  --mappings /path/to/mappings.csv

# 3. Import students
docker compose exec backend python manage.py import_csv \
  --students /path/to/students.csv
```

CSV templates: `backend/data/templates/*.csv`

### 5. Verify Installation

Run smoke test:
```bash
./tests/smoke_test.sh
```

Expected output: All tests pass, no errors.

### 6. Access Application

- Backend API: http://localhost:8001
- Admin: http://localhost:8001/admin

## Data Import

### CSV Field Requirements

**counselors.csv:**
- employee_id (required)
- name (required)
- department (optional)

**mappings.csv:**
- class_id (required)
- counselor_employee_id (required)

**students.csv:**
- student_id (required)
- name (required)
- class_id (required)
- is_graduating (required, true/false)
- graduation_year (required)

### Import Order

**CRITICAL:** Import in this order:
1. Counselors (creates counselor accounts)
2. Mappings (links classes to counselors)
3. Students (validates class mappings exist)

### Dry-Run Mode

Always preview before applying:
```bash
docker compose exec backend python manage.py import_csv \
  --students students.csv --dry-run
```

## Troubleshooting

**Database connection failed:**
```bash
docker compose logs db
docker compose restart db
```

**Migration failed:**
```bash
docker compose exec backend python manage.py showmigrations
docker compose exec backend python manage.py migrate --fake-initial
```

**Import validation errors:**
Check error summary in output. Common issues:
- Missing required fields
- Duplicate IDs
- Counselor not found (for mappings)
- Class mapping missing (for students)

## Maintenance

**View logs:**
```bash
docker compose logs -f backend
```

**Reset database:**
```bash
docker compose down -v
docker compose up -d
docker compose exec backend python manage.py migrate
```

**Backup media files:**
```bash
docker compose exec backend tar czf /tmp/media-backup.tar.gz /app/media
docker compose cp backend:/tmp/media-backup.tar.gz ./media-backup.tar.gz
```

exec
/bin/bash -lc "rtk sed -n '1,220p' backend/requirements/base.txt" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Django Core
Django==4.2.13
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
django-filter==23.5

# Database
psycopg2-binary==2.9.9

# State Machine
django-fsm==2.8.1

# Celery
celery==5.3.6
redis==5.0.3

# WeChat
wechatpy==1.8.18

# Retry
tenacity==8.2.3

# Password
bcrypt==4.1.2

# Environment
python-decouple==3.8

# Utils
python-dateutil==2.9.0
pytz==2024.1

# File Processing
python-magic==0.4.27

# Work Day Calculation
chinese-calendar==1.9.0

# HTTP Client
requests==2.31.0

# Encryption
cryptography==42.0.5

# Cache
django-redis==5.4.0

exec
/bin/bash -lc "rtk rg -n \"APPLICATION_SUBMITTED|application_submitted|APPROVAL_APPROVED|approval_approved|type=|NotificationType\" backend/apps/notifications backend/apps/applications backend/apps/approvals -g '*.py'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/notifications/services.py:15:def notify_application_submitted(application, approval):
backend/apps/notifications/services.py:31:        entity_type='approval',
backend/apps/notifications/services.py:33:        type='APPLICATION_SUBMITTED',
backend/apps/notifications/services.py:57:        notification_type = 'APPROVAL_APPROVED'
backend/apps/notifications/services.py:65:        entity_type='approval',
backend/apps/notifications/services.py:67:        type=notification_type,
backend/apps/notifications/models.py:14:class NotificationType(models.TextChoices):
backend/apps/notifications/models.py:15:    APPLICATION_SUBMITTED = 'application_submitted', '申请已提交'
backend/apps/notifications/models.py:16:    APPROVAL_APPROVED = 'approval_approved', '审批通过'
backend/apps/notifications/models.py:51:        choices=NotificationType.choices,
backend/apps/notifications/migrations/0001_initial.py:22:                ('type', models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('dorm_clearance_blocked', '宿舍清退阻断'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型')),
backend/apps/notifications/tests/test_models.py:4:from apps.notifications.models import Notification, NotificationType, EntityType
backend/apps/notifications/tests/test_models.py:26:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:27:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:42:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_models.py:43:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:50:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_models.py:51:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:62:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:63:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:71:                type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:72:                entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:88:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:89:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:96:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:97:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:108:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_models.py:109:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_models.py:116:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_models.py:117:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:5:from apps.notifications.models import Notification, NotificationType, EntityType
backend/apps/notifications/tests/test_api.py:33:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:34:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:41:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_api.py:42:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:59:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:60:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:67:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_api.py:68:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:91:                type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:92:                entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:111:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:112:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:119:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:120:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:134:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:135:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:142:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_api.py:143:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:160:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:161:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:180:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:181:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:201:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:202:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:226:            type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/tests/test_api.py:227:            entity_type=EntityType.APPLICATION,
backend/apps/notifications/tests/test_api.py:234:            type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/tests/test_api.py:235:            entity_type=EntityType.APPLICATION,
backend/apps/applications/tests/test_p0_fixes.py:139:        self.approval_approved = Approval.objects.create(
backend/apps/applications/views.py:14:from apps.notifications.services import notify_application_submitted
backend/apps/applications/views.py:135:    notify_application_submitted(application, counselor_approval)
backend/apps/notifications/tests/test_auto_notifications.py:5:- Student submits application (APPLICATION_SUBMITTED)
backend/apps/notifications/tests/test_auto_notifications.py:6:- Approval is approved (APPROVAL_APPROVED)
backend/apps/notifications/tests/test_auto_notifications.py:17:from apps.notifications.services import notify_application_submitted, notify_approval_decided
backend/apps/notifications/tests/test_auto_notifications.py:44:    def test_application_submitted_notification(self):
backend/apps/notifications/tests/test_auto_notifications.py:45:        """Test APPLICATION_SUBMITTED notification creation."""
backend/apps/notifications/tests/test_auto_notifications.py:65:        notification, created = notify_application_submitted(application, approval)
backend/apps/notifications/tests/test_auto_notifications.py:70:        self.assertEqual(notification.type, 'APPLICATION_SUBMITTED')
backend/apps/notifications/tests/test_auto_notifications.py:76:    def test_approval_approved_notification_counselor(self):
backend/apps/notifications/tests/test_auto_notifications.py:77:        """Test APPROVAL_APPROVED notification for counselor approval."""
backend/apps/notifications/tests/test_auto_notifications.py:102:        self.assertEqual(notification.type, 'APPROVAL_APPROVED')
backend/apps/notifications/tests/test_auto_notifications.py:107:    def test_approval_approved_notification_dean(self):
backend/apps/notifications/tests/test_auto_notifications.py:108:        """Test APPROVAL_APPROVED notification for dean approval."""
backend/apps/notifications/tests/test_auto_notifications.py:133:        self.assertEqual(notification.type, 'APPROVAL_APPROVED')
backend/apps/notifications/tests/test_auto_notifications.py:167:    def test_idempotency_application_submitted(self):
backend/apps/notifications/tests/test_auto_notifications.py:188:        notification1, created1 = notify_application_submitted(application, approval)
backend/apps/notifications/tests/test_auto_notifications.py:191:        notification2, created2 = notify_application_submitted(application, approval)
backend/apps/notifications/tests/test_auto_notifications.py:197:            entity_type='approval',
backend/apps/notifications/tests/test_auto_notifications.py:199:            type='APPLICATION_SUBMITTED'
backend/apps/notifications/tests/test_auto_notifications.py:232:            entity_type='approval',
backend/apps/notifications/tests/test_auto_notifications.py:234:            type='APPROVAL_APPROVED'
backend/apps/notifications/management/commands/seed_notifications.py:4:from apps.notifications.models import Notification, NotificationType, EntityType
backend/apps/notifications/management/commands/seed_notifications.py:22:                type=NotificationType.APPLICATION_SUBMITTED,
backend/apps/notifications/management/commands/seed_notifications.py:23:                entity_type=EntityType.APPLICATION,
backend/apps/notifications/management/commands/seed_notifications.py:33:                    type=NotificationType.APPROVAL_APPROVED,
backend/apps/notifications/management/commands/seed_notifications.py:34:                    entity_type=EntityType.APPLICATION,

exec
/bin/bash -lc "rtk rg -n \"rest_framework|INSTALLED_APPS|DEFAULT_SCHEMA_CLASS|spectacular\" backend/config backend -g '*.py'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/config/settings/base.py:18:INSTALLED_APPS = [
backend/config/settings/base.py:27:    'rest_framework',
backend/config/settings/base.py:28:    'rest_framework_simplejwt',
backend/config/settings/base.py:114:        'rest_framework_simplejwt.authentication.JWTAuthentication',
backend/config/settings/base.py:117:        'rest_framework.permissions.IsAuthenticated',
backend/config/settings/base.py:120:        'rest_framework.renderers.JSONRenderer',
backend/config/settings/base.py:123:        'rest_framework.parsers.JSONParser',
backend/apps/approvals/pagination.py:1:from rest_framework.pagination import LimitOffsetPagination
backend/apps/approvals/pagination.py:2:from rest_framework.response import Response
backend/apps/approvals/tests/test_rejection_flow.py:2:from rest_framework.test import APIClient
backend/apps/approvals/tests/test_rejection_flow.py:3:from rest_framework import status
backend/apps/approvals/tests/test_list_permissions.py:2:from rest_framework.test import APIClient
backend/apps/approvals/tests/test_permissions.py:2:from rest_framework.test import APIClient
backend/apps/approvals/tests/test_permissions.py:3:from rest_framework import status
backend/apps/approvals/tests/test_state_machine.py:2:from rest_framework.test import APIClient
backend/apps/approvals/tests/test_state_machine.py:3:from rest_framework import status
backend/apps/approvals/views.py:1:from rest_framework import status
backend/apps/approvals/views.py:2:from rest_framework.decorators import api_view, permission_classes
backend/apps/approvals/views.py:3:from rest_framework.permissions import IsAuthenticated
backend/apps/approvals/views.py:4:from rest_framework.response import Response
backend/apps/approvals/serializers.py:1:from rest_framework import serializers
backend/apps/notifications/tests/test_api.py:3:from rest_framework.test import APIClient
backend/apps/notifications/views.py:2:from rest_framework import status
backend/apps/notifications/views.py:3:from rest_framework.decorators import api_view, permission_classes
backend/apps/notifications/views.py:4:from rest_framework.permissions import IsAuthenticated
backend/apps/notifications/views.py:5:from rest_framework.response import Response
backend/apps/applications/pagination.py:1:from rest_framework.pagination import LimitOffsetPagination
backend/apps/applications/pagination.py:2:from rest_framework.response import Response
backend/apps/notifications/serializers.py:1:from rest_framework import serializers
backend/apps/applications/tests/test_error_cases.py:2:from rest_framework.test import APIClient
backend/apps/applications/tests/test_error_cases.py:3:from rest_framework import status
backend/apps/applications/tests/test_detail_permissions.py:2:from rest_framework.test import APIClient
backend/apps/attachments/tests/test_list.py:3:from rest_framework.test import APIClient
backend/apps/attachments/tests/test_list.py:4:from rest_framework import status
backend/apps/attachments/tests/test_delete.py:3:from rest_framework.test import APIClient
backend/apps/attachments/tests/test_delete.py:4:from rest_framework import status
backend/apps/applications/tests/test_list_permissions.py:2:from rest_framework.test import APIClient
backend/apps/applications/tests/test_constraints.py:2:from rest_framework.test import APIClient
backend/apps/applications/tests/test_constraints.py:3:from rest_framework import status
backend/apps/applications/tests/test_application_flow.py:2:from rest_framework.test import APIClient
backend/apps/applications/tests/test_application_flow.py:3:from rest_framework import status
backend/apps/applications/views.py:1:from rest_framework import status
backend/apps/applications/views.py:2:from rest_framework.decorators import api_view, permission_classes
backend/apps/applications/views.py:3:from rest_framework.permissions import IsAuthenticated
backend/apps/applications/views.py:4:from rest_framework.response import Response
backend/config/settings/base.py:18:INSTALLED_APPS = [
backend/config/settings/base.py:27:    'rest_framework',
backend/config/settings/base.py:28:    'rest_framework_simplejwt',
backend/config/settings/base.py:114:        'rest_framework_simplejwt.authentication.JWTAuthentication',
backend/config/settings/base.py:117:        'rest_framework.permissions.IsAuthenticated',
backend/config/settings/base.py:120:        'rest_framework.renderers.JSONRenderer',
backend/config/settings/base.py:123:        'rest_framework.parsers.JSONParser',
backend/apps/attachments/serializers.py:1:from rest_framework import serializers
backend/apps/attachments/tests/test_download.py:3:from rest_framework.test import APIClient
backend/apps/attachments/tests/test_download.py:4:from rest_framework import status
backend/apps/applications/serializers.py:1:from rest_framework import serializers
backend/apps/attachments/views.py:1:from rest_framework import status
backend/apps/attachments/views.py:2:from rest_framework.decorators import api_view, permission_classes, parser_classes
backend/apps/attachments/views.py:3:from rest_framework.permissions import IsAuthenticated
backend/apps/attachments/views.py:4:from rest_framework.parsers import MultiPartParser, FormParser
backend/apps/attachments/views.py:5:from rest_framework.response import Response
backend/apps/attachments/tests/test_upload.py:3:from rest_framework.test import APIClient
backend/apps/attachments/tests/test_upload.py:4:from rest_framework import status
backend/apps/users/serializers.py:1:from rest_framework import serializers
backend/apps/users/serializers.py:2:from rest_framework_simplejwt.tokens import RefreshToken
backend/apps/users/views.py:1:from rest_framework import status
backend/apps/users/views.py:2:from rest_framework.decorators import api_view, permission_classes
backend/apps/users/views.py:3:from rest_framework.permissions import AllowAny
backend/apps/users/views.py:4:from rest_framework.response import Response

exec
/bin/bash -lc "rtk sed -n '280,560p' backend/apps/notifications/tests/test_auto_notifications.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
exec
/bin/bash -lc "rtk sed -n '1,160p' backend/apps/notifications/serializers.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'notification_id',
            'recipient_id',
            'actor_id',
            'type',
            'entity_type',
            'entity_id',
            'title',
            'message',
            'read_at',
            'created_at'
        ]
        read_only_fields = ['notification_id', 'created_at']

    recipient_id = serializers.CharField(source='recipient.user_id', read_only=True)
    actor_id = serializers.CharField(source='actor.user_id', read_only=True, allow_null=True)

exec
/bin/bash -lc "rtk sed -n '1,180p' backend/apps/notifications/views.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    """
    GET /api/notifications/
    列出当前用户的通知
    查询参数：
    - read: all/read/unread (默认all)
    - limit: 每页数量 (默认20)
    - offset: 偏移量 (默认0)
    """
    user = request.user
    read_filter = request.query_params.get('read', 'all')
    limit = int(request.query_params.get('limit', 20))
    offset = int(request.query_params.get('offset', 0))

    queryset = Notification.objects.filter(recipient=user)

    if read_filter == 'read':
        queryset = queryset.filter(read_at__isnull=False)
    elif read_filter == 'unread':
        queryset = queryset.filter(read_at__isnull=True)

    count = queryset.count()
    notifications = queryset[offset:offset + limit]
    serializer = NotificationSerializer(notifications, many=True)

    return Response({
        'count': count,
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_count(request):
    """
    GET /api/notifications/unread_count/
    获取当前用户的未读通知数
    """
    user = request.user
    count = Notification.objects.filter(recipient=user, read_at__isnull=True).count()
    return Response({'unread_count': count})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id):
    """
    PATCH /api/notifications/{notification_id}/read/
    标记通知为已读（幂等）
    """
    user = request.user

    try:
        notification = Notification.objects.get(notification_id=notification_id)
    except Notification.DoesNotExist:
        return Response(
            {'error': {'code': 'NOT_FOUND', 'message': '通知不存在'}},
            status=status.HTTP_404_NOT_FOUND
        )

    if notification.recipient != user:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '无权访问此通知'}},
            status=status.HTTP_403_FORBIDDEN
        )

    if notification.read_at is None:
        notification.read_at = timezone.now()
        notification.save(update_fields=['read_at'])

    serializer = NotificationSerializer(notification)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_read(request):
    """
    POST /api/notifications/mark_all_read/
    标记当前用户的所有未读通知为已读
    """
    user = request.user
    now = timezone.now()
    updated_count = Notification.objects.filter(
        recipient=user,
        read_at__isnull=True
    ).update(read_at=now)

    return Response({'marked_count': updated_count})

exec
/bin/bash -lc "rtk nl -ba backend/apps/notifications/services.py | sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""
     2	Notification service layer for idempotent notification creation.
     3	
     4	This module provides business logic for creating notifications automatically
     5	when key events occur (application submission, approval decisions).
     6	"""
     7	
     8	from django.contrib.auth import get_user_model
     9	from .models import Notification
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
    33	        type='APPLICATION_SUBMITTED',
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
    57	        notification_type = 'APPROVAL_APPROVED'
    58	    else:  # rejected
    59	        title = "审批驳回"
    60	        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
    61	        notification_type = 'APPROVAL_REJECTED'
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
/bin/bash -lc "rtk nl -ba backend/apps/approvals/views.py | sed -n '88,135p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    88	
    89	    if approval.decision != ApprovalDecision.PENDING:
    90	        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
    91	                        status=status.HTTP_409_CONFLICT)
    92	
    93	    if not approval_step_matches_application_status(approval):
    94	        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
    95	                        status=status.HTTP_409_CONFLICT)
    96	
    97	    serializer = ApprovalActionSerializer(data=request.data)
    98	    if not serializer.is_valid():
    99	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
   100	                        status=status.HTTP_400_BAD_REQUEST)
   101	
   102	    approval.decision = ApprovalDecision.APPROVED
   103	    approval.comment = serializer.validated_data.get('comment', '')
   104	    approval.decided_at = timezone.now()
   105	    approval.save()
   106	
   107	    notify_approval_decided(approval)
   108	
   109	    application = approval.application
   110	    if approval.step == ApprovalStep.COUNSELOR:
   111	        # Check for existing dean approval to prevent duplicates
   112	        existing_dean_approval = Approval.objects.filter(
   113	            application=application,
   114	            step=ApprovalStep.DEAN
   115	        ).exists()
   116	
   117	        if existing_dean_approval:
   118	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
   119	                            status=status.HTTP_409_CONFLICT)
   120	
   121	        application.status = ApplicationStatus.PENDING_DEAN
   122	        application.save()
   123	        Approval.objects.create(
   124	            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   125	            application=application,
   126	            step=ApprovalStep.DEAN,
   127	            approver_id='D001',
   128	            approver_name='赵主任',
   129	            decision=ApprovalDecision.PENDING
   130	        )
   131	    elif approval.step == ApprovalStep.DEAN:
   132	        application.status = ApplicationStatus.APPROVED
   133	        application.save()
   134	
   135	    return Response(ApprovalSerializer(approval).data)

exec
/bin/bash -lc "rtk nl -ba docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md | sed -n '220,310p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   220	---
   221	
   222	## Claude建议：Option E + 部分Option A
   223	
   224	**推荐策略：测试文档完善 + 选择性通知增强**
   225	
   226	### 主线1: 测试和文档完善（1.5-2小时）
   227	
   228	**任务1: API文档生成（30分钟）**
   229	- 使用drf-spectacular生成OpenAPI schema
   230	- 配置Swagger UI
   231	- 验证所有API端点文档完整
   232	
   233	**任务2: 端到端测试增强（45分钟）**
   234	- 扩展smoke_test.sh覆盖更多场景
   235	- 添加负向测试用例（权限拒绝、状态冲突）
   236	- 验证错误处理完整性
   237	
   238	**任务3: 部署文档优化（30分钟）**
   239	- 更新DEPLOYMENT.md
   240	- 添加故障排查指南
   241	- 补充环境变量说明
   242	
   243	### 主线2: 选择性通知增强（可选，1小时）
   244	
   245	**仅实现Phase 2B（宿舍阻断通知）：**
   246	- 契约修正：允许`entity_type=student`，`entity_id=student.id`
   247	- 实现`notify_dorm_clearance_blocked(student, dorm_status)`
   248	- 在views.py:105返回422前调用通知服务
   249	- 添加测试验证
   250	
   251	**不实现Phase 2C（审批超时提醒）：**
   252	- 需要Celery基础设施（复杂度高）
   253	- 优先级P2（非核心）
   254	- 推迟到生产部署准备阶段
   255	
   256	### 理由
   257	
   258	1. **测试文档完善是当前最高价值工作：**
   259	   - 系统已具备核心功能
   260	   - 缺少完整API文档（交付必需）
   261	   - 端到端测试覆盖不足（质量保障）
   262	   - 部署文档需要优化（运维必需）
   263	
   264	2. **Phase 2B可选实现：**
   265	   - 契约修正相对简单（不影响现有通知）
   266	   - 提升用户体验（宿舍阻断时收到通知）
   267	   - 不引入新依赖（无Celery）
   268	   - 1小时可完成
   269	
   270	3. **Phase 2C推迟合理：**
   271	   - Celery引入复杂度高
   272	   - 审批超时提醒非核心功能
   273	   - 可通过审批列表查看待审批项
   274	
   275	4. **避免外部阻塞工作：**
   276	   - 不推进小程序前端（DevTools阻塞）
   277	   - 不推进宿舍真实集成（API文档阻塞）
   278	
   279	5. **为交付做准备：**
   280	   - API文档是交付必需品
   281	   - 完善的测试提升交付信心
   282	   - 优化的部署文档降低运维成本
   283	
   284	---
   285	
   286	## 验收标准
   287	
   288	**主线1（测试文档完善）：**
   289	1. Swagger UI可访问，所有API端点文档完整
   290	2. smoke_test.sh覆盖至少20个场景（当前15个）
   291	3. DEPLOYMENT.md包含故障排查指南和环境变量说明
   292	4. 所有测试通过
   293	
   294	**主线2（Phase 2B，可选）：**
   295	1. 宿舍阻断时学生收到DORM_CLEARANCE_BLOCKED通知
   296	2. 通知内容包含阻断原因
   297	3. 幂等性验证通过
   298	4. 测试覆盖通过
   299	
   300	---
   301	
   302	## 请Codex审查
   303	
   304	**审查要点：**
   305	1. Option E + 部分Option A策略是否合理？
   306	2. 是否有遗漏的高价值工作？
   307	3. Phase 2B（宿舍阻断通知）是否值得实现？
   308	4. Phase 2C（审批超时提醒）推迟是否合理？
   309	5. 测试文档完善的优先级是否正确？
   310	6. 是否应该硬停止等待外部解除阻塞？

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/views.py | sed -n '96,145p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    96	                                    'details': serializer.errors}},
    97	                        status=status.HTTP_400_BAD_REQUEST)
    98	
    99	    provider = MockDormCheckoutProvider()
   100	    dorm_status = provider.check_status(user.user_id)
   101	
   102	    if dorm_status.status != DormCheckoutStatus.COMPLETED:
   103	        return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
   104	                                    'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
   105	                                                'blocking_reason': dorm_status.blocking_reason}}},
   106	                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
   107	
   108	    try:
   109	        class_mapping = ClassMapping.objects.get(class_id=user.class_id, active=True)
   110	    except ClassMapping.DoesNotExist:
   111	        return Response({'error': {'code': 'NOT_FOUND', 'message': '班级映射不存在',
   112	                                    'details': {'class_id': user.class_id}}},
   113	                        status=status.HTTP_404_NOT_FOUND)
   114	
   115	    application = Application.objects.create(
   116	        application_id=f'app_{uuid.uuid4().hex[:8]}',
   117	        student=user,
   118	        student_name=user.name,
   119	        class_id=user.class_id,
   120	        reason=serializer.validated_data['reason'],
   121	        leave_date=serializer.validated_data['leave_date'],
   122	        status=ApplicationStatus.PENDING_COUNSELOR,
   123	        dorm_checkout_status=dorm_status.status
   124	    )
   125	
   126	    counselor_approval = Approval.objects.create(
   127	        approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   128	        application=application,
   129	        step=ApprovalStep.COUNSELOR,
   130	        approver=class_mapping.counselor,
   131	        approver_name=class_mapping.counselor_name,
   132	        decision=ApprovalDecision.PENDING
   133	    )
   134	
   135	    notify_application_submitted(application, counselor_approval)
   136	
   137	    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
   138	
   139	
   140	@api_view(['GET'])
   141	@permission_classes([IsAuthenticated])
   142	def get_application(request, application_id):
   143	    try:
   144	        application = Application.objects.get(application_id=application_id)
   145	    except Application.DoesNotExist:

codex
A concrete implementation risk surfaced: the notification service writes uppercase type strings while the model choices define lowercase values. I’m going to run the focused notification tests to see whether the current suite catches that or encodes the wrong expectation.
exec
/bin/bash -lc 'rtk python backend/manage.py test apps.notifications.tests.test_auto_notifications apps.notifications.tests.test_models apps.notifications.tests.test_api' in /home/caohui/projects/graduation-leave-system
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

exec
/bin/bash -lc 'rtk python manage.py test apps.notifications.tests.test_auto_notifications apps.notifications.tests.test_models apps.notifications.tests.test_api' in /home/caohui/projects/graduation-leave-system/backend
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

exec
/bin/bash -lc 'rtk ls -la backend' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
.omc/
apps/
config/
data/
docs/
media/
requirements/
utils/
.env  269B
Dockerfile  493B
manage.py  666B

exec
/bin/bash -lc 'rtk which python' in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
exec
/bin/bash -lc 'rtk which python3' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
/usr/bin/python3

exec
/bin/bash -lc 'rtk python3 manage.py test apps.notifications.tests.test_auto_notifications apps.notifications.tests.test_models apps.notifications.tests.test_api' in /home/caohui/projects/graduation-leave-system/backend
 exited 1 in 164ms:
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/manage.py", line 11, in main
    from django.core.management import execute_from_command_line
ModuleNotFoundError: No module named 'django'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/manage.py", line 22, in <module>
    main()
    ~~~~^^
  File "/home/caohui/projects/graduation-leave-system/backend/manage.py", line 13, in main
    raise ImportError(
    ...<3 lines>...
    ) from exc
ImportError: Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?

exec
/bin/bash -lc "rtk git diff -- backend/apps/notifications/services.py backend/apps/notifications/tests/test_auto_notifications.py tests/smoke_test.sh | sed -n '1,260p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
exec
/bin/bash -lc 'rtk ls -1 docs/discussions/phase4c-next-steps | tail -20' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
22-claude-post-execution-next-steps.md  4.9K
23-codex-post-execution-next-steps-response.md  7.1K
24-claude-consensus-evidence-closure.md  3.4K
25-claude-post-evidence-next-strategy.md  6.5K
26-codex-post-evidence-strategy-review.md  6.9K
27-claude-consensus-decision-gate.md  5.6K
28-claude-post-phase0-next-strategy.md  7.4K
29-codex-post-phase0-next-strategy-response.md  8.6K
29-codex-post-phase0-next-strategy-review.md  6.9K
30-claude-consensus-contract-revision-gate.md  5.8K
31-claude-post-contract-revision-next-strategy.md  10.5K
32-codex-post-contract-revision-next-strategy-response.md  7.5K
33-claude-consensus-authorization-gate.md  3.7K
34-claude-authorization-interpretation-request.md  3.6K
35-codex-authorization-interpretation-response.md  5.4K
36-claude-consensus-minimal-confirmation.md  1.9K
37-claude-post-phase1-next-strategy.md  6.6K
38-codex-post-phase1-next-strategy-response.md  9.3K
39-claude-consensus-option-a-lite.md  6.2K
40-claude-post-phase2a-next-strategy.md  8.3K

exec
/bin/bash -lc "rtk sed -n '1,220p' .env.example" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=graduation_leave
DB_USER=postgres
DB_PASSWORD=your_secure_password_here
DB_HOST=db
DB_PORT=5432

# Django Settings
SECRET_KEY=your-secret-key-here-generate-with-django-get-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost

# Media Files
MEDIA_ROOT=/app/media
MEDIA_URL=/media/

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=3600
JWT_REFRESH_TOKEN_LIFETIME=86400

# Redis (optional, for future use)
REDIS_HOST=localhost
REDIS_PORT=6379

# Celery (optional, for future use)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

codex
I have enough to write the formal Codex response. The response will accept the general move toward verification/docs, but it will make Phase 2A stabilization a gate because the current notification implementation and tests have a contract mismatch.
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
diff --git a/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md b/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..08ad4c90be7da58a2055e16db4c2d38a06595663
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
@@ -0,0 +1,237 @@
+# Track 3 Phase 2A后续策略 - Codex审查响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对文档：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md`  
+**审查类型：** Phase 2A后下一步策略审查
+
+---
+
+## 审查结论
+
+**结论：部分同意 Option E，但不同意立即把 Phase 2B 纳入“可选1小时增强”。**
+
+下一步不应硬停止，也不应继续扩大通知功能。建议改为：
+
+1. **先做 Phase 2A稳定化门禁**：修正自动通知实现与契约不一致的问题，补足现有测试缺口。
+2. **再做 Option E-lite**：API文档基线 + smoke回归增强 + 部署文档补漏。
+3. **暂缓 Phase 2B/2C**：宿舍阻断通知需要契约版本化或申请尝试实体设计；审批超时提醒继续推迟。
+
+当前系统已经进入“交付可信度提升”阶段，但在生成Swagger/OpenAPI之前，必须先避免把现有实现缺陷固化进文档。
+
+---
+
+## 关键问题
+
+### P1：Phase 2A仍有契约不一致，必须先修复再生成API文档
+
+**位置：** `backend/apps/notifications/services.py:33`、`backend/apps/notifications/services.py:57-61`、`backend/apps/notifications/models.py:14-18`
+
+`NotificationType`模型枚举值是小写字符串：
+
+- `application_submitted`
+- `approval_approved`
+- `approval_rejected`
+
+但自动通知服务写入的是大写常量名：
+
+- `APPLICATION_SUBMITTED`
+- `APPROVAL_APPROVED`
+- `APPROVAL_REJECTED`
+
+Django不会在普通`save()`/`get_or_create()`时自动校验`choices`，所以这类非法枚举值可以落库，并通过通知API返回。现有`test_auto_notifications.py`也断言大写值，等于把错误行为写进测试。
+
+**影响：**
+
+- OpenAPI/Swagger会暴露小写枚举，但自动通知API实际返回大写值。
+- 前端类型与后端运行时数据可能不一致。
+- 后续如果增加严格校验、导出、过滤或数据迁移，会出现脏数据。
+
+**建议：**
+
+先修正服务层使用`NotificationType.APPLICATION_SUBMITTED`等枚举值，而不是裸字符串常量名；同步修正测试断言为枚举值/小写值。这个修复应作为所有文档工作的前置门禁。
+
+### P1：Phase 2A测试覆盖没有达到前一轮共识验收
+
+**位置：** `backend/apps/notifications/tests/test_auto_notifications.py`
+
+当前自动通知测试覆盖了服务函数的正向创建和幂等，但没有覆盖关键API路径和负向路径：
+
+- `create_application`成功后辅导员通知是否通过API可见；
+- `approve_approval`/`reject_approval`成功后学生通知是否通过API可见；
+- 权限拒绝、状态冲突、参数校验失败、宿舍阻断时是否不创建通知；
+- 通知类型是否与契约枚举一致；
+- `APPROVAL_REJECTED`的真实API路径是否包含驳回原因。
+
+**建议：**
+
+在扩展`smoke_test.sh`之前，先补Django层的focused API测试。smoke适合端到端信心，不适合承担所有回归细节。
+
+### P1：drf-spectacular 30分钟生成“完整API文档”的估算偏乐观
+
+**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:228-231`
+
+当前后端大量使用function-based views和自定义错误响应 envelope。仅安装`drf-spectacular`并暴露Swagger UI，通常只能生成“可访问的schema”，不能保证：
+
+- 自定义错误码与`details`结构完整；
+- 登录响应token字段准确；
+- 文件上传multipart参数准确；
+- 分页响应、通知响应、审批动作请求体都有明确schema；
+- 权限与JWT认证说明准确。
+
+**建议：**
+
+把API文档任务拆成两级验收：
+
+1. 本轮：生成可访问的schema和Swagger UI，覆盖端点清单、认证、主要请求/响应对象。
+2. 后续：补`extend_schema`注解、错误码schema、文件上传schema、示例响应。
+
+不要把“所有API端点文档完整”作为1.5-2小时内的硬验收。
+
+### P2：Phase 2B不是简单契约修正，`entity_type=student`会引入新语义债务
+
+**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:245-249`
+
+宿舍阻断发生在`Application.objects.create()`之前，这一点判断正确。但直接允许`entity_type=student`并不只是简单改枚举：
+
+- 需要模型枚举、迁移、契约版本、seed/API测试同步更新；
+- 同一学生多次被阻断时，当前唯一约束`recipient + entity_type + entity_id + type`会天然去重，可能丢失不同阻断时间或不同阻断原因；
+- 学生阻断通知的业务价值有限，因为接口已经同步返回422和阻断原因；
+- 如果未来要审计“申请尝试”，`student`实体无法表达每次尝试的上下文。
+
+**建议：**
+
+本轮不要实现Phase 2B。若未来确实需要，应优先设计`application_attempt`或显式`dedupe_key`/`occurred_at`语义，而不是直接复用`student`作为实体。
+
+### P2：smoke测试应增强质量，不应追求“20个场景”数字
+
+**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:233-236`、`tests/smoke_test.sh`
+
+当前smoke已有15步，并已加入通知数量验证。但下一步更重要的是提升断言质量：
+
+- 验证通知`type`、`entity_type`、`entity_id`，而不只是未读数量；
+- 增加审批驳回路径，覆盖`APPROVAL_REJECTED`；
+- 验证通知权限隔离与`mark_as_read`；
+- 保证脚本可重复运行，或在文档中明确要求先重置数据库。
+
+**建议：**
+
+验收标准改为“覆盖关键端到端风险”，不要固定为“至少20个场景”。
+
+---
+
+## 对审查问题的回答
+
+### 1. Option E + 部分Option A策略是否合理？
+
+**Option E方向合理，但必须前置Phase 2A稳定化；部分Option A不建议本轮做。**
+
+当前最高价值不是增加新通知类型，而是让现有自动通知的契约、测试、API行为一致。完成这一步后，再做API文档、smoke增强、部署文档补漏是正确方向。
+
+### 2. 是否有遗漏的高价值工作？
+
+有。遗漏了“Phase 2A后验收修复”：
+
+1. 修复通知类型枚举大小写不一致。
+2. 补API路径级自动通知测试。
+3. 明确通知创建失败对核心流程的边界，至少用测试保证正常路径不产生脏数据。
+4. 在生成OpenAPI前确认API实际返回值与契约一致。
+
+这些比Phase 2B更高价值。
+
+### 3. Phase 2B是否值得实现？
+
+**本轮不值得。**
+
+宿舍阻断通知确实能增加一点用户体验，但同步422已经给了学生明确反馈。为这点价值引入`student`实体通知、迁移、幂等语义和契约版本变更，投入产出比不高。
+
+推荐记录为后续设计项：
+
+> Phase 2B只有在需要审计阻断历史或产品明确要求站内留痕时才启动；届时优先设计`application_attempt`，不要只把`entity_type=student`作为快捷方案。
+
+### 4. Phase 2C推迟是否合理？
+
+**合理。**
+
+审批超时提醒需要定时调度、工作日计算、重复提醒窗口、幂等键或提醒周期字段。即使`celery`依赖已经在`requirements`中，生产运行的Celery beat/worker、监控和部署复杂度仍然没有准备好。当前阶段不应引入。
+
+### 5. 测试文档完善的优先级是否正确？
+
+**正确，但顺序应调整。**
+
+推荐顺序：
+
+1. Phase 2A稳定化修复和focused tests。
+2. smoke脚本增强，覆盖真实API行为。
+3. OpenAPI/Swagger基线。
+4. 部署文档补漏。
+
+如果先生成文档，容易把当前错误枚举和不完整schema固化为“交付事实”。
+
+### 6. 是否应该硬停止等待外部解除阻塞？
+
+**不应该硬停止。**
+
+WeChat DevTools和宿舍系统API确实阻塞小程序验收和真实集成，但不阻塞后端交付质量工作。当前可以继续推进不依赖外部系统的验收、文档和测试闭环。
+
+---
+
+## 最终推荐策略
+
+**推荐执行 Option E-lite + Phase 2A稳定化门禁，暂不执行Phase 2B/2C。**
+
+### Step 0：Phase 2A稳定化门禁（优先，0.5-1小时）
+
+- 修复自动通知`type`使用小写枚举值。
+- 修正`test_auto_notifications.py`中错误的大写断言。
+- 补至少1-2个API路径级测试，验证提交/审批后通知API返回契约值。
+- 验证宿舍阻断、权限拒绝、状态冲突不创建通知。
+
+### Step 1：smoke增强（0.5-1小时）
+
+- 不追求场景数量，改为验证关键通知字段。
+- 增加审批驳回通知路径或单独负向脚本。
+- 明确脚本运行前置条件：干净seed数据或自动重置策略。
+
+### Step 2：API文档基线（1-2小时）
+
+- 引入并配置`drf-spectacular`。
+- 暴露schema和Swagger UI。
+- 至少覆盖认证、申请、审批、附件、通知端点清单。
+- 对自定义错误响应和文件上传标注“后续完善”，不要声称已完整。
+
+### Step 3：部署文档补漏（0.5小时）
+
+- 补环境变量表：用途、默认值、生产是否必填。
+- 补smoke运行前置条件。
+- 补常见失败：重复申请导致409、宿舍阻断422、JWT过期、media权限。
+
+---
+
+## 修订验收标准
+
+1. 自动通知落库`type`与`NotificationType`枚举/契约一致。
+2. 现有通知API返回值与OpenAPI枚举一致。
+3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
+4. 权限拒绝、状态冲突、参数校验失败、宿舍阻断不创建误通知。
+5. Swagger UI可访问，端点清单完整，主要请求/响应对象可读。
+6. `DEPLOYMENT.md`包含环境变量说明、smoke前置条件和故障排查。
+7. 所有可运行的后端测试通过；若本地环境缺依赖，必须记录未运行原因。
+
+---
+
+## 最终裁决
+
+给Claude的执行口径：
+
+> 下一步不要启动Phase 2B/2C，也不要硬停止。先修复Phase 2A自动通知的契约一致性和测试缺口，再推进Option E-lite：smoke增强、OpenAPI基线、部署文档补漏。Phase 2B只有在需要审计阻断历史时再以`application_attempt`或明确幂等语义重新设计；Phase 2C继续推迟到Celery运行方案确定后。
+
+---
+
+**验证记录：**
+
+- 已检查`40-claude-post-phase2a-next-strategy.md`。
+- 已检查通知模型、服务层、应用提交和审批视图、自动通知测试、smoke脚本、部署文档。
+- 尝试运行通知测试：`python3 manage.py test apps.notifications...`，本地环境缺少Django依赖，未能执行。
+
+**Codex状态：** 建议按“Phase 2A稳定化门禁 + Option E-lite”达成共识后执行。

diff --git a/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md b/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..08ad4c90be7da58a2055e16db4c2d38a06595663
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
@@ -0,0 +1,237 @@
+# Track 3 Phase 2A后续策略 - Codex审查响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对文档：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md`  
+**审查类型：** Phase 2A后下一步策略审查
+
+---
+
+## 审查结论
+
+**结论：部分同意 Option E，但不同意立即把 Phase 2B 纳入“可选1小时增强”。**
+
+下一步不应硬停止，也不应继续扩大通知功能。建议改为：
+
+1. **先做 Phase 2A稳定化门禁**：修正自动通知实现与契约不一致的问题，补足现有测试缺口。
+2. **再做 Option E-lite**：API文档基线 + smoke回归增强 + 部署文档补漏。
+3. **暂缓 Phase 2B/2C**：宿舍阻断通知需要契约版本化或申请尝试实体设计；审批超时提醒继续推迟。
+
+当前系统已经进入“交付可信度提升”阶段，但在生成Swagger/OpenAPI之前，必须先避免把现有实现缺陷固化进文档。
+
+---
+
+## 关键问题
+
+### P1：Phase 2A仍有契约不一致，必须先修复再生成API文档
+
+**位置：** `backend/apps/notifications/services.py:33`、`backend/apps/notifications/services.py:57-61`、`backend/apps/notifications/models.py:14-18`
+
+`NotificationType`模型枚举值是小写字符串：
+
+- `application_submitted`
+- `approval_approved`
+- `approval_rejected`
+
+但自动通知服务写入的是大写常量名：
+
+- `APPLICATION_SUBMITTED`
+- `APPROVAL_APPROVED`
+- `APPROVAL_REJECTED`
+
+Django不会在普通`save()`/`get_or_create()`时自动校验`choices`，所以这类非法枚举值可以落库，并通过通知API返回。现有`test_auto_notifications.py`也断言大写值，等于把错误行为写进测试。
+
+**影响：**
+
+- OpenAPI/Swagger会暴露小写枚举，但自动通知API实际返回大写值。
+- 前端类型与后端运行时数据可能不一致。
+- 后续如果增加严格校验、导出、过滤或数据迁移，会出现脏数据。
+
+**建议：**
+
+先修正服务层使用`NotificationType.APPLICATION_SUBMITTED`等枚举值，而不是裸字符串常量名；同步修正测试断言为枚举值/小写值。这个修复应作为所有文档工作的前置门禁。
+
+### P1：Phase 2A测试覆盖没有达到前一轮共识验收
+
+**位置：** `backend/apps/notifications/tests/test_auto_notifications.py`
+
+当前自动通知测试覆盖了服务函数的正向创建和幂等，但没有覆盖关键API路径和负向路径：
+
+- `create_application`成功后辅导员通知是否通过API可见；
+- `approve_approval`/`reject_approval`成功后学生通知是否通过API可见；
+- 权限拒绝、状态冲突、参数校验失败、宿舍阻断时是否不创建通知；
+- 通知类型是否与契约枚举一致；
+- `APPROVAL_REJECTED`的真实API路径是否包含驳回原因。
+
+**建议：**
+
+在扩展`smoke_test.sh`之前，先补Django层的focused API测试。smoke适合端到端信心，不适合承担所有回归细节。
+
+### P1：drf-spectacular 30分钟生成“完整API文档”的估算偏乐观
+
+**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:228-231`
+
+当前后端大量使用function-based views和自定义错误响应 envelope。仅安装`drf-spectacular`并暴露Swagger UI，通常只能生成“可访问的schema”，不能保证：
+
+- 自定义错误码与`details`结构完整；
+- 登录响应token字段准确；
+- 文件上传multipart参数准确；
+- 分页响应、通知响应、审批动作请求体都有明确schema；
+- 权限与JWT认证说明准确。
+
+**建议：**
+
+把API文档任务拆成两级验收：
+
+1. 本轮：生成可访问的schema和Swagger UI，覆盖端点清单、认证、主要请求/响应对象。
+2. 后续：补`extend_schema`注解、错误码schema、文件上传schema、示例响应。
+
+不要把“所有API端点文档完整”作为1.5-2小时内的硬验收。
+
+### P2：Phase 2B不是简单契约修正，`entity_type=student`会引入新语义债务
+
+**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:245-249`
+
+宿舍阻断发生在`Application.objects.create()`之前，这一点判断正确。但直接允许`entity_type=student`并不只是简单改枚举：
+
+- 需要模型枚举、迁移、契约版本、seed/API测试同步更新；
+- 同一学生多次被阻断时，当前唯一约束`recipient + entity_type + entity_id + type`会天然去重，可能丢失不同阻断时间或不同阻断原因；
+- 学生阻断通知的业务价值有限，因为接口已经同步返回422和阻断原因；
+- 如果未来要审计“申请尝试”，`student`实体无法表达每次尝试的上下文。
+
+**建议：**
+
+本轮不要实现Phase 2B。若未来确实需要，应优先设计`application_attempt`或显式`dedupe_key`/`occurred_at`语义，而不是直接复用`student`作为实体。
+
+### P2：smoke测试应增强质量，不应追求“20个场景”数字
+
+**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:233-236`、`tests/smoke_test.sh`
+
+当前smoke已有15步，并已加入通知数量验证。但下一步更重要的是提升断言质量：
+
+- 验证通知`type`、`entity_type`、`entity_id`，而不只是未读数量；
+- 增加审批驳回路径，覆盖`APPROVAL_REJECTED`；
+- 验证通知权限隔离与`mark_as_read`；
+- 保证脚本可重复运行，或在文档中明确要求先重置数据库。
+
+**建议：**
+
+验收标准改为“覆盖关键端到端风险”，不要固定为“至少20个场景”。
+
+---
+
+## 对审查问题的回答
+
+### 1. Option E + 部分Option A策略是否合理？
+
+**Option E方向合理，但必须前置Phase 2A稳定化；部分Option A不建议本轮做。**
+
+当前最高价值不是增加新通知类型，而是让现有自动通知的契约、测试、API行为一致。完成这一步后，再做API文档、smoke增强、部署文档补漏是正确方向。
+
+### 2. 是否有遗漏的高价值工作？
+
+有。遗漏了“Phase 2A后验收修复”：
+
+1. 修复通知类型枚举大小写不一致。
+2. 补API路径级自动通知测试。
+3. 明确通知创建失败对核心流程的边界，至少用测试保证正常路径不产生脏数据。
+4. 在生成OpenAPI前确认API实际返回值与契约一致。
+
+这些比Phase 2B更高价值。
+
+### 3. Phase 2B是否值得实现？
+
+**本轮不值得。**
+
+宿舍阻断通知确实能增加一点用户体验，但同步422已经给了学生明确反馈。为这点价值引入`student`实体通知、迁移、幂等语义和契约版本变更，投入产出比不高。
+
+推荐记录为后续设计项：
+
+> Phase 2B只有在需要审计阻断历史或产品明确要求站内留痕时才启动；届时优先设计`application_attempt`，不要只把`entity_type=student`作为快捷方案。
+
+### 4. Phase 2C推迟是否合理？
+
+**合理。**
+
+审批超时提醒需要定时调度、工作日计算、重复提醒窗口、幂等键或提醒周期字段。即使`celery`依赖已经在`requirements`中，生产运行的Celery beat/worker、监控和部署复杂度仍然没有准备好。当前阶段不应引入。
+
+### 5. 测试文档完善的优先级是否正确？
+
+**正确，但顺序应调整。**
+
+推荐顺序：
+
+1. Phase 2A稳定化修复和focused tests。
+2. smoke脚本增强，覆盖真实API行为。
+3. OpenAPI/Swagger基线。
+4. 部署文档补漏。
+
+如果先生成文档，容易把当前错误枚举和不完整schema固化为“交付事实”。
+
+### 6. 是否应该硬停止等待外部解除阻塞？
+
+**不应该硬停止。**
+
+WeChat DevTools和宿舍系统API确实阻塞小程序验收和真实集成，但不阻塞后端交付质量工作。当前可以继续推进不依赖外部系统的验收、文档和测试闭环。
+
+---
+
+## 最终推荐策略
+
+**推荐执行 Option E-lite + Phase 2A稳定化门禁，暂不执行Phase 2B/2C。**
+
+### Step 0：Phase 2A稳定化门禁（优先，0.5-1小时）
+
+- 修复自动通知`type`使用小写枚举值。
+- 修正`test_auto_notifications.py`中错误的大写断言。
+- 补至少1-2个API路径级测试，验证提交/审批后通知API返回契约值。
+- 验证宿舍阻断、权限拒绝、状态冲突不创建通知。
+
+### Step 1：smoke增强（0.5-1小时）
+
+- 不追求场景数量，改为验证关键通知字段。
+- 增加审批驳回通知路径或单独负向脚本。
+- 明确脚本运行前置条件：干净seed数据或自动重置策略。
+
+### Step 2：API文档基线（1-2小时）
+
+- 引入并配置`drf-spectacular`。
+- 暴露schema和Swagger UI。
+- 至少覆盖认证、申请、审批、附件、通知端点清单。
+- 对自定义错误响应和文件上传标注“后续完善”，不要声称已完整。
+
+### Step 3：部署文档补漏（0.5小时）
+
+- 补环境变量表：用途、默认值、生产是否必填。
+- 补smoke运行前置条件。
+- 补常见失败：重复申请导致409、宿舍阻断422、JWT过期、media权限。
+
+---
+
+## 修订验收标准
+
+1. 自动通知落库`type`与`NotificationType`枚举/契约一致。
+2. 现有通知API返回值与OpenAPI枚举一致。
+3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
+4. 权限拒绝、状态冲突、参数校验失败、宿舍阻断不创建误通知。
+5. Swagger UI可访问，端点清单完整，主要请求/响应对象可读。
+6. `DEPLOYMENT.md`包含环境变量说明、smoke前置条件和故障排查。
+7. 所有可运行的后端测试通过；若本地环境缺依赖，必须记录未运行原因。
+
+---
+
+## 最终裁决
+
+给Claude的执行口径：
+
+> 下一步不要启动Phase 2B/2C，也不要硬停止。先修复Phase 2A自动通知的契约一致性和测试缺口，再推进Option E-lite：smoke增强、OpenAPI基线、部署文档补漏。Phase 2B只有在需要审计阻断历史时再以`application_attempt`或明确幂等语义重新设计；Phase 2C继续推迟到Celery运行方案确定后。
+
+---
+
+**验证记录：**
+
+- 已检查`40-claude-post-phase2a-next-strategy.md`。
+- 已检查通知模型、服务层、应用提交和审批视图、自动通知测试、smoke脚本、部署文档。
+- 尝试运行通知测试：`python3 manage.py test apps.notifications...`，本地环境缺少Django依赖，未能执行。
+
+**Codex状态：** 建议按“Phase 2A稳定化门禁 + Option E-lite”达成共识后执行。

codex
The review artifact is written. I’ll do a quick sanity check on the new file and the worktree state so the final response can point to the exact output and note verification limits.
exec
/bin/bash -lc 'rtk git status --short docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
?? docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Track 3 Phase 2A后续策略 - Codex审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对文档：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md`  
**审查类型：** Phase 2A后下一步策略审查

---

## 审查结论

**结论：部分同意 Option E，但不同意立即把 Phase 2B 纳入“可选1小时增强”。**

下一步不应硬停止，也不应继续扩大通知功能。建议改为：

1. **先做 Phase 2A稳定化门禁**：修正自动通知实现与契约不一致的问题，补足现有测试缺口。
2. **再做 Option E-lite**：API文档基线 + smoke回归增强 + 部署文档补漏。
3. **暂缓 Phase 2B/2C**：宿舍阻断通知需要契约版本化或申请尝试实体设计；审批超时提醒继续推迟。

当前系统已经进入“交付可信度提升”阶段，但在生成Swagger/OpenAPI之前，必须先避免把现有实现缺陷固化进文档。

---

## 关键问题

### P1：Phase 2A仍有契约不一致，必须先修复再生成API文档

**位置：** `backend/apps/notifications/services.py:33`、`backend/apps/notifications/services.py:57-61`、`backend/apps/notifications/models.py:14-18`

`NotificationType`模型枚举值是小写字符串：

- `application_submitted`
- `approval_approved`
- `approval_rejected`

但自动通知服务写入的是大写常量名：

- `APPLICATION_SUBMITTED`
- `APPROVAL_APPROVED`
- `APPROVAL_REJECTED`

Django不会在普通`save()`/`get_or_create()`时自动校验`choices`，所以这类非法枚举值可以落库，并通过通知API返回。现有`test_auto_notifications.py`也断言大写值，等于把错误行为写进测试。

**影响：**

- OpenAPI/Swagger会暴露小写枚举，但自动通知API实际返回大写值。
- 前端类型与后端运行时数据可能不一致。
- 后续如果增加严格校验、导出、过滤或数据迁移，会出现脏数据。

**建议：**

先修正服务层使用`NotificationType.APPLICATION_SUBMITTED`等枚举值，而不是裸字符串常量名；同步修正测试断言为枚举值/小写值。这个修复应作为所有文档工作的前置门禁。

### P1：Phase 2A测试覆盖没有达到前一轮共识验收

**位置：** `backend/apps/notifications/tests/test_auto_notifications.py`

当前自动通知测试覆盖了服务函数的正向创建和幂等，但没有覆盖关键API路径和负向路径：

- `create_application`成功后辅导员通知是否通过API可见；
- `approve_approval`/`reject_approval`成功后学生通知是否通过API可见；
- 权限拒绝、状态冲突、参数校验失败、宿舍阻断时是否不创建通知；
- 通知类型是否与契约枚举一致；
- `APPROVAL_REJECTED`的真实API路径是否包含驳回原因。

**建议：**

在扩展`smoke_test.sh`之前，先补Django层的focused API测试。smoke适合端到端信心，不适合承担所有回归细节。

### P1：drf-spectacular 30分钟生成“完整API文档”的估算偏乐观

**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:228-231`

当前后端大量使用function-based views和自定义错误响应 envelope。仅安装`drf-spectacular`并暴露Swagger UI，通常只能生成“可访问的schema”，不能保证：

- 自定义错误码与`details`结构完整；
- 登录响应token字段准确；
- 文件上传multipart参数准确；
- 分页响应、通知响应、审批动作请求体都有明确schema；
- 权限与JWT认证说明准确。

**建议：**

把API文档任务拆成两级验收：

1. 本轮：生成可访问的schema和Swagger UI，覆盖端点清单、认证、主要请求/响应对象。
2. 后续：补`extend_schema`注解、错误码schema、文件上传schema、示例响应。

不要把“所有API端点文档完整”作为1.5-2小时内的硬验收。

### P2：Phase 2B不是简单契约修正，`entity_type=student`会引入新语义债务

**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:245-249`

宿舍阻断发生在`Application.objects.create()`之前，这一点判断正确。但直接允许`entity_type=student`并不只是简单改枚举：

- 需要模型枚举、迁移、契约版本、seed/API测试同步更新；
- 同一学生多次被阻断时，当前唯一约束`recipient + entity_type + entity_id + type`会天然去重，可能丢失不同阻断时间或不同阻断原因；
- 学生阻断通知的业务价值有限，因为接口已经同步返回422和阻断原因；
- 如果未来要审计“申请尝试”，`student`实体无法表达每次尝试的上下文。

**建议：**

本轮不要实现Phase 2B。若未来确实需要，应优先设计`application_attempt`或显式`dedupe_key`/`occurred_at`语义，而不是直接复用`student`作为实体。

### P2：smoke测试应增强质量，不应追求“20个场景”数字

**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:233-236`、`tests/smoke_test.sh`

当前smoke已有15步，并已加入通知数量验证。但下一步更重要的是提升断言质量：

- 验证通知`type`、`entity_type`、`entity_id`，而不只是未读数量；
- 增加审批驳回路径，覆盖`APPROVAL_REJECTED`；
- 验证通知权限隔离与`mark_as_read`；
- 保证脚本可重复运行，或在文档中明确要求先重置数据库。

**建议：**

验收标准改为“覆盖关键端到端风险”，不要固定为“至少20个场景”。

---

## 对审查问题的回答

### 1. Option E + 部分Option A策略是否合理？

**Option E方向合理，但必须前置Phase 2A稳定化；部分Option A不建议本轮做。**

当前最高价值不是增加新通知类型，而是让现有自动通知的契约、测试、API行为一致。完成这一步后，再做API文档、smoke增强、部署文档补漏是正确方向。

### 2. 是否有遗漏的高价值工作？

有。遗漏了“Phase 2A后验收修复”：

1. 修复通知类型枚举大小写不一致。
2. 补API路径级自动通知测试。
3. 明确通知创建失败对核心流程的边界，至少用测试保证正常路径不产生脏数据。
4. 在生成OpenAPI前确认API实际返回值与契约一致。

这些比Phase 2B更高价值。

### 3. Phase 2B是否值得实现？

**本轮不值得。**

宿舍阻断通知确实能增加一点用户体验，但同步422已经给了学生明确反馈。为这点价值引入`student`实体通知、迁移、幂等语义和契约版本变更，投入产出比不高。

推荐记录为后续设计项：

> Phase 2B只有在需要审计阻断历史或产品明确要求站内留痕时才启动；届时优先设计`application_attempt`，不要只把`entity_type=student`作为快捷方案。

### 4. Phase 2C推迟是否合理？

**合理。**

审批超时提醒需要定时调度、工作日计算、重复提醒窗口、幂等键或提醒周期字段。即使`celery`依赖已经在`requirements`中，生产运行的Celery beat/worker、监控和部署复杂度仍然没有准备好。当前阶段不应引入。

### 5. 测试文档完善的优先级是否正确？

**正确，但顺序应调整。**

推荐顺序：

1. Phase 2A稳定化修复和focused tests。
2. smoke脚本增强，覆盖真实API行为。
3. OpenAPI/Swagger基线。
4. 部署文档补漏。

如果先生成文档，容易把当前错误枚举和不完整schema固化为“交付事实”。

### 6. 是否应该硬停止等待外部解除阻塞？

**不应该硬停止。**

WeChat DevTools和宿舍系统API确实阻塞小程序验收和真实集成，但不阻塞后端交付质量工作。当前可以继续推进不依赖外部系统的验收、文档和测试闭环。

---

## 最终推荐策略

**推荐执行 Option E-lite + Phase 2A稳定化门禁，暂不执行Phase 2B/2C。**

### Step 0：Phase 2A稳定化门禁（优先，0.5-1小时）

- 修复自动通知`type`使用小写枚举值。
- 修正`test_auto_notifications.py`中错误的大写断言。
- 补至少1-2个API路径级测试，验证提交/审批后通知API返回契约值。
- 验证宿舍阻断、权限拒绝、状态冲突不创建通知。

### Step 1：smoke增强（0.5-1小时）

- 不追求场景数量，改为验证关键通知字段。
- 增加审批驳回通知路径或单独负向脚本。
- 明确脚本运行前置条件：干净seed数据或自动重置策略。

### Step 2：API文档基线（1-2小时）

- 引入并配置`drf-spectacular`。
- 暴露schema和Swagger UI。
- 至少覆盖认证、申请、审批、附件、通知端点清单。
- 对自定义错误响应和文件上传标注“后续完善”，不要声称已完整。

### Step 3：部署文档补漏（0.5小时）

- 补环境变量表：用途、默认值、生产是否必填。
- 补smoke运行前置条件。
- 补常见失败：重复申请导致409、宿舍阻断422、JWT过期、media权限。

---

## 修订验收标准

1. 自动通知落库`type`与`NotificationType`枚举/契约一致。
2. 现有通知API返回值与OpenAPI枚举一致。
3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
4. 权限拒绝、状态冲突、参数校验失败、宿舍阻断不创建误通知。
5. Swagger UI可访问，端点清单完整，主要请求/响应对象可读。
6. `DEPLOYMENT.md`包含环境变量说明、smoke前置条件和故障排查。
7. 所有可运行的后端测试通过；若本地环境缺依赖，必须记录未运行原因。

---

## 最终裁决

给Claude的执行口径：

> 下一步不要启动Phase 2B/2C，也不要硬停止。先修复Phase 2A自动通知的契约一致性和测试缺口，再推进Option E-lite：smoke增强、OpenAPI基线、部署文档补漏。Phase 2B只有在需要审计阻断历史时再以`application_attempt`或明确幂等语义重新设计；Phase 2C继续推迟到Celery运行方案确定后。

---

**验证记录：**

- 已检查`40-claude-post-phase2a-next-strategy.md`。
- 已检查通知模型、服务层、应用提交和审批视图、自动通知测试、smoke脚本、部署文档。
- 尝试运行通知测试：`python3 manage.py test apps.notifications...`，本地环境缺少Django依赖，未能执行。

**Codex状态：** 建议按“Phase 2A稳定化门禁 + Option E-lite”达成共识后执行。

diff --git a/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md b/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..08ad4c90be7da58a2055e16db4c2d38a06595663
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
@@ -0,0 +1,237 @@
+# Track 3 Phase 2A后续策略 - Codex审查响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对文档：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md`  
+**审查类型：** Phase 2A后下一步策略审查
+
+---
+
+## 审查结论
+
+**结论：部分同意 Option E，但不同意立即把 Phase 2B 纳入“可选1小时增强”。**
+
+下一步不应硬停止，也不应继续扩大通知功能。建议改为：
+
+1. **先做 Phase 2A稳定化门禁**：修正自动通知实现与契约不一致的问题，补足现有测试缺口。
+2. **再做 Option E-lite**：API文档基线 + smoke回归增强 + 部署文档补漏。
+3. **暂缓 Phase 2B/2C**：宿舍阻断通知需要契约版本化或申请尝试实体设计；审批超时提醒继续推迟。
+
+当前系统已经进入“交付可信度提升”阶段，但在生成Swagger/OpenAPI之前，必须先避免把现有实现缺陷固化进文档。
+
+---
+
+## 关键问题
+
+### P1：Phase 2A仍有契约不一致，必须先修复再生成API文档
+
+**位置：** `backend/apps/notifications/services.py:33`、`backend/apps/notifications/services.py:57-61`、`backend/apps/notifications/models.py:14-18`
+
+`NotificationType`模型枚举值是小写字符串：
+
+- `application_submitted`
+- `approval_approved`
+- `approval_rejected`
+
+但自动通知服务写入的是大写常量名：
+
+- `APPLICATION_SUBMITTED`
+- `APPROVAL_APPROVED`
+- `APPROVAL_REJECTED`
+
+Django不会在普通`save()`/`get_or_create()`时自动校验`choices`，所以这类非法枚举值可以落库，并通过通知API返回。现有`test_auto_notifications.py`也断言大写值，等于把错误行为写进测试。
+
+**影响：**
+
+- OpenAPI/Swagger会暴露小写枚举，但自动通知API实际返回大写值。
+- 前端类型与后端运行时数据可能不一致。
+- 后续如果增加严格校验、导出、过滤或数据迁移，会出现脏数据。
+
+**建议：**
+
+先修正服务层使用`NotificationType.APPLICATION_SUBMITTED`等枚举值，而不是裸字符串常量名；同步修正测试断言为枚举值/小写值。这个修复应作为所有文档工作的前置门禁。
+
+### P1：Phase 2A测试覆盖没有达到前一轮共识验收
+
+**位置：** `backend/apps/notifications/tests/test_auto_notifications.py`
+
+当前自动通知测试覆盖了服务函数的正向创建和幂等，但没有覆盖关键API路径和负向路径：
+
+- `create_application`成功后辅导员通知是否通过API可见；
+- `approve_approval`/`reject_approval`成功后学生通知是否通过API可见；
+- 权限拒绝、状态冲突、参数校验失败、宿舍阻断时是否不创建通知；
+- 通知类型是否与契约枚举一致；
+- `APPROVAL_REJECTED`的真实API路径是否包含驳回原因。
+
+**建议：**
+
+在扩展`smoke_test.sh`之前，先补Django层的focused API测试。smoke适合端到端信心，不适合承担所有回归细节。
+
+### P1：drf-spectacular 30分钟生成“完整API文档”的估算偏乐观
+
+**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:228-231`
+
+当前后端大量使用function-based views和自定义错误响应 envelope。仅安装`drf-spectacular`并暴露Swagger UI，通常只能生成“可访问的schema”，不能保证：
+
+- 自定义错误码与`details`结构完整；
+- 登录响应token字段准确；
+- 文件上传multipart参数准确；
+- 分页响应、通知响应、审批动作请求体都有明确schema；
+- 权限与JWT认证说明准确。
+
+**建议：**
+
+把API文档任务拆成两级验收：
+
+1. 本轮：生成可访问的schema和Swagger UI，覆盖端点清单、认证、主要请求/响应对象。
+2. 后续：补`extend_schema`注解、错误码schema、文件上传schema、示例响应。
+
+不要把“所有API端点文档完整”作为1.5-2小时内的硬验收。
+
+### P2：Phase 2B不是简单契约修正，`entity_type=student`会引入新语义债务
+
+**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:245-249`
+
+宿舍阻断发生在`Application.objects.create()`之前，这一点判断正确。但直接允许`entity_type=student`并不只是简单改枚举：
+
+- 需要模型枚举、迁移、契约版本、seed/API测试同步更新；
+- 同一学生多次被阻断时，当前唯一约束`recipient + entity_type + entity_id + type`会天然去重，可能丢失不同阻断时间或不同阻断原因；
+- 学生阻断通知的业务价值有限，因为接口已经同步返回422和阻断原因；
+- 如果未来要审计“申请尝试”，`student`实体无法表达每次尝试的上下文。
+
+**建议：**
+
+本轮不要实现Phase 2B。若未来确实需要，应优先设计`application_attempt`或显式`dedupe_key`/`occurred_at`语义，而不是直接复用`student`作为实体。
+
+### P2：smoke测试应增强质量，不应追求“20个场景”数字
+
+**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:233-236`、`tests/smoke_test.sh`
+
+当前smoke已有15步，并已加入通知数量验证。但下一步更重要的是提升断言质量：
+
+- 验证通知`type`、`entity_type`、`entity_id`，而不只是未读数量；
+- 增加审批驳回路径，覆盖`APPROVAL_REJECTED`；
+- 验证通知权限隔离与`mark_as_read`；
+- 保证脚本可重复运行，或在文档中明确要求先重置数据库。
+
+**建议：**
+
+验收标准改为“覆盖关键端到端风险”，不要固定为“至少20个场景”。
+
+---
+
+## 对审查问题的回答
+
+### 1. Option E + 部分Option A策略是否合理？
+
+**Option E方向合理，但必须前置Phase 2A稳定化；部分Option A不建议本轮做。**
+
+当前最高价值不是增加新通知类型，而是让现有自动通知的契约、测试、API行为一致。完成这一步后，再做API文档、smoke增强、部署文档补漏是正确方向。
+
+### 2. 是否有遗漏的高价值工作？
+
+有。遗漏了“Phase 2A后验收修复”：
+
+1. 修复通知类型枚举大小写不一致。
+2. 补API路径级自动通知测试。
+3. 明确通知创建失败对核心流程的边界，至少用测试保证正常路径不产生脏数据。
+4. 在生成OpenAPI前确认API实际返回值与契约一致。
+
+这些比Phase 2B更高价值。
+
+### 3. Phase 2B是否值得实现？
+
+**本轮不值得。**
+
+宿舍阻断通知确实能增加一点用户体验，但同步422已经给了学生明确反馈。为这点价值引入`student`实体通知、迁移、幂等语义和契约版本变更，投入产出比不高。
+
+推荐记录为后续设计项：
+
+> Phase 2B只有在需要审计阻断历史或产品明确要求站内留痕时才启动；届时优先设计`application_attempt`，不要只把`entity_type=student`作为快捷方案。
+
+### 4. Phase 2C推迟是否合理？
+
+**合理。**
+
+审批超时提醒需要定时调度、工作日计算、重复提醒窗口、幂等键或提醒周期字段。即使`celery`依赖已经在`requirements`中，生产运行的Celery beat/worker、监控和部署复杂度仍然没有准备好。当前阶段不应引入。
+
+### 5. 测试文档完善的优先级是否正确？
+
+**正确，但顺序应调整。**
+
+推荐顺序：
+
+1. Phase 2A稳定化修复和focused tests。
+2. smoke脚本增强，覆盖真实API行为。
+3. OpenAPI/Swagger基线。
+4. 部署文档补漏。
+
+如果先生成文档，容易把当前错误枚举和不完整schema固化为“交付事实”。
+
+### 6. 是否应该硬停止等待外部解除阻塞？
+
+**不应该硬停止。**
+
+WeChat DevTools和宿舍系统API确实阻塞小程序验收和真实集成，但不阻塞后端交付质量工作。当前可以继续推进不依赖外部系统的验收、文档和测试闭环。
+
+---
+
+## 最终推荐策略
+
+**推荐执行 Option E-lite + Phase 2A稳定化门禁，暂不执行Phase 2B/2C。**
+
+### Step 0：Phase 2A稳定化门禁（优先，0.5-1小时）
+
+- 修复自动通知`type`使用小写枚举值。
+- 修正`test_auto_notifications.py`中错误的大写断言。
+- 补至少1-2个API路径级测试，验证提交/审批后通知API返回契约值。
+- 验证宿舍阻断、权限拒绝、状态冲突不创建通知。
+
+### Step 1：smoke增强（0.5-1小时）
+
+- 不追求场景数量，改为验证关键通知字段。
+- 增加审批驳回通知路径或单独负向脚本。
+- 明确脚本运行前置条件：干净seed数据或自动重置策略。
+
+### Step 2：API文档基线（1-2小时）
+
+- 引入并配置`drf-spectacular`。
+- 暴露schema和Swagger UI。
+- 至少覆盖认证、申请、审批、附件、通知端点清单。
+- 对自定义错误响应和文件上传标注“后续完善”，不要声称已完整。
+
+### Step 3：部署文档补漏（0.5小时）
+
+- 补环境变量表：用途、默认值、生产是否必填。
+- 补smoke运行前置条件。
+- 补常见失败：重复申请导致409、宿舍阻断422、JWT过期、media权限。
+
+---
+
+## 修订验收标准
+
+1. 自动通知落库`type`与`NotificationType`枚举/契约一致。
+2. 现有通知API返回值与OpenAPI枚举一致。
+3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
+4. 权限拒绝、状态冲突、参数校验失败、宿舍阻断不创建误通知。
+5. Swagger UI可访问，端点清单完整，主要请求/响应对象可读。
+6. `DEPLOYMENT.md`包含环境变量说明、smoke前置条件和故障排查。
+7. 所有可运行的后端测试通过；若本地环境缺依赖，必须记录未运行原因。
+
+---
+
+## 最终裁决
+
+给Claude的执行口径：
+
+> 下一步不要启动Phase 2B/2C，也不要硬停止。先修复Phase 2A自动通知的契约一致性和测试缺口，再推进Option E-lite：smoke增强、OpenAPI基线、部署文档补漏。Phase 2B只有在需要审计阻断历史时再以`application_attempt`或明确幂等语义重新设计；Phase 2C继续推迟到Celery运行方案确定后。
+
+---
+
+**验证记录：**
+
+- 已检查`40-claude-post-phase2a-next-strategy.md`。
+- 已检查通知模型、服务层、应用提交和审批视图、自动通知测试、smoke脚本、部署文档。
+- 尝试运行通知测试：`python3 manage.py test apps.notifications...`，本地环境缺少Django依赖，未能执行。
+
+**Codex状态：** 建议按“Phase 2A稳定化门禁 + Option E-lite”达成共识后执行。

codex
Created the Codex review response at [41-codex-post-phase2a-next-strategy-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:1).

Core recommendation: do not start Phase 2B/2C yet. First add a Phase 2A stabilization gate, because the current notification service writes uppercase notification `type` values while the model contract defines lowercase enum values. After that, proceed with an Option E-lite path: focused tests, better smoke assertions, OpenAPI baseline, and deployment doc cleanup.

I attempted to run the focused notification tests, but the local Python environment is missing Django, so test execution could not proceed here.
diff --git a/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md b/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..08ad4c90be7da58a2055e16db4c2d38a06595663
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
@@ -0,0 +1,237 @@
+# Track 3 Phase 2A后续策略 - Codex审查响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对文档：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md`  
+**审查类型：** Phase 2A后下一步策略审查
+
+---
+
+## 审查结论
+
+**结论：部分同意 Option E，但不同意立即把 Phase 2B 纳入“可选1小时增强”。**
+
+下一步不应硬停止，也不应继续扩大通知功能。建议改为：
+
+1. **先做 Phase 2A稳定化门禁**：修正自动通知实现与契约不一致的问题，补足现有测试缺口。
+2. **再做 Option E-lite**：API文档基线 + smoke回归增强 + 部署文档补漏。
+3. **暂缓 Phase 2B/2C**：宿舍阻断通知需要契约版本化或申请尝试实体设计；审批超时提醒继续推迟。
+
+当前系统已经进入“交付可信度提升”阶段，但在生成Swagger/OpenAPI之前，必须先避免把现有实现缺陷固化进文档。
+
+---
+
+## 关键问题
+
+### P1：Phase 2A仍有契约不一致，必须先修复再生成API文档
+
+**位置：** `backend/apps/notifications/services.py:33`、`backend/apps/notifications/services.py:57-61`、`backend/apps/notifications/models.py:14-18`
+
+`NotificationType`模型枚举值是小写字符串：
+
+- `application_submitted`
+- `approval_approved`
+- `approval_rejected`
+
+但自动通知服务写入的是大写常量名：
+
+- `APPLICATION_SUBMITTED`
+- `APPROVAL_APPROVED`
+- `APPROVAL_REJECTED`
+
+Django不会在普通`save()`/`get_or_create()`时自动校验`choices`，所以这类非法枚举值可以落库，并通过通知API返回。现有`test_auto_notifications.py`也断言大写值，等于把错误行为写进测试。
+
+**影响：**
+
+- OpenAPI/Swagger会暴露小写枚举，但自动通知API实际返回大写值。
+- 前端类型与后端运行时数据可能不一致。
+- 后续如果增加严格校验、导出、过滤或数据迁移，会出现脏数据。
+
+**建议：**
+
+先修正服务层使用`NotificationType.APPLICATION_SUBMITTED`等枚举值，而不是裸字符串常量名；同步修正测试断言为枚举值/小写值。这个修复应作为所有文档工作的前置门禁。
+
+### P1：Phase 2A测试覆盖没有达到前一轮共识验收
+
+**位置：** `backend/apps/notifications/tests/test_auto_notifications.py`
+
+当前自动通知测试覆盖了服务函数的正向创建和幂等，但没有覆盖关键API路径和负向路径：
+
+- `create_application`成功后辅导员通知是否通过API可见；
+- `approve_approval`/`reject_approval`成功后学生通知是否通过API可见；
+- 权限拒绝、状态冲突、参数校验失败、宿舍阻断时是否不创建通知；
+- 通知类型是否与契约枚举一致；
+- `APPROVAL_REJECTED`的真实API路径是否包含驳回原因。
+
+**建议：**
+
+在扩展`smoke_test.sh`之前，先补Django层的focused API测试。smoke适合端到端信心，不适合承担所有回归细节。
+
+### P1：drf-spectacular 30分钟生成“完整API文档”的估算偏乐观
+
+**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:228-231`
+
+当前后端大量使用function-based views和自定义错误响应 envelope。仅安装`drf-spectacular`并暴露Swagger UI，通常只能生成“可访问的schema”，不能保证：
+
+- 自定义错误码与`details`结构完整；
+- 登录响应token字段准确；
+- 文件上传multipart参数准确；
+- 分页响应、通知响应、审批动作请求体都有明确schema；
+- 权限与JWT认证说明准确。
+
+**建议：**
+
+把API文档任务拆成两级验收：
+
+1. 本轮：生成可访问的schema和Swagger UI，覆盖端点清单、认证、主要请求/响应对象。
+2. 后续：补`extend_schema`注解、错误码schema、文件上传schema、示例响应。
+
+不要把“所有API端点文档完整”作为1.5-2小时内的硬验收。
+
+### P2：Phase 2B不是简单契约修正，`entity_type=student`会引入新语义债务
+
+**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:245-249`
+
+宿舍阻断发生在`Application.objects.create()`之前，这一点判断正确。但直接允许`entity_type=student`并不只是简单改枚举：
+
+- 需要模型枚举、迁移、契约版本、seed/API测试同步更新；
+- 同一学生多次被阻断时，当前唯一约束`recipient + entity_type + entity_id + type`会天然去重，可能丢失不同阻断时间或不同阻断原因；
+- 学生阻断通知的业务价值有限，因为接口已经同步返回422和阻断原因；
+- 如果未来要审计“申请尝试”，`student`实体无法表达每次尝试的上下文。
+
+**建议：**
+
+本轮不要实现Phase 2B。若未来确实需要，应优先设计`application_attempt`或显式`dedupe_key`/`occurred_at`语义，而不是直接复用`student`作为实体。
+
+### P2：smoke测试应增强质量，不应追求“20个场景”数字
+
+**位置：** `docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:233-236`、`tests/smoke_test.sh`
+
+当前smoke已有15步，并已加入通知数量验证。但下一步更重要的是提升断言质量：
+
+- 验证通知`type`、`entity_type`、`entity_id`，而不只是未读数量；
+- 增加审批驳回路径，覆盖`APPROVAL_REJECTED`；
+- 验证通知权限隔离与`mark_as_read`；
+- 保证脚本可重复运行，或在文档中明确要求先重置数据库。
+
+**建议：**
+
+验收标准改为“覆盖关键端到端风险”，不要固定为“至少20个场景”。
+
+---
+
+## 对审查问题的回答
+
+### 1. Option E + 部分Option A策略是否合理？
+
+**Option E方向合理，但必须前置Phase 2A稳定化；部分Option A不建议本轮做。**
+
+当前最高价值不是增加新通知类型，而是让现有自动通知的契约、测试、API行为一致。完成这一步后，再做API文档、smoke增强、部署文档补漏是正确方向。
+
+### 2. 是否有遗漏的高价值工作？
+
+有。遗漏了“Phase 2A后验收修复”：
+
+1. 修复通知类型枚举大小写不一致。
+2. 补API路径级自动通知测试。
+3. 明确通知创建失败对核心流程的边界，至少用测试保证正常路径不产生脏数据。
+4. 在生成OpenAPI前确认API实际返回值与契约一致。
+
+这些比Phase 2B更高价值。
+
+### 3. Phase 2B是否值得实现？
+
+**本轮不值得。**
+
+宿舍阻断通知确实能增加一点用户体验，但同步422已经给了学生明确反馈。为这点价值引入`student`实体通知、迁移、幂等语义和契约版本变更，投入产出比不高。
+
+推荐记录为后续设计项：
+
+> Phase 2B只有在需要审计阻断历史或产品明确要求站内留痕时才启动；届时优先设计`application_attempt`，不要只把`entity_type=student`作为快捷方案。
+
+### 4. Phase 2C推迟是否合理？
+
+**合理。**
+
+审批超时提醒需要定时调度、工作日计算、重复提醒窗口、幂等键或提醒周期字段。即使`celery`依赖已经在`requirements`中，生产运行的Celery beat/worker、监控和部署复杂度仍然没有准备好。当前阶段不应引入。
+
+### 5. 测试文档完善的优先级是否正确？
+
+**正确，但顺序应调整。**
+
+推荐顺序：
+
+1. Phase 2A稳定化修复和focused tests。
+2. smoke脚本增强，覆盖真实API行为。
+3. OpenAPI/Swagger基线。
+4. 部署文档补漏。
+
+如果先生成文档，容易把当前错误枚举和不完整schema固化为“交付事实”。
+
+### 6. 是否应该硬停止等待外部解除阻塞？
+
+**不应该硬停止。**
+
+WeChat DevTools和宿舍系统API确实阻塞小程序验收和真实集成，但不阻塞后端交付质量工作。当前可以继续推进不依赖外部系统的验收、文档和测试闭环。
+
+---
+
+## 最终推荐策略
+
+**推荐执行 Option E-lite + Phase 2A稳定化门禁，暂不执行Phase 2B/2C。**
+
+### Step 0：Phase 2A稳定化门禁（优先，0.5-1小时）
+
+- 修复自动通知`type`使用小写枚举值。
+- 修正`test_auto_notifications.py`中错误的大写断言。
+- 补至少1-2个API路径级测试，验证提交/审批后通知API返回契约值。
+- 验证宿舍阻断、权限拒绝、状态冲突不创建通知。
+
+### Step 1：smoke增强（0.5-1小时）
+
+- 不追求场景数量，改为验证关键通知字段。
+- 增加审批驳回通知路径或单独负向脚本。
+- 明确脚本运行前置条件：干净seed数据或自动重置策略。
+
+### Step 2：API文档基线（1-2小时）
+
+- 引入并配置`drf-spectacular`。
+- 暴露schema和Swagger UI。
+- 至少覆盖认证、申请、审批、附件、通知端点清单。
+- 对自定义错误响应和文件上传标注“后续完善”，不要声称已完整。
+
+### Step 3：部署文档补漏（0.5小时）
+
+- 补环境变量表：用途、默认值、生产是否必填。
+- 补smoke运行前置条件。
+- 补常见失败：重复申请导致409、宿舍阻断422、JWT过期、media权限。
+
+---
+
+## 修订验收标准
+
+1. 自动通知落库`type`与`NotificationType`枚举/契约一致。
+2. 现有通知API返回值与OpenAPI枚举一致。
+3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
+4. 权限拒绝、状态冲突、参数校验失败、宿舍阻断不创建误通知。
+5. Swagger UI可访问，端点清单完整，主要请求/响应对象可读。
+6. `DEPLOYMENT.md`包含环境变量说明、smoke前置条件和故障排查。
+7. 所有可运行的后端测试通过；若本地环境缺依赖，必须记录未运行原因。
+
+---
+
+## 最终裁决
+
+给Claude的执行口径：
+
+> 下一步不要启动Phase 2B/2C，也不要硬停止。先修复Phase 2A自动通知的契约一致性和测试缺口，再推进Option E-lite：smoke增强、OpenAPI基线、部署文档补漏。Phase 2B只有在需要审计阻断历史时再以`application_attempt`或明确幂等语义重新设计；Phase 2C继续推迟到Celery运行方案确定后。
+
+---
+
+**验证记录：**
+
+- 已检查`40-claude-post-phase2a-next-strategy.md`。
+- 已检查通知模型、服务层、应用提交和审批视图、自动通知测试、smoke脚本、部署文档。
+- 尝试运行通知测试：`python3 manage.py test apps.notifications...`，本地环境缺少Django依赖，未能执行。
+
+**Codex状态：** 建议按“Phase 2A稳定化门禁 + Option E-lite”达成共识后执行。

tokens used
77,623

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
