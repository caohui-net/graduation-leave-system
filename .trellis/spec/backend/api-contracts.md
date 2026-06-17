# API Contracts

> Executable API contracts: signatures, payloads, validation, errors.

---

## Scenario: 附件上传草稿转化流程

### 1. Scope / Trigger
- 用户创建草稿 → 上传附件 → 提交申请，需确保附件绑定到正确的申请记录
- 触发code-spec深度：跨层数据流（前端→后端→数据库），API契约变更

### 2. Signatures

**Backend API:**
```python
# POST /api/applications/
def create_application(request):
    # 接收参数
    application_id = request.data.get('application_id')  # 可选
    contact_phone = request.data['contact_phone']
    reason = request.data.get('reason', '')
    leave_date = request.data['leave_date']
```

**Frontend API调用:**
```javascript
async function apiSubmitApplication(phone, reason, leaveDate, applicationId)
```

### 3. Contracts

**请求字段:**
- `contact_phone` (string, required): 联系电话
- `reason` (string, optional): 离校原因
- `leave_date` (date, required): 离校日期
- `application_id` (string, optional): 草稿ID，用于精确转化指定草稿

**响应字段 (ApplicationListSerializer):**
- `application_id` (string): 申请ID
- `has_attachments` (boolean): 是否有附件
- `attachment_count` (int): 附件数量（新增字段）
- `approvals` (array): 审批记录

### 4. Validation & Error Matrix

| 条件 | 错误码 | 错误信息 |
|------|--------|----------|
| `application_id`提供但草稿不存在 | `NOT_FOUND` | "草稿不存在或已提交" |
| `application_id`提供但不属于当前用户 | `NOT_FOUND` | "草稿不存在或已提交" |
| `application_id`提供但状态不是DRAFT | `NOT_FOUND` | "草稿不存在或已提交" |
| `application_id`未提供 | - | 回退：自动查找任意草稿（向后兼容） |

### 5. Good/Base/Bad Cases

**Good (精确转化):**
```python
# 前端传递草稿ID
formData.append('application_id', draftId)

# 后端精确查找
draft = Application.objects.filter(
    student=user,
    application_id=application_id,
    status=ApplicationStatus.DRAFT
).first()
```

**Base (向后兼容):**
```python
# 前端未传application_id
# 后端自动查找任意草稿
draft = Application.objects.filter(
    student=user, 
    status=ApplicationStatus.DRAFT
).first()
```

**Bad (丢失附件):**
```python
# 问题：前端有draftId但未传递，后端总是查找"任意草稿"
# 结果：如果用户有多个草稿，可能转化错误的草稿，导致附件丢失
draft = Application.objects.filter(
    student=user,
    status=ApplicationStatus.DRAFT
).first()  # 不精确
```

### 6. Tests Required

**Unit Tests:**
- 测试精确草稿转化：传递`application_id`，验证转化正确草稿
- 测试向后兼容：不传`application_id`，验证自动查找行为
- 测试草稿不存在：传递无效`application_id`，验证404错误

**Integration Tests:**
- 完整流程：创建草稿 → 上传2个附件 → 提交（传递draftId） → 验证附件数量
- 验证API返回`attachment_count`字段

**Assertion Points:**
- `assert response.data['attachment_count'] == 2`
- `assert draft.application_id == provided_application_id`
- `assert application.attachments.count() == 2`

### 7. Wrong vs Correct

#### Wrong
```javascript
// 前端：未传递草稿ID
const result = await apiSubmitApplication(phone, reason, leaveDate);

// 后端：总是查找"任意草稿"
draft = Application.objects.filter(student=user, status=ApplicationStatus.DRAFT).first()
# 问题：多个草稿时可能转化错误的草稿
```

#### Correct
```javascript
// 前端：传递草稿ID
const result = await apiSubmitApplication(phone, reason, leaveDate, draftId);

// 后端：优先精确查找
if application_id:
    draft = Application.objects.filter(
        student=user,
        application_id=application_id,
        status=ApplicationStatus.DRAFT
    ).first()
    if not draft:
        return Response({'error': {'code': 'NOT_FOUND', ...}}, 404)
else:
    # 回退：向后兼容
    draft = Application.objects.filter(student=user, status=ApplicationStatus.DRAFT).first()
```

---

## Design Decision: 列表API返回附件数量

**Context:** 前端列表需要显示附件状态（📎图标+数量），避免对每个申请单独查询附件

**Options Considered:**
1. 前端逐个查询附件 → 性能差，N+1查询
2. 后端只返回`has_attachments` → 不够直观
3. 后端返回`attachment_count` → 一次查询，清晰展示

**Decision:** 后端`ApplicationListSerializer`新增`attachment_count`字段

**Implementation:**
```python
class ApplicationListSerializer(serializers.ModelSerializer):
    attachment_count = serializers.SerializerMethodField()
    
    def get_attachment_count(self, obj):
        return obj.attachments.filter(is_deleted=False).count()
```

**Frontend Usage:**
```javascript
const attachmentInfo = app.has_attachments 
    ? `<span style="color: #1890ff;">📎 ${app.attachment_count}个附件</span>` 
    : '';
```

**Extensibility:** 未来如需附件详情，可增加`attachments`字段返回列表；当前方案满足列表展示需求

---

## Common Mistakes

### Mistake 1: 草稿转化不精确导致附件丢失

**Symptom:** 用户上传附件后提交，申请记录无附件

**Cause:** 
- 前端创建草稿A，上传附件到草稿A
- 前端提交时未传`application_id`
- 后端查找"任意草稿"，可能找到旧的草稿B
- 草稿B转化为申请，草稿A的附件丢失

**Fix:** 前端传递`application_id`，后端精确查找并转化指定草稿

**Prevention:** 
- 前端保存`draftId`到全局变量
- 提交时传递`draftId`到API
- 后端优先精确查找，回退到自动查找（向后兼容）

---

**Created:** 2026-06-17  
**Task:** .trellis/tasks/06-17-fix-attachment-workflow-and-ui
