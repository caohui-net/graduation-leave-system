# Discussion Context

**Task:** DISCUSS-宿管员审批流程变更-从单一审批改为楼栋内任意宿管员可审批-业务需求变更-1780773777
**Round:** 2

## Topic

宿管员审批流程变更：从单一审批改为楼栋内任意宿管员可审批

**业务需求变更：**
当前流程：学生提交申请 → 匹配1个宿管员（按building） → 该宿管员审批 → 进入辅导员审批

新需求：学生提交申请 → 匹配所有符合building的宿管员 → 任意1个宿管员审批即可 → 其他宿管员看到已审批提示无需重复 → 进入辅导员审批

**技术上下文：**
- 当前Approval模型：approver字段ForeignKey(User), NOT NULL
- 当前创建逻辑：applications/views.py Lines 147-176，只创建1个宿管员审批
- 当前审批逻辑：approvals/views.py Lines 150-195

**待讨论方案：**
方案A：修改模型允许approver=null，运行时动态绑定第一个审批人
方案B：为每个符合building的宿管员创建审批记录，第一个审批后其他自动完成
方案C：添加approved_by字段区分分配人和实际审批人

**讨论重点：**
1. 哪个方案最符合业务语义（任意宿管员可审批）
2. 数据一致性和并发处理（多个宿管员同时审批）
3. 对现有代码和数据的影响（是否需要迁移）
4. 性能影响（创建N个审批记录 vs 1个记录）
5. 列表展示逻辑（如何区分待审批和已由他人完成）

**期望输出：**
- 推荐方案及理由
- 需要修改的文件和关键逻辑
- 潜在风险和缓解措施

## Previous Discussion

[Earlier: 2 discussion events]

[claude]: Round 1 ended
[claude]: Round 2 started

## Referenced Artifacts

- .omc/collaboration/artifacts/DISCUSS-宿管员审批流程变更-从单一审批改为楼栋内任意宿管员可审批-业务需求变更-1780773777-discuss-r1-codex-20260606-192437.md

