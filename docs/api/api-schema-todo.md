# API Schema 待完善清单

**创建日期：** 2026-06-02  
**状态：** Option E-lite Step 2基线完成，待后续完善

---

## 基线验收状态

✓ `/api/schema/` 可访问（HTTP 200）  
✓ Swagger UI 可访问（HTTP 200）  
✓ 13条path/15个operation出现在schema中  
✓ JWT Bearer认证可见（type: http, scheme: bearer, bearerFormat: JWT）  
✓ 生成器警告已记录（见下方待完善项）

---

## 待完善项

### 1. Function-based Views需要extend_schema装饰器

**影响端点：**
- `/api/notifications/` - list_notifications
- `/api/notifications/{notification_id}/read/` - mark_as_read
- `/api/notifications/mark_all_read/` - mark_all_read
- `/api/notifications/unread_count/` - unread_count
- `/api/applications/` - applications_view
- `/api/applications/{application_id}/` - get_application
- `/api/applications/{application_id}/attachments/` - attachments_view
- `/api/approvals/` - list_approvals
- `/api/approvals/{approval_id}/approve/` - approve_approval
- `/api/approvals/{approval_id}/reject/` - reject_approval
- `/api/attachments/{attachment_id}/` - delete_attachment
- `/api/attachments/{attachment_id}/download/` - download_attachment
- `/api/auth/login/` - login

**问题：**
```
Error [function_name]: unable to guess serializer. This is graceful fallback handling for APIViews.
Consider using GenericAPIView as view base class, if view is under your control.
Either way you may want to add a serializer_class (or method). Ignoring view for now.
```

**解决方案：**
为每个function-based view添加`@extend_schema`装饰器，明确指定：
- request body schema（POST/PUT/PATCH）
- response schema（所有方法）
- parameters（query/path参数）
- examples（请求/响应示例）

**示例：**
```python
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

@extend_schema(
    request=LoginSerializer,
    responses={200: TokenSerializer, 400: ErrorSerializer},
    examples=[
        OpenApiExample(
            'Login Success',
            value={'access_token': 'eyJ...', 'refresh_token': 'eyJ...'},
            response_only=True,
        ),
    ],
)
@api_view(['POST'])
def login(request):
    ...
```

---

### 2. OperationId冲突

**问题：**
```
Warning: operationId "applications_retrieve" has collisions 
[('/api/applications/', 'get'), ('/api/applications/{application_id}/', 'get')]. 
resolving with numeral suffixes.
```

**影响：**
- `/api/applications/` GET - 列表端点
- `/api/applications/{application_id}/` GET - 详情端点

**当前解决：**
drf-spectacular自动添加数字后缀（applications_retrieve, applications_retrieve_2）

**建议改进：**
使用`@extend_schema`明确指定operationId：
```python
@extend_schema(operation_id='list_applications')
@api_view(['GET'])
def applications_view(request):
    ...

@extend_schema(operation_id='get_application_detail')
@api_view(['GET'])
def get_application(request, application_id):
    ...
```

---

### 3. 自定义错误响应结构

**当前状态：**
Schema中错误响应为空（`description: No response body`）

**待补充：**
统一错误响应结构：
```python
{
  "error": {
    "code": "ERROR_CODE",
    "message": "错误消息",
    "details": {...}  # 可选
  }
}
```

**解决方案：**
1. 创建ErrorSerializer
2. 在所有`@extend_schema`中添加错误响应：
```python
responses={
    200: SuccessSerializer,
    400: ErrorSerializer,
    401: ErrorSerializer,
    403: ErrorSerializer,
    404: ErrorSerializer,
    422: ErrorSerializer,
}
```

---

### 4. 文件上传/下载Schema

**影响端点：**
- `/api/applications/{application_id}/attachments/` POST - 文件上传
- `/api/attachments/{attachment_id}/download/` GET - 文件下载

**当前状态：**
文件上传/下载的schema不完整

**待补充：**
1. 文件上传：multipart/form-data格式
2. 文件下载：binary response
3. 文件类型限制说明
4. 文件大小限制说明

**解决方案：**
```python
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'file': {'type': 'string', 'format': 'binary'},
                'attachment_type': {'type': 'string', 'enum': ['transcript', 'certificate', 'other']},
            },
        },
    },
    responses={200: AttachmentSerializer},
)
```

---

### 5. 分页结构

**当前状态：**
通知列表API使用分页，但schema中未体现分页结构

**待补充：**
分页响应结构：
```python
{
  "count": 100,
  "next": "http://...",
  "previous": "http://...",
  "results": [...]
}
```

**解决方案：**
使用drf-spectacular的分页支持或自定义分页serializer

---

### 6. 请求/响应示例

**当前状态：**
Schema中缺少请求/响应示例

**待补充：**
为关键端点添加OpenApiExample：
- 登录请求/响应
- 申请提交请求/响应
- 审批操作请求/响应
- 通知列表响应
- 错误响应示例

---

## 优先级建议

**P0（必须）：**
- 无（基线已满足验收标准）

**P1（重要）：**
- 为function-based views添加基本的request/response schema
- 修复operationId冲突
- 补充统一错误响应结构

**P2（建议）：**
- 添加文件上传/下载schema
- 完善分页结构
- 添加请求/响应示例

---

## 执行建议

根据Option E-lite执行约束：
- 本轮（Step 2）只验收基线可访问性，不承诺完整schema
- 待完善项可在后续Phase中逐步完善
- 建议在Track 3 Phase 2B或Phase 3中统一处理schema完善

---

**文档版本：** v1.0  
**最后更新：** 2026-06-02
