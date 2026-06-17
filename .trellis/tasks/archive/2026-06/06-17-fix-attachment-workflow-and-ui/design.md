# 技术设计：附件流程修复与UI完善

## 架构边界

**修改范围：**
- 后端：`applications/views.py` - 接收草稿ID参数
- 前端：`demo-web/js/api.js` + `demo-web/index.html` - 传递草稿ID，完善附件UI

**不修改：** 附件上传/下载/删除API（已正常工作）

## 数据流修复

### 当前流程（有bug）

```
前端                                后端
────────                            ──────
创建草稿 ────────────────────────→  返回 draftId=A
上传附件(A) ─────────────────────→  附件保存到A
提交申请(无ID) ──────────────────→  查找任意draft草稿 ← Bug!
                                    找到草稿B或创建新申请C
                                    附件留在A，申请是C ✗
```

### 修复后流程

```
前端                                后端
────────                            ──────
创建草稿 ────────────────────────→  返回 draftId=A
上传附件(A) ─────────────────────→  附件保存到A
提交申请(A) ─────────────────────→  精确查找草稿A
                                    转化草稿A为正式申请
                                    附件保留在A ✓
```

## API契约修改

### 修改：提交申请API

**前端调用：**
```javascript
// 新增application_id参数
POST /api/applications/
Content-Type: multipart/form-data
Body:
  - contact_phone: "..."
  - reason: "..."
  - leave_date: "YYYY-MM-DD"
  - application_id: "app_xxx"  ← 新增（可选）
```

**后端处理逻辑：**
```python
# views.py create_application()
application_id = request.data.get('application_id')  # 可选参数

if application_id:
    # 优先：精确查找指定草稿
    draft = Application.objects.filter(
        student=user,
        application_id=application_id,
        status=ApplicationStatus.DRAFT
    ).first()
else:
    # 回退：自动查找任意草稿（保持向后兼容）
    draft = Application.objects.filter(
        student=user,
        status=ApplicationStatus.DRAFT
    ).first()

if draft:
    # 转化草稿
    draft.contact_phone = ...
    draft.status = ApplicationStatus.PENDING_DORM_MANAGER
    draft.save()
    application = draft
else:
    # 创建新申请
    application = Application.objects.create(...)
```

**向后兼容：** `application_id` 可选，不传则使用旧逻辑

## 前端实现设计

### 修改1：apiSubmitApplication 传递草稿ID

**文件：** `demo-web/js/api.js`

**修改：**
```javascript
// 原签名
async function apiSubmitApplication(phone, reason, leaveDate)

// 新签名
async function apiSubmitApplication(phone, reason, leaveDate, applicationId)

// 实现
async function apiSubmitApplication(phone, reason, leaveDate, applicationId) {
    const formData = new FormData();
    formData.append('contact_phone', phone);
    formData.append('reason', reason);
    formData.append('leave_date', leaveDate);
    if (applicationId) {
        formData.append('application_id', applicationId);  // ← 新增
    }
    // ... fetch ...
}
```

### 修改2：提交流程传递草稿ID

**文件：** `demo-web/index.html`

**修改：**
```javascript
// 步骤3: 提交申请
btn.textContent = '提交申请中...';
const result = await apiSubmitApplication(phone, reason, leaveDate, draftId);  // ← 传递draftId
```

### 修改3：列表显示附件状态

**文件：** `demo-web/index.html` 行288附近

**当前代码：**
```javascript
const attachmentIcon = app.has_attachments ? '📎' : '';
```

**修改为：**
```javascript
let attachmentInfo = '';
if (app.has_attachments) {
    const count = app.approvals?.reduce((sum, apv) => sum, 0) || '';  // 暂时显示图标
    attachmentInfo = `<span style="color: #1890ff;">📎</span>`;
}
```

**优化方案：** API返回附件数量字段

**后端修改：** `ApplicationListSerializer` 添加 `attachment_count` 字段

```python
class ApplicationListSerializer(serializers.ModelSerializer):
    attachment_count = serializers.SerializerMethodField()
    
    def get_attachment_count(self, obj):
        return obj.attachments.filter(is_deleted=False).count()
```

**前端显示：**
```javascript
if (app.has_attachments) {
    const count = app.attachment_count || 0;
    attachmentInfo = `<span style="color: #1890ff;">📎 ${count}个附件</span>`;
}
```

### 修改4：详情页附件UI优化

**文件：** `demo-web/index.html` 行446-454

**当前代码：**
```javascript
let attachmentsHtml = '...附件...</div>';
if (attachments && attachments.length > 0) {
    attachments.forEach(att => {
        attachmentsHtml += '<div>...a href...</div>';
    });
} else {
    attachmentsHtml += '<div style="color: #999;">无附件</div>';
}
```

**优化为：**
```javascript
let attachmentsHtml = `
<div class="card">
  <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">
    附件 ${attachments.length > 0 ? `(${attachments.length}个)` : ''}
  </div>
`;

if (attachments && attachments.length > 0) {
    attachments.forEach(att => {
        const sizeKB = (att.file_size / 1024).toFixed(1);
        attachmentsHtml += `
        <div style="display: flex; align-items: center; padding: 8px; border: 1px solid #f0f0f0; border-radius: 4px; margin-bottom: 8px;">
          <span style="font-size: 20px; margin-right: 10px;">📄</span>
          <div style="flex: 1;">
            <div style="font-weight: 500;">${att.file_name}</div>
            <div style="font-size: 12px; color: #999;">${sizeKB} KB</div>
          </div>
          <button onclick="previewAttachment('${att.attachment_id}')" 
                  style="padding: 4px 12px; background: #1890ff; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 8px;">
            预览
          </button>
          <button onclick="downloadAttachment('${att.attachment_id}')" 
                  style="padding: 4px 12px; background: #52c41a; color: white; border: none; border-radius: 4px; cursor: pointer;">
            下载
          </button>
        </div>
        `;
    });
} else {
    attachmentsHtml += '<div style="color: #999; padding: 20px; text-align: center;">暂无附件</div>';
}
attachmentsHtml += '</div>';
```

**新增函数：**
```javascript
function previewAttachment(attachmentId) {
    const url = API_BASE_URL + '/applications/' + currentAppId + '/attachments/' + attachmentId + '/download/?preview=true';
    window.open(url, '_blank');
}

function downloadAttachment(attachmentId) {
    const url = API_BASE_URL + '/applications/' + currentAppId + '/attachments/' + attachmentId + '/download/';
    window.open(url, '_blank');
}
```

**注意：** 需要存储 `currentAppId` 全局变量

### 修改5：审批详情页附件显示

**文件：** `demo-web/index.html` 行627附近

**当前：** 已有附件查询逻辑

**确保：** 审批详情页复用相同的附件渲染逻辑

## 移动端适配

**响应式CSS：**
```css
@media (max-width: 768px) {
  .attachment-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .attachment-item button {
    width: 100%;
    margin-top: 8px;
  }
}
```

**触摸优化：**
- 按钮最小尺寸：44x44px
- 点击区域充足
- 预览/下载合并为一个操作

## 数据一致性

**草稿转申请：**
```
Application (draft)
  ├─ application_id: app_A
  └─ status: draft

Attachment (关联到app_A)
  └─ application_id: app_A (FK)

提交后：
Application
  ├─ application_id: app_A (不变)
  └─ status: pending_dorm_manager

Attachment (不变)
  └─ application_id: app_A (FK仍有效)
```

**无需数据迁移**

## 错误处理

**前端：**
```javascript
// 步骤3: 提交申请
const result = await apiSubmitApplication(phone, reason, leaveDate, draftId);

if (!result.success) {
    // 检查是否因为草稿不存在
    if (result.error?.code === 'NOT_FOUND') {
        showToast('草稿已过期，请刷新页面重试', 'error');
    } else {
        showToast('提交失败：' + result.error.message, 'error');
    }
    return;
}
```

**后端：**
```python
if application_id:
    draft = Application.objects.filter(...).first()
    if not draft:
        return Response({
            'error': {'code': 'NOT_FOUND', 'message': '草稿不存在或已提交'}
        }, status=404)
```

## 性能考虑

**附件数量查询优化：**
```python
# 使用annotate避免N+1查询
from django.db.models import Count

queryset = Application.objects.annotate(
    attachment_count=Count('attachments', filter=Q(attachments__is_deleted=False))
)
```

**列表查询优化：**
```python
queryset = queryset.select_related('student').prefetch_related(
    'approvals__approver',
    'attachments'  # 预加载附件
)
```

## 测试策略

### 单元测试（后端）

```python
def test_submit_with_draft_id():
    # 创建草稿
    draft = Application.objects.create(status='draft', ...)
    
    # 上传附件
    Attachment.objects.create(application=draft, ...)
    
    # 提交申请（带draft_id）
    response = client.post('/api/applications/', {
        'contact_phone': '...',
        'application_id': draft.application_id
    })
    
    # 验证
    assert response.status_code == 201
    draft.refresh_from_db()
    assert draft.status == 'pending_dorm_manager'
    assert draft.attachments.count() == 1
```

### 集成测试（前端）

**测试脚本：** 复用 `/tmp/test_attachment_upload.py`

**修改：** 验证提交后附件仍存在

```python
# 步骤4: 提交申请（传递draftId）
form_data = {
    'contact_phone': '...',
    'application_id': draft_id  # ← 新增
}

# 步骤5: 验证附件保留
response = requests.get(f"{API_BASE_URL}/applications/{draft_id}/attachments/", ...)
assert len(attachments) == 2
```

## 回滚计划

**触发条件：**
- 后端修改导致兼容性问题
- 前端附件UI严重错误

**回滚步骤：**
```bash
git revert <commit-hash>
git push origin main
```

**数据清理（可选）：**
```sql
-- 删除孤儿附件
DELETE FROM attachments_attachment 
WHERE application_id IN (
  SELECT application_id FROM applications_application WHERE status = 'draft'
);
```

## 后续优化

**不在本次范围：**
- 附件缩略图
- 大文件分片上传
- 附件批量下载
- 附件类型图标识别
