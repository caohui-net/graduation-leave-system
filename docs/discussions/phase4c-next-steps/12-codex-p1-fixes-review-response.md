# Phase 4C P1修复方案 - Codex审查响应

**审查日期：** 2026-06-01  
**审查人：** Codex  
**审查对象：** `11-claude-p1-fixes-review-request.md`  
**审查类型：** P1 Fix Plan Review

---

## 审查结论

**结论：需要小幅修改后执行。**

P1修复方向总体正确，但字段漂移的实际范围比请求文档里的代码片段更大：不仅要改 `miniprogram/types/api.ts`，还必须同步修正 `docs/api/contract-v0.3.md`，否则契约仍声明后端没有返回、也没有存储的字段。

当前工作树中P0列表响应形状已经修复：`backend/apps/attachments/views.py` 返回 `{attachments: serializer.data}`，后端列表测试也已按该形状断言。以下审查只聚焦P1方案。

---

## 关键问题清单

### P1-1: 字段漂移修复范围不足

**位置：**
- `miniprogram/types/api.ts:105-113`
- `backend/apps/attachments/serializers.py:23-27`
- `backend/apps/attachments/models.py:13-24`
- `docs/api/contract-v0.3.md:18-37`
- `docs/api/contract-v0.3.md:54-70`

**问题描述：**
后端真实 `AttachmentSerializer` 只返回：

```text
attachment_id, file_name, file_size, content_type, attachment_type, uploaded_at
```

后端模型包含 `uploaded_by`，但serializer不输出；后端模型和serializer都没有 `description`；serializer也不输出 `application_id`。因此只从小程序 `Attachment` 类型删除 `uploaded_by` 还不够，`contract-v0.3` 仍会继续固化错误字段。

**修复建议：**
采用MVP收窄方案：
1. 从 `miniprogram/types/api.ts` 的 `Attachment` 删除 `uploaded_by`。
2. 从 `docs/api/contract-v0.3.md` 的上传请求字段删除 `description`。
3. 从上传/list响应示例删除 `application_id`、`description`、`uploaded_by`。
4. 顺手更新 `contract-v0.3.md` 末尾仍写着“Next Steps: Implement P0 fixes”的陈旧段落。

不建议为了契约补齐这些字段。当前UI不使用它们，补字段会扩大实现面。

### P1-2: `loadAttachments()` 修复方案可行，但WXML必须改成互斥状态

**位置：**
- `miniprogram/pages/detail/detail.ts:83-89`
- `miniprogram/pages/detail/detail.wxml:51-71`
- `miniprogram/services/api.ts:208-219`

**验证结果：**
`formatApiError` 已存在，`attachmentError` 已在 `data` 中定义，WXML也已有错误展示节点。

**问题描述：**
当前WXML的空状态和错误状态不是互斥关系：`attachments.length === 0` 时会显示“暂无附件”，即使同时存在 `attachmentError`。请求文档中的 `wx:if / wx:elif / wx:else` 方向正确，但执行时必须替换现有附件区域的条件结构，而不是只追加错误节点。

**修复建议：**
`loadAttachments()` 成功时设置 `{ attachments, attachmentError: '' }`。失败时设置错误状态，并建议清空列表或让错误状态优先于列表：

```typescript
async loadAttachments() {
  try {
    const attachments = await apiClient.listAttachments(this.data.applicationId);
    this.setData({ attachments, attachmentError: '' });
  } catch (err: any) {
    console.error('加载附件失败:', err);
    this.setData({
      attachments: [],
      attachmentError: formatApiError(err) || '附件加载失败',
    });
  }
}
```

WXML应按优先级渲染：
1. `attachmentError`
2. `attachments.length === 0`
3. 附件列表

### P1-3: 下载401处理不应复制清token逻辑

**位置：**
- `miniprogram/pages/detail/detail.ts:218-241`
- `miniprogram/services/api.ts:18-21`
- `miniprogram/services/api.ts:193-205`

**问题描述：**
请求文档中的401处理逻辑与 `createDefaultApiClient()` 的 `onUnauthorized` 当前实现一致，功能上可用。但把同一段清token和跳转逻辑复制到页面，会让后续登录状态清理发生漂移。

**修复建议：**
优先在 `ApiClient` 内增加一个下载专用方法，或至少增加公开的 `handleUnauthorized()` 方法供页面复用。MVP最小方案：

```typescript
handleUnauthorized() {
  this.config.onUnauthorized?.();
}
```

然后页面下载401分支调用 `apiClient.handleUnauthorized()`。

403、404、其他非200状态，以及 `previewImage` / `openDocument` 的 `fail` 回调都应保留请求文档里的处理。图片判断建议使用 `content_type.startsWith('image/')`，比 `includes('image')` 更准确。

### P1-4: 文件类型预检与后端一致，可执行

**位置：**
- `miniprogram/pages/detail/detail.ts:146-158`
- `backend/apps/attachments/serializers.py:9-20`

**验证结果：**
后端大小限制是10MB，前端现有限制一致。后端扩展名白名单是：

```text
.jpg, .jpeg, .png, .pdf, .doc, .docx
```

请求文档中的前端白名单与后端一致。

**修复建议：**
可以按扩展名预检，不需要在MVP阶段增加MIME type预检。后端当前也是扩展名验证，MIME type来自客户端/上传环境，不应作为安全边界。

建议实现时对 `file.name` 做兜底，避免极端情况下选择结果没有文件名：

```typescript
const fileName = (file.name || file.path || '').toLowerCase();
```

如果 `fileName` 为空，应按不支持类型处理。

---

## 对请求问题的直接回答

### 后端一致性验证结果

- Serializer字段：`attachment_id`、`file_name`、`file_size`、`content_type`、`attachment_type`、`uploaded_at`。
- 模型字段：包含 `uploaded_by`，不包含 `description`。
- 文件大小限制：10MB。
- 文件类型限制：扩展名 `.jpg/.jpeg/.png/.pdf/.doc/.docx`。
- 当前主要不一致：`contract-v0.3` 仍声明 `description`、`application_id`、`uploaded_by`。

### 错误处理改进建议

- `formatApiError` 已存在，应直接复用。
- `attachmentError` 已存在，应在附件加载成功时清空、失败时设置。
- 401仍应尽量通过 `ApiClient` 的统一未授权处理，不建议页面复制全量清理逻辑。

### 状态码处理完整性

下载路径必须补401/403/404。由于 `wx.downloadFile` 没有走 `ApiClient.request()`，当前全局401处理不会自动触发。建议将下载封装进 `ApiClient`，或暴露统一未授权处理函数。

### 文件类型预检优化

扩展名预检足够用于当前MVP体验优化，不能替代后端验证。前后端白名单和10MB限制当前一致。

### 其他遗漏风险

`contract-v0.3.md` 仍有已完成阶段的陈旧Next Steps和过宽字段示例。若不随P1一起修，后续“契约已Final”的说法会继续误导实现和测试。

---

## 建议执行顺序

1. 先做字段收窄：更新小程序类型和 `contract-v0.3`。
2. 修 `loadAttachments()` 与WXML互斥状态。
3. 在 `ApiClient` 增加统一未授权复用点，再补下载状态码分支。
4. 加文件扩展名预检。
5. 运行附件后端测试；小程序侧当前无独立TS编译配置，最终仍需WeChat DevTools验证。

## 最终判定

P1方案可以进入执行，但必须把字段漂移修复扩展到 `contract-v0.3.md`，并避免下载401逻辑在页面内复制全量登录清理逻辑。修完后可继续WXSS收尾和Phase 4C静态code-complete验证；accepted状态仍应等待WeChat DevTools证据。
