# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-07T11:48:29.324Z

## Original task

请分析demo-web/index.html的UI实现与实际业务流程的差异。

业务流程（参考docs/design/2026-05-27-system-design.md和backend实现）：
1. 学生提交申请（contact_phone, reason, leave_date, 可上传附件）
2. 宿管员审批（第一级，approve/reject）
3. 辅导员审批（第二级，approve/reject）
4. 最终状态：approved/rejected

当前demo-web目录：/home/caohui/projects/graduation-leave-system/demo-web/
后端API：http://localhost:8001

请检查：
1. demo-web是否正确展示完整审批流程（2级审批）
2. 表单字段是否与API匹配（contact_phone必填）
3. 状态展示是否准确（pending_dorm_manager, pending_counselor, approved, rejected）
4. 用户角色切换是否支持（学生、宿管员、辅导员视图）
5. 附件上传功能是否完整

输出：
1. 当前UI与业务流程的具体差异列表
2. 需要修改的UI组件清单
3. 优先级排序的修改建议

## Final prompt

请分析demo-web/index.html的UI实现与实际业务流程的差异。

业务流程（参考docs/design/2026-05-27-system-design.md和backend实现）：
1. 学生提交申请（contact_phone, reason, leave_date, 可上传附件）
2. 宿管员审批（第一级，approve/reject）
3. 辅导员审批（第二级，approve/reject）
4. 最终状态：approved/rejected

当前demo-web目录：/home/caohui/projects/graduation-leave-system/demo-web/
后端API：http://localhost:8001

请检查：
1. demo-web是否正确展示完整审批流程（2级审批）
2. 表单字段是否与API匹配（contact_phone必填）
3. 状态展示是否准确（pending_dorm_manager, pending_counselor, approved, rejected）
4. 用户角色切换是否支持（学生、宿管员、辅导员视图）
5. 附件上传功能是否完整

输出：
1. 当前UI与业务流程的具体差异列表
2. 需要修改的UI组件清单
3. 优先级排序的修改建议

## Raw output

```text
**结论**

`demo-web/index.html` 目前更像静态 UI 草图，不是按后端真实流程运行的 demo。它没有接入 `http://localhost:8001`，也没有完整表达“学生提交 -> 宿管员审批 -> 辅导员审批 -> approved/rejected”的两级审批链路。

**1. 当前 UI 与业务流程差异**

1. 审批流程展示不完整  
   后端真实状态是 `pending_dorm_manager -> pending_counselor -> approved/rejected`，见 [models.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/models.py:6)。宿管通过后进入辅导员审批，辅导员通过后最终 `approved`，见 [views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:179)。  
   当前详情时间轴只显示“宿管员审批 + 提交申请”，没有辅导员审批节点，也没有最终状态节点，见 [index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:267)。

2. 表单字段与 API 不匹配  
   后端提交申请必填 `contact_phone`、`leave_date`，`reason` 可选，见 [serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/serializers.py:35)。  
   当前 UI 只有“离校原因”和“离校日期”，缺少必填联系电话 `contact_phone`，见 [index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:150)。

3. 状态展示不准确  
   当前 UI 只用“待审批 / 已通过 / 已完成”等文案，没有映射 `pending_dorm_manager`、`pending_counselor`、`approved`、`rejected`，也没有区分“待宿管员审批”和“待辅导员审批”。列表里甚至静态展示“辅导员审批 + 已通过”，但不表示申请最终状态，见 [index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:214)。

4. 角色切换不完整  
   后端角色包含 `student`、`dorm_manager`、`counselor`、`dean`、`admin`，见 [models.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/models.py:5)。  
   当前选择器只有宿管员、辅导员、学工部，没有学生角色；“学生申请”页始终可见，角色切换只改标题和是否隐藏审批按钮，不会切换数据源、权限视图或待办步骤，见 [index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:123)。

5. 审批操作未接 API  
   后端审批接口按 `approval_id` 操作：`POST /api/approvals/{approval_id}/approve/` 和 `/reject/`，见 [urls.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/urls.py:4)。请求字段是 `comment`，见 [serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/serializers.py:30)。  
   当前“通过 / 拒绝”按钮没有事件处理，也没有使用 `approval_id` 或提交 `comment`，见 [index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:294)。

6. 附件上传不完整  
   后端附件上传需要 `POST /api/applications/{application_id}/attachments/`，multipart 字段为 `file` 和 `attachment_type`，见 [views.py](/home/caohui/projects/graduation-leave-system/backend/apps/attachments/views.py:56)。  
   当前 UI 只是本地维护 `uploadedFiles`，没有创建草稿、没有拿 `application_id`、没有上传到后端、没有选择 `attachment_type`、没有下载/删除已上传附件列表，见 [index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:337)。

7. 附件类型命名需以后端为准  
   设计文档里有 `dorm_clearance`，但后端当前枚举是 `dorm_checkout`、`library_clearance`、`finance_clearance`、`other`，见 [models.py](/home/caohui/projects/graduation-leave-system/backend/apps/attachments/models.py:6)。UI 如果接后端，应使用后端枚举。

**2. 需要修改的 UI 组件清单**

- 角色选择器：增加 `student`，并按角色控制可见页面和操作权限。
- 学生申请表单：增加 `contact_phone` 必填字段，绑定 `reason`、`leave_date`，提交到 `/api/applications/`。
- 附件上传组件：支持先创建/获取草稿 `/api/applications/draft/`，选择 `attachment_type`，调用上传、列表、下载、删除接口。
- 审批列表：从 `/api/approvals/?decision=pending|approved|rejected|all` 拉取数据，按宿管员/辅导员展示对应 `step`。
- 申请详情：展示 `contact_phone`、`status`、`dorm_checkout_status`、审批记录、附件列表。
- 审批时间轴：按状态动态展示“提交申请、宿管员审批、辅导员审批、最终结果”。
- 审批操作区：只有当前角色匹配待审批 `step` 且 `decision=pending` 时显示；提交 `comment` 到 approve/reject 接口。
- 状态标签组件：建立状态映射：`pending_dorm_manager=待宿管员审批`、`pending_counselor=待辅导员审批`、`approved=已通过`、`rejected=已驳回`。

**3. 优先级修改建议**

P0：先修正流程和字段  
增加 `contact_phone`，接入申请提交 API；修正状态映射；详情页补齐两级审批时间轴。

P1：接入审批视图  
宿管员和辅导员分别读取 `/api/approvals/`，用 `approval_id` 执行 approve/reject，审批意见字段改为 `comment`。

P2：补完整附件能力  
增加 `attachment_type` 选择，支持草稿申请、真实上传、列表展示、下载和删除。

P3：整理角色体验  
学生只看申请/我的申请，宿管员只看宿管审批，辅导员只看辅导员审批，学工部只做 approved 备案查询；避免所有角色共用同一套静态页面。


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019ea1e7-9487-7a23-b6e4-b924de6ea20e
--------
user
请分析demo-web/index.html的UI实现与实际业务流程的差异。

业务流程（参考docs/design/2026-05-27-system-design.md和backend实现）：
1. 学生提交申请（contact_phone, reason, leave_date, 可上传附件）
2. 宿管员审批（第一级，approve/reject）
3. 辅导员审批（第二级，approve/reject）
4. 最终状态：approved/rejected

当前demo-web目录：/home/caohui/projects/graduation-leave-system/demo-web/
后端API：http://localhost:8001

请检查：
1. demo-web是否正确展示完整审批流程（2级审批）
2. 表单字段是否与API匹配（contact_phone必填）
3. 状态展示是否准确（pending_dorm_manager, pending_counselor, approved, rejected）
4. 用户角色切换是否支持（学生、宿管员、辅导员视图）
5. 附件上传功能是否完整

输出：
1. 当前UI与业务流程的具体差异列表
2. 需要修改的UI组件清单
3. 优先级排序的修改建议
codex
我会先读取项目的执行规则，然后对照设计文档、后端接口实现和 `demo-web/index.html`，把 UI 与真实流程的偏差整理出来。
exec
/bin/bash -lc "sed -n '1,220p' /home/caohui/.codex/RTK.md" in /home/caohui/projects/graduation-leave-system
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

codex
项目规则要求 shell 命令经 `rtk` 运行；另外这类对照检查接近 API/UI 审查，我会读取项目的 Codex review 协议，避免漏掉本地要求。
exec
/bin/bash -lc "rtk sed -n '1,240p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system
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

exec
/bin/bash -lc 'rtk rg -n "pending_dorm_manager|pending_counselor|contact_phone|attachment|leave_date|approve|reject|dorm" docs/design/2026-05-27-system-design.md backend demo-web/index.html' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
demo-web/index.html:124:      <option value="dorm_manager">宿管员</option>
demo-web/index.html:217:          <span class="tag tag-approved">已通过</span>
demo-web/index.html:281:            <span class="tag tag-approved">已完成</span>
demo-web/index.html:303:    let currentRole = 'dorm_manager';
demo-web/index.html:317:        'dorm_manager': '宿管员',
docs/design/2026-05-27-system-design.md:157:│   ├── attachments/       # 附件管理模块
docs/design/2026-05-27-system-design.md:168:│       ├── dorm_system.py # 宿舍系统对接
docs/design/2026-05-27-system-design.md:207:4. **attachments（附件管理）**
docs/design/2026-05-27-system-design.md:249:4. attachments - 附件表
docs/design/2026-05-27-system-design.md:316:    planned_leave_date DATE NOT NULL COMMENT '计划离校日期',
docs/design/2026-05-27-system-design.md:318:    current_approver_id BIGINT COMMENT '当前审批人ID',
docs/design/2026-05-27-system-design.md:321:    reject_reason TEXT COMMENT '驳回原因',
docs/design/2026-05-27-system-design.md:338:    FOREIGN KEY (current_approver_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:345:    INDEX idx_planned_leave_date (planned_leave_date),
docs/design/2026-05-27-system-design.md:346:    INDEX idx_approver_status (current_approver_id, status, submit_time),
docs/design/2026-05-27-system-design.md:354:- `pending_counselor` - 待辅导员审核
docs/design/2026-05-27-system-design.md:356:- `approved` - 审批通过
docs/design/2026-05-27-system-design.md:357:- `rejected` - 已驳回
docs/design/2026-05-27-system-design.md:368:    approver_id BIGINT NOT NULL COMMENT '审批人ID',
docs/design/2026-05-27-system-design.md:369:    approver_role VARCHAR(20) NOT NULL COMMENT '审批人角色',
docs/design/2026-05-27-system-design.md:370:    action VARCHAR(20) NOT NULL COMMENT '操作: approve/reject',
docs/design/2026-05-27-system-design.md:378:    FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:380:    INDEX idx_approver_id (approver_id),
docs/design/2026-05-27-system-design.md:387:- `approver_role`: counselor（辅导员）、admin（学工部）
docs/design/2026-05-27-system-design.md:388:- `action`: approve（同意）、reject（驳回）
docs/design/2026-05-27-system-design.md:392:### 2.5 附件表（attachments）
docs/design/2026-05-27-system-design.md:395:CREATE TABLE attachments (
docs/design/2026-05-27-system-design.md:403:    attachment_type VARCHAR(50) NOT NULL COMMENT '附件类型',
docs/design/2026-05-27-system-design.md:409:    INDEX idx_attachment_type (attachment_type),
docs/design/2026-05-27-system-design.md:411:    INDEX idx_app_type (application_id, attachment_type, is_deleted)
docs/design/2026-05-27-system-design.md:415:**附件类型（attachment_type）：**
docs/design/2026-05-27-system-design.md:416:- `dorm_clearance` - 宿舍清退证明
docs/design/2026-05-27-system-design.md:456:- `application_approved` - 申请通过
docs/design/2026-05-27-system-design.md:457:- `application_rejected` - 申请驳回
docs/design/2026-05-27-system-design.md:496:- `dorm_integration_type` - 宿舍系统集成类型（api/database）
docs/design/2026-05-27-system-design.md:497:- `dorm_api_url` - 宿舍系统API地址
docs/design/2026-05-27-system-design.md:498:- `dorm_api_key` - 宿舍系统API密钥（加密存储）
docs/design/2026-05-27-system-design.md:499:- `dorm_db_config` - 宿舍系统数据库配置（加密存储，JSON格式）
docs/design/2026-05-27-system-design.md:544:- `approve` - 审批通过
docs/design/2026-05-27-system-design.md:545:- `reject` - 审批驳回
docs/design/2026-05-27-system-design.md:546:- `upload_attachment` - 上传附件
docs/design/2026-05-27-system-design.md:547:- `delete_attachment` - 删除附件
docs/design/2026-05-27-system-design.md:554:- `attachment` - 附件
docs/design/2026-05-27-system-design.md:567:    milestone VARCHAR(50) NOT NULL COMMENT '里程碑: submitted/approved/rejected',
docs/design/2026-05-27-system-design.md:582:  - `approved`: 最终通过时
docs/design/2026-05-27-system-design.md:583:  - `rejected`: 驳回时
docs/design/2026-05-27-system-design.md:602:  ├─1:N─→ attachments (一个申请多个附件)
docs/design/2026-05-27-system-design.md:611:attachments (附件表)
docs/design/2026-05-27-system-design.md:668:    "planned_leave_date": ["日期不能早于今天"]
docs/design/2026-05-27-system-design.md:856:  "planned_leave_date": "2026-06-15",
docs/design/2026-05-27-system-design.md:867:    "planned_leave_date": "2026-06-15",
docs/design/2026-05-27-system-design.md:875:GET /api/v1/applications?status=pending_counselor&page=1&page_size=20
docs/design/2026-05-27-system-design.md:891:        "status": "pending_counselor",
docs/design/2026-05-27-system-design.md:892:        "planned_leave_date": "2026-06-15",
docs/design/2026-05-27-system-design.md:917:    "status": "pending_counselor",
docs/design/2026-05-27-system-design.md:918:    "planned_leave_date": "2026-06-15",
docs/design/2026-05-27-system-design.md:920:    "attachments": [
docs/design/2026-05-27-system-design.md:924:        "attachment_type": "dorm_clearance"
docs/design/2026-05-27-system-design.md:929:        "approver_name": "李老师",
docs/design/2026-05-27-system-design.md:930:        "approver_role": "counselor",
docs/design/2026-05-27-system-design.md:931:        "action": "approve",
docs/design/2026-05-27-system-design.md:946:  "planned_leave_date": "2026-06-20",
docs/design/2026-05-27-system-design.md:967:    "status": "pending_counselor",
docs/design/2026-05-27-system-design.md:990:        "planned_leave_date": "2026-06-15",
docs/design/2026-05-27-system-design.md:1001:POST /api/v1/approvals/{application_id}/approve
docs/design/2026-05-27-system-design.md:1016:    "next_approver": "学工部",
docs/design/2026-05-27-system-design.md:1033:POST /api/v1/approvals/{application_id}/reject
docs/design/2026-05-27-system-design.md:1047:    "status": "rejected",
docs/design/2026-05-27-system-design.md:1066:POST /api/v1/applications/{id}/attachments
docs/design/2026-05-27-system-design.md:1072:- attachment_type: dorm_clearance
docs/design/2026-05-27-system-design.md:1083:    "attachment_type": "dorm_clearance",
docs/design/2026-05-27-system-design.md:1120:GET /api/v1/attachments/{id}/download
docs/design/2026-05-27-system-design.md:1128:DELETE /api/v1/attachments/{id}
docs/design/2026-05-27-system-design.md:1187:      "config_key": "dorm_integration_type",
docs/design/2026-05-27-system-design.md:1192:      "config_key": "dorm_api_url",
docs/design/2026-05-27-system-design.md:1193:      "config_value": "https://dorm.university.edu/api",
docs/design/2026-05-27-system-design.md:1197:      "config_key": "dorm_api_key",
docs/design/2026-05-27-system-design.md:1213:  "config_value": "https://dorm.new-university.edu/api"
docs/design/2026-05-27-system-design.md:1365:def approve_application(request, application_id):
docs/design/2026-05-27-system-design.md:1396:pending_counselor（待辅导员审核）
docs/design/2026-05-27-system-design.md:1397:  ↓ approve              ↓ reject
docs/design/2026-05-27-system-design.md:1398:pending_admin        rejected（已驳回）
docs/design/2026-05-27-system-design.md:1400:  ↓ approve
docs/design/2026-05-27-system-design.md:1401:approved（审批通过）
docs/design/2026-05-27-system-design.md:1407:    'draft': ['pending_counselor'],  # 提交
docs/design/2026-05-27-system-design.md:1408:    'pending_counselor': ['pending_admin', 'rejected'],  # 辅导员审批
docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
docs/design/2026-05-27-system-design.md:1410:    'rejected': ['pending_counselor'],  # 重新提交
docs/design/2026-05-27-system-design.md:1411:    'approved': []  # 终态
docs/design/2026-05-27-system-design.md:1425:  - 状态变更：draft → pending_counselor
docs/design/2026-05-27-system-design.md:1428:  - 设置当前审批人：current_approver_id = counselor_id
docs/design/2026-05-27-system-design.md:1437:- 触发条件：申请状态为 pending_counselor
docs/design/2026-05-27-system-design.md:1438:- 权限要求：辅导员角色 + current_approver_id匹配
docs/design/2026-05-27-system-design.md:1443:    - 更新当前审批人：current_approver_id = admin_id
docs/design/2026-05-27-system-design.md:1445:    - 创建审批记录：approvals（approver_role='counselor', action='approve'）
docs/design/2026-05-27-system-design.md:1447:    - 记录审计日志：audit_logs（action='approve', resource_type='application'）
docs/design/2026-05-27-system-design.md:1450:    - 状态变更 → rejected
docs/design/2026-05-27-system-design.md:1451:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1453:    - 创建审批记录：approvals（approver_role='counselor', action='reject'）
docs/design/2026-05-27-system-design.md:1455:    - 记录审计日志：audit_logs（action='reject', resource_type='application'）
docs/design/2026-05-27-system-design.md:1463:- 权限要求：学工部管理员角色 + current_approver_id匹配
docs/design/2026-05-27-system-design.md:1467:    - 状态变更 → approved
docs/design/2026-05-27-system-design.md:1468:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1472:    - 创建审批记录：approvals（approver_role='admin', action='approve'）
docs/design/2026-05-27-system-design.md:1474:    - 记录审计日志：audit_logs（action='approve', resource_type='application'）
docs/design/2026-05-27-system-design.md:1478:    - 状态变更 → rejected
docs/design/2026-05-27-system-design.md:1479:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1481:    - 创建审批记录：approvals（approver_role='admin', action='reject'）
docs/design/2026-05-27-system-design.md:1483:    - 记录审计日志：audit_logs（action='reject', resource_type='application'）
docs/design/2026-05-27-system-design.md:1490:- 触发条件：申请状态为 rejected
docs/design/2026-05-27-system-design.md:1494:  - 重新提交 → pending_counselor
docs/design/2026-05-27-system-design.md:1509:        status__in=['pending_counselor', 'pending_admin'],
docs/design/2026-05-27-system-design.md:1516:            approver_id=app.current_approver_id
docs/design/2026-05-27-system-design.md:1533:                approver_id=app.current_approver_id,
docs/design/2026-05-27-system-design.md:1534:                approver_role=app.status.replace('pending_', ''),
docs/design/2026-05-27-system-design.md:1623:GET /api/dorm/clearance/status
docs/design/2026-05-27-system-design.md:1636:    "dorm_building": "1号楼",
docs/design/2026-05-27-system-design.md:1637:    "dorm_room": "101",
docs/design/2026-05-27-system-design.md:1650:# apps/integrations/dorm_system.py
docs/design/2026-05-27-system-design.md:1653:        config = SystemConfig.objects.get(config_key='dorm_api_url')
docs/design/2026-05-27-system-design.md:1655:        self.api_key = SystemConfig.objects.get(config_key='dorm_api_key').get_decrypted_value()
docs/design/2026-05-27-system-design.md:1672:('dorm_integration_type', 'api', 'integration', FALSE),
docs/design/2026-05-27-system-design.md:1673:('dorm_api_url', 'https://dorm.university.edu/api', 'integration', FALSE),
docs/design/2026-05-27-system-design.md:1674:('dorm_api_key', 'encrypted_key_here', 'integration', TRUE);
docs/design/2026-05-27-system-design.md:1727:def verify_dorm_clearance(student_id):
docs/design/2026-05-27-system-design.md:2108:        location /api/v1/applications/*/attachments {
docs/design/2026-05-27-system-design.md:2206:def handle_file_upload(file, application_id, attachment_type):
docs/design/2026-05-27-system-design.md:2278:- 按操作查询：`/api/v1/audit-logs?action=approve`
docs/design/2026-05-27-system-design.md:2320:- `dorm_api_key` - 宿舍系统API密钥
docs/design/2026-05-27-system-design.md:2321:- `dorm_db_config` - 宿舍系统数据库配置（JSON格式）
docs/design/2026-05-27-system-design.md:2349:CREATE INDEX idx_planned_leave_date ON applications(planned_leave_date);
docs/design/2026-05-27-system-design.md:2352:CREATE INDEX idx_approver_status ON applications(current_approver_id, status, submit_time);
docs/design/2026-05-27-system-design.md:2358:CREATE INDEX idx_approver_id ON approvals(approver_id);
docs/design/2026-05-27-system-design.md:2362:-- attachments表索引
docs/design/2026-05-27-system-design.md:2363:CREATE INDEX idx_application_id ON attachments(application_id);
docs/design/2026-05-27-system-design.md:2364:CREATE INDEX idx_attachment_type ON attachments(attachment_type);
docs/design/2026-05-27-system-design.md:2365:CREATE INDEX idx_file_hash ON attachments(file_hash);
docs/design/2026-05-27-system-design.md:2366:CREATE INDEX idx_app_type ON attachments(application_id, attachment_type, is_deleted);
docs/design/2026-05-27-system-design.md:2386:- `idx_approver_status`: 待审批列表查询（按审批人+状态+时间）
docs/design/2026-05-27-system-design.md:2460:    if app.current_approver_id:
docs/design/2026-05-27-system-design.md:2461:        cache.delete(f'pending:count:{app.current_approver_id}')
docs/design/2026-05-27-system-design.md:2504:def upload_to_storage(file_path, attachment_id):
docs/design/2026-05-27-system-design.md:2576:    self.status = 'pending_counselor'
docs/design/2026-05-27-system-design.md:2589:    assert app.status == 'pending_counselor'
docs/design/2026-05-27-system-design.md:2593:    result = approve_application(app_id, counselor_id, 'approve')
docs/design/2026-05-27-system-design.md:2648:def test_student_cannot_approve():
docs/design/2026-05-27-system-design.md:2651:    response = client.post(f'/api/v1/approvals/{app_id}/approve')
docs/design/2026-05-27-system-design.md:2665:    response = client.post(f'/api/v1/applications/{app_id}/attachments', files={'file': fake_image})
docs/design/2026-05-27-system-design.md:2678:    approve_application(app_id, counselor_id, 'approve')
docs/design/2026-05-27-system-design.md:2679:    log = AuditLog.objects.filter(action='approve', resource_id=app_id).last()
docs/design/2026-05-27-system-design.md:2744:    def approve_application(self):
docs/design/2026-05-27-system-design.md:2745:        self.client.post("/api/v1/approvals/1/approve", json={"opinion": "同意", "version": 0})
backend/data/routing_coverage_report.json:3:  "dorm_manager_coverage": 5830,
backend/data/routing_coverage_report.json:6:  "missing_dorm_manager": [
backend/data/routing_coverage_report.json:596:        "dorm_manager": true,
backend/data/routing_coverage_report.json:606:        "dorm_manager": true,
backend/data/routing_coverage_report.json:616:        "dorm_manager": true,
backend/data/routing_coverage_report.json:626:        "dorm_manager": true,
backend/data/routing_coverage_report.json:636:        "dorm_manager": true,
backend/data/routing_coverage_report.json:646:        "dorm_manager": true,
backend/data/routing_coverage_report.json:656:        "dorm_manager": true,
backend/data/routing_coverage_report.json:666:        "dorm_manager": true,
backend/data/routing_coverage_report.json:676:        "dorm_manager": true,
backend/data/routing_coverage_report.json:686:        "dorm_manager": true,
backend/data/routing_coverage_report.json:696:        "dorm_manager": true,
backend/data/routing_coverage_report.json:706:        "dorm_manager": true,
backend/data/routing_coverage_report.json:716:        "dorm_manager": true,
backend/data/routing_coverage_report.json:726:        "dorm_manager": true,
backend/data/routing_coverage_report.json:736:        "dorm_manager": true,
backend/data/routing_coverage_report.json:746:        "dorm_manager": true,
backend/data/routing_coverage_report.json:756:        "dorm_manager": true,
backend/data/routing_coverage_report.json:766:        "dorm_manager": true,
backend/data/routing_coverage_report.json:776:        "dorm_manager": true,
backend/data/routing_coverage_report.json:786:        "dorm_manager": true,
backend/data/routing_coverage_report.json:796:        "dorm_manager": true,
backend/data/routing_coverage_report.json:806:        "dorm_manager": true,
backend/data/routing_coverage_report.json:816:        "dorm_manager": true,
backend/data/routing_coverage_report.json:826:        "dorm_manager": true,
backend/data/routing_coverage_report.json:836:        "dorm_manager": true,
backend/data/routing_coverage_report.json:846:        "dorm_manager": true,
backend/data/routing_coverage_report.json:856:        "dorm_manager": true,
backend/data/routing_coverage_report.json:866:        "dorm_manager": true,
backend/data/routing_coverage_report.json:876:        "dorm_manager": true,
backend/data/routing_coverage_report.json:886:        "dorm_manager": true,
backend/data/routing_coverage_report.json:896:        "dorm_manager": true,
backend/data/routing_coverage_report.json:906:        "dorm_manager": true,
backend/data/routing_coverage_report.json:916:        "dorm_manager": true,
backend/data/routing_coverage_report.json:926:        "dorm_manager": true,
backend/data/routing_coverage_report.json:936:        "dorm_manager": true,
backend/data/routing_coverage_report.json:946:        "dorm_manager": true,
backend/data/routing_coverage_report.json:956:        "dorm_manager": true,
backend/data/routing_coverage_report.json:966:        "dorm_manager": true,
backend/data/routing_coverage_report.json:976:        "dorm_manager": true,
backend/data/routing_coverage_report.json:986:        "dorm_manager": true,
backend/data/routing_coverage_report.json:996:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1006:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1016:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1026:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1036:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1046:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1056:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1066:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1076:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1086:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1096:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1106:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1116:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1126:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1136:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1146:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1156:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1166:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1176:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1186:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1196:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1206:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1216:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1226:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1236:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1246:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1256:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1266:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1276:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1286:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1296:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1306:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1316:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1326:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1336:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1346:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1356:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1366:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1376:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1386:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1396:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1406:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1416:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1426:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1436:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1446:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1456:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1466:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1476:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1486:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1496:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1506:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1516:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1526:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1536:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1546:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1556:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1566:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1576:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1586:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1596:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1606:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1616:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1626:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1636:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1646:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1656:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1666:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1676:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1686:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1696:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1706:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1716:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1726:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1736:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1746:        "dorm_manager": true,
backend/data/routing_coverage_report.json:1751:  "dorm_manager_coverage_pct": 98.04910864446687,
backend/scripts/execute_import_direct.py:55:        "data/dorm_managers_processed.csv",
backend/scripts/execute_import_direct.py:70:         "--file", "data/dorm_managers_processed.csv", "--dry-run"],
backend/scripts/execute_import_direct.py:113:         "--file", "data/dorm_managers_processed.csv"],
backend/scripts/execute_import_manual.sh:24:wc -l data/file5_students_merged_v2.csv data/dorm_managers_processed.csv data/counselors_processed.csv data/additional_staff.csv
backend/scripts/execute_import_manual.sh:29:python manage.py import_staff --file data/dorm_managers_processed.csv --dry-run
backend/scripts/execute_import_manual.sh:54:python manage.py import_staff --file data/dorm_managers_processed.csv
backend/scripts/verify_system_readiness.py:25:    dorm_managers = User.objects.filter(role='dorm_manager')
backend/scripts/verify_system_readiness.py:32:    print(f"宿管员: {dorm_managers.count()}")
backend/scripts/verify_system_readiness.py:60:    manager_buildings = set(dorm_managers.exclude(Q(building__isnull=True) | Q(building='')).values_list('building', flat=True))
backend/config/urls.py:9:    path('api/', include('apps.attachments.urls')),
backend/scripts/verify_db_status.py:30:    dorm_mgrs = User.objects.filter(role='dorm_manager').count()
backend/scripts/verify_db_status.py:36:    print(f"- 宿管: {dorm_mgrs}")
backend/scripts/verify_import_integrity.py:47:    dorm_mgrs = User.objects.filter(role='dorm_manager').count()
backend/scripts/verify_import_integrity.py:53:    print(f"  - 宿管: {dorm_mgrs} ({dorm_mgrs/total*100:.1f}%)")
backend/scripts/verify_import_integrity.py:59:    expected_dorm = 73
backend/scripts/verify_import_integrity.py:62:    expected_total = expected_students + expected_dorm + expected_counselor + expected_admin
backend/scripts/verify_import_integrity.py:67:    print(f"  宿管: {dorm_mgrs} / {expected_dorm} ({dorm_mgrs/expected_dorm*100:.1f}%)")
backend/scripts/verify_import_integrity.py:90:    # Note: Skipping dorm_manager and counselor field checks
backend/scripts/verify_import_integrity.py:111:    students_with_dorm_mgr = User.objects.filter(
backend/scripts/verify_import_integrity.py:122:    dorm_coverage = students_with_dorm_mgr / total_students * 100 if total_students > 0 else 0
backend/scripts/verify_import_integrity.py:125:    print(f"宿管路由覆盖: {students_with_dorm_mgr}/{total_students} ({dorm_coverage:.1f}%)")
backend/scripts/verify_import_integrity.py:128:    if dorm_coverage >= 98 and counselor_coverage >= 98:
backend/scripts/validate_routing_coverage.py:4:Ensures every student can be routed to dorm manager and counselor.
backend/scripts/validate_routing_coverage.py:27:def load_dorm_managers(file3_path: str) -> Dict[str, List[str]]:
backend/scripts/validate_routing_coverage.py:29:    Load File3 dorm manager data.
backend/scripts/validate_routing_coverage.py:75:    Validate that all students can be routed to approvers.
backend/scripts/validate_routing_coverage.py:80:    building_managers = load_dorm_managers(file3_path)
backend/scripts/validate_routing_coverage.py:85:        'dorm_manager_coverage': 0,
backend/scripts/validate_routing_coverage.py:88:        'missing_dorm_manager': [],
backend/scripts/validate_routing_coverage.py:99:        # Check dorm manager routing
backend/scripts/validate_routing_coverage.py:100:        has_dorm_manager = building in building_managers
backend/scripts/validate_routing_coverage.py:101:        if has_dorm_manager:
backend/scripts/validate_routing_coverage.py:102:            report['dorm_manager_coverage'] += 1
backend/scripts/validate_routing_coverage.py:104:            report['missing_dorm_manager'].append({
backend/scripts/validate_routing_coverage.py:122:        if has_dorm_manager and has_counselor:
backend/scripts/validate_routing_coverage.py:131:                    'dorm_manager': not has_dorm_manager,
backend/scripts/validate_routing_coverage.py:138:    report['dorm_manager_coverage_pct'] = (report['dorm_manager_coverage'] / total * 100) if total > 0 else 0
backend/scripts/validate_routing_coverage.py:150:    parser.add_argument('--file3', required=True, help='Path to File3 (dorm managers)')
backend/scripts/validate_routing_coverage.py:161:    print(f"\nDorm manager coverage: {report['dorm_manager_coverage']}/{report['total_students']} ({report['dorm_manager_coverage_pct']:.1f}%)")
backend/scripts/validate_routing_coverage.py:171:        print("\nMissing dorm managers for buildings:")
backend/scripts/validate_routing_coverage.py:172:        missing_buildings = set(s['building'] for s in report['missing_dorm_manager'])
backend/scripts/validate_routing_coverage.py:174:            count = sum(1 for s in report['missing_dorm_manager'] if s['building'] == building)
backend/config/settings/base.py:37:    'apps.attachments',
backend/config/settings/base.py:159:# Fallback dorm manager for students without building assignment
backend/scripts/execute_real_data_import_stage1.sh:32:wc -l backend/data/dorm_managers_processed.csv
backend/scripts/execute_real_data_import_stage1.sh:38:docker compose exec -T backend python manage.py import_staff --file data/dorm_managers_processed.csv --dry-run
backend/apps/approvals/validators.py:5:    'dorm_manager': ApplicationStatus.PENDING_DORM_MANAGER,
backend/apps/approvals/admin.py:7:    list_display = ['approval_id', 'application', 'step', 'approver', 'decision', 'decided_at']
backend/apps/approvals/admin.py:9:    search_fields = ['approval_id', 'application__application_id', 'approver__user_id']
backend/apps/approvals/urls.py:7:    path('<str:approval_id>/approve/', views.approve_approval, name='approve_approval'),
backend/apps/approvals/urls.py:8:    path('<str:approval_id>/reject/', views.reject_approval, name='reject_approval'),
backend/apps/approvals/migrations/0003_alter_approval_step.py:16:            field=models.CharField(choices=[('dorm_manager', '宿管员'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20),
backend/apps/approvals/migrations/0002_initial.py:20:            name='approver',
backend/apps/approvals/migrations/0001_initial.py:21:                ('approver_name', models.CharField(max_length=100)),
backend/apps/approvals/migrations/0001_initial.py:22:                ('decision', models.CharField(choices=[('pending', '待审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='pending', max_length=20)),
backend/scripts/validate_graduate_data.py:10:def validate_graduate_csv(csv_file, counselors_file, dorm_managers_file):
backend/scripts/validate_graduate_data.py:28:    # Load valid buildings from dorm managers
backend/scripts/validate_graduate_data.py:31:        with open(dorm_managers_file, 'r', encoding='utf-8') as f:
backend/scripts/validate_graduate_data.py:39:        warnings.append(f"Dorm managers file not found: {dorm_managers_file}")
backend/scripts/validate_graduate_data.py:41:        warnings.append(f"Error reading dorm managers: {str(e)}")
backend/scripts/validate_graduate_data.py:178:    parser.add_argument('--dorm-managers', default='backend/data/2026年社区辅导员信息统计表.csv',
backend/scripts/validate_graduate_data.py:186:        args.dorm_managers
backend/apps/approvals/tests/test_rejection_flow.py:36:        self.dorm_manager = User.objects.create_user(
backend/apps/approvals/tests/test_rejection_flow.py:47:            dorm_manager=self.dorm_manager,
backend/apps/approvals/tests/test_rejection_flow.py:48:            dorm_manager_name='宿管员',
backend/apps/approvals/tests/test_rejection_flow.py:64:            'contact_phone': '13800138000',
backend/apps/approvals/tests/test_rejection_flow.py:66:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/approvals/tests/test_rejection_flow.py:71:    def _approve_dorm_manager_step(self, application):
backend/apps/approvals/tests/test_rejection_flow.py:76:        dorm_manager_token = response.data['access_token']
backend/apps/approvals/tests/test_rejection_flow.py:78:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/approvals/tests/test_rejection_flow.py:80:        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dorm_manager_token}')
backend/apps/approvals/tests/test_rejection_flow.py:81:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/approve/', {
backend/apps/approvals/tests/test_rejection_flow.py:86:    def test_dorm_manager_rejection(self):
backend/apps/approvals/tests/test_rejection_flow.py:94:        dorm_manager_token = response.data['access_token']
backend/apps/approvals/tests/test_rejection_flow.py:97:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/approvals/tests/test_rejection_flow.py:99:        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dorm_manager_token}')
backend/apps/approvals/tests/test_rejection_flow.py:100:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/reject/', {
backend/apps/approvals/tests/test_rejection_flow.py:109:    def test_counselor_rejection(self):
backend/apps/approvals/tests/test_rejection_flow.py:113:        self._approve_dorm_manager_step(application)
backend/apps/approvals/tests/test_rejection_flow.py:115:        # Counselor login and reject
backend/apps/approvals/tests/test_rejection_flow.py:126:        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/reject/', {
backend/apps/approvals/tests/test_list_permissions.py:25:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
backend/apps/approvals/tests/test_list_permissions.py:26:        self.dorm_manager1.set_password('M001')
backend/apps/approvals/tests/test_list_permissions.py:27:        self.dorm_manager1.save()
backend/apps/approvals/tests/test_list_permissions.py:29:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
backend/apps/approvals/tests/test_list_permissions.py:30:        self.dorm_manager2.set_password('M002')
backend/apps/approvals/tests/test_list_permissions.py:31:        self.dorm_manager2.save()
backend/apps/approvals/tests/test_list_permissions.py:48:            leave_date='2024-07-01',
backend/apps/approvals/tests/test_list_permissions.py:57:            approver=self.counselor1,
backend/apps/approvals/tests/test_list_permissions.py:58:            approver_name='辅导员1',
backend/apps/approvals/tests/test_list_permissions.py:66:            approver=self.dorm_manager1,
backend/apps/approvals/tests/test_list_permissions.py:67:            approver_name='宿管员1',
backend/apps/approvals/tests/test_list_permissions.py:89:    def test_dorm_manager_sees_only_own_pending_approvals(self):
backend/apps/approvals/tests/test_list_permissions.py:90:        self.client.force_authenticate(user=self.dorm_manager1)
backend/apps/approvals/tests/test_list_permissions.py:96:    def test_dorm_manager_cannot_see_other_dorm_manager_approvals(self):
backend/apps/approvals/tests/test_list_permissions.py:97:        self.client.force_authenticate(user=self.dorm_manager2)
backend/apps/approvals/tests/test_list_permissions.py:115:    def test_decision_all_does_not_leak_cross_approver_data(self):
backend/apps/approvals/tests/test_list_permissions.py:116:        # Create second application and approval for counselor1 (approved)
backend/apps/approvals/tests/test_list_permissions.py:123:            leave_date='2024-07-02',
backend/apps/approvals/tests/test_list_permissions.py:126:        approval_c1_approved = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:127:            approval_id='apv_c1_approved',
backend/apps/approvals/tests/test_list_permissions.py:130:            approver=self.counselor1,
backend/apps/approvals/tests/test_list_permissions.py:131:            approver_name='辅导员1',
backend/apps/approvals/tests/test_list_permissions.py:142:            leave_date='2024-07-03',
backend/apps/approvals/tests/test_list_permissions.py:149:            approver=self.counselor2,
backend/apps/approvals/tests/test_list_permissions.py:150:            approver_name='辅导员2',
backend/apps/approvals/tests/test_list_permissions.py:163:        self.assertIn('apv_c1_approved', approval_ids)
backend/apps/approvals/tests/test_permissions.py:47:        self.dorm_manager1 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:54:        self.dorm_manager2 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:77:            dorm_manager=self.dorm_manager1,
backend/apps/approvals/tests/test_permissions.py:78:            dorm_manager_name='宿管员1',
backend/apps/approvals/tests/test_permissions.py:85:            dorm_manager=self.dorm_manager2,
backend/apps/approvals/tests/test_permissions.py:86:            dorm_manager_name='宿管员2',
backend/apps/approvals/tests/test_permissions.py:99:            leave_date='2024-06-30',
backend/apps/approvals/tests/test_permissions.py:108:            approver=self.counselor1,
backend/apps/approvals/tests/test_permissions.py:109:            approver_name='李老师',
backend/apps/approvals/tests/test_permissions.py:115:    def _create_dorm_manager_approval(self):
backend/apps/approvals/tests/test_permissions.py:122:            approver=self.dorm_manager1,
backend/apps/approvals/tests/test_permissions.py:123:            approver_name='宿管员1',
backend/apps/approvals/tests/test_permissions.py:127:    def test_student_cannot_approve_or_reject(self):
backend/apps/approvals/tests/test_permissions.py:131:        approve_response = self.client.post(
backend/apps/approvals/tests/test_permissions.py:132:            f'/api/approvals/{self.approval1.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:136:        reject_response = self.client.post(
backend/apps/approvals/tests/test_permissions.py:137:            f'/api/approvals/{self.approval1.approval_id}/reject/',
backend/apps/approvals/tests/test_permissions.py:142:        self.assertEqual(approve_response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/approvals/tests/test_permissions.py:143:        self.assertEqual(reject_response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/approvals/tests/test_permissions.py:150:            f'/api/approvals/{self.approval1.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:157:    def test_counselor_cannot_act_on_dorm_manager_step(self):
backend/apps/approvals/tests/test_permissions.py:159:        dorm_manager_approval = self._create_dorm_manager_approval()
backend/apps/approvals/tests/test_permissions.py:163:            f'/api/approvals/{dorm_manager_approval.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:170:    def test_non_assigned_dorm_manager_forbidden(self):
backend/apps/approvals/tests/test_permissions.py:172:        dorm_manager_approval = self._create_dorm_manager_approval()
backend/apps/approvals/tests/test_permissions.py:173:        self.client.force_authenticate(user=self.dorm_manager2)
backend/apps/approvals/tests/test_permissions.py:176:            f'/api/approvals/{dorm_manager_approval.approval_id}/reject/',
backend/apps/approvals/tests/test_permissions.py:183:    def test_cross_counselor_approve_forbidden(self):
backend/apps/approvals/tests/test_permissions.py:185:        # T002 tries to approve T001's application
backend/apps/approvals/tests/test_permissions.py:188:            f'/api/approvals/{self.approval1.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:194:    def test_cross_counselor_reject_forbidden(self):
backend/apps/approvals/tests/test_permissions.py:196:        # T002 tries to reject T001's application
backend/apps/approvals/tests/test_permissions.py:199:            f'/api/approvals/{self.approval1.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:32:        # Create dorm manager
backend/apps/approvals/tests/test_state_machine.py:33:        self.dorm_manager = User.objects.create_user(
backend/apps/approvals/tests/test_state_machine.py:52:            dorm_manager=self.dorm_manager,
backend/apps/approvals/tests/test_state_machine.py:53:            dorm_manager_name='宿管员',
backend/apps/approvals/tests/test_state_machine.py:66:            leave_date='2024-06-30',
backend/apps/approvals/tests/test_state_machine.py:75:            approver=self.counselor,
backend/apps/approvals/tests/test_state_machine.py:76:            approver_name='李老师',
backend/apps/approvals/tests/test_state_machine.py:88:            f'/api/approvals/{self.approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:96:            f'/api/approvals/{self.approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:102:    def test_reject_then_repeat_operation_conflict(self):
backend/apps/approvals/tests/test_state_machine.py:107:            f'/api/approvals/{self.approval.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:114:            f'/api/approvals/{self.approval.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:120:    def test_counselor_step_requires_pending_counselor_status(self):
backend/apps/approvals/tests/test_state_machine.py:126:        approve_response = self.client.post(
backend/apps/approvals/tests/test_state_machine.py:127:            f'/api/approvals/{self.approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:131:        reject_response = self.client.post(
backend/apps/approvals/tests/test_state_machine.py:132:            f'/api/approvals/{self.approval.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:137:        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_state_machine.py:138:        self.assertEqual(reject_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_state_machine.py:140:    def test_dorm_manager_step_requires_pending_dorm_manager_status(self):
backend/apps/approvals/tests/test_state_machine.py:144:        dorm_manager_approval = Approval.objects.create(
backend/apps/approvals/tests/test_state_machine.py:148:            approver=self.dorm_manager,
backend/apps/approvals/tests/test_state_machine.py:149:            approver_name='宿管员',
backend/apps/approvals/tests/test_state_machine.py:152:        self.client.force_authenticate(user=self.dorm_manager)
backend/apps/approvals/tests/test_state_machine.py:154:        approve_response = self.client.post(
backend/apps/approvals/tests/test_state_machine.py:155:            f'/api/approvals/{dorm_manager_approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:159:        reject_response = self.client.post(
backend/apps/approvals/tests/test_state_machine.py:160:            f'/api/approvals/{dorm_manager_approval.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:165:        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_state_machine.py:166:        self.assertEqual(reject_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/views.py:25:        OpenApiParameter('decision', str, description='决策过滤：pending/approved/rejected/all（默认pending）'),
backend/apps/approvals/views.py:47:    # 宿管员: 只看自己的dorm_manager审批
backend/apps/approvals/views.py:50:            approver=user,
backend/apps/approvals/views.py:52:        ).select_related('application', 'approver')
backend/apps/approvals/views.py:57:            approver=user,
backend/apps/approvals/views.py:59:        ).select_related('application', 'approver')
backend/apps/approvals/views.py:63:        queryset = Approval.objects.all().select_related('application', 'approver')
backend/apps/approvals/views.py:104:        approval = Approval.objects.select_related('application', 'approver').get(approval_id=approval_id)
backend/apps/approvals/views.py:111:    # Permission check: only the approver or dean can view this approval
backend/apps/approvals/views.py:112:    if user.role == UserRole.DEAN or approval.approver_id == user.user_id:
backend/apps/approvals/views.py:120:    operation_id='approvals_approve',
backend/apps/approvals/views.py:136:def approve_approval(request, approval_id):
backend/apps/approvals/views.py:154:    if approval.approver_id != user.user_id:
backend/apps/approvals/views.py:180:        # Auto-complete other pending dorm manager approvals for the same building
backend/apps/approvals/views.py:181:        # (New requirement: any dorm manager in the building can approve, others see "already approved")
backend/apps/approvals/views.py:182:        other_dorm_approvals = Approval.objects.filter(
backend/apps/approvals/views.py:188:        if other_dorm_approvals.exists():
backend/apps/approvals/views.py:189:            other_dorm_approvals.update(
backend/apps/approvals/views.py:191:                comment=f'已由{approval.approver_name}完成审批，无需重复操作',
backend/apps/approvals/views.py:195:                f"Auto-completed {other_dorm_approvals.count()} other dorm manager approvals "
backend/apps/approvals/views.py:196:                f"for application {application.application_id} after approval by {approval.approver.user_id}"
backend/apps/approvals/views.py:240:            approver=counselor,
backend/apps/approvals/views.py:241:            approver_name=counselor.name,
backend/apps/approvals/views.py:253:    operation_id='approvals_reject',
backend/apps/approvals/views.py:269:def reject_approval(request, approval_id):
backend/apps/approvals/views.py:287:    if approval.approver_id != user.user_id:
backend/apps/approvals/serializers.py:8:    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
backend/apps/approvals/serializers.py:12:        fields = ['approval_id', 'application_id', 'step', 'approver_id',
backend/apps/approvals/serializers.py:13:                  'approver_name', 'decision', 'created_at']
backend/apps/approvals/serializers.py:15:                            'approver_id', 'approver_name', 'decision', 'created_at']
backend/apps/approvals/serializers.py:20:    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
backend/apps/approvals/serializers.py:24:        fields = ['approval_id', 'application_id', 'step', 'approver_id',
backend/apps/approvals/serializers.py:25:                  'approver_name', 'decision', 'comment', 'decided_at']
backend/apps/approvals/serializers.py:27:                            'approver_id', 'approver_name', 'decision', 'decided_at']
backend/scripts/validate_import.py:4:Validates student-counselor-dorm_manager routing coverage after data import.
backend/scripts/validate_import.py:77:def validate_dorm_manager_coverage():
backend/scripts/validate_import.py:78:    """Validate every student building has at least one dorm manager."""
backend/scripts/validate_import.py:82:    dorm_managers = User.objects.filter(role=UserRole.DORM_MANAGER, active=True)
backend/scripts/validate_import.py:85:    manager_buildings = set(dorm_managers.values_list('building', flat=True).distinct())
backend/scripts/validate_import.py:94:        print(f"⚠ WARNING: {len(missing_buildings)} buildings without dorm managers:")
backend/scripts/validate_import.py:100:    print("✓ All student buildings have dorm managers")
backend/scripts/validate_import.py:103:    bldg_counts = dorm_managers.values('building').annotate(count=Count('user_id'))
backend/scripts/validate_import.py:129:        # Check dorm manager
backend/scripts/validate_import.py:132:            failures.append(f"Student {student.user_id}: No dorm manager for building {student.building}")
backend/scripts/validate_import.py:158:    results.append(validate_dorm_manager_coverage())
backend/apps/approvals/models.py:7:    DORM_MANAGER = 'dorm_manager', '宿管员'
backend/apps/approvals/models.py:14:    APPROVED = 'approved', '已通过'
backend/apps/approvals/models.py:15:    REJECTED = 'rejected', '已驳回'
backend/apps/approvals/models.py:22:    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals')
backend/apps/approvals/models.py:23:    approver_name = models.CharField(max_length=100)
backend/apps/applications/migrations/0001_initial.py:21:                ('leave_date', models.DateField()),
backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
backend/apps/applications/migrations/0001_initial.py:23:                ('dorm_checkout_status', models.CharField(choices=[('completed', '已清退'), ('pending', '清退中'), ('not_started', '未开始'), ('unknown', '状态未知')], default='not_started', max_length=20)),
backend/apps/applications/migrations/0006_application_contact_phone_and_more.py:15:            name='contact_phone',
backend/apps/applications/migrations/0006_application_contact_phone_and_more.py:20:            name='leave_date',
backend/apps/applications/migrations/0006_application_contact_phone_and_more.py:31:            field=models.CharField(choices=[('draft', '草稿'), ('pending_dorm_manager', '待宿管员审批'), ('pending_counselor', '待辅导员审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20),
backend/apps/applications/migrations/0005_alter_application_status.py:16:            field=models.CharField(choices=[('draft', '草稿'), ('pending_dorm_manager', '待宿管员审批'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20),
backend/apps/applications/tests/test_p0_fixes.py:30:    def test_can_resubmit_after_rejection(self):
backend/apps/applications/tests/test_p0_fixes.py:31:        # Create and reject first application
backend/apps/applications/tests/test_p0_fixes.py:38:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:42:        # Should be able to create second application after rejection
backend/apps/applications/tests/test_p0_fixes.py:49:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:64:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:75:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:105:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:109:        self.app_approved = Application.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:110:            application_id='app_approved',
backend/apps/applications/tests/test_p0_fixes.py:115:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:119:        self.app_rejected = Application.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:120:            application_id='app_rejected',
backend/apps/applications/tests/test_p0_fixes.py:125:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:134:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:135:            approver_name=self.counselor.name,
backend/apps/applications/tests/test_p0_fixes.py:139:        self.approval_approved = Approval.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:140:            approval_id='apv_approved',
backend/apps/applications/tests/test_p0_fixes.py:141:            application=self.app_approved,
backend/apps/applications/tests/test_p0_fixes.py:143:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:144:            approver_name=self.counselor.name,
backend/apps/applications/tests/test_p0_fixes.py:148:        self.approval_rejected = Approval.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:149:            approval_id='apv_rejected',
backend/apps/applications/tests/test_p0_fixes.py:150:            application=self.app_rejected,
backend/apps/applications/tests/test_p0_fixes.py:152:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:153:            approver_name=self.counselor.name,
backend/apps/applications/tests/test_p0_fixes.py:159:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:165:    def test_filter_approved_approvals(self):
backend/apps/applications/tests/test_p0_fixes.py:167:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:171:        self.assertEqual(approvals.first().approval_id, 'apv_approved')
backend/apps/applications/tests/test_p0_fixes.py:173:    def test_filter_rejected_approvals(self):
backend/apps/applications/tests/test_p0_fixes.py:175:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:179:        self.assertEqual(approvals.first().approval_id, 'apv_rejected')
backend/apps/applications/tests/test_p0_fixes.py:182:        approvals = Approval.objects.filter(approver=self.counselor)
backend/apps/applications/serializers.py:12:                  'contact_phone', 'reason', 'leave_date', 'status', 'created_at', 'updated_at']
backend/apps/applications/serializers.py:24:                  'contact_phone', 'reason', 'leave_date', 'status', 'dorm_checkout_status',
backend/apps/applications/serializers.py:27:                            'class_id', 'status', 'dorm_checkout_status',
backend/apps/applications/serializers.py:36:    contact_phone = serializers.CharField(max_length=20, required=True)
backend/apps/applications/serializers.py:38:    leave_date = serializers.DateField()
backend/apps/applications/serializers.py:40:    def validate_leave_date(self, value):
backend/apps/applications/models.py:8:    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
backend/apps/applications/models.py:9:    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
backend/apps/applications/models.py:10:    APPROVED = 'approved', '已通过'
backend/apps/applications/models.py:11:    REJECTED = 'rejected', '已驳回'
backend/apps/applications/models.py:26:    contact_phone = models.CharField(max_length=20, null=True, blank=True)
backend/apps/applications/models.py:28:    leave_date = models.DateField(null=True, blank=True)
backend/apps/applications/models.py:30:    dorm_checkout_status = models.CharField(max_length=20, choices=DormCheckoutStatus.choices, default=DormCheckoutStatus.NOT_STARTED)
backend/apps/applications/tests/test_error_cases.py:59:        self.dorm_manager = User.objects.create_user(
backend/apps/applications/tests/test_error_cases.py:77:            dorm_manager=self.dorm_manager,
backend/apps/applications/tests/test_error_cases.py:78:            dorm_manager_name='宿管员',
backend/apps/applications/tests/test_error_cases.py:84:    def test_dorm_blocked_error(self):
backend/apps/applications/tests/test_error_cases.py:94:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_error_cases.py:96:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_error_cases.py:113:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_error_cases.py:115:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_error_cases.py:121:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_error_cases.py:123:            'leave_date': (timezone.now().date() + timedelta(days=2)).isoformat()
backend/apps/applications/tests/test_error_cases.py:139:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_error_cases.py:141:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_error_cases.py:182:            # Missing leave_date
backend/apps/applications/tests/test_detail_permissions.py:32:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER, building='1号楼')
backend/apps/applications/tests/test_detail_permissions.py:33:        self.dorm_manager1.set_password('M001')
backend/apps/applications/tests/test_detail_permissions.py:34:        self.dorm_manager1.save()
backend/apps/applications/tests/test_detail_permissions.py:36:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER, building='2号楼')
backend/apps/applications/tests/test_detail_permissions.py:37:        self.dorm_manager2.set_password('M002')
backend/apps/applications/tests/test_detail_permissions.py:38:        self.dorm_manager2.save()
backend/apps/applications/tests/test_detail_permissions.py:50:        ClassMapping.objects.create(class_id='CS2020-01', dorm_manager=self.dorm_manager1, dorm_manager_name='宿管员1', counselor=self.counselor1, counselor_name='辅导员1', active=True)
backend/apps/applications/tests/test_detail_permissions.py:51:        ClassMapping.objects.create(class_id='CS2020-02', dorm_manager=self.dorm_manager2, dorm_manager_name='宿管员2', counselor=self.counselor2, counselor_name='辅导员2', active=True)
backend/apps/applications/tests/test_detail_permissions.py:57:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_detail_permissions.py:59:            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_detail_permissions.py:74:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_detail_permissions.py:76:            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_detail_permissions.py:91:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_detail_permissions.py:93:            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:12:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:14:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:21:        """Test reason field rejects empty string after trim"""
backend/apps/applications/tests/test_serializer_validation.py:23:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:25:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:31:    def test_leave_date_past(self):
backend/apps/applications/tests/test_serializer_validation.py:32:        """Test leave_date field rejects dates before today"""
backend/apps/applications/tests/test_serializer_validation.py:34:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:36:            'leave_date': (timezone.now().date() - timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:40:        self.assertIn('leave_date', serializer.errors)
backend/apps/applications/tests/test_serializer_validation.py:42:    def test_leave_date_today(self):
backend/apps/applications/tests/test_serializer_validation.py:43:        """Test leave_date field accepts today"""
backend/apps/applications/tests/test_serializer_validation.py:45:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:47:            'leave_date': timezone.now().date().isoformat()
backend/apps/applications/tests/test_serializer_validation.py:55:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:57:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:64:    def test_leave_date_validation_at_midnight_boundary(self, mock_now):
backend/apps/applications/tests/test_serializer_validation.py:65:        """Test leave_date validation at 23:59:59 boundary"""
backend/apps/applications/tests/test_serializer_validation.py:72:        # Submit with leave_date=tomorrow (2026-06-02)
backend/apps/applications/tests/test_serializer_validation.py:74:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:76:            'leave_date': '2026-06-02'
backend/apps/applications/tests/test_serializer_validation.py:82:    def test_leave_date_validation_after_midnight(self, mock_now):
backend/apps/applications/tests/test_serializer_validation.py:83:        """Test leave_date validation rejects past date after midnight"""
backend/apps/applications/tests/test_serializer_validation.py:90:        # Submit with leave_date=yesterday (2026-06-01)
backend/apps/applications/tests/test_serializer_validation.py:92:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:94:            'leave_date': '2026-06-01'
backend/apps/applications/tests/test_serializer_validation.py:98:        self.assertIn('leave_date', serializer.errors)
backend/apps/applications/tests/test_list_permissions.py:30:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
backend/apps/applications/tests/test_list_permissions.py:31:        self.dorm_manager1.set_password('M001')
backend/apps/applications/tests/test_list_permissions.py:32:        self.dorm_manager1.save()
backend/apps/applications/tests/test_list_permissions.py:34:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
backend/apps/applications/tests/test_list_permissions.py:35:        self.dorm_manager2.set_password('M002')
backend/apps/applications/tests/test_list_permissions.py:36:        self.dorm_manager2.save()
backend/apps/applications/tests/test_list_permissions.py:43:        ClassMapping.objects.create(class_id='CS2020-01', dorm_manager=self.dorm_manager1, dorm_manager_name='宿管员1', counselor=self.counselor1, counselor_name='辅导员1', active=True)
backend/apps/applications/tests/test_list_permissions.py:44:        ClassMapping.objects.create(class_id='CS2020-02', dorm_manager=self.dorm_manager2, dorm_manager_name='宿管员2', counselor=self.counselor2, counselor_name='辅导员2', active=True)
backend/apps/applications/tests/test_list_permissions.py:53:            leave_date='2024-07-01',
backend/apps/applications/tests/test_list_permissions.py:63:            leave_date='2024-07-01',
backend/apps/applications/tests/test_list_permissions.py:72:            approver=self.counselor1,
backend/apps/applications/tests/test_list_permissions.py:73:            approver_name='辅导员1',
backend/apps/applications/tests/test_list_permissions.py:90:    def test_counselor_sees_only_pending_counselor_approvals(self):
backend/apps/applications/tests/test_list_permissions.py:102:    def test_dean_sees_only_approved_applications_for_archive(self):
backend/apps/applications/tests/test_constraints.py:34:        self.dorm_manager = User.objects.create_user(
backend/apps/applications/tests/test_constraints.py:45:            dorm_manager=self.dorm_manager,
backend/apps/applications/tests/test_constraints.py:46:            dorm_manager_name='宿管员',
backend/apps/applications/tests/test_constraints.py:62:                'contact_phone': '13800138000',
backend/apps/applications/tests/test_constraints.py:64:                'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_constraints.py:74:                'contact_phone': '13800138000',
backend/apps/applications/tests/test_constraints.py:76:                'leave_date': (timezone.now().date() + timedelta(days=2)).isoformat()
backend/scripts/comprehensive_db_analysis.py:30:    for role in ['student', 'dorm_manager', 'counselor', 'admin']:
backend/apps/applications/tests/test_application_flow.py:37:        self.dorm_manager = User.objects.create_user(
backend/apps/applications/tests/test_application_flow.py:55:            dorm_manager=self.dorm_manager,
backend/apps/applications/tests/test_application_flow.py:56:            dorm_manager_name='宿管员',
backend/apps/applications/tests/test_application_flow.py:76:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_application_flow.py:78:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_application_flow.py:89:        dorm_manager_token = response.data['access_token']
backend/apps/applications/tests/test_application_flow.py:93:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/applications/tests/test_application_flow.py:95:        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dorm_manager_token}')
backend/apps/applications/tests/test_application_flow.py:96:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/approve/', {
backend/apps/applications/tests/test_application_flow.py:116:        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/approve/', {
backend/apps/applications/views.py:68:    # Dorm Manager: applications with own pending dorm manager approvals
backend/apps/applications/views.py:71:            approver=user,
backend/apps/applications/views.py:80:            approver=user,
backend/apps/applications/views.py:86:    # Dean: view all approved applications (archiving role)
backend/apps/applications/views.py:134:        # Check for existing pending/approved applications
backend/apps/applications/views.py:145:        dorm_status = provider.check_status(user.user_id)
backend/apps/applications/views.py:147:        if dorm_status.status != DormCheckoutStatus.COMPLETED:
backend/apps/applications/views.py:149:                                        'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
backend/apps/applications/views.py:150:                                                    'blocking_reason': dorm_status.blocking_reason}}},
backend/apps/applications/views.py:153:        # Find dorm managers
backend/apps/applications/views.py:154:        dorm_managers = []
backend/apps/applications/views.py:158:            dorm_managers = list(User.objects.filter(
backend/apps/applications/views.py:164:        if not dorm_managers:
backend/apps/applications/views.py:169:                dorm_managers = [fallback_manager]
backend/apps/applications/views.py:180:            draft.contact_phone = serializer.validated_data['contact_phone']
backend/apps/applications/views.py:182:            draft.leave_date = serializer.validated_data['leave_date']
backend/apps/applications/views.py:184:            draft.dorm_checkout_status = dorm_status.status
backend/apps/applications/views.py:194:                contact_phone=serializer.validated_data['contact_phone'],
backend/apps/applications/views.py:196:                leave_date=serializer.validated_data['leave_date'],
backend/apps/applications/views.py:198:                dorm_checkout_status=dorm_status.status
backend/apps/applications/views.py:202:        for dorm_manager in dorm_managers:
backend/apps/applications/views.py:203:            dorm_manager_approval = Approval.objects.create(
backend/apps/applications/views.py:207:                approver=dorm_manager,
backend/apps/applications/views.py:208:                approver_name=dorm_manager.name,
backend/apps/applications/views.py:211:            notify_application_submitted(application, dorm_manager_approval)
backend/apps/applications/views.py:215:            user.phone = serializer.validated_data['contact_phone']
backend/apps/users/class_mapping.py:7:    dorm_manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_dorms', null=True, blank=True)
backend/apps/users/class_mapping.py:8:    dorm_manager_name = models.CharField(max_length=100, null=True, blank=True)
backend/apps/applications/permissions.py:6:    """Check if user can view application and its attachments."""
backend/apps/applications/permissions.py:24:        return application.status == 'approved'
backend/apps/users/models.py:7:    DORM_MANAGER = 'dorm_manager', '宿管员'
backend/apps/users/services/xg_user_sync.py:83:            "until User model adds phone/email/department or name overwrite policy is approved"
backend/apps/attachments/urls.py:5:    path('applications/<str:application_id>/attachments/', views.attachments_view, name='attachments'),
backend/apps/attachments/urls.py:6:    path('attachments/<str:attachment_id>/download/', views.download_attachment, name='download_attachment'),
backend/apps/attachments/urls.py:7:    path('attachments/<str:attachment_id>/', views.delete_attachment, name='delete_attachment'),
backend/apps/users/migrations/0006_add_admin_role.py:19:                    ('dorm_manager', '宿管员'),
backend/apps/attachments/migrations/0001_initial.py:21:                ('attachment_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
backend/apps/attachments/migrations/0001_initial.py:22:                ('file', models.FileField(upload_to='attachments/%Y/%m/%d/')),
backend/apps/attachments/migrations/0001_initial.py:23:                ('attachment_type', models.CharField(choices=[('dorm_checkout', '宿舍清退证明'), ('library_clearance', '图书馆清书证明'), ('finance_clearance', '财务结清证明'), ('other', '其他')], max_length=50)),
backend/apps/attachments/migrations/0001_initial.py:30:                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='applications.application')),
backend/apps/attachments/migrations/0001_initial.py:34:                'db_table': 'attachments',
backend/apps/users/migrations/0004_backfill_dorm_manager.py:6:def backfill_dorm_manager(apps, schema_editor):
backend/apps/users/migrations/0004_backfill_dorm_manager.py:8:    for mapping in ClassMapping.objects.filter(dorm_manager__isnull=True):
backend/apps/users/migrations/0004_backfill_dorm_manager.py:9:        mapping.dorm_manager_id = mapping.counselor_id
backend/apps/users/migrations/0004_backfill_dorm_manager.py:10:        mapping.dorm_manager_name = mapping.counselor_name
backend/apps/users/migrations/0004_backfill_dorm_manager.py:11:        mapping.save(update_fields=["dorm_manager", "dorm_manager_name"])
backend/apps/users/migrations/0004_backfill_dorm_manager.py:16:    ClassMapping.objects.all().update(dorm_manager=None, dorm_manager_name=None)
backend/apps/users/migrations/0004_backfill_dorm_manager.py:22:        ('users', '0003_classmapping_dorm_manager_and_more'),
backend/apps/users/migrations/0004_backfill_dorm_manager.py:26:        migrations.RunPython(backfill_dorm_manager, reverse_backfill),
backend/apps/notifications/services.py:32:        recipient=approval.approver,
backend/apps/notifications/services.py:46:    Create notification for student when approval is approved or rejected.
backend/apps/notifications/services.py:54:    approver_role_map = {
backend/apps/notifications/services.py:55:        "dorm_manager": "宿管员",
backend/apps/notifications/services.py:58:    approver_role = approver_role_map.get(approval.step, "审批人")
backend/apps/notifications/services.py:62:        message = f"您的离校申请已通过{approver_role}审批。"
backend/apps/notifications/services.py:64:    else:  # rejected
backend/apps/notifications/services.py:66:        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
backend/apps/notifications/services.py:75:            'actor': approval.approver,
backend/apps/notifications/services.py:98:    dorm_manager_threshold = now - timedelta(days=2)
backend/apps/notifications/services.py:103:    ).select_related('approver', 'application__student')
backend/apps/notifications/services.py:110:        threshold = counselor_threshold if approval.step == 'counselor' else dorm_manager_threshold
backend/apps/notifications/services.py:122:                'approver': approval.approver.name,
backend/apps/notifications/services.py:128:                recipient=approval.approver,
backend/apps/notifications/services.py:143:                    'approver': approval.approver.name,
backend/apps/users/migrations/0005_user_building.py:7:        ('users', '0004_backfill_dorm_manager'),
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:17:            name='dorm_manager',
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:18:            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='managed_dorms', to=settings.AUTH_USER_MODEL),
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:22:            name='dorm_manager_name',
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:28:            field=models.CharField(choices=[('student', '学生'), ('dorm_manager', '宿管员'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20),
backend/backend/apps/users/management/commands/cleanup_test_data.py:36:        test_approvals = Approval.objects.filter(approver__user_id__in=test_ids)
backend/apps/notifications/models.py:16:    APPROVAL_APPROVED = 'approval_approved', '审批通过'
backend/apps/notifications/models.py:17:    APPROVAL_REJECTED = 'approval_rejected', '审批驳回'
backend/apps/users/management/commands/seed_data.py:81:        dorm_managers = [
backend/apps/users/management/commands/seed_data.py:87:        for dm_data in dorm_managers:
backend/apps/users/management/commands/seed_data.py:100:                self.stdout.write(f'Created dorm_manager: {user.user_id}')
backend/apps/users/management/commands/cleanup_test_data.py:32:            'dorm_managers': User.objects.filter(role='dorm_manager').count(),
backend/apps/users/management/commands/cleanup_test_data.py:42:            self.stdout.write(f'  - 宿管: {stats["dorm_managers"]}')
backend/apps/attachments/views.py:21:    operation_id='attachments_list',
backend/apps/attachments/views.py:33:    operation_id='attachments_upload',
backend/apps/attachments/views.py:48:def attachments_view(request, application_id):
backend/apps/attachments/views.py:49:    """Dispatcher for attachment list (GET) and upload (POST)"""
backend/apps/attachments/views.py:51:        return list_attachments(request, application_id)
backend/apps/attachments/views.py:53:        return upload_attachment(request, application_id)
backend/apps/attachments/views.py:56:def upload_attachment(request, application_id):
backend/apps/attachments/views.py:78:    # Create attachment
backend/apps/attachments/views.py:80:    attachment = Attachment.objects.create(
backend/apps/attachments/views.py:81:        attachment_id=f'att_{uuid.uuid4().hex[:12]}',
backend/apps/attachments/views.py:85:        attachment_type=serializer.validated_data['attachment_type'],
backend/apps/attachments/views.py:91:    return Response(AttachmentSerializer(attachment).data, status=status.HTTP_201_CREATED)
backend/apps/attachments/views.py:94:def list_attachments(request, application_id):
backend/apps/attachments/views.py:109:    # List attachments (exclude soft-deleted)
backend/apps/attachments/views.py:110:    attachments = Attachment.objects.filter(application=application, is_deleted=False)
backend/apps/attachments/views.py:111:    serializer = AttachmentSerializer(attachments, many=True)
backend/apps/attachments/views.py:112:    return Response({'attachments': serializer.data})
backend/apps/attachments/views.py:116:    operation_id='attachments_download',
backend/apps/attachments/views.py:128:def download_attachment(request, attachment_id):
backend/apps/attachments/views.py:131:    # Get attachment
backend/apps/attachments/views.py:133:        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
backend/apps/attachments/views.py:139:    if attachment.is_deleted:
backend/apps/attachments/views.py:144:    application = attachment.application
backend/apps/attachments/views.py:151:        return FileResponse(attachment.file.open('rb'), as_attachment=True, filename=attachment.file_name, content_type=attachment.content_type)
backend/apps/attachments/views.py:158:    operation_id='attachments_delete',
backend/apps/attachments/views.py:171:def delete_attachment(request, attachment_id):
backend/apps/attachments/views.py:174:    # Get attachment
backend/apps/attachments/views.py:176:        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
backend/apps/attachments/views.py:182:    if attachment.is_deleted:
backend/apps/attachments/views.py:187:    if user.role != UserRole.STUDENT or attachment.application.student_id != user.user_id:
backend/apps/attachments/views.py:192:    attachment.is_deleted = True
backend/apps/attachments/views.py:193:    attachment.deleted_at = timezone.now()
backend/apps/attachments/views.py:194:    attachment.save()
backend/apps/attachments/serializers.py:7:    attachment_type = serializers.ChoiceField(choices=AttachmentType.choices)
backend/apps/attachments/serializers.py:26:        fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'attachment_type', 'uploaded_at']
backend/apps/attachments/serializers.py:27:        read_only_fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'uploaded_at']
backend/apps/attachments/serializers.py:31:    """Schema-only: attachment list response with wrapper"""
backend/apps/attachments/serializers.py:32:    attachments = AttachmentSerializer(many=True)
backend/apps/applications/admin.py:8:    list_filter = ['status', 'dorm_checkout_status']
backend/apps/notifications/migrations/0001_initial.py:22:                ('type', models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('dorm_clearance_blocked', '宿舍清退阻断'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型')),
backend/apps/notifications/migrations/0002_alter_notification_type.py:16:            field=models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型'),
backend/apps/attachments/models.py:7:    DORM_CHECKOUT = 'dorm_checkout', '宿舍清退证明'
backend/apps/attachments/models.py:14:    attachment_id = models.CharField(max_length=50, primary_key=True)
backend/apps/attachments/models.py:15:    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='attachments')
backend/apps/attachments/models.py:17:    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
backend/apps/attachments/models.py:18:    attachment_type = models.CharField(max_length=50, choices=AttachmentType.choices)
backend/apps/attachments/models.py:27:        db_table = 'attachments'
backend/apps/attachments/models.py:31:        return f"{self.attachment_id} - {self.file_name}"
backend/apps/notifications/management/commands/send_approval_timeout_warnings.py:32:                    f"{warning['approver']} ({warning['days']} days)"
backend/apps/attachments/tests/test_upload.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_upload.py:65:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_upload.py:76:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_upload.py:81:        """Student can upload attachment to own application"""
backend/apps/attachments/tests/test_upload.py:86:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:89:                'attachment_type': AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_upload.py:96:        self.assertIn('attachment_id', response.data)
backend/apps/attachments/tests/test_upload.py:97:        self.assertTrue(response.data['attachment_id'].startswith('att_'))
backend/apps/attachments/tests/test_upload.py:98:        self.assertEqual(len(response.data['attachment_id']), 16)  # att_ + 12 hex chars
backend/apps/attachments/tests/test_upload.py:99:        self.assertEqual(response.data['attachment_type'], AttachmentType.DORM_CHECKOUT)
backend/apps/attachments/tests/test_upload.py:108:            f'/api/applications/{self.other_application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:111:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:120:        """Counselor cannot upload attachments"""
backend/apps/attachments/tests/test_upload.py:125:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:128:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:141:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:143:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:154:        """Upload fails with missing attachment_type"""
backend/apps/attachments/tests/test_upload.py:159:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:169:        self.assertIn('attachment_type', response.data['error']['details'])
backend/apps/attachments/tests/test_delete.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_delete.py:64:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_delete.py:68:        # Create attachment
backend/apps/attachments/tests/test_delete.py:70:        self.attachment = Attachment.objects.create(
backend/apps/attachments/tests/test_delete.py:71:            attachment_id='att_test001',
backend/apps/attachments/tests/test_delete.py:75:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_delete.py:82:        """Owner student can soft-delete attachment"""
backend/apps/attachments/tests/test_delete.py:86:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:92:        self.attachment.refresh_from_db()
backend/apps/attachments/tests/test_delete.py:93:        self.assertTrue(self.attachment.is_deleted)
backend/apps/attachments/tests/test_delete.py:94:        self.assertIsNotNone(self.attachment.deleted_at)
backend/apps/attachments/tests/test_delete.py:97:        """Non-owner student cannot delete attachment"""
backend/apps/attachments/tests/test_delete.py:101:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:108:        self.attachment.refresh_from_db()
backend/apps/attachments/tests/test_delete.py:109:        self.assertFalse(self.attachment.is_deleted)
backend/apps/attachments/tests/test_delete.py:112:        """Counselor cannot delete attachment"""
backend/apps/attachments/tests/test_delete.py:116:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:123:        """Deleting already-deleted attachment returns 404"""
backend/apps/attachments/tests/test_delete.py:124:        self.attachment.is_deleted = True
backend/apps/attachments/tests/test_delete.py:125:        self.attachment.save()
backend/apps/attachments/tests/test_delete.py:130:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_download.py:9:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_download.py:65:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_download.py:69:        # Create attachment with actual file
backend/apps/attachments/tests/test_download.py:71:        self.attachment = Attachment.objects.create(
backend/apps/attachments/tests/test_download.py:72:            attachment_id='att_test001',
backend/apps/attachments/tests/test_download.py:76:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_download.py:83:        """Student can download own application attachment"""
backend/apps/attachments/tests/test_download.py:87:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:94:        """Assigned counselor can download attachment"""
backend/apps/attachments/tests/test_download.py:98:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:104:        """Unauthorized student cannot download attachment"""
backend/apps/attachments/tests/test_download.py:108:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:115:        """Soft-deleted attachment returns 404"""
backend/apps/attachments/tests/test_download.py:116:        self.attachment.is_deleted = True
backend/apps/attachments/tests/test_download.py:117:        self.attachment.save()
backend/apps/attachments/tests/test_download.py:122:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/notifications/tests/test_timeout_warnings.py:30:        self.dorm_manager = User.objects.create_user(
backend/apps/notifications/tests/test_timeout_warnings.py:33:            role='dorm_manager',
backend/apps/notifications/tests/test_timeout_warnings.py:42:            leave_date='2026-07-01'
backend/apps/notifications/tests/test_timeout_warnings.py:47:            approver=self.counselor
backend/apps/notifications/tests/test_timeout_warnings.py:60:    def test_dorm_manager_timeout_2_days(self):
backend/apps/notifications/tests/test_timeout_warnings.py:61:        """Test dorm manager approval timeout after 2 days"""
backend/apps/notifications/tests/test_timeout_warnings.py:65:            leave_date='2026-07-01'
backend/apps/notifications/tests/test_timeout_warnings.py:69:            step='dorm_manager',
backend/apps/notifications/tests/test_timeout_warnings.py:70:            approver=self.dorm_manager
backend/apps/notifications/tests/test_timeout_warnings.py:80:            recipient=self.dorm_manager
backend/apps/notifications/tests/test_timeout_warnings.py:88:            leave_date='2026-07-01'
backend/apps/notifications/tests/test_timeout_warnings.py:93:            approver=self.counselor
backend/apps/notifications/tests/test_timeout_warnings.py:101:    def test_approved_not_notified(self):
backend/apps/notifications/tests/test_timeout_warnings.py:102:        """Test that approved/rejected approvals are not notified"""
backend/apps/notifications/tests/test_timeout_warnings.py:106:            leave_date='2026-07-01'
backend/apps/notifications/tests/test_timeout_warnings.py:111:            approver=self.counselor,
backend/apps/notifications/tests/test_timeout_warnings.py:127:            leave_date='2026-07-01'
backend/apps/notifications/tests/test_timeout_warnings.py:132:            approver=self.counselor
backend/apps/notifications/tests/test_timeout_warnings.py:150:            leave_date='2026-07-01'
backend/apps/notifications/tests/test_timeout_warnings.py:155:            approver=self.counselor
backend/apps/notifications/tests/test_auto_notifications.py:6:- Approval is approved (APPROVAL_APPROVED)
backend/apps/notifications/tests/test_auto_notifications.py:7:- Approval is rejected (APPROVAL_REJECTED)
backend/apps/notifications/tests/test_auto_notifications.py:41:        self.dorm_manager = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications.py:44:            role='dorm_manager',
backend/apps/notifications/tests/test_auto_notifications.py:56:            leave_date='2024-06-30',
backend/apps/notifications/tests/test_auto_notifications.py:64:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:65:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:80:    def test_approval_approved_notification_counselor(self):
backend/apps/notifications/tests/test_auto_notifications.py:88:            leave_date='2024-06-30',
backend/apps/notifications/tests/test_auto_notifications.py:96:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:97:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:106:        self.assertEqual(notification.type, 'approval_approved')
backend/apps/notifications/tests/test_auto_notifications.py:111:    def test_approval_approved_notification_dorm_manager(self):
backend/apps/notifications/tests/test_auto_notifications.py:112:        """Test APPROVAL_APPROVED notification for dorm manager approval."""
backend/apps/notifications/tests/test_auto_notifications.py:119:            leave_date='2024-06-30',
backend/apps/notifications/tests/test_auto_notifications.py:127:            approver=self.dorm_manager,
backend/apps/notifications/tests/test_auto_notifications.py:128:            approver_name=self.dorm_manager.name,
backend/apps/notifications/tests/test_auto_notifications.py:136:        self.assertEqual(notification.actor, self.dorm_manager)
backend/apps/notifications/tests/test_auto_notifications.py:137:        self.assertEqual(notification.type, 'approval_approved')
backend/apps/notifications/tests/test_auto_notifications.py:140:    def test_approval_rejected_notification(self):
backend/apps/notifications/tests/test_auto_notifications.py:148:            leave_date='2024-06-30',
backend/apps/notifications/tests/test_auto_notifications.py:156:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:157:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:167:        self.assertEqual(notification.type, 'approval_rejected')
backend/apps/notifications/tests/test_auto_notifications.py:179:            leave_date='2024-06-30',
backend/apps/notifications/tests/test_auto_notifications.py:187:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:188:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:214:            leave_date='2024-06-30',
backend/apps/notifications/tests/test_auto_notifications.py:222:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:223:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:238:            type='approval_approved'
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:40:- `apps/approvals/tests/test_rejection_flow.py`
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:56:### 修复3: 校准test_dorm_blocked_error测试数据 ✓
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:77:  apps.approvals.tests.test_rejection_flow
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:107:### 问题3: test_dorm_blocked_error返回201而非422
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:119:4. **数据校准建议:** 指出test_dorm_blocked_error需要重新校准测试数据
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:153:3. `apps/applications/tests/test_error_cases.py` - 添加ClassMapping + 修复test_dorm_blocked_error
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:154:4. `apps/approvals/tests/test_rejection_flow.py` - 添加ClassMapping
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:25:**Codex指出:** 未修复点集中在test_error_cases.py和test_rejection_flow.py，7个测试中6个KeyError
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:29:- 剩余工作：test_error_cases.py 4个方法 + test_rejection_flow.py 10个POST调用
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:43:**Codex指出:** `test_dorm_blocked_error`已加`format='json'`但返回404而非422
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:89:2. ~~手动给test_rejection_flow.py所有10个POST添加format='json'~~
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:112:docker exec backend python manage.py test apps.applications.tests.test_application_flow apps.applications.tests.test_error_cases apps.approvals.tests.test_rejection_flow --keepdb
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:115:**Step 5: 处理test_dorm_blocked_error的404问题**
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:192:4. **test_dorm_blocked_error的404问题:** 是否应该在Phase 0处理，还是作为独立问题？
backend/apps/attachments/tests/test_list.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_list.py:87:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_list.py:91:        # Create attachment
backend/apps/attachments/tests/test_list.py:92:        self.attachment = Attachment.objects.create(
backend/apps/attachments/tests/test_list.py:93:            attachment_id='att_test001',
backend/apps/attachments/tests/test_list.py:97:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_list.py:104:        """Student can list own application attachments"""
backend/apps/attachments/tests/test_list.py:108:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:112:        self.assertEqual(len(response.data['attachments']), 1)
backend/apps/attachments/tests/test_list.py:113:        self.assertEqual(response.data['attachments'][0]['attachment_id'], 'att_test001')
backend/apps/attachments/tests/test_list.py:116:        """Student cannot list another student's attachments"""
backend/apps/attachments/tests/test_list.py:120:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:127:        """Assigned counselor can list application attachments"""
backend/apps/attachments/tests/test_list.py:131:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:135:        self.assertEqual(len(response.data['attachments']), 1)
backend/apps/attachments/tests/test_list.py:138:        """Cross-counselor cannot list application attachments"""
backend/apps/attachments/tests/test_list.py:142:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:149:        """Dean can list approved application attachments for archiving"""
backend/apps/attachments/tests/test_list.py:153:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:157:        self.assertEqual(len(response.data['attachments']), 1)
backend/apps/attachments/tests/test_list.py:160:        """List excludes soft-deleted attachments"""
backend/apps/attachments/tests/test_list.py:161:        # Soft delete the attachment
backend/apps/attachments/tests/test_list.py:162:        self.attachment.is_deleted = True
backend/apps/attachments/tests/test_list.py:163:        self.attachment.save()
backend/apps/attachments/tests/test_list.py:168:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:172:        self.assertEqual(len(response.data['attachments']), 0)
backend/apps/users/management/commands/import_staff.py:18:    help = 'Import staff (dorm managers, counselors, admins) from CSV'
backend/apps/users/management/commands/import_staff.py:106:            # Allow empty building for fallback dorm manager
backend/apps/notifications/tests/test_auto_notifications_api.py:40:        self.dorm_manager = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:43:            role='dorm_manager',
backend/apps/notifications/tests/test_auto_notifications_api.py:54:            dorm_manager=self.dorm_manager,
backend/apps/notifications/tests/test_auto_notifications_api.py:55:            dorm_manager_name=self.dorm_manager.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:62:        """Test dorm manager can see APPLICATION_SUBMITTED notification via API after student submits."""
backend/apps/notifications/tests/test_auto_notifications_api.py:66:            'contact_phone': '13800138000',
backend/apps/notifications/tests/test_auto_notifications_api.py:68:            'leave_date': '2026-07-01'
backend/apps/notifications/tests/test_auto_notifications_api.py:73:        self.client.force_authenticate(user=self.dorm_manager)
backend/apps/notifications/tests/test_auto_notifications_api.py:83:    def test_approval_approved_notification_visible_via_api(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:84:        """Test student can see APPROVAL_APPROVED notification via API after counselor approves."""
backend/apps/notifications/tests/test_auto_notifications_api.py:92:            leave_date='2026-07-01',
backend/apps/notifications/tests/test_auto_notifications_api.py:100:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications_api.py:101:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:105:        # Counselor approves (triggers notification)
backend/apps/notifications/tests/test_auto_notifications_api.py:107:        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
backend/apps/notifications/tests/test_auto_notifications_api.py:121:        approval_notif = [n for n in notifications if n['type'] == 'approval_approved'][0]
backend/apps/notifications/tests/test_auto_notifications_api.py:125:    def test_approval_rejected_notification_includes_reason(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:126:        """Test APPROVAL_REJECTED notification includes rejection reason in message."""
backend/apps/notifications/tests/test_auto_notifications_api.py:134:            leave_date='2026-07-01',
backend/apps/notifications/tests/test_auto_notifications_api.py:142:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications_api.py:143:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:147:        # Counselor rejects with reason
backend/apps/notifications/tests/test_auto_notifications_api.py:149:        response = self.client.post(f'/api/approvals/{approval.approval_id}/reject/', {
backend/apps/notifications/tests/test_auto_notifications_api.py:160:        reject_notif = [n for n in notifications if n['type'] == 'approval_rejected'][0]
backend/apps/notifications/tests/test_auto_notifications_api.py:161:        self.assertIn('材料不齐全，请补充', reject_notif['message'])
backend/apps/notifications/tests/test_auto_notifications_api.py:181:            leave_date='2026-07-01',
backend/apps/notifications/tests/test_auto_notifications_api.py:189:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications_api.py:190:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:194:        # Student2 tries to approve (should fail with permission denied)
backend/apps/notifications/tests/test_auto_notifications_api.py:196:        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
backend/apps/notifications/tests/test_auto_notifications_api.py:216:            leave_date='2026-07-01',
backend/apps/notifications/tests/test_auto_notifications_api.py:224:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications_api.py:225:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:226:            decision=ApprovalDecision.APPROVED  # Already approved
backend/apps/notifications/tests/test_auto_notifications_api.py:229:        # Counselor tries to approve again (should fail with conflict)
backend/apps/notifications/tests/test_auto_notifications_api.py:231:        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
backend/apps/notifications/tests/test_auto_notifications_api.py:243:    def test_dorm_blocked_does_not_create_notification(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:244:        """Test that dorm checkout blockage does not create notifications."""
backend/apps/notifications/tests/test_auto_notifications_api.py:245:        # Create student with non-completed dorm status (use ID not in mock data)
backend/apps/notifications/tests/test_auto_notifications_api.py:255:        # Student tries to submit application (should fail with 422 dorm blocked)
backend/apps/notifications/tests/test_auto_notifications_api.py:258:            'contact_phone': '13800138000',
backend/apps/notifications/tests/test_auto_notifications_api.py:260:            'leave_date': '2026-07-01'
backend/apps/notifications/tests/test_auto_notifications_api.py:272:            recipient=self.dorm_manager,
backend/apps/users/management/commands/import_students.py:34:            active_apps = Application.objects.exclude(status='rejected').count()

codex
初步搜索显示设计文档内部有旧版“辅导员→学工部”的片段，但后端代码和用户给出的目标流程以“宿管员→辅导员”为准；我会以后端实现作为校准源，顺带标注设计文档中的不一致风险。
exec
/bin/bash -lc "rtk sed -n '1,430p' demo-web/index.html" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>毕业离校申请系统 - UI Demo</title>
  <link rel="stylesheet" href="css/global.css">
  <style>
    /* 导航标签 */
    .nav-tabs {
      background: white;
      display: flex;
      border-bottom: 1px solid #f0f0f0;
      position: sticky;
      top: 0;
      z-index: 10;
    }
    .nav-tab {
      flex: 1;
      text-align: center;
      padding: 12px 0;
      font-size: 14px;
      color: #666;
      cursor: pointer;
      position: relative;
      border: none;
      background: none;
    }
    .nav-tab.active {
      color: var(--primary-color);
      font-weight: 600;
    }
    .nav-tab.active::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 30px;
      height: 2px;
      background: var(--primary-color);
      border-radius: 1px;
    }

    /* 响应式：桌面端Tab导航优化 */
    @media (min-width: 1024px) {
      .nav-tabs {
        padding: 0 40px;
      }
      .nav-tab {
        padding: 16px 24px;
        font-size: 16px;
      }
      .nav-tab.active::after {
        width: 50px;
        height: 3px;
      }
    }

    /* 附件上传区域样式 */
    .upload-area {
      border: 2px dashed #d9d9d9;
      border-radius: 8px;
      padding: 30px;
      text-align: center;
      cursor: pointer;
      transition: all 0.3s;
    }
    .upload-area:hover {
      border-color: var(--primary-color);
      background: #fafafa;
    }
    .file-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px;
      background: #fafafa;
      border-radius: 4px;
      margin-bottom: 8px;
    }
    .file-info {
      flex: 1;
      margin-left: 8px;
    }
    .file-name {
      font-size: 14px;
      color: #333;
    }
    .file-size {
      font-size: 12px;
      color: #999;
    }
    .btn-delete {
      background: none;
      border: none;
      color: var(--status-error);
      font-size: 20px;
      cursor: pointer;
      padding: 0 8px;
    }

    .screen {
      display: none;
      min-height: calc(100vh - 45px);
    }
    .screen.active {
      display: block;
    }
  </style>
</head>
<body>
  <!-- 顶部导航 -->
  <div class="nav-tabs">
    <button class="nav-tab active" onclick="showScreen(0)">学生申请</button>
    <button class="nav-tab" onclick="showScreen(1)"><span id="nav-approval-text">审批列表</span></button>
    <button class="nav-tab" onclick="showScreen(2)">申请详情</button>
  </div>

  <!-- 角色选择器 -->
  <div style="background: white; padding: 8px 16px; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; gap: 10px;">
    <span style="font-size: 14px; color: #666;">演示角色:</span>
    <select id="roleSelector" onchange="switchRole(this.value)" style="padding: 4px 8px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;">
      <option value="dorm_manager">宿管员</option>
      <option value="counselor">辅导员</option>
      <option value="dean">学工部</option>
    </select>
  </div>

  <!-- 屏幕1: 学生申请页 -->
  <div class="screen active" id="screen-0">
    <div style="padding: 20px;">
      <!-- 用户信息卡片 -->
      <div class="card" style="margin-bottom: 20px;">
        <div style="font-size: 16px; font-weight: 600; color: var(--primary-color); margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #f0f0f0;">
          申请人信息
        </div>
        <div style="display: flex; align-items: center; padding: 10px 0;">
          <span style="font-size: 14px; color: #666; width: 80px;">姓名</span>
          <span style="font-size: 14px; color: #333;">张三</span>
        </div>
        <div style="display: flex; align-items: center; padding: 10px 0;">
          <span style="font-size: 14px; color: #666; width: 80px;">学号</span>
          <span style="font-size: 14px; color: #333;">2020001</span>
        </div>
      </div>

      <!-- 表单卡片 -->
      <div class="card">
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">离校原因</label>
          <textarea style="width: 100%; min-height: 120px; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入离校原因"></textarea>
          <span style="display: block; text-align: right; font-size: 12px; color: #999; margin-top: 4px;">0/500</span>
        </div>
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">离校日期</label>
          <input type="date" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;">
        </div>

        <!-- 附件上传区域 -->
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">附件材料（可选）</label>
          <div class="upload-zone">
            <input type="file" id="fileInput" multiple accept=".jpg,.jpeg,.png,.pdf,.doc,.docx" style="display: none;">
            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
              <div style="font-size: 40px; color: #999; margin-bottom: 8px;">📎</div>
              <div style="font-size: 14px; color: #666;">点击或拖拽文件到此处上传</div>
              <div style="font-size: 12px; color: #999; margin-top: 4px;">支持jpg/png/pdf/doc/docx，单文件不超过10MB</div>
            </div>
          </div>
          <!-- 文件列表 -->
          <div id="fileList" style="margin-top: 12px;"></div>
        </div>

        <button class="btn-primary">提交申请</button>
      </div>
    </div>
  </div>

  <!-- 屏幕2: 审批列表页 -->
  <div class="screen" id="screen-1">
    <div style="background: white; padding: 16px; display: flex; justify-content: space-between; align-items: center;">
      <div style="font-size: 18px; font-weight: bold;" id="list-title">审批列表</div>
      <div style="font-size: 12px; color: #999;" id="role-display">宿管员</div>
    </div>

    <!-- Tab切换 -->
    <div style="background: white; display: flex; border-bottom: 1px solid #f0f0f0;">
      <div class="nav-tab active" style="flex: 1;">全部</div>
      <div class="nav-tab" style="flex: 1;">待审批</div>
      <div class="nav-tab" style="flex: 1;">已审批</div>
    </div>

    <div style="padding: 10px;">
      <!-- 列表项 -->
      <div class="card">
        <div class="flex-row justify-between align-center" style="margin-bottom: 8px;">
          <span style="font-size: 16px; font-weight: bold;">申请 APP-001</span>
          <span class="tag tag-pending">待审批</span>
        </div>
        <div style="margin-bottom: 4px;">
          <span style="font-size: 14px; color: #999; margin-right: 8px;">申请ID:</span>
          <span style="font-size: 14px; color: #333;">APP-001</span>
        </div>
        <div style="margin-bottom: 4px;">
          <span style="font-size: 14px; color: #999; margin-right: 8px;">审批步骤:</span>
          <span style="font-size: 14px; color: #333;">宿管员审批</span>
        </div>
        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0f0f0;">
          <span style="font-size: 12px; color: #999;">2024-06-01 10:30</span>
        </div>
      </div>

      <div class="card">
        <div class="flex-row justify-between align-center" style="margin-bottom: 8px;">
          <span style="font-size: 16px; font-weight: bold;">申请 APP-002</span>
          <span class="tag tag-approved">已通过</span>
        </div>
        <div style="margin-bottom: 4px;">
          <span style="font-size: 14px; color: #999; margin-right: 8px;">申请ID:</span>
          <span style="font-size: 14px; color: #333;">APP-002</span>
        </div>
        <div style="margin-bottom: 4px;">
          <span style="font-size: 14px; color: #999; margin-right: 8px;">审批步骤:</span>
          <span style="font-size: 14px; color: #333;">辅导员审批</span>
        </div>
        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0f0f0;">
          <span style="font-size: 12px; color: #999;">2024-05-30 14:20</span>
        </div>
      </div>
    </div>
  </div>

  <!-- 屏幕3: 申请详情页 -->
  <div class="screen" id="screen-2">
    <div style="background: white; padding: 16px;">
      <div style="font-size: 18px; font-weight: bold;">申请详情</div>
    </div>

    <div style="padding: 10px;">
      <!-- 基本信息 -->
      <div class="card">
        <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">基本信息</div>
        <div style="display: flex; margin-bottom: 8px;">
          <span style="font-size: 14px; color: #999; width: 80px;">申请ID:</span>
          <span style="font-size: 14px; color: #333; flex: 1;">APP-001</span>
        </div>
        <div style="display: flex; margin-bottom: 8px;">
          <span style="font-size: 14px; color: #999; width: 80px;">学生:</span>
          <span style="font-size: 14px; color: #333; flex: 1;">张三 (2020001)</span>
        </div>
        <div style="display: flex; margin-bottom: 8px;">
          <span style="font-size: 14px; color: #999; width: 80px;">离校日期:</span>
          <span style="font-size: 14px; color: #333; flex: 1;">2024-06-15</span>
        </div>
        <div style="display: flex; margin-bottom: 8px;">
          <span style="font-size: 14px; color: #999; width: 80px;">申请原因:</span>
          <span style="font-size: 14px; color: #333; flex: 1;">毕业实习，需要提前离校</span>
        </div>
      </div>

      <!-- 审批记录时间轴 -->
      <div class="card">
        <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">审批记录</div>

        <!-- 时间轴项 -->
        <div style="position: relative; padding-left: 30px; margin-bottom: 20px;">
          <div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: white; border: 2px solid var(--primary-color);"></div>
          <div style="position: absolute; left: 14px; top: 16px; bottom: -20px; width: 1px; background: #e8e8e8;"></div>
          <div class="flex-row justify-between align-center" style="margin-bottom: 6px;">
            <span style="font-size: 15px; font-weight: 600;">宿管员审批</span>
            <span class="tag tag-pending">待审批</span>
          </div>
          <div style="font-size: 13px; color: #666;">审批人: 李老师</div>
        </div>

        <div style="position: relative; padding-left: 30px; margin-bottom: 20px;">
          <div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--status-success); border: 2px solid var(--status-success);"></div>
          <div class="flex-row justify-between align-center" style="margin-bottom: 6px;">
            <span style="font-size: 15px; font-weight: 600;">提交申请</span>
            <span class="tag tag-approved">已完成</span>
          </div>
          <div style="font-size: 13px; color: #666;">提交时间: 2024-06-01 10:30</div>
        </div>
      </div>

      <!-- 审批操作 -->
      <div style="padding: 10px;">
        <div class="card" style="margin-bottom: 10px;">
          <label style="display: block; font-size: 14px; color: #333; margin-bottom: 6px; font-weight: 500;">审批意见（可选）</label>
          <textarea style="width: 100%; min-height: 60px; padding: 8px; border: 1px solid #e8e8e8; border-radius: 4px; font-size: 14px;" placeholder="请输入审批意见"></textarea>
          <span style="display: block; text-align: right; font-size: 12px; color: #999; margin-top: 4px;">0/200</span>
        </div>
        <div style="display: flex; gap: 10px;" id="approval-actions">
          <button class="btn-primary" style="flex: 1;">通过</button>
          <button class="btn-outline" style="flex: 1;">拒绝</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    let currentRole = 'dorm_manager';

    function showScreen(index) {
      document.querySelectorAll('.screen').forEach((s, i) => {
        s.classList.toggle('active', i === index);
      });
      document.querySelectorAll('.nav-tabs .nav-tab').forEach((t, i) => {
        t.classList.toggle('active', i === index);
      });
    }

    function switchRole(role) {
      currentRole = role;
      const roleMap = {
        'dorm_manager': '宿管员',
        'counselor': '辅导员',
        'dean': '学工部'
      };
      const isDean = role === 'dean';

      // Update nav tab text
      document.getElementById('nav-approval-text').textContent = isDean ? '备案查询' : '审批列表';

      // Update list page title and role display
      document.getElementById('list-title').textContent = isDean ? '备案查询' : '审批列表';
      document.getElementById('role-display').textContent = roleMap[role];

      // Show/hide approval buttons
      const approvalActions = document.getElementById('approval-actions');
      if (approvalActions) {
        approvalActions.style.display = isDean ? 'none' : 'flex';
      }
    }

    // File upload management
    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
    const ALLOWED_TYPES = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx'];
    let uploadedFiles = [];

    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    const uploadArea = document.querySelector('.upload-area');

    // File selection handler
    fileInput.addEventListener('change', (e) => {
      handleFiles(e.target.files);
    });

    // Drag and drop handlers
    uploadArea.addEventListener('dragover', (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = 'var(--primary-color)';
      uploadArea.style.background = '#fafafa';
    });

    uploadArea.addEventListener('dragleave', () => {
      uploadArea.style.borderColor = '#d9d9d9';
      uploadArea.style.background = 'white';
    });

    uploadArea.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = '#d9d9d9';
      uploadArea.style.background = 'white';
      handleFiles(e.dataTransfer.files);
    });

    function handleFiles(files) {
      const validFiles = [];
      const errors = [];

      Array.from(files).forEach(file => {
        const ext = '.' + file.name.split('.').pop().toLowerCase();

        if (!ALLOWED_TYPES.includes(ext)) {
          errors.push(`${file.name}: 不支持的文件格式`);
          return;
        }

        if (file.size > MAX_FILE_SIZE) {
          errors.push(`${file.name}: 文件大小超过10MB`);
          return;
        }

        validFiles.push(file);
      });

      if (errors.length > 0) {
        alert(errors.join('\n'));
      }

      uploadedFiles = uploadedFiles.concat(validFiles);
      renderFileList();
      fileInput.value = ''; // Reset input
    }

    function renderFileList() {
      fileList.innerHTML = uploadedFiles.map((file, index) => `
        <div class="file-item">
          <span style="font-size: 20px;">📄</span>
          <div class="file-info">
            <div class="file-name">${file.name}</div>
            <div class="file-size">${formatFileSize(file.size)}</div>
          </div>
          <button class="btn-delete" onclick="removeFile(${index})" type="button">×</button>
        </div>
      `).join('');
    }

    function removeFile(index) {
      uploadedFiles.splice(index, 1);
      renderFileList();
    }

    function formatFileSize(bytes) {
      if (bytes < 1024) return bytes + ' B';
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
      return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }
  </script>
</body>
</html>

exec
/bin/bash -lc "rtk rg -n \"class Application|ApplicationStatus|contact_phone|leave_date|reason|pending_dorm_manager|pending_counselor|Approval|approve|reject|attachments|attachment_type\" backend/apps -g '*.py'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/approvals/validators.py:1:from apps.applications.models import ApplicationStatus
backend/apps/approvals/validators.py:5:    'dorm_manager': ApplicationStatus.PENDING_DORM_MANAGER,
backend/apps/approvals/validators.py:6:    'counselor': ApplicationStatus.PENDING_COUNSELOR,
backend/apps/approvals/admin.py:2:from .models import Approval
backend/apps/approvals/admin.py:5:@admin.register(Approval)
backend/apps/approvals/admin.py:6:class ApprovalAdmin(admin.ModelAdmin):
backend/apps/approvals/admin.py:7:    list_display = ['approval_id', 'application', 'step', 'approver', 'decision', 'decided_at']
backend/apps/approvals/admin.py:9:    search_fields = ['approval_id', 'application__application_id', 'approver__user_id']
backend/apps/approvals/pagination.py:5:class ApprovalLimitOffsetPagination(LimitOffsetPagination):
backend/apps/approvals/urls.py:7:    path('<str:approval_id>/approve/', views.approve_approval, name='approve_approval'),
backend/apps/approvals/urls.py:8:    path('<str:approval_id>/reject/', views.reject_approval, name='reject_approval'),
backend/apps/approvals/migrations/0002_initial.py:20:            name='approver',
backend/apps/approvals/migrations/0001_initial.py:17:            name='Approval',
backend/apps/approvals/migrations/0001_initial.py:21:                ('approver_name', models.CharField(max_length=100)),
backend/apps/approvals/migrations/0001_initial.py:22:                ('decision', models.CharField(choices=[('pending', '待审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='pending', max_length=20)),
backend/apps/approvals/tests/test_rejection_flow.py:8:from apps.applications.models import Application, ApplicationStatus
backend/apps/approvals/tests/test_rejection_flow.py:9:from apps.approvals.models import ApprovalDecision, ApprovalStep
backend/apps/approvals/tests/test_rejection_flow.py:64:            'contact_phone': '13800138000',
backend/apps/approvals/tests/test_rejection_flow.py:65:            'reason': '毕业离校',
backend/apps/approvals/tests/test_rejection_flow.py:66:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/approvals/tests/test_rejection_flow.py:71:    def _approve_dorm_manager_step(self, application):
backend/apps/approvals/tests/test_rejection_flow.py:78:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/approvals/tests/test_rejection_flow.py:81:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/approve/', {
backend/apps/approvals/tests/test_rejection_flow.py:86:    def test_dorm_manager_rejection(self):
backend/apps/approvals/tests/test_rejection_flow.py:97:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/approvals/tests/test_rejection_flow.py:100:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/reject/', {
backend/apps/approvals/tests/test_rejection_flow.py:104:        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)
backend/apps/approvals/tests/test_rejection_flow.py:107:        self.assertEqual(application.status, ApplicationStatus.REJECTED)
backend/apps/approvals/tests/test_rejection_flow.py:109:    def test_counselor_rejection(self):
backend/apps/approvals/tests/test_rejection_flow.py:113:        self._approve_dorm_manager_step(application)
backend/apps/approvals/tests/test_rejection_flow.py:115:        # Counselor login and reject
backend/apps/approvals/tests/test_rejection_flow.py:123:        counselor_approval = application.approvals.get(step=ApprovalStep.COUNSELOR)
backend/apps/approvals/tests/test_rejection_flow.py:126:        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/reject/', {
backend/apps/approvals/tests/test_rejection_flow.py:130:        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)
backend/apps/approvals/tests/test_rejection_flow.py:134:        self.assertEqual(application.status, ApplicationStatus.REJECTED)
backend/apps/approvals/tests/test_list_permissions.py:4:from apps.applications.models import Application, ApplicationStatus
backend/apps/approvals/tests/test_list_permissions.py:5:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_list_permissions.py:8:class ApprovalListPermissionTest(TestCase):
backend/apps/approvals/tests/test_list_permissions.py:47:            reason='测试',
backend/apps/approvals/tests/test_list_permissions.py:48:            leave_date='2024-07-01',
backend/apps/approvals/tests/test_list_permissions.py:49:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/approvals/tests/test_list_permissions.py:53:        self.approval_c1 = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:56:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/tests/test_list_permissions.py:57:            approver=self.counselor1,
backend/apps/approvals/tests/test_list_permissions.py:58:            approver_name='辅导员1',
backend/apps/approvals/tests/test_list_permissions.py:59:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_list_permissions.py:62:        self.approval_m1 = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:65:            step=ApprovalStep.DORM_MANAGER,
backend/apps/approvals/tests/test_list_permissions.py:66:            approver=self.dorm_manager1,
backend/apps/approvals/tests/test_list_permissions.py:67:            approver_name='宿管员1',
backend/apps/approvals/tests/test_list_permissions.py:68:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_list_permissions.py:115:    def test_decision_all_does_not_leak_cross_approver_data(self):
backend/apps/approvals/tests/test_list_permissions.py:116:        # Create second application and approval for counselor1 (approved)
backend/apps/approvals/tests/test_list_permissions.py:122:            reason='测试2',
backend/apps/approvals/tests/test_list_permissions.py:123:            leave_date='2024-07-02',
backend/apps/approvals/tests/test_list_permissions.py:124:            status=ApplicationStatus.APPROVED
backend/apps/approvals/tests/test_list_permissions.py:126:        approval_c1_approved = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:127:            approval_id='apv_c1_approved',
backend/apps/approvals/tests/test_list_permissions.py:129:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/tests/test_list_permissions.py:130:            approver=self.counselor1,
backend/apps/approvals/tests/test_list_permissions.py:131:            approver_name='辅导员1',
backend/apps/approvals/tests/test_list_permissions.py:132:            decision=ApprovalDecision.APPROVED
backend/apps/approvals/tests/test_list_permissions.py:141:            reason='测试3',
backend/apps/approvals/tests/test_list_permissions.py:142:            leave_date='2024-07-03',
backend/apps/approvals/tests/test_list_permissions.py:143:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/approvals/tests/test_list_permissions.py:145:        approval_c2 = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:148:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/tests/test_list_permissions.py:149:            approver=self.counselor2,
backend/apps/approvals/tests/test_list_permissions.py:150:            approver_name='辅导员2',
backend/apps/approvals/tests/test_list_permissions.py:151:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_list_permissions.py:163:        self.assertIn('apv_c1_approved', approval_ids)
backend/apps/approvals/tests/test_permissions.py:5:from apps.applications.models import Application, ApplicationStatus
backend/apps/approvals/tests/test_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_permissions.py:10:class ApprovalPermissionsTestCase(TestCase):
backend/apps/approvals/tests/test_permissions.py:98:            reason='测试原因',
backend/apps/approvals/tests/test_permissions.py:99:            leave_date='2024-06-30',
backend/apps/approvals/tests/test_permissions.py:100:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/approvals/tests/test_permissions.py:104:        self.approval1 = Approval.objects.create(
backend/apps/approvals/tests/test_permissions.py:107:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/tests/test_permissions.py:108:            approver=self.counselor1,
backend/apps/approvals/tests/test_permissions.py:109:            approver_name='李老师',
backend/apps/approvals/tests/test_permissions.py:110:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_permissions.py:116:        self.application1.status = ApplicationStatus.PENDING_DORM_MANAGER
backend/apps/approvals/tests/test_permissions.py:118:        return Approval.objects.create(
backend/apps/approvals/tests/test_permissions.py:121:            step=ApprovalStep.DORM_MANAGER,
backend/apps/approvals/tests/test_permissions.py:122:            approver=self.dorm_manager1,
backend/apps/approvals/tests/test_permissions.py:123:            approver_name='宿管员1',
backend/apps/approvals/tests/test_permissions.py:124:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_permissions.py:127:    def test_student_cannot_approve_or_reject(self):
backend/apps/approvals/tests/test_permissions.py:131:        approve_response = self.client.post(
backend/apps/approvals/tests/test_permissions.py:132:            f'/api/approvals/{self.approval1.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:136:        reject_response = self.client.post(
backend/apps/approvals/tests/test_permissions.py:137:            f'/api/approvals/{self.approval1.approval_id}/reject/',
backend/apps/approvals/tests/test_permissions.py:142:        self.assertEqual(approve_response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/approvals/tests/test_permissions.py:143:        self.assertEqual(reject_response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/approvals/tests/test_permissions.py:150:            f'/api/approvals/{self.approval1.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:163:            f'/api/approvals/{dorm_manager_approval.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:176:            f'/api/approvals/{dorm_manager_approval.approval_id}/reject/',
backend/apps/approvals/tests/test_permissions.py:183:    def test_cross_counselor_approve_forbidden(self):
backend/apps/approvals/tests/test_permissions.py:185:        # T002 tries to approve T001's application
backend/apps/approvals/tests/test_permissions.py:188:            f'/api/approvals/{self.approval1.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:194:    def test_cross_counselor_reject_forbidden(self):
backend/apps/approvals/tests/test_permissions.py:196:        # T002 tries to reject T001's application
backend/apps/approvals/tests/test_permissions.py:199:            f'/api/approvals/{self.approval1.approval_id}/reject/',
backend/apps/approvals/models.py:6:class ApprovalStep(models.TextChoices):
backend/apps/approvals/models.py:12:class ApprovalDecision(models.TextChoices):
backend/apps/approvals/models.py:14:    APPROVED = 'approved', '已通过'
backend/apps/approvals/models.py:15:    REJECTED = 'rejected', '已驳回'
backend/apps/approvals/models.py:18:class Approval(models.Model):
backend/apps/approvals/models.py:21:    step = models.CharField(max_length=20, choices=ApprovalStep.choices)
backend/apps/approvals/models.py:22:    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals')
backend/apps/approvals/models.py:23:    approver_name = models.CharField(max_length=100)
backend/apps/approvals/models.py:24:    decision = models.CharField(max_length=20, choices=ApprovalDecision.choices, default=ApprovalDecision.PENDING)
backend/apps/approvals/tests/test_state_machine.py:5:from apps.applications.models import Application, ApplicationStatus
backend/apps/approvals/tests/test_state_machine.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_state_machine.py:10:class ApprovalStateMachineTestCase(TestCase):
backend/apps/approvals/tests/test_state_machine.py:65:            reason='测试原因',
backend/apps/approvals/tests/test_state_machine.py:66:            leave_date='2024-06-30',
backend/apps/approvals/tests/test_state_machine.py:67:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/approvals/tests/test_state_machine.py:71:        self.approval = Approval.objects.create(
backend/apps/approvals/tests/test_state_machine.py:74:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/tests/test_state_machine.py:75:            approver=self.counselor,
backend/apps/approvals/tests/test_state_machine.py:76:            approver_name='李老师',
backend/apps/approvals/tests/test_state_machine.py:77:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_state_machine.py:88:            f'/api/approvals/{self.approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:96:            f'/api/approvals/{self.approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:102:    def test_reject_then_repeat_operation_conflict(self):
backend/apps/approvals/tests/test_state_machine.py:107:            f'/api/approvals/{self.approval.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:114:            f'/api/approvals/{self.approval.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:120:    def test_counselor_step_requires_pending_counselor_status(self):
backend/apps/approvals/tests/test_state_machine.py:122:        self.application.status = ApplicationStatus.PENDING_DORM_MANAGER
backend/apps/approvals/tests/test_state_machine.py:126:        approve_response = self.client.post(
backend/apps/approvals/tests/test_state_machine.py:127:            f'/api/approvals/{self.approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:131:        reject_response = self.client.post(
backend/apps/approvals/tests/test_state_machine.py:132:            f'/api/approvals/{self.approval.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:137:        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_state_machine.py:138:        self.assertEqual(reject_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_state_machine.py:140:    def test_dorm_manager_step_requires_pending_dorm_manager_status(self):
backend/apps/approvals/tests/test_state_machine.py:142:        self.application.status = ApplicationStatus.APPROVED
backend/apps/approvals/tests/test_state_machine.py:144:        dorm_manager_approval = Approval.objects.create(
backend/apps/approvals/tests/test_state_machine.py:147:            step=ApprovalStep.DORM_MANAGER,
backend/apps/approvals/tests/test_state_machine.py:148:            approver=self.dorm_manager,
backend/apps/approvals/tests/test_state_machine.py:149:            approver_name='宿管员',
backend/apps/approvals/tests/test_state_machine.py:150:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_state_machine.py:154:        approve_response = self.client.post(
backend/apps/approvals/tests/test_state_machine.py:155:            f'/api/approvals/{dorm_manager_approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:159:        reject_response = self.client.post(
backend/apps/approvals/tests/test_state_machine.py:160:            f'/api/approvals/{dorm_manager_approval.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:165:        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_state_machine.py:166:        self.assertEqual(reject_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/views.py:9:from .models import Approval, ApprovalDecision, ApprovalStep
backend/apps/approvals/views.py:10:from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalListSerializer, ApprovalListResponseSerializer
backend/apps/approvals/views.py:11:from .pagination import ApprovalLimitOffsetPagination
backend/apps/approvals/views.py:13:from apps.applications.models import Application, ApplicationStatus
backend/apps/approvals/views.py:25:        OpenApiParameter('decision', str, description='决策过滤：pending/approved/rejected/all（默认pending）'),
backend/apps/approvals/views.py:30:        200: ApprovalListResponseSerializer,
backend/apps/approvals/views.py:49:        queryset = Approval.objects.filter(
backend/apps/approvals/views.py:50:            approver=user,
backend/apps/approvals/views.py:51:            step=ApprovalStep.DORM_MANAGER
backend/apps/approvals/views.py:52:        ).select_related('application', 'approver')
backend/apps/approvals/views.py:56:        queryset = Approval.objects.filter(
backend/apps/approvals/views.py:57:            approver=user,
backend/apps/approvals/views.py:58:            step=ApprovalStep.COUNSELOR
backend/apps/approvals/views.py:59:        ).select_related('application', 'approver')
backend/apps/approvals/views.py:63:        queryset = Approval.objects.all().select_related('application', 'approver')
backend/apps/approvals/views.py:80:    paginator = ApprovalLimitOffsetPagination()
backend/apps/approvals/views.py:84:    serializer = ApprovalListSerializer(page, many=True)
backend/apps/approvals/views.py:94:        200: ApprovalSerializer,
backend/apps/approvals/views.py:104:        approval = Approval.objects.select_related('application', 'approver').get(approval_id=approval_id)
backend/apps/approvals/views.py:105:    except Approval.DoesNotExist:
backend/apps/approvals/views.py:111:    # Permission check: only the approver or dean can view this approval
backend/apps/approvals/views.py:112:    if user.role == UserRole.DEAN or approval.approver_id == user.user_id:
backend/apps/approvals/views.py:113:        return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:120:    operation_id='approvals_approve',
backend/apps/approvals/views.py:123:    request=ApprovalActionSerializer,
backend/apps/approvals/views.py:125:        200: ApprovalSerializer,
backend/apps/approvals/views.py:136:def approve_approval(request, approval_id):
backend/apps/approvals/views.py:138:        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
backend/apps/approvals/views.py:139:    except Approval.DoesNotExist:
backend/apps/approvals/views.py:144:    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
backend/apps/approvals/views.py:147:    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
backend/apps/approvals/views.py:150:    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
backend/apps/approvals/views.py:154:    if approval.approver_id != user.user_id:
backend/apps/approvals/views.py:158:    if approval.decision != ApprovalDecision.PENDING:
backend/apps/approvals/views.py:166:    serializer = ApprovalActionSerializer(data=request.data)
backend/apps/approvals/views.py:171:    approval.decision = ApprovalDecision.APPROVED
backend/apps/approvals/views.py:179:    if approval.step == ApprovalStep.DORM_MANAGER:
backend/apps/approvals/views.py:181:        # (New requirement: any dorm manager in the building can approve, others see "already approved")
backend/apps/approvals/views.py:182:        other_dorm_approvals = Approval.objects.filter(
backend/apps/approvals/views.py:184:            step=ApprovalStep.DORM_MANAGER,
backend/apps/approvals/views.py:185:            decision=ApprovalDecision.PENDING
backend/apps/approvals/views.py:190:                decision=ApprovalDecision.APPROVED,
backend/apps/approvals/views.py:191:                comment=f'已由{approval.approver_name}完成审批，无需重复操作',
backend/apps/approvals/views.py:196:                f"for application {application.application_id} after approval by {approval.approver.user_id}"
backend/apps/approvals/views.py:200:        existing_counselor_approval = Approval.objects.filter(
backend/apps/approvals/views.py:202:            step=ApprovalStep.COUNSELOR
backend/apps/approvals/views.py:209:        application.status = ApplicationStatus.PENDING_COUNSELOR
backend/apps/approvals/views.py:236:        Approval.objects.create(
backend/apps/approvals/views.py:239:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/views.py:240:            approver=counselor,
backend/apps/approvals/views.py:241:            approver_name=counselor.name,
backend/apps/approvals/views.py:242:            decision=ApprovalDecision.PENDING
backend/apps/approvals/views.py:244:    elif approval.step == ApprovalStep.COUNSELOR:
backend/apps/approvals/views.py:246:        application.status = ApplicationStatus.APPROVED
backend/apps/approvals/views.py:249:    return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:253:    operation_id='approvals_reject',
backend/apps/approvals/views.py:256:    request=ApprovalActionSerializer,
backend/apps/approvals/views.py:258:        200: ApprovalSerializer,
backend/apps/approvals/views.py:269:def reject_approval(request, approval_id):
backend/apps/approvals/views.py:271:        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
backend/apps/approvals/views.py:272:    except Approval.DoesNotExist:
backend/apps/approvals/views.py:277:    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
backend/apps/approvals/views.py:280:    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
backend/apps/approvals/views.py:283:    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
backend/apps/approvals/views.py:287:    if approval.approver_id != user.user_id:
backend/apps/approvals/views.py:291:    if approval.decision != ApprovalDecision.PENDING:
backend/apps/approvals/views.py:299:    serializer = ApprovalActionSerializer(data=request.data)
backend/apps/approvals/views.py:304:    approval.decision = ApprovalDecision.REJECTED
backend/apps/approvals/views.py:312:    application.status = ApplicationStatus.REJECTED
backend/apps/approvals/views.py:315:    return Response(ApprovalSerializer(approval).data)
backend/apps/applications/admin.py:6:class ApplicationAdmin(admin.ModelAdmin):
backend/apps/attachments/urls.py:5:    path('applications/<str:application_id>/attachments/', views.attachments_view, name='attachments'),
backend/apps/attachments/urls.py:6:    path('attachments/<str:attachment_id>/download/', views.download_attachment, name='download_attachment'),
backend/apps/attachments/urls.py:7:    path('attachments/<str:attachment_id>/', views.delete_attachment, name='delete_attachment'),
backend/apps/applications/providers.py:11:    blocking_reason: Optional[str]
backend/apps/applications/providers.py:22:                blocking_reason=None,
backend/apps/applications/providers.py:29:                blocking_reason=None,
backend/apps/applications/providers.py:36:                blocking_reason="未提交清退申请",
backend/apps/applications/providers.py:43:                blocking_reason=None,
backend/apps/applications/providers.py:50:                blocking_reason="学生信息不存在",
backend/apps/applications/providers.py:57:                blocking_reason=None,
backend/apps/applications/providers.py:64:                blocking_reason=None,
backend/apps/applications/providers.py:71:                blocking_reason=None,
backend/apps/applications/providers.py:78:                blocking_reason=None,
backend/apps/applications/providers.py:85:                blocking_reason=None,
backend/apps/applications/providers.py:92:                blocking_reason=None,
backend/apps/applications/providers.py:99:                blocking_reason=None,
backend/apps/applications/providers.py:108:            blocking_reason="未在宿舍系统中找到记录",
backend/apps/applications/pagination.py:5:class ApplicationLimitOffsetPagination(LimitOffsetPagination):
backend/apps/attachments/migrations/0001_initial.py:22:                ('file', models.FileField(upload_to='attachments/%Y/%m/%d/')),
backend/apps/attachments/migrations/0001_initial.py:23:                ('attachment_type', models.CharField(choices=[('dorm_checkout', '宿舍清退证明'), ('library_clearance', '图书馆清书证明'), ('finance_clearance', '财务结清证明'), ('other', '其他')], max_length=50)),
backend/apps/attachments/migrations/0001_initial.py:30:                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='applications.application')),
backend/apps/attachments/migrations/0001_initial.py:34:                'db_table': 'attachments',
backend/apps/users/integrations/xg_user_client.py:199:                return {'users': all_users, 'total': total, 'pages_fetched': page, 'stopped_reason': 'max_pages'}
backend/apps/users/integrations/xg_user_client.py:202:                return {'users': all_users, 'total': total, 'pages_fetched': page, 'stopped_reason': 'empty'}
backend/apps/users/integrations/xg_user_client.py:207:                    return {'users': all_users, 'total': total, 'pages_fetched': page, 'stopped_reason': 'complete'}
backend/apps/approvals/serializers.py:2:from .models import Approval
backend/apps/approvals/serializers.py:5:class ApprovalListSerializer(serializers.ModelSerializer):
backend/apps/approvals/serializers.py:8:    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
backend/apps/approvals/serializers.py:11:        model = Approval
backend/apps/approvals/serializers.py:12:        fields = ['approval_id', 'application_id', 'step', 'approver_id',
backend/apps/approvals/serializers.py:13:                  'approver_name', 'decision', 'created_at']
backend/apps/approvals/serializers.py:15:                            'approver_id', 'approver_name', 'decision', 'created_at']
backend/apps/approvals/serializers.py:18:class ApprovalSerializer(serializers.ModelSerializer):
backend/apps/approvals/serializers.py:20:    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
backend/apps/approvals/serializers.py:23:        model = Approval
backend/apps/approvals/serializers.py:24:        fields = ['approval_id', 'application_id', 'step', 'approver_id',
backend/apps/approvals/serializers.py:25:                  'approver_name', 'decision', 'comment', 'decided_at']
backend/apps/approvals/serializers.py:27:                            'approver_id', 'approver_name', 'decision', 'decided_at']
backend/apps/approvals/serializers.py:30:class ApprovalActionSerializer(serializers.Serializer):
backend/apps/approvals/serializers.py:34:class ApprovalListResponseSerializer(serializers.Serializer):
backend/apps/approvals/serializers.py:37:    results = ApprovalListSerializer(many=True)
backend/apps/attachments/tests/test_list.py:7:from apps.applications.models import Application, ApplicationStatus
backend/apps/attachments/tests/test_list.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_list.py:86:            reason='毕业离校',
backend/apps/attachments/tests/test_list.py:87:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_list.py:88:            status=ApplicationStatus.APPROVED
backend/apps/attachments/tests/test_list.py:97:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_list.py:104:        """Student can list own application attachments"""
backend/apps/attachments/tests/test_list.py:108:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:112:        self.assertEqual(len(response.data['attachments']), 1)
backend/apps/attachments/tests/test_list.py:113:        self.assertEqual(response.data['attachments'][0]['attachment_id'], 'att_test001')
backend/apps/attachments/tests/test_list.py:116:        """Student cannot list another student's attachments"""
backend/apps/attachments/tests/test_list.py:120:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:127:        """Assigned counselor can list application attachments"""
backend/apps/attachments/tests/test_list.py:131:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:135:        self.assertEqual(len(response.data['attachments']), 1)
backend/apps/attachments/tests/test_list.py:138:        """Cross-counselor cannot list application attachments"""
backend/apps/attachments/tests/test_list.py:142:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:149:        """Dean can list approved application attachments for archiving"""
backend/apps/attachments/tests/test_list.py:153:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:157:        self.assertEqual(len(response.data['attachments']), 1)
backend/apps/attachments/tests/test_list.py:160:        """List excludes soft-deleted attachments"""
backend/apps/attachments/tests/test_list.py:168:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:172:        self.assertEqual(len(response.data['attachments']), 0)
backend/apps/users/integrations/xg_user_mapper.py:22:            'skip_reason': str | None  # 如果应跳过，说明原因
backend/apps/users/integrations/xg_user_mapper.py:35:        'skip_reason': None
backend/apps/users/integrations/xg_user_mapper.py:61:        result['skip_reason'] = 'missing_user_id'
backend/apps/users/integrations/xg_user_mapper.py:66:        result['skip_reason'] = 'missing_name'
backend/apps/users/integrations/xg_user_mapper.py:81:                result['skip_reason'] = f'unknown_user_identity: name={identity_name}, id={identity_id}'
backend/apps/users/integrations/xg_user_mapper.py:91:                result['skip_reason'] = f'unknown_user_identity: {user_identity_str}'
backend/apps/users/integrations/xg_user_mapper.py:96:        result['skip_reason'] = 'missing_user_identity'
backend/apps/applications/migrations/0001_initial.py:20:                ('reason', models.TextField()),
backend/apps/applications/migrations/0001_initial.py:21:                ('leave_date', models.DateField()),
backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
backend/apps/attachments/tests/test_delete.py:7:from apps.applications.models import Application, ApplicationStatus
backend/apps/attachments/tests/test_delete.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_delete.py:63:            reason='毕业离校',
backend/apps/attachments/tests/test_delete.py:64:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_delete.py:65:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/attachments/tests/test_delete.py:75:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_delete.py:86:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:101:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:116:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:130:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/users/tests/test_xg_user_mapper.py:31:        self.assertIsNone(result['skip_reason'])
backend/apps/users/tests/test_xg_user_mapper.py:44:        self.assertIsNone(result['skip_reason'])
backend/apps/users/tests/test_xg_user_mapper.py:56:        self.assertEqual(result['skip_reason'], 'missing_user_id')
backend/apps/users/tests/test_xg_user_mapper.py:70:        self.assertEqual(result['skip_reason'], 'missing_name')
backend/apps/users/tests/test_xg_user_mapper.py:85:        self.assertEqual(result['skip_reason'], 'unknown_user_identity: 999')
backend/apps/users/tests/test_xg_user_mapper.py:99:        self.assertEqual(result['skip_reason'], 'missing_user_identity')
backend/apps/users/tests/test_xg_user_mapper.py:116:        self.assertIsNone(result['skip_reason'])
backend/apps/users/tests/test_xg_user_mapper.py:125:        self.assertEqual(result['skip_reason'], 'missing_user_id')
backend/apps/users/tests/test_xg_user_mapper.py:144:        self.assertIsNone(result['skip_reason'])
backend/apps/users/tests/test_xg_user_mapper.py:162:        self.assertIsNone(result['skip_reason'])
backend/apps/users/tests/test_xg_user_mapper.py:176:        self.assertIsNone(result['skip_reason'])
backend/apps/users/tests/test_xg_user_mapper.py:190:        self.assertIsNone(result['skip_reason'])
backend/apps/applications/migrations/0006_application_contact_phone_and_more.py:15:            name='contact_phone',
backend/apps/applications/migrations/0006_application_contact_phone_and_more.py:20:            name='leave_date',
backend/apps/applications/migrations/0006_application_contact_phone_and_more.py:25:            name='reason',
backend/apps/applications/migrations/0006_application_contact_phone_and_more.py:31:            field=models.CharField(choices=[('draft', '草稿'), ('pending_dorm_manager', '待宿管员审批'), ('pending_counselor', '待辅导员审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20),
backend/apps/attachments/views.py:12:from apps.approvals.models import Approval, ApprovalStep
backend/apps/attachments/views.py:21:    operation_id='attachments_list',
backend/apps/attachments/views.py:33:    operation_id='attachments_upload',
backend/apps/attachments/views.py:48:def attachments_view(request, application_id):
backend/apps/attachments/views.py:51:        return list_attachments(request, application_id)
backend/apps/attachments/views.py:85:        attachment_type=serializer.validated_data['attachment_type'],
backend/apps/attachments/views.py:94:def list_attachments(request, application_id):
backend/apps/attachments/views.py:109:    # List attachments (exclude soft-deleted)
backend/apps/attachments/views.py:110:    attachments = Attachment.objects.filter(application=application, is_deleted=False)
backend/apps/attachments/views.py:111:    serializer = AttachmentSerializer(attachments, many=True)
backend/apps/attachments/views.py:112:    return Response({'attachments': serializer.data})
backend/apps/attachments/views.py:116:    operation_id='attachments_download',
backend/apps/attachments/views.py:158:    operation_id='attachments_delete',
backend/apps/applications/migrations/0005_alter_application_status.py:16:            field=models.CharField(choices=[('draft', '草稿'), ('pending_dorm_manager', '待宿管员审批'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20),
backend/apps/users/tests/test_xg_user_client.py:258:        self.assertEqual(result['stopped_reason'], 'complete')
backend/apps/users/tests/test_xg_user_client.py:284:        self.assertEqual(result['stopped_reason'], 'complete')
backend/apps/users/tests/test_xg_user_client.py:302:        self.assertEqual(result['stopped_reason'], 'empty')
backend/apps/users/tests/test_xg_user_client.py:347:        self.assertEqual(result['stopped_reason'], 'complete')
backend/apps/users/tests/test_xg_user_client.py:395:        self.assertEqual(result['stopped_reason'], 'max_pages')
backend/apps/users/tests/test_xg_user_client.py:521:        self.assertEqual(result['stopped_reason'], 'complete')
backend/apps/attachments/tests/test_upload.py:7:from apps.applications.models import Application, ApplicationStatus
backend/apps/attachments/tests/test_upload.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_upload.py:64:            reason='毕业离校',
backend/apps/attachments/tests/test_upload.py:65:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_upload.py:66:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/attachments/tests/test_upload.py:75:            reason='毕业离校',
backend/apps/attachments/tests/test_upload.py:76:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_upload.py:77:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/attachments/tests/test_upload.py:86:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:89:                'attachment_type': AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_upload.py:99:        self.assertEqual(response.data['attachment_type'], AttachmentType.DORM_CHECKOUT)
backend/apps/attachments/tests/test_upload.py:108:            f'/api/applications/{self.other_application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:111:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:120:        """Counselor cannot upload attachments"""
backend/apps/attachments/tests/test_upload.py:125:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:128:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:141:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:143:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:154:        """Upload fails with missing attachment_type"""
backend/apps/attachments/tests/test_upload.py:159:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:169:        self.assertIn('attachment_type', response.data['error']['details'])
backend/apps/users/tests/test_xg_user_sync.py:46:        self.assertGreater(len(result['skipped_by_reason']), 0)
backend/apps/users/tests/test_xg_user_sync.py:47:        # 验证统计了不同的skip_reason
backend/apps/users/tests/test_xg_user_sync.py:48:        self.assertIn('missing_user_id', result['skipped_by_reason'])
backend/apps/users/tests/test_xg_user_sync.py:49:        self.assertIn('missing_name', result['skipped_by_reason'])
backend/apps/users/tests/test_xg_user_sync.py:119:        self.assertEqual(conflict['reason'], 'role_mismatch')
backend/apps/users/tests/test_xg_user_sync.py:190:            # skip - 未知身份（不同reason）
backend/apps/users/tests/test_xg_user_sync.py:213:        # 验证多个skip_reason统计
backend/apps/users/tests/test_xg_user_sync.py:214:        self.assertEqual(len(result['skipped_by_reason']), 2)
backend/apps/users/tests/test_xg_user_sync.py:269:    def test_scenario2_skip_mapper_skip_reason(self):
backend/apps/users/tests/test_xg_user_sync.py:270:        """场景2：跳过mapper标记skip_reason的用户"""
backend/apps/users/tests/test_xg_user_sync.py:280:        self.assertIn('missing_user_id', result['skipped_by_reason'])
backend/apps/users/tests/test_xg_user_sync.py:290:        self.assertEqual(result['conflicts'][0]['reason'], 'role_mismatch')
backend/apps/applications/serializers.py:5:class ApplicationListSerializer(serializers.ModelSerializer):
backend/apps/applications/serializers.py:12:                  'contact_phone', 'reason', 'leave_date', 'status', 'created_at', 'updated_at']
backend/apps/applications/serializers.py:17:class ApplicationSerializer(serializers.ModelSerializer):
backend/apps/applications/serializers.py:24:                  'contact_phone', 'reason', 'leave_date', 'status', 'dorm_checkout_status',
backend/apps/applications/serializers.py:31:        from apps.approvals.serializers import ApprovalSerializer
backend/apps/applications/serializers.py:32:        return ApprovalSerializer(obj.approvals.all(), many=True).data
backend/apps/applications/serializers.py:35:class ApplicationCreateSerializer(serializers.Serializer):
backend/apps/applications/serializers.py:36:    contact_phone = serializers.CharField(max_length=20, required=True)
backend/apps/applications/serializers.py:37:    reason = serializers.CharField(max_length=500, required=False, allow_blank=True, default='')
backend/apps/applications/serializers.py:38:    leave_date = serializers.DateField()
backend/apps/applications/serializers.py:40:    def validate_leave_date(self, value):
backend/apps/applications/serializers.py:48:class ApplicationListResponseSerializer(serializers.Serializer):
backend/apps/users/management/commands/sync_xg_users.py:57:        if result['skipped_by_reason']:
backend/apps/users/management/commands/sync_xg_users.py:58:            self.stdout.write('\nSkip reasons:')
backend/apps/users/management/commands/sync_xg_users.py:59:            for reason, count in result['skipped_by_reason'].items():
backend/apps/users/management/commands/sync_xg_users.py:60:                self.stdout.write(f'  {reason}: {count}')
backend/apps/applications/models.py:6:class ApplicationStatus(models.TextChoices):
backend/apps/applications/models.py:8:    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
backend/apps/applications/models.py:9:    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
backend/apps/applications/models.py:10:    APPROVED = 'approved', '已通过'
backend/apps/applications/models.py:11:    REJECTED = 'rejected', '已驳回'
backend/apps/applications/models.py:21:class Application(models.Model):
backend/apps/applications/models.py:26:    contact_phone = models.CharField(max_length=20, null=True, blank=True)
backend/apps/applications/models.py:27:    reason = models.TextField(blank=True, default='')
backend/apps/applications/models.py:28:    leave_date = models.DateField(null=True, blank=True)
backend/apps/applications/models.py:29:    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT)
backend/apps/applications/models.py:39:            ApplicationStatus.PENDING_DORM_MANAGER,
backend/apps/applications/models.py:40:            ApplicationStatus.PENDING_COUNSELOR,
backend/apps/applications/models.py:41:            ApplicationStatus.APPROVED,
backend/apps/users/management/commands/import_students.py:34:            active_apps = Application.objects.exclude(status='rejected').count()
backend/apps/attachments/tests/test_download.py:7:from apps.applications.models import Application, ApplicationStatus
backend/apps/attachments/tests/test_download.py:8:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/attachments/tests/test_download.py:9:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_download.py:64:            reason='毕业离校',
backend/apps/attachments/tests/test_download.py:65:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_download.py:66:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/attachments/tests/test_download.py:76:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_download.py:87:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:98:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:108:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:122:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/applications/tests/test_constraints.py:7:from apps.applications.models import Application, ApplicationStatus
backend/apps/applications/tests/test_constraints.py:11:class ApplicationConstraintsTestCase(TestCase):
backend/apps/applications/tests/test_constraints.py:62:                'contact_phone': '13800138000',
backend/apps/applications/tests/test_constraints.py:63:                'reason': '毕业离校',
backend/apps/applications/tests/test_constraints.py:64:                'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_constraints.py:74:                'contact_phone': '13800138000',
backend/apps/applications/tests/test_constraints.py:75:                'reason': '再次提交',
backend/apps/applications/tests/test_constraints.py:76:                'leave_date': (timezone.now().date() + timedelta(days=2)).isoformat()
backend/apps/applications/tests/test_p0_fixes.py:3:from apps.applications.models import Application, ApplicationStatus
backend/apps/applications/tests/test_p0_fixes.py:4:from apps.approvals.models import Approval, ApprovalDecision, ApprovalStep
backend/apps/applications/tests/test_p0_fixes.py:30:    def test_can_resubmit_after_rejection(self):
backend/apps/applications/tests/test_p0_fixes.py:31:        # Create and reject first application
backend/apps/applications/tests/test_p0_fixes.py:37:            reason='First attempt',
backend/apps/applications/tests/test_p0_fixes.py:38:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:39:            status=ApplicationStatus.REJECTED
backend/apps/applications/tests/test_p0_fixes.py:42:        # Should be able to create second application after rejection
backend/apps/applications/tests/test_p0_fixes.py:48:            reason='Second attempt',
backend/apps/applications/tests/test_p0_fixes.py:49:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:50:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:54:        self.assertEqual(app2.status, ApplicationStatus.PENDING_COUNSELOR)
backend/apps/applications/tests/test_p0_fixes.py:63:            reason='First attempt',
backend/apps/applications/tests/test_p0_fixes.py:64:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:65:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:74:            reason='Second attempt',
backend/apps/applications/tests/test_p0_fixes.py:75:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:76:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:84:class ApprovalDecisionFilterTest(TestCase):
backend/apps/applications/tests/test_p0_fixes.py:104:            reason='Pending',
backend/apps/applications/tests/test_p0_fixes.py:105:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:106:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:109:        self.app_approved = Application.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:110:            application_id='app_approved',
backend/apps/applications/tests/test_p0_fixes.py:114:            reason='Approved',
backend/apps/applications/tests/test_p0_fixes.py:115:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:116:            status=ApplicationStatus.APPROVED
backend/apps/applications/tests/test_p0_fixes.py:119:        self.app_rejected = Application.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:120:            application_id='app_rejected',
backend/apps/applications/tests/test_p0_fixes.py:124:            reason='Rejected',
backend/apps/applications/tests/test_p0_fixes.py:125:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:126:            status=ApplicationStatus.REJECTED
backend/apps/applications/tests/test_p0_fixes.py:130:        self.approval_pending = Approval.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:133:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/tests/test_p0_fixes.py:134:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:135:            approver_name=self.counselor.name,
backend/apps/applications/tests/test_p0_fixes.py:136:            decision=ApprovalDecision.PENDING
backend/apps/applications/tests/test_p0_fixes.py:139:        self.approval_approved = Approval.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:140:            approval_id='apv_approved',
backend/apps/applications/tests/test_p0_fixes.py:141:            application=self.app_approved,
backend/apps/applications/tests/test_p0_fixes.py:142:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/tests/test_p0_fixes.py:143:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:144:            approver_name=self.counselor.name,
backend/apps/applications/tests/test_p0_fixes.py:145:            decision=ApprovalDecision.APPROVED
backend/apps/applications/tests/test_p0_fixes.py:148:        self.approval_rejected = Approval.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:149:            approval_id='apv_rejected',
backend/apps/applications/tests/test_p0_fixes.py:150:            application=self.app_rejected,
backend/apps/applications/tests/test_p0_fixes.py:151:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/tests/test_p0_fixes.py:152:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:153:            approver_name=self.counselor.name,
backend/apps/applications/tests/test_p0_fixes.py:154:            decision=ApprovalDecision.REJECTED
backend/apps/applications/tests/test_p0_fixes.py:158:        approvals = Approval.objects.filter(
backend/apps/applications/tests/test_p0_fixes.py:159:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:160:            decision=ApprovalDecision.PENDING
backend/apps/applications/tests/test_p0_fixes.py:165:    def test_filter_approved_approvals(self):
backend/apps/applications/tests/test_p0_fixes.py:166:        approvals = Approval.objects.filter(
backend/apps/applications/tests/test_p0_fixes.py:167:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:168:            decision=ApprovalDecision.APPROVED
backend/apps/applications/tests/test_p0_fixes.py:171:        self.assertEqual(approvals.first().approval_id, 'apv_approved')
backend/apps/applications/tests/test_p0_fixes.py:173:    def test_filter_rejected_approvals(self):
backend/apps/applications/tests/test_p0_fixes.py:174:        approvals = Approval.objects.filter(
backend/apps/applications/tests/test_p0_fixes.py:175:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:176:            decision=ApprovalDecision.REJECTED
backend/apps/applications/tests/test_p0_fixes.py:179:        self.assertEqual(approvals.first().approval_id, 'apv_rejected')
backend/apps/applications/tests/test_p0_fixes.py:182:        approvals = Approval.objects.filter(approver=self.counselor)
backend/apps/users/services/xg_user_sync.py:21:            'skipped_by_reason': dict,
backend/apps/users/services/xg_user_sync.py:33:        'skipped_by_reason': {},
backend/apps/users/services/xg_user_sync.py:45:        if mapped['skip_reason']:
backend/apps/users/services/xg_user_sync.py:47:            reason = mapped['skip_reason']
backend/apps/users/services/xg_user_sync.py:48:            result['skipped_by_reason'][reason] = result['skipped_by_reason'].get(reason, 0) + 1
backend/apps/users/services/xg_user_sync.py:65:                    'reason': 'role_mismatch',
backend/apps/users/services/xg_user_sync.py:83:            "until User model adds phone/email/department or name overwrite policy is approved"
backend/apps/users/services/xg_user_sync.py:102:            'skipped_by_reason': dict,
backend/apps/users/services/xg_user_sync.py:114:        'skipped_by_reason': {},
backend/apps/users/services/xg_user_sync.py:125:        if mapped['skip_reason']:
backend/apps/users/services/xg_user_sync.py:127:            reason = mapped['skip_reason']
backend/apps/users/services/xg_user_sync.py:128:            result['skipped_by_reason'][reason] = result['skipped_by_reason'].get(reason, 0) + 1
backend/apps/users/services/xg_user_sync.py:141:                    'reason': 'role_mismatch',
backend/apps/users/management/commands/seed_data.py:19:            from apps.approvals.models import Approval
backend/apps/users/management/commands/seed_data.py:20:            Approval.objects.all().delete()
backend/apps/applications/tests/test_detail_permissions.py:5:from apps.applications.models import Application, ApplicationStatus
backend/apps/applications/tests/test_detail_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/applications/tests/test_detail_permissions.py:10:class ApplicationDetailPermissionTest(TestCase):
backend/apps/applications/tests/test_detail_permissions.py:57:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_detail_permissions.py:58:            'reason': '测试',
backend/apps/applications/tests/test_detail_permissions.py:59:            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_detail_permissions.py:74:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_detail_permissions.py:75:            'reason': '测试',
backend/apps/applications/tests/test_detail_permissions.py:76:            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_detail_permissions.py:91:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_detail_permissions.py:92:            'reason': '测试',
backend/apps/applications/tests/test_detail_permissions.py:93:            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
backend/apps/attachments/models.py:15:    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='attachments')
backend/apps/attachments/models.py:17:    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
backend/apps/attachments/models.py:18:    attachment_type = models.CharField(max_length=50, choices=AttachmentType.choices)
backend/apps/attachments/models.py:27:        db_table = 'attachments'
backend/apps/attachments/serializers.py:7:    attachment_type = serializers.ChoiceField(choices=AttachmentType.choices)
backend/apps/attachments/serializers.py:26:        fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'attachment_type', 'uploaded_at']
backend/apps/attachments/serializers.py:32:    attachments = AttachmentSerializer(many=True)
backend/apps/applications/tests/test_serializer_validation.py:8:class ApplicationCreateSerializerTest(TestCase):
backend/apps/applications/tests/test_serializer_validation.py:9:    def test_reason_max_length_500(self):
backend/apps/applications/tests/test_serializer_validation.py:10:        """Test reason field enforces 500 character limit"""
backend/apps/applications/tests/test_serializer_validation.py:12:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:13:            'reason': 'a' * 501,
backend/apps/applications/tests/test_serializer_validation.py:14:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:18:        self.assertIn('reason', serializer.errors)
backend/apps/applications/tests/test_serializer_validation.py:20:    def test_reason_empty_after_trim(self):
backend/apps/applications/tests/test_serializer_validation.py:21:        """Test reason field rejects empty string after trim"""
backend/apps/applications/tests/test_serializer_validation.py:23:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:24:            'reason': '   ',
backend/apps/applications/tests/test_serializer_validation.py:25:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:31:    def test_leave_date_past(self):
backend/apps/applications/tests/test_serializer_validation.py:32:        """Test leave_date field rejects dates before today"""
backend/apps/applications/tests/test_serializer_validation.py:34:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:35:            'reason': '毕业离校',
backend/apps/applications/tests/test_serializer_validation.py:36:            'leave_date': (timezone.now().date() - timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:40:        self.assertIn('leave_date', serializer.errors)
backend/apps/applications/tests/test_serializer_validation.py:42:    def test_leave_date_today(self):
backend/apps/applications/tests/test_serializer_validation.py:43:        """Test leave_date field accepts today"""
backend/apps/applications/tests/test_serializer_validation.py:45:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:46:            'reason': '毕业离校',
backend/apps/applications/tests/test_serializer_validation.py:47:            'leave_date': timezone.now().date().isoformat()
backend/apps/applications/tests/test_serializer_validation.py:55:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:56:            'reason': '毕业离校',
backend/apps/applications/tests/test_serializer_validation.py:57:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:61:        self.assertEqual(serializer.validated_data['reason'], '毕业离校')
backend/apps/applications/tests/test_serializer_validation.py:64:    def test_leave_date_validation_at_midnight_boundary(self, mock_now):
backend/apps/applications/tests/test_serializer_validation.py:65:        """Test leave_date validation at 23:59:59 boundary"""
backend/apps/applications/tests/test_serializer_validation.py:72:        # Submit with leave_date=tomorrow (2026-06-02)
backend/apps/applications/tests/test_serializer_validation.py:74:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:75:            'reason': '毕业离校',
backend/apps/applications/tests/test_serializer_validation.py:76:            'leave_date': '2026-06-02'
backend/apps/applications/tests/test_serializer_validation.py:82:    def test_leave_date_validation_after_midnight(self, mock_now):
backend/apps/applications/tests/test_serializer_validation.py:83:        """Test leave_date validation rejects past date after midnight"""
backend/apps/applications/tests/test_serializer_validation.py:90:        # Submit with leave_date=yesterday (2026-06-01)
backend/apps/applications/tests/test_serializer_validation.py:92:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:93:            'reason': '毕业离校',
backend/apps/applications/tests/test_serializer_validation.py:94:            'leave_date': '2026-06-01'
backend/apps/applications/tests/test_serializer_validation.py:98:        self.assertIn('leave_date', serializer.errors)
backend/apps/applications/permissions.py:2:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/applications/permissions.py:6:    """Check if user can view application and its attachments."""
backend/apps/applications/permissions.py:24:        return application.status == 'approved'
backend/apps/applications/views.py:7:from .models import Application, ApplicationStatus, DormCheckoutStatus
backend/apps/applications/views.py:12:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/applications/views.py:70:        pending_approvals = Approval.objects.filter(
backend/apps/applications/views.py:71:            approver=user,
backend/apps/applications/views.py:72:            step=ApprovalStep.DORM_MANAGER,
backend/apps/applications/views.py:73:            decision=ApprovalDecision.PENDING
backend/apps/applications/views.py:79:        pending_approvals = Approval.objects.filter(
backend/apps/applications/views.py:80:            approver=user,
backend/apps/applications/views.py:81:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/views.py:82:            decision=ApprovalDecision.PENDING
backend/apps/applications/views.py:86:    # Dean: view all approved applications (archiving role)
backend/apps/applications/views.py:88:        queryset = Application.objects.filter(status=ApplicationStatus.APPROVED)
backend/apps/applications/views.py:134:        # Check for existing pending/approved applications
backend/apps/applications/views.py:137:            status__in=[ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.APPROVED]
backend/apps/applications/views.py:150:                                                    'blocking_reason': dorm_status.blocking_reason}}},
backend/apps/applications/views.py:176:        draft = Application.objects.select_for_update().filter(student=user, status=ApplicationStatus.DRAFT).first()
backend/apps/applications/views.py:180:            draft.contact_phone = serializer.validated_data['contact_phone']
backend/apps/applications/views.py:181:            draft.reason = serializer.validated_data.get('reason', '')
backend/apps/applications/views.py:182:            draft.leave_date = serializer.validated_data['leave_date']
backend/apps/applications/views.py:183:            draft.status = ApplicationStatus.PENDING_DORM_MANAGER
backend/apps/applications/views.py:194:                contact_phone=serializer.validated_data['contact_phone'],
backend/apps/applications/views.py:195:                reason=serializer.validated_data.get('reason', ''),
backend/apps/applications/views.py:196:                leave_date=serializer.validated_data['leave_date'],
backend/apps/applications/views.py:197:                status=ApplicationStatus.PENDING_DORM_MANAGER,
backend/apps/applications/views.py:203:            dorm_manager_approval = Approval.objects.create(
backend/apps/applications/views.py:206:                step=ApprovalStep.DORM_MANAGER,
backend/apps/applications/views.py:207:                approver=dorm_manager,
backend/apps/applications/views.py:208:                approver_name=dorm_manager.name,
backend/apps/applications/views.py:209:                decision=ApprovalDecision.PENDING
backend/apps/applications/views.py:215:            user.phone = serializer.validated_data['contact_phone']
backend/apps/applications/views.py:276:        draft = Application.objects.select_for_update().filter(student=user, status=ApplicationStatus.DRAFT).first()
backend/apps/applications/views.py:287:        status=ApplicationStatus.DRAFT
backend/apps/notifications/migrations/0002_alter_notification_type.py:16:            field=models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型'),
backend/apps/applications/tests/test_error_cases.py:8:from apps.applications.models import Application, ApplicationStatus
backend/apps/applications/tests/test_error_cases.py:94:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_error_cases.py:95:            'reason': '毕业离校',
backend/apps/applications/tests/test_error_cases.py:96:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_error_cases.py:113:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_error_cases.py:114:            'reason': '毕业离校',
backend/apps/applications/tests/test_error_cases.py:115:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_error_cases.py:121:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_error_cases.py:122:            'reason': '再次提交',
backend/apps/applications/tests/test_error_cases.py:123:            'leave_date': (timezone.now().date() + timedelta(days=2)).isoformat()
backend/apps/applications/tests/test_error_cases.py:139:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_error_cases.py:140:            'reason': '毕业离校',
backend/apps/applications/tests/test_error_cases.py:141:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_error_cases.py:181:            'reason': '毕业离校'
backend/apps/applications/tests/test_error_cases.py:182:            # Missing leave_date
backend/apps/applications/tests/test_list_permissions.py:5:from apps.applications.models import Application, ApplicationStatus
backend/apps/applications/tests/test_list_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/applications/tests/test_list_permissions.py:9:class ApplicationListPermissionTest(TestCase):
backend/apps/applications/tests/test_list_permissions.py:52:            reason='测试',
backend/apps/applications/tests/test_list_permissions.py:53:            leave_date='2024-07-01',
backend/apps/applications/tests/test_list_permissions.py:54:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_list_permissions.py:62:            reason='测试',
backend/apps/applications/tests/test_list_permissions.py:63:            leave_date='2024-07-01',
backend/apps/applications/tests/test_list_permissions.py:64:            status=ApplicationStatus.APPROVED
backend/apps/applications/tests/test_list_permissions.py:68:        Approval.objects.create(
backend/apps/applications/tests/test_list_permissions.py:71:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/tests/test_list_permissions.py:72:            approver=self.counselor1,
backend/apps/applications/tests/test_list_permissions.py:73:            approver_name='辅导员1',
backend/apps/applications/tests/test_list_permissions.py:74:            decision=ApprovalDecision.PENDING
backend/apps/applications/tests/test_list_permissions.py:90:    def test_counselor_sees_only_pending_counselor_approvals(self):
backend/apps/applications/tests/test_list_permissions.py:102:    def test_dean_sees_only_approved_applications_for_archive(self):
backend/apps/notifications/services.py:12:from apps.approvals.models import ApprovalDecision
backend/apps/notifications/services.py:32:        recipient=approval.approver,
backend/apps/notifications/services.py:46:    Create notification for student when approval is approved or rejected.
backend/apps/notifications/services.py:49:        approval: Approval instance with decision
backend/apps/notifications/services.py:54:    approver_role_map = {
backend/apps/notifications/services.py:58:    approver_role = approver_role_map.get(approval.step, "审批人")
backend/apps/notifications/services.py:60:    if approval.decision == ApprovalDecision.APPROVED:
backend/apps/notifications/services.py:62:        message = f"您的离校申请已通过{approver_role}审批。"
backend/apps/notifications/services.py:64:    else:  # rejected
backend/apps/notifications/services.py:66:        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
backend/apps/notifications/services.py:75:            'actor': approval.approver,
backend/apps/notifications/services.py:93:    from apps.approvals.models import Approval
backend/apps/notifications/services.py:101:    pending_approvals = Approval.objects.filter(
backend/apps/notifications/services.py:102:        decision=ApprovalDecision.PENDING
backend/apps/notifications/services.py:103:    ).select_related('approver', 'application__student')
backend/apps/notifications/services.py:122:                'approver': approval.approver.name,
backend/apps/notifications/services.py:128:                recipient=approval.approver,
backend/apps/notifications/services.py:143:                    'approver': approval.approver.name,
backend/apps/notifications/models.py:16:    APPROVAL_APPROVED = 'approval_approved', '审批通过'
backend/apps/notifications/models.py:17:    APPROVAL_REJECTED = 'approval_rejected', '审批驳回'
backend/apps/notifications/management/commands/send_approval_timeout_warnings.py:31:                    f"  - Approval {warning['approval_id']}: "
backend/apps/notifications/management/commands/send_approval_timeout_warnings.py:32:                    f"{warning['approver']} ({warning['days']} days)"
backend/apps/notifications/tests/test_timeout_warnings.py:8:from apps.approvals.models import Approval, ApprovalDecision
backend/apps/notifications/tests/test_timeout_warnings.py:13:class ApprovalTimeoutWarningTests(TestCase):
backend/apps/notifications/tests/test_timeout_warnings.py:41:            reason='毕业离校',
backend/apps/notifications/tests/test_timeout_warnings.py:42:            leave_date='2026-07-01'
backend/apps/notifications/tests/test_timeout_warnings.py:44:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_timeout_warnings.py:47:            approver=self.counselor
backend/apps/notifications/tests/test_timeout_warnings.py:64:            reason='毕业离校',
backend/apps/notifications/tests/test_timeout_warnings.py:65:            leave_date='2026-07-01'
backend/apps/notifications/tests/test_timeout_warnings.py:67:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_timeout_warnings.py:70:            approver=self.dorm_manager
backend/apps/notifications/tests/test_timeout_warnings.py:87:            reason='毕业离校',
backend/apps/notifications/tests/test_timeout_warnings.py:88:            leave_date='2026-07-01'
backend/apps/notifications/tests/test_timeout_warnings.py:90:        Approval.objects.create(
backend/apps/notifications/tests/test_timeout_warnings.py:93:            approver=self.counselor
backend/apps/notifications/tests/test_timeout_warnings.py:101:    def test_approved_not_notified(self):
backend/apps/notifications/tests/test_timeout_warnings.py:102:        """Test that approved/rejected approvals are not notified"""
backend/apps/notifications/tests/test_timeout_warnings.py:105:            reason='毕业离校',
backend/apps/notifications/tests/test_timeout_warnings.py:106:            leave_date='2026-07-01'
backend/apps/notifications/tests/test_timeout_warnings.py:108:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_timeout_warnings.py:111:            approver=self.counselor,
backend/apps/notifications/tests/test_timeout_warnings.py:112:            decision=ApprovalDecision.APPROVED
backend/apps/notifications/tests/test_timeout_warnings.py:126:            reason='毕业离校',
backend/apps/notifications/tests/test_timeout_warnings.py:127:            leave_date='2026-07-01'
backend/apps/notifications/tests/test_timeout_warnings.py:129:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_timeout_warnings.py:132:            approver=self.counselor
backend/apps/notifications/tests/test_timeout_warnings.py:149:            reason='毕业离校',
backend/apps/notifications/tests/test_timeout_warnings.py:150:            leave_date='2026-07-01'
backend/apps/notifications/tests/test_timeout_warnings.py:152:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_timeout_warnings.py:155:            approver=self.counselor
backend/apps/notifications/tests/test_auto_notifications_api.py:11:from apps.applications.models import Application, ApplicationStatus
backend/apps/notifications/tests/test_auto_notifications_api.py:12:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/notifications/tests/test_auto_notifications_api.py:66:            'contact_phone': '13800138000',
backend/apps/notifications/tests/test_auto_notifications_api.py:67:            'reason': '毕业离校',
backend/apps/notifications/tests/test_auto_notifications_api.py:68:            'leave_date': '2026-07-01'
backend/apps/notifications/tests/test_auto_notifications_api.py:83:    def test_approval_approved_notification_visible_via_api(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:84:        """Test student can see APPROVAL_APPROVED notification via API after counselor approves."""
backend/apps/notifications/tests/test_auto_notifications_api.py:91:            reason='毕业离校',
backend/apps/notifications/tests/test_auto_notifications_api.py:92:            leave_date='2026-07-01',
backend/apps/notifications/tests/test_auto_notifications_api.py:93:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications_api.py:96:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications_api.py:99:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications_api.py:100:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications_api.py:101:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:102:            decision=ApprovalDecision.PENDING
backend/apps/notifications/tests/test_auto_notifications_api.py:105:        # Counselor approves (triggers notification)
backend/apps/notifications/tests/test_auto_notifications_api.py:107:        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
backend/apps/notifications/tests/test_auto_notifications_api.py:121:        approval_notif = [n for n in notifications if n['type'] == 'approval_approved'][0]
backend/apps/notifications/tests/test_auto_notifications_api.py:125:    def test_approval_rejected_notification_includes_reason(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:126:        """Test APPROVAL_REJECTED notification includes rejection reason in message."""
backend/apps/notifications/tests/test_auto_notifications_api.py:133:            reason='毕业离校',
backend/apps/notifications/tests/test_auto_notifications_api.py:134:            leave_date='2026-07-01',
backend/apps/notifications/tests/test_auto_notifications_api.py:135:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications_api.py:138:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications_api.py:141:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications_api.py:142:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications_api.py:143:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:144:            decision=ApprovalDecision.PENDING
backend/apps/notifications/tests/test_auto_notifications_api.py:147:        # Counselor rejects with reason
backend/apps/notifications/tests/test_auto_notifications_api.py:149:        response = self.client.post(f'/api/approvals/{approval.approval_id}/reject/', {
backend/apps/notifications/tests/test_auto_notifications_api.py:160:        reject_notif = [n for n in notifications if n['type'] == 'approval_rejected'][0]
backend/apps/notifications/tests/test_auto_notifications_api.py:161:        self.assertIn('材料不齐全，请补充', reject_notif['message'])
backend/apps/notifications/tests/test_auto_notifications_api.py:180:            reason='毕业离校',
backend/apps/notifications/tests/test_auto_notifications_api.py:181:            leave_date='2026-07-01',
backend/apps/notifications/tests/test_auto_notifications_api.py:182:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications_api.py:185:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications_api.py:188:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications_api.py:189:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications_api.py:190:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:191:            decision=ApprovalDecision.PENDING
backend/apps/notifications/tests/test_auto_notifications_api.py:194:        # Student2 tries to approve (should fail with permission denied)
backend/apps/notifications/tests/test_auto_notifications_api.py:196:        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
backend/apps/notifications/tests/test_auto_notifications_api.py:215:            reason='毕业离校',
backend/apps/notifications/tests/test_auto_notifications_api.py:216:            leave_date='2026-07-01',
backend/apps/notifications/tests/test_auto_notifications_api.py:217:            status=ApplicationStatus.APPROVED
backend/apps/notifications/tests/test_auto_notifications_api.py:220:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications_api.py:223:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications_api.py:224:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications_api.py:225:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:226:            decision=ApprovalDecision.APPROVED  # Already approved
backend/apps/notifications/tests/test_auto_notifications_api.py:229:        # Counselor tries to approve again (should fail with conflict)
backend/apps/notifications/tests/test_auto_notifications_api.py:231:        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
backend/apps/notifications/tests/test_auto_notifications_api.py:258:            'contact_phone': '13800138000',
backend/apps/notifications/tests/test_auto_notifications_api.py:259:            'reason': '毕业离校',
backend/apps/notifications/tests/test_auto_notifications_api.py:260:            'leave_date': '2026-07-01'
backend/apps/notifications/migrations/0001_initial.py:22:                ('type', models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('dorm_clearance_blocked', '宿舍清退阻断'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型')),
backend/apps/applications/tests/test_application_flow.py:8:from apps.applications.models import Application, ApplicationStatus
backend/apps/applications/tests/test_application_flow.py:9:from apps.approvals.models import ApprovalDecision, ApprovalStep
backend/apps/applications/tests/test_application_flow.py:12:class ApplicationFlowTestCase(TestCase):
backend/apps/applications/tests/test_application_flow.py:76:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_application_flow.py:77:            'reason': '毕业离校',
backend/apps/applications/tests/test_application_flow.py:78:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_application_flow.py:81:        self.assertEqual(response.data['status'], ApplicationStatus.PENDING_DORM_MANAGER)
backend/apps/applications/tests/test_application_flow.py:93:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/applications/tests/test_application_flow.py:96:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/approve/', {
backend/apps/applications/tests/test_application_flow.py:100:        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)
backend/apps/applications/tests/test_application_flow.py:103:        self.assertEqual(application.status, ApplicationStatus.PENDING_COUNSELOR)
backend/apps/applications/tests/test_application_flow.py:113:        counselor_approval = application.approvals.get(step=ApprovalStep.COUNSELOR)
backend/apps/applications/tests/test_application_flow.py:116:        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/approve/', {
backend/apps/applications/tests/test_application_flow.py:120:        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)
backend/apps/applications/tests/test_application_flow.py:124:        self.assertEqual(application.status, ApplicationStatus.APPROVED)
backend/apps/applications/tests/test_application_flow.py:130:        self.assertEqual(response.data['status'], ApplicationStatus.APPROVED)
backend/apps/notifications/tests/test_auto_notifications.py:6:- Approval is approved (APPROVAL_APPROVED)
backend/apps/notifications/tests/test_auto_notifications.py:7:- Approval is rejected (APPROVAL_REJECTED)
backend/apps/notifications/tests/test_auto_notifications.py:14:from apps.applications.models import Application, ApplicationStatus
backend/apps/notifications/tests/test_auto_notifications.py:15:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/notifications/tests/test_auto_notifications.py:55:            reason='毕业离校',
backend/apps/notifications/tests/test_auto_notifications.py:56:            leave_date='2024-06-30',
backend/apps/notifications/tests/test_auto_notifications.py:57:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications.py:60:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications.py:63:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:64:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:65:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:66:            decision=ApprovalDecision.PENDING
backend/apps/notifications/tests/test_auto_notifications.py:80:    def test_approval_approved_notification_counselor(self):
backend/apps/notifications/tests/test_auto_notifications.py:87:            reason='毕业离校',
backend/apps/notifications/tests/test_auto_notifications.py:88:            leave_date='2024-06-30',
backend/apps/notifications/tests/test_auto_notifications.py:89:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications.py:92:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications.py:95:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:96:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:97:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:98:            decision=ApprovalDecision.APPROVED
backend/apps/notifications/tests/test_auto_notifications.py:106:        self.assertEqual(notification.type, 'approval_approved')
backend/apps/notifications/tests/test_auto_notifications.py:111:    def test_approval_approved_notification_dorm_manager(self):
backend/apps/notifications/tests/test_auto_notifications.py:118:            reason='毕业离校',
backend/apps/notifications/tests/test_auto_notifications.py:119:            leave_date='2024-06-30',
backend/apps/notifications/tests/test_auto_notifications.py:120:            status=ApplicationStatus.PENDING_DORM_MANAGER
backend/apps/notifications/tests/test_auto_notifications.py:123:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications.py:126:            step=ApprovalStep.DORM_MANAGER,
backend/apps/notifications/tests/test_auto_notifications.py:127:            approver=self.dorm_manager,
backend/apps/notifications/tests/test_auto_notifications.py:128:            approver_name=self.dorm_manager.name,
backend/apps/notifications/tests/test_auto_notifications.py:129:            decision=ApprovalDecision.APPROVED
backend/apps/notifications/tests/test_auto_notifications.py:137:        self.assertEqual(notification.type, 'approval_approved')
backend/apps/notifications/tests/test_auto_notifications.py:140:    def test_approval_rejected_notification(self):
backend/apps/notifications/tests/test_auto_notifications.py:147:            reason='毕业离校',
backend/apps/notifications/tests/test_auto_notifications.py:148:            leave_date='2024-06-30',
backend/apps/notifications/tests/test_auto_notifications.py:149:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications.py:152:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications.py:155:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:156:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:157:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:158:            decision=ApprovalDecision.REJECTED,
backend/apps/notifications/tests/test_auto_notifications.py:167:        self.assertEqual(notification.type, 'approval_rejected')
backend/apps/notifications/tests/test_auto_notifications.py:178:            reason='毕业离校',
backend/apps/notifications/tests/test_auto_notifications.py:179:            leave_date='2024-06-30',
backend/apps/notifications/tests/test_auto_notifications.py:180:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications.py:183:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications.py:186:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:187:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:188:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:189:            decision=ApprovalDecision.PENDING
backend/apps/notifications/tests/test_auto_notifications.py:213:            reason='毕业离校',
backend/apps/notifications/tests/test_auto_notifications.py:214:            leave_date='2024-06-30',
backend/apps/notifications/tests/test_auto_notifications.py:215:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/notifications/tests/test_auto_notifications.py:218:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications.py:221:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:222:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:223:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:224:            decision=ApprovalDecision.APPROVED
backend/apps/notifications/tests/test_auto_notifications.py:238:            type='approval_approved'

exec
/bin/bash -lc "rtk sed -n '330,430p' docs/design/2026-05-27-system-design.md && rtk sed -n '840,1090p' docs/design/2026-05-27-system-design.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE PROTECT,
    FOREIGN KEY (counselor_id) REFERENCES users(id) ON DELETE PROTECT,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE PROTECT,
    FOREIGN KEY (current_approver_id) REFERENCES users(id) ON DELETE PROTECT,
    
    INDEX idx_student_id (student_id),
    INDEX idx_counselor_id (counselor_id),
    INDEX idx_admin_id (admin_id),
    INDEX idx_status (status),
    INDEX idx_application_no (application_no),
    INDEX idx_planned_leave_date (planned_leave_date),
    INDEX idx_approver_status (current_approver_id, status, submit_time),
    INDEX idx_student_status (student_id, status, created_at),
    INDEX idx_status_deleted (status, is_deleted, submit_time)
) COMMENT='离校申请表';
```

**状态枚举（status）：**
- `draft` - 草稿
- `pending_counselor` - 待辅导员审核
- `pending_admin` - 待学工部备案
- `approved` - 审批通过
- `rejected` - 已驳回

**申请编号规则：**
`LX{YYYYMMDD}{6位序号}` 例如：LX202605270000001

### 2.4 审批记录表（approvals）

```sql
CREATE TABLE approvals (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_id BIGINT NOT NULL COMMENT '申请ID',
    approver_id BIGINT NOT NULL COMMENT '审批人ID',
    approver_role VARCHAR(20) NOT NULL COMMENT '审批人角色',
    action VARCHAR(20) NOT NULL COMMENT '操作: approve/reject',
    opinion TEXT COMMENT '审批意见',
    approval_time TIMESTAMP NOT NULL COMMENT '审批时间',
    time_limit INT COMMENT '办理时限(小时)',
    is_timeout BOOLEAN DEFAULT FALSE COMMENT '是否超时',
    created_at TIMESTAMP,
    
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
    FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE PROTECT,
    INDEX idx_application_id (application_id),
    INDEX idx_approver_id (approver_id),
    INDEX idx_approval_time (approval_time),
    INDEX idx_app_time (application_id, approval_time DESC)
) COMMENT='审批记录表';
```

**字段说明：**
- `approver_role`: counselor（辅导员）、admin（学工部）
- `action`: approve（同意）、reject（驳回）
- `time_limit`: 辅导员1个工作日(24小时)，学工部1个工作日(24小时)
- `is_timeout`: 超过时限标记为超时

### 2.5 附件表（attachments）

```sql
CREATE TABLE attachments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_id BIGINT NOT NULL COMMENT '申请ID',
    file_name VARCHAR(255) NOT NULL COMMENT '文件名',
    file_path VARCHAR(500) NOT NULL COMMENT '文件路径',
    file_size BIGINT NOT NULL COMMENT '文件大小(字节)',
    file_type VARCHAR(50) NOT NULL COMMENT '文件类型',
    file_hash VARCHAR(64) COMMENT 'SHA256文件哈希',
    attachment_type VARCHAR(50) NOT NULL COMMENT '附件类型',
    upload_time TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
    INDEX idx_application_id (application_id),
    INDEX idx_attachment_type (attachment_type),
    INDEX idx_file_hash (file_hash),
    INDEX idx_app_type (application_id, attachment_type, is_deleted)
) COMMENT='附件表';
```

**附件类型（attachment_type）：**
- `dorm_clearance` - 宿舍清退证明
- `library_clearance` - 图书馆清书证明
- `finance_settlement` - 财务结清截图
- `other` - 其他附件

**文件限制：**
- 单文件最大 10MB
- 支持格式：jpg, png, pdf, doc, docx
- 存储路径：`/data/uploads/{year}/{month}/{application_no}/`

### 2.6 通知表（notifications）

```sql
CREATE TABLE notifications (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
{
  "code": 200,
  "message": "登出成功"
}
```

### 3.3 申请相关API

**1. 创建申请**
```
POST /api/v1/applications
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "planned_leave_date": "2026-06-15",
  "remarks": "毕业离校"
}

Response:
{
  "code": 201,
  "message": "创建成功",
  "data": {
    "id": 1,
    "status": "draft",
    "planned_leave_date": "2026-06-15",
    "created_at": "2026-05-27T10:00:00Z"
  }
}
```

**2. 获取申请列表**
```
GET /api/v1/applications?status=pending_counselor&page=1&page_size=20
Authorization: Bearer {access_token}

Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 50,
    "page": 1,
    "page_size": 20,
    "items": [
      {
        "id": 1,
        "application_no": "LX202605270000001",
        "student_name": "张三",
        "status": "pending_counselor",
        "planned_leave_date": "2026-06-15",
        "submit_time": "2026-05-27T10:00:00Z"
      }
    ]
  }
}
```

**3. 获取申请详情**
```
GET /api/v1/applications/{id}
Authorization: Bearer {access_token}

Response:
{
  "code": 200,
  "data": {
    "id": 1,
    "application_no": "LX202605270000001",
    "student": {
      "id": 1,
      "student_id": "2020001",
      "name": "张三",
      "department": "计算机学院"
    },
    "status": "pending_counselor",
    "planned_leave_date": "2026-06-15",
    "submit_time": "2026-05-27T10:00:00Z",
    "attachments": [
      {
        "id": 1,
        "file_name": "宿舍清退证明.jpg",
        "attachment_type": "dorm_clearance"
      }
    ],
    "approvals": [
      {
        "approver_name": "李老师",
        "approver_role": "counselor",
        "action": "approve",
        "approval_time": "2026-05-27T14:00:00Z"
      }
    ]
  }
}
```

**4. 更新申请**
```
PUT /api/v1/applications/{id}
Authorization: Bearer {access_token}

Request:
{
  "planned_leave_date": "2026-06-20",
  "remarks": "延后离校"
}

Response:
{
  "code": 200,
  "message": "更新成功"
}
```

**5. 提交申请**
```
POST /api/v1/applications/{id}/submit
Authorization: Bearer {access_token}

Response:
{
  "code": 200,
  "message": "提交成功",
  "data": {
    "status": "pending_counselor",
    "submit_time": "2026-05-27T10:00:00Z"
  }
}
```

### 3.4 审批相关API

**1. 获取待审批列表**
```
GET /api/v1/approvals/pending?page=1&page_size=20
Authorization: Bearer {access_token}

Response:
{
  "code": 200,
  "data": {
    "total": 15,
    "items": [
      {
        "application_id": 1,
        "application_no": "LX202605270000001",
        "student_name": "张三",
        "planned_leave_date": "2026-06-15",
        "submit_time": "2026-05-27T10:00:00Z",
        "time_remaining": 20
      }
    ]
  }
}
```

**2. 审批通过**
```
POST /api/v1/approvals/{application_id}/approve
Authorization: Bearer {access_token}

Request:
{
  "opinion": "材料齐全，同意离校",
  "version": 0
}

Response (成功):
{
  "code": 200,
  "message": "审批成功",
  "data": {
    "status": "pending_admin",
    "next_approver": "学工部",
    "version": 1
  }
}

Response (版本冲突):
{
  "code": 409,
  "message": "申请已被修改，请刷新后重试",
  "data": {
    "current_version": 2
  }
}
```

**3. 审批驳回**
```
POST /api/v1/approvals/{application_id}/reject
Authorization: Bearer {access_token}

Request:
{
  "opinion": "宿舍清退证明不完整，请重新提交",
  "version": 0
}

Response (成功):
{
  "code": 200,
  "message": "已驳回",
  "data": {
    "status": "rejected",
    "version": 1
  }
}

Response (版本冲突):
{
  "code": 409,
  "message": "申请已被修改，请刷新后重试",
  "data": {
    "current_version": 2
  }
}
```

### 3.5 附件相关API

**1. 上传附件**
```
POST /api/v1/applications/{id}/attachments
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

Request:
- file: (binary)
- attachment_type: dorm_clearance

Response (成功):
{
  "code": 201,
  "message": "上传成功",
  "data": {
    "id": 1,
    "file_name": "宿舍清退证明.jpg",
    "file_size": 1024000,
    "file_hash": "a3b2c1d4e5f6...",
    "attachment_type": "dorm_clearance",
    "upload_time": "2026-05-27T10:00:00Z"
  }
}

Response (文件过大):
{
  "code": 400,

codex
`demo-web/index.html` 本身是静态假数据页面，尚未接入 `localhost:8001`；接下来我会读取后端模型、序列化器和视图，确认真实字段名、状态机和附件接口。
exec
/bin/bash -lc 'rtk nl -ba backend/apps/applications/urls.py' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/serializers.py | sed -n '1,240p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import serializers
     2	from .models import Application
     3	
     4	
     5	class ApplicationListSerializer(serializers.ModelSerializer):
     6	    """Lean serializer for application lists - no nested approvals"""
     7	    student_id = serializers.CharField(source='student.user_id', read_only=True)
     8	
     9	    class Meta:
    10	        model = Application
    11	        fields = ['application_id', 'student_id', 'student_name', 'class_id',
    12	                  'contact_phone', 'reason', 'leave_date', 'status', 'created_at', 'updated_at']
    13	        read_only_fields = ['application_id', 'student_id', 'student_name',
    14	                            'class_id', 'status', 'created_at', 'updated_at']
    15	
    16	
    17	class ApplicationSerializer(serializers.ModelSerializer):
    18	    student_id = serializers.CharField(source='student.user_id', read_only=True)
    19	    approvals = serializers.SerializerMethodField()
    20	
    21	    class Meta:
    22	        model = Application
    23	        fields = ['application_id', 'student_id', 'student_name', 'class_id',
    24	                  'contact_phone', 'reason', 'leave_date', 'status', 'dorm_checkout_status',
    25	                  'approvals', 'created_at', 'updated_at']
    26	        read_only_fields = ['application_id', 'student_id', 'student_name',
    27	                            'class_id', 'status', 'dorm_checkout_status',
    28	                            'created_at', 'updated_at']
    29	
    30	    def get_approvals(self, obj):
    31	        from apps.approvals.serializers import ApprovalSerializer
    32	        return ApprovalSerializer(obj.approvals.all(), many=True).data
    33	
    34	
    35	class ApplicationCreateSerializer(serializers.Serializer):
    36	    contact_phone = serializers.CharField(max_length=20, required=True)
    37	    reason = serializers.CharField(max_length=500, required=False, allow_blank=True, default='')
    38	    leave_date = serializers.DateField()
    39	
    40	    def validate_leave_date(self, value):
    41	        from django.utils import timezone
    42	        today = timezone.now().date()
    43	        if value < today:
    44	            raise serializers.ValidationError('离校日期不能早于今天')
    45	        return value
    46	
    47	
    48	class ApplicationListResponseSerializer(serializers.Serializer):
    49	    """Schema-only: application list response with pagination"""
    50	    count = serializers.IntegerField()
    51	    results = ApplicationListSerializer(many=True)

 succeeded in 0ms:
     1	from django.urls import path
     2	from . import views
     3	
     4	urlpatterns = [
     5	    path('', views.applications_view, name='applications'),
     6	    path('draft/', views.get_or_create_draft, name='create_draft'),
     7	    path('<str:application_id>/', views.get_application, name='get_application'),
     8	]

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/models.py | sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/views.py | sed -n '1,260p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.db import models
     2	from django.core.exceptions import ValidationError
     3	from apps.users.models import User
     4	
     5	
     6	class ApplicationStatus(models.TextChoices):
     7	    DRAFT = 'draft', '草稿'
     8	    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
     9	    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
    10	    APPROVED = 'approved', '已通过'
    11	    REJECTED = 'rejected', '已驳回'
    12	
    13	
    14	class DormCheckoutStatus(models.TextChoices):
    15	    COMPLETED = 'completed', '已清退'
    16	    PENDING = 'pending', '清退中'
    17	    NOT_STARTED = 'not_started', '未开始'
    18	    UNKNOWN = 'unknown', '状态未知'
    19	
    20	
    21	class Application(models.Model):
    22	    application_id = models.CharField(max_length=50, primary_key=True)
    23	    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
    24	    student_name = models.CharField(max_length=100)
    25	    class_id = models.CharField(max_length=50)
    26	    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    27	    reason = models.TextField(blank=True, default='')
    28	    leave_date = models.DateField(null=True, blank=True)
    29	    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT)
    30	    dorm_checkout_status = models.CharField(max_length=20, choices=DormCheckoutStatus.choices, default=DormCheckoutStatus.NOT_STARTED)
    31	    created_at = models.DateTimeField(auto_now_add=True)
    32	    updated_at = models.DateTimeField(auto_now=True)
    33	
    34	    class Meta:
    35	        db_table = 'applications'
    36	
    37	    def clean(self):
    38	        active_statuses = [
    39	            ApplicationStatus.PENDING_DORM_MANAGER,
    40	            ApplicationStatus.PENDING_COUNSELOR,
    41	            ApplicationStatus.APPROVED,
    42	        ]
    43	        if self.status in active_statuses:
    44	            existing = Application.objects.filter(
    45	                student=self.student,
    46	                status__in=active_statuses
    47	            ).exclude(application_id=self.application_id).exists()
    48	            if existing:
    49	                raise ValidationError('该学生已有待审批或已通过的申请，不能重复提交')

 succeeded in 0ms:
     1	from rest_framework import status
     2	from rest_framework.decorators import api_view, permission_classes
     3	from rest_framework.permissions import IsAuthenticated
     4	from rest_framework.response import Response
     5	from django.utils import timezone
     6	from drf_spectacular.utils import extend_schema, OpenApiParameter
     7	from .models import Application, ApplicationStatus, DormCheckoutStatus
     8	from .serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationListSerializer, ApplicationListResponseSerializer
     9	from .pagination import ApplicationLimitOffsetPagination
    10	from .providers import MockDormCheckoutProvider
    11	from .permissions import can_view_application
    12	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
    13	from apps.users.models import UserRole, User
    14	from apps.notifications.services import notify_application_submitted
    15	from schema import ErrorResponseSerializer
    16	import uuid
    17	import logging
    18	
    19	
    20	@extend_schema(
    21	    methods=['GET'],
    22	    operation_id='applications_list',
    23	    summary='获取申请列表',
    24	    description='获取当前用户的申请列表（学生/辅导员/学工部）',
    25	    parameters=[
    26	        OpenApiParameter('status', str, description='状态过滤'),
    27	        OpenApiParameter('limit', int, description='每页数量（默认20）'),
    28	        OpenApiParameter('offset', int, description='偏移量（默认0）'),
    29	    ],
    30	    responses={
    31	        200: ApplicationListResponseSerializer,
    32	        403: ErrorResponseSerializer,
    33	    },
    34	    tags=['申请']
    35	)
    36	@extend_schema(
    37	    methods=['POST'],
    38	    operation_id='applications_create',
    39	    summary='提交离校申请',
    40	    description='学生提交新的离校申请',
    41	    request=ApplicationCreateSerializer,
    42	    responses={
    43	        201: ApplicationSerializer,
    44	        400: ErrorResponseSerializer,
    45	        403: ErrorResponseSerializer,
    46	        404: ErrorResponseSerializer,
    47	        409: ErrorResponseSerializer,
    48	        422: ErrorResponseSerializer,
    49	    },
    50	    tags=['申请']
    51	)
    52	@api_view(['GET', 'POST'])
    53	@permission_classes([IsAuthenticated])
    54	def applications_view(request):
    55	    if request.method == 'GET':
    56	        return list_applications(request)
    57	    else:
    58	        return create_application(request)
    59	
    60	
    61	def list_applications(request):
    62	    user = request.user
    63	
    64	    # Student: own applications only
    65	    if user.role == UserRole.STUDENT:
    66	        queryset = Application.objects.filter(student=user)
    67	
    68	    # Dorm Manager: applications with own pending dorm manager approvals
    69	    elif user.role == UserRole.DORM_MANAGER:
    70	        pending_approvals = Approval.objects.filter(
    71	            approver=user,
    72	            step=ApprovalStep.DORM_MANAGER,
    73	            decision=ApprovalDecision.PENDING
    74	        ).values_list('application', flat=True)
    75	        queryset = Application.objects.filter(pk__in=pending_approvals)
    76	
    77	    # Counselor: applications with own pending counselor approvals
    78	    elif user.role == UserRole.COUNSELOR:
    79	        pending_approvals = Approval.objects.filter(
    80	            approver=user,
    81	            step=ApprovalStep.COUNSELOR,
    82	            decision=ApprovalDecision.PENDING
    83	        ).values_list('application', flat=True)
    84	        queryset = Application.objects.filter(pk__in=pending_approvals)
    85	
    86	    # Dean: view all approved applications (archiving role)
    87	    elif user.role == UserRole.DEAN:
    88	        queryset = Application.objects.filter(status=ApplicationStatus.APPROVED)
    89	
    90	    # Admin: view all applications
    91	    elif user.role == UserRole.ADMIN:
    92	        queryset = Application.objects.all()
    93	
    94	    else:
    95	        return Response(
    96	            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
    97	            status=status.HTTP_403_FORBIDDEN
    98	        )
    99	
   100	    # Status filtering
   101	    status_param = request.query_params.get('status')
   102	    if status_param:
   103	        queryset = queryset.filter(status=status_param)
   104	
   105	    # Sort by created_at DESC
   106	    queryset = queryset.order_by('-created_at', '-application_id')
   107	
   108	    # Paginate
   109	    paginator = ApplicationLimitOffsetPagination()
   110	    page = paginator.paginate_queryset(queryset, request)
   111	
   112	    # Serialize
   113	    serializer = ApplicationListSerializer(page, many=True)
   114	
   115	    return paginator.get_paginated_response(serializer.data)
   116	
   117	
   118	def create_application(request):
   119	    from django.db import transaction
   120	
   121	    user = request.user
   122	
   123	    if user.role != UserRole.STUDENT:
   124	        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以提交申请'}},
   125	                        status=status.HTTP_403_FORBIDDEN)
   126	
   127	    serializer = ApplicationCreateSerializer(data=request.data)
   128	    if not serializer.is_valid():
   129	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
   130	                                    'details': serializer.errors}},
   131	                        status=status.HTTP_400_BAD_REQUEST)
   132	
   133	    with transaction.atomic():
   134	        # Check for existing pending/approved applications
   135	        existing = Application.objects.select_for_update().filter(
   136	            student=user,
   137	            status__in=[ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.APPROVED]
   138	        ).first()
   139	        if existing:
   140	            return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
   141	                                        'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
   142	                            status=status.HTTP_409_CONFLICT)
   143	
   144	        provider = MockDormCheckoutProvider()
   145	        dorm_status = provider.check_status(user.user_id)
   146	
   147	        if dorm_status.status != DormCheckoutStatus.COMPLETED:
   148	            return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
   149	                                        'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
   150	                                                    'blocking_reason': dorm_status.blocking_reason}}},
   151	                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
   152	
   153	        # Find dorm managers
   154	        dorm_managers = []
   155	        building = user.building
   156	
   157	        if building and building.strip():
   158	            dorm_managers = list(User.objects.filter(
   159	                role=UserRole.DORM_MANAGER,
   160	                building=building,
   161	                active=True
   162	            ).order_by('user_id'))
   163	
   164	        if not dorm_managers:
   165	            from django.conf import settings
   166	            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
   167	            try:
   168	                fallback_manager = User.objects.get(role=UserRole.DORM_MANAGER, user_id=fallback_id, active=True)
   169	                dorm_managers = [fallback_manager]
   170	            except User.DoesNotExist:
   171	                return Response({'error': {'code': 'NOT_FOUND', 'message': '无可用宿管员',
   172	                                            'details': {'building': building or '未分配', 'fallback_id': fallback_id}}},
   173	                                status=status.HTTP_404_NOT_FOUND)
   174	
   175	        # Check for existing draft, convert if exists
   176	        draft = Application.objects.select_for_update().filter(student=user, status=ApplicationStatus.DRAFT).first()
   177	
   178	        if draft:
   179	            # Update draft to submitted application
   180	            draft.contact_phone = serializer.validated_data['contact_phone']
   181	            draft.reason = serializer.validated_data.get('reason', '')
   182	            draft.leave_date = serializer.validated_data['leave_date']
   183	            draft.status = ApplicationStatus.PENDING_DORM_MANAGER
   184	            draft.dorm_checkout_status = dorm_status.status
   185	            draft.save()
   186	            application = draft
   187	        else:
   188	            # Create new application
   189	            application = Application.objects.create(
   190	                application_id=f'app_{uuid.uuid4().hex[:8]}',
   191	                student=user,
   192	                student_name=user.name,
   193	                class_id=user.class_id,
   194	                contact_phone=serializer.validated_data['contact_phone'],
   195	                reason=serializer.validated_data.get('reason', ''),
   196	                leave_date=serializer.validated_data['leave_date'],
   197	                status=ApplicationStatus.PENDING_DORM_MANAGER,
   198	                dorm_checkout_status=dorm_status.status
   199	            )
   200	
   201	        # Create approvals
   202	        for dorm_manager in dorm_managers:
   203	            dorm_manager_approval = Approval.objects.create(
   204	                approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   205	                application=application,
   206	                step=ApprovalStep.DORM_MANAGER,
   207	                approver=dorm_manager,
   208	                approver_name=dorm_manager.name,
   209	                decision=ApprovalDecision.PENDING
   210	            )
   211	            notify_application_submitted(application, dorm_manager_approval)
   212	
   213	        # Sync phone to User table
   214	        if not user.phone:
   215	            user.phone = serializer.validated_data['contact_phone']
   216	            user.save()
   217	
   218	    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
   219	
   220	
   221	@extend_schema(
   222	    operation_id='applications_get',
   223	    summary='获取申请详情',
   224	    description='获取指定申请的详细信息（包括审批记录）',
   225	    responses={
   226	        200: ApplicationSerializer,
   227	        403: ErrorResponseSerializer,
   228	        404: ErrorResponseSerializer,
   229	    },
   230	    tags=['申请']
   231	)
   232	@api_view(['GET'])
   233	@permission_classes([IsAuthenticated])
   234	def get_application(request, application_id):
   235	    try:
   236	        application = Application.objects.get(application_id=application_id)
   237	    except Application.DoesNotExist:
   238	        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在',
   239	                                    'details': {'application_id': application_id}}},
   240	                        status=status.HTTP_404_NOT_FOUND)
   241	
   242	    user = request.user
   243	
   244	    # Check permission using shared helper
   245	    if not can_view_application(user, application):
   246	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
   247	                        status=status.HTTP_403_FORBIDDEN)
   248	
   249	    return Response(ApplicationSerializer(application).data)
   250	
   251	
   252	@extend_schema(
   253	    operation_id='applications_draft',
   254	    summary='获取或创建草稿申请',
   255	    description='学生获取或创建草稿申请，用于附件上传前置',
   256	    responses={
   257	        200: ApplicationSerializer,
   258	        201: ApplicationSerializer,
   259	        403: ErrorResponseSerializer,
   260	    },

codex
目前后端创建申请是一次 POST 到 `/api/applications/`，字段是 `contact_phone`、`reason`、`leave_date`，提交后直接进入 `pending_dorm_manager` 并创建宿管审批记录。附件上传需要先有申请或草稿 ID，不是单纯本地保存文件列表。
exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/serializers.py | sed -n '1,220p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import serializers
     2	from .models import Approval
     3	
     4	
     5	class ApprovalListSerializer(serializers.ModelSerializer):
     6	    """Lean serializer for approval lists - includes created_at"""
     7	    application_id = serializers.CharField(source='application.application_id', read_only=True)
     8	    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
     9	
    10	    class Meta:
    11	        model = Approval
    12	        fields = ['approval_id', 'application_id', 'step', 'approver_id',
    13	                  'approver_name', 'decision', 'created_at']
    14	        read_only_fields = ['approval_id', 'application_id', 'step',
    15	                            'approver_id', 'approver_name', 'decision', 'created_at']
    16	
    17	
    18	class ApprovalSerializer(serializers.ModelSerializer):
    19	    application_id = serializers.CharField(source='application.application_id', read_only=True)
    20	    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
    21	
    22	    class Meta:
    23	        model = Approval
    24	        fields = ['approval_id', 'application_id', 'step', 'approver_id',
    25	                  'approver_name', 'decision', 'comment', 'decided_at']
    26	        read_only_fields = ['approval_id', 'application_id', 'step',
    27	                            'approver_id', 'approver_name', 'decision', 'decided_at']
    28	
    29	
    30	class ApprovalActionSerializer(serializers.Serializer):
    31	    comment = serializers.CharField(required=False, allow_blank=True)
    32	
    33	
    34	class ApprovalListResponseSerializer(serializers.Serializer):
    35	    """Schema-only: approval list response with pagination"""
    36	    count = serializers.IntegerField()
    37	    results = ApprovalListSerializer(many=True)

exec
/bin/bash -lc 'rtk nl -ba backend/apps/approvals/urls.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.urls import path
     2	from . import views
     3	
     4	urlpatterns = [
     5	    path('', views.list_approvals, name='list_approvals'),
     6	    path('<str:approval_id>/', views.get_approval, name='get_approval'),
     7	    path('<str:approval_id>/approve/', views.approve_approval, name='approve_approval'),
     8	    path('<str:approval_id>/reject/', views.reject_approval, name='reject_approval'),
     9	]

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/views.py | sed -n '1,320p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import status
     2	from rest_framework.decorators import api_view, permission_classes
     3	from rest_framework.permissions import IsAuthenticated
     4	from rest_framework.response import Response
     5	from django.utils import timezone
     6	from django.db import transaction
     7	import logging
     8	from drf_spectacular.utils import extend_schema, OpenApiParameter
     9	from .models import Approval, ApprovalDecision, ApprovalStep
    10	from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalListSerializer, ApprovalListResponseSerializer
    11	from .pagination import ApprovalLimitOffsetPagination
    12	from .validators import approval_step_matches_application_status
    13	from apps.applications.models import Application, ApplicationStatus
    14	from apps.users.models import User, UserRole
    15	from apps.notifications.services import notify_approval_decided
    16	from schema import ErrorResponseSerializer
    17	import uuid
    18	
    19	
    20	@extend_schema(
    21	    operation_id='approvals_list',
    22	    summary='获取审批列表',
    23	    description='获取当前用户的待审批列表（辅导员或学工部）',
    24	    parameters=[
    25	        OpenApiParameter('decision', str, description='决策过滤：pending/approved/rejected/all（默认pending）'),
    26	        OpenApiParameter('limit', int, description='每页数量（默认20）'),
    27	        OpenApiParameter('offset', int, description='偏移量（默认0）'),
    28	    ],
    29	    responses={
    30	        200: ApprovalListResponseSerializer,
    31	        403: ErrorResponseSerializer,
    32	    },
    33	    tags=['审批']
    34	)
    35	@api_view(['GET'])
    36	@permission_classes([IsAuthenticated])
    37	def list_approvals(request):
    38	    user = request.user
    39	
    40	    # 学生禁止访问
    41	    if user.role == UserRole.STUDENT:
    42	        return Response(
    43	            {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
    44	            status=status.HTTP_403_FORBIDDEN
    45	        )
    46	
    47	    # 宿管员: 只看自己的dorm_manager审批
    48	    if user.role == UserRole.DORM_MANAGER:
    49	        queryset = Approval.objects.filter(
    50	            approver=user,
    51	            step=ApprovalStep.DORM_MANAGER
    52	        ).select_related('application', 'approver')
    53	
    54	    # 辅导员: 只看自己的counselor审批
    55	    elif user.role == UserRole.COUNSELOR:
    56	        queryset = Approval.objects.filter(
    57	            approver=user,
    58	            step=ApprovalStep.COUNSELOR
    59	        ).select_related('application', 'approver')
    60	
    61	    # 学工部: 查看所有审批（存档用）
    62	    elif user.role == UserRole.DEAN:
    63	        queryset = Approval.objects.all().select_related('application', 'approver')
    64	
    65	    else:
    66	        return Response(
    67	            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
    68	            status=status.HTTP_403_FORBIDDEN
    69	        )
    70	
    71	    # Decision filtering (default: pending)
    72	    decision_param = request.query_params.get('decision', 'pending')
    73	    if decision_param != 'all':
    74	        queryset = queryset.filter(decision=decision_param)
    75	
    76	    # 排序
    77	    queryset = queryset.order_by('-created_at', '-approval_id')
    78	
    79	    # 分页
    80	    paginator = ApprovalLimitOffsetPagination()
    81	    page = paginator.paginate_queryset(queryset, request)
    82	
    83	    # 序列化
    84	    serializer = ApprovalListSerializer(page, many=True)
    85	
    86	    return paginator.get_paginated_response(serializer.data)
    87	
    88	
    89	@extend_schema(
    90	    operation_id='approvals_get',
    91	    summary='获取审批详情',
    92	    description='获取指定审批的详细信息',
    93	    responses={
    94	        200: ApprovalSerializer,
    95	        403: ErrorResponseSerializer,
    96	        404: ErrorResponseSerializer,
    97	    },
    98	    tags=['审批']
    99	)
   100	@api_view(['GET'])
   101	@permission_classes([IsAuthenticated])
   102	def get_approval(request, approval_id):
   103	    try:
   104	        approval = Approval.objects.select_related('application', 'approver').get(approval_id=approval_id)
   105	    except Approval.DoesNotExist:
   106	        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
   107	                        status=status.HTTP_404_NOT_FOUND)
   108	
   109	    user = request.user
   110	
   111	    # Permission check: only the approver or dean can view this approval
   112	    if user.role == UserRole.DEAN or approval.approver_id == user.user_id:
   113	        return Response(ApprovalSerializer(approval).data)
   114	
   115	    return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
   116	                    status=status.HTTP_403_FORBIDDEN)
   117	
   118	
   119	@extend_schema(
   120	    operation_id='approvals_approve',
   121	    summary='通过审批',
   122	    description='审批人通过指定的审批申请',
   123	    request=ApprovalActionSerializer,
   124	    responses={
   125	        200: ApprovalSerializer,
   126	        400: ErrorResponseSerializer,
   127	        403: ErrorResponseSerializer,
   128	        404: ErrorResponseSerializer,
   129	        409: ErrorResponseSerializer,
   130	    },
   131	    tags=['审批']
   132	)
   133	@api_view(['POST'])
   134	@permission_classes([IsAuthenticated])
   135	@transaction.atomic
   136	def approve_approval(request, approval_id):
   137	    try:
   138	        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
   139	    except Approval.DoesNotExist:
   140	        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
   141	                        status=status.HTTP_404_NOT_FOUND)
   142	
   143	    user = request.user
   144	    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
   145	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   146	                        status=status.HTTP_403_FORBIDDEN)
   147	    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
   148	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   149	                        status=status.HTTP_403_FORBIDDEN)
   150	    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
   151	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   152	                        status=status.HTTP_403_FORBIDDEN)
   153	
   154	    if approval.approver_id != user.user_id:
   155	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   156	                        status=status.HTTP_403_FORBIDDEN)
   157	
   158	    if approval.decision != ApprovalDecision.PENDING:
   159	        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
   160	                        status=status.HTTP_409_CONFLICT)
   161	
   162	    if not approval_step_matches_application_status(approval):
   163	        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
   164	                        status=status.HTTP_409_CONFLICT)
   165	
   166	    serializer = ApprovalActionSerializer(data=request.data)
   167	    if not serializer.is_valid():
   168	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
   169	                        status=status.HTTP_400_BAD_REQUEST)
   170	
   171	    approval.decision = ApprovalDecision.APPROVED
   172	    approval.comment = serializer.validated_data.get('comment', '')
   173	    approval.decided_at = timezone.now()
   174	    approval.save()
   175	
   176	    notify_approval_decided(approval)
   177	
   178	    application = approval.application
   179	    if approval.step == ApprovalStep.DORM_MANAGER:
   180	        # Auto-complete other pending dorm manager approvals for the same building
   181	        # (New requirement: any dorm manager in the building can approve, others see "already approved")
   182	        other_dorm_approvals = Approval.objects.filter(
   183	            application=application,
   184	            step=ApprovalStep.DORM_MANAGER,
   185	            decision=ApprovalDecision.PENDING
   186	        ).exclude(approval_id=approval.approval_id)
   187	
   188	        if other_dorm_approvals.exists():
   189	            other_dorm_approvals.update(
   190	                decision=ApprovalDecision.APPROVED,
   191	                comment=f'已由{approval.approver_name}完成审批，无需重复操作',
   192	                decided_at=timezone.now()
   193	            )
   194	            logging.info(
   195	                f"Auto-completed {other_dorm_approvals.count()} other dorm manager approvals "
   196	                f"for application {application.application_id} after approval by {approval.approver.user_id}"
   197	            )
   198	
   199	        # Check for existing counselor approval to prevent duplicates
   200	        existing_counselor_approval = Approval.objects.filter(
   201	            application=application,
   202	            step=ApprovalStep.COUNSELOR
   203	        ).exists()
   204	
   205	        if existing_counselor_approval:
   206	            return Response({'error': {'code': 'CONFLICT', 'message': '辅导员审批已存在，不能重复创建'}},
   207	                            status=status.HTTP_409_CONFLICT)
   208	
   209	        application.status = ApplicationStatus.PENDING_COUNSELOR
   210	        application.save()
   211	
   212	        # Get counselor by department (Phase 3 design: department-based routing)
   213	        # Note: Original design used ClassMapping (class_id), but Phase 3 user requirements
   214	        # changed to "按学院向辅导员审批" (approval by department/college).
   215	        # Multiple counselors per department are allowed (different classes within department).
   216	        # Selection: order_by('user_id') picks lowest ID for deterministic routing.
   217	        counselors = User.objects.filter(
   218	            role=UserRole.COUNSELOR,
   219	            department=application.student.department,
   220	            active=True
   221	        ).order_by('user_id')
   222	
   223	        if counselors.count() > 1:
   224	            logging.warning(
   225	                f"Multiple counselors found for department {application.student.department}: "
   226	                f"{counselors.count()} matches. Selected {counselors.first().user_id} via order_by('user_id')"
   227	            )
   228	
   229	        counselor = counselors.first()
   230	
   231	        if not counselor:
   232	            return Response({'error': {'code': 'NOT_FOUND', 'message': '该学院辅导员不存在',
   233	                                        'details': {'department': application.student.department}}},
   234	                            status=status.HTTP_404_NOT_FOUND)
   235	
   236	        Approval.objects.create(
   237	            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   238	            application=application,
   239	            step=ApprovalStep.COUNSELOR,
   240	            approver=counselor,
   241	            approver_name=counselor.name,
   242	            decision=ApprovalDecision.PENDING
   243	        )
   244	    elif approval.step == ApprovalStep.COUNSELOR:
   245	        # Counselor approval completes the process (2-level approval)
   246	        application.status = ApplicationStatus.APPROVED
   247	        application.save()
   248	
   249	    return Response(ApprovalSerializer(approval).data)
   250	
   251	
   252	@extend_schema(
   253	    operation_id='approvals_reject',
   254	    summary='驳回审批',
   255	    description='审批人驳回指定的审批申请',
   256	    request=ApprovalActionSerializer,
   257	    responses={
   258	        200: ApprovalSerializer,
   259	        400: ErrorResponseSerializer,
   260	        403: ErrorResponseSerializer,
   261	        404: ErrorResponseSerializer,
   262	        409: ErrorResponseSerializer,
   263	    },
   264	    tags=['审批']
   265	)
   266	@api_view(['POST'])
   267	@permission_classes([IsAuthenticated])
   268	@transaction.atomic
   269	def reject_approval(request, approval_id):
   270	    try:
   271	        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
   272	    except Approval.DoesNotExist:
   273	        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
   274	                        status=status.HTTP_404_NOT_FOUND)
   275	
   276	    user = request.user
   277	    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
   278	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   279	                        status=status.HTTP_403_FORBIDDEN)
   280	    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
   281	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   282	                        status=status.HTTP_403_FORBIDDEN)
   283	    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
   284	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   285	                        status=status.HTTP_403_FORBIDDEN)
   286	
   287	    if approval.approver_id != user.user_id:
   288	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   289	                        status=status.HTTP_403_FORBIDDEN)
   290	
   291	    if approval.decision != ApprovalDecision.PENDING:
   292	        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
   293	                        status=status.HTTP_409_CONFLICT)
   294	
   295	    if not approval_step_matches_application_status(approval):
   296	        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
   297	                        status=status.HTTP_409_CONFLICT)
   298	
   299	    serializer = ApprovalActionSerializer(data=request.data)
   300	    if not serializer.is_valid():
   301	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
   302	                        status=status.HTTP_400_BAD_REQUEST)
   303	
   304	    approval.decision = ApprovalDecision.REJECTED
   305	    approval.comment = serializer.validated_data.get('comment', '')
   306	    approval.decided_at = timezone.now()
   307	    approval.save()
   308	
   309	    notify_approval_decided(approval)
   310	
   311	    application = approval.application
   312	    application.status = ApplicationStatus.REJECTED
   313	    application.save()
   314	
   315	    return Response(ApprovalSerializer(approval).data)

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/models.py | sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.db import models
     2	from apps.users.models import User
     3	from apps.applications.models import Application
     4	
     5	
     6	class ApprovalStep(models.TextChoices):
     7	    DORM_MANAGER = 'dorm_manager', '宿管员'
     8	    COUNSELOR = 'counselor', '辅导员'
     9	    DEAN = 'dean', '学工部'
    10	
    11	
    12	class ApprovalDecision(models.TextChoices):
    13	    PENDING = 'pending', '待审批'
    14	    APPROVED = 'approved', '已通过'
    15	    REJECTED = 'rejected', '已驳回'
    16	
    17	
    18	class Approval(models.Model):
    19	    approval_id = models.CharField(max_length=50, primary_key=True)
    20	    application = models.ForeignKey(Application, on_delete=models.PROTECT, related_name='approvals')
    21	    step = models.CharField(max_length=20, choices=ApprovalStep.choices)
    22	    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals')
    23	    approver_name = models.CharField(max_length=100)
    24	    decision = models.CharField(max_length=20, choices=ApprovalDecision.choices, default=ApprovalDecision.PENDING)
    25	    comment = models.TextField(null=True, blank=True)
    26	    decided_at = models.DateTimeField(null=True, blank=True)
    27	    created_at = models.DateTimeField(auto_now_add=True)
    28	    updated_at = models.DateTimeField(auto_now=True)
    29	
    30	    class Meta:
    31	        db_table = 'approvals'

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/views.py | sed -n '252,380p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   252	@extend_schema(
   253	    operation_id='applications_draft',
   254	    summary='获取或创建草稿申请',
   255	    description='学生获取或创建草稿申请，用于附件上传前置',
   256	    responses={
   257	        200: ApplicationSerializer,
   258	        201: ApplicationSerializer,
   259	        403: ErrorResponseSerializer,
   260	    },
   261	    tags=['申请']
   262	)
   263	@api_view(['POST'])
   264	@permission_classes([IsAuthenticated])
   265	def get_or_create_draft(request):
   266	    from django.db import transaction
   267	
   268	    user = request.user
   269	
   270	    if user.role != UserRole.STUDENT:
   271	        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以创建草稿'}},
   272	                        status=status.HTTP_403_FORBIDDEN)
   273	
   274	    with transaction.atomic():
   275	        # Get existing draft or create new one
   276	        draft = Application.objects.select_for_update().filter(student=user, status=ApplicationStatus.DRAFT).first()
   277	
   278	    if draft:
   279	        return Response(ApplicationSerializer(draft).data, status=status.HTTP_200_OK)
   280	
   281	    # Create new draft
   282	    draft = Application.objects.create(
   283	        application_id=f'app_{uuid.uuid4().hex[:8]}',
   284	        student=user,
   285	        student_name=user.name,
   286	        class_id=user.class_id,
   287	        status=ApplicationStatus.DRAFT
   288	    )
   289	
   290	    return Response(ApplicationSerializer(draft).data, status=status.HTTP_201_CREATED)

exec
/bin/bash -lc "rtk nl -ba backend/apps/attachments/models.py | sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.db import models
     2	from apps.applications.models import Application
     3	from apps.users.models import User
     4	
     5	
     6	class AttachmentType(models.TextChoices):
     7	    DORM_CHECKOUT = 'dorm_checkout', '宿舍清退证明'
     8	    LIBRARY_CLEARANCE = 'library_clearance', '图书馆清书证明'
     9	    FINANCE_CLEARANCE = 'finance_clearance', '财务结清证明'
    10	    OTHER = 'other', '其他'
    11	
    12	
    13	class Attachment(models.Model):
    14	    attachment_id = models.CharField(max_length=50, primary_key=True)
    15	    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='attachments')
    16	    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT)
    17	    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    18	    attachment_type = models.CharField(max_length=50, choices=AttachmentType.choices)
    19	    file_name = models.CharField(max_length=255)
    20	    file_size = models.IntegerField()
    21	    content_type = models.CharField(max_length=100)
    22	    uploaded_at = models.DateTimeField(auto_now_add=True)
    23	    is_deleted = models.BooleanField(default=False)
    24	    deleted_at = models.DateTimeField(null=True, blank=True)
    25	
    26	    class Meta:
    27	        db_table = 'attachments'
    28	        ordering = ['-uploaded_at']
    29	
    30	    def __str__(self):
    31	        return f"{self.attachment_id} - {self.file_name}"

exec
/bin/bash -lc "rtk nl -ba backend/apps/attachments/serializers.py | sed -n '1,220p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import serializers
     2	from .models import Attachment, AttachmentType
     3	
     4	
     5	class AttachmentUploadSerializer(serializers.Serializer):
     6	    file = serializers.FileField()
     7	    attachment_type = serializers.ChoiceField(choices=AttachmentType.choices)
     8	
     9	    def validate_file(self, value):
    10	        # Max 10MB
    11	        if value.size > 10 * 1024 * 1024:
    12	            raise serializers.ValidationError('文件大小不能超过10MB')
    13	
    14	        # Allowed extensions
    15	        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']
    16	        file_name = value.name.lower()
    17	        if not any(file_name.endswith(ext) for ext in allowed_extensions):
    18	            raise serializers.ValidationError(f'不支持的文件类型，仅支持：{", ".join(allowed_extensions)}')
    19	
    20	        return value
    21	
    22	
    23	class AttachmentSerializer(serializers.ModelSerializer):
    24	    class Meta:
    25	        model = Attachment
    26	        fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'attachment_type', 'uploaded_at']
    27	        read_only_fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'uploaded_at']
    28	
    29	
    30	class AttachmentListResponseSerializer(serializers.Serializer):
    31	    """Schema-only: attachment list response with wrapper"""
    32	    attachments = AttachmentSerializer(many=True)

exec
/bin/bash -lc 'rtk nl -ba backend/apps/attachments/urls.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.urls import path
     2	from . import views
     3	
     4	urlpatterns = [
     5	    path('applications/<str:application_id>/attachments/', views.attachments_view, name='attachments'),
     6	    path('attachments/<str:attachment_id>/download/', views.download_attachment, name='download_attachment'),
     7	    path('attachments/<str:attachment_id>/', views.delete_attachment, name='delete_attachment'),
     8	]

exec
/bin/bash -lc "rtk rg -n \"path\\('api|include\\(|applications|approvals|attachments\" backend -g 'urls.py'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/config/urls.py:8:    path('api/auth/', include('apps.users.urls')),
backend/config/urls.py:9:    path('api/', include('apps.attachments.urls')),
backend/config/urls.py:10:    path('api/applications/', include('apps.applications.urls')),
backend/config/urls.py:11:    path('api/approvals/', include('apps.approvals.urls')),
backend/config/urls.py:12:    path('api/notifications/', include('apps.notifications.urls')),
backend/config/urls.py:15:    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
backend/config/urls.py:16:    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
backend/apps/approvals/urls.py:5:    path('', views.list_approvals, name='list_approvals'),
backend/apps/attachments/urls.py:5:    path('applications/<str:application_id>/attachments/', views.attachments_view, name='attachments'),
backend/apps/attachments/urls.py:6:    path('attachments/<str:attachment_id>/download/', views.download_attachment, name='download_attachment'),
backend/apps/attachments/urls.py:7:    path('attachments/<str:attachment_id>/', views.delete_attachment, name='delete_attachment'),
backend/apps/applications/urls.py:5:    path('', views.applications_view, name='applications'),

exec
/bin/bash -lc "rtk nl -ba backend/apps/attachments/views.py | sed -n '1,320p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import status
     2	from rest_framework.decorators import api_view, permission_classes, parser_classes
     3	from rest_framework.permissions import IsAuthenticated
     4	from rest_framework.parsers import MultiPartParser, FormParser
     5	from rest_framework.response import Response
     6	from django.http import FileResponse, Http404
     7	from django.utils import timezone
     8	from drf_spectacular.utils import extend_schema, OpenApiResponse
     9	from apps.users.models import UserRole
    10	from apps.applications.models import Application
    11	from apps.applications.permissions import can_view_application
    12	from apps.approvals.models import Approval, ApprovalStep
    13	from .models import Attachment
    14	from .serializers import AttachmentUploadSerializer, AttachmentSerializer, AttachmentListResponseSerializer
    15	from schema import ErrorResponseSerializer
    16	import uuid
    17	
    18	
    19	@extend_schema(
    20	    methods=['GET'],
    21	    operation_id='attachments_list',
    22	    summary='获取附件列表',
    23	    description='获取指定申请的附件列表',
    24	    responses={
    25	        200: AttachmentListResponseSerializer,
    26	        403: ErrorResponseSerializer,
    27	        404: ErrorResponseSerializer,
    28	    },
    29	    tags=['附件']
    30	)
    31	@extend_schema(
    32	    methods=['POST'],
    33	    operation_id='attachments_upload',
    34	    summary='上传附件',
    35	    description='为指定申请上传附件（仅申请所有者可上传）',
    36	    request=AttachmentUploadSerializer,
    37	    responses={
    38	        201: AttachmentSerializer,
    39	        400: ErrorResponseSerializer,
    40	        403: ErrorResponseSerializer,
    41	        404: ErrorResponseSerializer,
    42	    },
    43	    tags=['附件']
    44	)
    45	@api_view(['GET', 'POST'])
    46	@permission_classes([IsAuthenticated])
    47	@parser_classes([MultiPartParser, FormParser])
    48	def attachments_view(request, application_id):
    49	    """Dispatcher for attachment list (GET) and upload (POST)"""
    50	    if request.method == 'GET':
    51	        return list_attachments(request, application_id)
    52	    else:
    53	        return upload_attachment(request, application_id)
    54	
    55	
    56	def upload_attachment(request, application_id):
    57	    user = request.user
    58	
    59	    # Get application
    60	    try:
    61	        application = Application.objects.get(application_id=application_id)
    62	    except Application.DoesNotExist:
    63	        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在'}},
    64	                        status=status.HTTP_404_NOT_FOUND)
    65	
    66	    # Permission: only student who owns the application
    67	    if user.role != UserRole.STUDENT or application.student_id != user.user_id:
    68	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限上传附件'}},
    69	                        status=status.HTTP_403_FORBIDDEN)
    70	
    71	    # Validate
    72	    serializer = AttachmentUploadSerializer(data=request.data)
    73	    if not serializer.is_valid():
    74	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
    75	                                    'details': serializer.errors}},
    76	                        status=status.HTTP_400_BAD_REQUEST)
    77	
    78	    # Create attachment
    79	    file = serializer.validated_data['file']
    80	    attachment = Attachment.objects.create(
    81	        attachment_id=f'att_{uuid.uuid4().hex[:12]}',
    82	        application=application,
    83	        uploaded_by=user,
    84	        file=file,
    85	        attachment_type=serializer.validated_data['attachment_type'],
    86	        file_name=file.name,
    87	        file_size=file.size,
    88	        content_type=file.content_type or 'application/octet-stream'
    89	    )
    90	
    91	    return Response(AttachmentSerializer(attachment).data, status=status.HTTP_201_CREATED)
    92	
    93	
    94	def list_attachments(request, application_id):
    95	    user = request.user
    96	
    97	    # Get application
    98	    try:
    99	        application = Application.objects.get(application_id=application_id)
   100	    except Application.DoesNotExist:
   101	        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在'}},
   102	                        status=status.HTTP_404_NOT_FOUND)
   103	
   104	    # Permission check using shared helper
   105	    if not can_view_application(user, application):
   106	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限查看附件'}},
   107	                        status=status.HTTP_403_FORBIDDEN)
   108	
   109	    # List attachments (exclude soft-deleted)
   110	    attachments = Attachment.objects.filter(application=application, is_deleted=False)
   111	    serializer = AttachmentSerializer(attachments, many=True)
   112	    return Response({'attachments': serializer.data})
   113	
   114	
   115	@extend_schema(
   116	    operation_id='attachments_download',
   117	    summary='下载附件',
   118	    description='下载指定附件文件',
   119	    responses={
   120	        200: OpenApiResponse(description='附件文件内容'),
   121	        403: ErrorResponseSerializer,
   122	        404: ErrorResponseSerializer,
   123	    },
   124	    tags=['附件']
   125	)
   126	@api_view(['GET'])
   127	@permission_classes([IsAuthenticated])
   128	def download_attachment(request, attachment_id):
   129	    user = request.user
   130	
   131	    # Get attachment
   132	    try:
   133	        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
   134	    except Attachment.DoesNotExist:
   135	        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
   136	                        status=status.HTTP_404_NOT_FOUND)
   137	
   138	    # Check if soft-deleted
   139	    if attachment.is_deleted:
   140	        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
   141	                        status=status.HTTP_404_NOT_FOUND)
   142	
   143	    # Permission check using shared helper
   144	    application = attachment.application
   145	    if not can_view_application(user, application):
   146	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限下载附件'}},
   147	                        status=status.HTTP_403_FORBIDDEN)
   148	
   149	    # Return file
   150	    try:
   151	        return FileResponse(attachment.file.open('rb'), as_attachment=True, filename=attachment.file_name, content_type=attachment.content_type)
   152	    except FileNotFoundError:
   153	        return Response({'error': {'code': 'NOT_FOUND', 'message': '文件不存在'}},
   154	                        status=status.HTTP_404_NOT_FOUND)
   155	
   156	
   157	@extend_schema(
   158	    operation_id='attachments_delete',
   159	    summary='删除附件',
   160	    description='软删除指定附件（仅申请所有者可删除）',
   161	    request=None,
   162	    responses={
   163	        204: OpenApiResponse(description='删除成功'),
   164	        403: ErrorResponseSerializer,
   165	        404: ErrorResponseSerializer,
   166	    },
   167	    tags=['附件']
   168	)
   169	@api_view(['DELETE'])
   170	@permission_classes([IsAuthenticated])
   171	def delete_attachment(request, attachment_id):
   172	    user = request.user
   173	
   174	    # Get attachment
   175	    try:
   176	        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
   177	    except Attachment.DoesNotExist:
   178	        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
   179	                        status=status.HTTP_404_NOT_FOUND)
   180	
   181	    # Check if already deleted
   182	    if attachment.is_deleted:
   183	        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
   184	                        status=status.HTTP_404_NOT_FOUND)
   185	
   186	    # Permission: only student who owns the application
   187	    if user.role != UserRole.STUDENT or attachment.application.student_id != user.user_id:
   188	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限删除附件'}},
   189	                        status=status.HTTP_403_FORBIDDEN)
   190	
   191	    # Soft delete
   192	    attachment.is_deleted = True
   193	    attachment.deleted_at = timezone.now()
   194	    attachment.save()
   195	
   196	    return Response(status=status.HTTP_204_NO_CONTENT)

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/permissions.py | sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from apps.users.models import UserRole, User
     2	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
     3	
     4	
     5	def can_view_application(user, application):
     6	    """Check if user can view application and its attachments."""
     7	    if user.role == UserRole.STUDENT:
     8	        return application.student_id == user.user_id
     9	
    10	    if user.role == UserRole.DORM_MANAGER:
    11	        student = User.objects.filter(user_id=application.student_id).first()
    12	        if not student or not student.building:
    13	            return False
    14	        return user.building == student.building
    15	
    16	    if user.role == UserRole.COUNSELOR:
    17	        student = User.objects.filter(user_id=application.student_id).first()
    18	        if not student or not student.department:
    19	            return False
    20	        return user.department == student.department
    21	
    22	    if user.role == UserRole.DEAN:
    23	        # Dean archives completed applications and does not participate in approval.
    24	        return application.status == 'approved'
    25	
    26	    if user.role == UserRole.ADMIN:
    27	        # Admin can view all applications
    28	        return True
    29	
    30	    return False

exec
/bin/bash -lc "rtk nl -ba demo-web/index.html | sed -n '100,390p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   100	      padding: 0 8px;
   101	    }
   102	
   103	    .screen {
   104	      display: none;
   105	      min-height: calc(100vh - 45px);
   106	    }
   107	    .screen.active {
   108	      display: block;
   109	    }
   110	  </style>
   111	</head>
   112	<body>
   113	  <!-- 顶部导航 -->
   114	  <div class="nav-tabs">
   115	    <button class="nav-tab active" onclick="showScreen(0)">学生申请</button>
   116	    <button class="nav-tab" onclick="showScreen(1)"><span id="nav-approval-text">审批列表</span></button>
   117	    <button class="nav-tab" onclick="showScreen(2)">申请详情</button>
   118	  </div>
   119	
   120	  <!-- 角色选择器 -->
   121	  <div style="background: white; padding: 8px 16px; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; gap: 10px;">
   122	    <span style="font-size: 14px; color: #666;">演示角色:</span>
   123	    <select id="roleSelector" onchange="switchRole(this.value)" style="padding: 4px 8px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;">
   124	      <option value="dorm_manager">宿管员</option>
   125	      <option value="counselor">辅导员</option>
   126	      <option value="dean">学工部</option>
   127	    </select>
   128	  </div>
   129	
   130	  <!-- 屏幕1: 学生申请页 -->
   131	  <div class="screen active" id="screen-0">
   132	    <div style="padding: 20px;">
   133	      <!-- 用户信息卡片 -->
   134	      <div class="card" style="margin-bottom: 20px;">
   135	        <div style="font-size: 16px; font-weight: 600; color: var(--primary-color); margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #f0f0f0;">
   136	          申请人信息
   137	        </div>
   138	        <div style="display: flex; align-items: center; padding: 10px 0;">
   139	          <span style="font-size: 14px; color: #666; width: 80px;">姓名</span>
   140	          <span style="font-size: 14px; color: #333;">张三</span>
   141	        </div>
   142	        <div style="display: flex; align-items: center; padding: 10px 0;">
   143	          <span style="font-size: 14px; color: #666; width: 80px;">学号</span>
   144	          <span style="font-size: 14px; color: #333;">2020001</span>
   145	        </div>
   146	      </div>
   147	
   148	      <!-- 表单卡片 -->
   149	      <div class="card">
   150	        <div style="margin-bottom: 20px;">
   151	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">离校原因</label>
   152	          <textarea style="width: 100%; min-height: 120px; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入离校原因"></textarea>
   153	          <span style="display: block; text-align: right; font-size: 12px; color: #999; margin-top: 4px;">0/500</span>
   154	        </div>
   155	        <div style="margin-bottom: 20px;">
   156	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">离校日期</label>
   157	          <input type="date" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;">
   158	        </div>
   159	
   160	        <!-- 附件上传区域 -->
   161	        <div style="margin-bottom: 20px;">
   162	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">附件材料（可选）</label>
   163	          <div class="upload-zone">
   164	            <input type="file" id="fileInput" multiple accept=".jpg,.jpeg,.png,.pdf,.doc,.docx" style="display: none;">
   165	            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
   166	              <div style="font-size: 40px; color: #999; margin-bottom: 8px;">📎</div>
   167	              <div style="font-size: 14px; color: #666;">点击或拖拽文件到此处上传</div>
   168	              <div style="font-size: 12px; color: #999; margin-top: 4px;">支持jpg/png/pdf/doc/docx，单文件不超过10MB</div>
   169	            </div>
   170	          </div>
   171	          <!-- 文件列表 -->
   172	          <div id="fileList" style="margin-top: 12px;"></div>
   173	        </div>
   174	
   175	        <button class="btn-primary">提交申请</button>
   176	      </div>
   177	    </div>
   178	  </div>
   179	
   180	  <!-- 屏幕2: 审批列表页 -->
   181	  <div class="screen" id="screen-1">
   182	    <div style="background: white; padding: 16px; display: flex; justify-content: space-between; align-items: center;">
   183	      <div style="font-size: 18px; font-weight: bold;" id="list-title">审批列表</div>
   184	      <div style="font-size: 12px; color: #999;" id="role-display">宿管员</div>
   185	    </div>
   186	
   187	    <!-- Tab切换 -->
   188	    <div style="background: white; display: flex; border-bottom: 1px solid #f0f0f0;">
   189	      <div class="nav-tab active" style="flex: 1;">全部</div>
   190	      <div class="nav-tab" style="flex: 1;">待审批</div>
   191	      <div class="nav-tab" style="flex: 1;">已审批</div>
   192	    </div>
   193	
   194	    <div style="padding: 10px;">
   195	      <!-- 列表项 -->
   196	      <div class="card">
   197	        <div class="flex-row justify-between align-center" style="margin-bottom: 8px;">
   198	          <span style="font-size: 16px; font-weight: bold;">申请 APP-001</span>
   199	          <span class="tag tag-pending">待审批</span>
   200	        </div>
   201	        <div style="margin-bottom: 4px;">
   202	          <span style="font-size: 14px; color: #999; margin-right: 8px;">申请ID:</span>
   203	          <span style="font-size: 14px; color: #333;">APP-001</span>
   204	        </div>
   205	        <div style="margin-bottom: 4px;">
   206	          <span style="font-size: 14px; color: #999; margin-right: 8px;">审批步骤:</span>
   207	          <span style="font-size: 14px; color: #333;">宿管员审批</span>
   208	        </div>
   209	        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0f0f0;">
   210	          <span style="font-size: 12px; color: #999;">2024-06-01 10:30</span>
   211	        </div>
   212	      </div>
   213	
   214	      <div class="card">
   215	        <div class="flex-row justify-between align-center" style="margin-bottom: 8px;">
   216	          <span style="font-size: 16px; font-weight: bold;">申请 APP-002</span>
   217	          <span class="tag tag-approved">已通过</span>
   218	        </div>
   219	        <div style="margin-bottom: 4px;">
   220	          <span style="font-size: 14px; color: #999; margin-right: 8px;">申请ID:</span>
   221	          <span style="font-size: 14px; color: #333;">APP-002</span>
   222	        </div>
   223	        <div style="margin-bottom: 4px;">
   224	          <span style="font-size: 14px; color: #999; margin-right: 8px;">审批步骤:</span>
   225	          <span style="font-size: 14px; color: #333;">辅导员审批</span>
   226	        </div>
   227	        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0f0f0;">
   228	          <span style="font-size: 12px; color: #999;">2024-05-30 14:20</span>
   229	        </div>
   230	      </div>
   231	    </div>
   232	  </div>
   233	
   234	  <!-- 屏幕3: 申请详情页 -->
   235	  <div class="screen" id="screen-2">
   236	    <div style="background: white; padding: 16px;">
   237	      <div style="font-size: 18px; font-weight: bold;">申请详情</div>
   238	    </div>
   239	
   240	    <div style="padding: 10px;">
   241	      <!-- 基本信息 -->
   242	      <div class="card">
   243	        <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">基本信息</div>
   244	        <div style="display: flex; margin-bottom: 8px;">
   245	          <span style="font-size: 14px; color: #999; width: 80px;">申请ID:</span>
   246	          <span style="font-size: 14px; color: #333; flex: 1;">APP-001</span>
   247	        </div>
   248	        <div style="display: flex; margin-bottom: 8px;">
   249	          <span style="font-size: 14px; color: #999; width: 80px;">学生:</span>
   250	          <span style="font-size: 14px; color: #333; flex: 1;">张三 (2020001)</span>
   251	        </div>
   252	        <div style="display: flex; margin-bottom: 8px;">
   253	          <span style="font-size: 14px; color: #999; width: 80px;">离校日期:</span>
   254	          <span style="font-size: 14px; color: #333; flex: 1;">2024-06-15</span>
   255	        </div>
   256	        <div style="display: flex; margin-bottom: 8px;">
   257	          <span style="font-size: 14px; color: #999; width: 80px;">申请原因:</span>
   258	          <span style="font-size: 14px; color: #333; flex: 1;">毕业实习，需要提前离校</span>
   259	        </div>
   260	      </div>
   261	
   262	      <!-- 审批记录时间轴 -->
   263	      <div class="card">
   264	        <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">审批记录</div>
   265	
   266	        <!-- 时间轴项 -->
   267	        <div style="position: relative; padding-left: 30px; margin-bottom: 20px;">
   268	          <div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: white; border: 2px solid var(--primary-color);"></div>
   269	          <div style="position: absolute; left: 14px; top: 16px; bottom: -20px; width: 1px; background: #e8e8e8;"></div>
   270	          <div class="flex-row justify-between align-center" style="margin-bottom: 6px;">
   271	            <span style="font-size: 15px; font-weight: 600;">宿管员审批</span>
   272	            <span class="tag tag-pending">待审批</span>
   273	          </div>
   274	          <div style="font-size: 13px; color: #666;">审批人: 李老师</div>
   275	        </div>
   276	
   277	        <div style="position: relative; padding-left: 30px; margin-bottom: 20px;">
   278	          <div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--status-success); border: 2px solid var(--status-success);"></div>
   279	          <div class="flex-row justify-between align-center" style="margin-bottom: 6px;">
   280	            <span style="font-size: 15px; font-weight: 600;">提交申请</span>
   281	            <span class="tag tag-approved">已完成</span>
   282	          </div>
   283	          <div style="font-size: 13px; color: #666;">提交时间: 2024-06-01 10:30</div>
   284	        </div>
   285	      </div>
   286	
   287	      <!-- 审批操作 -->
   288	      <div style="padding: 10px;">
   289	        <div class="card" style="margin-bottom: 10px;">
   290	          <label style="display: block; font-size: 14px; color: #333; margin-bottom: 6px; font-weight: 500;">审批意见（可选）</label>
   291	          <textarea style="width: 100%; min-height: 60px; padding: 8px; border: 1px solid #e8e8e8; border-radius: 4px; font-size: 14px;" placeholder="请输入审批意见"></textarea>
   292	          <span style="display: block; text-align: right; font-size: 12px; color: #999; margin-top: 4px;">0/200</span>
   293	        </div>
   294	        <div style="display: flex; gap: 10px;" id="approval-actions">
   295	          <button class="btn-primary" style="flex: 1;">通过</button>
   296	          <button class="btn-outline" style="flex: 1;">拒绝</button>
   297	        </div>
   298	      </div>
   299	    </div>
   300	  </div>
   301	
   302	  <script>
   303	    let currentRole = 'dorm_manager';
   304	
   305	    function showScreen(index) {
   306	      document.querySelectorAll('.screen').forEach((s, i) => {
   307	        s.classList.toggle('active', i === index);
   308	      });
   309	      document.querySelectorAll('.nav-tabs .nav-tab').forEach((t, i) => {
   310	        t.classList.toggle('active', i === index);
   311	      });
   312	    }
   313	
   314	    function switchRole(role) {
   315	      currentRole = role;
   316	      const roleMap = {
   317	        'dorm_manager': '宿管员',
   318	        'counselor': '辅导员',
   319	        'dean': '学工部'
   320	      };
   321	      const isDean = role === 'dean';
   322	
   323	      // Update nav tab text
   324	      document.getElementById('nav-approval-text').textContent = isDean ? '备案查询' : '审批列表';
   325	
   326	      // Update list page title and role display
   327	      document.getElementById('list-title').textContent = isDean ? '备案查询' : '审批列表';
   328	      document.getElementById('role-display').textContent = roleMap[role];
   329	
   330	      // Show/hide approval buttons
   331	      const approvalActions = document.getElementById('approval-actions');
   332	      if (approvalActions) {
   333	        approvalActions.style.display = isDean ? 'none' : 'flex';
   334	      }
   335	    }
   336	
   337	    // File upload management
   338	    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
   339	    const ALLOWED_TYPES = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx'];
   340	    let uploadedFiles = [];
   341	
   342	    const fileInput = document.getElementById('fileInput');
   343	    const fileList = document.getElementById('fileList');
   344	    const uploadArea = document.querySelector('.upload-area');
   345	
   346	    // File selection handler
   347	    fileInput.addEventListener('change', (e) => {
   348	      handleFiles(e.target.files);
   349	    });
   350	
   351	    // Drag and drop handlers
   352	    uploadArea.addEventListener('dragover', (e) => {
   353	      e.preventDefault();
   354	      uploadArea.style.borderColor = 'var(--primary-color)';
   355	      uploadArea.style.background = '#fafafa';
   356	    });
   357	
   358	    uploadArea.addEventListener('dragleave', () => {
   359	      uploadArea.style.borderColor = '#d9d9d9';
   360	      uploadArea.style.background = 'white';
   361	    });
   362	
   363	    uploadArea.addEventListener('drop', (e) => {
   364	      e.preventDefault();
   365	      uploadArea.style.borderColor = '#d9d9d9';
   366	      uploadArea.style.background = 'white';
   367	      handleFiles(e.dataTransfer.files);
   368	    });
   369	
   370	    function handleFiles(files) {
   371	      const validFiles = [];
   372	      const errors = [];
   373	
   374	      Array.from(files).forEach(file => {
   375	        const ext = '.' + file.name.split('.').pop().toLowerCase();
   376	
   377	        if (!ALLOWED_TYPES.includes(ext)) {
   378	          errors.push(`${file.name}: 不支持的文件格式`);
   379	          return;
   380	        }
   381	
   382	        if (file.size > MAX_FILE_SIZE) {
   383	          errors.push(`${file.name}: 文件大小超过10MB`);
   384	          return;
   385	        }
   386	
   387	        validFiles.push(file);
   388	      });
   389	
   390	      if (errors.length > 0) {

exec
/bin/bash -lc "rtk nl -ba backend/apps/users/models.py | sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
     2	from django.db import models
     3	
     4	
     5	class UserRole(models.TextChoices):
     6	    STUDENT = 'student', '学生'
     7	    DORM_MANAGER = 'dorm_manager', '宿管员'
     8	    COUNSELOR = 'counselor', '辅导员'
     9	    DEAN = 'dean', '学工部'
    10	    ADMIN = 'admin', '学工管理员'
    11	
    12	
    13	class UserManager(BaseUserManager):
    14	    def create_user(self, user_id, password=None, **extra_fields):
    15	        if not user_id:
    16	            raise ValueError('user_id is required')
    17	        user = self.model(user_id=user_id, **extra_fields)
    18	        user.set_password(password)
    19	        user.save(using=self._db)
    20	        return user
    21	
    22	    def create_superuser(self, user_id, password=None, **extra_fields):
    23	        extra_fields.setdefault('is_staff', True)
    24	        extra_fields.setdefault('is_superuser', True)
    25	        extra_fields.setdefault('active', True)
    26	        return self.create_user(user_id, password, **extra_fields)
    27	
    28	
    29	class User(AbstractBaseUser, PermissionsMixin):
    30	    user_id = models.CharField(max_length=50, unique=True, primary_key=True)
    31	    name = models.CharField(max_length=100)
    32	    role = models.CharField(max_length=20, choices=UserRole.choices)
    33	    active = models.BooleanField(default=True)
    34	    class_id = models.CharField(max_length=50, null=True, blank=True)
    35	    is_graduating = models.BooleanField(null=True, blank=True)
    36	    graduation_year = models.IntegerField(null=True, blank=True)
    37	
    38	    # API补充字段（学工系统）
    39	    phone = models.CharField(max_length=20, null=True, blank=True)
    40	    email = models.EmailField(null=True, blank=True)
    41	    department = models.CharField(max_length=100, null=True, blank=True)
    42	    building = models.CharField(max_length=100, null=True, blank=True)
    43	
    44	    is_staff = models.BooleanField(default=False)
    45	    created_at = models.DateTimeField(auto_now_add=True)
    46	    updated_at = models.DateTimeField(auto_now=True)
    47	
    48	    objects = UserManager()
    49	
    50	    USERNAME_FIELD = 'user_id'
    51	    REQUIRED_FIELDS = ['name', 'role']
    52	
    53	    class Meta:
    54	        db_table = 'users'
    55	
    56	    def __str__(self):
    57	        return f"{self.user_id} - {self.name}"

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/validators.py | sed -n '1,80p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from apps.applications.models import ApplicationStatus
     2	
     3	
     4	EXPECTED_STATUS_BY_STEP = {
     5	    'dorm_manager': ApplicationStatus.PENDING_DORM_MANAGER,
     6	    'counselor': ApplicationStatus.PENDING_COUNSELOR,
     7	}
     8	
     9	
    10	def approval_step_matches_application_status(approval):
    11	    expected_status = EXPECTED_STATUS_BY_STEP.get(approval.step)
    12	    if expected_status is None:
    13	        return False
    14	    return approval.application.status == expected_status

exec
/bin/bash -lc "rtk nl -ba demo-web/index.html | sed -n '390,430p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   390	      if (errors.length > 0) {
   391	        alert(errors.join('\n'));
   392	      }
   393	
   394	      uploadedFiles = uploadedFiles.concat(validFiles);
   395	      renderFileList();
   396	      fileInput.value = ''; // Reset input
   397	    }
   398	
   399	    function renderFileList() {
   400	      fileList.innerHTML = uploadedFiles.map((file, index) => `
   401	        <div class="file-item">
   402	          <span style="font-size: 20px;">📄</span>
   403	          <div class="file-info">
   404	            <div class="file-name">${file.name}</div>
   405	            <div class="file-size">${formatFileSize(file.size)}</div>
   406	          </div>
   407	          <button class="btn-delete" onclick="removeFile(${index})" type="button">×</button>
   408	        </div>
   409	      `).join('');
   410	    }
   411	
   412	    function removeFile(index) {
   413	      uploadedFiles.splice(index, 1);
   414	      renderFileList();
   415	    }
   416	
   417	    function formatFileSize(bytes) {
   418	      if (bytes < 1024) return bytes + ' B';
   419	      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
   420	      return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
   421	    }
   422	  </script>
   423	</body>
   424	</html>

exec
/bin/bash -lc "rtk rg -n \"fetch\\(|axios|localhost:8001|/api/|contact_phone|pending_dorm_manager|pending_counselor|approved|rejected|dorm_checkout|attachment_type|comment|opinion|approve|reject\" demo-web/index.html" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
217:          <span class="tag tag-approved">已通过</span>
281:            <span class="tag tag-approved">已完成</span>

exec
/bin/bash -lc "rtk rg -n \"pending_dorm_manager|PENDING_DORM_MANAGER|DORM_MANAGER|PENDING_COUNSELOR|APPROVED|REJECTED|contact_phone|leave_date|dorm_checkout|AttachmentType|attachment_type\" backend/apps/applications/tests backend/apps/approvals/tests backend/apps/attachments/tests -g '*.py'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/attachments/tests/test_list.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_list.py:87:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_list.py:88:            status=ApplicationStatus.APPROVED
backend/apps/attachments/tests/test_list.py:97:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_delete.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_delete.py:64:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_delete.py:65:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/attachments/tests/test_delete.py:75:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/approvals/tests/test_permissions.py:50:            role=UserRole.DORM_MANAGER,
backend/apps/approvals/tests/test_permissions.py:57:            role=UserRole.DORM_MANAGER,
backend/apps/approvals/tests/test_permissions.py:99:            leave_date='2024-06-30',
backend/apps/approvals/tests/test_permissions.py:100:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/approvals/tests/test_permissions.py:116:        self.application1.status = ApplicationStatus.PENDING_DORM_MANAGER
backend/apps/approvals/tests/test_permissions.py:121:            step=ApprovalStep.DORM_MANAGER,
backend/apps/applications/tests/test_p0_fixes.py:38:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:39:            status=ApplicationStatus.REJECTED
backend/apps/applications/tests/test_p0_fixes.py:49:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:50:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:54:        self.assertEqual(app2.status, ApplicationStatus.PENDING_COUNSELOR)
backend/apps/applications/tests/test_p0_fixes.py:64:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:65:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:75:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:76:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:105:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:106:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:115:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:116:            status=ApplicationStatus.APPROVED
backend/apps/applications/tests/test_p0_fixes.py:125:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:126:            status=ApplicationStatus.REJECTED
backend/apps/applications/tests/test_p0_fixes.py:145:            decision=ApprovalDecision.APPROVED
backend/apps/applications/tests/test_p0_fixes.py:154:            decision=ApprovalDecision.REJECTED
backend/apps/applications/tests/test_p0_fixes.py:168:            decision=ApprovalDecision.APPROVED
backend/apps/applications/tests/test_p0_fixes.py:176:            decision=ApprovalDecision.REJECTED
backend/apps/approvals/tests/test_state_machine.py:36:            role=UserRole.DORM_MANAGER,
backend/apps/approvals/tests/test_state_machine.py:66:            leave_date='2024-06-30',
backend/apps/approvals/tests/test_state_machine.py:67:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/approvals/tests/test_state_machine.py:122:        self.application.status = ApplicationStatus.PENDING_DORM_MANAGER
backend/apps/approvals/tests/test_state_machine.py:140:    def test_dorm_manager_step_requires_pending_dorm_manager_status(self):
backend/apps/approvals/tests/test_state_machine.py:142:        self.application.status = ApplicationStatus.APPROVED
backend/apps/approvals/tests/test_state_machine.py:147:            step=ApprovalStep.DORM_MANAGER,
backend/apps/applications/tests/test_error_cases.py:63:            role=UserRole.DORM_MANAGER,
backend/apps/applications/tests/test_error_cases.py:94:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_error_cases.py:96:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_error_cases.py:113:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_error_cases.py:115:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_error_cases.py:121:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_error_cases.py:123:            'leave_date': (timezone.now().date() + timedelta(days=2)).isoformat()
backend/apps/applications/tests/test_error_cases.py:139:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_error_cases.py:141:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_error_cases.py:182:            # Missing leave_date
backend/apps/approvals/tests/test_rejection_flow.py:40:            role=UserRole.DORM_MANAGER,
backend/apps/approvals/tests/test_rejection_flow.py:64:            'contact_phone': '13800138000',
backend/apps/approvals/tests/test_rejection_flow.py:66:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/approvals/tests/test_rejection_flow.py:78:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/approvals/tests/test_rejection_flow.py:97:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/approvals/tests/test_rejection_flow.py:104:        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)
backend/apps/approvals/tests/test_rejection_flow.py:107:        self.assertEqual(application.status, ApplicationStatus.REJECTED)
backend/apps/approvals/tests/test_rejection_flow.py:130:        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)
backend/apps/approvals/tests/test_rejection_flow.py:134:        self.assertEqual(application.status, ApplicationStatus.REJECTED)
backend/apps/applications/tests/test_detail_permissions.py:32:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER, building='1号楼')
backend/apps/applications/tests/test_detail_permissions.py:36:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER, building='2号楼')
backend/apps/applications/tests/test_detail_permissions.py:57:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_detail_permissions.py:59:            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_detail_permissions.py:74:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_detail_permissions.py:76:            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_detail_permissions.py:91:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_detail_permissions.py:93:            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
backend/apps/approvals/tests/test_list_permissions.py:25:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
backend/apps/approvals/tests/test_list_permissions.py:29:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
backend/apps/approvals/tests/test_list_permissions.py:48:            leave_date='2024-07-01',
backend/apps/approvals/tests/test_list_permissions.py:49:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/approvals/tests/test_list_permissions.py:65:            step=ApprovalStep.DORM_MANAGER,
backend/apps/approvals/tests/test_list_permissions.py:123:            leave_date='2024-07-02',
backend/apps/approvals/tests/test_list_permissions.py:124:            status=ApplicationStatus.APPROVED
backend/apps/approvals/tests/test_list_permissions.py:132:            decision=ApprovalDecision.APPROVED
backend/apps/approvals/tests/test_list_permissions.py:142:            leave_date='2024-07-03',
backend/apps/approvals/tests/test_list_permissions.py:143:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_application_flow.py:41:            role=UserRole.DORM_MANAGER,
backend/apps/applications/tests/test_application_flow.py:76:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_application_flow.py:78:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_application_flow.py:81:        self.assertEqual(response.data['status'], ApplicationStatus.PENDING_DORM_MANAGER)
backend/apps/applications/tests/test_application_flow.py:93:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/applications/tests/test_application_flow.py:100:        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)
backend/apps/applications/tests/test_application_flow.py:103:        self.assertEqual(application.status, ApplicationStatus.PENDING_COUNSELOR)
backend/apps/applications/tests/test_application_flow.py:120:        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)
backend/apps/applications/tests/test_application_flow.py:124:        self.assertEqual(application.status, ApplicationStatus.APPROVED)
backend/apps/applications/tests/test_application_flow.py:130:        self.assertEqual(response.data['status'], ApplicationStatus.APPROVED)
backend/apps/applications/tests/test_serializer_validation.py:12:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:14:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:23:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:25:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:31:    def test_leave_date_past(self):
backend/apps/applications/tests/test_serializer_validation.py:32:        """Test leave_date field rejects dates before today"""
backend/apps/applications/tests/test_serializer_validation.py:34:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:36:            'leave_date': (timezone.now().date() - timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:40:        self.assertIn('leave_date', serializer.errors)
backend/apps/applications/tests/test_serializer_validation.py:42:    def test_leave_date_today(self):
backend/apps/applications/tests/test_serializer_validation.py:43:        """Test leave_date field accepts today"""
backend/apps/applications/tests/test_serializer_validation.py:45:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:47:            'leave_date': timezone.now().date().isoformat()
backend/apps/applications/tests/test_serializer_validation.py:55:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:57:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_serializer_validation.py:64:    def test_leave_date_validation_at_midnight_boundary(self, mock_now):
backend/apps/applications/tests/test_serializer_validation.py:65:        """Test leave_date validation at 23:59:59 boundary"""
backend/apps/applications/tests/test_serializer_validation.py:72:        # Submit with leave_date=tomorrow (2026-06-02)
backend/apps/applications/tests/test_serializer_validation.py:74:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:76:            'leave_date': '2026-06-02'
backend/apps/applications/tests/test_serializer_validation.py:82:    def test_leave_date_validation_after_midnight(self, mock_now):
backend/apps/applications/tests/test_serializer_validation.py:83:        """Test leave_date validation rejects past date after midnight"""
backend/apps/applications/tests/test_serializer_validation.py:90:        # Submit with leave_date=yesterday (2026-06-01)
backend/apps/applications/tests/test_serializer_validation.py:92:            'contact_phone': '13800138000',
backend/apps/applications/tests/test_serializer_validation.py:94:            'leave_date': '2026-06-01'
backend/apps/applications/tests/test_serializer_validation.py:98:        self.assertIn('leave_date', serializer.errors)
backend/apps/applications/tests/test_list_permissions.py:30:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
backend/apps/applications/tests/test_list_permissions.py:34:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
backend/apps/applications/tests/test_list_permissions.py:53:            leave_date='2024-07-01',
backend/apps/applications/tests/test_list_permissions.py:54:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/applications/tests/test_list_permissions.py:63:            leave_date='2024-07-01',
backend/apps/applications/tests/test_list_permissions.py:64:            status=ApplicationStatus.APPROVED
backend/apps/attachments/tests/test_download.py:9:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_download.py:65:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_download.py:66:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/attachments/tests/test_download.py:76:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/applications/tests/test_constraints.py:37:            role=UserRole.DORM_MANAGER,
backend/apps/applications/tests/test_constraints.py:62:                'contact_phone': '13800138000',
backend/apps/applications/tests/test_constraints.py:64:                'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/applications/tests/test_constraints.py:74:                'contact_phone': '13800138000',
backend/apps/applications/tests/test_constraints.py:76:                'leave_date': (timezone.now().date() + timedelta(days=2)).isoformat()
backend/apps/attachments/tests/test_upload.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_upload.py:65:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_upload.py:66:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/attachments/tests/test_upload.py:76:            leave_date='2024-07-01',
backend/apps/attachments/tests/test_upload.py:77:            status=ApplicationStatus.PENDING_COUNSELOR
backend/apps/attachments/tests/test_upload.py:89:                'attachment_type': AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_upload.py:99:        self.assertEqual(response.data['attachment_type'], AttachmentType.DORM_CHECKOUT)
backend/apps/attachments/tests/test_upload.py:111:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:128:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:143:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:154:        """Upload fails with missing attachment_type"""
backend/apps/attachments/tests/test_upload.py:169:        self.assertIn('attachment_type', response.data['error']['details'])

codex
**结论**

`demo-web/index.html` 目前更像静态 UI 草图，不是按后端真实流程运行的 demo。它没有接入 `http://localhost:8001`，也没有完整表达“学生提交 -> 宿管员审批 -> 辅导员审批 -> approved/rejected”的两级审批链路。

**1. 当前 UI 与业务流程差异**

1. 审批流程展示不完整  
   后端真实状态是 `pending_dorm_manager -> pending_counselor -> approved/rejected`，见 [models.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/models.py:6)。宿管通过后进入辅导员审批，辅导员通过后最终 `approved`，见 [views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:179)。  
   当前详情时间轴只显示“宿管员审批 + 提交申请”，没有辅导员审批节点，也没有最终状态节点，见 [index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:267)。

2. 表单字段与 API 不匹配  
   后端提交申请必填 `contact_phone`、`leave_date`，`reason` 可选，见 [serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/serializers.py:35)。  
   当前 UI 只有“离校原因”和“离校日期”，缺少必填联系电话 `contact_phone`，见 [index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:150)。

3. 状态展示不准确  
   当前 UI 只用“待审批 / 已通过 / 已完成”等文案，没有映射 `pending_dorm_manager`、`pending_counselor`、`approved`、`rejected`，也没有区分“待宿管员审批”和“待辅导员审批”。列表里甚至静态展示“辅导员审批 + 已通过”，但不表示申请最终状态，见 [index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:214)。

4. 角色切换不完整  
   后端角色包含 `student`、`dorm_manager`、`counselor`、`dean`、`admin`，见 [models.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/models.py:5)。  
   当前选择器只有宿管员、辅导员、学工部，没有学生角色；“学生申请”页始终可见，角色切换只改标题和是否隐藏审批按钮，不会切换数据源、权限视图或待办步骤，见 [index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:123)。

5. 审批操作未接 API  
   后端审批接口按 `approval_id` 操作：`POST /api/approvals/{approval_id}/approve/` 和 `/reject/`，见 [urls.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/urls.py:4)。请求字段是 `comment`，见 [serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/serializers.py:30)。  
   当前“通过 / 拒绝”按钮没有事件处理，也没有使用 `approval_id` 或提交 `comment`，见 [index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:294)。

6. 附件上传不完整  
   后端附件上传需要 `POST /api/applications/{application_id}/attachments/`，multipart 字段为 `file` 和 `attachment_type`，见 [views.py](/home/caohui/projects/graduation-leave-system/backend/apps/attachments/views.py:56)。  
   当前 UI 只是本地维护 `uploadedFiles`，没有创建草稿、没有拿 `application_id`、没有上传到后端、没有选择 `attachment_type`、没有下载/删除已上传附件列表，见 [index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:337)。

7. 附件类型命名需以后端为准  
   设计文档里有 `dorm_clearance`，但后端当前枚举是 `dorm_checkout`、`library_clearance`、`finance_clearance`、`other`，见 [models.py](/home/caohui/projects/graduation-leave-system/backend/apps/attachments/models.py:6)。UI 如果接后端，应使用后端枚举。

**2. 需要修改的 UI 组件清单**

- 角色选择器：增加 `student`，并按角色控制可见页面和操作权限。
- 学生申请表单：增加 `contact_phone` 必填字段，绑定 `reason`、`leave_date`，提交到 `/api/applications/`。
- 附件上传组件：支持先创建/获取草稿 `/api/applications/draft/`，选择 `attachment_type`，调用上传、列表、下载、删除接口。
- 审批列表：从 `/api/approvals/?decision=pending|approved|rejected|all` 拉取数据，按宿管员/辅导员展示对应 `step`。
- 申请详情：展示 `contact_phone`、`status`、`dorm_checkout_status`、审批记录、附件列表。
- 审批时间轴：按状态动态展示“提交申请、宿管员审批、辅导员审批、最终结果”。
- 审批操作区：只有当前角色匹配待审批 `step` 且 `decision=pending` 时显示；提交 `comment` 到 approve/reject 接口。
- 状态标签组件：建立状态映射：`pending_dorm_manager=待宿管员审批`、`pending_counselor=待辅导员审批`、`approved=已通过`、`rejected=已驳回`。

**3. 优先级修改建议**

P0：先修正流程和字段  
增加 `contact_phone`，接入申请提交 API；修正状态映射；详情页补齐两级审批时间轴。

P1：接入审批视图  
宿管员和辅导员分别读取 `/api/approvals/`，用 `approval_id` 执行 approve/reject，审批意见字段改为 `comment`。

P2：补完整附件能力  
增加 `attachment_type` 选择，支持草稿申请、真实上传、列表展示、下载和删除。

P3：整理角色体验  
学生只看申请/我的申请，宿管员只看宿管审批，辅导员只看辅导员审批，学工部只做 approved 备案查询；避免所有角色共用同一套静态页面。
tokens used
70,834

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
