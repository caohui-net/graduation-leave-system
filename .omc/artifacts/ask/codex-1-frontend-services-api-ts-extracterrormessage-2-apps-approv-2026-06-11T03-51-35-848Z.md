# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-11T03:51:35.848Z

## Original task

请审计本次代码修改：

修改清单：
1. frontend/services/api.ts - 添加extractErrorMessage()方法，优化错误提示
2. apps/approvals/serializers.py - 添加leave_date和attachments字段到审批接口
3. apps/attachments/views.py - 添加preview模式支持（?preview=true参数）
4. 新增前端组件：PC端/移动端/小程序审批详情页，包含附件预览按钮
5. 新增frontend/services/attachment.ts和hooks/useAttachment.ts实现逻辑复用

审查重点：
- API向后兼容性（serializer新增字段是否影响现有客户端）
- 类型安全（frontend/types/api.ts是否需要更新）
- 附件预览权限控制是否充分
- 前端错误处理边界情况（网络错误、超时等）
- 代码复用架构的合理性

请提供具体的审计意见和改进建议。

## Final prompt

请审计本次代码修改：

修改清单：
1. frontend/services/api.ts - 添加extractErrorMessage()方法，优化错误提示
2. apps/approvals/serializers.py - 添加leave_date和attachments字段到审批接口
3. apps/attachments/views.py - 添加preview模式支持（?preview=true参数）
4. 新增前端组件：PC端/移动端/小程序审批详情页，包含附件预览按钮
5. 新增frontend/services/attachment.ts和hooks/useAttachment.ts实现逻辑复用

审查重点：
- API向后兼容性（serializer新增字段是否影响现有客户端）
- 类型安全（frontend/types/api.ts是否需要更新）
- 附件预览权限控制是否充分
- 前端错误处理边界情况（网络错误、超时等）
- 代码复用架构的合理性

请提供具体的审计意见和改进建议。

## Raw output

```text
审计结论：**需要修改后再合并**。主要风险集中在前端附件预览鉴权、类型契约未同步、错误处理对非标准响应不稳，以及附件权限边界不够明确。

**主要问题**

1. **附件预览/下载在 Web 和 React Native 端大概率无法鉴权**
   [frontend/services/attachment.ts](/home/caohui/projects/graduation-leave-system/frontend/services/attachment.ts:20) 使用 `window.open(url)`， [frontend/mobile/ApprovalDetail.tsx](/home/caohui/projects/graduation-leave-system/frontend/mobile/ApprovalDetail.tsx:28) 使用 `Linking.openURL(url)`，都不能携带 `Authorization: Bearer ...`。后端下载接口有 `IsAuthenticated`，如果系统不是 cookie 鉴权，PC/移动端预览和下载会 401。
   建议：复用 `ApiClient.getToken`，用 `fetch(url, { headers: Authorization })` 获取 `Blob` 后 `URL.createObjectURL()` 预览/下载；或后端提供短时签名 URL。不要直接裸开受保护 API URL。

2. **前端类型没有更新，当前 PC 组件会类型错误**
   [frontend/types/api.ts](/home/caohui/projects/graduation-leave-system/frontend/types/api.ts:62) 的 `ApprovalDetail` 缺少 `student_name`、`student_id`、`contact_phone`、`reason`、`leave_date`、`attachments`，也没有导出 `Attachment`，但 [frontend/components/ApprovalDetail.tsx](/home/caohui/projects/graduation-leave-system/frontend/components/ApprovalDetail.tsx:3) 已导入并使用这些字段。
   建议：补充 `Attachment` 接口，并同步 `ApprovalDetail`、`ApprovalListItem` 的真实响应结构。注意后端列表 serializer 当前返回 `id` 和嵌套 `application`，不是前端类型里的 `approval_id/application_id`。

3. **附件下载权限与审批详情权限不一致，可能扩大附件可见范围**
   审批详情只允许审批人或 dean/admin 查看：[backend/apps/approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:129)。附件下载则使用 `can_view_application`：[backend/apps/attachments/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/attachments/views.py:143)，该 helper 允许同楼栋宿管、同学院辅导员、dean/admin 查看：[backend/apps/applications/permissions.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/permissions.py:5)。
   如果业务要求“只有当前审批记录的审批人能看详情附件”，这里权限不充分。建议新增 `can_view_attachment(user, attachment)`，明确按申请所有者、当前/历史审批人、归档角色分别授权，并让附件列表、下载、审批详情三处共用同一策略。

4. **`preview=true` 会把用户上传文件以内联方式返回，需限制可预览 MIME**
   [backend/apps/attachments/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/attachments/views.py:151) 仅通过 query 参数切换 `as_attachment`。上传校验只看扩展名，`content_type` 来自客户端上传值：[backend/apps/attachments/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/attachments/views.py:86)。恶意用户可能上传伪装文件并设置危险 `Content-Type`。
   建议：预览只允许 `image/jpeg/png/gif` 和 `application/pdf`；doc/docx 保持下载或走安全预览服务；响应加 `X-Content-Type-Options: nosniff`，并尽量用服务端探测 MIME。

5. **错误处理优化会丢失结构化错误，并且非 JSON/网络错误边界不足**
   [frontend/services/api.ts](/home/caohui/projects/graduation-leave-system/frontend/services/api.ts:90) 在检查 `response.ok` 前直接 `response.json()`，遇到空响应、HTML 网关错误、502 页面会抛 `SyntaxError`。`extractErrorMessage` 也假设 `data.error.details[field][0]` 一定是字符串：[frontend/services/api.ts](/home/caohui/projects/graduation-leave-system/frontend/services/api.ts:45)。另外原本抛出的 `ApiError` 被改成普通 `Error`：[frontend/services/api.ts](/home/caohui/projects/graduation-leave-system/frontend/services/api.ts:93)，调用方拿不到 `code/status/details`。
   建议：实现 `ApiClientError extends Error`，保留 `status/code/details/raw`；JSON parse 失败时降级为“服务异常”；网络错误、超时用 `AbortController` 和统一中文消息处理。

6. **新增 `attachments` 字段会影响 `ApplicationSerializer` 的响应体和查询量**
   [backend/apps/applications/serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/serializers.py:30) 复用了 `ApprovalSerializer`，而该 serializer 现在会为每个 approval 查询同一个 application 的附件：[backend/apps/approvals/serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/serializers.py:48)。这会让申请详情中的 `approvals[]` 也带附件列表，形成重复 payload 和 N+1。
   建议：拆分 `ApprovalDetailSerializer` 和 `ApprovalInApplicationSerializer`，只在审批详情接口返回附件；或在 view 层 `prefetch_related('application__attachments')` 并避免重复序列化。

7. **小程序实现把 `wx.request` 当 Promise 用，运行时不可靠**
   [frontend/miniprogram/pages/approval-detail/index.js](/home/caohui/projects/graduation-leave-system/frontend/miniprogram/pages/approval-detail/index.js:18) `await wx.request(...)` 在原生小程序 API 下不会按预期返回响应对象，除非项目已有 promisify 包装。`wx.downloadFile` 也没有检查 `statusCode`，403/404 仍可能走 success：[frontend/miniprogram/pages/approval-detail/index.js](/home/caohui/projects/graduation-leave-system/frontend/miniprogram/pages/approval-detail/index.js:39)。
   建议：封装 `request()`/`downloadFile()` Promise 工具，统一检查 `statusCode` 和错误体；文件类型不要从临时路径判断，优先使用附件的 `content_type/file_name`。

8. **代码复用没有真正覆盖多端**
   Web 有 `AttachmentService/useAttachment`，但 React Native 仍手写 URL 拼接：[frontend/mobile/ApprovalDetail.tsx](/home/caohui/projects/graduation-leave-system/frontend/mobile/ApprovalDetail.tsx:28)，小程序也单独拼接 URL。当前复用只覆盖 PC。
   建议：抽出纯函数 `buildAttachmentPreviewUrl/buildAttachmentDownloadUrl` 和平台适配层：Web 用 Blob URL，RN 用带 header 的下载/文件预览库，小程序用 `wx.downloadFile`。

**API 兼容性判断**

`leave_date` 和 `attachments` 作为只读新增响应字段，对宽松 JSON 客户端通常是向后兼容的。但如果已有客户端做精确 schema 校验，或依赖 `ApprovalSerializer` 在申请详情里不包含附件，则可能出现兼容问题。建议更新 OpenAPI/前端类型，并补充契约测试。

**验证情况**

我尝试运行定向 Django 测试。`pytest` 未收集到测试；用 `backend/venv/bin/python backend/manage.py test ... --keepdb` 运行后失败，原因包括现有测试库缺少 `class_mappings` 表，以及审批列表测试仍期望 `approval_id` 但 serializer 返回 `id`。因此本次审计没有拿到通过的自动化测试结果。


OpenAI Codex v0.138.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019eb4ca-3c81-7811-b549-c1cc58b0aa27
--------
user
请审计本次代码修改：

修改清单：
1. frontend/services/api.ts - 添加extractErrorMessage()方法，优化错误提示
2. apps/approvals/serializers.py - 添加leave_date和attachments字段到审批接口
3. apps/attachments/views.py - 添加preview模式支持（?preview=true参数）
4. 新增前端组件：PC端/移动端/小程序审批详情页，包含附件预览按钮
5. 新增frontend/services/attachment.ts和hooks/useAttachment.ts实现逻辑复用

审查重点：
- API向后兼容性（serializer新增字段是否影响现有客户端）
- 类型安全（frontend/types/api.ts是否需要更新）
- 附件预览权限控制是否充分
- 前端错误处理边界情况（网络错误、超时等）
- 代码复用架构的合理性

请提供具体的审计意见和改进建议。
codex
我会按项目的审查流程先读取本地规则和 Codex review 协议，然后再看本次改动的 diff 与相关实现。审计会以风险和可执行改进为主，不会直接改代码。
exec
/bin/bash -lc "sed -n '1,260p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "sed -n '1,220p' /home/caohui/.codex/RTK.md" in /home/caohui/projects/graduation-leave-system
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
RTK 规则要求后续所有 shell 命令都用 `rtk` 前缀；我已确认审查协议内容。接下来我会读取协作协议和当前 diff，先确定实际变更范围再逐项审计。
exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 D .claude/skills/claude-codex-collab/SKILL.md
 D .claude/skills/claude-codex-collab/assets/protocol.md
 D .claude/skills/claude-codex-collab/scripts/collab_event.py
 D .claude/skills/claude-codex-collab/scripts/collab_init.py
 D .claude/skills/claude-codex-collab/scripts/collab_status.py
 D .claude/skills/claude-codex-collab/scripts/collab_task.py
 D .claude/skills/claude-codex-collab/scripts/collab_validate.py
 M .omc/project-memory.json
 D .omc/state/agent-replay-60cdae76-a26f-4a8e-b614-137cc704545b.jsonl
 M .omc/state/hud-stdin-cache.json
 M .omc/state/last-tool-error.json
 D .omc/state/sessions/60cdae76-a26f-4a8e-b614-137cc704545b/session-started.json
 M .wolf/anatomy.md
 M .wolf/hooks/_session.json
 M .wolf/memory.md
 M .wolf/token-ledger.json
 M backend/.omc/state/last-tool-error.json
 M backend/apps/approvals/serializers.py
 M backend/apps/attachments/views.py
 M backend/apps/sso_qingganlian/client.py
 M backend/apps/sso_qingganlian/settings.py
 M backend/apps/sso_qingganlian/urls.py
 M backend/apps/sso_qingganlian/views.py
 M demo-web/js/api.js
 M demo-web/mobile-sso-callback.html
 M docker-compose.yml
 M frontend/services/api.ts
?? .claude/skills/claude-codex-gemini-collab
?? .collab/
?? .omc/sessions/60cdae76-a26f-4a8e-b614-137cc704545b.json
?? .omc/state/agent-replay-d6e66725-4b67-4dd4-a5e4-db4b7079be97.jsonl
?? .omc/state/checkpoints/checkpoint-2026-06-10T07-26-05-437Z.json
?? .omc/state/checkpoints/checkpoint-2026-06-10T09-20-45-171Z.json
?? .omc/state/sessions/d6e66725-4b67-4dd4-a5e4-db4b7079be97/
?? .omc/state/subagent-tracking.json
?? docs/.omc/
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260610151330_176_1559.png"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260610151330_177_1559.png"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260610152135_183_1559.png"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260610152136_184_1559.png"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260610170155_635_2.png"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260610171038_1027_47.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260610173058_1042_47.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260610173058_1043_47.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260610173059_1044_47.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260610174545_241_1559.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260610174834_244_1559.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260610174850_246_1559.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260611100206_1072_47.png"
?? frontend-server.service
?? frontend/.omc/
?? frontend/components/
?? frontend/hooks/
?? frontend/miniprogram/
?? frontend/mobile/
?? frontend/services/attachment.ts
?? replace_script.js
?? replace_script2.js
?? replace_script3.js
?? replace_script4.js
?? scripts/setup-systemd.sh
?? scripts/start-services.sh
exec
/bin/bash -lc 'rtk git diff --stat' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
.claude/skills/claude-codex-collab/SKILL.md        |  167 -
 .../skills/claude-codex-collab/assets/protocol.md  |  280 -
 .../claude-codex-collab/scripts/collab_event.py    |  143 -
 .../claude-codex-collab/scripts/collab_init.py     |   67 -
 .../claude-codex-collab/scripts/collab_status.py   |   89 -
 .../claude-codex-collab/scripts/collab_task.py     |  140 -
 .../claude-codex-collab/scripts/collab_validate.py |  142 -
 .omc/project-memory.json                           |    4 +-
 ...play-60cdae76-a26f-4a8e-b614-137cc704545b.jsonl |    2 -
 .omc/state/hud-stdin-cache.json                    |    2 +-
 .omc/state/last-tool-error.json                    |    8 +-
 .../session-started.json                           |    7 -
 .wolf/anatomy.md                                   |   61 +-
 .wolf/hooks/_session.json                          |  202 +-
 .wolf/memory.md                                    |  147 +
 .wolf/token-ledger.json                            | 9408 +++++++++++++++++++-
 backend/.omc/state/last-tool-error.json            |    4 +-
 backend/apps/approvals/serializers.py              |   14 +-
 backend/apps/attachments/views.py                  |    9 +-
 backend/apps/sso_qingganlian/client.py             |   23 +-
 backend/apps/sso_qingganlian/settings.py           |   18 +-
 backend/apps/sso_qingganlian/urls.py               |    1 +
 backend/apps/sso_qingganlian/views.py              |  113 +
 demo-web/js/api.js                                 |    2 +-
 demo-web/mobile-sso-callback.html                  |   85 +-
 docker-compose.yml                                 |    2 +
 frontend/services/api.ts                           |   41 +-
 27 files changed, 9986 insertions(+), 1195 deletions(-)

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
当前工作区有大量非本次审计相关的未提交/状态文件变更。我会把审查范围收敛到你列出的后端接口、附件预览和新增前端审批详情相关文件，避免把协作状态文件噪声混进结论。
exec
/bin/bash -lc 'rtk git diff -- backend/apps/approvals/serializers.py backend/apps/attachments/views.py frontend/services/api.ts' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/approvals/serializers.py | 14 ++++++++++--
 backend/apps/attachments/views.py     |  9 +++++++-
 frontend/services/api.ts              | 41 ++++++++++++++++++++++++++++++++++-
 3 files changed, 60 insertions(+), 4 deletions(-)

--- Changes ---

backend/apps/approvals/serializers.py
  @@ -8,6 +8,7 @@ class ApplicationBriefSerializer(serializers.Serializer):
  +    leave_date = serializers.DateField()
   
   
   class ApprovalListSerializer(serializers.ModelSerializer):
  @@ -31,17 +32,26 @@ class ApprovalSerializer(serializers.ModelSerializer):
  +    leave_date = serializers.DateField(source='application.leave_date', read_only=True)
  +    attachments = serializers.SerializerMethodField()
       approver_id = serializers.CharField(source='approver.user_id', read_only=True)
   
       class Meta:
           model = Approval
           fields = ['approval_id', 'application_id', 'student_name', 'student_id',
  -                  'contact_phone', 'reason', 'step', 'approver_id',
  +                  'contact_phone', 'reason', 'leave_date', 'attachments', 'step', 'approver_id',
                     'approver_name', 'decision', 'comment', 'decided_at']
           read_only_fields = ['approval_id', 'application_id', 'student_name', 'student_id',
  -                            'contact_phone', 'reason', 'step',
  +                            'contact_phone', 'reason', 'leave_date', 'attachments', 'step',
                               'approver_id', 'approver_name', 'decision', 'decided_at']
   
  +    def get_attachments(self, obj):
  +        from apps.attachments.serializers import AttachmentSerializer
  +        return AttachmentSerializer(
  +            obj.application.attachments.filter(is_deleted=False),
  +            many=True
  +        ).data
  +
   
   class ApprovalActionSerializer(serializers.Serializer):
       comment = serializers.CharField(required=False, allow_blank=True)
  +12 -2

backend/apps/attachments/views.py
  @@ -148,7 +148,14 @@ def download_attachment(request, attachment_id):
  -        return FileResponse(attachment.file.open('rb'), as_attachment=True, filename=attachment.file_name, content_type=attachment.content_type)
  +        # Check if preview mode (query param: ?preview=true)
  +        preview_mode = request.GET.get('preview', 'false').lower() == 'true'
  +        return FileResponse(
  +            attachment.file.open('rb'),
  +            as_attachment=not preview_mode,
  +            filename=attachment.file_name,
  +            content_type=attachment.content_type
  +        )
       except FileNotFoundError:
           return Response({'error': {'code': 'NOT_FOUND', 'message': '文件不存在'}},
                           status=status.HTTP_404_NOT_FOUND)
  +8 -1

frontend/services/api.ts
  @@ -27,6 +27,42 @@ export class ApiClient {
  +  private extractErrorMessage(apiError: ApiError): string {
  +    const { error } = apiError;
  +
  +    // 字段名映射（英文 -> 中文）
  +    const fieldNames: Record<string, string> = {
  +      contact_phone: '联系电话',
  +      leave_date: '离校日期',
  +      reason: '离校原因',
  +      file: '附件',
  +      user_id: '用户ID',
  +      password: '密码',
  +      comment: '审批意见',
  +    };
  +
  +    // 如果有详细错误信息（字段验证错误）
  +    if (error.details) {
  +      // 提取第一个字段的第一个错误
  +      const firstField = Object.keys(error.details)[0];
  +      if (firstField && Array.isArray(error.details[firstField])) {
  +        const fieldError = error.details[firstField][0];
  +        const fieldLabel = fieldNames[firstField] || firstField;
  +
  +        // 如果错误消息已经很具体，直接返回
  +        if (fieldError.includes('不能') || fieldError.includes('超过') || fieldError.includes('支持')) {
  +          return fieldError;
  +        }
  +
  +        // 否则加上字段名前缀
  +        return `${fieldLabel}：${fieldError}`;
  +      }
  +    }
  +
  +    // 否则返回通用错误消息
  +    return error.message || '操作失败，请稍后重试';
  +  }
  +
     private async request<T>(
       endpoint: string,
       options: RequestInit = {}
  @@ -54,7 +90,10 @@ export class ApiClient {
  -      throw data as ApiError;
  +      const apiError = data as ApiError;
  +      // 提取详细错误信息
  +      const errorMessage = this.extractErrorMessage(apiError);
  +      throw new Error(errorMessage);
       }
   
       return data as T;
  +40 -1

exec
/bin/bash -lc 'rtk rg --files frontend | sort' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
frontend/components/ApprovalDetail.tsx
frontend/hooks/useAttachment.ts
frontend/miniprogram/pages/approval-detail/index.js
frontend/miniprogram/pages/approval-detail/index.wxml
frontend/mobile/ApprovalDetail.tsx
frontend/services/api.ts
frontend/services/attachment.ts
frontend/services/mock.ts
frontend/types/api.ts

exec
/bin/bash -lc 'rtk rg -n "Attachment|attachment|approve|approval|leave_date|preview|extractErrorMessage|useAttachment|types/api" frontend backend/apps/approvals backend/apps/attachments -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/approvals/validators.py:10:def approval_step_matches_application_status(approval):
backend/apps/approvals/validators.py:11:    expected_status = EXPECTED_STATUS_BY_STEP.get(approval.step)
backend/apps/approvals/validators.py:14:    return approval.application.status == expected_status
backend/apps/approvals/admin.py:7:    list_display = ['approval_id', 'application', 'step', 'approver', 'decision', 'decided_at']
backend/apps/approvals/admin.py:9:    search_fields = ['approval_id', 'application__application_id', 'approver__user_id']
backend/apps/approvals/urls.py:5:    path('', views.list_approvals, name='list_approvals'),
backend/apps/approvals/urls.py:6:    path('export/', views.export_approvals, name='export_approvals'),
backend/apps/approvals/urls.py:7:    path('<str:approval_id>/', views.get_approval, name='get_approval'),
backend/apps/approvals/urls.py:8:    path('<str:approval_id>/approve/', views.approve_approval, name='approve_approval'),
backend/apps/approvals/urls.py:9:    path('<str:approval_id>/reject/', views.reject_approval, name='reject_approval'),
backend/apps/attachments/urls.py:5:    path('applications/<str:application_id>/attachments/', views.attachments_view, name='attachments'),
backend/apps/attachments/urls.py:6:    path('attachments/<str:attachment_id>/download/', views.download_attachment, name='download_attachment'),
backend/apps/attachments/urls.py:7:    path('attachments/<str:attachment_id>/', views.delete_attachment, name='delete_attachment'),
frontend/services/attachment.ts:2:export class AttachmentService {
frontend/services/attachment.ts:10:  getPreviewUrl(attachmentId: string): string {
frontend/services/attachment.ts:11:    return `${this.baseUrl}/api/attachments/${attachmentId}/download/?preview=true`;
frontend/services/attachment.ts:15:  getDownloadUrl(attachmentId: string): string {
frontend/services/attachment.ts:16:    return `${this.baseUrl}/api/attachments/${attachmentId}/download/`;
frontend/services/attachment.ts:20:  previewWeb(attachmentId: string): void {
frontend/services/attachment.ts:21:    const url = this.getPreviewUrl(attachmentId);
frontend/services/attachment.ts:26:  downloadWeb(attachmentId: string): void {
frontend/services/attachment.ts:27:    const url = this.getDownloadUrl(attachmentId);
frontend/services/attachment.ts:33:export const attachmentService = new AttachmentService(
backend/apps/approvals/serializers.py:6:    """Brief application info for approval list"""
backend/apps/approvals/serializers.py:11:    leave_date = serializers.DateField()
backend/apps/approvals/serializers.py:15:    """Lean serializer for approval lists - nested application structure"""
backend/apps/approvals/serializers.py:16:    id = serializers.CharField(source='approval_id', read_only=True)
backend/apps/approvals/serializers.py:18:    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
backend/apps/approvals/serializers.py:22:        fields = ['id', 'application', 'step', 'approver_id',
backend/apps/approvals/serializers.py:23:                  'approver_name', 'decision', 'comment', 'decided_at', 'created_at']
backend/apps/approvals/serializers.py:24:        read_only_fields = ['id', 'step', 'approver_id',
backend/apps/approvals/serializers.py:25:                            'approver_name', 'decision', 'comment', 'decided_at', 'created_at']
backend/apps/approvals/serializers.py:29:    """Full approval detail with nested application info"""
backend/apps/approvals/serializers.py:35:    leave_date = serializers.DateField(source='application.leave_date', read_only=True)
backend/apps/approvals/serializers.py:36:    attachments = serializers.SerializerMethodField()
backend/apps/approvals/serializers.py:37:    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
backend/apps/approvals/serializers.py:41:        fields = ['approval_id', 'application_id', 'student_name', 'student_id',
backend/apps/approvals/serializers.py:42:                  'contact_phone', 'reason', 'leave_date', 'attachments', 'step', 'approver_id',
backend/apps/approvals/serializers.py:43:                  'approver_name', 'decision', 'comment', 'decided_at']
backend/apps/approvals/serializers.py:44:        read_only_fields = ['approval_id', 'application_id', 'student_name', 'student_id',
backend/apps/approvals/serializers.py:45:                            'contact_phone', 'reason', 'leave_date', 'attachments', 'step',
backend/apps/approvals/serializers.py:46:                            'approver_id', 'approver_name', 'decision', 'decided_at']
backend/apps/approvals/serializers.py:48:    def get_attachments(self, obj):
backend/apps/approvals/serializers.py:49:        from apps.attachments.serializers import AttachmentSerializer
backend/apps/approvals/serializers.py:50:        return AttachmentSerializer(
backend/apps/approvals/serializers.py:51:            obj.application.attachments.filter(is_deleted=False),
backend/apps/approvals/serializers.py:61:    """Schema-only: approval list response with pagination"""
frontend/services/mock.ts:10:} from '../types/api';
frontend/services/mock.ts:43:      leave_date: '2024-06-30',
frontend/services/mock.ts:57:  leave_date: '2024-06-30',
frontend/services/mock.ts:60:  approvals: [
frontend/services/mock.ts:62:      approval_id: 'apv_c9f566c2',
frontend/services/mock.ts:65:      approver_id: 'T001',
frontend/services/mock.ts:66:      approver_name: '李老师',
frontend/services/mock.ts:80:      approval_id: 'apv_c9f566c2',
frontend/services/mock.ts:83:      approver_id: 'T001',
frontend/services/mock.ts:84:      approver_name: '李老师',
frontend/services/api.ts:15:} from '../types/api';
frontend/services/api.ts:30:  private extractErrorMessage(apiError: ApiError): string {
frontend/services/api.ts:36:      leave_date: '离校日期',
frontend/services/api.ts:95:      const errorMessage = this.extractErrorMessage(apiError);
frontend/services/api.ts:133:    decision: 'pending' | 'approved' | 'rejected' | 'all' = 'pending',
frontend/services/api.ts:138:      `/api/approvals/?decision=${decision}&limit=${limit}&offset=${offset}`
frontend/services/api.ts:142:  async approveApproval(
frontend/services/api.ts:146:    return this.request(`/api/approvals/${id}/approve/`, {
frontend/services/api.ts:156:    return this.request(`/api/approvals/${id}/reject/`, {
backend/apps/approvals/models.py:14:    APPROVED = 'approved', '已通过'
backend/apps/approvals/models.py:19:    approval_id = models.CharField(max_length=50, primary_key=True)
backend/apps/approvals/models.py:20:    application = models.ForeignKey(Application, on_delete=models.PROTECT, related_name='approvals')
backend/apps/approvals/models.py:22:    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals')
backend/apps/approvals/models.py:23:    approver_name = models.CharField(max_length=100)
backend/apps/approvals/models.py:24:    decided_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='decided_approvals', null=True, blank=True, verbose_name='实际审批人')
backend/apps/approvals/models.py:32:        db_table = 'approvals'
backend/apps/attachments/migrations/0001_initial.py:19:            name='Attachment',
backend/apps/attachments/migrations/0001_initial.py:21:                ('attachment_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
backend/apps/attachments/migrations/0001_initial.py:22:                ('file', models.FileField(upload_to='attachments/%Y/%m/%d/')),
backend/apps/attachments/migrations/0001_initial.py:23:                ('attachment_type', models.CharField(choices=[('dorm_checkout', '宿舍清退证明'), ('library_clearance', '图书馆清书证明'), ('finance_clearance', '财务结清证明'), ('other', '其他')], max_length=50)),
backend/apps/attachments/migrations/0001_initial.py:30:                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='applications.application')),
backend/apps/attachments/migrations/0001_initial.py:34:                'db_table': 'attachments',
backend/apps/attachments/serializers.py:2:from .models import Attachment, AttachmentType
backend/apps/attachments/serializers.py:5:class AttachmentUploadSerializer(serializers.Serializer):
backend/apps/attachments/serializers.py:7:    attachment_type = serializers.ChoiceField(choices=AttachmentType.choices)
backend/apps/attachments/serializers.py:23:class AttachmentSerializer(serializers.ModelSerializer):
backend/apps/attachments/serializers.py:25:        model = Attachment
backend/apps/attachments/serializers.py:26:        fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'attachment_type', 'uploaded_at']
backend/apps/attachments/serializers.py:27:        read_only_fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'uploaded_at']
backend/apps/attachments/serializers.py:30:class AttachmentListResponseSerializer(serializers.Serializer):
backend/apps/attachments/serializers.py:31:    """Schema-only: attachment list response with wrapper"""
backend/apps/attachments/serializers.py:32:    attachments = AttachmentSerializer(many=True)
backend/apps/attachments/models.py:6:class AttachmentType(models.TextChoices):
backend/apps/attachments/models.py:13:class Attachment(models.Model):
backend/apps/attachments/models.py:14:    attachment_id = models.CharField(max_length=50, primary_key=True)
backend/apps/attachments/models.py:15:    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='attachments')
backend/apps/attachments/models.py:17:    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
backend/apps/attachments/models.py:18:    attachment_type = models.CharField(max_length=50, choices=AttachmentType.choices)
backend/apps/attachments/models.py:27:        db_table = 'attachments'
backend/apps/attachments/models.py:31:        return f"{self.attachment_id} - {self.file_name}"
backend/apps/attachments/tests/test_list.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_list.py:11:class AttachmentListTestCase(TestCase):
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
frontend/components/ApprovalDetail.tsx:3:import type { ApprovalDetail, Attachment } from '../types/api';
frontend/components/ApprovalDetail.tsx:4:import { useAttachment } from '../hooks/useAttachment';
frontend/components/ApprovalDetail.tsx:7:  approval: ApprovalDetail;
frontend/components/ApprovalDetail.tsx:10:export const ApprovalDetailView: React.FC<Props> = ({ approval }) => {
frontend/components/ApprovalDetail.tsx:11:  const { handlePreview, handleDownload } = useAttachment();
frontend/components/ApprovalDetail.tsx:14:    <div className="approval-detail">
frontend/components/ApprovalDetail.tsx:20:          <span>{approval.student_name}</span>
frontend/components/ApprovalDetail.tsx:24:          <span>{approval.student_id}</span>
frontend/components/ApprovalDetail.tsx:28:          <span>{approval.contact_phone}</span>
frontend/components/ApprovalDetail.tsx:32:          <span>{approval.leave_date}</span>
frontend/components/ApprovalDetail.tsx:36:          <span>{approval.reason}</span>
frontend/components/ApprovalDetail.tsx:41:      {approval.attachments && approval.attachments.length > 0 && (
frontend/components/ApprovalDetail.tsx:42:        <div className="attachments-section">
frontend/components/ApprovalDetail.tsx:44:          {approval.attachments.map((file: Attachment) => (
frontend/components/ApprovalDetail.tsx:45:            <div key={file.attachment_id} className="attachment-item">
frontend/components/ApprovalDetail.tsx:50:              <div className="attachment-actions">
frontend/components/ApprovalDetail.tsx:53:                  className="btn-preview"
frontend/components/ApprovalDetail.tsx:54:                  onClick={() => handlePreview(file.attachment_id)}
frontend/components/ApprovalDetail.tsx:60:                  onClick={() => handleDownload(file.attachment_id)}
frontend/components/ApprovalDetail.tsx:71:      <div className="approval-actions">
frontend/components/ApprovalDetail.tsx:72:        {approval.decision === 'pending' && (
frontend/components/ApprovalDetail.tsx:74:            <button className="btn-approve">通过</button>
backend/apps/attachments/tests/test_upload.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_upload.py:11:class AttachmentUploadTestCase(TestCase):
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
backend/apps/attachments/tests/test_delete.py:11:class AttachmentDeleteTestCase(TestCase):
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
backend/apps/attachments/tests/test_download.py:8:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/attachments/tests/test_download.py:9:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_download.py:12:class AttachmentDownloadTestCase(TestCase):
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
backend/apps/attachments/views.py:12:from apps.approvals.models import Approval, ApprovalStep
backend/apps/attachments/views.py:13:from .models import Attachment
backend/apps/attachments/views.py:14:from .serializers import AttachmentUploadSerializer, AttachmentSerializer, AttachmentListResponseSerializer
backend/apps/attachments/views.py:21:    operation_id='attachments_list',
backend/apps/attachments/views.py:25:        200: AttachmentListResponseSerializer,
backend/apps/attachments/views.py:33:    operation_id='attachments_upload',
backend/apps/attachments/views.py:36:    request=AttachmentUploadSerializer,
backend/apps/attachments/views.py:38:        201: AttachmentSerializer,
backend/apps/attachments/views.py:48:def attachments_view(request, application_id):
backend/apps/attachments/views.py:49:    """Dispatcher for attachment list (GET) and upload (POST)"""
backend/apps/attachments/views.py:51:        return list_attachments(request, application_id)
backend/apps/attachments/views.py:53:        return upload_attachment(request, application_id)
backend/apps/attachments/views.py:56:def upload_attachment(request, application_id):
backend/apps/attachments/views.py:72:    serializer = AttachmentUploadSerializer(data=request.data)
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
backend/apps/attachments/views.py:134:    except Attachment.DoesNotExist:
backend/apps/attachments/views.py:139:    if attachment.is_deleted:
backend/apps/attachments/views.py:144:    application = attachment.application
backend/apps/attachments/views.py:151:        # Check if preview mode (query param: ?preview=true)
backend/apps/attachments/views.py:152:        preview_mode = request.GET.get('preview', 'false').lower() == 'true'
backend/apps/attachments/views.py:154:            attachment.file.open('rb'),
backend/apps/attachments/views.py:155:            as_attachment=not preview_mode,
backend/apps/attachments/views.py:156:            filename=attachment.file_name,
backend/apps/attachments/views.py:157:            content_type=attachment.content_type
backend/apps/attachments/views.py:165:    operation_id='attachments_delete',
backend/apps/attachments/views.py:178:def delete_attachment(request, attachment_id):
backend/apps/attachments/views.py:181:    # Get attachment
backend/apps/attachments/views.py:183:        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
backend/apps/attachments/views.py:184:    except Attachment.DoesNotExist:
backend/apps/attachments/views.py:189:    if attachment.is_deleted:
backend/apps/attachments/views.py:194:    if user.role != UserRole.STUDENT or attachment.application.student_id != user.user_id:
backend/apps/attachments/views.py:199:    attachment.is_deleted = True
backend/apps/attachments/views.py:200:    attachment.deleted_at = timezone.now()
backend/apps/attachments/views.py:201:    attachment.save()
backend/apps/approvals/views.py:16:from .validators import approval_step_matches_application_status
backend/apps/approvals/views.py:19:from apps.notifications.services import notify_approval_decided
backend/apps/approvals/views.py:35:    operation_id='approvals_list',
backend/apps/approvals/views.py:39:        OpenApiParameter('decision', str, description='决策过滤：pending/approved/rejected/all（默认pending）'),
backend/apps/approvals/views.py:51:def list_approvals(request):
backend/apps/approvals/views.py:64:            approver=user,
backend/apps/approvals/views.py:66:        ).select_related('application', 'application__student', 'approver')
backend/apps/approvals/views.py:71:            approver=user,
backend/apps/approvals/views.py:73:        ).select_related('application', 'application__student', 'approver')
backend/apps/approvals/views.py:77:        queryset = Approval.objects.all().select_related('application', 'application__student', 'approver')
backend/apps/approvals/views.py:81:        queryset = Approval.objects.all().select_related('application', 'application__student', 'approver')
backend/apps/approvals/views.py:95:    queryset = queryset.order_by('-created_at', '-approval_id')
backend/apps/approvals/views.py:108:    operation_id='approvals_get',
backend/apps/approvals/views.py:120:def get_approval(request, approval_id):
backend/apps/approvals/views.py:122:        approval = Approval.objects.select_related('application', 'approver').get(approval_id=approval_id)
backend/apps/approvals/views.py:129:    # Permission check: only the approver or dean/admin can view this approval
backend/apps/approvals/views.py:130:    if user.role in [UserRole.DEAN, UserRole.ADMIN] or approval.approver_id == user.user_id:
backend/apps/approvals/views.py:131:        return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:138:    operation_id='approvals_approve',
backend/apps/approvals/views.py:154:def approve_approval(request, approval_id):
backend/apps/approvals/views.py:156:        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
backend/apps/approvals/views.py:162:    # Admin can approve/reject any step
backend/apps/approvals/views.py:164:        if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
backend/apps/approvals/views.py:167:        if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
backend/apps/approvals/views.py:170:        if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
backend/apps/approvals/views.py:174:        if approval.approver_id != user.user_id:
backend/apps/approvals/views.py:178:    if approval.decision != ApprovalDecision.PENDING:
backend/apps/approvals/views.py:182:    if not approval_step_matches_application_status(approval):
backend/apps/approvals/views.py:191:    approval.decision = ApprovalDecision.APPROVED
backend/apps/approvals/views.py:192:    approval.comment = serializer.validated_data.get('comment', '')
backend/apps/approvals/views.py:193:    approval.decided_at = timezone.now()
backend/apps/approvals/views.py:194:    approval.decided_by = user
backend/apps/approvals/views.py:195:    approval.save()
backend/apps/approvals/views.py:197:    notify_approval_decided(approval)
backend/apps/approvals/views.py:199:    application = approval.application
backend/apps/approvals/views.py:200:    if approval.step == ApprovalStep.DORM_MANAGER:
backend/apps/approvals/views.py:201:        # Auto-complete other pending dorm manager approvals for the same building
backend/apps/approvals/views.py:202:        # (New requirement: any dorm manager in the building can approve, others see "already approved")
backend/apps/approvals/views.py:203:        other_dorm_approvals = Approval.objects.filter(
backend/apps/approvals/views.py:207:        ).exclude(approval_id=approval.approval_id)
backend/apps/approvals/views.py:209:        if other_dorm_approvals.exists():
backend/apps/approvals/views.py:211:            actual_approver = approval.decided_by or approval.approver
backend/apps/approvals/views.py:212:            count = other_dorm_approvals.count()
backend/apps/approvals/views.py:213:            for other_approval in other_dorm_approvals:
backend/apps/approvals/views.py:214:                other_approval.decision = ApprovalDecision.APPROVED
backend/apps/approvals/views.py:215:                other_approval.comment = f'已由{approval.approver_name}完成审批，无需重复操作'
backend/apps/approvals/views.py:216:                other_approval.decided_at = now
backend/apps/approvals/views.py:217:                other_approval.decided_by = actual_approver
backend/apps/approvals/views.py:218:                other_approval.save()
backend/apps/approvals/views.py:220:                f"Auto-completed {count} other dorm manager approvals "
backend/apps/approvals/views.py:221:                f"for application {application.application_id} after approval by {actual_approver.user_id}"
backend/apps/approvals/views.py:224:        # Check for existing counselor approval to prevent duplicates
backend/apps/approvals/views.py:225:        existing_counselor_approval = Approval.objects.filter(
backend/apps/approvals/views.py:230:        if existing_counselor_approval:
backend/apps/approvals/views.py:239:        # changed to "按学院向辅导员审批" (approval by department/college).
backend/apps/approvals/views.py:262:            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
backend/apps/approvals/views.py:265:            approver=counselor,
backend/apps/approvals/views.py:266:            approver_name=counselor.name,
backend/apps/approvals/views.py:269:    elif approval.step == ApprovalStep.COUNSELOR:
backend/apps/approvals/views.py:270:        # Counselor approval completes the process (2-level approval)
backend/apps/approvals/views.py:274:    return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:278:    operation_id='approvals_reject',
backend/apps/approvals/views.py:294:def reject_approval(request, approval_id):
backend/apps/approvals/views.py:296:        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
backend/apps/approvals/views.py:302:    # Admin can approve/reject any step
backend/apps/approvals/views.py:304:        if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
backend/apps/approvals/views.py:307:        if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
backend/apps/approvals/views.py:310:        if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
backend/apps/approvals/views.py:314:        if approval.approver_id != user.user_id:
backend/apps/approvals/views.py:318:    if approval.decision != ApprovalDecision.PENDING:
backend/apps/approvals/views.py:322:    if not approval_step_matches_application_status(approval):
backend/apps/approvals/views.py:331:    approval.decision = ApprovalDecision.REJECTED
backend/apps/approvals/views.py:332:    approval.comment = serializer.validated_data.get('comment', '')
backend/apps/approvals/views.py:333:    approval.decided_at = timezone.now()
backend/apps/approvals/views.py:334:    approval.decided_by = user
backend/apps/approvals/views.py:335:    approval.save()
backend/apps/approvals/views.py:337:    notify_approval_decided(approval)
backend/apps/approvals/views.py:339:    application = approval.application
backend/apps/approvals/views.py:343:    return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:347:    operation_id='approvals_export',
backend/apps/approvals/views.py:358:def export_approvals(request):
backend/apps/approvals/views.py:370:        'approvals',
backend/apps/approvals/views.py:372:        to_attr='dorm_approvals_list'
backend/apps/approvals/views.py:375:        'approvals',
backend/apps/approvals/views.py:377:        to_attr='counselor_approvals_list'
backend/apps/approvals/views.py:398:        dorm_approval = app.dorm_approvals_list[0] if app.dorm_approvals_list else None
backend/apps/approvals/views.py:399:        counselor_approval = app.counselor_approvals_list[0] if app.counselor_approvals_list else None
backend/apps/approvals/views.py:407:            sanitize_excel_formula(dorm_approval.approver_name if dorm_approval else ''),
backend/apps/approvals/views.py:408:            dorm_approval.decided_at.strftime('%Y-%m-%d %H:%M:%S') if dorm_approval and dorm_approval.decided_at else '',
backend/apps/approvals/views.py:409:            dorm_approval.get_decision_display() if dorm_approval else '',
backend/apps/approvals/views.py:410:            sanitize_excel_formula(counselor_approval.approver_name if counselor_approval else ''),
backend/apps/approvals/views.py:411:            counselor_approval.decided_at.strftime('%Y-%m-%d %H:%M:%S') if counselor_approval and counselor_approval.decided_at else '',
backend/apps/approvals/views.py:412:            counselor_approval.get_decision_display() if counselor_approval else '',
backend/apps/approvals/views.py:427:    response['Content-Disposition'] = f'attachment; filename="approvals_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
backend/apps/approvals/migrations/0003_alter_approval_step.py:9:        ('approvals', '0002_initial'),
backend/apps/approvals/migrations/0003_alter_approval_step.py:14:            model_name='approval',
backend/apps/approvals/migrations/0002_initial.py:14:        ('approvals', '0001_initial'),
backend/apps/approvals/migrations/0002_initial.py:19:            model_name='approval',
backend/apps/approvals/migrations/0002_initial.py:20:            name='approver',
backend/apps/approvals/migrations/0002_initial.py:21:            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='approvals', to=settings.AUTH_USER_MODEL),
backend/apps/approvals/migrations/0001_initial.py:19:                ('approval_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
backend/apps/approvals/migrations/0001_initial.py:21:                ('approver_name', models.CharField(max_length=100)),
backend/apps/approvals/migrations/0001_initial.py:22:                ('decision', models.CharField(choices=[('pending', '待审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='pending', max_length=20)),
backend/apps/approvals/migrations/0001_initial.py:27:                ('application', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='approvals', to='applications.application')),
backend/apps/approvals/migrations/0001_initial.py:30:                'db_table': 'approvals',
backend/apps/approvals/migrations/0004_add_decided_by_field.py:12:        ('approvals', '0003_alter_approval_step'),
backend/apps/approvals/migrations/0004_add_decided_by_field.py:17:            model_name='approval',
backend/apps/approvals/migrations/0004_add_decided_by_field.py:19:            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='decided_approvals', to=settings.AUTH_USER_MODEL, verbose_name='实际审批人'),
frontend/types/api.ts:10:  | 'approved'
frontend/types/api.ts:13:export type ApprovalDecision = 'pending' | 'approved' | 'rejected';
frontend/types/api.ts:40:  leave_date: string; // YYYY-MM-DD
frontend/types/api.ts:50:  leave_date: string;
frontend/types/api.ts:58:  approvals: ApprovalDetail[];
frontend/types/api.ts:63:  approval_id: string;
frontend/types/api.ts:66:  approver_id: string;
frontend/types/api.ts:67:  approver_name: string;
frontend/types/api.ts:74:  approval_id: string;
frontend/types/api.ts:77:  approver_id: string;
frontend/types/api.ts:78:  approver_name: string;
frontend/types/api.ts:88:  approval_id: string;
frontend/mobile/ApprovalDetail.tsx:5:interface Attachment {
frontend/mobile/ApprovalDetail.tsx:6:  attachment_id: string;
frontend/mobile/ApprovalDetail.tsx:15:  leave_date: string;
frontend/mobile/ApprovalDetail.tsx:17:  attachments: Attachment[];
frontend/mobile/ApprovalDetail.tsx:22:  approval: ApprovalDetail;
frontend/mobile/ApprovalDetail.tsx:27:export const ApprovalDetailView: React.FC<Props> = ({ approval, onApprove, onReject }) => {
frontend/mobile/ApprovalDetail.tsx:28:  const handlePreview = (attachmentId: string) => {
frontend/mobile/ApprovalDetail.tsx:29:    const url = `${API_BASE_URL}/api/attachments/${attachmentId}/download/?preview=true`;
frontend/mobile/ApprovalDetail.tsx:33:  const handleDownload = (attachmentId: string) => {
frontend/mobile/ApprovalDetail.tsx:34:    const url = `${API_BASE_URL}/api/attachments/${attachmentId}/download/`;
frontend/mobile/ApprovalDetail.tsx:46:          <Text style={styles.value}>{approval.student_name}</Text>
frontend/mobile/ApprovalDetail.tsx:51:          <Text style={styles.value}>{approval.student_id}</Text>
frontend/mobile/ApprovalDetail.tsx:56:          <Text style={styles.value}>{approval.contact_phone}</Text>
frontend/mobile/ApprovalDetail.tsx:61:          <Text style={styles.value}>{approval.leave_date}</Text>
frontend/mobile/ApprovalDetail.tsx:66:          <Text style={styles.value}>{approval.reason}</Text>
frontend/mobile/ApprovalDetail.tsx:71:      {approval.attachments && approval.attachments.length > 0 && (
frontend/mobile/ApprovalDetail.tsx:75:          {approval.attachments.map((file) => (
frontend/mobile/ApprovalDetail.tsx:76:            <View key={file.attachment_id} style={styles.attachmentItem}>
frontend/mobile/ApprovalDetail.tsx:84:              <View style={styles.attachmentActions}>
frontend/mobile/ApprovalDetail.tsx:87:                  style={[styles.button, styles.previewButton]}
frontend/mobile/ApprovalDetail.tsx:88:                  onPress={() => handlePreview(file.attachment_id)}
frontend/mobile/ApprovalDetail.tsx:95:                  onPress={() => handleDownload(file.attachment_id)}
frontend/mobile/ApprovalDetail.tsx:106:      {approval.decision === 'pending' && (
frontend/mobile/ApprovalDetail.tsx:109:            style={[styles.button, styles.approveButton]}
frontend/mobile/ApprovalDetail.tsx:159:  attachmentItem: {
frontend/mobile/ApprovalDetail.tsx:177:  attachmentActions: {
frontend/mobile/ApprovalDetail.tsx:188:  previewButton: {
frontend/mobile/ApprovalDetail.tsx:204:  approveButton: {
frontend/miniprogram/pages/approval-detail/index.js:6:    approval: null,
frontend/miniprogram/pages/approval-detail/index.js:10:    const approvalId = options.id;
frontend/miniprogram/pages/approval-detail/index.js:11:    this.loadApprovalDetail(approvalId);
frontend/miniprogram/pages/approval-detail/index.js:15:  async loadApprovalDetail(approvalId) {
frontend/miniprogram/pages/approval-detail/index.js:19:        url: `${app.globalData.apiBase}/api/approvals/${approvalId}/`,
frontend/miniprogram/pages/approval-detail/index.js:25:      this.setData({ approval: res.data });
frontend/miniprogram/pages/approval-detail/index.js:35:    const attachmentId = e.currentTarget.dataset.id;
frontend/miniprogram/pages/approval-detail/index.js:36:    const url = `${app.globalData.apiBase}/api/attachments/${attachmentId}/download/?preview=true`;
frontend/miniprogram/pages/approval-detail/index.js:50:          wx.previewImage({
frontend/miniprogram/pages/approval-detail/index.js:71:    const attachmentId = e.currentTarget.dataset.id;
frontend/miniprogram/pages/approval-detail/index.js:72:    const url = `${app.globalData.apiBase}/api/attachments/${attachmentId}/download/`;
frontend/miniprogram/pages/approval-detail/index.js:109:          this.submitApproval('approve');
frontend/miniprogram/pages/approval-detail/index.js:133:        url: `${app.globalData.apiBase}/api/approvals/${this.data.approval.approval_id}/${action}/`,
frontend/hooks/useAttachment.ts:2:import { attachmentService } from '../services/attachment';
frontend/hooks/useAttachment.ts:4:export const useAttachment = () => {
frontend/hooks/useAttachment.ts:5:  const handlePreview = (attachmentId: string) => {
frontend/hooks/useAttachment.ts:6:    attachmentService.previewWeb(attachmentId);
frontend/hooks/useAttachment.ts:9:  const handleDownload = (attachmentId: string) => {
frontend/hooks/useAttachment.ts:10:    attachmentService.downloadWeb(attachmentId);
frontend/hooks/useAttachment.ts:13:  const getPreviewUrl = (attachmentId: string) => {
frontend/hooks/useAttachment.ts:14:    return attachmentService.getPreviewUrl(attachmentId);
frontend/hooks/useAttachment.ts:17:  const getDownloadUrl = (attachmentId: string) => {
frontend/hooks/useAttachment.ts:18:    return attachmentService.getDownloadUrl(attachmentId);
frontend/miniprogram/pages/approval-detail/index.wxml:9:      <text class="value">{{approval.student_name}}</text>
frontend/miniprogram/pages/approval-detail/index.wxml:14:      <text class="value">{{approval.student_id}}</text>
frontend/miniprogram/pages/approval-detail/index.wxml:19:      <text class="value">{{approval.contact_phone}}</text>
frontend/miniprogram/pages/approval-detail/index.wxml:24:      <text class="value">{{approval.leave_date}}</text>
frontend/miniprogram/pages/approval-detail/index.wxml:29:      <text class="value">{{approval.reason}}</text>
frontend/miniprogram/pages/approval-detail/index.wxml:34:  <view class="section" wx:if="{{approval.attachments && approval.attachments.length > 0}}">
frontend/miniprogram/pages/approval-detail/index.wxml:37:    <view class="attachment-item" wx:for="{{approval.attachments}}" wx:key="attachment_id">
frontend/miniprogram/pages/approval-detail/index.wxml:43:      <view class="attachment-actions">
frontend/miniprogram/pages/approval-detail/index.wxml:46:          class="btn btn-preview"
frontend/miniprogram/pages/approval-detail/index.wxml:48:          data-id="{{item.attachment_id}}"
frontend/miniprogram/pages/approval-detail/index.wxml:56:          data-id="{{item.attachment_id}}"
frontend/miniprogram/pages/approval-detail/index.wxml:65:  <view class="action-section" wx:if="{{approval.decision === 'pending'}}">
frontend/miniprogram/pages/approval-detail/index.wxml:66:    <button class="btn btn-approve" bindtap="handleApprove">通过</button>
backend/apps/approvals/tests/test_state_machine.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_state_machine.py:66:            leave_date='2024-06-30',
backend/apps/approvals/tests/test_state_machine.py:70:        # Create counselor approval
backend/apps/approvals/tests/test_state_machine.py:71:        self.approval = Approval.objects.create(
backend/apps/approvals/tests/test_state_machine.py:72:            approval_id='apv_test001',
backend/apps/approvals/tests/test_state_machine.py:75:            approver=self.counselor,
backend/apps/approvals/tests/test_state_machine.py:76:            approver_name='李老师',
backend/apps/approvals/tests/test_state_machine.py:82:    def test_duplicate_approval_conflict(self):
backend/apps/approvals/tests/test_state_machine.py:86:        # First approval
backend/apps/approvals/tests/test_state_machine.py:88:            f'/api/approvals/{self.approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:94:        # Second approval attempt
backend/apps/approvals/tests/test_state_machine.py:96:            f'/api/approvals/{self.approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:107:            f'/api/approvals/{self.approval.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:114:            f'/api/approvals/{self.approval.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:126:        approve_response = self.client.post(
backend/apps/approvals/tests/test_state_machine.py:127:            f'/api/approvals/{self.approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:132:            f'/api/approvals/{self.approval.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:137:        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_state_machine.py:144:        dorm_manager_approval = Approval.objects.create(
backend/apps/approvals/tests/test_state_machine.py:145:            approval_id='apv_test002',
backend/apps/approvals/tests/test_state_machine.py:148:            approver=self.dorm_manager,
backend/apps/approvals/tests/test_state_machine.py:149:            approver_name='宿管员',
backend/apps/approvals/tests/test_state_machine.py:154:        approve_response = self.client.post(
backend/apps/approvals/tests/test_state_machine.py:155:            f'/api/approvals/{dorm_manager_approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:160:            f'/api/approvals/{dorm_manager_approval.approval_id}/reject/',
backend/apps/approvals/tests/test_state_machine.py:165:        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_admin_and_export.py:3:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_admin_and_export.py:5:from apps.approvals.views import sanitize_excel_formula
backend/apps/approvals/tests/test_admin_and_export.py:11:    """Test ADMIN role can approve/reject any step and decided_by is recorded."""
backend/apps/approvals/tests/test_admin_and_export.py:33:            leave_date='2026-07-01',
backend/apps/approvals/tests/test_admin_and_export.py:37:        self.approval = Approval.objects.create(
backend/apps/approvals/tests/test_admin_and_export.py:38:            approval_id='apv_test001',
backend/apps/approvals/tests/test_admin_and_export.py:41:            approver=self.dorm_manager,
backend/apps/approvals/tests/test_admin_and_export.py:42:            approver_name=self.dorm_manager.name,
backend/apps/approvals/tests/test_admin_and_export.py:46:    def test_admin_can_approve_dorm_manager_step(self):
backend/apps/approvals/tests/test_admin_and_export.py:47:        """ADMIN can approve dorm manager step."""
backend/apps/approvals/tests/test_admin_and_export.py:50:            f'/api/approvals/{self.approval.approval_id}/approve/',
backend/apps/approvals/tests/test_admin_and_export.py:54:        self.approval.refresh_from_db()
backend/apps/approvals/tests/test_admin_and_export.py:55:        self.assertEqual(self.approval.decision, ApprovalDecision.APPROVED)
backend/apps/approvals/tests/test_admin_and_export.py:56:        self.assertEqual(self.approval.decided_by, self.admin)
backend/apps/approvals/tests/test_admin_and_export.py:62:            f'/api/approvals/{self.approval.approval_id}/reject/',
backend/apps/approvals/tests/test_admin_and_export.py:66:        self.approval.refresh_from_db()
backend/apps/approvals/tests/test_admin_and_export.py:67:        self.assertEqual(self.approval.decision, ApprovalDecision.REJECTED)
backend/apps/approvals/tests/test_admin_and_export.py:68:        self.assertEqual(self.approval.decided_by, self.admin)
backend/apps/approvals/tests/test_admin_and_export.py:91:        response = self.client.get('/api/approvals/export/')
backend/apps/approvals/tests/test_admin_and_export.py:97:        response = self.client.get('/api/approvals/export/')
backend/apps/approvals/tests/test_admin_and_export.py:107:        response = self.client.get('/api/approvals/export/')
backend/apps/approvals/tests/test_rejection_flow.py:9:from apps.approvals.models import ApprovalDecision, ApprovalStep
backend/apps/approvals/tests/test_rejection_flow.py:66:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
backend/apps/approvals/tests/test_rejection_flow.py:71:    def _approve_dorm_manager_step(self, application):
backend/apps/approvals/tests/test_rejection_flow.py:78:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/approvals/tests/test_rejection_flow.py:81:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/approve/', {
backend/apps/approvals/tests/test_rejection_flow.py:97:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/approvals/tests/test_rejection_flow.py:100:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/reject/', {
backend/apps/approvals/tests/test_rejection_flow.py:113:        self._approve_dorm_manager_step(application)
backend/apps/approvals/tests/test_rejection_flow.py:123:        counselor_approval = application.approvals.get(step=ApprovalStep.COUNSELOR)
backend/apps/approvals/tests/test_rejection_flow.py:126:        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/reject/', {
backend/apps/approvals/tests/test_list_permissions.py:5:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_list_permissions.py:48:            leave_date='2024-07-01',
backend/apps/approvals/tests/test_list_permissions.py:52:        # Create approvals
backend/apps/approvals/tests/test_list_permissions.py:53:        self.approval_c1 = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:54:            approval_id='apv_c1',
backend/apps/approvals/tests/test_list_permissions.py:57:            approver=self.counselor1,
backend/apps/approvals/tests/test_list_permissions.py:58:            approver_name='辅导员1',
backend/apps/approvals/tests/test_list_permissions.py:62:        self.approval_m1 = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:63:            approval_id='apv_m1',
backend/apps/approvals/tests/test_list_permissions.py:66:            approver=self.dorm_manager1,
backend/apps/approvals/tests/test_list_permissions.py:67:            approver_name='宿管员1',
backend/apps/approvals/tests/test_list_permissions.py:71:    def test_student_403_on_approval_list(self):
backend/apps/approvals/tests/test_list_permissions.py:73:        response = self.client.get('/api/approvals/')
backend/apps/approvals/tests/test_list_permissions.py:77:    def test_counselor_sees_only_own_pending_approvals(self):
backend/apps/approvals/tests/test_list_permissions.py:79:        response = self.client.get('/api/approvals/')
backend/apps/approvals/tests/test_list_permissions.py:82:        self.assertEqual(response.data['results'][0]['approval_id'], 'apv_c1')
backend/apps/approvals/tests/test_list_permissions.py:84:    def test_counselor_cannot_see_other_counselor_approvals(self):
backend/apps/approvals/tests/test_list_permissions.py:86:        response = self.client.get('/api/approvals/')
backend/apps/approvals/tests/test_list_permissions.py:89:    def test_dorm_manager_sees_only_own_pending_approvals(self):
backend/apps/approvals/tests/test_list_permissions.py:91:        response = self.client.get('/api/approvals/')
backend/apps/approvals/tests/test_list_permissions.py:94:        self.assertEqual(response.data['results'][0]['approval_id'], 'apv_m1')
backend/apps/approvals/tests/test_list_permissions.py:96:    def test_dorm_manager_cannot_see_other_dorm_manager_approvals(self):
backend/apps/approvals/tests/test_list_permissions.py:98:        response = self.client.get('/api/approvals/')
backend/apps/approvals/tests/test_list_permissions.py:101:    def test_dean_sees_all_approvals_for_archive(self):
backend/apps/approvals/tests/test_list_permissions.py:103:        response = self.client.get('/api/approvals/')
backend/apps/approvals/tests/test_list_permissions.py:109:        response = self.client.get('/api/approvals/')
backend/apps/approvals/tests/test_list_permissions.py:115:    def test_decision_all_does_not_leak_cross_approver_data(self):
backend/apps/approvals/tests/test_list_permissions.py:116:        # Create second application and approval for counselor1 (approved)
backend/apps/approvals/tests/test_list_permissions.py:123:            leave_date='2024-07-02',
backend/apps/approvals/tests/test_list_permissions.py:126:        approval_c1_approved = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:127:            approval_id='apv_c1_approved',
backend/apps/approvals/tests/test_list_permissions.py:130:            approver=self.counselor1,
backend/apps/approvals/tests/test_list_permissions.py:131:            approver_name='辅导员1',
backend/apps/approvals/tests/test_list_permissions.py:135:        # Create approval for counselor2
backend/apps/approvals/tests/test_list_permissions.py:142:            leave_date='2024-07-03',
backend/apps/approvals/tests/test_list_permissions.py:145:        approval_c2 = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:146:            approval_id='apv_c2',
backend/apps/approvals/tests/test_list_permissions.py:149:            approver=self.counselor2,
backend/apps/approvals/tests/test_list_permissions.py:150:            approver_name='辅导员2',
backend/apps/approvals/tests/test_list_permissions.py:156:        response = self.client.get('/api/approvals/?decision=all')
backend/apps/approvals/tests/test_list_permissions.py:160:        # Verify only counselor1's approvals returned
backend/apps/approvals/tests/test_list_permissions.py:161:        approval_ids = [a['approval_id'] for a in response.data['results']]
backend/apps/approvals/tests/test_list_permissions.py:162:        self.assertIn('apv_c1', approval_ids)
backend/apps/approvals/tests/test_list_permissions.py:163:        self.assertIn('apv_c1_approved', approval_ids)
backend/apps/approvals/tests/test_list_permissions.py:164:        self.assertNotIn('apv_c2', approval_ids)
backend/apps/approvals/tests/test_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_permissions.py:99:            leave_date='2024-06-30',
backend/apps/approvals/tests/test_permissions.py:103:        # Create counselor approval for application1
backend/apps/approvals/tests/test_permissions.py:104:        self.approval1 = Approval.objects.create(
backend/apps/approvals/tests/test_permissions.py:105:            approval_id='apv_test001',
backend/apps/approvals/tests/test_permissions.py:108:            approver=self.counselor1,
backend/apps/approvals/tests/test_permissions.py:109:            approver_name='李老师',
backend/apps/approvals/tests/test_permissions.py:115:    def _create_dorm_manager_approval(self):
backend/apps/approvals/tests/test_permissions.py:119:            approval_id='apv_test002',
backend/apps/approvals/tests/test_permissions.py:122:            approver=self.dorm_manager1,
backend/apps/approvals/tests/test_permissions.py:123:            approver_name='宿管员1',
backend/apps/approvals/tests/test_permissions.py:127:    def test_student_cannot_approve_or_reject(self):
backend/apps/approvals/tests/test_permissions.py:131:        approve_response = self.client.post(
backend/apps/approvals/tests/test_permissions.py:132:            f'/api/approvals/{self.approval1.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:137:            f'/api/approvals/{self.approval1.approval_id}/reject/',
backend/apps/approvals/tests/test_permissions.py:142:        self.assertEqual(approve_response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/approvals/tests/test_permissions.py:150:            f'/api/approvals/{self.approval1.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:159:        dorm_manager_approval = self._create_dorm_manager_approval()
backend/apps/approvals/tests/test_permissions.py:163:            f'/api/approvals/{dorm_manager_approval.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:172:        dorm_manager_approval = self._create_dorm_manager_approval()
backend/apps/approvals/tests/test_permissions.py:176:            f'/api/approvals/{dorm_manager_approval.approval_id}/reject/',
backend/apps/approvals/tests/test_permissions.py:183:    def test_cross_counselor_approve_forbidden(self):
backend/apps/approvals/tests/test_permissions.py:185:        # T002 tries to approve T001's application
backend/apps/approvals/tests/test_permissions.py:188:            f'/api/approvals/{self.approval1.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:199:            f'/api/approvals/{self.approval1.approval_id}/reject/',

codex
我已经看到一个重要方向：后端详情接口新增了 `attachments`，但前端类型和多端组件是否真的复用还需要逐文件核对。现在读取具体实现和行号，用于给出可定位的审计结论。
exec
/bin/bash -lc "rtk nl -ba backend/apps/attachments/views.py | sed -n '1,240p'" in /home/caohui/projects/graduation-leave-system
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
   151	        # Check if preview mode (query param: ?preview=true)
   152	        preview_mode = request.GET.get('preview', 'false').lower() == 'true'
   153	        return FileResponse(
   154	            attachment.file.open('rb'),
   155	            as_attachment=not preview_mode,
   156	            filename=attachment.file_name,
   157	            content_type=attachment.content_type
   158	        )
   159	    except FileNotFoundError:
   160	        return Response({'error': {'code': 'NOT_FOUND', 'message': '文件不存在'}},
   161	                        status=status.HTTP_404_NOT_FOUND)
   162	
   163	
   164	@extend_schema(
   165	    operation_id='attachments_delete',
   166	    summary='删除附件',
   167	    description='软删除指定附件（仅申请所有者可删除）',
   168	    request=None,
   169	    responses={
   170	        204: OpenApiResponse(description='删除成功'),
   171	        403: ErrorResponseSerializer,
   172	        404: ErrorResponseSerializer,
   173	    },
   174	    tags=['附件']
   175	)
   176	@api_view(['DELETE'])
   177	@permission_classes([IsAuthenticated])
   178	def delete_attachment(request, attachment_id):
   179	    user = request.user
   180	
   181	    # Get attachment
   182	    try:
   183	        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
   184	    except Attachment.DoesNotExist:
   185	        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
   186	                        status=status.HTTP_404_NOT_FOUND)
   187	
   188	    # Check if already deleted
   189	    if attachment.is_deleted:
   190	        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
   191	                        status=status.HTTP_404_NOT_FOUND)
   192	
   193	    # Permission: only student who owns the application
   194	    if user.role != UserRole.STUDENT or attachment.application.student_id != user.user_id:
   195	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限删除附件'}},
   196	                        status=status.HTTP_403_FORBIDDEN)
   197	
   198	    # Soft delete
   199	    attachment.is_deleted = True
   200	    attachment.deleted_at = timezone.now()
   201	    attachment.save()
   202	
   203	    return Response(status=status.HTTP_204_NO_CONTENT)

exec
/bin/bash -lc "rtk nl -ba frontend/services/api.ts | sed -n '1,220p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// API Client for v0.2 Contract
     2	// Minimal implementation - can be extended
     3	
     4	import type {
     5	  LoginRequest,
     6	  LoginResponse,
     7	  ApplicationCreateRequest,
     8	  ApplicationDetail,
     9	  Application,
    10	  ApprovalListItem,
    11	  ApprovalActionRequest,
    12	  ApprovalActionResponse,
    13	  PaginatedResponse,
    14	  ApiError,
    15	} from '../types/api';
    16	
    17	export interface ApiConfig {
    18	  baseUrl: string;
    19	  getToken?: () => string | null;
    20	  onUnauthorized?: () => void;
    21	}
    22	
    23	export class ApiClient {
    24	  private config: ApiConfig;
    25	
    26	  constructor(config: ApiConfig) {
    27	    this.config = config;
    28	  }
    29	
    30	  private extractErrorMessage(apiError: ApiError): string {
    31	    const { error } = apiError;
    32	
    33	    // 字段名映射（英文 -> 中文）
    34	    const fieldNames: Record<string, string> = {
    35	      contact_phone: '联系电话',
    36	      leave_date: '离校日期',
    37	      reason: '离校原因',
    38	      file: '附件',
    39	      user_id: '用户ID',
    40	      password: '密码',
    41	      comment: '审批意见',
    42	    };
    43	
    44	    // 如果有详细错误信息（字段验证错误）
    45	    if (error.details) {
    46	      // 提取第一个字段的第一个错误
    47	      const firstField = Object.keys(error.details)[0];
    48	      if (firstField && Array.isArray(error.details[firstField])) {
    49	        const fieldError = error.details[firstField][0];
    50	        const fieldLabel = fieldNames[firstField] || firstField;
    51	
    52	        // 如果错误消息已经很具体，直接返回
    53	        if (fieldError.includes('不能') || fieldError.includes('超过') || fieldError.includes('支持')) {
    54	          return fieldError;
    55	        }
    56	
    57	        // 否则加上字段名前缀
    58	        return `${fieldLabel}：${fieldError}`;
    59	      }
    60	    }
    61	
    62	    // 否则返回通用错误消息
    63	    return error.message || '操作失败，请稍后重试';
    64	  }
    65	
    66	  private async request<T>(
    67	    endpoint: string,
    68	    options: RequestInit = {}
    69	  ): Promise<T> {
    70	    const token = this.config.getToken?.();
    71	    const headers: HeadersInit = {
    72	      'Content-Type': 'application/json',
    73	      ...options.headers,
    74	    };
    75	
    76	    if (token) {
    77	      headers['Authorization'] = `Bearer ${token}`;
    78	    }
    79	
    80	    const response = await fetch(`${this.config.baseUrl}${endpoint}`, {
    81	      ...options,
    82	      headers,
    83	    });
    84	
    85	    if (response.status === 401) {
    86	      this.config.onUnauthorized?.();
    87	      throw new Error('Unauthorized');
    88	    }
    89	
    90	    const data = await response.json();
    91	
    92	    if (!response.ok) {
    93	      const apiError = data as ApiError;
    94	      // 提取详细错误信息
    95	      const errorMessage = this.extractErrorMessage(apiError);
    96	      throw new Error(errorMessage);
    97	    }
    98	
    99	    return data as T;
   100	  }
   101	
   102	  // Auth
   103	  async login(req: LoginRequest): Promise<LoginResponse> {
   104	    return this.request('/api/auth/login', {
   105	      method: 'POST',
   106	      body: JSON.stringify(req),
   107	    });
   108	  }
   109	
   110	  // Applications
   111	  async createApplication(req: ApplicationCreateRequest): Promise<ApplicationDetail> {
   112	    return this.request('/api/applications/', {
   113	      method: 'POST',
   114	      body: JSON.stringify(req),
   115	    });
   116	  }
   117	
   118	  async listApplications(
   119	    limit = 20,
   120	    offset = 0
   121	  ): Promise<PaginatedResponse<Application>> {
   122	    return this.request(
   123	      `/api/applications/?limit=${limit}&offset=${offset}`
   124	    );
   125	  }
   126	
   127	  async getApplication(id: string): Promise<ApplicationDetail> {
   128	    return this.request(`/api/applications/${id}/`);
   129	  }
   130	
   131	  // Approvals
   132	  async listApprovals(
   133	    decision: 'pending' | 'approved' | 'rejected' | 'all' = 'pending',
   134	    limit = 20,
   135	    offset = 0
   136	  ): Promise<PaginatedResponse<ApprovalListItem>> {
   137	    return this.request(
   138	      `/api/approvals/?decision=${decision}&limit=${limit}&offset=${offset}`
   139	    );
   140	  }
   141	
   142	  async approveApproval(
   143	    id: string,
   144	    req: ApprovalActionRequest
   145	  ): Promise<ApprovalActionResponse> {
   146	    return this.request(`/api/approvals/${id}/approve/`, {
   147	      method: 'POST',
   148	      body: JSON.stringify(req),
   149	    });
   150	  }
   151	
   152	  async rejectApproval(
   153	    id: string,
   154	    req: ApprovalActionRequest
   155	  ): Promise<ApprovalActionResponse> {
   156	    return this.request(`/api/approvals/${id}/reject/`, {
   157	      method: 'POST',
   158	      body: JSON.stringify(req),
   159	    });
   160	  }
   161	}

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/serializers.py | sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import serializers
     2	from .models import Approval
     3	
     4	
     5	class ApplicationBriefSerializer(serializers.Serializer):
     6	    """Brief application info for approval list"""
     7	    id = serializers.CharField(source='application_id')
     8	    status = serializers.CharField()
     9	    student_name = serializers.CharField(source='student.name')
    10	    student_id = serializers.CharField(source='student.user_id')
    11	    leave_date = serializers.DateField()
    12	
    13	
    14	class ApprovalListSerializer(serializers.ModelSerializer):
    15	    """Lean serializer for approval lists - nested application structure"""
    16	    id = serializers.CharField(source='approval_id', read_only=True)
    17	    application = ApplicationBriefSerializer(read_only=True)
    18	    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
    19	
    20	    class Meta:
    21	        model = Approval
    22	        fields = ['id', 'application', 'step', 'approver_id',
    23	                  'approver_name', 'decision', 'comment', 'decided_at', 'created_at']
    24	        read_only_fields = ['id', 'step', 'approver_id',
    25	                            'approver_name', 'decision', 'comment', 'decided_at', 'created_at']
    26	
    27	
    28	class ApprovalSerializer(serializers.ModelSerializer):
    29	    """Full approval detail with nested application info"""
    30	    application_id = serializers.CharField(source='application.application_id', read_only=True)
    31	    student_name = serializers.CharField(source='application.student.name', read_only=True)
    32	    student_id = serializers.CharField(source='application.student.user_id', read_only=True)
    33	    contact_phone = serializers.CharField(source='application.contact_phone', read_only=True)
    34	    reason = serializers.CharField(source='application.reason', read_only=True)
    35	    leave_date = serializers.DateField(source='application.leave_date', read_only=True)
    36	    attachments = serializers.SerializerMethodField()
    37	    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
    38	
    39	    class Meta:
    40	        model = Approval
    41	        fields = ['approval_id', 'application_id', 'student_name', 'student_id',
    42	                  'contact_phone', 'reason', 'leave_date', 'attachments', 'step', 'approver_id',
    43	                  'approver_name', 'decision', 'comment', 'decided_at']
    44	        read_only_fields = ['approval_id', 'application_id', 'student_name', 'student_id',
    45	                            'contact_phone', 'reason', 'leave_date', 'attachments', 'step',
    46	                            'approver_id', 'approver_name', 'decision', 'decided_at']
    47	
    48	    def get_attachments(self, obj):
    49	        from apps.attachments.serializers import AttachmentSerializer
    50	        return AttachmentSerializer(
    51	            obj.application.attachments.filter(is_deleted=False),
    52	            many=True
    53	        ).data
    54	
    55	
    56	class ApprovalActionSerializer(serializers.Serializer):
    57	    comment = serializers.CharField(required=False, allow_blank=True)
    58	
    59	
    60	class ApprovalListResponseSerializer(serializers.Serializer):
    61	    """Schema-only: approval list response with pagination"""
    62	    count = serializers.IntegerField()
    63	    results = ApprovalListSerializer(many=True)

exec
/bin/bash -lc "rtk nl -ba frontend/types/api.ts | sed -n '1,240p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// API Types based on v0.2 Contract
     2	// Generated: 2026-05-31
     3	
     4	export type UserRole = 'student' | 'dorm_manager' | 'counselor' | 'dean' | 'admin';
     5	
     6	export type ApplicationStatus =
     7	  | 'draft'
     8	  | 'pending_dorm_manager'
     9	  | 'pending_counselor'
    10	  | 'approved'
    11	  | 'rejected';
    12	
    13	export type ApprovalDecision = 'pending' | 'approved' | 'rejected';
    14	
    15	export type ApprovalStep = 'dorm_manager' | 'counselor';
    16	
    17	// Auth
    18	export interface LoginRequest {
    19	  user_id: string;
    20	  password: string;
    21	}
    22	
    23	export interface User {
    24	  user_id: string;
    25	  name: string;
    26	  role: UserRole;
    27	  class_id?: string | null;
    28	}
    29	
    30	export interface LoginResponse {
    31	  access_token: string;
    32	  token_type: 'Bearer';
    33	  user: User;
    34	}
    35	
    36	// Applications
    37	export interface ApplicationCreateRequest {
    38	  contact_phone: string;
    39	  reason?: string;
    40	  leave_date: string; // YYYY-MM-DD
    41	}
    42	
    43	export interface Application {
    44	  application_id: string;
    45	  student_id: string;
    46	  student_name: string;
    47	  class_id: string;
    48	  contact_phone?: string | null;
    49	  reason: string;
    50	  leave_date: string;
    51	  status: ApplicationStatus;
    52	  created_at: string;
    53	  updated_at: string;
    54	}
    55	
    56	export interface ApplicationDetail extends Application {
    57	  dorm_checkout_status: string;
    58	  approvals: ApprovalDetail[];
    59	}
    60	
    61	// Approvals
    62	export interface ApprovalDetail {
    63	  approval_id: string;
    64	  application_id: string;
    65	  step: ApprovalStep;
    66	  approver_id: string;
    67	  approver_name: string;
    68	  decision: ApprovalDecision;
    69	  comment: string | null;
    70	  decided_at: string | null;
    71	}
    72	
    73	export interface ApprovalListItem {
    74	  approval_id: string;
    75	  application_id: string;
    76	  step: ApprovalStep;
    77	  approver_id: string;
    78	  approver_name: string;
    79	  decision: ApprovalDecision;
    80	  created_at: string;
    81	}
    82	
    83	export interface ApprovalActionRequest {
    84	  comment?: string;
    85	}
    86	
    87	export interface ApprovalActionResponse {
    88	  approval_id: string;
    89	  decision: ApprovalDecision;
    90	  comment: string | null;
    91	  decided_at: string;
    92	}
    93	
    94	// Pagination
    95	export interface PaginatedResponse<T> {
    96	  count: number;
    97	  results: T[];
    98	}
    99	
   100	// Errors
   101	export interface ApiError {
   102	  error: {
   103	    code: string;
   104	    message: string;
   105	    details?: any;
   106	  };
   107	}

codex
目前已确认 `frontend/types/api.ts` 没有跟上详情字段，且 API client 的错误处理路径对非 JSON/网络异常还比较脆。下一步我会核对审批详情接口权限和附件下载权限是否共享同一套判定。
exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/views.py | sed -n '1,280p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import status
     2	from rest_framework.decorators import api_view, permission_classes
     3	from rest_framework.permissions import IsAuthenticated
     4	from rest_framework.response import Response
     5	from django.utils import timezone
     6	from django.db import transaction
     7	from django.http import HttpResponse
     8	from django.db.models import Prefetch
     9	import logging
    10	from drf_spectacular.utils import extend_schema, OpenApiParameter
    11	from openpyxl import Workbook
    12	from openpyxl.styles import Font, Alignment
    13	from .models import Approval, ApprovalDecision, ApprovalStep
    14	from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalListSerializer, ApprovalListResponseSerializer
    15	from .pagination import ApprovalLimitOffsetPagination
    16	from .validators import approval_step_matches_application_status
    17	from apps.applications.models import Application, ApplicationStatus
    18	from apps.users.models import User, UserRole
    19	from apps.notifications.services import notify_approval_decided
    20	from schema import ErrorResponseSerializer
    21	import uuid
    22	
    23	
    24	def sanitize_excel_formula(value):
    25	    """Sanitize text to prevent Excel formula injection."""
    26	    if not value:
    27	        return value
    28	    value_str = str(value)
    29	    if value_str and value_str[0] in ('=', '+', '-', '@'):
    30	        return "'" + value_str
    31	    return value_str
    32	
    33	
    34	@extend_schema(
    35	    operation_id='approvals_list',
    36	    summary='获取审批列表',
    37	    description='获取当前用户的待审批列表（辅导员或学工部）',
    38	    parameters=[
    39	        OpenApiParameter('decision', str, description='决策过滤：pending/approved/rejected/all（默认pending）'),
    40	        OpenApiParameter('limit', int, description='每页数量（默认20）'),
    41	        OpenApiParameter('offset', int, description='偏移量（默认0）'),
    42	    ],
    43	    responses={
    44	        200: ApprovalListResponseSerializer,
    45	        403: ErrorResponseSerializer,
    46	    },
    47	    tags=['审批']
    48	)
    49	@api_view(['GET'])
    50	@permission_classes([IsAuthenticated])
    51	def list_approvals(request):
    52	    user = request.user
    53	
    54	    # 学生禁止访问
    55	    if user.role == UserRole.STUDENT:
    56	        return Response(
    57	            {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
    58	            status=status.HTTP_403_FORBIDDEN
    59	        )
    60	
    61	    # 宿管员: 只看自己的dorm_manager审批
    62	    if user.role == UserRole.DORM_MANAGER:
    63	        queryset = Approval.objects.filter(
    64	            approver=user,
    65	            step=ApprovalStep.DORM_MANAGER
    66	        ).select_related('application', 'application__student', 'approver')
    67	
    68	    # 辅导员: 只看自己的counselor审批
    69	    elif user.role == UserRole.COUNSELOR:
    70	        queryset = Approval.objects.filter(
    71	            approver=user,
    72	            step=ApprovalStep.COUNSELOR
    73	        ).select_related('application', 'application__student', 'approver')
    74	
    75	    # 学工部: 查看所有审批（存档用）
    76	    elif user.role == UserRole.DEAN:
    77	        queryset = Approval.objects.all().select_related('application', 'application__student', 'approver')
    78	
    79	    # 学工管理员: 查看所有审批（管理用）
    80	    elif user.role == UserRole.ADMIN:
    81	        queryset = Approval.objects.all().select_related('application', 'application__student', 'approver')
    82	
    83	    else:
    84	        return Response(
    85	            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
    86	            status=status.HTTP_403_FORBIDDEN
    87	        )
    88	
    89	    # Decision filtering (default: pending)
    90	    decision_param = request.query_params.get('decision', 'pending')
    91	    if decision_param != 'all':
    92	        queryset = queryset.filter(decision=decision_param)
    93	
    94	    # 排序
    95	    queryset = queryset.order_by('-created_at', '-approval_id')
    96	
    97	    # 分页
    98	    paginator = ApprovalLimitOffsetPagination()
    99	    page = paginator.paginate_queryset(queryset, request)
   100	
   101	    # 序列化
   102	    serializer = ApprovalListSerializer(page, many=True)
   103	
   104	    return paginator.get_paginated_response(serializer.data)
   105	
   106	
   107	@extend_schema(
   108	    operation_id='approvals_get',
   109	    summary='获取审批详情',
   110	    description='获取指定审批的详细信息',
   111	    responses={
   112	        200: ApprovalSerializer,
   113	        403: ErrorResponseSerializer,
   114	        404: ErrorResponseSerializer,
   115	    },
   116	    tags=['审批']
   117	)
   118	@api_view(['GET'])
   119	@permission_classes([IsAuthenticated])
   120	def get_approval(request, approval_id):
   121	    try:
   122	        approval = Approval.objects.select_related('application', 'approver').get(approval_id=approval_id)
   123	    except Approval.DoesNotExist:
   124	        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
   125	                        status=status.HTTP_404_NOT_FOUND)
   126	
   127	    user = request.user
   128	
   129	    # Permission check: only the approver or dean/admin can view this approval
   130	    if user.role in [UserRole.DEAN, UserRole.ADMIN] or approval.approver_id == user.user_id:
   131	        return Response(ApprovalSerializer(approval).data)
   132	
   133	    return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
   134	                    status=status.HTTP_403_FORBIDDEN)
   135	
   136	
   137	@extend_schema(
   138	    operation_id='approvals_approve',
   139	    summary='通过审批',
   140	    description='审批人通过指定的审批申请',
   141	    request=ApprovalActionSerializer,
   142	    responses={
   143	        200: ApprovalSerializer,
   144	        400: ErrorResponseSerializer,
   145	        403: ErrorResponseSerializer,
   146	        404: ErrorResponseSerializer,
   147	        409: ErrorResponseSerializer,
   148	    },
   149	    tags=['审批']
   150	)
   151	@api_view(['POST'])
   152	@permission_classes([IsAuthenticated])
   153	@transaction.atomic
   154	def approve_approval(request, approval_id):
   155	    try:
   156	        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
   157	    except Approval.DoesNotExist:
   158	        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
   159	                        status=status.HTTP_404_NOT_FOUND)
   160	
   161	    user = request.user
   162	    # Admin can approve/reject any step
   163	    if user.role != UserRole.ADMIN:
   164	        if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
   165	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   166	                            status=status.HTTP_403_FORBIDDEN)
   167	        if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
   168	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   169	                            status=status.HTTP_403_FORBIDDEN)
   170	        if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
   171	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   172	                            status=status.HTTP_403_FORBIDDEN)
   173	
   174	        if approval.approver_id != user.user_id:
   175	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   176	                            status=status.HTTP_403_FORBIDDEN)
   177	
   178	    if approval.decision != ApprovalDecision.PENDING:
   179	        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
   180	                        status=status.HTTP_409_CONFLICT)
   181	
   182	    if not approval_step_matches_application_status(approval):
   183	        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
   184	                        status=status.HTTP_409_CONFLICT)
   185	
   186	    serializer = ApprovalActionSerializer(data=request.data)
   187	    if not serializer.is_valid():
   188	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
   189	                        status=status.HTTP_400_BAD_REQUEST)
   190	
   191	    approval.decision = ApprovalDecision.APPROVED
   192	    approval.comment = serializer.validated_data.get('comment', '')
   193	    approval.decided_at = timezone.now()
   194	    approval.decided_by = user
   195	    approval.save()
   196	
   197	    notify_approval_decided(approval)
   198	
   199	    application = approval.application
   200	    if approval.step == ApprovalStep.DORM_MANAGER:
   201	        # Auto-complete other pending dorm manager approvals for the same building
   202	        # (New requirement: any dorm manager in the building can approve, others see "already approved")
   203	        other_dorm_approvals = Approval.objects.filter(
   204	            application=application,
   205	            step=ApprovalStep.DORM_MANAGER,
   206	            decision=ApprovalDecision.PENDING
   207	        ).exclude(approval_id=approval.approval_id)
   208	
   209	        if other_dorm_approvals.exists():
   210	            now = timezone.now()
   211	            actual_approver = approval.decided_by or approval.approver
   212	            count = other_dorm_approvals.count()
   213	            for other_approval in other_dorm_approvals:
   214	                other_approval.decision = ApprovalDecision.APPROVED
   215	                other_approval.comment = f'已由{approval.approver_name}完成审批，无需重复操作'
   216	                other_approval.decided_at = now
   217	                other_approval.decided_by = actual_approver
   218	                other_approval.save()
   219	            logging.info(
   220	                f"Auto-completed {count} other dorm manager approvals "
   221	                f"for application {application.application_id} after approval by {actual_approver.user_id}"
   222	            )
   223	
   224	        # Check for existing counselor approval to prevent duplicates
   225	        existing_counselor_approval = Approval.objects.filter(
   226	            application=application,
   227	            step=ApprovalStep.COUNSELOR
   228	        ).exists()
   229	
   230	        if existing_counselor_approval:
   231	            return Response({'error': {'code': 'CONFLICT', 'message': '辅导员审批已存在，不能重复创建'}},
   232	                            status=status.HTTP_409_CONFLICT)
   233	
   234	        application.status = ApplicationStatus.PENDING_COUNSELOR
   235	        application.save()
   236	
   237	        # Get counselor by department (Phase 3 design: department-based routing)
   238	        # Note: Original design used ClassMapping (class_id), but Phase 3 user requirements
   239	        # changed to "按学院向辅导员审批" (approval by department/college).
   240	        # Multiple counselors per department are allowed (different classes within department).
   241	        # Selection: order_by('user_id') picks lowest ID for deterministic routing.
   242	        counselors = User.objects.filter(
   243	            role=UserRole.COUNSELOR,
   244	            department=application.student.department,
   245	            active=True
   246	        ).order_by('user_id')
   247	
   248	        if counselors.count() > 1:
   249	            logging.warning(
   250	                f"Multiple counselors found for department {application.student.department}: "
   251	                f"{counselors.count()} matches. Selected {counselors.first().user_id} via order_by('user_id')"
   252	            )
   253	
   254	        counselor = counselors.first()
   255	
   256	        if not counselor:
   257	            return Response({'error': {'code': 'NOT_FOUND', 'message': '该学院辅导员不存在',
   258	                                        'details': {'department': application.student.department}}},
   259	                            status=status.HTTP_404_NOT_FOUND)
   260	
   261	        Approval.objects.create(
   262	            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   263	            application=application,
   264	            step=ApprovalStep.COUNSELOR,
   265	            approver=counselor,
   266	            approver_name=counselor.name,
   267	            decision=ApprovalDecision.PENDING
   268	        )
   269	    elif approval.step == ApprovalStep.COUNSELOR:
   270	        # Counselor approval completes the process (2-level approval)
   271	        application.status = ApplicationStatus.APPROVED
   272	        application.save()
   273	
   274	    return Response(ApprovalSerializer(approval).data)
   275	
   276	
   277	@extend_schema(
   278	    operation_id='approvals_reject',
   279	    summary='驳回审批',
   280	    description='审批人驳回指定的审批申请',

exec
/bin/bash -lc "rtk nl -ba frontend/hooks/useAttachment.ts | sed -n '1,140p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// 附件操作Hook - 跨平台复用
     2	import { attachmentService } from '../services/attachment';
     3	
     4	export const useAttachment = () => {
     5	  const handlePreview = (attachmentId: string) => {
     6	    attachmentService.previewWeb(attachmentId);
     7	  };
     8	
     9	  const handleDownload = (attachmentId: string) => {
    10	    attachmentService.downloadWeb(attachmentId);
    11	  };
    12	
    13	  const getPreviewUrl = (attachmentId: string) => {
    14	    return attachmentService.getPreviewUrl(attachmentId);
    15	  };
    16	
    17	  const getDownloadUrl = (attachmentId: string) => {
    18	    return attachmentService.getDownloadUrl(attachmentId);
    19	  };
    20	
    21	  return {
    22	    handlePreview,
    23	    handleDownload,
    24	    getPreviewUrl,
    25	    getDownloadUrl,
    26	  };
    27	};

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/permissions.py | sed -n '1,220p'" in /home/caohui/projects/graduation-leave-system
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
    22	    if user.role in [UserRole.DEAN, UserRole.ADMIN]:
    23	        # Dean/Admin can view all applications
    24	        return True
    25	
    26	    return False

exec
/bin/bash -lc "rtk nl -ba frontend/services/attachment.ts | sed -n '1,200p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// 附件服务 - 跨平台复用
     2	export class AttachmentService {
     3	  private baseUrl: string;
     4	
     5	  constructor(baseUrl: string) {
     6	    this.baseUrl = baseUrl;
     7	  }
     8	
     9	  // 生成预览URL
    10	  getPreviewUrl(attachmentId: string): string {
    11	    return `${this.baseUrl}/api/attachments/${attachmentId}/download/?preview=true`;
    12	  }
    13	
    14	  // 生成下载URL
    15	  getDownloadUrl(attachmentId: string): string {
    16	    return `${this.baseUrl}/api/attachments/${attachmentId}/download/`;
    17	  }
    18	
    19	  // Web平台预览
    20	  previewWeb(attachmentId: string): void {
    21	    const url = this.getPreviewUrl(attachmentId);
    22	    window.open(url, '_blank');
    23	  }
    24	
    25	  // Web平台下载
    26	  downloadWeb(attachmentId: string): void {
    27	    const url = this.getDownloadUrl(attachmentId);
    28	    window.open(url, '_blank');
    29	  }
    30	}
    31	
    32	// 单例
    33	export const attachmentService = new AttachmentService(
    34	  process.env.API_BASE_URL || 'http://localhost:8000'
    35	);

codex
权限层面有一个细节需要特别指出：详情接口只允许“当前审批人”看详情，但附件下载使用的是 `can_view_application`，权限面更宽。我要再看前端实际调用路径，确认是否会把附件 ID 暴露给更多角色或出现鉴权绕过。
exec
/bin/bash -lc "rtk nl -ba frontend/miniprogram/pages/approval-detail/index.js | sed -n '1,240p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// 小程序审批详情页面逻辑
     2	const app = getApp();
     3	
     4	Page({
     5	  data: {
     6	    approval: null,
     7	  },
     8	
     9	  onLoad(options) {
    10	    const approvalId = options.id;
    11	    this.loadApprovalDetail(approvalId);
    12	  },
    13	
    14	  // 加载审批详情
    15	  async loadApprovalDetail(approvalId) {
    16	    wx.showLoading({ title: '加载中...' });
    17	    try {
    18	      const res = await wx.request({
    19	        url: `${app.globalData.apiBase}/api/approvals/${approvalId}/`,
    20	        method: 'GET',
    21	        header: {
    22	          'Authorization': `Bearer ${app.globalData.token}`
    23	        }
    24	      });
    25	      this.setData({ approval: res.data });
    26	    } catch (error) {
    27	      wx.showToast({ title: '加载失败', icon: 'none' });
    28	    } finally {
    29	      wx.hideLoading();
    30	    }
    31	  },
    32	
    33	  // 附件预览
    34	  handlePreview(e) {
    35	    const attachmentId = e.currentTarget.dataset.id;
    36	    const url = `${app.globalData.apiBase}/api/attachments/${attachmentId}/download/?preview=true`;
    37	
    38	    // 下载文件到临时路径
    39	    wx.downloadFile({
    40	      url: url,
    41	      header: {
    42	        'Authorization': `Bearer ${app.globalData.token}`
    43	      },
    44	      success: (res) => {
    45	        const filePath = res.tempFilePath;
    46	        const fileType = this.getFileType(filePath);
    47	
    48	        // 根据文件类型预览
    49	        if (fileType === 'image') {
    50	          wx.previewImage({
    51	            urls: [filePath],
    52	            current: filePath
    53	          });
    54	        } else if (fileType === 'pdf' || fileType === 'doc') {
    55	          wx.openDocument({
    56	            filePath: filePath,
    57	            showMenu: true
    58	          });
    59	        } else {
    60	          wx.showToast({ title: '不支持预览此文件类型', icon: 'none' });
    61	        }
    62	      },
    63	      fail: () => {
    64	        wx.showToast({ title: '预览失败', icon: 'none' });
    65	      }
    66	    });
    67	  },
    68	
    69	  // 下载附件
    70	  handleDownload(e) {
    71	    const attachmentId = e.currentTarget.dataset.id;
    72	    const url = `${app.globalData.apiBase}/api/attachments/${attachmentId}/download/`;
    73	
    74	    wx.downloadFile({
    75	      url: url,
    76	      header: {
    77	        'Authorization': `Bearer ${app.globalData.token}`
    78	      },
    79	      success: (res) => {
    80	        wx.saveFile({
    81	          tempFilePath: res.tempFilePath,
    82	          success: () => {
    83	            wx.showToast({ title: '下载成功', icon: 'success' });
    84	          }
    85	        });
    86	      },
    87	      fail: () => {
    88	        wx.showToast({ title: '下载失败', icon: 'none' });
    89	      }
    90	    });
    91	  },
    92	
    93	  // 判断文件类型
    94	  getFileType(filePath) {
    95	    const ext = filePath.split('.').pop().toLowerCase();
    96	    if (['jpg', 'jpeg', 'png', 'gif'].includes(ext)) return 'image';
    97	    if (ext === 'pdf') return 'pdf';
    98	    if (['doc', 'docx'].includes(ext)) return 'doc';
    99	    return 'other';
   100	  },
   101	
   102	  // 通过审批
   103	  handleApprove() {
   104	    wx.showModal({
   105	      title: '确认通过',
   106	      content: '确定通过该申请吗？',
   107	      success: (res) => {
   108	        if (res.confirm) {
   109	          this.submitApproval('approve');
   110	        }
   111	      }
   112	    });
   113	  },
   114	
   115	  // 驳回审批
   116	  handleReject() {
   117	    wx.showModal({
   118	      title: '确认驳回',
   119	      content: '确定驳回该申请吗？',
   120	      success: (res) => {
   121	        if (res.confirm) {
   122	          this.submitApproval('reject');
   123	        }
   124	      }
   125	    });
   126	  },
   127	
   128	  // 提交审批
   129	  async submitApproval(action) {
   130	    wx.showLoading({ title: '提交中...' });
   131	    try {
   132	      await wx.request({
   133	        url: `${app.globalData.apiBase}/api/approvals/${this.data.approval.approval_id}/${action}/`,
   134	        method: 'POST',
   135	        header: {
   136	          'Authorization': `Bearer ${app.globalData.token}`
   137	        },
   138	        data: { comment: '' }
   139	      });
   140	      wx.showToast({ title: '提交成功', icon: 'success' });
   141	      setTimeout(() => wx.navigateBack(), 1500);
   142	    } catch (error) {
   143	      wx.showToast({ title: '提交失败', icon: 'none' });
   144	    } finally {
   145	      wx.hideLoading();
   146	    }
   147	  }
   148	});

exec
/bin/bash -lc "rtk nl -ba frontend/mobile/ApprovalDetail.tsx | sed -n '1,260p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// 移动端审批详情组件 - React Native
     2	import React from 'react';
     3	import { View, Text, TouchableOpacity, Linking, StyleSheet } from 'react-native';
     4	
     5	interface Attachment {
     6	  attachment_id: string;
     7	  file_name: string;
     8	  file_size: number;
     9	}
    10	
    11	interface ApprovalDetail {
    12	  student_name: string;
    13	  student_id: string;
    14	  contact_phone: string;
    15	  leave_date: string;
    16	  reason: string;
    17	  attachments: Attachment[];
    18	  decision: string;
    19	}
    20	
    21	interface Props {
    22	  approval: ApprovalDetail;
    23	  onApprove?: () => void;
    24	  onReject?: () => void;
    25	}
    26	
    27	export const ApprovalDetailView: React.FC<Props> = ({ approval, onApprove, onReject }) => {
    28	  const handlePreview = (attachmentId: string) => {
    29	    const url = `${API_BASE_URL}/api/attachments/${attachmentId}/download/?preview=true`;
    30	    Linking.openURL(url);
    31	  };
    32	
    33	  const handleDownload = (attachmentId: string) => {
    34	    const url = `${API_BASE_URL}/api/attachments/${attachmentId}/download/`;
    35	    Linking.openURL(url);
    36	  };
    37	
    38	  return (
    39	    <View style={styles.container}>
    40	      {/* 基本信息 */}
    41	      <View style={styles.section}>
    42	        <Text style={styles.sectionTitle}>申请信息</Text>
    43	
    44	        <View style={styles.infoRow}>
    45	          <Text style={styles.label}>学生姓名：</Text>
    46	          <Text style={styles.value}>{approval.student_name}</Text>
    47	        </View>
    48	
    49	        <View style={styles.infoRow}>
    50	          <Text style={styles.label}>学号：</Text>
    51	          <Text style={styles.value}>{approval.student_id}</Text>
    52	        </View>
    53	
    54	        <View style={styles.infoRow}>
    55	          <Text style={styles.label}>联系电话：</Text>
    56	          <Text style={styles.value}>{approval.contact_phone}</Text>
    57	        </View>
    58	
    59	        <View style={styles.infoRow}>
    60	          <Text style={styles.label}>离校日期：</Text>
    61	          <Text style={styles.value}>{approval.leave_date}</Text>
    62	        </View>
    63	
    64	        <View style={styles.infoRow}>
    65	          <Text style={styles.label}>离校原因：</Text>
    66	          <Text style={styles.value}>{approval.reason}</Text>
    67	        </View>
    68	      </View>
    69	
    70	      {/* 附件列表 */}
    71	      {approval.attachments && approval.attachments.length > 0 && (
    72	        <View style={styles.section}>
    73	          <Text style={styles.sectionTitle}>附件材料</Text>
    74	
    75	          {approval.attachments.map((file) => (
    76	            <View key={file.attachment_id} style={styles.attachmentItem}>
    77	              <View style={styles.fileInfo}>
    78	                <Text style={styles.fileName}>{file.file_name}</Text>
    79	                <Text style={styles.fileSize}>
    80	                  ({(file.file_size / 1024).toFixed(2)} KB)
    81	                </Text>
    82	              </View>
    83	
    84	              <View style={styles.attachmentActions}>
    85	                {/* 附件预览按钮 */}
    86	                <TouchableOpacity
    87	                  style={[styles.button, styles.previewButton]}
    88	                  onPress={() => handlePreview(file.attachment_id)}
    89	                >
    90	                  <Text style={styles.buttonText}>附件预览</Text>
    91	                </TouchableOpacity>
    92	
    93	                <TouchableOpacity
    94	                  style={[styles.button, styles.downloadButton]}
    95	                  onPress={() => handleDownload(file.attachment_id)}
    96	                >
    97	                  <Text style={styles.buttonText}>下载</Text>
    98	                </TouchableOpacity>
    99	              </View>
   100	            </View>
   101	          ))}
   102	        </View>
   103	      )}
   104	
   105	      {/* 审批操作 */}
   106	      {approval.decision === 'pending' && (
   107	        <View style={styles.actionSection}>
   108	          <TouchableOpacity
   109	            style={[styles.button, styles.approveButton]}
   110	            onPress={onApprove}
   111	          >
   112	            <Text style={styles.buttonText}>通过</Text>
   113	          </TouchableOpacity>
   114	
   115	          <TouchableOpacity
   116	            style={[styles.button, styles.rejectButton]}
   117	            onPress={onReject}
   118	          >
   119	            <Text style={styles.buttonText}>驳回</Text>
   120	          </TouchableOpacity>
   121	        </View>
   122	      )}
   123	    </View>
   124	  );
   125	};
   126	
   127	const styles = StyleSheet.create({
   128	  container: {
   129	    flex: 1,
   130	    padding: 16,
   131	    backgroundColor: '#f5f5f5',
   132	  },
   133	  section: {
   134	    backgroundColor: '#fff',
   135	    borderRadius: 8,
   136	    padding: 16,
   137	    marginBottom: 16,
   138	  },
   139	  sectionTitle: {
   140	    fontSize: 18,
   141	    fontWeight: 'bold',
   142	    marginBottom: 12,
   143	    color: '#333',
   144	  },
   145	  infoRow: {
   146	    flexDirection: 'row',
   147	    marginBottom: 8,
   148	  },
   149	  label: {
   150	    fontSize: 14,
   151	    color: '#666',
   152	    width: 80,
   153	  },
   154	  value: {
   155	    fontSize: 14,
   156	    color: '#333',
   157	    flex: 1,
   158	  },
   159	  attachmentItem: {
   160	    borderTopWidth: 1,
   161	    borderTopColor: '#eee',
   162	    paddingTop: 12,
   163	    marginTop: 12,
   164	  },
   165	  fileInfo: {
   166	    marginBottom: 8,
   167	  },
   168	  fileName: {
   169	    fontSize: 14,
   170	    color: '#333',
   171	    marginBottom: 4,
   172	  },
   173	  fileSize: {
   174	    fontSize: 12,
   175	    color: '#999',
   176	  },
   177	  attachmentActions: {
   178	    flexDirection: 'row',
   179	    gap: 8,
   180	  },
   181	  button: {
   182	    flex: 1,
   183	    paddingVertical: 10,
   184	    paddingHorizontal: 16,
   185	    borderRadius: 4,
   186	    alignItems: 'center',
   187	  },
   188	  previewButton: {
   189	    backgroundColor: '#1890ff',
   190	  },
   191	  downloadButton: {
   192	    backgroundColor: '#52c41a',
   193	  },
   194	  buttonText: {
   195	    color: '#fff',
   196	    fontSize: 14,
   197	    fontWeight: '500',
   198	  },
   199	  actionSection: {
   200	    flexDirection: 'row',
   201	    gap: 12,
   202	    marginTop: 16,
   203	  },
   204	  approveButton: {
   205	    backgroundColor: '#52c41a',
   206	  },
   207	  rejectButton: {
   208	    backgroundColor: '#ff4d4f',
   209	  },
   210	});
   211	
   212	const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

exec
/bin/bash -lc "rtk nl -ba frontend/components/ApprovalDetail.tsx | sed -n '1,220p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// 审批详情组件 - 包含附件预览功能
     2	import React from 'react';
     3	import type { ApprovalDetail, Attachment } from '../types/api';
     4	import { useAttachment } from '../hooks/useAttachment';
     5	
     6	interface Props {
     7	  approval: ApprovalDetail;
     8	}
     9	
    10	export const ApprovalDetailView: React.FC<Props> = ({ approval }) => {
    11	  const { handlePreview, handleDownload } = useAttachment();
    12	
    13	  return (
    14	    <div className="approval-detail">
    15	      {/* 基本信息 */}
    16	      <div className="info-section">
    17	        <h3>申请信息</h3>
    18	        <div className="info-item">
    19	          <label>学生姓名：</label>
    20	          <span>{approval.student_name}</span>
    21	        </div>
    22	        <div className="info-item">
    23	          <label>学号：</label>
    24	          <span>{approval.student_id}</span>
    25	        </div>
    26	        <div className="info-item">
    27	          <label>联系电话：</label>
    28	          <span>{approval.contact_phone}</span>
    29	        </div>
    30	        <div className="info-item">
    31	          <label>离校日期：</label>
    32	          <span>{approval.leave_date}</span>
    33	        </div>
    34	        <div className="info-item">
    35	          <label>离校原因：</label>
    36	          <span>{approval.reason}</span>
    37	        </div>
    38	      </div>
    39	
    40	      {/* 附件列表 */}
    41	      {approval.attachments && approval.attachments.length > 0 && (
    42	        <div className="attachments-section">
    43	          <h3>附件材料</h3>
    44	          {approval.attachments.map((file: Attachment) => (
    45	            <div key={file.attachment_id} className="attachment-item">
    46	              <span className="file-name">{file.file_name}</span>
    47	              <span className="file-size">
    48	                ({(file.file_size / 1024).toFixed(2)} KB)
    49	              </span>
    50	              <div className="attachment-actions">
    51	                {/* 附件预览按钮 */}
    52	                <button
    53	                  className="btn-preview"
    54	                  onClick={() => handlePreview(file.attachment_id)}
    55	                >
    56	                  附件预览
    57	                </button>
    58	                <button
    59	                  className="btn-download"
    60	                  onClick={() => handleDownload(file.attachment_id)}
    61	                >
    62	                  下载
    63	                </button>
    64	              </div>
    65	            </div>
    66	          ))}
    67	        </div>
    68	      )}
    69	
    70	      {/* 审批操作 */}
    71	      <div className="approval-actions">
    72	        {approval.decision === 'pending' && (
    73	          <>
    74	            <button className="btn-approve">通过</button>
    75	            <button className="btn-reject">驳回</button>
    76	          </>
    77	        )}
    78	      </div>
    79	    </div>
    80	  );
    81	};

exec
/bin/bash -lc "rtk nl -ba frontend/miniprogram/pages/approval-detail/index.wxml | sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	<!-- 小程序审批详情页面 -->
     2	<view class="container">
     3	  <!-- 基本信息 -->
     4	  <view class="section">
     5	    <view class="section-title">申请信息</view>
     6	
     7	    <view class="info-row">
     8	      <text class="label">学生姓名：</text>
     9	      <text class="value">{{approval.student_name}}</text>
    10	    </view>
    11	
    12	    <view class="info-row">
    13	      <text class="label">学号：</text>
    14	      <text class="value">{{approval.student_id}}</text>
    15	    </view>
    16	
    17	    <view class="info-row">
    18	      <text class="label">联系电话：</text>
    19	      <text class="value">{{approval.contact_phone}}</text>
    20	    </view>
    21	
    22	    <view class="info-row">
    23	      <text class="label">离校日期：</text>
    24	      <text class="value">{{approval.leave_date}}</text>
    25	    </view>
    26	
    27	    <view class="info-row">
    28	      <text class="label">离校原因：</text>
    29	      <text class="value">{{approval.reason}}</text>
    30	    </view>
    31	  </view>
    32	
    33	  <!-- 附件列表 -->
    34	  <view class="section" wx:if="{{approval.attachments && approval.attachments.length > 0}}">
    35	    <view class="section-title">附件材料</view>
    36	
    37	    <view class="attachment-item" wx:for="{{approval.attachments}}" wx:key="attachment_id">
    38	      <view class="file-info">
    39	        <text class="file-name">{{item.file_name}}</text>
    40	        <text class="file-size">({{item.file_size / 1024}}KB)</text>
    41	      </view>
    42	
    43	      <view class="attachment-actions">
    44	        <!-- 附件预览按钮 -->
    45	        <button
    46	          class="btn btn-preview"
    47	          bindtap="handlePreview"
    48	          data-id="{{item.attachment_id}}"
    49	        >
    50	          附件预览
    51	        </button>
    52	
    53	        <button
    54	          class="btn btn-download"
    55	          bindtap="handleDownload"
    56	          data-id="{{item.attachment_id}}"
    57	        >
    58	          下载
    59	        </button>
    60	      </view>
    61	    </view>
    62	  </view>
    63	
    64	  <!-- 审批操作 -->
    65	  <view class="action-section" wx:if="{{approval.decision === 'pending'}}">
    66	    <button class="btn btn-approve" bindtap="handleApprove">通过</button>
    67	    <button class="btn btn-reject" bindtap="handleReject">驳回</button>
    68	  </view>
    69	</view>

codex
前端多端实现里还有几个可编译性/运行时问题：PC 组件依赖未声明的类型字段，React Native 里重复实现了附件 URL 拼接，小程序页把 `wx.request` 当 Promise 用。最后我会再查测试覆盖和接口契约，判断是否已有回归保护。
exec
/bin/bash -lc "rtk find frontend -maxdepth 2 -type f \\( -name 'package.json' -o -name 'tsconfig*.json' -o -name '*.env*' -o -name 'vite.config.*' -o -name 'next.config.*' \\) -print" in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
rtk: rtk find does not support compound predicates or actions (e.g. -not, -exec). Use `find` directly.

exec
/bin/bash -lc 'rtk ls -la frontend' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
.omc/
components/
hooks/
miniprogram/
mobile/
services/
types/

exec
/bin/bash -lc "rtk rg -n \"get_approval|download_attachment|preview|attachments|ApprovalDetail|Attachment\" backend/apps frontend -S --glob '*test*' --glob '*.py' --glob '*.ts' --glob '*.tsx' --glob '*.js'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
frontend/services/attachment.ts:2:export class AttachmentService {
frontend/services/attachment.ts:11:    return `${this.baseUrl}/api/attachments/${attachmentId}/download/?preview=true`;
frontend/services/attachment.ts:16:    return `${this.baseUrl}/api/attachments/${attachmentId}/download/`;
frontend/services/attachment.ts:20:  previewWeb(attachmentId: string): void {
frontend/services/attachment.ts:33:export const attachmentService = new AttachmentService(
backend/apps/approvals/urls.py:7:    path('<str:approval_id>/', views.get_approval, name='get_approval'),
frontend/components/ApprovalDetail.tsx:3:import type { ApprovalDetail, Attachment } from '../types/api';
frontend/components/ApprovalDetail.tsx:4:import { useAttachment } from '../hooks/useAttachment';
frontend/components/ApprovalDetail.tsx:7:  approval: ApprovalDetail;
frontend/components/ApprovalDetail.tsx:10:export const ApprovalDetailView: React.FC<Props> = ({ approval }) => {
frontend/components/ApprovalDetail.tsx:11:  const { handlePreview, handleDownload } = useAttachment();
frontend/components/ApprovalDetail.tsx:41:      {approval.attachments && approval.attachments.length > 0 && (
frontend/components/ApprovalDetail.tsx:42:        <div className="attachments-section">
frontend/components/ApprovalDetail.tsx:44:          {approval.attachments.map((file: Attachment) => (
frontend/components/ApprovalDetail.tsx:53:                  className="btn-preview"
frontend/miniprogram/pages/approval-detail/index.js:11:    this.loadApprovalDetail(approvalId);
frontend/miniprogram/pages/approval-detail/index.js:15:  async loadApprovalDetail(approvalId) {
frontend/miniprogram/pages/approval-detail/index.js:36:    const url = `${app.globalData.apiBase}/api/attachments/${attachmentId}/download/?preview=true`;
frontend/miniprogram/pages/approval-detail/index.js:50:          wx.previewImage({
frontend/miniprogram/pages/approval-detail/index.js:72:    const url = `${app.globalData.apiBase}/api/attachments/${attachmentId}/download/`;
backend/apps/applications/permissions.py:6:    """Check if user can view application and its attachments."""
frontend/types/api.ts:58:  approvals: ApprovalDetail[];
frontend/types/api.ts:62:export interface ApprovalDetail {
backend/apps/approvals/views.py:120:def get_approval(request, approval_id):
frontend/hooks/useAttachment.ts:4:export const useAttachment = () => {
frontend/hooks/useAttachment.ts:6:    attachmentService.previewWeb(attachmentId);
backend/apps/attachments/serializers.py:2:from .models import Attachment, AttachmentType
backend/apps/attachments/serializers.py:5:class AttachmentUploadSerializer(serializers.Serializer):
backend/apps/attachments/serializers.py:7:    attachment_type = serializers.ChoiceField(choices=AttachmentType.choices)
backend/apps/attachments/serializers.py:23:class AttachmentSerializer(serializers.ModelSerializer):
backend/apps/attachments/serializers.py:25:        model = Attachment
backend/apps/attachments/serializers.py:30:class AttachmentListResponseSerializer(serializers.Serializer):
backend/apps/attachments/serializers.py:32:    attachments = AttachmentSerializer(many=True)
backend/apps/attachments/models.py:6:class AttachmentType(models.TextChoices):
backend/apps/attachments/models.py:13:class Attachment(models.Model):
backend/apps/attachments/models.py:15:    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='attachments')
backend/apps/attachments/models.py:17:    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
backend/apps/attachments/models.py:18:    attachment_type = models.CharField(max_length=50, choices=AttachmentType.choices)
backend/apps/attachments/models.py:27:        db_table = 'attachments'
backend/apps/attachments/views.py:13:from .models import Attachment
backend/apps/attachments/views.py:14:from .serializers import AttachmentUploadSerializer, AttachmentSerializer, AttachmentListResponseSerializer
backend/apps/attachments/views.py:21:    operation_id='attachments_list',
backend/apps/attachments/views.py:25:        200: AttachmentListResponseSerializer,
backend/apps/attachments/views.py:33:    operation_id='attachments_upload',
backend/apps/attachments/views.py:36:    request=AttachmentUploadSerializer,
backend/apps/attachments/views.py:38:        201: AttachmentSerializer,
backend/apps/attachments/views.py:48:def attachments_view(request, application_id):
backend/apps/attachments/views.py:51:        return list_attachments(request, application_id)
backend/apps/attachments/views.py:72:    serializer = AttachmentUploadSerializer(data=request.data)
backend/apps/attachments/views.py:80:    attachment = Attachment.objects.create(
backend/apps/attachments/views.py:91:    return Response(AttachmentSerializer(attachment).data, status=status.HTTP_201_CREATED)
backend/apps/attachments/views.py:94:def list_attachments(request, application_id):
backend/apps/attachments/views.py:109:    # List attachments (exclude soft-deleted)
backend/apps/attachments/views.py:110:    attachments = Attachment.objects.filter(application=application, is_deleted=False)
backend/apps/attachments/views.py:111:    serializer = AttachmentSerializer(attachments, many=True)
backend/apps/attachments/views.py:112:    return Response({'attachments': serializer.data})
backend/apps/attachments/views.py:116:    operation_id='attachments_download',
backend/apps/attachments/views.py:128:def download_attachment(request, attachment_id):
backend/apps/attachments/views.py:133:        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
backend/apps/attachments/views.py:134:    except Attachment.DoesNotExist:
backend/apps/attachments/views.py:151:        # Check if preview mode (query param: ?preview=true)
backend/apps/attachments/views.py:152:        preview_mode = request.GET.get('preview', 'false').lower() == 'true'
backend/apps/attachments/views.py:155:            as_attachment=not preview_mode,
backend/apps/attachments/views.py:165:    operation_id='attachments_delete',
backend/apps/attachments/views.py:183:        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
backend/apps/attachments/views.py:184:    except Attachment.DoesNotExist:
backend/apps/attachments/urls.py:5:    path('applications/<str:application_id>/attachments/', views.attachments_view, name='attachments'),
backend/apps/attachments/urls.py:6:    path('attachments/<str:attachment_id>/download/', views.download_attachment, name='download_attachment'),
backend/apps/attachments/urls.py:7:    path('attachments/<str:attachment_id>/', views.delete_attachment, name='delete_attachment'),
frontend/mobile/ApprovalDetail.tsx:5:interface Attachment {
frontend/mobile/ApprovalDetail.tsx:11:interface ApprovalDetail {
frontend/mobile/ApprovalDetail.tsx:17:  attachments: Attachment[];
frontend/mobile/ApprovalDetail.tsx:22:  approval: ApprovalDetail;
frontend/mobile/ApprovalDetail.tsx:27:export const ApprovalDetailView: React.FC<Props> = ({ approval, onApprove, onReject }) => {
frontend/mobile/ApprovalDetail.tsx:29:    const url = `${API_BASE_URL}/api/attachments/${attachmentId}/download/?preview=true`;
frontend/mobile/ApprovalDetail.tsx:34:    const url = `${API_BASE_URL}/api/attachments/${attachmentId}/download/`;
frontend/mobile/ApprovalDetail.tsx:71:      {approval.attachments && approval.attachments.length > 0 && (
frontend/mobile/ApprovalDetail.tsx:75:          {approval.attachments.map((file) => (
frontend/mobile/ApprovalDetail.tsx:87:                  style={[styles.button, styles.previewButton]}
frontend/mobile/ApprovalDetail.tsx:188:  previewButton: {
backend/apps/approvals/serializers.py:36:    attachments = serializers.SerializerMethodField()
backend/apps/approvals/serializers.py:42:                  'contact_phone', 'reason', 'leave_date', 'attachments', 'step', 'approver_id',
backend/apps/approvals/serializers.py:45:                            'contact_phone', 'reason', 'leave_date', 'attachments', 'step',
backend/apps/approvals/serializers.py:48:    def get_attachments(self, obj):
backend/apps/approvals/serializers.py:49:        from apps.attachments.serializers import AttachmentSerializer
backend/apps/approvals/serializers.py:50:        return AttachmentSerializer(
backend/apps/approvals/serializers.py:51:            obj.application.attachments.filter(is_deleted=False),
backend/apps/applications/serializers.py:30:    def get_approvals(self, obj):
backend/apps/attachments/migrations/0001_initial.py:19:            name='Attachment',
backend/apps/attachments/migrations/0001_initial.py:22:                ('file', models.FileField(upload_to='attachments/%Y/%m/%d/')),
backend/apps/attachments/migrations/0001_initial.py:30:                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='applications.application')),
backend/apps/attachments/migrations/0001_initial.py:34:                'db_table': 'attachments',
backend/apps/applications/management/commands/reset_test_data.py:4:from apps.attachments.models import Attachment
backend/apps/applications/management/commands/reset_test_data.py:11:        # Delete all attachments
backend/apps/applications/management/commands/reset_test_data.py:12:        attachment_count = Attachment.objects.count()
backend/apps/applications/management/commands/reset_test_data.py:13:        Attachment.objects.all().delete()
backend/apps/attachments/tests/test_download.py:9:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_download.py:12:class AttachmentDownloadTestCase(TestCase):
backend/apps/attachments/tests/test_download.py:71:        self.attachment = Attachment.objects.create(
backend/apps/attachments/tests/test_download.py:76:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_download.py:87:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:98:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:108:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:122:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_delete.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_delete.py:11:class AttachmentDeleteTestCase(TestCase):
backend/apps/attachments/tests/test_delete.py:70:        self.attachment = Attachment.objects.create(
backend/apps/attachments/tests/test_delete.py:75:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_delete.py:86:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:101:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:116:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:130:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_list.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_list.py:11:class AttachmentListTestCase(TestCase):
backend/apps/attachments/tests/test_list.py:92:        self.attachment = Attachment.objects.create(
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
backend/apps/attachments/tests/test_upload.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_upload.py:11:class AttachmentUploadTestCase(TestCase):
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
backend/apps/attachments/tests/test_upload.py:159:            f'/api/applications/{self.application.application_id}/attachments/',

exec
/bin/bash -lc "rtk rg -n \"API_BASE_URL|NEXT_PUBLIC|VITE|process\\.env\" -S frontend demo-web" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
demo-web/js/api.js:2:const API_BASE_URL = `http://${window.location.hostname}:7787/api`;
demo-web/js/api.js:63:        const response = await fetch(API_BASE_URL + '/auth/login', {
demo-web/js/api.js:105:        const response = await fetch(API_BASE_URL + '/applications/', {
demo-web/js/api.js:124:        const response = await fetch(API_BASE_URL + '/applications/', {
demo-web/js/api.js:138:        const url = API_BASE_URL + '/approvals/?decision=' + decision + '&limit=' + limit + '&offset=' + offset;
demo-web/js/api.js:153:        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/approve/', {
demo-web/js/api.js:167:        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/reject/', {
demo-web/js/api.js:185:        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
demo-web/js/api.js:201:        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
demo-web/js/api.js:215:        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/' + attachmentId + '/', {
demo-web/mobile-sso-callback.html:49:    const API_BASE_URL = 'http://218.75.196.218:7787';
demo-web/mobile-sso-callback.html:71:        const response = await fetch(`${API_BASE_URL}/api/sso/qingganlian/mobile/saas-login`, {
demo-web/mobile-sso-callback.html:104:        const response = await fetch(`${API_BASE_URL}/api/sso/qingganlian/mobile/login`, {
frontend/services/attachment.ts:34:  process.env.API_BASE_URL || 'http://localhost:8000'
demo-web/index.html:212:        const res = await fetch(API_BASE_URL + '/approvals/' + id + '/', {
demo-web/index.html:218:            const appRes = await fetch(API_BASE_URL + '/applications/' + detail.application_id + '/', {
demo-web/index.html:447:            const res = await fetch(API_BASE_URL + '/approvals/export/', {
demo-web/admin-sso-callback.html:49:    const API_BASE_URL = 'http://218.75.196.218:7787';
demo-web/admin-sso-callback.html:62:        const response = await fetch(`${API_BASE_URL}/api/sso/qingganlian/admin/login`, {
frontend/mobile/ApprovalDetail.tsx:29:    const url = `${API_BASE_URL}/api/attachments/${attachmentId}/download/?preview=true`;
frontend/mobile/ApprovalDetail.tsx:34:    const url = `${API_BASE_URL}/api/attachments/${attachmentId}/download/`;
frontend/mobile/ApprovalDetail.tsx:212:const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

codex
测试检索显示已有下载/列表测试，但没有命中 `preview=true` 的回归用例，也没有审批详情新增附件字段的测试。为了判断权限断言是否够，我会读取现有附件下载测试。
exec
/bin/bash -lc "rtk nl -ba backend/apps/attachments/tests/test_download.py | sed -n '1,220p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.test import TestCase
     2	from django.core.files.uploadedfile import SimpleUploadedFile
     3	from rest_framework.test import APIClient
     4	from rest_framework import status
     5	from apps.users.models import User, UserRole
     6	from apps.users.class_mapping import ClassMapping
     7	from apps.applications.models import Application, ApplicationStatus
     8	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
     9	from apps.attachments.models import Attachment, AttachmentType
    10	
    11	
    12	class AttachmentDownloadTestCase(TestCase):
    13	    def setUp(self):
    14	        self.client = APIClient()
    15	
    16	        # Create students
    17	        self.student = User.objects.create_user(
    18	            user_id='2020001',
    19	            password='2020001',
    20	            name='张三',
    21	            role=UserRole.STUDENT,
    22	            class_id='CS2020-01',
    23	            is_graduating=True,
    24	            graduation_year=2024,
    25	            building='1号楼',
    26	            department='计算机学院'
    27	        )
    28	
    29	        self.other_student = User.objects.create_user(
    30	            user_id='2020002',
    31	            password='2020002',
    32	            name='李四',
    33	            role=UserRole.STUDENT,
    34	            class_id='CS2020-02',
    35	            is_graduating=True,
    36	            graduation_year=2024,
    37	            building='2号楼',
    38	            department='软件学院'
    39	        )
    40	
    41	        # Create counselor
    42	        self.counselor = User.objects.create_user(
    43	            user_id='T001',
    44	            password='T001',
    45	            name='李老师',
    46	            role=UserRole.COUNSELOR,
    47	            department='计算机学院'
    48	        )
    49	
    50	        # Create class mapping
    51	        ClassMapping.objects.create(
    52	            class_id='CS2020-01',
    53	            counselor=self.counselor,
    54	            counselor_name='李老师',
    55	            active=True
    56	        )
    57	
    58	        # Create application
    59	        self.application = Application.objects.create(
    60	            application_id='app_test001',
    61	            student=self.student,
    62	            student_name='张三',
    63	            class_id='CS2020-01',
    64	            reason='毕业离校',
    65	            leave_date='2024-07-01',
    66	            status=ApplicationStatus.PENDING_COUNSELOR
    67	        )
    68	
    69	        # Create attachment with actual file
    70	        test_file = SimpleUploadedFile("test.pdf", b"test file content", content_type="application/pdf")
    71	        self.attachment = Attachment.objects.create(
    72	            attachment_id='att_test001',
    73	            application=self.application,
    74	            uploaded_by=self.student,
    75	            file=test_file,
    76	            attachment_type=AttachmentType.DORM_CHECKOUT,
    77	            file_name='test.pdf',
    78	            file_size=1024,
    79	            content_type='application/pdf'
    80	        )
    81	
    82	    def test_download_positive_student(self):
    83	        """Student can download own application attachment"""
    84	        self.client.force_authenticate(user=self.student)
    85	
    86	        response = self.client.get(
    87	            f'/api/attachments/{self.attachment.attachment_id}/download/'
    88	        )
    89	
    90	        self.assertEqual(response.status_code, status.HTTP_200_OK)
    91	        self.assertEqual(response['Content-Type'], 'application/pdf')
    92	
    93	    def test_download_positive_counselor(self):
    94	        """Assigned counselor can download attachment"""
    95	        self.client.force_authenticate(user=self.counselor)
    96	
    97	        response = self.client.get(
    98	            f'/api/attachments/{self.attachment.attachment_id}/download/'
    99	        )
   100	
   101	        self.assertEqual(response.status_code, status.HTTP_200_OK)
   102	
   103	    def test_download_forbidden(self):
   104	        """Unauthorized student cannot download attachment"""
   105	        self.client.force_authenticate(user=self.other_student)
   106	
   107	        response = self.client.get(
   108	            f'/api/attachments/{self.attachment.attachment_id}/download/'
   109	        )
   110	
   111	        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
   112	        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
   113	
   114	    def test_download_soft_deleted_returns_404(self):
   115	        """Soft-deleted attachment returns 404"""
   116	        self.attachment.is_deleted = True
   117	        self.attachment.save()
   118	
   119	        self.client.force_authenticate(user=self.student)
   120	
   121	        response = self.client.get(
   122	            f'/api/attachments/{self.attachment.attachment_id}/download/'
   123	        )
   124	
   125	        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
   126	        self.assertEqual(response.data['error']['code'], 'NOT_FOUND')

exec
/bin/bash -lc 'rtk rg -n "class .*Approval|approvals_get|ApprovalSerializer|ApprovalDetail|ApprovalListItem|ApplicationBrief" backend/apps/approvals/tests backend -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/approvals/tests/test_state_machine.py:10:class ApprovalStateMachineTestCase(TestCase):
backend/apps/approvals/tests/test_permissions.py:10:class ApprovalPermissionsTestCase(TestCase):
backend/apps/approvals/tests/test_list_permissions.py:8:class ApprovalListPermissionTest(TestCase):
backend/apps/approvals/admin.py:6:class ApprovalAdmin(admin.ModelAdmin):
backend/apps/approvals/views.py:14:from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalListSerializer, ApprovalListResponseSerializer
backend/apps/approvals/views.py:108:    operation_id='approvals_get',
backend/apps/approvals/views.py:112:        200: ApprovalSerializer,
backend/apps/approvals/views.py:131:        return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:143:        200: ApprovalSerializer,
backend/apps/approvals/views.py:274:    return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:283:        200: ApprovalSerializer,
backend/apps/approvals/views.py:343:    return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/serializers.py:5:class ApplicationBriefSerializer(serializers.Serializer):
backend/apps/approvals/serializers.py:14:class ApprovalListSerializer(serializers.ModelSerializer):
backend/apps/approvals/serializers.py:17:    application = ApplicationBriefSerializer(read_only=True)
backend/apps/approvals/serializers.py:28:class ApprovalSerializer(serializers.ModelSerializer):
backend/apps/approvals/serializers.py:56:class ApprovalActionSerializer(serializers.Serializer):
backend/apps/approvals/serializers.py:60:class ApprovalListResponseSerializer(serializers.Serializer):
backend/apps/approvals/pagination.py:5:class ApprovalLimitOffsetPagination(LimitOffsetPagination):
backend/apps/applications/serializers.py:31:        from apps.approvals.serializers import ApprovalSerializer
backend/apps/applications/serializers.py:32:        return ApprovalSerializer(obj.approvals.all(), many=True).data
backend/apps/approvals/tests/test_list_permissions.py:8:class ApprovalListPermissionTest(TestCase):
backend/apps/approvals/tests/test_permissions.py:10:class ApprovalPermissionsTestCase(TestCase):
backend/apps/applications/tests/test_p0_fixes.py:84:class ApprovalDecisionFilterTest(TestCase):
backend/apps/approvals/tests/test_state_machine.py:10:class ApprovalStateMachineTestCase(TestCase):
backend/apps/approvals/models.py:6:class ApprovalStep(models.TextChoices):
backend/apps/approvals/models.py:12:class ApprovalDecision(models.TextChoices):
backend/apps/approvals/models.py:18:class Approval(models.Model):
backend/apps/notifications/tests/test_timeout_warnings.py:13:class ApprovalTimeoutWarningTests(TestCase):

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/serializers.py | sed -n '1,140p'" in /home/caohui/projects/graduation-leave-system
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

exec
/bin/bash -lc "rtk nl -ba backend/apps/attachments/serializers.py | sed -n '1,100p'" in /home/caohui/projects/graduation-leave-system
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

codex
还有一个后端性能/契约问题：`ApplicationSerializer.get_approvals()` 复用了现在带附件的 `ApprovalSerializer`，这会让“申请详情”也递归带上每个审批的附件列表。我要确认相关接口是否可能放大 payload 或造成 N+1。
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
    24	    decided_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='decided_approvals', null=True, blank=True, verbose_name='实际审批人')
    25	    decision = models.CharField(max_length=20, choices=ApprovalDecision.choices, default=ApprovalDecision.PENDING)
    26	    comment = models.TextField(null=True, blank=True)
    27	    decided_at = models.DateTimeField(null=True, blank=True)
    28	    created_at = models.DateTimeField(auto_now_add=True)
    29	    updated_at = models.DateTimeField(auto_now=True)
    30	
    31	    class Meta:
    32	        db_table = 'approvals'

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/tests/test_permissions.py | sed -n '1,260p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.test import TestCase
     2	from rest_framework.test import APIClient
     3	from rest_framework import status
     4	from apps.users.models import User, UserRole
     5	from apps.applications.models import Application, ApplicationStatus
     6	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
     7	from apps.users.class_mapping import ClassMapping
     8	
     9	
    10	class ApprovalPermissionsTestCase(TestCase):
    11	    def setUp(self):
    12	        # Create students
    13	        self.student1 = User.objects.create_user(
    14	            user_id='2020001',
    15	            name='张三',
    16	            role=UserRole.STUDENT,
    17	            class_id='CS2020-01',
    18	            password='2020001',
    19	            building='1号楼',
    20	            department='计算机学院'
    21	        )
    22	        self.student2 = User.objects.create_user(
    23	            user_id='2020002',
    24	            name='李四',
    25	            role=UserRole.STUDENT,
    26	            class_id='CS2020-02',
    27	            password='2020002',
    28	            building='2号楼',
    29	            department='软件学院'
    30	        )
    31	
    32	        # Create counselors
    33	        self.counselor1 = User.objects.create_user(
    34	            user_id='T001',
    35	            name='李老师',
    36	            role=UserRole.COUNSELOR,
    37	            password='T001',
    38	            department='计算机学院'
    39	        )
    40	        self.counselor2 = User.objects.create_user(
    41	            user_id='T002',
    42	            name='王老师',
    43	            role=UserRole.COUNSELOR,
    44	            password='T002',
    45	            department='软件学院'
    46	        )
    47	        self.dorm_manager1 = User.objects.create_user(
    48	            user_id='M001',
    49	            name='宿管员1',
    50	            role=UserRole.DORM_MANAGER,
    51	            password='M001',
    52	            building='1号楼'
    53	        )
    54	        self.dorm_manager2 = User.objects.create_user(
    55	            user_id='M002',
    56	            name='宿管员2',
    57	            role=UserRole.DORM_MANAGER,
    58	            password='M002',
    59	            building='2号楼'
    60	        )
    61	        self.dean1 = User.objects.create_user(
    62	            user_id='D001',
    63	            name='赵主任',
    64	            role=UserRole.DEAN,
    65	            password='D001'
    66	        )
    67	        self.dean2 = User.objects.create_user(
    68	            user_id='D002',
    69	            name='钱主任',
    70	            role=UserRole.DEAN,
    71	            password='D002'
    72	        )
    73	
    74	        # Create class mappings
    75	        ClassMapping.objects.create(
    76	            class_id='CS2020-01',
    77	            dorm_manager=self.dorm_manager1,
    78	            dorm_manager_name='宿管员1',
    79	            counselor=self.counselor1,
    80	            counselor_name='李老师',
    81	            active=True
    82	        )
    83	        ClassMapping.objects.create(
    84	            class_id='CS2020-02',
    85	            dorm_manager=self.dorm_manager2,
    86	            dorm_manager_name='宿管员2',
    87	            counselor=self.counselor2,
    88	            counselor_name='王老师',
    89	            active=True
    90	        )
    91	
    92	        # Create application for student1
    93	        self.application1 = Application.objects.create(
    94	            application_id='app_test001',
    95	            student=self.student1,
    96	            student_name='张三',
    97	            class_id='CS2020-01',
    98	            reason='测试原因',
    99	            leave_date='2024-06-30',
   100	            status=ApplicationStatus.PENDING_COUNSELOR
   101	        )
   102	
   103	        # Create counselor approval for application1
   104	        self.approval1 = Approval.objects.create(
   105	            approval_id='apv_test001',
   106	            application=self.application1,
   107	            step=ApprovalStep.COUNSELOR,
   108	            approver=self.counselor1,
   109	            approver_name='李老师',
   110	            decision=ApprovalDecision.PENDING
   111	        )
   112	
   113	        self.client = APIClient()
   114	
   115	    def _create_dorm_manager_approval(self):
   116	        self.application1.status = ApplicationStatus.PENDING_DORM_MANAGER
   117	        self.application1.save()
   118	        return Approval.objects.create(
   119	            approval_id='apv_test002',
   120	            application=self.application1,
   121	            step=ApprovalStep.DORM_MANAGER,
   122	            approver=self.dorm_manager1,
   123	            approver_name='宿管员1',
   124	            decision=ApprovalDecision.PENDING
   125	        )
   126	
   127	    def test_student_cannot_approve_or_reject(self):
   128	        """学生不能调用审批操作接口"""
   129	        self.client.force_authenticate(user=self.student1)
   130	
   131	        approve_response = self.client.post(
   132	            f'/api/approvals/{self.approval1.approval_id}/approve/',
   133	            {'comment': '同意'},
   134	            format='json'
   135	        )
   136	        reject_response = self.client.post(
   137	            f'/api/approvals/{self.approval1.approval_id}/reject/',
   138	            {'comment': '不同意'},
   139	            format='json'
   140	        )
   141	
   142	        self.assertEqual(approve_response.status_code, status.HTTP_403_FORBIDDEN)
   143	        self.assertEqual(reject_response.status_code, status.HTTP_403_FORBIDDEN)
   144	
   145	    def test_dean_cannot_act_on_counselor_step(self):
   146	        """学工部不能处理辅导员审批步骤"""
   147	        self.client.force_authenticate(user=self.dean1)
   148	
   149	        response = self.client.post(
   150	            f'/api/approvals/{self.approval1.approval_id}/approve/',
   151	            {'comment': '同意'},
   152	            format='json'
   153	        )
   154	
   155	        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
   156	
   157	    def test_counselor_cannot_act_on_dorm_manager_step(self):
   158	        """辅导员不能处理宿管员审批步骤"""
   159	        dorm_manager_approval = self._create_dorm_manager_approval()
   160	        self.client.force_authenticate(user=self.counselor1)
   161	
   162	        response = self.client.post(
   163	            f'/api/approvals/{dorm_manager_approval.approval_id}/approve/',
   164	            {'comment': '同意'},
   165	            format='json'
   166	        )
   167	
   168	        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
   169	
   170	    def test_non_assigned_dorm_manager_forbidden(self):
   171	        """同角色但非指定宿管员审批人不能处理审批"""
   172	        dorm_manager_approval = self._create_dorm_manager_approval()
   173	        self.client.force_authenticate(user=self.dorm_manager2)
   174	
   175	        response = self.client.post(
   176	            f'/api/approvals/{dorm_manager_approval.approval_id}/reject/',
   177	            {'comment': '不同意'},
   178	            format='json'
   179	        )
   180	
   181	        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
   182	
   183	    def test_cross_counselor_approve_forbidden(self):
   184	        """测试跨辅导员审批返回403"""
   185	        # T002 tries to approve T001's application
   186	        self.client.force_authenticate(user=self.counselor2)
   187	        response = self.client.post(
   188	            f'/api/approvals/{self.approval1.approval_id}/approve/',
   189	            {'comment': '同意'},
   190	            format='json'
   191	        )
   192	        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
   193	
   194	    def test_cross_counselor_reject_forbidden(self):
   195	        """测试跨辅导员驳回返回403"""
   196	        # T002 tries to reject T001's application
   197	        self.client.force_authenticate(user=self.counselor2)
   198	        response = self.client.post(
   199	            f'/api/approvals/{self.approval1.approval_id}/reject/',
   200	            {'comment': '不同意'},
   201	            format='json'
   202	        )
   203	        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/tests/test_list_permissions.py | sed -n '1,220p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.test import TestCase
     2	from rest_framework.test import APIClient
     3	from apps.users.models import User, UserRole
     4	from apps.applications.models import Application, ApplicationStatus
     5	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
     6	
     7	
     8	class ApprovalListPermissionTest(TestCase):
     9	    def setUp(self):
    10	        self.client = APIClient()
    11	
    12	        # Create users
    13	        self.student = User.objects.create(user_id='S001', name='学生', role=UserRole.STUDENT, class_id='CS2020-01')
    14	        self.student.set_password('S001')
    15	        self.student.save()
    16	
    17	        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
    18	        self.counselor1.set_password('T001')
    19	        self.counselor1.save()
    20	
    21	        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
    22	        self.counselor2.set_password('T002')
    23	        self.counselor2.save()
    24	
    25	        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
    26	        self.dorm_manager1.set_password('M001')
    27	        self.dorm_manager1.save()
    28	
    29	        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
    30	        self.dorm_manager2.set_password('M002')
    31	        self.dorm_manager2.save()
    32	
    33	        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
    34	        self.dean1.set_password('D001')
    35	        self.dean1.save()
    36	
    37	        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
    38	        self.dean2.set_password('D002')
    39	        self.dean2.save()
    40	
    41	        # Create application
    42	        self.app = Application.objects.create(
    43	            application_id='app_001',
    44	            student=self.student,
    45	            student_name='学生',
    46	            class_id='CS2020-01',
    47	            reason='测试',
    48	            leave_date='2024-07-01',
    49	            status=ApplicationStatus.PENDING_COUNSELOR
    50	        )
    51	
    52	        # Create approvals
    53	        self.approval_c1 = Approval.objects.create(
    54	            approval_id='apv_c1',
    55	            application=self.app,
    56	            step=ApprovalStep.COUNSELOR,
    57	            approver=self.counselor1,
    58	            approver_name='辅导员1',
    59	            decision=ApprovalDecision.PENDING
    60	        )
    61	
    62	        self.approval_m1 = Approval.objects.create(
    63	            approval_id='apv_m1',
    64	            application=self.app,
    65	            step=ApprovalStep.DORM_MANAGER,
    66	            approver=self.dorm_manager1,
    67	            approver_name='宿管员1',
    68	            decision=ApprovalDecision.PENDING
    69	        )
    70	
    71	    def test_student_403_on_approval_list(self):
    72	        self.client.force_authenticate(user=self.student)
    73	        response = self.client.get('/api/approvals/')
    74	        self.assertEqual(response.status_code, 403)
    75	        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
    76	
    77	    def test_counselor_sees_only_own_pending_approvals(self):
    78	        self.client.force_authenticate(user=self.counselor1)
    79	        response = self.client.get('/api/approvals/')
    80	        self.assertEqual(response.status_code, 200)
    81	        self.assertEqual(response.data['count'], 1)
    82	        self.assertEqual(response.data['results'][0]['approval_id'], 'apv_c1')
    83	
    84	    def test_counselor_cannot_see_other_counselor_approvals(self):
    85	        self.client.force_authenticate(user=self.counselor2)
    86	        response = self.client.get('/api/approvals/')
    87	        self.assertEqual(response.data['count'], 0)
    88	
    89	    def test_dorm_manager_sees_only_own_pending_approvals(self):
    90	        self.client.force_authenticate(user=self.dorm_manager1)
    91	        response = self.client.get('/api/approvals/')
    92	        self.assertEqual(response.status_code, 200)
    93	        self.assertEqual(response.data['count'], 1)
    94	        self.assertEqual(response.data['results'][0]['approval_id'], 'apv_m1')
    95	
    96	    def test_dorm_manager_cannot_see_other_dorm_manager_approvals(self):
    97	        self.client.force_authenticate(user=self.dorm_manager2)
    98	        response = self.client.get('/api/approvals/')
    99	        self.assertEqual(response.data['count'], 0)
   100	
   101	    def test_dean_sees_all_approvals_for_archive(self):
   102	        self.client.force_authenticate(user=self.dean1)
   103	        response = self.client.get('/api/approvals/')
   104	        self.assertEqual(response.status_code, 200)
   105	        self.assertEqual(response.data['count'], 2)
   106	
   107	    def test_response_format_count_and_results(self):
   108	        self.client.force_authenticate(user=self.counselor1)
   109	        response = self.client.get('/api/approvals/')
   110	        self.assertIn('count', response.data)
   111	        self.assertIn('results', response.data)
   112	        self.assertNotIn('next', response.data)
   113	        self.assertNotIn('previous', response.data)
   114	
   115	    def test_decision_all_does_not_leak_cross_approver_data(self):
   116	        # Create second application and approval for counselor1 (approved)
   117	        app2 = Application.objects.create(
   118	            application_id='app_002',
   119	            student=self.student,
   120	            student_name='学生',
   121	            class_id='CS2020-01',
   122	            reason='测试2',
   123	            leave_date='2024-07-02',
   124	            status=ApplicationStatus.APPROVED
   125	        )
   126	        approval_c1_approved = Approval.objects.create(
   127	            approval_id='apv_c1_approved',
   128	            application=app2,
   129	            step=ApprovalStep.COUNSELOR,
   130	            approver=self.counselor1,
   131	            approver_name='辅导员1',
   132	            decision=ApprovalDecision.APPROVED
   133	        )
   134	
   135	        # Create approval for counselor2
   136	        app3 = Application.objects.create(
   137	            application_id='app_003',
   138	            student=self.student,
   139	            student_name='学生',
   140	            class_id='CS2020-01',
   141	            reason='测试3',
   142	            leave_date='2024-07-03',
   143	            status=ApplicationStatus.PENDING_COUNSELOR
   144	        )
   145	        approval_c2 = Approval.objects.create(
   146	            approval_id='apv_c2',
   147	            application=app3,
   148	            step=ApprovalStep.COUNSELOR,
   149	            approver=self.counselor2,
   150	            approver_name='辅导员2',
   151	            decision=ApprovalDecision.PENDING
   152	        )
   153	
   154	        # Counselor1 calls decision=all
   155	        self.client.force_authenticate(user=self.counselor1)
   156	        response = self.client.get('/api/approvals/?decision=all')
   157	        self.assertEqual(response.status_code, 200)
   158	        self.assertEqual(response.data['count'], 2)
   159	
   160	        # Verify only counselor1's approvals returned
   161	        approval_ids = [a['approval_id'] for a in response.data['results']]
   162	        self.assertIn('apv_c1', approval_ids)
   163	        self.assertIn('apv_c1_approved', approval_ids)
   164	        self.assertNotIn('apv_c2', approval_ids)

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/views.py | sed -n '1,240p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import status
     2	from rest_framework.decorators import api_view, permission_classes, parser_classes
     3	from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
     4	from rest_framework.permissions import IsAuthenticated
     5	from rest_framework.response import Response
     6	from django.utils import timezone
     7	from drf_spectacular.utils import extend_schema, OpenApiParameter
     8	from .models import Application, ApplicationStatus, DormCheckoutStatus
     9	from .serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationListSerializer, ApplicationListResponseSerializer
    10	from .pagination import ApplicationLimitOffsetPagination
    11	from .providers import MockDormCheckoutProvider
    12	from .permissions import can_view_application
    13	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
    14	from apps.users.models import UserRole, User
    15	from apps.notifications.services import notify_application_submitted
    16	from schema import ErrorResponseSerializer
    17	import uuid
    18	import logging
    19	
    20	
    21	@extend_schema(
    22	    methods=['GET'],
    23	    operation_id='applications_list',
    24	    summary='获取申请列表',
    25	    description='获取当前用户的申请列表（学生/辅导员/学工部）',
    26	    parameters=[
    27	        OpenApiParameter('status', str, description='状态过滤'),
    28	        OpenApiParameter('limit', int, description='每页数量（默认20）'),
    29	        OpenApiParameter('offset', int, description='偏移量（默认0）'),
    30	    ],
    31	    responses={
    32	        200: ApplicationListResponseSerializer,
    33	        403: ErrorResponseSerializer,
    34	    },
    35	    tags=['申请']
    36	)
    37	@extend_schema(
    38	    methods=['POST'],
    39	    operation_id='applications_create',
    40	    summary='提交离校申请',
    41	    description='学生提交新的离校申请',
    42	    request=ApplicationCreateSerializer,
    43	    responses={
    44	        201: ApplicationSerializer,
    45	        400: ErrorResponseSerializer,
    46	        403: ErrorResponseSerializer,
    47	        404: ErrorResponseSerializer,
    48	        409: ErrorResponseSerializer,
    49	        422: ErrorResponseSerializer,
    50	    },
    51	    tags=['申请']
    52	)
    53	@api_view(['GET', 'POST'])
    54	@permission_classes([IsAuthenticated])
    55	@parser_classes([JSONParser, MultiPartParser, FormParser])
    56	def applications_view(request):
    57	    if request.method == 'GET':
    58	        return list_applications(request)
    59	    else:
    60	        return create_application(request)
    61	
    62	
    63	def list_applications(request):
    64	    user = request.user
    65	
    66	    # Student: own applications only
    67	    if user.role == UserRole.STUDENT:
    68	        queryset = Application.objects.filter(student=user)
    69	
    70	    # Dorm Manager: applications with own pending dorm manager approvals
    71	    elif user.role == UserRole.DORM_MANAGER:
    72	        pending_approvals = Approval.objects.filter(
    73	            approver=user,
    74	            step=ApprovalStep.DORM_MANAGER,
    75	            decision=ApprovalDecision.PENDING
    76	        ).values_list('application', flat=True)
    77	        queryset = Application.objects.filter(pk__in=pending_approvals)
    78	
    79	    # Counselor: applications with own pending counselor approvals
    80	    elif user.role == UserRole.COUNSELOR:
    81	        pending_approvals = Approval.objects.filter(
    82	            approver=user,
    83	            step=ApprovalStep.COUNSELOR,
    84	            decision=ApprovalDecision.PENDING
    85	        ).values_list('application', flat=True)
    86	        queryset = Application.objects.filter(pk__in=pending_approvals)
    87	
    88	    # Dean/Admin: view all applications
    89	    elif user.role in [UserRole.DEAN, UserRole.ADMIN]:
    90	        queryset = Application.objects.all()
    91	
    92	    else:
    93	        return Response(
    94	            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
    95	            status=status.HTTP_403_FORBIDDEN
    96	        )
    97	
    98	    # Status filtering
    99	    status_param = request.query_params.get('status')
   100	    if status_param:
   101	        queryset = queryset.filter(status=status_param)
   102	
   103	    # Sort by created_at DESC
   104	    queryset = queryset.order_by('-created_at', '-application_id')
   105	
   106	    # Paginate
   107	    paginator = ApplicationLimitOffsetPagination()
   108	    page = paginator.paginate_queryset(queryset, request)
   109	
   110	    # Serialize
   111	    serializer = ApplicationListSerializer(page, many=True)
   112	
   113	    return paginator.get_paginated_response(serializer.data)
   114	
   115	
   116	def create_application(request):
   117	    from django.db import transaction
   118	
   119	    user = request.user
   120	
   121	    if user.role != UserRole.STUDENT:
   122	        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以提交申请'}},
   123	                        status=status.HTTP_403_FORBIDDEN)
   124	
   125	    serializer = ApplicationCreateSerializer(data=request.data)
   126	    if not serializer.is_valid():
   127	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
   128	                                    'details': serializer.errors}},
   129	                        status=status.HTTP_400_BAD_REQUEST)
   130	
   131	    with transaction.atomic():
   132	        # Check for existing pending/approved applications
   133	        existing = Application.objects.select_for_update().filter(
   134	            student=user,
   135	            status__in=[ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.APPROVED]
   136	        ).first()
   137	        if existing:
   138	            return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
   139	                                        'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
   140	                            status=status.HTTP_409_CONFLICT)
   141	
   142	        provider = MockDormCheckoutProvider()
   143	        dorm_status = provider.check_status(user.user_id)
   144	
   145	        if dorm_status.status != DormCheckoutStatus.COMPLETED:
   146	            return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
   147	                                        'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
   148	                                                    'blocking_reason': dorm_status.blocking_reason}}},
   149	                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
   150	
   151	        # Find dorm managers
   152	        dorm_managers = []
   153	        building = user.building
   154	
   155	        if building and building.strip():
   156	            dorm_managers = list(User.objects.filter(
   157	                role=UserRole.DORM_MANAGER,
   158	                building=building,
   159	                active=True
   160	            ).order_by('user_id'))
   161	
   162	        if not dorm_managers:
   163	            from django.conf import settings
   164	            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
   165	            try:
   166	                fallback_manager = User.objects.get(role=UserRole.DORM_MANAGER, user_id=fallback_id, active=True)
   167	                dorm_managers = [fallback_manager]
   168	            except User.DoesNotExist:
   169	                return Response({'error': {'code': 'NOT_FOUND', 'message': '无可用宿管员',
   170	                                            'details': {'building': building or '未分配', 'fallback_id': fallback_id}}},
   171	                                status=status.HTTP_404_NOT_FOUND)
   172	
   173	        # Check for existing draft, convert if exists
   174	        draft = Application.objects.select_for_update().filter(student=user, status=ApplicationStatus.DRAFT).first()
   175	
   176	        if draft:
   177	            # Update draft to submitted application
   178	            draft.contact_phone = serializer.validated_data['contact_phone']
   179	            draft.reason = serializer.validated_data.get('reason', '')
   180	            draft.leave_date = serializer.validated_data['leave_date']
   181	            draft.status = ApplicationStatus.PENDING_DORM_MANAGER
   182	            draft.dorm_checkout_status = dorm_status.status
   183	            draft.save()
   184	            application = draft
   185	        else:
   186	            # Create new application
   187	            application = Application.objects.create(
   188	                application_id=f'app_{uuid.uuid4().hex[:8]}',
   189	                student=user,
   190	                student_name=user.name,
   191	                class_id=user.class_id,
   192	                contact_phone=serializer.validated_data['contact_phone'],
   193	                reason=serializer.validated_data.get('reason', ''),
   194	                leave_date=serializer.validated_data['leave_date'],
   195	                status=ApplicationStatus.PENDING_DORM_MANAGER,
   196	                dorm_checkout_status=dorm_status.status
   197	            )
   198	
   199	        # Create approvals
   200	        for dorm_manager in dorm_managers:
   201	            dorm_manager_approval = Approval.objects.create(
   202	                approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   203	                application=application,
   204	                step=ApprovalStep.DORM_MANAGER,
   205	                approver=dorm_manager,
   206	                approver_name=dorm_manager.name,
   207	                decision=ApprovalDecision.PENDING
   208	            )
   209	            notify_application_submitted(application, dorm_manager_approval)
   210	
   211	        # Sync phone to User table
   212	        if not user.phone:
   213	            user.phone = serializer.validated_data['contact_phone']
   214	            user.save()
   215	
   216	    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
   217	
   218	
   219	@extend_schema(
   220	    operation_id='applications_get',
   221	    summary='获取申请详情',
   222	    description='获取指定申请的详细信息（包括审批记录）',
   223	    responses={
   224	        200: ApplicationSerializer,
   225	        403: ErrorResponseSerializer,
   226	        404: ErrorResponseSerializer,
   227	    },
   228	    tags=['申请']
   229	)
   230	@api_view(['GET'])
   231	@permission_classes([IsAuthenticated])
   232	def get_application(request, application_id):
   233	    try:
   234	        application = Application.objects.get(application_id=application_id)
   235	    except Application.DoesNotExist:
   236	        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在',
   237	                                    'details': {'application_id': application_id}}},
   238	                        status=status.HTTP_404_NOT_FOUND)
   239	
   240	    user = request.user

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/tests/test_permissions.py | sed -n '1,260p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
nl: backend/apps/applications/tests/test_permissions.py: No such file or directory

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/views.py | sed -n '232,330p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   232	def get_application(request, application_id):
   233	    try:
   234	        application = Application.objects.get(application_id=application_id)
   235	    except Application.DoesNotExist:
   236	        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在',
   237	                                    'details': {'application_id': application_id}}},
   238	                        status=status.HTTP_404_NOT_FOUND)
   239	
   240	    user = request.user
   241	
   242	    # Check permission using shared helper
   243	    if not can_view_application(user, application):
   244	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
   245	                        status=status.HTTP_403_FORBIDDEN)
   246	
   247	    return Response(ApplicationSerializer(application).data)
   248	
   249	
   250	@extend_schema(
   251	    operation_id='applications_draft',
   252	    summary='获取或创建草稿申请',
   253	    description='学生获取或创建草稿申请，用于附件上传前置',
   254	    responses={
   255	        200: ApplicationSerializer,
   256	        201: ApplicationSerializer,
   257	        403: ErrorResponseSerializer,
   258	    },
   259	    tags=['申请']
   260	)
   261	@api_view(['POST'])
   262	@permission_classes([IsAuthenticated])
   263	def get_or_create_draft(request):
   264	    from django.db import transaction
   265	
   266	    user = request.user
   267	
   268	    if user.role != UserRole.STUDENT:
   269	        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以创建草稿'}},
   270	                        status=status.HTTP_403_FORBIDDEN)
   271	
   272	    with transaction.atomic():
   273	        # Get existing draft or create new one
   274	        draft = Application.objects.select_for_update().filter(student=user, status=ApplicationStatus.DRAFT).first()
   275	
   276	    if draft:
   277	        return Response(ApplicationSerializer(draft).data, status=status.HTTP_200_OK)
   278	
   279	    # Create new draft
   280	    draft = Application.objects.create(
   281	        application_id=f'app_{uuid.uuid4().hex[:8]}',
   282	        student=user,
   283	        student_name=user.name,
   284	        class_id=user.class_id,
   285	        status=ApplicationStatus.DRAFT
   286	    )
   287	
   288	    return Response(ApplicationSerializer(draft).data, status=status.HTTP_201_CREATED)

exec
/bin/bash -lc 'rtk rg -n "get_application|applications/.*/|applications_get|approvals" backend/apps/applications/tests -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/applications/tests/test_p0_fixes.py:4:from apps.approvals.models import Approval, ApprovalDecision, ApprovalStep
backend/apps/applications/tests/test_p0_fixes.py:129:        # Create approvals
backend/apps/applications/tests/test_p0_fixes.py:133:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/tests/test_p0_fixes.py:142:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/tests/test_p0_fixes.py:151:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/tests/test_p0_fixes.py:157:    def test_filter_pending_approvals(self):
backend/apps/applications/tests/test_p0_fixes.py:158:        approvals = Approval.objects.filter(
backend/apps/applications/tests/test_p0_fixes.py:162:        self.assertEqual(approvals.count(), 1)
backend/apps/applications/tests/test_p0_fixes.py:163:        self.assertEqual(approvals.first().approval_id, 'apv_pending')
backend/apps/applications/tests/test_p0_fixes.py:165:    def test_filter_approved_approvals(self):
backend/apps/applications/tests/test_p0_fixes.py:166:        approvals = Approval.objects.filter(
backend/apps/applications/tests/test_p0_fixes.py:170:        self.assertEqual(approvals.count(), 1)
backend/apps/applications/tests/test_p0_fixes.py:171:        self.assertEqual(approvals.first().approval_id, 'apv_approved')
backend/apps/applications/tests/test_p0_fixes.py:173:    def test_filter_rejected_approvals(self):
backend/apps/applications/tests/test_p0_fixes.py:174:        approvals = Approval.objects.filter(
backend/apps/applications/tests/test_p0_fixes.py:178:        self.assertEqual(approvals.count(), 1)
backend/apps/applications/tests/test_p0_fixes.py:179:        self.assertEqual(approvals.first().approval_id, 'apv_rejected')
backend/apps/applications/tests/test_p0_fixes.py:181:    def test_filter_all_approvals(self):
backend/apps/applications/tests/test_p0_fixes.py:182:        approvals = Approval.objects.filter(approver=self.counselor)
backend/apps/applications/tests/test_p0_fixes.py:183:        self.assertEqual(approvals.count(), 3)
backend/apps/applications/tests/test_error_cases.py:154:        response = self.client.get(f'/api/applications/{application_id}/')
backend/apps/applications/tests/test_error_cases.py:167:        response = self.client.get('/api/applications/app_nonexistent/')
backend/apps/applications/tests/test_detail_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/applications/tests/test_detail_permissions.py:66:        response = self.client.get(f'/api/applications/{app_id}/')
backend/apps/applications/tests/test_detail_permissions.py:83:        response = self.client.get(f'/api/applications/{app_id}/')
backend/apps/applications/tests/test_detail_permissions.py:100:        response = self.client.get(f'/api/applications/{app_id}/')
backend/apps/applications/tests/test_application_flow.py:9:from apps.approvals.models import ApprovalDecision, ApprovalStep
backend/apps/applications/tests/test_application_flow.py:93:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/applications/tests/test_application_flow.py:96:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/approve/', {
backend/apps/applications/tests/test_application_flow.py:113:        counselor_approval = application.approvals.get(step=ApprovalStep.COUNSELOR)
backend/apps/applications/tests/test_application_flow.py:116:        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/approve/', {
backend/apps/applications/tests/test_application_flow.py:128:        response = self.client.get(f'/api/applications/{application_id}/')
backend/apps/applications/tests/test_application_flow.py:131:        self.assertEqual(len(response.data['approvals']), 2)  # 2-level approval
backend/apps/applications/tests/test_list_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/applications/tests/test_list_permissions.py:67:        # Create approvals
backend/apps/applications/tests/test_list_permissions.py:71:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/tests/test_list_permissions.py:90:    def test_counselor_sees_only_pending_counselor_approvals(self):
backend/apps/applications/tests/test_list_permissions.py:109:    def test_response_format_no_nested_approvals(self):
backend/apps/applications/tests/test_list_permissions.py:114:        self.assertNotIn('approvals', response.data['results'][0])

codex
我还注意到审批列表 serializer 使用 `id` 字段，而前端类型仍写 `approval_id`，这可能是既有不一致；本次新增详情字段又扩大了这个问题。审计结论里我会把“本次变更直接引入”和“已有但会被放大”的问题区分开。
exec
/bin/bash -lc "rtk nl -ba demo-web/index.html | sed -n '190,245p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   190	        tabs.forEach((tab, index) => {
   191	            tab.classList.remove('active');
   192	            if ((filter === 'all' && index === 0) ||
   193	                (filter === 'pending' && index === 1) ||
   194	                (filter === 'decided' && index === 2)) {
   195	                tab.classList.add('active');
   196	            }
   197	        });
   198	
   199	        // Reload list with filter
   200	        if (currentUser && currentUser.role === 'student') {
   201	            loadMyApplications();
   202	        } else {
   203	            loadApprovals();
   204	        }
   205	    }
   206	
   207	    let currentApprovalId = null;
   208	    async function openApproval(id) {
   209	        currentApprovalId = id;
   210	        showScreen(2);
   211	
   212	        const res = await fetch(API_BASE_URL + '/approvals/' + id + '/', {
   213	            headers: getAuthHeaders()
   214	        });
   215	        if (res.ok) {
   216	            const detail = await res.json();
   217	
   218	            const appRes = await fetch(API_BASE_URL + '/applications/' + detail.application_id + '/', {
   219	                headers: getAuthHeaders()
   220	            });
   221	            const appData = appRes.ok ? await appRes.json() : null;
   222	
   223	            // Fetch attachments
   224	            const attachments = await apiGetAttachments(detail.application_id);
   225	
   226	            const container = document.querySelector('#screen-2');
   227	
   228	            const basicInfoHtml = '<div class="card">' +
   229	                '<div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">基本信息</div>' +
   230	                '<div style="display: flex; margin-bottom: 8px;">' +
   231	                  '<span style="font-size: 14px; color: #999; width: 80px;">申请ID:</span>' +
   232	                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.application_id || detail.id.substring(0,8)) + '</span>' +
   233	                '</div>' +
   234	                '<div style="display: flex; margin-bottom: 8px;">' +
   235	                  '<span style="font-size: 14px; color: #999; width: 80px;">学生:</span>' +
   236	                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.student_name || '-') + ' (' + (detail.student_id || '-') + ')</span>' +
   237	                '</div>' +
   238	                '<div style="display: flex; margin-bottom: 8px;">' +
   239	                  '<span style="font-size: 14px; color: #999; width: 80px;">联系电话:</span>' +
   240	                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.contact_phone || '-') + '</span>' +
   241	                '</div>' +
   242	                '<div style="display: flex; margin-bottom: 8px;">' +
   243	                  '<span style="font-size: 14px; color: #999; width: 80px;">申请原因:</span>' +
   244	                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.reason || '无') + '</span>' +
   245	                '</div>' +

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/tests/test_detail_permissions.py | sed -n '1,130p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.test import TestCase
     2	from rest_framework.test import APIClient
     3	from apps.users.models import User, UserRole
     4	from apps.users.class_mapping import ClassMapping
     5	from apps.applications.models import Application, ApplicationStatus
     6	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
     7	from django.utils import timezone
     8	
     9	
    10	class ApplicationDetailPermissionTest(TestCase):
    11	    def setUp(self):
    12	        self.client = APIClient()
    13	
    14	        # Students (use IDs that mock provider recognizes as COMPLETED)
    15	        self.student1 = User.objects.create(user_id='2020001', name='学生1', role=UserRole.STUDENT, class_id='CS2020-01', building='1号楼', department='计算机学院')
    16	        self.student1.set_password('2020001')
    17	        self.student1.save()
    18	
    19	        self.student2 = User.objects.create(user_id='2020002', name='学生2', role=UserRole.STUDENT, class_id='CS2020-02', building='2号楼', department='软件学院')
    20	        self.student2.set_password('2020002')
    21	        self.student2.save()
    22	
    23	        # Counselors
    24	        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR, department='计算机学院')
    25	        self.counselor1.set_password('T001')
    26	        self.counselor1.save()
    27	
    28	        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR, department='软件学院')
    29	        self.counselor2.set_password('T002')
    30	        self.counselor2.save()
    31	
    32	        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER, building='1号楼')
    33	        self.dorm_manager1.set_password('M001')
    34	        self.dorm_manager1.save()
    35	
    36	        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER, building='2号楼')
    37	        self.dorm_manager2.set_password('M002')
    38	        self.dorm_manager2.save()
    39	
    40	        # Deans
    41	        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
    42	        self.dean1.set_password('D001')
    43	        self.dean1.save()
    44	
    45	        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
    46	        self.dean2.set_password('D002')
    47	        self.dean2.save()
    48	
    49	        # Class mappings
    50	        ClassMapping.objects.create(class_id='CS2020-01', dorm_manager=self.dorm_manager1, dorm_manager_name='宿管员1', counselor=self.counselor1, counselor_name='辅导员1', active=True)
    51	        ClassMapping.objects.create(class_id='CS2020-02', dorm_manager=self.dorm_manager2, dorm_manager_name='宿管员2', counselor=self.counselor2, counselor_name='辅导员2', active=True)
    52	
    53	    def test_student_cannot_access_other_student_application(self):
    54	        # Student1 creates application
    55	        self.client.force_authenticate(user=self.student1)
    56	        response = self.client.post('/api/applications/', {
    57	            'contact_phone': '13800138000',
    58	            'reason': '测试',
    59	            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
    60	        }, format='json')
    61	        self.assertEqual(response.status_code, 201)
    62	        app_id = response.data['application_id']
    63	
    64	        # Student2 tries to access Student1's application
    65	        self.client.force_authenticate(user=self.student2)
    66	        response = self.client.get(f'/api/applications/{app_id}/')
    67	        self.assertEqual(response.status_code, 403)
    68	        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
    69	
    70	    def test_counselor_cannot_access_cross_class_application(self):
    71	        # Student from CS2020-01 creates application
    72	        self.client.force_authenticate(user=self.student1)
    73	        response = self.client.post('/api/applications/', {
    74	            'contact_phone': '13800138000',
    75	            'reason': '测试',
    76	            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
    77	        }, format='json')
    78	        self.assertEqual(response.status_code, 201)
    79	        app_id = response.data['application_id']
    80	
    81	        # Counselor T002 (assigned to CS2020-02) tries to access
    82	        self.client.force_authenticate(user=self.counselor2)
    83	        response = self.client.get(f'/api/applications/{app_id}/')
    84	        self.assertEqual(response.status_code, 403)
    85	        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
    86	
    87	    def test_dean_cannot_access_in_progress_application(self):
    88	        # Student creates application
    89	        self.client.force_authenticate(user=self.student1)
    90	        response = self.client.post('/api/applications/', {
    91	            'contact_phone': '13800138000',
    92	            'reason': '测试',
    93	            'leave_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
    94	        }, format='json')
    95	        self.assertEqual(response.status_code, 201)
    96	        app_id = response.data['application_id']
    97	
    98	        # Dean archive role cannot access in-progress applications
    99	        self.client.force_authenticate(user=self.dean2)
   100	        response = self.client.get(f'/api/applications/{app_id}/')
   101	        self.assertEqual(response.status_code, 403)
   102	        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

exec
/bin/bash -lc "rtk nl -ba demo-web/js/api.js | sed -n '1,260p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// API Integration Layer
     2	const API_BASE_URL = `http://${window.location.hostname}:7787/api`;
     3	
     4	let currentToken = null;
     5	let currentUser = null;
     6	
     7	// 页面加载时自动恢复登录状态
     8	function restoreAuthState() {
     9	    const savedToken = localStorage.getItem('auth_token');
    10	    const savedUser = localStorage.getItem('user_info');
    11	
    12	    if (savedToken) {
    13	        currentToken = savedToken;
    14	        if (savedUser) {
    15	            try {
    16	                currentUser = JSON.parse(savedUser);
    17	                console.log('Auth state restored from localStorage', currentUser);
    18	            } catch (e) {
    19	                console.error('Failed to parse user info:', e);
    20	            }
    21	        }
    22	    }
    23	}
    24	
    25	// 恢复登录后初始化UI
    26	function initializeUIAfterRestore(user) {
    27	    // 隐藏登录界面
    28	    const loginScreen = document.getElementById('screen-login');
    29	    if (loginScreen && loginScreen.classList.contains('active')) {
    30	        loginScreen.classList.remove('active');
    31	
    32	        // 显示导航栏和用户栏
    33	        const navTabs = document.getElementById('navTabs');
    34	        const userBar = document.getElementById('userBar');
    35	        if (navTabs) navTabs.style.display = 'flex';
    36	        if (userBar) userBar.style.display = 'flex';
    37	
    38	        // 显示用户信息
    39	        const userNameEl = document.getElementById('currentUserName');
    40	        const userRoleEl = document.getElementById('currentUserRole');
    41	        if (userNameEl && user.real_name) userNameEl.textContent = user.real_name;
    42	        if (userRoleEl && user.role) {
    43	            const roleMap = { 'student': '学生', 'dorm_manager': '宿管', 'counselor': '辅导员', 'dean': '学工部', 'admin': '管理员' };
    44	            userRoleEl.textContent = '(' + (roleMap[user.role] || user.role) + ')';
    45	        }
    46	
    47	        // 根据角色显示对应界面
    48	        if (user.role === 'student') {
    49	            if (typeof showScreen === 'function') showScreen(0);
    50	        } else {
    51	            if (typeof showScreen === 'function') showScreen(1); // 审批列表
    52	        }
    53	
    54	        console.log('UI initialized for user:', user.username);
    55	    }
    56	}
    57	
    58	// 页面加载时立即执行
    59	restoreAuthState();
    60	
    61	async function apiLogin(userId, password) {
    62	    try {
    63	        const response = await fetch(API_BASE_URL + '/auth/login', {
    64	            method: 'POST',
    65	            headers: { 'Content-Type': 'application/json' },
    66	            body: JSON.stringify({
    67	                user_id: userId,
    68	                password: password
    69	            })
    70	        });
    71	
    72	        if (response.ok) {
    73	            const data = await response.json();
    74	            currentToken = data.access_token;
    75	            currentUser = data.user;
    76	            return { success: true, user: data.user };
    77	        } else {
    78	            currentToken = null;
    79	            currentUser = null;
    80	            const error = await response.json().catch(() => ({ error: 'Login failed' }));
    81	            return { success: false, error: error };
    82	        }
    83	    } catch (e) {
    84	        console.error("Login failed:", e);
    85	        currentToken = null;
    86	        currentUser = null;
    87	        return { success: false, error: 'Network error' };
    88	    }
    89	}
    90	
    91	function getAuthHeaders() {
    92	    return {
    93	        'Authorization': 'Bearer ' + currentToken
    94	    };
    95	}
    96	
    97	async function apiSubmitApplication(phone, reason, leaveDate, files) {
    98	    const formData = new FormData();
    99	    formData.append('contact_phone', phone);
   100	    formData.append('reason', reason);
   101	    formData.append('leave_date', leaveDate);
   102	    files.forEach(f => formData.append('attachments', f));
   103	
   104	    try {
   105	        const response = await fetch(API_BASE_URL + '/applications/', {
   106	            method: 'POST',
   107	            headers: { 'Authorization': 'Bearer ' + currentToken },
   108	            body: formData
   109	        });
   110	        if (response.ok) {
   111	            return { success: true, data: await response.json() };
   112	        } else {
   113	            const error = await response.json().catch(() => ({ error: { message: '提交失败' } }));
   114	            return { success: false, error: error.error || { message: '提交失败' } };
   115	        }
   116	    } catch (e) {
   117	        console.error("Submit application failed:", e);
   118	        return { success: false, error: { message: '网络错误，请检查连接' } };
   119	    }
   120	}
   121	
   122	async function apiGetApplications() {
   123	    try {
   124	        const response = await fetch(API_BASE_URL + '/applications/', {
   125	            headers: getAuthHeaders()
   126	        });
   127	        if (response.ok) {
   128	            return await response.json();
   129	        }
   130	    } catch (e) {
   131	        console.error("Get applications failed:", e);
   132	    }
   133	    return { results: [] };
   134	}
   135	
   136	async function apiGetApprovals(decision = 'pending', limit = 20, offset = 0) {
   137	    try {
   138	        const url = API_BASE_URL + '/approvals/?decision=' + decision + '&limit=' + limit + '&offset=' + offset;
   139	        const response = await fetch(url, {
   140	            headers: getAuthHeaders()
   141	        });
   142	        if (response.ok) {
   143	            return await response.json();
   144	        }
   145	    } catch (e) {
   146	        console.error("Get approvals failed:", e);
   147	    }
   148	    return { results: [], count: 0 };
   149	}
   150	
   151	async function apiApprove(approvalId, comment) {
   152	    try {
   153	        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/approve/', {
   154	            method: 'POST',
   155	            headers: Object.assign({}, getAuthHeaders(), { 'Content-Type': 'application/json' }),
   156	            body: JSON.stringify({ comment: comment })
   157	        });
   158	        return response.ok;
   159	    } catch (e) {
   160	        console.error("Approve failed:", e);
   161	        return false;
   162	    }
   163	}
   164	
   165	async function apiReject(approvalId, comment) {
   166	    try {
   167	        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/reject/', {
   168	            method: 'POST',
   169	            headers: Object.assign({}, getAuthHeaders(), { 'Content-Type': 'application/json' }),
   170	            body: JSON.stringify({ comment: comment })
   171	        });
   172	        return response.ok;
   173	    } catch (e) {
   174	        console.error("Reject failed:", e);
   175	        return false;
   176	    }
   177	}
   178	
   179	async function apiUploadAttachment(applicationId, file, attachmentType = 'other') {
   180	    const formData = new FormData();
   181	    formData.append('file', file);
   182	    formData.append('attachment_type', attachmentType);
   183	
   184	    try {
   185	        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
   186	            method: 'POST',
   187	            headers: getAuthHeaders(),
   188	            body: formData
   189	        });
   190	        if (response.ok) {
   191	            return await response.json();
   192	        }
   193	    } catch (e) {
   194	        console.error("Upload attachment failed:", e);
   195	    }
   196	    return null;
   197	}
   198	
   199	async function apiGetAttachments(applicationId) {
   200	    try {
   201	        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
   202	            headers: getAuthHeaders()
   203	        });
   204	        if (response.ok) {
   205	            return await response.json();
   206	        }
   207	    } catch (e) {
   208	        console.error("Get attachments failed:", e);
   209	    }
   210	    return [];
   211	}
   212	
   213	async function apiDeleteAttachment(applicationId, attachmentId) {
   214	    try {
   215	        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/' + attachmentId + '/', {
   216	            method: 'DELETE',
   217	            headers: getAuthHeaders()
   218	        });
   219	        return response.ok;
   220	    } catch (e) {
   221	        console.error("Delete attachment failed:", e);
   222	        return false;
   223	    }
   224	}
   225	
   226	// DOM加载完成后，如果有token则自动初始化UI
   227	if (typeof document !== 'undefined') {
   228	    document.addEventListener('DOMContentLoaded', function() {
   229	        if (currentToken && currentUser) {
   230	            console.log('Initializing UI after token restore');
   231	            initializeUIAfterRestore(currentUser);
   232	        }
   233	    });
   234	}

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/tests/test_application_flow.py | sed -n '120,145p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   120	        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)
   121	
   122	        # Step 7: 查询申请状态 - 辅导员审批后直接完成（2级审批）
   123	        application.refresh_from_db()
   124	        self.assertEqual(application.status, ApplicationStatus.APPROVED)
   125	
   126	        # Step 8: 最终状态查询
   127	        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
   128	        response = self.client.get(f'/api/applications/{application_id}/')
   129	        self.assertEqual(response.status_code, status.HTTP_200_OK)
   130	        self.assertEqual(response.data['status'], ApplicationStatus.APPROVED)
   131	        self.assertEqual(len(response.data['approvals']), 2)  # 2-level approval

codex
我会跑一组后端定向测试作为辅助证据，尤其是附件下载权限。前端这边目录看起来不是完整可构建项目，若没有 package/tsconfig，我会以静态审查为准。
exec
/bin/bash -lc "rtk rg --files -g 'package.json' -g 'tsconfig*.json' -g 'pyproject.toml' -g 'pytest.ini' -g 'manage.py' -g 'requirements*.txt'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/requirements.txt
backend/manage.py

exec
/bin/bash -lc 'rtk pytest backend/apps/attachments/tests/test_download.py backend/apps/attachments/tests/test_list.py backend/apps/approvals/tests/test_list_permissions.py -q' in /home/caohui/projects/graduation-leave-system
 exited 2 in 609ms:
Pytest: No tests collected
[full output: ~/.local/share/rtk/tee/1781149774_pytest.log]

codex
`pytest` 没有收集到这些 Django `TestCase` 测试，项目看起来走 `manage.py test`。我会改用 Django test runner 跑定向用例，避免把测试结论误报成通过。
exec
/bin/bash -lc 'rtk ls -la backend' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
.omc/
.pytest_cache/
__pycache__/
apps/
backend/
config/
data/
docs/
media/
plans/
reports/
requirements/
scripts/
utils/
venv/
.env  961B
.env.docker  314B
.env.example  761B
API接口清单.md  1.8K
Dockerfile  493B
app -> /app  4B
export_admins_for_qgl.py  1.6K
manage.py  666B
requirements.txt  398B
schema.py  739B
test_admin_apis.py  1.6K
test_admin_sso.py  2.2K
test_admin_sso_mock.py  3.2K
test_mobile_apis.py  2.1K
test_sso_e2e.py  2.8K
test_xuegong_api.py  3.0K
test_xuegong_api_full.py  4.5K
接口测试分析报告.md  7.3K

exec
/bin/bash -lc 'rtk python backend/manage.py test apps.attachments.tests.test_download apps.attachments.tests.test_list apps.approvals.tests.test_list_permissions -v 1' in /home/caohui/projects/graduation-leave-system
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

codex
`python` 命令在当前环境里不可用，我会用 `python3` 重跑同一组 Django 测试。
exec
/bin/bash -lc 'rtk python3 backend/manage.py test apps.attachments.tests.test_download apps.attachments.tests.test_list apps.approvals.tests.test_list_permissions -v 1' in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
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

codex
系统 Python 缺少 Django，仓库下有 `backend/venv`。我会用项目虚拟环境再跑一次；如果依赖或配置仍失败，会在审计结论中标明测试未能完成。
exec
/bin/bash -lc 'rtk backend/venv/bin/python backend/manage.py test apps.attachments.tests.test_download apps.attachments.tests.test_list apps.approvals.tests.test_list_permissions -v 1' in /home/caohui/projects/graduation-leave-system
 exited 1 in 623ms:
Creating test database for alias 'default'...
Found 18 test(s).
Type 'yes' if you would like to try deleting the test database 'test_graduation_leave', or 'no' to cancel: Got an error creating the test database: database "test_graduation_leave" already exists

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 103, in _execute
    return self.cursor.execute(sql)
           ~~~~~~~~~~~~~~~~~~~^^^^^
psycopg2.errors.DuplicateDatabase: database "test_graduation_leave" already exists


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/base/creation.py", line 201, in _create_test_db
    self._execute_create_test_db(cursor, test_db_params, keepdb)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/postgresql/creation.py", line 46, in _execute_create_test_db
    super()._execute_create_test_db(cursor, parameters, keepdb)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/base/creation.py", line 187, in _execute_create_test_db
    cursor.execute("CREATE DATABASE %(dbname)s %(suffix)s" % parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sql, params, many=False, executor=self._execute
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 103, in _execute
    return self.cursor.execute(sql)
           ~~~~~~~~~~~~~~~~~~~^^^^^
django.db.utils.ProgrammingError: database "test_graduation_leave" already exists


During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/manage.py", line 22, in <module>
    main()
    ~~~~^^
  File "/home/caohui/projects/graduation-leave-system/backend/manage.py", line 18, in main
    execute_from_command_line(sys.argv)
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
    utility.execute()
    ~~~~~~~~~~~~~~~^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/core/management/__init__.py", line 436, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/core/management/commands/test.py", line 24, in run_from_argv
    super().run_from_argv(argv)
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/core/management/base.py", line 412, in run_from_argv
    self.execute(*args, **cmd_options)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/core/management/base.py", line 458, in execute
    output = self.handle(*args, **options)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/core/management/commands/test.py", line 68, in handle
    failures = test_runner.run_tests(test_labels)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/test/runner.py", line 1061, in run_tests
    old_config = self.setup_databases(
        aliases=databases,
        serialized_aliases=suite.serialized_aliases,
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/test/runner.py", line 959, in setup_databases
    return _setup_databases(
        self.verbosity,
    ...<5 lines>...
        **kwargs,
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/test/utils.py", line 203, in setup_databases
    connection.creation.create_test_db(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        verbosity=verbosity,
        ^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        serialize=serialize_alias,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/base/creation.py", line 62, in create_test_db
    self._create_test_db(verbosity, autoclobber, keepdb)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/base/creation.py", line 210, in _create_test_db
    confirm = input(
        "Type 'yes' if you would like to try deleting the test "
        "database '%s', or 'no' to cancel: " % test_database_name
    )
EOFError: EOF when reading a line

codex
Django 测试发现已有测试库且命令要求交互确认，不能在当前非交互模式下删除。我会用 `--keepdb` 尝试复用现有测试库。
exec
/bin/bash -lc 'rtk backend/venv/bin/python backend/manage.py test apps.attachments.tests.test_download apps.attachments.tests.test_list apps.approvals.tests.test_list_permissions -v 1 --keepdb' in /home/caohui/projects/graduation-leave-system
 exited 1 in 9729ms:
Using existing test database for alias 'default'...
Found 18 test(s).
System check identified no issues (0 silenced).
EEEEEEEEEE.E.E.E..
======================================================================
ERROR: test_download_forbidden (apps.attachments.tests.test_download.AttachmentDownloadTestCase.test_download_forbidden)
Unauthorized student cannot download attachment
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
psycopg2.errors.UndefinedTable: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/attachments/tests/test_download.py", line 51, in setUp
    ClassMapping.objects.create(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        class_id='CS2020-01',
        ^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        active=True
        ^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 677, in create
    obj.save(force_insert=True, using=self.db)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
    ~~~~~~~~~~~~~~^
        using=using,
        ^^^^^^^^^^^^
    ...<2 lines>...
        update_fields=update_fields,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 901, in save_base
    updated = self._save_table(
        raw,
    ...<4 lines>...
        update_fields,
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1059, in _save_table
    results = self._do_insert(
        cls._base_manager, using, fields, returning_fields, raw
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1100, in _do_insert
    return manager._insert(
           ~~~~~~~~~~~~~~~^
        [self],
        ^^^^^^^
    ...<3 lines>...
        raw=raw,
        ^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 1845, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sql, params, many=False, executor=self._execute
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
django.db.utils.ProgrammingError: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


======================================================================
ERROR: test_download_positive_counselor (apps.attachments.tests.test_download.AttachmentDownloadTestCase.test_download_positive_counselor)
Assigned counselor can download attachment
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
psycopg2.errors.UndefinedTable: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/attachments/tests/test_download.py", line 51, in setUp
    ClassMapping.objects.create(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        class_id='CS2020-01',
        ^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        active=True
        ^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 677, in create
    obj.save(force_insert=True, using=self.db)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
    ~~~~~~~~~~~~~~^
        using=using,
        ^^^^^^^^^^^^
    ...<2 lines>...
        update_fields=update_fields,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 901, in save_base
    updated = self._save_table(
        raw,
    ...<4 lines>...
        update_fields,
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1059, in _save_table
    results = self._do_insert(
        cls._base_manager, using, fields, returning_fields, raw
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1100, in _do_insert
    return manager._insert(
           ~~~~~~~~~~~~~~~^
        [self],
        ^^^^^^^
    ...<3 lines>...
        raw=raw,
        ^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 1845, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sql, params, many=False, executor=self._execute
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
django.db.utils.ProgrammingError: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


======================================================================
ERROR: test_download_positive_student (apps.attachments.tests.test_download.AttachmentDownloadTestCase.test_download_positive_student)
Student can download own application attachment
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
psycopg2.errors.UndefinedTable: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/attachments/tests/test_download.py", line 51, in setUp
    ClassMapping.objects.create(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        class_id='CS2020-01',
        ^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        active=True
        ^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 677, in create
    obj.save(force_insert=True, using=self.db)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
    ~~~~~~~~~~~~~~^
        using=using,
        ^^^^^^^^^^^^
    ...<2 lines>...
        update_fields=update_fields,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 901, in save_base
    updated = self._save_table(
        raw,
    ...<4 lines>...
        update_fields,
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1059, in _save_table
    results = self._do_insert(
        cls._base_manager, using, fields, returning_fields, raw
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1100, in _do_insert
    return manager._insert(
           ~~~~~~~~~~~~~~~^
        [self],
        ^^^^^^^
    ...<3 lines>...
        raw=raw,
        ^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 1845, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sql, params, many=False, executor=self._execute
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
django.db.utils.ProgrammingError: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


======================================================================
ERROR: test_download_soft_deleted_returns_404 (apps.attachments.tests.test_download.AttachmentDownloadTestCase.test_download_soft_deleted_returns_404)
Soft-deleted attachment returns 404
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
psycopg2.errors.UndefinedTable: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/attachments/tests/test_download.py", line 51, in setUp
    ClassMapping.objects.create(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        class_id='CS2020-01',
        ^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        active=True
        ^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 677, in create
    obj.save(force_insert=True, using=self.db)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
    ~~~~~~~~~~~~~~^
        using=using,
        ^^^^^^^^^^^^
    ...<2 lines>...
        update_fields=update_fields,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 901, in save_base
    updated = self._save_table(
        raw,
    ...<4 lines>...
        update_fields,
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1059, in _save_table
    results = self._do_insert(
        cls._base_manager, using, fields, returning_fields, raw
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1100, in _do_insert
    return manager._insert(
           ~~~~~~~~~~~~~~~^
        [self],
        ^^^^^^^
    ...<3 lines>...
        raw=raw,
        ^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 1845, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sql, params, many=False, executor=self._execute
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
django.db.utils.ProgrammingError: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


======================================================================
ERROR: test_list_assigned_counselor_positive (apps.attachments.tests.test_list.AttachmentListTestCase.test_list_assigned_counselor_positive)
Assigned counselor can list application attachments
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
psycopg2.errors.UndefinedTable: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/attachments/tests/test_list.py", line 66, in setUp
    ClassMapping.objects.create(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        class_id='CS2020-01',
        ^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        active=True
        ^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 677, in create
    obj.save(force_insert=True, using=self.db)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
    ~~~~~~~~~~~~~~^
        using=using,
        ^^^^^^^^^^^^
    ...<2 lines>...
        update_fields=update_fields,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 901, in save_base
    updated = self._save_table(
        raw,
    ...<4 lines>...
        update_fields,
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1059, in _save_table
    results = self._do_insert(
        cls._base_manager, using, fields, returning_fields, raw
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1100, in _do_insert
    return manager._insert(
           ~~~~~~~~~~~~~~~^
        [self],
        ^^^^^^^
    ...<3 lines>...
        raw=raw,
        ^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 1845, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sql, params, many=False, executor=self._execute
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
django.db.utils.ProgrammingError: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


======================================================================
ERROR: test_list_cross_counselor_negative (apps.attachments.tests.test_list.AttachmentListTestCase.test_list_cross_counselor_negative)
Cross-counselor cannot list application attachments
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
psycopg2.errors.UndefinedTable: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/attachments/tests/test_list.py", line 66, in setUp
    ClassMapping.objects.create(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        class_id='CS2020-01',
        ^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        active=True
        ^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 677, in create
    obj.save(force_insert=True, using=self.db)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
    ~~~~~~~~~~~~~~^
        using=using,
        ^^^^^^^^^^^^
    ...<2 lines>...
        update_fields=update_fields,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 901, in save_base
    updated = self._save_table(
        raw,
    ...<4 lines>...
        update_fields,
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1059, in _save_table
    results = self._do_insert(
        cls._base_manager, using, fields, returning_fields, raw
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1100, in _do_insert
    return manager._insert(
           ~~~~~~~~~~~~~~~^
        [self],
        ^^^^^^^
    ...<3 lines>...
        raw=raw,
        ^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 1845, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sql, params, many=False, executor=self._execute
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
django.db.utils.ProgrammingError: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


======================================================================
ERROR: test_list_dean_archive_positive (apps.attachments.tests.test_list.AttachmentListTestCase.test_list_dean_archive_positive)
Dean can list approved application attachments for archiving
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
psycopg2.errors.UndefinedTable: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/attachments/tests/test_list.py", line 66, in setUp
    ClassMapping.objects.create(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        class_id='CS2020-01',
        ^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        active=True
        ^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 677, in create
    obj.save(force_insert=True, using=self.db)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
    ~~~~~~~~~~~~~~^
        using=using,
        ^^^^^^^^^^^^
    ...<2 lines>...
        update_fields=update_fields,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 901, in save_base
    updated = self._save_table(
        raw,
    ...<4 lines>...
        update_fields,
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1059, in _save_table
    results = self._do_insert(
        cls._base_manager, using, fields, returning_fields, raw
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1100, in _do_insert
    return manager._insert(
           ~~~~~~~~~~~~~~~^
        [self],
        ^^^^^^^
    ...<3 lines>...
        raw=raw,
        ^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 1845, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sql, params, many=False, executor=self._execute
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
django.db.utils.ProgrammingError: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


======================================================================
ERROR: test_list_excludes_soft_deleted (apps.attachments.tests.test_list.AttachmentListTestCase.test_list_excludes_soft_deleted)
List excludes soft-deleted attachments
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
psycopg2.errors.UndefinedTable: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/attachments/tests/test_list.py", line 66, in setUp
    ClassMapping.objects.create(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        class_id='CS2020-01',
        ^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        active=True
        ^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 677, in create
    obj.save(force_insert=True, using=self.db)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
    ~~~~~~~~~~~~~~^
        using=using,
        ^^^^^^^^^^^^
    ...<2 lines>...
        update_fields=update_fields,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 901, in save_base
    updated = self._save_table(
        raw,
    ...<4 lines>...
        update_fields,
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1059, in _save_table
    results = self._do_insert(
        cls._base_manager, using, fields, returning_fields, raw
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1100, in _do_insert
    return manager._insert(
           ~~~~~~~~~~~~~~~^
        [self],
        ^^^^^^^
    ...<3 lines>...
        raw=raw,
        ^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 1845, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sql, params, many=False, executor=self._execute
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
django.db.utils.ProgrammingError: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


======================================================================
ERROR: test_list_student_other_negative (apps.attachments.tests.test_list.AttachmentListTestCase.test_list_student_other_negative)
Student cannot list another student's attachments
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
psycopg2.errors.UndefinedTable: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/attachments/tests/test_list.py", line 66, in setUp
    ClassMapping.objects.create(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        class_id='CS2020-01',
        ^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        active=True
        ^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 677, in create
    obj.save(force_insert=True, using=self.db)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
    ~~~~~~~~~~~~~~^
        using=using,
        ^^^^^^^^^^^^
    ...<2 lines>...
        update_fields=update_fields,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 901, in save_base
    updated = self._save_table(
        raw,
    ...<4 lines>...
        update_fields,
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1059, in _save_table
    results = self._do_insert(
        cls._base_manager, using, fields, returning_fields, raw
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1100, in _do_insert
    return manager._insert(
           ~~~~~~~~~~~~~~~^
        [self],
        ^^^^^^^
    ...<3 lines>...
        raw=raw,
        ^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 1845, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sql, params, many=False, executor=self._execute
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
django.db.utils.ProgrammingError: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


======================================================================
ERROR: test_list_student_own_positive (apps.attachments.tests.test_list.AttachmentListTestCase.test_list_student_own_positive)
Student can list own application attachments
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
psycopg2.errors.UndefinedTable: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/attachments/tests/test_list.py", line 66, in setUp
    ClassMapping.objects.create(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        class_id='CS2020-01',
        ^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        active=True
        ^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 677, in create
    obj.save(force_insert=True, using=self.db)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
    ~~~~~~~~~~~~~~^
        using=using,
        ^^^^^^^^^^^^
    ...<2 lines>...
        update_fields=update_fields,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 901, in save_base
    updated = self._save_table(
        raw,
    ...<4 lines>...
        update_fields,
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1059, in _save_table
    results = self._do_insert(
        cls._base_manager, using, fields, returning_fields, raw
    )
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/base.py", line 1100, in _do_insert
    return manager._insert(
           ~~~~~~~~~~~~~~~^
        [self],
        ^^^^^^^
    ...<3 lines>...
        raw=raw,
        ^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/query.py", line 1845, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sql, params, many=False, executor=self._execute
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
django.db.utils.ProgrammingError: relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                    ^


======================================================================
ERROR: test_counselor_sees_only_own_pending_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_counselor_sees_only_own_pending_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/approvals/tests/test_list_permissions.py", line 82, in test_counselor_sees_only_own_pending_approvals
    self.assertEqual(response.data['results'][0]['approval_id'], 'apv_c1')
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
KeyError: 'approval_id'

======================================================================
ERROR: test_decision_all_does_not_leak_cross_approver_data (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_decision_all_does_not_leak_cross_approver_data)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/approvals/tests/test_list_permissions.py", line 161, in test_decision_all_does_not_leak_cross_approver_data
    approval_ids = [a['approval_id'] for a in response.data['results']]
                    ~^^^^^^^^^^^^^^^
KeyError: 'approval_id'

======================================================================
ERROR: test_dorm_manager_sees_only_own_pending_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_dorm_manager_sees_only_own_pending_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/apps/approvals/tests/test_list_permissions.py", line 94, in test_dorm_manager_sees_only_own_pending_approvals
    self.assertEqual(response.data['results'][0]['approval_id'], 'apv_m1')
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
KeyError: 'approval_id'

----------------------------------------------------------------------
Ran 18 tests in 8.720s

FAILED (errors=13)
Preserving test database for alias 'default'...

codex
审计结论：**需要修改后再合并**。主要风险集中在前端附件预览鉴权、类型契约未同步、错误处理对非标准响应不稳，以及附件权限边界不够明确。

**主要问题**

1. **附件预览/下载在 Web 和 React Native 端大概率无法鉴权**
   [frontend/services/attachment.ts](/home/caohui/projects/graduation-leave-system/frontend/services/attachment.ts:20) 使用 `window.open(url)`， [frontend/mobile/ApprovalDetail.tsx](/home/caohui/projects/graduation-leave-system/frontend/mobile/ApprovalDetail.tsx:28) 使用 `Linking.openURL(url)`，都不能携带 `Authorization: Bearer ...`。后端下载接口有 `IsAuthenticated`，如果系统不是 cookie 鉴权，PC/移动端预览和下载会 401。
   建议：复用 `ApiClient.getToken`，用 `fetch(url, { headers: Authorization })` 获取 `Blob` 后 `URL.createObjectURL()` 预览/下载；或后端提供短时签名 URL。不要直接裸开受保护 API URL。

2. **前端类型没有更新，当前 PC 组件会类型错误**
   [frontend/types/api.ts](/home/caohui/projects/graduation-leave-system/frontend/types/api.ts:62) 的 `ApprovalDetail` 缺少 `student_name`、`student_id`、`contact_phone`、`reason`、`leave_date`、`attachments`，也没有导出 `Attachment`，但 [frontend/components/ApprovalDetail.tsx](/home/caohui/projects/graduation-leave-system/frontend/components/ApprovalDetail.tsx:3) 已导入并使用这些字段。
   建议：补充 `Attachment` 接口，并同步 `ApprovalDetail`、`ApprovalListItem` 的真实响应结构。注意后端列表 serializer 当前返回 `id` 和嵌套 `application`，不是前端类型里的 `approval_id/application_id`。

3. **附件下载权限与审批详情权限不一致，可能扩大附件可见范围**
   审批详情只允许审批人或 dean/admin 查看：[backend/apps/approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:129)。附件下载则使用 `can_view_application`：[backend/apps/attachments/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/attachments/views.py:143)，该 helper 允许同楼栋宿管、同学院辅导员、dean/admin 查看：[backend/apps/applications/permissions.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/permissions.py:5)。
   如果业务要求“只有当前审批记录的审批人能看详情附件”，这里权限不充分。建议新增 `can_view_attachment(user, attachment)`，明确按申请所有者、当前/历史审批人、归档角色分别授权，并让附件列表、下载、审批详情三处共用同一策略。

4. **`preview=true` 会把用户上传文件以内联方式返回，需限制可预览 MIME**
   [backend/apps/attachments/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/attachments/views.py:151) 仅通过 query 参数切换 `as_attachment`。上传校验只看扩展名，`content_type` 来自客户端上传值：[backend/apps/attachments/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/attachments/views.py:86)。恶意用户可能上传伪装文件并设置危险 `Content-Type`。
   建议：预览只允许 `image/jpeg/png/gif` 和 `application/pdf`；doc/docx 保持下载或走安全预览服务；响应加 `X-Content-Type-Options: nosniff`，并尽量用服务端探测 MIME。

5. **错误处理优化会丢失结构化错误，并且非 JSON/网络错误边界不足**
   [frontend/services/api.ts](/home/caohui/projects/graduation-leave-system/frontend/services/api.ts:90) 在检查 `response.ok` 前直接 `response.json()`，遇到空响应、HTML 网关错误、502 页面会抛 `SyntaxError`。`extractErrorMessage` 也假设 `data.error.details[field][0]` 一定是字符串：[frontend/services/api.ts](/home/caohui/projects/graduation-leave-system/frontend/services/api.ts:45)。另外原本抛出的 `ApiError` 被改成普通 `Error`：[frontend/services/api.ts](/home/caohui/projects/graduation-leave-system/frontend/services/api.ts:93)，调用方拿不到 `code/status/details`。
   建议：实现 `ApiClientError extends Error`，保留 `status/code/details/raw`；JSON parse 失败时降级为“服务异常”；网络错误、超时用 `AbortController` 和统一中文消息处理。

6. **新增 `attachments` 字段会影响 `ApplicationSerializer` 的响应体和查询量**
   [backend/apps/applications/serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/serializers.py:30) 复用了 `ApprovalSerializer`，而该 serializer 现在会为每个 approval 查询同一个 application 的附件：[backend/apps/approvals/serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/serializers.py:48)。这会让申请详情中的 `approvals[]` 也带附件列表，形成重复 payload 和 N+1。
   建议：拆分 `ApprovalDetailSerializer` 和 `ApprovalInApplicationSerializer`，只在审批详情接口返回附件；或在 view 层 `prefetch_related('application__attachments')` 并避免重复序列化。

7. **小程序实现把 `wx.request` 当 Promise 用，运行时不可靠**
   [frontend/miniprogram/pages/approval-detail/index.js](/home/caohui/projects/graduation-leave-system/frontend/miniprogram/pages/approval-detail/index.js:18) `await wx.request(...)` 在原生小程序 API 下不会按预期返回响应对象，除非项目已有 promisify 包装。`wx.downloadFile` 也没有检查 `statusCode`，403/404 仍可能走 success：[frontend/miniprogram/pages/approval-detail/index.js](/home/caohui/projects/graduation-leave-system/frontend/miniprogram/pages/approval-detail/index.js:39)。
   建议：封装 `request()`/`downloadFile()` Promise 工具，统一检查 `statusCode` 和错误体；文件类型不要从临时路径判断，优先使用附件的 `content_type/file_name`。

8. **代码复用没有真正覆盖多端**
   Web 有 `AttachmentService/useAttachment`，但 React Native 仍手写 URL 拼接：[frontend/mobile/ApprovalDetail.tsx](/home/caohui/projects/graduation-leave-system/frontend/mobile/ApprovalDetail.tsx:28)，小程序也单独拼接 URL。当前复用只覆盖 PC。
   建议：抽出纯函数 `buildAttachmentPreviewUrl/buildAttachmentDownloadUrl` 和平台适配层：Web 用 Blob URL，RN 用带 header 的下载/文件预览库，小程序用 `wx.downloadFile`。

**API 兼容性判断**

`leave_date` 和 `attachments` 作为只读新增响应字段，对宽松 JSON 客户端通常是向后兼容的。但如果已有客户端做精确 schema 校验，或依赖 `ApprovalSerializer` 在申请详情里不包含附件，则可能出现兼容问题。建议更新 OpenAPI/前端类型，并补充契约测试。

**验证情况**

我尝试运行定向 Django 测试。`pytest` 未收集到测试；用 `backend/venv/bin/python backend/manage.py test ... --keepdb` 运行后失败，原因包括现有测试库缺少 `class_mappings` 表，以及审批列表测试仍期望 `approval_id` 但 serializer 返回 `id`。因此本次审计没有拿到通过的自动化测试结果。
tokens used
152,718

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
