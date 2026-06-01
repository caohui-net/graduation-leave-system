# API Schema 待完善清单

**创建日期：** 2026-06-02  
**最后更新：** 2026-06-02  
**状态：** P1代码完成，验收阻塞（环境依赖未满足），P2待后续完善

---

## 基线验收状态

⏸ 待可用环境复验（Django环境依赖未满足）
- `/api/schema/` 端点可访问性
- Swagger UI 可访问性
- Operation统计（13条path/15个operation）
- JWT Bearer认证配置
- Schema生成警告检查

---

## 已完成项（P1）

### 1. ✓ Function-based Views的extend_schema装饰器

**完成状态：** 已为所有13个function-based views添加@extend_schema装饰器
- 2个dispatchers使用method-scoped装饰器（applications_view, attachments_view）
- 11个单方法views使用标准装饰器
- 明确指定request/response schema、parameters、operationId

---

### 2. ✓ OperationId冲突修复

**完成状态：** 所有@extend_schema装饰器中明确指定operation_id，避免自动生成冲突

---

### 3. ✓ 统一错误响应结构

**完成状态：** 
- 创建ErrorResponseSerializer（backend/schema.py）
- 所有使用项目错误envelope的端点在responses中包含ErrorResponseSerializer
- Login的DRF默认ValidationError单独记录

---

### 4. ✓ 文件上传/下载Schema

**完成状态：**
- 文件上传：使用AttachmentUploadSerializer（multipart/form-data）
- 文件下载：使用OpenApiTypes.BINARY
- 文件类型和大小限制在serializer中定义

---

### 5. ✓ 分页结构

**完成状态：**
- 创建ApplicationListResponseSerializer、ApprovalListResponseSerializer、NotificationListResponseSerializer
- 创建AttachmentListResponseSerializer（wrapper结构）
- 所有分页响应使用专用serializers

---

### 6. ✓ Login响应Schema修复

**完成状态：**
- 创建LoginResponseSerializer（schema-only）
- 修复auth_login的200响应schema不匹配问题
- 原问题：@extend_schema使用LoginSerializer（字段：user_id, password），但运行时返回{access_token, token_type, user}
- 修复后：200响应使用LoginResponseSerializer，准确描述实际响应结构

---

## 待完善项（P2）

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

## 完成状态总结

**P1（重要）- 已完成：**
- ✓ 为13个function-based views添加@extend_schema装饰器
- ✓ 修复operationId冲突（明确指定operation_id）
- ✓ 补充统一错误响应结构（ErrorResponseSerializer）
- ✓ 补充文件上传/下载schema
- ✓ 完善分页结构（专用响应serializers）
- ✓ 修复login响应schema不匹配（LoginResponseSerializer）

**P2（建议）- 待完善：**
- 添加请求/响应示例（OpenApiExample）

---

## 验证说明

由于环境限制（Django未安装），以下验证需要在可用环境中完成：
- Schema生成无警告
- `/api/schema/` 返回200
- `/api/schema/swagger-ui/` 返回200
- Operation IDs唯一性验证
- 后端测试通过

代码修改已完成，语法正确。

---

## 后续建议

P2项（请求/响应示例）可在后续Phase中添加，建议在Track 3 Phase 2B或Phase 3中统一处理。

---

**文档版本：** v2.2  
**最后更新：** 2026-06-02  
**变更：** D0修正：状态改为"代码完成，验收阻塞"，基线验收改为"待环境复验"
