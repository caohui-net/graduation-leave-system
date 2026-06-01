# Phase 4C P1修复方案 - Claude审查请求

**日期：** 2026-06-01  
**请求人：** Claude  
**审查对象：** P1问题修复方案  
**前置：** P0修复已完成并验证（6/6测试通过）

---

## 审查目标

验证P1修复方案的完整性和正确性，确保：
1. 字段漂移修复不引入新问题
2. 错误处理覆盖所有关键路径
3. 状态码处理符合微信小程序最佳实践
4. 文件类型预检逻辑合理

---

## P1问题清单（来自Codex审查）

### P1-1: 字段漂移
**问题：** `miniprogram/types/api.ts` 的 `Attachment` 接口包含 `uploaded_by` 字段，但：
- 当前UI不使用该字段
- 后端模型不存在 `description` 字段
- 添加无用字段增加维护成本

**修复方案：**
```typescript
// miniprogram/types/api.ts
export interface Attachment {
  attachment_id: string;
  attachment_type: AttachmentType;
  file_name: string;
  file_size: number;
  content_type: string;
  uploaded_at: string;
  // 移除: uploaded_by: string;
}
```

**问题：** 这个修复是否会影响其他地方？需要检查：
- `miniprogram/services/api.ts` 是否使用 `uploaded_by`
- `miniprogram/pages/detail/detail.ts` 是否使用 `uploaded_by`
- 后端序列化器是否返回 `uploaded_by`

---

### P1-2: `loadAttachments()` 静默吞错
**问题：** 当前实现只打印 `console.error`，不设置错误状态，用户无法感知加载失败。

**修复方案：**
```typescript
// miniprogram/pages/detail/detail.ts
async loadAttachments() {
  try {
    const attachments = await apiClient.listAttachments(this.data.applicationId);
    this.setData({ attachments, attachmentError: '' });
  } catch (err: any) {
    console.error('加载附件失败:', err);
    const errorMsg = formatApiError(err) || '附件加载失败';
    this.setData({ attachmentError: errorMsg });
  }
}
```

**问题：**
1. `formatApiError` 函数是否已存在？如果不存在，需要实现还是直接用简单字符串？
2. `attachmentError` 字段是否已在 `data` 中定义？
3. WXML是否已有显示 `attachmentError` 的逻辑？

**WXML修复方案：**
```xml
<!-- miniprogram/pages/detail/detail.wxml -->
<!-- 区分空状态和错误状态 -->
<view wx:if="{{attachmentError}}" class="error-message">{{attachmentError}}</view>
<view wx:elif="{{attachments.length === 0}}" class="empty-message">暂无附件</view>
<view wx:else>
  <!-- 附件列表 -->
</view>
```

---

### P1-3: 下载状态码处理不足
**问题：** 当前 `onDownloadAttachment` 只处理 `statusCode === 200`，不处理 401/403/404。

**修复方案：**
```typescript
// miniprogram/pages/detail/detail.ts
onDownloadAttachment(e: any) {
  const attachment = e.currentTarget.dataset.attachment as Attachment;
  const url = apiClient.getDownloadUrl(attachment.attachment_id);
  const token = app.globalData.token;

  wx.downloadFile({
    url,
    header: token ? { Authorization: `Bearer ${token}` } : {},
    success: (res) => {
      if (res.statusCode === 401) {
        // 清token并重新登录
        wx.removeStorageSync('token');
        wx.removeStorageSync('userInfo');
        app.globalData.token = '';
        app.globalData.userInfo = null;
        wx.reLaunch({ url: '/pages/login/login' });
        return;
      }
      if (res.statusCode === 403) {
        wx.showToast({ title: '无权限下载附件', icon: 'none' });
        return;
      }
      if (res.statusCode === 404) {
        wx.showToast({ title: '附件不存在或已删除', icon: 'none' });
        return;
      }
      if (res.statusCode === 200) {
        const filePath = res.tempFilePath;
        if (attachment.content_type.startsWith('image/')) {
          wx.previewImage({ 
            urls: [filePath], 
            current: filePath,
            fail: () => wx.showToast({ title: '预览失败', icon: 'none' })
          });
        } else {
          wx.openDocument({ 
            filePath, 
            showMenu: true,
            fail: () => wx.showToast({ title: '打开失败', icon: 'none' })
          });
        }
      } else {
        wx.showToast({ title: '下载失败', icon: 'none' });
      }
    },
    fail: () => {
      wx.showToast({ title: '下载失败', icon: 'none' });
    },
  });
}
```

**问题：**
1. 401处理是否应该在全局拦截器中处理，而不是每个下载方法中重复？
2. `app.globalData` 的清理逻辑是否完整？是否需要清理其他状态？
3. `wx.previewImage` 和 `wx.openDocument` 的 `fail` 回调是否需要更详细的错误信息？

---

### P1-4: 文件类型预检
**问题：** 当前 `onChooseFile` 只检查文件大小，不检查文件类型，可能导致上传不支持的文件类型后后端拒绝。

**修复方案：**
```typescript
// miniprogram/pages/detail/detail.ts
onChooseFile() {
  wx.chooseMessageFile({
    count: 1,
    type: 'file',
    success: (res) => {
      const file = res.tempFiles[0];
      
      // 文件大小检查
      if (file.size > 10 * 1024 * 1024) {
        wx.showToast({ title: '文件大小不能超过10MB', icon: 'none' });
        return;
      }
      
      // 文件类型预检
      const fileName = file.name.toLowerCase();
      const allowedExts = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx'];
      if (!allowedExts.some(ext => fileName.endsWith(ext))) {
        wx.showToast({ 
          title: '不支持的文件类型，仅支持图片、PDF、Word文档', 
          icon: 'none',
          duration: 2000
        });
        return;
      }
      
      this.showAttachmentTypeDialog(file.path);
    },
  });
}
```

**问题：**
1. 允许的文件扩展名列表是否与后端验证逻辑一致？需要检查后端代码。
2. 是否需要检查 MIME type 而不是文件扩展名？扩展名可以伪造。
3. 10MB 限制是否与后端配置一致？

---

## 关键审查点

### 1. 后端一致性检查
**需要验证：**
- 后端序列化器返回哪些字段？是否包含 `uploaded_by`？
- 后端文件类型验证逻辑是什么？
- 后端文件大小限制是多少？

**文件位置：**
- `backend/apps/attachments/serializers.py`
- `backend/apps/attachments/views.py` (upload_attachment)

### 2. 错误处理一致性
**需要验证：**
- 是否有全局错误处理机制？
- `formatApiError` 函数是否存在？
- 其他页面如何处理类似错误？

**文件位置：**
- `miniprogram/services/api.ts`
- `miniprogram/utils/` (如果有工具函数)

### 3. 状态管理完整性
**需要验证：**
- `attachmentError` 字段是否已在 `data` 中定义？
- 是否需要在其他生命周期方法中重置 `attachmentError`？
- 是否需要在上传/删除成功后重新加载附件列表？

---

## 期望Codex审查输出

1. **后端一致性验证结果**
   - 序列化器字段列表
   - 文件类型/大小验证逻辑
   - 是否存在字段不一致

2. **错误处理改进建议**
   - 是否需要全局拦截器
   - `formatApiError` 实现建议
   - 错误状态管理最佳实践

3. **状态码处理完整性**
   - 401处理是否应该全局化
   - 是否遗漏其他重要状态码
   - 微信小程序下载API最佳实践

4. **文件类型预检优化**
   - 扩展名 vs MIME type
   - 前后端验证逻辑对齐
   - 用户体验优化建议

5. **遗漏问题识别**
   - 是否有其他P1级别问题未发现
   - 修复方案是否引入新风险
   - 是否需要额外的测试覆盖

---

## 审查范围

**包含文件：**
- `miniprogram/types/api.ts`
- `miniprogram/pages/detail/detail.ts`
- `miniprogram/pages/detail/detail.wxml`
- `backend/apps/attachments/serializers.py`
- `backend/apps/attachments/views.py`
- `docs/api/contract-v0.3.md`

**不包含：**
- WXSS样式（P2问题，后续处理）
- 其他页面的附件功能
- 后端测试代码（P0已验证）

---

## 成功标准

修复方案通过审查需满足：
1. 前后端字段完全一致
2. 错误处理覆盖所有关键路径
3. 状态码处理符合微信小程序规范
4. 文件类型预检与后端验证对齐
5. 不引入新的P0/P1级别问题
6. 代码可读性和可维护性良好

---

**请Codex审查以上P1修复方案，重点关注前后端一致性、错误处理完整性、状态码处理正确性。**
