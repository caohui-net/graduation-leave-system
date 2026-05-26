# 系统架构审查 - Round 1

**审查时间：** 2026-05-27  
**审查人：** Codex Critic Agent  
**审查范围：** 系统设计文档第1-2节（项目概述、系统架构）

## 审查结论

**VERDICT: REJECT**

发现2个CRITICAL问题和4个MAJOR问题，阻止实施。

---

## CRITICAL问题

### 1. 多数据库支持架构上不可行

**证据：** 设计文档 lines 50-51, 118-119, 236-240, 446-452

**问题：**
- 声称"支持多数据库（MySQL/PostgreSQL/SQL Server/Oracle）"
- 使用Django ORM抽象层
- 但system_configs表存储数据库连接为运行时配置
- Django数据库配置在启动时从settings.py加载，无法运行时切换

**影响：** 整个"多数据库支持"声明在架构上不可能实现。

**修复方案：**
- **方案A（推荐）：** 移除多数据库支持声明，选择一个数据库（推荐PostgreSQL）
- **方案B：** 使用环境变量+容器重启实现数据库切换，移除system_configs.db.*字段
- **方案C：** 实现真正的多租户（Django DATABASE_ROUTERS），但这是巨大的范围蔓延

### 2. 混合认证存在账户接管漏洞

**证据：** 设计文档 lines 987-1007, 256-263, 1029-1036

**问题：**
- 允许学号+密码 AND 微信OpenID同时认证同一用户
- password_hash和wechat_openid都是nullable
- 微信登录可以绑定到现有账户，无需密码验证（lines 1003-1006）

**攻击路径：**
1. 学生用学号+密码创建账户
2. 攻击者用微信OAuth绑定到该学号（无密码验证）
3. 攻击者获得永久访问权限

**修复方案：**
```python
# 微信绑定时必须验证现有凭证
if existing_user := User.objects.filter(student_id=student_id).first():
    if not existing_user.wechat_openid:
        # 用户必须先用密码登录，然后在设置中绑定微信
        raise PermissionDenied("请先使用学号密码登录，然后在设置中绑定微信")
    else:
        raise ValidationError("该学号已绑定其他微信账号")
```

添加数据库约束：
```sql
CONSTRAINT chk_auth_method CHECK (
    (password_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
)
```

---

## MAJOR问题

### 3. 缺少关键API安全组件

**问题：**
- 无速率限制
- 无请求大小限制
- 无DDoS防护

**攻击场景：**
- 暴力破解密码（/api/v1/auth/login无速率限制）
- 上传垃圾文件（/api/v1/applications/{id}/attachments无速率限制）
- DoS审批队列（垃圾申请提交）

**修复方案：**
```python
# Django REST Framework throttling
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'login': '5/minute',
        'upload': '10/hour'
    }
}
```

### 4. 文件上传缺少关键验证和安全

**问题：**
- 无MIME类型验证
- 无病毒扫描
- 无内容验证
- 路径遍历风险

**修复方案：**
```python
import magic

def validate_file_upload(file):
    # 大小检查
    if file.size > 10 * 1024 * 1024:
        raise ValidationError("文件大小超过限制")
    
    # MIME类型检查（读取实际文件内容，不是扩展名）
    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)
    if mime not in ALLOWED_MIME_TYPES:
        raise ValidationError(f"不支持的文件类型: {mime}")
    
    # 文件名清理
    safe_name = re.sub(r'[^\w\s.-]', '', file.name)
    if safe_name != file.name:
        raise ValidationError("文件名包含非法字符")
```

### 5. 审批超时监控不完整

**问题：**
- "1个工作日"应该是工作日，不是日历日
- 当前实现计算周末，导致误报
- 无明确的升级路径

**修复方案：**
```python
import chinese_calendar

def calculate_business_hours(start_time, hours=24):
    """计算截止时间，排除周末和中国节假日"""
    current = start_time
    remaining_hours = hours
    
    while remaining_hours > 0:
        current += timedelta(hours=1)
        if chinese_calendar.is_workday(current.date()):
            remaining_hours -= 1
    
    return current
```

### 6. 单体架构与可扩展性声明矛盾

**问题：**
- 架构图显示3个Django副本（水平扩展）
- 但模块设计紧耦合，阻止真正的无状态扩展
- 共享文件系统需求
- 无会话亲和性配置

**修复方案：**
- **方案A（推荐）：** 移除虚假的扩展声明，单实例部署
- **方案B：** 修复扩展问题（MinIO必需，添加分布式锁，nginx会话亲和性）

---

## 缺失组件

- 无回滚计划（辅导员误批准）
- 无批量操作（辅导员审批50个申请需点击50次）
- 无配置变更审计追踪
- 无文件保留策略
- 无学生数据变更处理
- 无微信降级方案
- 无申请撤回功能
- 无审批重新分配
- 无SLA监控仪表板
- 无数据导出（合规需求）

---

## 歧义风险

1. **"本地部署"** - 校内数据中心 vs 校属云？影响HTTPS证书策略
2. **"3个工作日" vs "1个工作日"** - 工作日 vs 日历日？当前代码用日历日
3. **"电子离校凭证"** - PDF证书 vs 数据库状态标志？

---

## 开放问题

- 为什么校园离校系统需要支持4种数据库？
- MinIO是可选还是必需？
- 预期峰值负载是多少？
- 为什么需要React Native？微信小程序不够？
- 大学能否为"本地部署"提供HTTPS证书？

---

**下一步：** 等待原设计者回应，讨论修复方案。
