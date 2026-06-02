# 网站UI分析及响应式方案

## 1. 提取完整配色方案

根据对 https://xuegong.hgnu.edu.cn/ （及样式表 `/_upload/tpl/00/10/16/template16/style.css`） 的分析，该网站视觉风格偏传统和正式，主要通过深红（Burgundy / Crimson）或红棕色系作为强调色，搭配暖灰色或米黄色背景，带有一种庄重、学术的氛围。

主要提取到的色值及分配：

- **主色调 (Primary)**：`#971010` (深红/绛红) - 用于主要标题、高亮强调
- **辅助色 (Secondary/Accent)**：`#B56D18` (土黄/金棕) - 用于副标题、辅助强调；`#d99749` / `#f0cd82` (暖金) - 导航悬停
- **背景色 (Backgrounds)**：
  - 页面背景：`#f2f2f2` (浅灰)
  - 卡片/区块背景：`#FFFFFF` (纯白), `#f7f3eb` (米黄底色)
  - 边框/分割线：`#e4e4e4`, `#dbdbdb`, `#edd9bd` (暖灰/暖米)
- **文本色 (Text)**：
  - 正文：`#333333`, `#535353` (深灰)
  - 辅助文本/副标题：`#6d6d6d`, `#787878`, `#999999` (中灰)
- **状态色 (Status)**：（基于常规正式UI补充，因为源网站未明确定义这些具体系统状态）
  - 待处理 (Pending)：`#d99749` (警告/橙色系)
  - 成功 (Success)：`#2a7337` (沉稳的绿色)
  - 错误 (Error)：`#971010` (主色兼做错误/拒绝色)

### CSS变量定义

```css
:root {
  /* 主色调 (深红/庄重) */
  --primary-color: #971010;
  --primary-hover: #781710;
  
  /* 辅助色 (金棕/暖黄) */
  --secondary-color: #B56D18;
  --accent-color: #d99749;
  
  /* 背景色 */
  --bg-primary: #f2f2f2;
  --bg-secondary: #f7f3eb;
  --card-bg: #FFFFFF;
  
  /* 边框及分割线 */
  --border-color: #e4e4e4;
  --border-accent: #edd9bd;
  
  /* 文本色 */
  --text-primary: #333333;
  --text-secondary: #535353;
  --text-tertiary: #787878;
  
  /* 状态色 */
  --status-pending: #d99749;
  --status-success: #2a7337;
  --status-error: #971010;
}
```

**整体风格评估：** 正式、学术、传统、稳重。

---

## 2. 响应式设计建议（PC + 移动端）

### 断点策略 (Breakpoints)
建议采用移动优先 (Mobile First) 策略：

```css
/* 默认：移动端 (<768px) */

/* 平板端 (Tablet) */
@media (min-width: 768px) {
  /* 调整卡片间距，适度放开宽度限制 */
}

/* 桌面端 (Desktop) */
@media (min-width: 1024px) {
  /* 实施多列布局，侧边栏或宽屏导航 */
}
```

### 布局调整方案

1. **整体容器**：
   - 移动端：`width: 100%; max-width: 100%;`
   - 桌面端：`max-width: 1004px` 或 `1200px`，并居中对齐 `margin: 0 auto;`。这是为了与参考网站风格保持一致。

2. **Tab导航**：
   - 移动端：底部 Fixed 导航或顶部横向可滑动 Tab。
   - 桌面端：改为侧边菜单 (Sidebar) 或顶部宽版导航栏 (Header Navigation)。

3. **卡片列表**：
   - 移动端：单列流式布局 (`flex-direction: column`)。
   - 桌面端：使用 CSS Grid 变为 2-3 列。`grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));`

4. **表单 (如离校申请表单)**：
   - 移动端：占满宽度。
   - 桌面端：限制最大宽度 (例如 `max-width: 600px; margin: 0 auto;`)，避免输入框过长导致视线移动疲劳。标签可由顶部对齐改为左侧对齐。

5. **详情页**：
   - 移动端：上下单列排列（基本信息 -> 附件 -> 审批记录）。
   - 桌面端：双列布局（左侧占 60-70% 展示基本信息与附件；右侧占 30-40% 侧边栏展示审批时间轴/操作区）。

---

## 3. 附件上传UI设计

在申请表单 (`student-application`) 提交前增加附件上传功能。考虑到目前已在 `detail` 页面实现了上传 (`wx.chooseMessageFile`) 和附件展示，我们需要将其提取复用到申请页面。

### 移动端UI方案 (小程序)
- **交互流程**：
  1. 用户在表单下方看到“附件材料（可选）”区块。
  2. 点击一个带有 `+` 号的虚线框按钮（或“上传附件”按钮）。
  3. 触发 `wx.chooseMessageFile` (针对微信生态最佳，支持选择各类文档和图片)。
  4. 选定后，前端校验大小 (<10MB) 和格式。
  5. **预览与存储**：由于需要在申请提交时一起关联，建议先将文件暂存在小程序的 `data.tempFiles` 数组中。
  6. **UI展示**：文件以列表项 (List Item) 形式展示，包含文件名、大小和一个“删除”小图标。
  7. **提交**：当用户点击“提交申请”时，先调用创建申请的 API 拿到 `application_id`，紧接着并发调用 `/api/attachments/upload/` 上传这些临时文件。显示统一的“提交中” loading 状态。

### PC端UI方案 (Web)
- **交互流程**：
  1. 提供一个拖拽区域 (Drag-and-Drop zone)，内部包含 `<input type="file" multiple accept=".jpg,.png,.pdf,.doc,.docx">`。
  2. **视觉提示**：区域内显示“点击或拖拽文件到此处上传，单文件不超过10MB”。
  3. **文件列表**：同移动端，采用卡片或列表项展示已选文件，附带删除按钮。
  4. 拖入或选择文件后触发 JS `File` 对象的校验。
  5. 随表单一起提交（可以使用 `FormData` 将表单字段与文件打包一次性 POST 给后端，或者同移动端分步进行）。

### 附件列表展示方式
推荐采用紧凑的 List 项：
```html
<div class="attachment-item">
  <span class="icon">📎</span>
  <div class="file-info">
    <div class="file-name">图书馆还书证明.pdf</div>
    <div class="file-size">1.2 MB</div>
  </div>
  <button class="btn-delete" aria-label="删除">×</button>
</div>
```

### 上传进度和状态反馈
- 在用户点击最终“提交申请”时，如果涉及附件上传：
  - 按钮文案变为“正在提交数据和附件 (0/2)...”
  - 提供全局 Toast 或 Loading 遮罩。
  - 成功后跳转详情页。
  - 若表单创建成功但附件上传失败，应跳转详情页并 Toast 提示“申请已提交，但部分附件上传失败，请在详情页重试”。