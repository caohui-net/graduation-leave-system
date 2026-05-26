# 混合认证方案审查 - Round 3

**审查时间：** 2026-05-27  
**审查人：** Codex Critic Agent  
**审查范围：** 原设计者提出的混合认证改进方案

---

## 审查结论

**ACCEPT WITH MANDATORY ADDITIONS**

改进方案从根本上解决了账户接管漏洞，但需要添加5个强制性修改。

---

## 对三个问题的回答

### 1. 改进方案是否解决了账户接管漏洞？

**是的，但需要一个关键补充。**

✅ **已修复：**
- 绑定微信到现有账户需要密码验证
- 防止绑定到已绑定账户
- wechat_openid唯一约束
- 至少一种认证方式的数据库约束

❌ **缺失（CRITICAL）：**
**微信新用户的密码强度验证和学生身份验证**

攻击场景：
1. 攻击者用微信注册，使用受害者的student_id
2. 设置弱密码"123456"
3. 攻击者获得永久访问权限

**必需修复：**
```python
def setup_password_for_wechat_user(user, password):
    # 密码强度验证
    if len(password) < 8:
        raise ValidationError("密码至少8位")
    if not re.search(r'[A-Za-z]', password):
        raise ValidationError("密码必须包含字母")
    if not re.search(r'\d', password):
        raise ValidationError("密码必须包含数字")
    
    # 学生身份验证（选择一种）：
    # 方案A: 短信验证到注册手机
    # 方案B: 邮件验证到学生邮箱
    # 方案C: 上传学生证照片人工审核
    
    user.set_password(password)
    user.save()
```

**关键补充：** 微信新用户必须**阻止登录**直到密码设置完成且学生身份验证通过。

---

### 2. 是否还有其他安全风险？

**是的 - 发现3个额外风险：**

#### 风险A: 学号枚举攻击（HIGH严重性）

**问题：** 代码泄露student_id是否存在：
- "该学号已绑定其他微信账号" → student_id存在
- "该学号已注册，请输入密码" → student_id存在但无微信
- 创建新用户 → student_id不存在

攻击者可以枚举所有有效学号。

**修复：** 使用通用错误消息 + 速率限制
```python
if existing_user := User.objects.filter(student_id=student_id).first():
    if existing_user.wechat_openid or not password:
        # 通用消息，不泄露账户是否存在
        raise ValidationError("绑定失败，请联系管理员")
    
    if not existing_user.check_password(password):
        raise ValidationError("绑定失败，请联系管理员")  # 相同消息
```

#### 风险B: 微信绑定的竞态条件（MEDIUM严重性）

**问题：** 两个请求使用相同student_id + 不同openid可能同时通过检查，然后都执行绑定。

**修复：** 添加数据库级锁
```python
from django.db import transaction

with transaction.atomic():
    existing_user = User.objects.select_for_update().filter(
        student_id=student_id
    ).first()
    
    if existing_user:
        # 绑定逻辑
```

#### 风险C: 绑定操作无审计追踪（MEDIUM严重性）

**问题：** 绑定操作静默发生，无取证证据。

**修复：** 添加到audit_logs表
```python
AuditLog.objects.create(
    user_id=existing_user.id,
    action='wechat_bind',
    resource_type='user',
    resource_id=existing_user.id,
    ip_address=request.META.get('REMOTE_ADDR'),
    request_data={'openid': openid[:8] + '***'}
)
```

---

### 3. 用户体验和安全性的平衡是否合理？

**大部分合理，但需要一个UX改进：**

✅ **好的UX决策：**
- 允许微信优先注册 - 减少摩擦
- 延迟密码设置而不是阻止 - 良好的渐进式披露
- 清晰的错误消息 - 帮助合法用户

⚠️ **安全-UX张力点：**

`'status': 'password_setup_required'` 在密码设置前返回token。

这创建了一个窗口：
- 用户有有效的JWT token
- 用户可以访问某些API
- 但账户安全不完整

**建议：** 实现**受限token**用于不完整账户：

```python
def generate_limited_token(user):
    """只允许密码设置的token，其他都不行"""
    return jwt.encode({
        'user_id': user.id,
        'scope': 'password_setup_only',  # 受限范围
        'exp': datetime.utcnow() + timedelta(hours=1)  # 短期过期
    }, settings.SECRET_KEY)

# 在API权限检查中
class RequireCompleteAuth(BasePermission):
    def has_permission(self, request, view):
        if request.auth.get('scope') == 'password_setup_only':
            # 只允许密码设置端点
            return view.__class__.__name__ == 'SetupPasswordView'
        return True
```

---

## 最终裁决

**ACCEPT WITH MANDATORY ADDITIONS**

改进的认证设计**从根本上是健全的**，修复了关键的账户接管漏洞。双路径方法（密码优先或微信优先）是良好的UX妥协。

**实施前必需的修改：**

1. **CRITICAL**: 为微信发起的账户添加学生身份验证
2. **CRITICAL**: 为不完整账户实现受限token范围
3. **MAJOR**: 为绑定操作添加事务锁
4. **MAJOR**: 为所有绑定操作添加审计日志
5. **MAJOR**: 使用通用错误消息防止学号枚举

**更新的安全检查清单：**
```python
WECHAT_BINDING_SECURITY_CHECKLIST = [
    "现有账户需要密码验证",           # ✅ 你的方案
    "wechat_openid唯一约束",          # ✅ 你的方案
    "至少一种认证方式",               # ✅ 你的方案
    "新微信用户的学生身份验证",       # ❌ 缺失 - CRITICAL
    "不完整账户的受限token范围",      # ❌ 缺失 - CRITICAL
    "绑定操作的事务锁",               # ❌ 缺失 - MAJOR
    "所有绑定操作的审计追踪",         # ❌ 缺失 - MAJOR
    "通用错误消息（无枚举）",         # ❌ 缺失 - MAJOR
]
```

---

## 建议

继续使用改进的认证设计，但在进入实施前**将上述5个强制性修改添加到设计文档**。核心架构现在是健全的。
