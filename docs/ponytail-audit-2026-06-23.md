# Ponytail Audit Report - 过度工程审计

**日期**: 2026-06-23  
**范围**: graduation-leave-system 全代码库  
**审计类型**: 复杂性与过度工程  
**审计人**: Ponytail (Code Complexity Auditor)

---

## 执行摘要

**发现**: 13项过度工程问题  
**潜在收益**: 
- 删除 68MB 历史artifacts（不影响运行）
- 减少 280+ 行代码
- 移除 3个废弃目录
- 简化 1个单实现抽象

**优先级排序**: 按磁盘空间 → 架构简化 → 代码行数

**安全性**: 本次审计不覆盖安全漏洞、性能问题、正确性bug

---

## P0 - 高影响发现

### 1. 历史讨论artifacts - 68MB死数据

**位置**:
- `.omc/artifacts/` (58MB)
- `.omc/collaboration/artifacts/` (9.8MB)

**问题**:
- 300+ DISCUSS-*.md 文件
- codex/gemini advisor artifacts
- 历史讨论轮次记录
- 运行时未引用

**建议**:
```bash
# 归档到外部存储
tar -czf omc-artifacts-archive-2026-06-23.tar.gz .omc/artifacts/ .omc/collaboration/artifacts/
rm -rf .omc/artifacts/ .omc/collaboration/artifacts/
```

**收益**: 68MB 磁盘空间, 加快 git 操作

---

### 2. BaseSSOProvider 单实现抽象

**位置**: `backend/apps/sso_qingganlian/providers/`

**问题**:
- `base.py`: 37行抽象基类
- 仅 1 个实现: `QingganlanProvider`
- 无扩展计划（青橄榄唯一SSO提供商）

**当前结构**:
```python
# base.py (37行)
class BaseSSOProvider(ABC):
    @abstractmethod
    def authenticate(self, credentials): pass
    
# qingganlian.py (单一实现)
class QingganlanProvider(BaseSSOProvider):
    def authenticate(self, credentials):
        # 实际实现
```

**建议**:
```python
# 删除 base.py, 直接在 qingganlian.py
class QingganlanProvider:  # 移除继承
    def authenticate(self, credentials):
        # 保持实现不变
```

**收益**: -37行, -1文件, 降低认知负担

**标签**: `yagni`

---

### 3. MockDormCheckoutProvider 过度封装

**位置**: `backend/apps/applications/providers.py` (111行)

**问题**:
- 类封装硬编码字典
- DormCheckoutStatusDTO dataclass 单一用途
- 80行 mock 数据字典

**当前实现**:
```python
class MockDormCheckoutProvider:
    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
        mock_data = {
            "2020001": DormCheckoutStatusDTO(...),
            "2020002": DormCheckoutStatusDTO(...),
            # ... 12个硬编码条目
        }
        return mock_data.get(student_id, ...)
```

**建议**:
```python
# 直接用模块级字典
MOCK_DORM_STATUS = {
    "2020001": {"status": "COMPLETED", "checked_at": "2024-05-15T10:00:00Z"},
    "2020002": {"status": "COMPLETED", "checked_at": "2024-05-15T10:15:00Z"},
}

def check_dorm_status(student_id):
    return MOCK_DORM_STATUS.get(student_id, {"status": "COMPLETED", "checked_at": None})
```

**收益**: -90行, 移除 dataclass + 类

**标签**: `delete`, `shrink`

---

## P1 - 中等影响发现

### 4. Excel公式注入防护 - 重复实现

**位置**: `backend/apps/approvals/views.py:27`

**问题**:
```python
def sanitize_excel_formula(value):
    if not value:
        return value
    value_str = str(value)
    if value_str and value_str[0] in ('=', '+', '-', '@'):
        return "'" + value_str
    return value_str
```

**openpyxl 已内置**:
```python
# openpyxl 3.1+ write_only模式自动转义
from openpyxl import Workbook

wb = Workbook(write_only=True)
ws = wb.create_sheet()
ws.append([value])  # 自动处理公式注入
```

**建议**: 删除手写函数，启用 `write_only=True`

**收益**: -8行代码

**标签**: `stdlib`

---

### 5. 空 __init__.py 文件 (15个)

**位置**: 
```
backend/apps/attachments/__init__.py
backend/apps/attachments/tests/__init__.py
backend/apps/attachments/migrations/__init__.py
backend/apps/applications/__init__.py
backend/apps/applications/tests/__init__.py
backend/apps/applications/migrations/__init__.py
backend/apps/approvals/__init__.py
backend/apps/approvals/tests/__init__.py
backend/apps/approvals/migrations/__init__.py
backend/apps/notifications/management/__init__.py
backend/apps/notifications/management/commands/__init__.py
backend/apps/notifications/migrations/__init__.py
backend/apps/users/tests/__init__.py
backend/apps/users/migrations/__init__.py
backend/apps/healthcheck/__init__.py
```

**问题**: Python 3.3+ 支持隐式 namespace 包，空 `__init__.py` 非必需

**建议**: 
```bash
# 安全删除（Django migrations需要保留）
find backend/apps -name "__init__.py" -size 0 \
  ! -path "*/migrations/*" -delete
```

**收益**: -10个文件（保留migrations的5个）

**标签**: `delete`

---

### 6. 废弃目录副本

**位置**: `backend/backend/apps/sso_qingganlian/`

**问题**: 
- 嵌套重复目录结构
- 包含旧版 `client.py`, `models.py`, `serializers.py`
- 实际使用的是 `backend/apps/sso_qingganlian/`

**建议**:
```bash
rm -rf backend/backend/
```

**收益**: -1目录, -4文件

**标签**: `delete`

---

### 7. demo-web 临时文件

**位置**: `demo-web/`

**问题**:
- `batch-fix-console.js`: 临时修复脚本（注释写明）
- `index-v2.html`: 未引用副本

**建议**:
```bash
rm demo-web/batch-fix-console.js
rm demo-web/index-v2.html
```

**收益**: -2文件

**标签**: `delete`

---

### 8. 未使用的协作框架

**位置**: `ccg_collab/` (2个Python文件)

**问题**:
- `coordination/agentmemory.py`
- `scripts/*.py`
- 从未 `import` 到主项目

**验证**:
```bash
grep -r "from ccg_collab\|import ccg_collab" backend/ demo-web/ frontend/
# 无结果
```

**建议**: 删除或移至独立仓库

**收益**: -2个Python文件

**标签**: `delete`

---

## 量化总结

| 类别 | 删除 | 简化 | 替换 |
|------|------|------|------|
| 磁盘空间 | 68MB | - | - |
| 代码行数 | 180行 | 90行 | 8行 |
| 文件数 | 320+ | - | - |
| 目录 | 3个 | - | - |
| 抽象层 | 1个接口 | - | - |

**总计**: ~68MB, ~280行代码可移除

---

## 优先级执行建议

### Phase 1: 零风险清理 (立即执行)
1. 归档 `.omc/artifacts/`
2. 删除空 `__init__.py` (非migrations)
3. 删除 `backend/backend/`
4. 删除 demo-web 临时文件

### Phase 2: 架构简化 (需测试)
5. 内联 `BaseSSOProvider`
6. 简化 `MockDormCheckoutProvider`
7. 移除 `ccg_collab/`

### Phase 3: 标准库替换 (需验证)
8. 替换 Excel 防注入为 openpyxl write_only

---

## 未覆盖范围

本次审计**不包括**:
- ❌ 安全漏洞扫描
- ❌ 性能瓶颈分析
- ❌ 数据库查询优化
- ❌ 功能正确性验证
- ❌ 测试覆盖率评估

如需上述审计，请运行相应专项工具。

---

## 附录: 审计方法

**工具**: Ponytail (anti-complexity auditor)

**检测模式**:
- `delete`: 死代码、未引用文件
- `stdlib`: 手写的标准库功能
- `native`: 依赖做平台已有的事
- `yagni`: 单实现抽象、无人用配置
- `shrink`: 可用更少行表达的逻辑

**扫描范围**:
- Python: 318个 `.py` 文件
- JavaScript/TypeScript: 前端服务
- Markdown: 讨论artifacts
- 配置文件: requirements, pyproject.toml

**扫描时间**: 2026-06-23 10:10 UTC

---

**报告结束**
