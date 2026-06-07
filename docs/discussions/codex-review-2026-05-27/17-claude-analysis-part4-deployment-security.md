# Round 3 Claude分析 - Part 4: 部署与安全设计

**分析日期：** 2026-05-27  
**分析人：** Claude Opus 4.7  
**分析范围：** 第7-8章（部署架构设计、安全设计）

---

## 第7章：部署架构设计

### 发现的问题

#### MAJOR - Gunicorn 4 workers配置缺少依据

**问题描述：**
设计中Django应用使用"Gunicorn 4 workers"，但未说明：
- 为什么是4个worker？
- 如何计算worker数量？
- 4核8G服务器是否足够？

**影响范围：**
- 性能目标可能无法达成
- 资源浪费或不足

**建议方案：**
**基于CPU核心数计算**：
```bash
# 推荐公式：workers = (2 × CPU核心数) + 1
# 4核服务器：workers = 9

gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 9 \
  --worker-class sync \
  --max-requests 1000 \
  --max-requests-jitter 50 \
  --timeout 30
```

**性能测试验证**：
- 测试不同worker数量（4, 6, 9, 12）
- 监控CPU使用率和响应时间
- 选择最优配置

#### MINOR - 备份策略缺少异地备份

**问题描述：**
备份策略只有本地备份（/data/backups），如果服务器硬件故障，备份也会丢失。

**建议方案：**
**本地 + 异地备份**：
```bash
# 本地备份
tar -czf /data/backups/db_${DATE}.tar.gz /data/postgres

# 异地备份（上传到对象存储或远程服务器）
rsync -avz /data/backups/ backup-server:/backups/graduation-leave/
# 或使用对象存储
aws s3 sync /data/backups/ s3://backup-bucket/graduation-leave/
```

#### MINOR - Docker Compose缺少健康检查

**问题描述：**
docker-compose.yml中服务没有健康检查配置，容器启动不代表服务就绪。

**建议方案：**
```yaml
services:
  django-app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
  
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### 优点总结

- ✓ Docker Compose配置清晰
- ✓ 数据持久化策略完善
- ✓ 备份脚本完整

### 改进建议

1. 调整Gunicorn workers配置（4 → 9）
2. 添加异地备份
3. 添加健康检查

---

## 第8章：安全设计

### 发现的问题

#### CRITICAL - API限流配置不合理

**问题描述：**
限流配置：
- 登录接口：5次/分钟
- 上传接口：10次/小时
- 普通API：1000次/小时

**问题：**
1. **登录限流过严**：5次/分钟意味着用户输错密码5次就要等1分钟，体验差
2. **上传限流过严**：10次/小时意味着用户最多上传10个文件，但申请需要3个附件，如果上传失败需要重试，很容易达到限制
3. **普通API限流过松**：1000次/小时 = 16.7次/分钟，对于恶意攻击来说太宽松

**影响范围：**
- 正常用户受限
- 恶意攻击防护不足

**建议方案：**
**分层限流**：
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        # 登录：每IP 10次/分钟，每用户 5次/5分钟
        'login_ip': '10/minute',
        'login_user': '5/5minute',
        
        # 上传：每用户 30次/小时（允许重试）
        'upload': '30/hour',
        
        # 普通API：每用户 100次/分钟
        'user': '100/minute',
        
        # 匿名：每IP 20次/分钟
        'anon': '20/minute',
    }
}
```

#### MAJOR - 文件上传缺少病毒扫描

**问题描述：**
文件上传安全措施包括：MIME验证、文件名清理、SHA256哈希，但**缺少病毒扫描**。

**影响范围：**
- 恶意文件可能上传到服务器
- 其他用户下载时感染

**建议方案：**
**集成ClamAV病毒扫描**：
```python
import pyclamd

def scan_file_for_virus(file_path):
    """使用ClamAV扫描文件"""
    cd = pyclamd.ClamdUnixSocket()
    
    # 扫描文件
    result = cd.scan_file(file_path)
    
    if result is None:
        return True  # 安全
    else:
        # 发现病毒
        virus_name = result[file_path][1]
        raise ValidationError(f"文件包含病毒：{virus_name}")

# Docker Compose添加ClamAV服务
services:
  clamav:
    image: clamav/clamav:latest
    volumes:
      - clamav_data:/var/lib/clamav
```

**或使用云服务**：
- VirusTotal API
- AWS S3 Malware Protection

#### MAJOR - 审计日志缺少敏感字段脱敏

**问题描述：**
审计日志记录`request_data`字段，可能包含敏感信息（密码、Token）。

**建议方案：**
**自动脱敏**：
```python
SENSITIVE_FIELDS = ['password', 'token', 'secret', 'api_key']

def sanitize_request_data(data):
    """脱敏敏感字段"""
    if isinstance(data, dict):
        return {
            k: '***REDACTED***' if k in SENSITIVE_FIELDS else v
            for k, v in data.items()
        }
    return data

def log_audit(user_id, action, request_data):
    AuditLog.objects.create(
        user_id=user_id,
        action=action,
        request_data=sanitize_request_data(request_data)
    )
```

#### MINOR - HTTPS证书管理未提及

**问题描述：**
设计中提到HTTPS强制，但未说明：
- 证书从哪里获取？
- 如何自动续期？
- 开发环境如何处理？

**建议方案：**
**Let's Encrypt + Certbot自动续期**：
```yaml
# docker-compose.yml
services:
  certbot:
    image: certbot/certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

### 优点总结

- ✓ 数据加密完善（bcrypt、AES-256）
- ✓ SQL注入防护（Django ORM）
- ✓ CSRF/XSS防护完善
- ✓ 审计日志完整

### 改进建议

1. **调整API限流配置**（更合理的限制）
2. **添加病毒扫描**（ClamAV或云服务）
3. **审计日志脱敏**（自动脱敏敏感字段）
4. **HTTPS证书管理**（Let's Encrypt自动续期）

---

## 实施建议优先级

### P0 - 必须修改（阻塞实施）
1. 调整API限流配置（避免误伤正常用户）

### P1 - 强烈建议（影响质量）
2. 添加病毒扫描（安全风险）
3. 审计日志脱敏（合规要求）
4. 调整Gunicorn workers配置

### P2 - 可选优化
5. 添加异地备份
6. 添加健康检查
7. HTTPS证书自动续期

---

**分析完成时间：** 2026-05-27  
**下一部分：** Part 5 - 性能与测试策略
