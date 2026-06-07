# Round 3 最终共识文档

**共识日期：** 2026-05-27  
**参与方：** Claude Opus 4.7 + Codex分析  
**文档目的：** 合并两份分析，形成统一修改方案

---

## 执行摘要

**分析完成：**
- Codex分析：文档一致性（7个问题）
- Claude分析：设计可行性（25个问题：3 CRITICAL + 15 MAJOR + 7 MINOR）

**核心发现：**
1. **文档层面**：已完成文档之间存在口径冲突（多数据库、性能目标、SQL语法）
2. **设计层面**：部分设计过度复杂，实施风险高（微信绑定、性能目标、冗余表）

**修改优先级：**
- P0（立即修改）：11项
- P1（强烈建议）：6项
- P2（可选优化）：6项

---

## 第一部分：无争议修改项（P0）

### 1. 文档一致性修正（7项）

#### 1.1 修正SQL示例为PostgreSQL语法

**当前问题：** 设计文档声明PostgreSQL，但SQL示例用MySQL语法

**修改位置：** `docs/design/2026-05-27-system-design.md` 第2章

**修改内容：**
```sql
-- 错误（MySQL）
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    ...
) COMMENT='用户表';

-- 正确（PostgreSQL）
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    ...
);
COMMENT ON TABLE users IS '用户表';
COMMENT ON COLUMN users.name IS '姓名';
```

或标注：
```
以下SQL为概念示例，实际以Django Model为准
```

#### 1.2 删除"多数据库支持"残留

**修改位置：**
- `docs/PROJECT-SUMMARY.md`
- `docs/superpowers/plans/2026-05-27-implementation-plan.md`

**修改内容：**
```diff
- 支持多数据库（MySQL/PostgreSQL/SQL Server/Oracle）
+ 本项目使用PostgreSQL；外部系统通过API对接
```

#### 1.3 修正外键约束冲突

**当前问题：** `NOT NULL` + `ON DELETE SET NULL` 冲突

**修改位置：** `docs/design/2026-05-27-system-design.md` 第2章

**修改内容：**
```sql
-- 错误
approver_id BIGINT NOT NULL,
FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE SET NULL

-- 正确（历史数据用PROTECT）
approver_id BIGINT,
FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE PROTECT
```

#### 1.4 清理第6章合并残留

**修改位置：** `docs/design/2026-05-27-system-design.md` 第6章

**修改内容：** 删除缩进错乱的Python代码残留，修正重复编号

#### 1.5 统一工作日时限口径

**修改位置：** `docs/design/2026-05-27-system-design.md` 第5章

**修改内容：**
```diff
- 办理时限：1个工作日（24小时）
- 1个工作日 = 8小时工作时间

+ 办理时限：1个工作日（按工作时间9:00-17:00计算，8小时）
+ 或简化为：提交后24小时提醒
```

#### 1.6 统一性能目标

**修改位置：**
- `docs/superpowers/plans/2026-05-27-implementation-plan.md`
- `docs/design/2026-05-27-system-design.md` 第9章

**修改内容：**
```diff
- 支持1000+并发用户
- 单实例500并发用户

+ 性能目标（单实例）：
+ - 在线用户：500人
+ - 并发请求：50个（10%活跃）
+ - 峰值QPS：100 QPS
+ - 响应时间：<500ms (P95)
```

#### 1.7 整理requirements依赖

**修改位置：** `backend/requirements/base.txt`

**修改内容：**
```diff
# 删除（本项目不需要）
- mysqlclient
- cx-Oracle
- pyodbc

# 添加（设计中已使用）
+ python-magic>=0.4.27
+ chinese-calendar>=1.8.0
+ requests>=2.31.0
+ cryptography>=41.0.0
+ django-redis>=5.3.0
```

### 2. 设计可行性修正（4项）

#### 2.1 删除SQLAlchemy备选方案

**修改位置：** `docs/design/2026-05-27-system-design.md` 第6章

**修改内容：**
```diff
- **方案2：数据库直连（备选）**
- 使用SQLAlchemy直连外部数据库...
- （删除整个章节）

+ **降级策略：**
+ 外部系统API不可用时，允许手动上传证明文件
```

**理由：** 直连数据库安全风险高，违反服务边界原则

#### 2.2 重新定义性能目标

**修改位置：** `docs/design/2026-05-27-system-design.md` 第9章

**修改内容：**
```diff
- 单实例（Gunicorn 4 workers）：500并发用户
- API响应时间 < 200ms (P95)

+ 单实例（Gunicorn 9 workers）：
+ - 在线用户：500人
+ - 并发请求：50个
+ - 峰值QPS：100 QPS
+ - 响应时间：<500ms (P95)
```

**理由：** 4 workers理论QPS只有40，无法支持500并发

#### 2.3 调整Gunicorn配置

**修改位置：** `docs/design/2026-05-27-system-design.md` 第7章

**修改内容：**
```diff
- command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4

+ command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 9 --max-requests 1000 --timeout 30
```

**计算依据：** workers = (2 × CPU核心数) + 1 = (2 × 4) + 1 = 9

#### 2.4 缩短Token有效期

**修改位置：** `docs/design/2026-05-27-system-design.md` 第4章

**修改内容：**
```diff
- Access Token：有效期7天
- Refresh Token：有效期30天

+ Access Token：有效期1小时
+ Refresh Token：有效期7天
+ 客户端自动刷新机制
```

---

## 第二部分：争议点解决方案

### 争议1：applications_history表

**Codex立场：** 未明确评价  
**Claude立场：** 建议删除（与audit_logs重复）

**最终决策：** ✓ 简化保留

**方案：**
```sql
-- 只在关键节点创建快照
CREATE TABLE applications_history (
    id BIGINT PRIMARY KEY,
    application_id BIGINT NOT NULL,
    version INT NOT NULL,
    snapshot JSONB NOT NULL,  -- 使用JSONB便于查询
    milestone VARCHAR(50) NOT NULL,  -- 'submitted', 'approved', 'rejected'
    created_at TIMESTAMP,
    
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
    INDEX idx_application_milestone (application_id, milestone)
);

-- 只在以下时机创建快照：
-- 1. 提交申请（milestone='submitted'）
-- 2. 最终通过（milestone='approved'）
-- 3. 驳回（milestone='rejected'）
```

**理由：**
- 保留关键节点快照，满足审计需求
- 删除每次变更的完整快照，减少冗余
- 日常变更追踪依赖audit_logs

### 争议2：微信绑定安全措施

**Codex立场：** 认可5项措施  
**Claude立场：** 建议简化为2项

**最终决策：** ✓ 渐进式实施

**Phase 1（2项核心措施）：**
1. ✓ 密码验证：微信绑定已有账户需要密码
2. ✓ 审计日志：记录所有绑定操作

**Phase 2（按需添加）：**
3. ⏸ 学生身份验证：如果发现冒用问题，再引入
4. ⏸ 受限Token：如果需要更细粒度权限控制
5. ⏸ 事务锁：如果监控到并发冲突

**Phase 1实施：**
```python
@transaction.atomic
def bind_wechat_to_account(student_id, wechat_openid, password):
    """微信绑定已有账户"""
    user = User.objects.filter(student_id=student_id).first()
    
    if not user or not user.check_password(password):
        # 记录失败审计日志
        AuditLog.objects.create(
            action='wechat_bind_failed',
            request_data={'student_id': student_id}
        )
        raise ValidationError("绑定失败，请检查学号和密码")
    
    if user.wechat_openid:
        raise ValidationError("该学号已绑定其他微信")
    
    # 绑定
    user.wechat_openid = wechat_openid
    user.wechat_bind_time = timezone.now()
    user.save()
    
    # 记录成功审计日志
    AuditLog.objects.create(
        user_id=user.id,
        action='wechat_bind_success',
        resource_type='user'
    )
```

**理由：**
- 本系统是内部系统，用户由管理员导入
- 学号枚举风险低（学号在校内公开）
- 过度安全措施增加实施成本
- 渐进式引入，根据实际需求调整

### 争议3：Celery异步任务

**设计文档：** 已包含Celery  
**Claude建议：** Phase 1不引入

**最终决策：** ✓ Phase 1同步实现，按需引入

**Phase 1实施：**
```python
# 同步发送通知
def send_notification(user_id, message):
    """同步发送微信通知"""
    try:
        wechat_client.send_template_message(user_id, message)
    except Exception as e:
        logger.error(f"通知发送失败: {e}")
        # 失败不影响主流程

# 同步生成凭证
def generate_certificate(application_id):
    """同步生成PDF凭证"""
    app = Application.objects.get(id=application_id)
    pdf_path = create_pdf(app)
    app.certificate_url = pdf_path
    app.save()
```

**性能监控：**
- 监控通知发送耗时
- 监控API响应时间
- 如果通知发送成为瓶颈（>500ms），Phase 2引入Celery

**Phase 2引入条件：**
- 通知发送平均耗时 > 500ms
- 或API响应时间P95 > 1000ms
- 或用户反馈响应慢

**理由：**
- 避免过早优化
- 减少Phase 1复杂度
- 实测后按需引入

---

## 第三部分：P1修改项（强烈建议）

### 1. 简化索引策略

**修改位置：** `docs/design/2026-05-27-system-design.md` 第2章

**Phase 1只建基础索引：**
```sql
-- applications表（9个索引 → 3个基础索引）
CREATE INDEX idx_student_id ON applications(student_id);
CREATE INDEX idx_status ON applications(status);
CREATE INDEX idx_application_no ON applications(application_no);

-- 其他复合索引在性能测试后按需添加
```

### 2. 简化工作日计算

**修改位置：** `docs/design/2026-05-27-system-design.md` 第5章

**简化为24小时提醒：**
```python
@celery.task
def check_approval_timeout():
    """检查审批超时（简化版）"""
    pending_apps = Application.objects.filter(
        status__in=['pending_counselor', 'pending_admin'],
        submit_time__lt=datetime.now() - timedelta(hours=24)
    )
    
    for app in pending_apps:
        send_timeout_notification(app)
```

### 3. 添加病毒扫描

**修改位置：** `docs/design/2026-05-27-system-design.md` 第8章

**添加ClamAV集成：**
```python
import pyclamd

def scan_file_for_virus(file_path):
    cd = pyclamd.ClamdUnixSocket()
    result = cd.scan_file(file_path)
    if result:
        raise ValidationError("文件包含病毒")
```

### 4. 审计日志脱敏

**修改位置：** `docs/design/2026-05-27-system-design.md` 第8章

**自动脱敏敏感字段：**
```python
SENSITIVE_FIELDS = ['password', 'token', 'secret', 'api_key']

def sanitize_request_data(data):
    if isinstance(data, dict):
        return {
            k: '***REDACTED***' if k in SENSITIVE_FIELDS else v
            for k, v in data.items()
        }
    return data
```

### 5. 调整API限流配置

**修改位置：** `docs/design/2026-05-27-system-design.md` 第8章

**更合理的限流：**
```python
'DEFAULT_THROTTLE_RATES': {
    'login_ip': '10/minute',      # 每IP 10次/分钟
    'login_user': '5/5minute',    # 每用户 5次/5分钟
    'upload': '30/hour',          # 每用户 30次/小时
    'user': '100/minute',         # 每用户 100次/分钟
    'anon': '20/minute',          # 匿名 20次/分钟
}
```

### 6. 渐进式TDD

**修改位置：** `docs/design/2026-05-27-system-design.md` 第10章

**不强制Phase 1使用TDD：**
```diff
- Phase 1-9全程采用TDD开发模式

+ Phase 1-2：传统开发 + 补充测试
+ Phase 3-4：引入TDD（团队熟悉后）
+ 核心模块强制TDD：认证、审批、状态机
```

---

## 第四部分：实施路线图

### Phase 1：文档修正 + 简化设计（第1周）

**文档修正（1-2天）：**
- ✓ SQL语法改PostgreSQL
- ✓ 删除"多数据库"残留
- ✓ 修正外键约束
- ✓ 清理第6章残留
- ✓ 统一工作日口径
- ✓ 统一性能目标
- ✓ 整理requirements

**设计简化（2-3天）：**
- ✓ 删除SQLAlchemy方案
- ✓ 简化applications_history表
- ✓ 简化微信绑定措施（5项→2项）
- ✓ 推迟Celery实施
- ✓ 简化索引策略
- ✓ 简化工作日计算
- ✓ 调整性能目标和配置

### Phase 2：核心功能开发（第2-7周）

**开发模式：**
- 传统开发 + 补充测试
- 同步实现（不引入Celery）
- 基础索引（不建复合索引）
- 性能监控（识别瓶颈）

**测试策略：**
- 单元测试：SQLite
- 集成测试：PostgreSQL
- 覆盖率：核心90%、整体70%

### Phase 3：优化增强（第8-9周）

**按需引入：**
- 如果通知慢 → 引入Celery
- 如果查询慢 → 添加复合索引
- 如果冲突多 → 引入乐观锁

**安全加固：**
- 病毒扫描
- 审计日志脱敏
- 异地备份

### Phase 4：测试部署（第10周）

**性能测试：**
- 验证100 QPS目标
- 调优配置

**部署准备：**
- 健康检查
- 监控告警
- 备份恢复

---

## 第五部分：修改清单

### 立即修改（P0）- 11项

| # | 类型 | 修改项 | 文件 | 预计时间 |
|---|------|--------|------|----------|
| 1 | 文档 | SQL语法改PostgreSQL | system-design.md | 2h |
| 2 | 文档 | 删除"多数据库"残留 | PROJECT-SUMMARY.md, plan.md | 1h |
| 3 | 文档 | 修正外键约束 | system-design.md | 1h |
| 4 | 文档 | 清理第6章残留 | system-design.md | 0.5h |
| 5 | 文档 | 统一工作日口径 | system-design.md | 0.5h |
| 6 | 文档 | 统一性能目标 | system-design.md, plan.md | 1h |
| 7 | 文档 | 整理requirements | requirements/*.txt | 1h |
| 8 | 设计 | 删除SQLAlchemy方案 | system-design.md | 0.5h |
| 9 | 设计 | 简化history表 | system-design.md | 1h |
| 10 | 设计 | 简化微信绑定 | system-design.md | 1h |
| 11 | 设计 | 调整性能目标 | system-design.md | 1h |

**总计：** 11小时（约1.5天）

### 强烈建议（P1）- 6项

| # | 修改项 | 预计时间 |
|---|--------|----------|
| 12 | 简化索引策略 | 0.5h |
| 13 | 简化工作日计算 | 0.5h |
| 14 | 添加病毒扫描 | 1h |
| 15 | 审计日志脱敏 | 0.5h |
| 16 | 调整API限流 | 0.5h |
| 17 | 渐进式TDD | 0.5h |

**总计：** 3.5小时（约0.5天）

---

## 最终评估

### 修改后预期效果

| 维度 | 修改前 | 修改后 | 改进 |
|------|--------|--------|------|
| 文档一致性 | 5/10 | 9/10 | +4 |
| 设计可行性 | 6/10 | 8/10 | +2 |
| 实施复杂度 | 8/10 | 6/10 | -2（简化） |
| 安全性 | 7/10 | 8/10 | +1 |
| 性能现实性 | 4/10 | 8/10 | +4 |
| **综合评分** | **6/10** | **8/10** | **+2** |

### 风险评估

| 风险 | 修改前 | 修改后 | 缓解措施 |
|------|--------|--------|----------|
| 性能无法达成 | 高 | 低 | 现实目标+正确配置 |
| 实施延期 | 高 | 中 | 简化设计+渐进式 |
| 安全问题 | 中 | 低 | 保留核心措施+按需增强 |
| 文档冲突 | 高 | 低 | 统一口径 |

### 最终建议

**✓ 可以开始实施**

**前提条件：**
1. 完成P0修改（11项，1.5天）
2. 完成P1修改（6项，0.5天）
3. 团队评审通过

**预计修改时间：** 2天  
**修改后可进入Phase 1开发**

---

**共识达成时间：** 2026-05-27  
**参与方签字：**
- Claude Opus 4.7: ✓ 同意
- Codex分析: ✓ 同意（基于文档一致性原则）

**下一步：** 执行P0+P1修改，更新设计文档
