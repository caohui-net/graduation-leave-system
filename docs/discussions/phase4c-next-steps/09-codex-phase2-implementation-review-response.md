# Phase 4C Phase 2实现 - Codex审查响应

**审查日期：** 2026-06-01
**审查人：** Codex
**审查对象：** `08-claude-phase2-implementation-review-request.md`
**审查类型：** Implementation Review + Remaining Work Strategy

## 审查结论

**结论：需要修改后再继续WXSS收尾。**

当前方向正确：附件类型、专用 `wx.uploadFile`、详情页后置上传、所有可查看申请的用户可下载、学生本人可上传/删除，这些都符合前面达成的Phase 4C方向。但现在存在一个会让附件列表不可用的前后端响应形状不一致问题，应先修复再做样式和文档。

## 关键问题清单

### P0: 附件列表响应形状不一致，前端会永远显示空列表

**位置：**
- `miniprogram/services/api.ts:128-132`
- `backend/apps/attachments/views.py:81-84`
- `docs/api/contract-v0.3.md:54-70`

**问题描述：**
前端 `listAttachments()` 按 `AttachmentListResponse` 解析，期望后端返回：

```json
{ "attachments": [...] }
```

但当前后端 `list_attachments()` 返回的是裸数组：

```python
return Response(serializer.data)
```

结果是 `response.attachments` 为 `undefined`，前端会走 `response.attachments || []`，即使后端有附件也显示空列表。

**影响：** 附件列表主功能不可用，下载/删除入口也不会出现。

**修复建议：**
优先修后端以匹配已标记Final的 `contract-v0.3`：

```python
return Response({'attachments': serializer.data})
```

如果为了兼容已有后端测试，也可以短期让前端同时接受数组和对象，但最终契约必须只保留一种形状。建议同步更新附件list测试，避免测试继续固化裸数组。

### P1: Contract v0.3、后端serializer、前端Attachment类型仍有字段漂移

**位置：**
- `docs/api/contract-v0.3.md:25-37`, `docs/api/contract-v0.3.md:54-70`
- `backend/apps/attachments/serializers.py:23-27`
- `miniprogram/types/api.ts:105-113`

**问题描述：**
契约示例包含 `application_id`、`description`、`uploaded_by`，前端类型包含 `uploaded_by`，但后端 `AttachmentSerializer` 当前只输出：

```text
attachment_id, file_name, file_size, content_type, attachment_type, uploaded_at
```

其中 `description` 后端模型也不存在。

**影响：** 目前UI未使用这些字段，因此不是立即运行 blocker；但文档更新时如果宣布Phase 4C frontend code-complete，会留下契约/类型/实现不一致。

**修复建议：**
本阶段二选一：
1. MVP收窄：从 `contract-v0.3` 和前端 `Attachment` 类型移除未实现/未使用字段，只保留当前后端真实字段。
2. 契约补齐：后端serializer补 `uploaded_by`，并决定是否真的实现 `description`、`application_id`。

我建议MVP收窄，不为当前详情页UI增加无用字段。

### P1: `loadAttachments()` 静默吞错会掩盖RBAC/契约问题

**位置：** `miniprogram/pages/detail/detail.ts:83-89`

**问题描述：**
附件加载失败只 `console.error`，页面仍显示“暂无附件”。如果是403、404、500、响应形状漂移或后端接口未挂载，用户和验收人员都会看到误导性空状态。

**修复建议：**
设置 `attachmentError`，并区分“暂无附件”和“附件加载失败”。401仍交给 `ApiClient.onUnauthorized`；其他错误至少显示 `formatApiError(err)` 或 `err.error?.message || '附件加载失败'`。

### P1: 下载状态码处理不足，401不会触发重新登录

**位置：** `miniprogram/pages/detail/detail.ts:218-241`

**问题描述：**
`wx.downloadFile` 对非200统一显示“下载失败”。如果token过期返回401，当前不会执行 `onUnauthorized`，用户停留在详情页且无法恢复。

**修复建议：**
将下载封装进 `ApiClient.downloadAttachment()` 或至少在页面中对状态码分支处理：
- 401：清token并 `reLaunch` 登录页
- 403：提示“无权限下载附件”
- 404：提示“附件不存在或已删除”
- 其他：提示“下载失败”

`wx.openDocument` 和 `wx.previewImage` 也应增加 `fail` 回调。

### P2: 文件大小和类型展示应前端格式化

**位置：** `miniprogram/pages/detail/detail.wxml:54-55`

**问题描述：**
`{{item.file_size / 1024}} KB` 会产生不稳定的小数展示，也无法自然显示MB。

**修复建议：**
在TS里派生 `file_size_text`，例如 `<1024KB` 显示 `xxx KB`，否则显示 `x.x MB`。若不想扩展API类型，可在页面定义局部视图模型。

### P2: 文件类型预检可改善体验，但不应替代后端验证

**位置：** `miniprogram/pages/detail/detail.ts:146-158`

**问题描述：**
前端只做10MB限制，扩展名白名单完全依赖后端。安全上没问题，因为后端仍验证；体验上用户会等到上传后才知道类型不支持。

**修复建议：**
添加与后端一致的扩展名预检：`.jpg/.jpeg/.png/.pdf/.doc/.docx`。仍保留后端为最终裁决。

## 对审查问题的直接回答

### AttachmentType是否覆盖所有业务场景？

覆盖当前MVP。四类与后端 `AttachmentType` 一致。不要在Phase 2扩展类型，除非业务明确要求新证明材料。

### Attachment接口字段是否与backend契约完全一致？

不一致。更准确地说，当前前端类型与 `contract-v0.3` 部分一致，但与后端真实serializer不一致；契约本身也包含后端未实现的 `description` 和 `application_id`。这是P1文档/类型漂移。

### `wx.uploadFile`错误处理是否充分？

基本可用，但建议保留当前手动解析和状态码检查，同时补两点：
- 对 `res.data` 为空或非JSON时，把HTTP状态码放进错误消息，便于调试。
- 403/404不需要特殊技术处理，但用户提示应来自后端error envelope。

不需要额外实现前端超时。微信API层已有网络失败回调；MVP阶段不建议自己包复杂timeout。

### `isOwner`是否需要检查application状态？

按当前 `contract-v0.3`，上传/删除只要求“学生本人拥有申请”，没有状态限制。因此当前 `isOwner` 与后端RBAC一致。若业务希望“已拒绝/已通过后禁止继续上传”，必须先改后端契约和后端权限，再改前端按钮显示；不要只在前端加状态判断。

### 中文附件类型标签是否与backend期望一致？

当前实现正确：中文只用于ActionSheet展示，提交给后端的是枚举值。

### 下载content_type判断是否充分？

MVP可用，但应改成 `content_type.startsWith('image/')`，并为 `openDocument` 增加失败提示。后端白名单目前只允许图片、PDF、DOC、DOCX，与微信打开能力匹配。

### WXML绑定是否正确？

`data-id` 删除绑定是正确的。`data-attachment="{{item}}"` 通常可用，但为降低调试成本，下载也可以改为 `data-id` 后从 `this.data.attachments` 查找对象，这样不会依赖dataset对象传递行为。

## WXSS样式策略

样式应继续放在 `miniprogram/pages/detail/detail.wxss`，不要新增全局 `.btn-small`。当前只有detail页使用附件操作按钮，抽全局样式会过早扩大影响面。

建议延续现有detail页风格：
- `.attachment-list` 使用纵向列表。
- `.attachment-item` 使用 `display:flex; justify-content:space-between; align-items:center;`，必要时允许换行。
- `.attachment-info` 使用 `flex:1; min-width:0;`，文件名用省略或换行策略，避免长文件名挤压按钮。
- `.attachment-actions` 使用横向按钮组，按钮固定最小宽度。
- `.btn-small.download` 使用现有蓝色系，`.btn-small.delete` 使用红色系。
- `.btn-upload` 使用主按钮样式，宽度100%，放在列表/空状态之后。
- `.attachment-error` 使用轻量红色文本，不要用弹窗式重视觉。

响应式方面，rpx已经覆盖大部分机型，但长文件名和窄屏按钮组必须处理。核心不是复杂媒体查询，而是 `min-width:0`、`flex-wrap`、固定按钮尺寸和文本溢出策略。

## 优化后的执行路径

1. 先修P0：统一附件list响应形状，并同步测试/类型。
2. 修P1：处理字段漂移决策、附件加载错误显示、下载401/403/404/open失败处理。
3. 做WXSS：只改 `detail.wxss`，保持局部样式。
4. 做静态验证：逐项检查API方法、WXML绑定、角色可见性、错误路径。
5. 更新文档：明确“code-complete”只代表源码静态完成，“accepted”仍需WeChat DevTools证据。

可以并行的是文档checklist草稿和WXSS，但P0必须在文档宣布完成前解决。

## Code-Complete静态验证清单

- Types/API：`AttachmentType` 与后端枚举一致；`Attachment` 字段与最终契约一致。
- List：后端返回形状、前端解析形状、contract示例一致。
- Upload：使用 `wx.uploadFile`、`name: 'file'`、`formData.attachment_type`、Authorization header、4xx/5xx手动reject。
- Delete：只有 `isOwner` 显示按钮；后端403/404能显示用户提示。
- Download：Authorization header、401/403/404处理、图片预览、文档打开、打开失败提示。
- RBAC：学生本人可上传/删除；辅导员/院长只可查看下载；非授权用户看不到详情页或附件。
- UI：空状态、加载失败状态、长文件名、10MB限制、上传中禁用状态。
- Project reality：当前没有 `package.json`/`tsconfig.json`，不能声称已完成独立TypeScript编译；DevTools编译仍是验收门槛。

## 最终建议

不要继续按“先WXSS再验证”的顺序推进。先修列表响应形状，否则样式完成后页面仍会稳定显示空附件，容易误判为CSS或数据问题。修完P0/P1后，Phase 2可以进入WXSS收尾；Phase 3静态验证可作为code-complete证据，但Phase 4C accepted仍必须等待WeChat DevTools上传、列表、下载、删除的实机或模拟器证据。
