# Error Logging Middleware

## 功能

捕获并记录所有视图中未处理的异常，包括：
- 请求方法和路径
- 用户ID
- 查询参数
- 异常类型和消息
- 完整堆栈跟踪

## 启用方法

在Django settings.py的MIDDLEWARE列表中添加：

```python
MIDDLEWARE = [
    # ... 其他中间件
    'apps.middleware.ErrorLoggingMiddleware',
]
```

**位置**: 建议放在MIDDLEWARE列表末尾，确保捕获所有异常

## 日志输出

错误日志会输出到Django配置的logger，包含：
- 日志级别: ERROR
- 额外字段: user_id, method, path, query_params, exception_type, exception_message, traceback

## 已有日志覆盖

- ✅ SSO登录异常（mobile_saas_login, mobile_login, admin_login）
- ✅ 批量审批错误（batch_action_approvals详细日志）
- ✅ 审批导出失败（export_approvals）
- ⚠️ 404/403预期错误无ERROR日志（符合预期）
