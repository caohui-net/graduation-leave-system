# 修复附件上传问题-实施草稿流程

## Goal

修复前端提交申请时附件丢失问题，实施草稿流程：创建草稿 → 上传附件 → 提交申请。

## Problem

**当前状况：**
- 前端发送附件到 `/applications/` 但后端 `ApplicationCreateSerializer` 不处理
- 结果：附件全部丢失，用户以为上传成功

**根本原因：** 前端一次性提交（申请+附件），后端设计为两步（先创建申请，再上传附件）

## Requirements

### 功能需求

1. **草稿流程：** 提交申请前先创建草稿
2. **附件上传：** 逐个上传附件到草稿，显示进度
3. **申请提交：** 草稿转正式申请，附件保留
4. **错误处理：** 任何步骤失败时，保留草稿和已上传附件，用户可重试

### 前端修改

**文件：** `demo-web/index.html` + `demo-web/js/api.js`

**修改点：**
1. 新增 `apiGetOrCreateDraft()` 函数
2. 修改 `apiSubmitApplication()`，移除 `files` 参数
3. 重构 `submitApplication()` 流程：
   - 步骤1: 创建草稿
   - 步骤2: 循环上传附件
   - 步骤3: 提交申请
4. UI反馈：显示"创建草稿中..."、"上传附件 (1/3)..."

### 后端验证

**验证已有API可用：**
- `POST /api/applications/draft/` - 创建草稿
- `POST /api/applications/{id}/attachments/` - 上传附件到草稿
- `POST /api/applications/` - 提交草稿转正式申请（views.py:196-207）

## Acceptance Criteria

### 功能验收

- [ ] 创建草稿成功，返回 `application_id`
- [ ] 上传3个附件到草稿，每个独立上传
- [ ] 提交草稿转正式申请，状态变为 `PENDING_DORM_MANAGER`
- [ ] 查询数据库/API，附件全部保留未丢失
- [ ] 无附件提交：跳过上传步骤，直接提交成功

### UI验收

- [ ] 提交按钮禁用时显示当前步骤（"创建草稿中..."/"上传附件 1/3"/"提交申请中..."）
- [ ] 附件上传失败时显示错误信息，停止后续步骤
- [ ] 整个流程失败时，草稿保留，用户可刷新页面重试

### 回归验收

- [ ] 辅导员/学工部查看申请时，附件列表正常显示
- [ ] 附件下载功能正常
- [ ] 重复提交时后端返回 409 错误

## Constraints

- 附件大小限制：10MB（前端已实现）
- 允许类型：`.jpg, .jpeg, .png, .pdf, .doc, .docx`（前端已实现）
- 草稿权限：仅学生本人可创建和上传附件
- 草稿转申请：后端自动处理，前端只需调用创建申请API

## Risks & Mitigation

**风险1：** 草稿堆积（用户创建但未提交）  
**缓解：** 后续任务 - 定时清理7天未提交草稿

**风险2：** 单个附件上传失败影响整体流程  
**缓解：** 失败时停止，保留草稿和已上传附件，用户可重试

**回滚：** 快照commit `2c30429`
```bash
git reset --hard 2c30429
```

## Test Plan

### 手动测试

1. **正常流程：** 填表单 + 2附件 → 提交 → 验证附件存在
2. **无附件：** 填表单 → 提交 → 成功
3. **重复提交：** 提交后再提交 → 409错误

### 数据库验证

```sql
-- 查看草稿
SELECT * FROM applications_application WHERE status = 'draft';

-- 查看附件
SELECT * FROM attachments_attachment WHERE application_id = '<draft_id>';
```

## References

- 后端草稿API：`backend/apps/applications/views.py:286-311`
- 后端附件API：`backend/apps/attachments/views.py:56-91`
- 前端提交：`demo-web/index.html:1179`
- 前端API：`demo-web/js/api.js:127-157, 240-263`
