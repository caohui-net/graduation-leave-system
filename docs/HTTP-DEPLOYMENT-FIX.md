# HTTP环境部署修复说明

## 问题描述

生产环境 `http://172.17.12.196:7788` 登录后会话无法保存，每次操作都被重定向到登录页。

## 根本原因

`backend/config/prod.py` 配置了：
```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

这要求必须使用HTTPS才能设置cookies，但内网部署使用HTTP协议，导致浏览器拒绝设置cookies。

## 解决方案

修改了 `backend/config/prod.py`，使用环境变量 `FORCE_HTTPS` 控制：

```python
FORCE_HTTPS = os.getenv('FORCE_HTTPS', 'True').lower() == 'true'

SECURE_SSL_REDIRECT = FORCE_HTTPS
SESSION_COOKIE_SECURE = FORCE_HTTPS
CSRF_COOKIE_SECURE = FORCE_HTTPS
```

## 部署配置

### 内网HTTP部署（当前172.17.12.196）

在 `.env` 或环境变量中设置：
```bash
FORCE_HTTPS=False
```

然后重启服务：
```bash
cd /path/to/project
source venv/bin/activate
pkill -f "gunicorn"
gunicorn config.wsgi:application --bind 0.0.0.0:7788
```

### 外网HTTPS部署（默认）

不设置 `FORCE_HTTPS` 或设置为 `True`（默认安全配置）

## 验证

重启后访问 `http://172.17.12.196:7788`：
1. 登录 → 应该看到cookies被设置
2. 点击"留校审批" → 应该进入管理页面而非重定向登录
3. 刷新页面 → 应该保持登录状态

## 安全提示

- **内网HTTP**：`FORCE_HTTPS=False` 仅用于内网测试/部署
- **外网生产**：务必使用HTTPS + `FORCE_HTTPS=True`（默认）
