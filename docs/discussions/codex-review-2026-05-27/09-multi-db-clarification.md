# 多数据库需求澄清 - Round 6

**澄清时间：** 2026-05-27  
**评估人：** Codex Critic Agent  
**评估范围：** 外部数据库集成需求

---

## 澄清结论

**RE-EVALUATION: EXTERNAL DATABASE INTEGRATION**

需求误解已澄清。实际需求是**外部系统数据库对接**，不是本项目多数据库运行。

---

## 需求确认

**原误解：**
- ❌ 本项目运行时切换自己的数据库

**实际需求：**
- ✅ 本项目使用单一数据库（PostgreSQL）
- ✅ 对接外部系统的多种数据库（MySQL/SQL Server/Oracle）
- ✅ 从外部数据库读取数据（如宿舍清退状态）

**场景：**
- 学校A宿舍系统用MySQL
- 学校B宿舍系统用SQL Server
- 学校C宿舍系统用Oracle
- 本项目需要对接这些不同的外部数据库

**结论：** 这是**完全合理且常见的企业集成需求**。

---

## 技术方案推荐

### 方案排序

**推荐：Option 3 (API) > Option 2 (SQLAlchemy) > Option 1 (Django多DB)**

---

### Option 3: API集成（强烈推荐）✅

**优点：**
- ✅ 松耦合 - 外部系统变更不影响本系统
- ✅ 安全 - 无需数据库凭证
- ✅ 可维护 - 外部系统负责数据验证/业务逻辑
- ✅ 可扩展 - 外部系统可添加缓存、限流
- ✅ 审计追踪 - API调用双方都有日志
- ✅ 未来兼容 - 外部系统迁移数据库不影响

**缺点：**
- ⚠️ 需要外部系统提供API（可能不存在）
- ⚠️ 网络延迟（但非实时查询可接受）

**实现：**
```python
# apps/integrations/dorm_system.py
class DormSystemClient:
    def __init__(self):
        config = SystemConfig.objects.get(config_key='dorm_api_url')
        self.base_url = config.config_value
        self.api_key = SystemConfig.objects.get(config_key='dorm_api_key').config_value
    
    def get_checkout_status(self, student_id):
        response = requests.get(
            f'{self.base_url}/api/students/{student_id}/checkout',
            headers={'X-API-Key': self.api_key},
            timeout=5
        )
        return response.json()
```

**system_configs配置：**
```sql
INSERT INTO system_configs (config_key, config_value, config_type) VALUES
('dorm_api_url', 'https://dorm.university.edu', 'integration'),
('dorm_api_key', 'encrypted_key_here', 'integration');
```

---

### Option 2: SQLAlchemy（可接受的备选）⚠️

**使用场景：** 外部系统**无API**且**允许直接数据库访问**。

**优点：**
- ✅ 无API时可用
- ✅ 灵活 - 支持所有主流数据库
- ✅ 只读查询相对安全
- ✅ 可通过system_configs配置

**缺点：**
- ⚠️ 安全风险 - 存储数据库凭证
- ⚠️ 紧耦合 - schema变更会破坏本系统
- ⚠️ 无业务逻辑验证
- ⚠️ 防火墙/网络复杂性

**实现：**
```python
# apps/integrations/external_db.py
from sqlalchemy import create_engine, text
import json

class ExternalDatabaseClient:
    def __init__(self, system_name):
        config = SystemConfig.objects.get(config_key=f'{system_name}_db_config')
        db_config = json.loads(config.config_value)
        
        # 构建连接字符串
        if db_config['type'] == 'mysql':
            conn_str = f"mysql+mysqldb://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        elif db_config['type'] == 'sqlserver':
            conn_str = f"mssql+pyodbc://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?driver=ODBC+Driver+17+for+SQL+Server"
        elif db_config['type'] == 'oracle':
            conn_str = f"oracle+cx_oracle://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['service_name']}"
        
        self.engine = create_engine(conn_str, pool_pre_ping=True)
    
    def query(self, sql, params=None):
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            return [dict(row) for row in result]
```

**关键安全要求：**
1. ✅ 使用**只读**数据库用户
2. ✅ 加密system_configs中的凭证
3. ✅ 连接池使用`pool_pre_ping=True`
4. ✅ 设置查询超时
5. ✅ 白名单允许的表
6. ✅ 记录所有外部数据库查询到audit_logs

---

### Option 1: Django多数据库（不推荐）❌

**为什么不推荐：**

Django多数据库功能设计用于：
- 分片自己的数据
- 自己数据库的读副本
- 分离自己的模型到不同数据库

**不适合**动态外部数据库连接因为：
- ❌ `DATABASES`设置在启动时加载，无法运行时变更
- ❌ 需要为外部表创建Django模型（紧耦合）
- ❌ Django迁移会尝试管理外部表
- ❌ 无法轻松处理每个部署的不同外部数据库类型

---

## system_configs存储可行性

**回答：是的，但需要严格的安全要求。**

### Option 3 (API) - 安全 ✅
```sql
INSERT INTO system_configs (config_key, config_value, config_type, is_encrypted) VALUES
('dorm_api_url', 'https://dorm.university.edu/api', 'integration', FALSE),
('dorm_api_key', 'encrypted_api_key', 'integration', TRUE);
```

### Option 2 (SQLAlchemy) - 有风险 ⚠️
```sql
INSERT INTO system_configs (config_key, config_value, config_type, is_encrypted) VALUES
('dorm_db_config', '{"type":"mysql","host":"10.0.1.50","port":3306,"database":"dorm","user":"readonly","password":"P@ssw0rd"}', 'integration', TRUE);
```

**强制安全措施：**

1. **静态加密：**
```python
from cryptography.fernet import Fernet

class SystemConfig(models.Model):
    def get_decrypted_value(self):
        if self.is_encrypted:
            cipher = Fernet(settings.ENCRYPTION_KEY)
            return cipher.decrypt(self.config_value.encode()).decode()
        return self.config_value
```

2. **加密密钥管理：**
```bash
# 环境变量存储，不在数据库
export ENCRYPTION_KEY="your-fernet-key-here"
```

3. **访问控制：**
```python
# 只有admin角色可查看/编辑集成配置
class SystemConfigViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
```

4. **审计日志：**
```python
# 记录每次访问加密配置
@receiver(post_init, sender=SystemConfig)
def log_config_access(sender, instance, **kwargs):
    if instance.is_encrypted:
        AuditLog.objects.create(
            action='view_encrypted_config',
            resource_type='config',
            resource_id=instance.id
        )
```

---

## 修订后的架构推荐

**Phase 1: API优先方法**
```
优先级顺序：
1. 检查外部系统是否有API → 使用Option 3
2. 如无API，请求外部团队构建
3. 如外部团队拒绝，使用Option 2（只读访问）
4. 永远不要对外部系统使用Option 1
```

---

## 最终裁决

**需求有效且常见。**

**推荐实现：**
1. ✅ **Option 3 (API)** 作为主要策略
2. ✅ **Option 2 (SQLAlchemy)** 作为无API时的备选
3. ✅ 在**system_configs**中存储连接信息（加密）
4. ❌ 避免对外部系统使用**Option 1 (Django多DB)**

**system_configs表适合此用例**，需要适当的加密和访问控制。

**无架构阻塞。** 按此澄清的需求继续。
