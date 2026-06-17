# 技术设计：草稿流程附件上传

## 架构边界

**修改范围：** 仅前端（demo-web/）
**不修改：** 后端（已有API满足需求）

## 数据流

```
用户操作          前端API调用                     后端API                状态变化
────────         ─────────────                   ─────────              ──────────
点击提交     →   apiGetOrCreateDraft()      →   POST /applications/draft/     draft created
                 返回: {application_id: "app_xxx"}                             
                 
             →   apiUploadAttachment(id, file1) → POST /applications/{id}/attachments/  file1 saved
             →   apiUploadAttachment(id, file2) → POST /applications/{id}/attachments/  file2 saved
             
             →   apiSubmitApplication(...)      → POST /applications/              draft → pending_dorm_manager
                                                     (后端转化草稿: views.py:196-207)
```

## API契约

### 1. 创建草稿

**前端调用：**
```javascript
POST /api/applications/draft/
Headers: Authorization: Bearer <token>
Body: (empty)
```

**后端返回：**
```json
{
  "application_id": "app_xxx",
  "status": "draft",
  "student_id": "...",
  "created_at": "..."
}
```

**后端实现：** `backend/apps/applications/views.py:286-311`

### 2. 上传附件

**前端调用：**
```javascript
POST /api/applications/{application_id}/attachments/
Headers: Authorization: Bearer <token>
Content-Type: multipart/form-data
Body: 
  - file: <File object>
  - attachment_type: "other"
```

**后端返回：**
```json
{
  "attachment_id": "att_xxx",
  "file_name": "...",
  "file_size": 1234,
  "content_type": "image/jpeg"
}
```

**后端实现：** `backend/apps/attachments/views.py:56-91`

**权限校验：** 仅student + owner可上传（views.py:67-69）

### 3. 提交申请

**前端调用：**
```javascript
POST /api/applications/
Headers: Authorization: Bearer <token>
Content-Type: multipart/form-data
Body:
  - contact_phone: "..."
  - reason: "..."
  - leave_date: "YYYY-MM-DD"
  // 不再发送 attachments
```

**后端行为：**
- 检测已有草稿（views.py:197）
- 更新草稿字段，状态改为 `pending_dorm_manager`（views.py:201-206）
- 附件通过 `application_id` 外键自动关联，无需额外处理

## 前端实现设计

### 修改文件

1. **demo-web/js/api.js** - 新增/修改API函数
2. **demo-web/index.html** - 修改提交逻辑和UI反馈

### API函数设计

#### 新增：apiGetOrCreateDraft()

```javascript
async function apiGetOrCreateDraft() {
    const response = await fetch(API_BASE_URL + '/applications/draft/', {
        method: 'POST',
        headers: getAuthHeaders()
    });
    if (response.ok) {
        return await response.json();
    }
    throw new Error('创建草稿失败');
}
```

#### 修改：apiSubmitApplication()

**移除files参数：**
```javascript
// 原签名：
async function apiSubmitApplication(phone, reason, leaveDate, files)

// 新签名：
async function apiSubmitApplication(phone, reason, leaveDate)
```

**移除附件处理：**
```javascript
// 删除这行：
files.forEach(f => formData.append('attachments', f));
```

#### 验证：apiUploadAttachment()

已存在（api.js:240-263），签名：
```javascript
async function apiUploadAttachment(applicationId, file, attachmentType = 'other')
```

**需确认：** 返回值处理正确

### 提交流程重构

**文件：** `demo-web/index.html` 行1179附近

**原流程：**
```javascript
const result = await apiSubmitApplication(phone, reason, leaveDate, uploadedFiles);
```

**新流程：**
```javascript
// 步骤1: 创建草稿
btn.textContent = '创建草稿中...';
const draft = await apiGetOrCreateDraft();

// 步骤2: 上传附件
if (uploadedFiles.length > 0) {
    for (let i = 0; i < uploadedFiles.length; i++) {
        btn.textContent = `上传附件 ${i+1}/${uploadedFiles.length}...`;
        await apiUploadAttachment(draft.application_id, uploadedFiles[i]);
    }
}

// 步骤3: 提交申请
btn.textContent = '提交申请中...';
const result = await apiSubmitApplication(phone, reason, leaveDate);
```

### 错误处理

**原则：** fail-fast，保留已完成操作

```javascript
try {
    const draft = await apiGetOrCreateDraft();
} catch (e) {
    showToast('创建草稿失败: ' + e.message, 'error');
    return; // 停止，不继续
}

try {
    for (...) {
        await apiUploadAttachment(...);
    }
} catch (e) {
    showToast('附件上传失败: ' + e.message + '。草稿已保存，请重试', 'error');
    return; // 停止，草稿和已上传附件保留
}

try {
    const result = await apiSubmitApplication(...);
} catch (e) {
    showToast('提交失败: ' + e.message + '。附件已上传，请重试', 'error');
    return; // 停止
}
```

### UI状态管理

**按钮状态：**
```javascript
btn.disabled = true;
btn.textContent = '创建草稿中...';  // 步骤1
btn.textContent = '上传附件 1/3...'; // 步骤2
btn.textContent = '提交申请中...';   // 步骤3
```

**成功后：**
```javascript
// 清空表单
document.getElementById('contactPhone').value = '';
document.getElementById('applicationReason').value = '';
document.getElementById('leaveDate').value = '';
uploadedFiles = [];
renderFileList();

// 切换界面
showScreen(1);
loadMyApplications();
```

## 兼容性考虑

### 后端兼容

**草稿转申请逻辑（views.py:196-207）：**
```python
draft = Application.objects.select_for_update().filter(
    student=user, status=ApplicationStatus.DRAFT
).first()

if draft:
    draft.contact_phone = serializer.validated_data['contact_phone']
    draft.reason = serializer.validated_data.get('reason', '')
    draft.leave_date = serializer.validated_data['leave_date']
    draft.status = ApplicationStatus.PENDING_DORM_MANAGER
    draft.save()
    application = draft
```

**附件保留机制：**
- `Attachment` 通过 `application_id` 外键关联
- 草稿ID不变，转为正式申请后附件自动关联
- 无需额外迁移附件

### 边界情况

**1. 无附件提交：**
```javascript
if (uploadedFiles.length > 0) {
    // 上传附件
}
// 跳过，直接提交
```

**2. 已有草稿：**
- `apiGetOrCreateDraft()` 返回已有草稿（后端逻辑：views.py:297-300）
- 新上传附件追加到草稿
- 提交时覆盖草稿字段

**3. 重复提交：**
- 后端检测已有 `pending/approved` 申请（views.py:156-163）
- 返回 409 错误
- 前端显示："已有待审批或已通过的申请"

## 数据一致性

**草稿附件关系：**
```
Application (draft)
  ├─ application_id: app_xxx
  └─ status: draft

Attachment
  ├─ attachment_id: att_yyy
  ├─ application_id: app_xxx (FK)
  └─ is_deleted: false

草稿提交后：
Application
  └─ status: pending_dorm_manager

Attachment (不变)
  └─ application_id: app_xxx (FK仍有效)
```

**无需数据迁移：** FK自动关联

## 性能考虑

**顺序上传 vs 并发上传：**
- 当前设计：顺序上传（简单，UI反馈清晰）
- 并发上传：复杂度高，进度反馈困难
- 附件通常1-3个，顺序上传可接受

**网络超时：**
- 前端已有超时配置（api.js:8-26，默认8秒）
- 附件上传可能超时，建议增加到30秒：
  ```javascript
  await fetchWithTimeout(url, options, 30000); // 30秒
  ```

## 测试策略

### 单元测试（手动）

1. **正常流程：** 表单+2附件 → 检查数据库
2. **无附件：** 表单 → 提交成功
3. **中断恢复：** 上传1附件 → 刷新页面 → 继续上传 → 提交

### API测试

使用curl验证后端：
```bash
# 1. 创建草稿
TOKEN="..."
curl -X POST http://localhost:7787/api/applications/draft/ \
  -H "Authorization: Bearer $TOKEN"

# 2. 上传附件
APP_ID="app_xxx"
curl -X POST http://localhost:7787/api/applications/$APP_ID/attachments/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.jpg" \
  -F "attachment_type=other"

# 3. 提交申请
curl -X POST http://localhost:7787/api/applications/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "contact_phone=13800138000" \
  -F "reason=test" \
  -F "leave_date=2026-07-01"
```

## 回滚计划

**触发条件：**
- 前端功能严重错误
- 后端API不兼容

**回滚步骤：**
```bash
git reset --hard 2c30429
git push -f origin main
```

**数据清理（可选）：**
```sql
-- 删除未提交草稿
DELETE FROM applications_application WHERE status = 'draft';

-- 删除孤儿附件
DELETE FROM attachments_attachment 
WHERE application_id NOT IN (SELECT application_id FROM applications_application);
```

## 后续优化方向

**不在本次实施范围：**
- 草稿自动保存（表单onChange实时保存）
- 大文件分片上传
- 附件缩略图预览
- 草稿管理界面
- 定时清理旧草稿
