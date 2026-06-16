# 毕业生离校系统综合审计报告（Codex + Gemini 共识版）

**审计日期：** 2026-06-15  
**评审方式：** Codex独立代码审计 + Claude-Gemini多轮协作讨论  
**审计范围：** 代码质量、架构设计、安全性、性能、可维护性、业务逻辑完整性

---

## 执行摘要

**Codex结论：** 项目功能完整，审批事务和基础权限控制良好，但**生产安全边界偏弱**。不建议按生产标准直接上线，需先修复SSO认证绕过、密钥硬编码、日志泄漏和性能问题。

**Gemini结论：** 采用分阶段、基于证据的审计策略，优先保障核心外部集成合约（青橄榄SSO、学工系统API）稳定性，同时严格评估系统性能、安全性和业务逻辑完整性。

**共识意见：** 两方一致认为系统业务逻辑完善，但**安全性和性能为生产环境主要阻塞项**。

---

## 关键发现对比

| 审计维度 | Codex 发现 | Gemini 发现 | 共识 |
|---------|-----------|------------|------|
| **架构设计** | 功能模块清晰，Django/DRF标准架构 | 外部依赖高耦合（SSO/学工API），同步阻塞式调用风险 | ✓ 架构合理但外部集成为脆弱点 |
| **安全性** | **P0严重**：SSO认证可绕过、密钥硬编码、日志泄漏敏感信息 | 基础防护到位（RBAC、ORM防注入），待强化审计日志和API限流 | ⚠️ **Codex识别出关键安全漏洞** |
| **性能** | N+1查询风险（列表/详情未预取关联） | 缺少负载测试，毕业高峰期并发未验证 | ✓ 性能为未知高风险项 |
| **代码质量** | 测试文件存在但pytest执行不稳定 | 实用主义风格，缺少静态分析自动化 | ✓ 功能优先，技术债需偿还 |
| **业务逻辑** | 审批事务和权限控制做得不错 | 边缘案例处理良好（兜底宿管员路由） | ✓ 业务逻辑健壮完整 |
| **可维护性** | 根路由硬编码外部IP，部署不通用 | 文档充足但测试覆盖率未知 | ✓ 需改进部署配置和测试 |

---

## 严重安全问题（Codex独家发现）

### 🚨 P0-1: SSO认证可被弱化或绕过

**位置：** `backend/apps/sso_qingganlian/views.py:143`

**问题详情：**
```python
# mobile_login 在 VERIFY_MOBILE_TOKEN=False 时直接信任请求里的 user_id
if not settings.VERIFY_MOBILE_TOKEN:
    user_id = request.data.get('user_id')  # 危险：无验证
```

```python
# admin_login 只验证token有效性，未校验token与username绑定关系
token_valid = verify_token(token)  # 仅验证格式
# 缺失：验证 token.user_id == username
```

**影响：**
- **账号冒用** - 任意用户可伪造他人身份登录
- **管理员身份伪造** - 持有任意有效token可登录任意管理员账号
- 生产环境配置失误风险极高

**修复方案：**
```python
# 1. 强制开启token验证
VERIFY_MOBILE_TOKEN = True  # 移除False选项

# 2. 校验token身份绑定
decoded = verify_token(token)
if decoded['user_id'] != request.data['user_id']:
    raise AuthenticationFailed('Token与用户身份不匹配')
```

**修复优先级：** P0 - 立即修复

---

### 🚨 P0-2: 密钥默认值硬编码

**位置：** 
- `backend/config/settings/base.py:11`
- `backend/apps/sso_qingganlian/settings.py:6`

**问题代码：**
```python
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')
QGL_MOBILE_APP_KEY = os.getenv('QGL_MOBILE_APP_KEY', 'cb6f276a42042179e90cd79c4126e075')
QGL_MOBILE_APP_SECRET = os.getenv('QGL_MOBILE_APP_SECRET', '5e7a4e70...')
```

**影响：**
- JWT签名密钥不安全（可被预测）
- 外部平台凭据泄漏
- 配置错误时默默降级为不安全状态

**修复方案：**
```python
# 启动时强制检查
SECRET_KEY = os.environ['SECRET_KEY']  # 移除默认值，环境变量缺失时抛异常
QGL_MOBILE_APP_KEY = os.environ['QGL_MOBILE_APP_KEY']

# 或使用fail-fast校验
if SECRET_KEY == 'django-insecure-*' or len(SECRET_KEY) < 50:
    raise ImproperlyConfigured('生产环境必须设置安全的SECRET_KEY')
```

**修复优先级：** P0 - 立即修复

---

### 🚨 P0-3: SSO客户端打印敏感信息

**位置：** `backend/apps/sso_qingganlian/client.py:61`

**问题代码：**
```python
print(f"[SSO API] Headers: {headers}")  # 泄漏签名和密钥
print(f"[SSO API] Data: {data}")        # 泄漏用户信息
print(f"[SSO API] Response: {response.text}")  # 泄漏token和身份证号
```

**影响：**
- 敏感数据写入日志文件
- 运维排查时暴露token、签名、个人信息
- 日志成为攻击面

**修复方案：**
```python
import logging
logger = logging.getLogger(__name__)

# 脱敏日志
logger.info(f"[SSO API] Endpoint: {endpoint}")
logger.debug(f"[SSO API] Headers: {self._sanitize_headers(headers)}")

def _sanitize_headers(self, headers):
    safe = headers.copy()
    for key in ['sign', 'appKey', 'Authorization']:
        if key in safe:
            safe[key] = safe[key][:8] + '***'
    return safe
```

**修复优先级：** P0 - 立即修复

---

## 性能问题共识

### ⚠️ P1-1: N+1查询风险（Codex发现）

**位置：** 
- `backend/apps/applications/views.py:67`
- `backend/apps/applications/serializers.py` - `SerializerMethodField`

**问题：**
```python
# Serializer中重复查询
def get_approvals(self, obj):
    return obj.approvals.all()  # 每个application都查一次

# 列表视图未预取
queryset = Application.objects.all()  # 缺少prefetch_related
```

**影响：**
- 100条申请记录 = 1 + 100次SQL查询
- 管理端分页查看时响应变慢

**修复方案：**
```python
# 视图层预取
queryset = Application.objects.all().prefetch_related(
    Prefetch('approvals', queryset=Approval.objects.select_related('approver'))
)
```

---

### ⚠️ P1-2: 负载测试缺失（Gemini发现）

**问题：** 毕业高峰期（数千学生同时提交）场景未验证

**影响：** 
- 同步SSO验证可能导致请求堆积
- 数据库连接池耗尽风险
- 外部API超时导致系统雪崩

**修复方案：**
```bash
# 负载测试（500并发用户提交申请）
locust -f tests/load_test.py --host=http://localhost:8000 -u 500 -r 50

# 压测场景
1. 500学生同时SSO登录
2. 300学生并发提交申请
3. 50宿管员批量审批
```

**目标指标：**
- P95响应时间 < 2s
- 错误率 < 0.1%
- 数据库连接数 < 80%

---

## 外部依赖脆弱性（Gemini核心关注）

### ⚠️ 架构风险：同步阻塞式SSO调用

**证据：**
- 本次修复的网络不可达错误：
  ```
  OSError: [Errno 101] Network is unreachable
  HTTPSConnectionPool(host='xuegongmj.hgnu.edu.cn', port=443): Max retries exceeded
  ```

**影响：**
- 青橄榄SSO故障 → 全系统登录不可用
- 学工API超时 → 申请列表加载失败

**Gemini质疑：**
> "如果外部系统故障是由我们API的刚性设计导致（如同步阻塞验证），如何平衡'保持兼容性'与'解决性能/安全问题'？"

**修复建议：**
1. **引入断路器模式**
   ```python
   from circuitbreaker import circuit
   
   @circuit(failure_threshold=5, recovery_timeout=60)
   def call_qgl_api(self, endpoint, data):
       # 5次失败后断路，60秒后尝试恢复
   ```

2. **异步SSO验证**（保持兼容性）
   ```python
   # 现有同步接口保持不变
   # 新增异步接口供前端升级
   @api_view(['POST'])
   async def mobile_login_async(request):
       token_data = await asyncio.to_thread(client.get_user_code_by_token, token)
   ```

3. **降级方案**
   - SSO故障时允许管理员使用本地密码登录
   - 学工API故障时使用缓存数据

---

## 测试与验证体系

### Codex发现：pytest执行不稳定

**问题：** 
- 测试文件存在但收集/运行配置有问题
- 未能完成自动化验证

### Gemini建议：执行覆盖率测试

**行动项：**
```bash
# 1. 修复pytest配置
pytest --collect-only  # 检查测试收集

# 2. 运行覆盖率测试
pytest --cov=backend/apps --cov-report=html --cov-report=term

# 3. 目标覆盖率
- 关键路径（SSO、审批流）：>90%
- 整体覆盖率：>70%
```

---

## 部署配置问题

### ⚠️ 根路由硬编码外部IP（Codex发现）

**位置：** `backend/config/urls.py:8`

**问题代码：**
```python
path('', lambda r: redirect('http://218.75.196.218:8081/'), name='home')
```

**影响：**
- 测试环境、灰度环境无法正常使用
- 迁移时必须修改代码

**修复方案：**
```python
# settings.py
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:8081/')

# urls.py
path('', lambda r: redirect(settings.FRONTEND_URL), name='home')
```

---

## 必须保持稳定的兼容性合约（Gemini明确）

**不可破坏的接口：**

1. **青橄榄SSO**
   - `/api/sso/qingganlian/admin-login`
   - `/api/sso/qingganlian/mobile/saas-login`
   - 请求/响应格式、签名算法

2. **学工系统数据同步**
   - 用户数据导入管道
   - Excel字段映射格式

3. **审批流状态机**
   - 宿管员 → 辅导员 → 学工部
   - `ApprovalStep` / `ApprovalDecision` 枚举值

**审计原则：** 所有安全加固和性能优化必须100%向后兼容这些合约。

---

## 修复优先级（综合Codex + Gemini）

### 🚨 P0 - 立即修复（阻塞上线）

| 问题 | 发现方 | 预计工时 |
|------|--------|---------|
| 1. SSO认证绕过漏洞 | Codex | 4h |
| 2. 密钥硬编码移除 | Codex | 2h |
| 3. 敏感日志脱敏 | Codex | 3h |

**总计：** 9小时（1个工作日）

---

### ⚠️ P1 - 本周完成

| 问题 | 发现方 | 预计工时 |
|------|--------|---------|
| 4. N+1查询优化 | Codex | 4h |
| 5. 负载测试执行 | Gemini | 8h |
| 6. 断路器引入 | Gemini | 6h |
| 7. 附件类型校验加强 | Codex | 3h |
| 8. 根路由配置化 | Codex | 1h |

**总计：** 22小时（3个工作日）

---

### 📋 P2 - 持续改进

| 问题 | 发现方 | 预计工时 |
|------|--------|---------|
| 9. pytest修复与覆盖率测试 | Codex+Gemini | 8h |
| 10. 静态分析CI集成 | Gemini | 4h |
| 11. 审计日志系统 | Gemini | 12h |
| 12. API限流机制 | Gemini | 6h |
| 13. 敏感数据加密 | Gemini | 8h |

**总计：** 38小时（5个工作日）

---

## 整体评级对比

| 维度 | Codex评分 | Gemini评分 | 共识评分 |
|------|----------|-----------|---------|
| **架构设计** | 7/10 | 6.5/10 | **6.5/10** - 功能实现但外部耦合高 |
| **代码质量** | 6.5/10 | 7/10 | **6.5/10** - 实用但需规范 |
| **安全性** | **4/10** ⚠️ | 7.5/10 | **5/10** ⚠️ - Codex发现严重漏洞 |
| **性能** | 6/10 | ?/10 | **?/10** - 未验证高风险 |
| **可维护性** | 6.5/10 | 7/10 | **6.5/10** - 测试待加强 |
| **业务逻辑** | 8/10 | 8/10 | **8/10** - 边缘案例完善 ✓ |

---

## 生产上线建议

### ❌ 当前状态：不建议生产上线

**阻塞原因（Codex + Gemini共识）：**
1. SSO认证绕过漏洞可导致任意账号冒用
2. 密钥硬编码存在被预测风险
3. 负载能力未验证，毕业高峰期可能崩溃

### ✅ 最小可上线标准

**必须完成：**
- ✅ 修复所有P0安全漏洞（9小时）
- ✅ 执行负载测试并通过指标（8小时）
- ✅ 引入外部API断路器（6小时）

**预计时间：** 3个工作日

**上线后监控：**
- 青橄榄/学工API可用性 >99%
- P95响应时间 <2s
- 错误率 <0.1%
- 每日生成审计日志报告

---

## 落地执行计划

### Day 1 - 安全加固（P0）
- 08:00-12:00 修复SSO认证绕过 + 密钥硬编码
- 13:00-16:00 敏感日志脱敏
- 16:00-18:00 安全修复验证测试

### Day 2 - 性能验证（P1）
- 08:00-12:00 N+1查询优化
- 13:00-17:00 负载测试执行
- 17:00-18:00 性能瓶颈分析

### Day 3 - 稳定性加固（P1）
- 08:00-14:00 断路器引入
- 14:00-16:00 附件校验 + 配置化
- 16:00-18:00 集成测试 + 部署验证

### Week 2 - 持续改进（P2）
- pytest修复（2天）
- 审计日志系统（2天）
- API限流 + 数据加密（1天）

---

## 审计工件位置

**Codex报告：** `docs/project-audit-report-2026-06-15.md`  
**Gemini讨论记录：** `.collab/artifacts/DISCUSS-毕业生离校系统项目整体评估分析和审计-*`  
**本报告：** `docs/project-audit-consolidated-report-2026-06-15.md`

---

## 审计团队

- **Codex：** 代码级安全审计，发现3个P0级严重漏洞
- **Gemini：** 架构与性能评估，提出外部依赖脆弱性关注
- **Claude：** 协调与综合，完成两方结论整合

**审计完成时间：** 2026-06-15 16:20  
**下次复审建议：** P0修复后1周内
