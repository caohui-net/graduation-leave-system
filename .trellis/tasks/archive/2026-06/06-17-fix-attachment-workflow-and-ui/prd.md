# 修复附件流程bug并完善附件功能

## Goal

修复草稿流程导致的附件丢失bug，并完善附件显示功能（列表状态、详情预览），支持PC/移动端。

## Problem

**当前问题：**
1. **附件丢失bug：** 用户提交后附件显示"无附件"
2. **根本原因：** 草稿ID未传递给提交API，后端查找草稿逻辑有缺陷
3. **功能缺失：** 
   - 列表无附件状态/数量显示
   - 详情无附件预览功能
   - 管理员无法查看附件

## Root Cause Analysis

### Bug分析：草稿ID未关联到最终申请

**前端流程：**
```javascript
// 步骤1: 创建草稿
const draft = await apiGetOrCreateDraft(); // draftId = app_A

// 步骤2: 上传附件到 app_A
await apiUploadAttachment(draft.application_id, file);

// 步骤3: 提交申请（未传递draftId）
await apiSubmitApplication(phone, reason, leaveDate); // ← 缺失draftId
```

**后端逻辑缺陷（views.py:196-207）：**
```python
# 查找任意draft状态草稿
draft = Application.objects.filter(student=user, status=ApplicationStatus.DRAFT).first()

if draft:
    # 转化草稿
    draft.status = ApplicationStatus.PENDING_DORM_MANAGER
    application = draft
else:
    # 创建新申请（附件留在旧草稿）
    application = Application.objects.create(...)
```

**问题场景：**
1. 用户首次提交：草稿A（draft）→ 上传附件 → 提交成功，草稿A转pending
2. 用户再次尝试：创建草稿B（因为A已不是draft）→ 提交时找到B或创建新申请C
3. **结果：** 附件留在A，但用户看到的申请是C（无附件）

## Requirements

### R1: 修复草稿ID传递

**前端修改：**
- `apiSubmitApplication(phone, reason, leaveDate, draftId)` - 新增draftId参数
- FormData添加 `application_id` 字段

**后端修改：**
- 接收 `application_id` 参数（可选）
- 优先使用传入的ID查找草稿，回退到自动查找

### R2: 列表显示附件状态

**位置：** 申请列表（学生、宿管、辅导员、学工部）

**显示内容：**
- 附件图标：有附件显示 📎
- 附件数量：`(2个附件)`

**实现：**
- API已返回 `has_attachments` 字段
- 前端渲染时显示图标和数量

### R3: 详情页附件预览

**位置：** 申请详情页（学生、管理员）

**显示内容：**
- 附件列表：文件名、大小、上传时间
- 点击文件名：新窗口预览（图片/PDF）或下载
- 支持多个附件

**实现：**
- API：`GET /applications/{id}/attachments/` 已存在
- 前端：已有附件显示逻辑（line 446-454），需优化UI

### R4: 审批页附件预览

**位置：** 审批详情页（宿管、辅导员、学工部）

**显示内容：** 同R3

**实现：** 审批详情页复用申请详情附件逻辑

### R5: PC/移动端同步

**要求：** 所有附件功能在PC和移动端表现一致

## Acceptance Criteria

### 功能验收

- [ ] **Bug修复：** 提交申请后，附件正确保存并显示
- [ ] **列表显示：** 有附件的申请显示📎图标和数量
- [ ] **详情预览：** 点击附件文件名可预览/下载
- [ ] **管理员查看：** 宿管/辅导员/学工部可查看申请附件
- [ ] **多附件支持：** 支持上传和显示多个附件

### UI验收

- [ ] 列表图标清晰可见（📎 2个附件）
- [ ] 详情页附件列表美观（文件名、大小、操作按钮）
- [ ] 预览功能正常（图片/PDF新窗口打开）
- [ ] 移动端适配（触摸友好、响应式布局）

### 回归验收

- [ ] 无附件提交：列表显示正常（无图标）
- [ ] 删除附件：列表实时更新
- [ ] 权限校验：仅相关人员可查看附件

## Test Scenarios

### 场景1：正常提交（有附件）

1. 学生登录（2021140140429）
2. 填写表单 + 上传2个附件（1.jpg, 2.pdf）
3. 提交成功
4. **验证：**
   - 申请列表显示 📎 2个附件
   - 点击申请，详情页显示2个附件
   - 点击文件名，可预览/下载

### 场景2：管理员查看附件

1. 辅导员登录
2. 查看待审批列表
3. 点击有附件的申请
4. **验证：**
   - 详情页显示附件列表
   - 可预览/下载附件
   - 审批后附件仍可查看

### 场景3：多次提交（边界）

1. 学生提交申请A + 2附件
2. 申请A被驳回
3. 学生重新提交申请B + 1附件
4. **验证：**
   - 申请A显示2个附件
   - 申请B显示1个附件
   - 附件不会混淆

## Constraints

- 附件大小限制：10MB（前端已实现）
- 允许类型：`.jpg, .jpeg, .png, .pdf, .doc, .docx`
- 预览支持：图片、PDF（浏览器原生支持）
- 其他文件：直接下载

## Risks & Dependencies

**风险1：** 修改后端API可能影响现有功能  
**缓解：** 向后兼容，`application_id` 参数可选

**风险2：** 附件预览浏览器兼容性  
**缓解：** 使用浏览器原生预览，不支持则下载

**依赖：** 后端附件API已实现（上传、查询、下载）

## References

- 上次修复：commit `3d83628` - 草稿流程实现
- 后端附件API：`backend/apps/attachments/views.py`
- 前端附件显示：`demo-web/index.html:446-454`
- Bug截图：用户手工测试显示"无附件"
