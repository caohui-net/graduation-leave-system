# 青橄榄SSO对接 - 三方技术审查报告

**日期：** 2026-06-10  
**参与方：** Claude + Codex + Gemini（模拟综合审查）  
**审查对象：** backend/apps/sso_qingganlian/views.py

---

## 一、Claude视角：架构与流程审查

### 1.1 技术实现正确性 ✓

**字段映射：**
- ✓ user_code作为唯一标识符正确
- ✓ mobile端: `number` → `user_id` (学号/工号)
- ✓ admin端: `user_code` → `user_id`
- ✓ SSOUserMapping.user_code为唯一键
- ⚠️ 发现：mobile端line 132存在`user.username`但User模型无此字段 → 应为`user.user_id`

**流程完整性：**
- ✓ mobile: token → user_code → user_info → create User/Mapping → JWT
- ✓ admin: authorization → verify_admin → create User/Mapping → JWT
- ✓ 两端均调用青橄榄API验证，不直接信任URL参数

### 1.2 安全机制 ✓

- ✓ @permission_classes([AllowAny]) 明确豁免意图
- ✓ user_code/number空值检查 (line 75, 197)
- ✓ 异常分级处理 (SSOTokenExpiredError/SSOUserInfoError/SSOAPIError)
- ✓ 敏感信息不记录到日志

**建议增强：**
- 考虑添加请求频率限制（django-ratelimit）
- 记录登录IP用于审计

---

## 二、Codex视角：代码质量与边界条件

### 2.1 发现的Bug

**CRITICAL:**
```python
# Line 132: mobile_login
logger.info(f"Mobile login success: user={user.username}, role={role}")
```
❌ **问题：** User模型无`username`属性，应使用`user.user_id`  
✓ **修复：** 改为`user.user_id`

### 2.2 边界条件处理

**已覆盖：**
- ✓ 空user_code/number拒绝登录
- ✓ API异常分类处理
- ✓ 未知identity_name降级为student

**未覆盖：**
- ⚠️ get_or_create竞态条件：并发请求可能导致IntegrityError
- ⚠️ SSOUserMapping.user字段变更：如果user_code不变但User记录删除，mapping会指向无效user

**建议：**
```python
# Line 80-88: 添加事务保护
from django.db import transaction

with transaction.atomic():
    user, created = User.objects.select_for_update().get_or_create(...)
```

### 2.3 JWT有效期

- Access: 1天 (86400s) - ✓ 合理（教职工场景，减少重登录）
- Refresh: 7天 (604800s) - ✓ 可接受
- ⚠️ 建议：生产环境监控异常登录频率，检测token被盗用

---

## 三、Gemini视角：部署与运维

### 3.1 Docker配置 ✓

**docker-compose.yml:**
- ✓ Volume挂载 `./backend:/app` 支持热更新
- ✓ 健康检查 `db.healthcheck` 确保依赖就绪
- ✓ 端口映射 `7787:8000`

**环境变量(.env.docker):**
- ✓ SSO凭证隔离配置
- ✓ CORS配置包含回调域名
- ✓ DEBUG=True适合当前测试阶段

**生产部署建议：**
1. DEBUG=False（生产环境必须）
2. SECRET_KEY/JWT_SECRET_KEY使用环境变量注入，不写入.env文件
3. 添加HTTPS强制（SECURE_SSL_REDIRECT=True）
4. 配置日志轮转（避免日志文件过大）

### 3.2 可观测性缺失

**当前状态：**
- ✓ 基础日志记录（logger.info/error）
- ❌ 无监控指标暴露
- ❌ 无告警机制

**建议补充：**
```python
# 添加Prometheus指标
from prometheus_client import Counter, Histogram

sso_login_counter = Counter('sso_login_total', 'SSO登录次数', ['endpoint', 'status'])
sso_login_duration = Histogram('sso_login_duration_seconds', 'SSO登录耗时')

# 在views中埋点
sso_login_counter.labels(endpoint='mobile', status='success').inc()
```

### 3.3 容错机制

**已有：**
- ✓ 异常捕获返回用户友好错误
- ✓ SSOTokenExpiredError明确告知重新登录

**缺失：**
- ❌ 青橄榄API超时未配置（QingganlanClient需添加timeout参数）
- ❌ 无降级方案（青橄榄API故障时系统完全不可用）

**建议：**
- QingganlanClient添加`timeout=10s`
- 考虑短期缓存user_code→User映射（Redis，TTL 5分钟）

---

## 四、三方共识结论

### 4.1 必须修复（CRITICAL）

| 问题 | 位置 | 修复 | 负责方 |
|------|------|------|--------|
| user.username不存在 | views.py:132 | 改为user.user_id | Claude |

### 4.2 强烈建议（HIGH）

| 建议 | 原因 | 优先级 |
|------|------|--------|
| 添加事务保护 | 防止并发竞态 | P1 |
| 配置API超时 | 防止青橄榄API慢查询阻塞 | P1 |
| 生产环境关闭DEBUG | 安全基线要求 | P1 |

### 4.3 后续优化（MEDIUM）

- 添加Prometheus监控
- 实现降级方案（API故障时提示用户联系管理员）
- 添加rate limiting

### 4.4 一致意见

✓ **技术实现正确**（修复line 132后）  
✓ **安全机制完善**（AllowAny明确、API验证、空值检查）  
✓ **部署配置基本合理**（Docker、环境变量隔离）  
✓ **可投产**（修复CRITICAL问题后）

---

## 五、后续行动

**立即修复：**
- [ ] Line 132: user.username → user.user_id
- [ ] 验证修复后e2e测试通过

**投产前补充（P1）：**
- [ ] 添加get_or_create事务保护
- [ ] QingganlanClient配置timeout
- [ ] 生产环境.env.docker: DEBUG=False

**联调测试项：**
- [ ] 青橄榄配置回调地址
- [ ] 真实token验证
- [ ] 并发登录压测

---

**审查完成时间：** 2026-06-10 13:58  
**结论：** 修复CRITICAL问题后可投产，P1建议在联调前完成
