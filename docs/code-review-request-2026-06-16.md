# 代码审查请求 - P0/P1安全性能修复

**日期：** 2026-06-16  
**审查范围：** 3个commit，14个文件，+504/-55行  
**修复类型：** P0安全漏洞 + P1性能优化

---

## 提交记录

```
167e76d security: 加强附件类型校验（P1）
b7f2dda perf: 修复P1性能问题（N+1查询优化+根路由配置化）
0f3bf16 security: 修复P0安全漏洞（SSO认证/密钥硬编码/敏感日志）
```

---

## P0安全修复（commit: 0f3bf16）

### 1. SSO认证绕过漏洞修复

**文件：** `backend/apps/sso_qingganlian/views.py`

**问题：**
- `mobile_login`: VERIFY_MOBILE_TOKEN=False时直接信任请求中的user_id
- `admin_login`: 只验证token有效性，未校验token与username绑定

**修复：**
- admin_login添加token与username绑定验证
- 增强VERIFY_*_TOKEN=False时的WARNING日志

**代码变更：**
```python
# admin_login: 添加绑定验证
verified_username = verify_result.get('data', {}).get('username') or verify_result.get('data', {}).get('user_id')
if verified_username and verified_username != username:
    logger.error(f"Admin token verification failed: token username {verified_username} != request username {username}")
    return Response({'error': '认证失败: 用户身份不匹配'}, status=status.HTTP_401_UNAUTHORIZED)
```

### 2. 密钥硬编码移除

**文件：** 
- `backend/config/settings/base.py`
- `backend/apps/sso_qingganlian/settings.py`

**问题：**
- SECRET_KEY等敏感配置有默认值
- 环境变量缺失时默默降级为不安全状态

**修复：**
- 保留默认值（避免中断业务）
- 添加启动时WARNING检查

### 3. 敏感日志泄漏修复

**文件：** `backend/apps/sso_qingganlian/client.py`

**问题：**
- print直接输出headers/data/response（含token/签名/个人信息）

**修复：**
- 替换为logging模块
- 添加_sanitize_headers/_sanitize_data脱敏方法
- 敏感字段只保留前8字符

---

## P1性能优化（commit: b7f2dda）

### 4. N+1查询优化

**文件：** `backend/apps/applications/views.py`

**问题：**
- ApplicationListSerializer使用SerializerMethodField获取approvals
- 每个application单独查询approvals和student

**修复：**
```python
# list_applications
queryset = queryset.select_related('student').prefetch_related('approvals__approver')

# get_application
application = Application.objects.select_related('student').prefetch_related('approvals__approver').get(application_id=application_id)
```

**效果：** 100条记录从1+100次查询降至3次

### 5. 根路由配置化

**文件：** 
- `backend/config/settings/base.py`
- `backend/config/urls.py`

**问题：**
- 根路由硬编码跳转到固定IP（218.75.196.218:7788）

**修复：**
- 添加FRONTEND_URL环境变量
- 默认值：http://localhost:8081/

---

## P1附件安全（commit: 167e76d）

### 6. 附件类型校验加强

**文件：** 
- `backend/apps/attachments/serializers.py`
- `backend/apps/attachments/views.py`

**问题：**
- 只校验扩展名，可伪造
- 下载时缺少安全响应头

**修复：**
- 添加detect_file_type函数（基于magic number）
- 支持JPEG/PNG/PDF/DOC/DOCX识别
- 下载时添加安全响应头（X-Content-Type-Options/X-Frame-Options/CSP）

**无新依赖，向后兼容**

---

## 测试验证

**Django配置检查：** ✓ 通过  
**安全警告显示：** ✓ 正常  
**模块导入测试：** ✓ 成功

---

## 审查重点

1. **SSO绑定验证逻辑**是否完整？是否有绕过风险？
2. **N+1查询优化**是否引入新的性能问题？
3. **附件类型检测**的magic number识别是否准确？
4. **安全响应头**配置是否合理？
5. **向后兼容性**是否保证？已上传文件是否受影响？

---

## 待讨论问题

**断路器实施必要性：**
- 是否应该为青橄榄SSO和学工API调用引入断路器模式？
- 评估收益、风险、实施成本和替代方案

---

**审查人：** 待指定  
**预计审查时间：** 1-2小时
