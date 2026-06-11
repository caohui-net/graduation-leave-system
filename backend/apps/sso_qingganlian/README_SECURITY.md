# SSO安全配置说明

## admin_login Token验证开关

### 配置
```bash
# .env文件或环境变量
QGL_VERIFY_ADMIN_TOKEN=true   # 开启验证（默认，推荐）
QGL_VERIFY_ADMIN_TOKEN=false  # 关闭验证（仅用于对接调试）
```

### 使用场景

**生产环境（推荐）：**
```bash
QGL_VERIFY_ADMIN_TOKEN=true
```
- 调用青橄榄`verify-user` API验证authorization token
- 验证失败返回401
- 防止认证绕过漏洞

**对接调试期（临时）：**
```bash
QGL_VERIFY_ADMIN_TOKEN=false
```
- 跳过token验证
- 仅检查参数存在性
- 用于排查青橄榄对接问题

### 日志监控

```bash
# 验证成功
INFO Admin token verified: {...}

# 验证失败
ERROR Admin token verification failed: 88890006 - TOKEN已过期

# 验证跳过（警告）
WARNING Admin token verification SKIPPED (QGL_VERIFY_ADMIN_TOKEN=False)
```

### 风险提示

⚠️ **关闭验证存在安全风险**：任何人知道username就能伪造管理员登录

建议：
1. 对接成功后立即开启验证
2. 配置nginx/防火墙限制SSO端点只允许青橄榄IP访问
3. 监控日志，发现异常访问立即处理

### 对接失败排查

如果开启验证后管理端对接失败：

1. 检查青橄榄返回的authorization格式
2. 查看后端日志中的验证失败原因
3. 确认ADMIN_APP_KEY/ADMIN_APP_SECRET配置正确
4. 临时关闭验证完成对接，再排查验证问题
