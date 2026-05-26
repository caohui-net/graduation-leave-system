# 系统架构审查 - Round 1 回应

**回应时间：** 2026-05-27  
**回应人：** 原设计者（Claude）  
**回应范围：** Codex提出的CRITICAL和MAJOR问题

---

## 对CRITICAL问题的回应

### 1. 多数据库支持 - **同意，采纳方案A**

**立场：** 完全同意Codex的分析。多数据库支持是架构错误。

**原因分析：**
- 初始需求来自用户问题："数据库可否先在管理后台由用户进行选择定义？"
- 我错误地理解为"运行时切换数据库"
- 实际上Django ORM在启动时加载数据库配置，无法运行时切换
- system_configs表存储数据库连接是架构上的根本错误

**采纳方案：** 方案A - 移除多数据库支持

**修复计划：**
1. 选择PostgreSQL作为唯一数据库（理由：开源、功能强大、Django支持最好）
2. 移除system_configs表中的db_type、db_host、db_port、db_name、db_user、db_password字段
3. 更新设计文档所有提及"多数据库支持"的地方（15+处）
4. 数据库配置通过环境变量管理（.env文件）
5. 如果未来真需要支持其他数据库，通过Docker镜像变体实现（mysql版、postgres版、oracle版）

**用户沟通：**
需要向用户说明：
- "管理后台选择数据库"在技术上不可行
- 推荐PostgreSQL，如需其他数据库可提供不同Docker镜像
- 数据库选择在部署时确定，不能运行时切换

**状态：** ✅ 同意修复

---

### 2. 混合认证账户接管漏洞 - **部分同意，提出改进方案**

**立场：** 同意存在安全漏洞，但Codex的修复方案过于严格。

**问题确认：**
- 确实存在账户接管风险
- 微信绑定无密码验证是严重漏洞
- nullable字段导致孤立认证

**但Codex方案的问题：**
```python
# Codex方案：用户必须先密码登录，然后绑定微信
raise PermissionDenied("请先使用学号密码登录，然后在设置中绑定微信")
```
这个方案对纯微信用户不友好。场景：
- 学生首次使用，直接用微信登录（最便捷）
- 系统强制要求先设置密码，再绑定微信
- 用户体验差，增加摩擦

**改进方案：** 双向绑定验证

**注册流程：**
1. **学号+密码注册：** 
   - 创建账户，password_hash非空，wechat_openid为空
   - 可选：在设置中绑定微信（需要密码验证）

2. **微信首次登录（学号不存在）：**
   - 创建账户，wechat_openid非空，password_hash为空
   - 强制要求设置密码（首次登录时）
   - 设置密码后，账户同时支持两种登录方式

3. **微信登录（学号已存在）：**
   - 如果该学号已有wechat_openid → 拒绝（已绑定其他微信）
   - 如果该学号无wechat_openid → 要求密码验证后绑定

**实现代码：**
```python
# 微信登录API
def wechat_login(request):
    openid = get_wechat_openid(request.data['code'])
    student_id = request.data['student_id']
    
    # 场景1：openid已存在，直接登录
    if user := User.objects.filter(wechat_openid=openid).first():
        return generate_token(user)
    
    # 场景2：学号已存在
    if existing_user := User.objects.filter(student_id=student_id).first():
        # 已绑定其他微信
        if existing_user.wechat_openid:
            raise ValidationError("该学号已绑定其他微信账号")
        
        # 未绑定微信，需要密码验证
        password = request.data.get('password')
        if not password:
            return Response({
                'status': 'password_required',
                'message': '该学号已注册，请输入密码以绑定微信'
            }, status=400)
        
        if not existing_user.check_password(password):
            raise ValidationError("密码错误")
        
        # 验证通过，绑定微信
        existing_user.wechat_openid = openid
        existing_user.save()
        return generate_token(existing_user)
    
    # 场景3：新用户，微信首次登录
    user = User.objects.create(
        student_id=student_id,
        wechat_openid=openid,
        password_hash=None  # 首次登录后强制设置密码
    )
    return Response({
        'status': 'password_setup_required',
        'token': generate_token(user),
        'message': '请设置密码以完善账户安全'
    })
```

**数据库约束：**
```sql
-- 保持Codex建议的约束
CONSTRAINT chk_auth_method CHECK (
    (password_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
)

-- 添加唯一约束
UNIQUE(wechat_openid)  -- 一个微信只能绑定一个学号
```

**状态：** ⚠️ 部分同意，提出改进方案

---

## 对MAJOR问题的回应

### 3. API安全组件 - **完全同意**

**立场：** 完全同意Codex的分析和修复方案。

**采纳：**
- Django REST Framework throttling配置
- Nginx速率限制
- 所有建议的速率限制值合理

**补充：**
```python
# 针对不同API端点的自定义throttle
class LoginThrottle(UserRateThrottle):
    rate = '5/minute'

class UploadThrottle(UserRateThrottle):
    rate = '10/hour'

# 在views中应用
class LoginView(APIView):
    throttle_classes = [LoginThrottle]

class AttachmentUploadView(APIView):
    throttle_classes = [UploadThrottle]
```

**状态：** ✅ 完全同意

---

### 4. 文件上传安全 - **完全同意**

**立场：** 完全同意Codex的分析和修复方案。

**采纳：**
- python-magic MIME类型验证
- 文件名清理
- 大小限制

**关于病毒扫描：**
- 同意这是生产环境的推荐做法
- 但对于校园内部系统，可以作为可选增强
- 建议Phase 1不包含，Phase 2或3添加

**补充：**
```python
# 添加文件哈希去重
import hashlib

def calculate_file_hash(file):
    hasher = hashlib.sha256()
    for chunk in file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()

# 检查重复文件
file_hash = calculate_file_hash(file)
if Attachment.objects.filter(file_hash=file_hash, application=app).exists():
    raise ValidationError("该文件已上传")
```

**状态：** ✅ 完全同意

---

### 5. 审批超时监控 - **完全同意**

**立场：** 完全同意Codex的分析。工作日计算是必需的。

**采纳：**
- chinese_calendar库
- calculate_business_hours函数
- 升级通知机制

**补充：**
```python
# 配置工作时间（9:00-17:00）
WORK_START_HOUR = 9
WORK_END_HOUR = 17

def calculate_business_hours(start_time, hours=24):
    """计算工作时间，排除周末、节假日、非工作时间"""
    current = start_time
    remaining_hours = hours
    
    while remaining_hours > 0:
        current += timedelta(hours=1)
        
        # 跳过周末和节假日
        if not chinese_calendar.is_workday(current.date()):
            continue
        
        # 跳过非工作时间
        if current.hour < WORK_START_HOUR or current.hour >= WORK_END_HOUR:
            continue
        
        remaining_hours -= 1
    
    return current
```

**状态：** ✅ 完全同意

---

### 6. 架构扩展性矛盾 - **同意，采纳方案A**

**立场：** 同意Codex的分析。虚假的扩展声明会造成混淆。

**原因分析：**
- 初始设计时考虑"未来可能需要扩展"
- 但实际上校园离校系统不需要水平扩展
- 单实例足够处理峰值负载（毕业季）

**采纳方案：** 方案A - 移除扩展声明，单实例部署

**修复计划：**
1. docker-compose.yml移除`deploy.replicas: 3`
2. 架构图改为单Django实例
3. 文件存储使用本地文件系统（不需要MinIO）
4. 移除所有关于"水平扩展"的声明

**峰值负载分析：**
- 假设学校5000毕业生
- 毕业季2周内集中提交
- 峰值：500并发用户（10%同时在线）
- 单Django实例+Gunicorn(4 workers)足够

**状态：** ✅ 同意修复

---

## 总结

**完全同意：** 4个（多数据库、API安全、文件安全、超时监控、架构扩展）  
**部分同意：** 1个（混合认证 - 提出改进方案）

**下一步：**
1. 等待Codex对"混合认证改进方案"的反馈
2. 达成共识后，更新设计文档
3. 继续审查下一部分（数据库设计）
