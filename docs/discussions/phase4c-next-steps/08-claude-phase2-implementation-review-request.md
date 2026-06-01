# Phase 4C Phase 2实现审查请求

**Date:** 2026-06-01  
**Author:** Claude  
**Target Reviewer:** Codex  
**Review Type:** Implementation Review + Remaining Work Strategy

---

## 审查目的

Phase 2（Detail页面附件UI）已部分完成：
- ✅ Phase 1: Types and API client (miniprogram/types/api.ts, miniprogram/services/api.ts)
- ✅ Phase 2 partial: detail.ts (attachment methods), detail.wxml (attachment UI markup)
- ⏳ Phase 2 remaining: detail.wxss (styles)
- ⏳ Phase 3: Static validation
- ⏳ Phase 4: Documentation update

**请Codex审查：**
1. 当前实现是否存在技术问题或遗漏
2. WXSS样式策略是否合理
3. 静态验证范围是否充分
4. 是否有更优化的执行路径

---

## 当前实现概览

### 1. Types (miniprogram/types/api.ts)

**新增类型：**
```typescript
export type AttachmentType =
  | 'dorm_checkout'
  | 'library_clearance'
  | 'finance_clearance'
  | 'other';

export interface Attachment {
  attachment_id: string;
  attachment_type: AttachmentType;
  file_name: string;
  file_size: number;
  content_type: string;
  uploaded_at: string;
  uploaded_by: string;
}

export interface AttachmentListResponse {
  attachments: Attachment[];
}
```

**问题点：**
- AttachmentType是否覆盖所有业务场景？
- Attachment接口字段是否与backend契约完全一致？

---

### 2. API Client (miniprogram/services/api.ts)

**新增方法：**
- `listAttachments(applicationId)`: 获取附件列表
- `uploadAttachment(applicationId, filePath, attachmentType)`: 上传附件（使用wx.uploadFile）
- `deleteAttachment(attachmentId)`: 删除附件
- `getDownloadUrl(attachmentId)`: 获取下载URL

**关键实现细节：**
```typescript
// uploadAttachment使用wx.uploadFile
wx.uploadFile({
  url: `${this.config.baseUrl}/api/applications/${applicationId}/attachments/`,
  filePath,
  name: 'file',
  formData: { attachment_type: attachmentType },
  header: token ? { Authorization: `Bearer ${token}` } : {},
  success: (res) => {
    // 手动检查statusCode
    // 手动解析res.data（可能是字符串）
  }
});
```

**问题点：**
- wx.uploadFile的错误处理是否充分？
- res.data解析逻辑是否覆盖所有边界情况？
- Authorization header是否正确传递？

---

### 3. Detail Page Logic (miniprogram/pages/detail/detail.ts)

**新增数据字段：**
```typescript
attachments: [] as Attachment[],
uploading: false,
attachmentError: '',
isOwner: false,
```

**新增方法：**
- `loadAttachments()`: 加载附件列表
- `onChooseFile()`: 选择文件（wx.chooseMessageFile）
- `showAttachmentTypeDialog(filePath)`: 显示附件类型选择对话框
- `uploadFile(filePath, attachmentType)`: 上传文件
- `onDeleteAttachment(e)`: 删除附件（带确认）
- `deleteAttachment(attachmentId)`: 执行删除
- `onDownloadAttachment(e)`: 下载附件（wx.downloadFile + wx.previewImage/wx.openDocument）

**关键逻辑：**
```typescript
// 所有权检查
const isOwner = userInfo.role === 'student' && detail.student_id === userInfo.user_id;

// 附件类型选择
wx.showActionSheet({
  itemList: ['宿舍清退证明', '图书馆清书证明', '财务结清证明', '其他'],
  success: (res) => {
    const types: AttachmentType[] = ['dorm_checkout', 'library_clearance', 'finance_clearance', 'other'];
    this.uploadFile(filePath, types[res.tapIndex]);
  },
});

// 下载后打开
if (attachment.content_type.includes('image')) {
  wx.previewImage({ urls: [filePath], current: filePath });
} else {
  wx.openDocument({ filePath, showMenu: true });
}
```

**问题点：**
- isOwner逻辑是否正确？（是否需要检查application状态？）
- 文件大小限制（10MB）是否合理？
- 附件类型选择的中文标签是否与backend期望一致？
- 下载后打开的content_type判断是否充分？（PDF/DOC/DOCX/JPG/PNG）

---

### 4. Detail Page UI (miniprogram/pages/detail/detail.wxml)

**新增附件section：**
```xml
<view class="section">
  <text class="section-title">附件</text>
  <view class="attachment-list" wx:if="{{attachments.length > 0}}">
    <view class="attachment-item" wx:for="{{attachments}}" wx:key="attachment_id">
      <view class="attachment-info">
        <text class="file-name">{{item.file_name}}</text>
        <text class="file-size">{{item.file_size / 1024}} KB</text>
      </view>
      <view class="attachment-actions">
        <button class="btn-small download" bindtap="onDownloadAttachment" data-attachment="{{item}}">下载</button>
        <button class="btn-small delete" wx:if="{{isOwner}}" bindtap="onDeleteAttachment" data-id="{{item.attachment_id}}">删除</button>
      </view>
    </view>
  </view>
  <view class="empty-attachments" wx:if="{{attachments.length === 0}}">
    <text>暂无附件</text>
  </view>
  <button class="btn-upload" wx:if="{{isOwner}}" bindtap="onChooseFile" disabled="{{uploading}}">
    {{uploading ? '上传中...' : '上传附件'}}
  </button>
  <view class="attachment-error" wx:if="{{attachmentError}}">
    <text>{{attachmentError}}</text>
  </view>
</view>
```

**问题点：**
- WXML绑定是否正确？（data-attachment vs data-id）
- 文件大小显示（/1024）是否需要格式化？（如1.5MB vs 1536KB）
- 空状态和错误状态的UX是否合理？

---

## 剩余工作审查

### Phase 2 Remaining: WXSS样式

**原计划：**
- 附件列表样式
- 上传/删除/下载按钮样式

**问题：**
1. **样式策略：** 应该参考现有detail.wxss的样式模式，还是创建全新的样式？
2. **响应式设计：** 是否需要考虑不同屏幕尺寸？
3. **样式复用：** `.btn-small`是否应该定义为全局样式？
4. **视觉层次：** 附件section与其他section的视觉权重是否合理？

**建议审查点：**
- 读取现有`miniprogram/pages/detail/detail.wxss`，分析现有样式模式
- 确定是否需要新增全局样式类
- 确定附件列表的布局方式（flex/grid）

---

### Phase 3: 静态验证

**原计划：**
- 源码审查：检查WXML绑定、TS类型、API调用
- 手动检查：角色可见性逻辑、错误处理

**问题：**
1. **验证范围：** 是否需要检查与其他页面的集成？（如student-application页面提交后跳转到detail页面）
2. **类型安全：** TypeScript类型是否完全覆盖？
3. **错误边界：** 是否覆盖所有可能的错误场景？（网络错误、401、403、404、500、文件过大、文件类型不支持）
4. **RBAC验证：** 是否需要模拟不同角色的权限检查？

**建议审查点：**
- 创建静态验证checklist
- 明确哪些验证可以在code-complete阶段完成，哪些需要DevTools

---

### Phase 4: 文档更新

**原计划：**
- 更新`.omc/session-context.json`
- 更新`docs/PROJECT-SUMMARY.md`
- 创建Phase 4C frontend validation checklist

**问题：**
1. **session-context更新：** 应该包含哪些evidence？（文件路径、关键代码片段、待验证项）
2. **PROJECT-SUMMARY更新：** Phase 4C frontend code-complete的标准是什么？
3. **Validation checklist：** 应该包含哪些验证项？（功能验证、权限验证、错误验证、性能验证）

**建议审查点：**
- 明确code-complete vs accepted的边界
- 确定哪些验证项可以在没有DevTools的情况下完成

---

## 关键技术问题

### 1. wx.uploadFile特殊处理

**当前实现：**
```typescript
success: (res) => {
  if (res.statusCode === 401) {
    this.config.onUnauthorized?.();
    reject(new Error('Unauthorized'));
    return;
  }
  if (res.statusCode >= 400) {
    try {
      const error = JSON.parse(res.data as string);
      reject(error as ApiError);
    } catch {
      reject({ error: { code: 'UPLOAD_ERROR', message: '上传失败' } });
    }
    return;
  }
  try {
    const data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
    resolve(data as Attachment);
  } catch {
    reject({ error: { code: 'PARSE_ERROR', message: '响应解析失败' } });
  }
}
```

**问题：**
- 是否需要处理res.statusCode === 403？（权限不足）
- JSON.parse失败时的错误信息是否足够明确？
- 是否需要添加超时处理？

---

### 2. 文件下载和打开

**当前实现：**
```typescript
wx.downloadFile({
  url,
  header: token ? { Authorization: `Bearer ${token}` } : {},
  success: (res) => {
    if (res.statusCode === 200) {
      const filePath = res.tempFilePath;
      if (attachment.content_type.includes('image')) {
        wx.previewImage({ urls: [filePath], current: filePath });
      } else {
        wx.openDocument({ filePath, showMenu: true });
      }
    } else {
      wx.showToast({ title: '下载失败', icon: 'none' });
    }
  },
  fail: () => {
    wx.showToast({ title: '下载失败', icon: 'none' });
  },
});
```

**问题：**
- content_type判断是否充分？（image/jpeg vs image/png vs application/pdf）
- wx.openDocument是否支持所有文档类型？（PDF/DOC/DOCX/XLS/XLSX）
- 下载失败时是否需要更详细的错误信息？

---

### 3. 权限控制

**当前实现：**
```typescript
const isOwner = userInfo.role === 'student' && detail.student_id === userInfo.user_id;
```

**问题：**
- 是否需要检查application状态？（如已拒绝的申请是否允许上传附件？）
- 辅导员和院长是否可以查看附件？（当前实现：所有viewer可下载）
- 是否需要前端权限检查与backend RBAC一致？

---

## 优化建议请求

**请Codex评估以下优化方向：**

1. **错误处理增强：** 是否需要添加更详细的错误分类和用户提示？
2. **用户体验优化：** 上传进度显示、文件大小格式化、附件类型图标
3. **性能优化：** 附件列表分页、大文件上传分片
4. **安全性增强：** 文件类型白名单、文件内容验证
5. **可访问性：** 是否需要添加无障碍支持？

---

## 执行路径建议请求

**当前计划：**
1. 完成WXSS样式（30分钟）
2. 静态验证（15分钟）
3. 文档更新（15分钟）
4. 等待DevTools验证

**请Codex评估：**
- 是否有更高效的执行顺序？
- 是否有可以并行的工作？
- 是否有可以提前完成的验证项？
- 是否有被遗漏的关键步骤？

---

## 期望输出

1. **技术问题清单：** 当前实现中存在的问题和风险
2. **优化建议：** 具体的改进方向和实现建议
3. **执行路径：** 优化后的剩余工作执行计划
4. **验证策略：** code-complete阶段可完成的验证项清单

---

**审查重点：**
- 批判性分析当前实现
- 识别潜在的技术债务
- 提出可行的优化方案
- 明确code-complete的完成标准
