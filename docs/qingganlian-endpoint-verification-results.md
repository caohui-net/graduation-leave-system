# 青橄榄API Endpoint验证结果

**验证日期:** 2026-06-09  
**验证脚本:** `backend/scripts/verify_qgl_endpoint.py`

## 测试结果

测试了两个可能的endpoint路径：

1. `/saas_api/open-api/user-center/user-info` → HTTP 200, body: `{"code":404,"msg":"该页面未找到"}`
2. `/open-api/user-center/user-info` → HTTP 200, body: `{"code":404,"msg":"该页面未找到"}`

## 结论

两个路径均返回404错误，可能原因：

1. **需要真实token** - 测试使用的是模拟数据，青橄榄API可能需要真实的用户token才能访问
2. **endpoint路径不同** - 实际API路径可能与文档不一致
3. **环境问题** - 测试环境(dev-lshospital.goliveplus.cn)可能与正式环境不同

## 建议

1. 使用真实的青橄榄移动端token进行端到端测试
2. 联系青橄榄技术支持确认正确的API endpoint路径
3. 查阅最新的API文档

## 当前实现

代码中使用 `/saas_api/open-api/user-center/user-info` 路径（基于之前的实现）。
在真实环境测试时需要验证此路径是否正确。

## 相关文件

- 验证脚本: `backend/scripts/verify_qgl_endpoint.py`
- API客户端: `backend/apps/sso_qingganlian/client.py`
- 实现文档: `docs/design/2026-06-08-sso-qingganlian-integration.md`
