# 青橄榄SSO API结构修复记录

**修复时间:** 2026-06-09T04:21  
**问题发现:** 用户指出API地址不对，要求重新分析接口文档

## 问题分析

**原错误理解:**
- 之前错误地统一了移动端API前缀为 `/saas_api/open-api/`
- 实际上移动端使用两种不同的endpoint前缀

**正确的API结构:**

### 移动端API (Mobile)

Base URL: `https://dev-lshospital.goliveplus.cn`

1. **Token换取user_code**
   - Endpoint: `/open-api/user-center/user-code-by-token`
   - 注意：**没有** `/saas_api` 前缀
   - 参数: `tenant_code`, `appid`, `saas_wap_token`

2. **获取用户信息**
   - Endpoint: `/saas_api/open-api/user-center/user-info`
   - 注意：**有** `/saas_api` 前缀
   - 参数: `tenantCode`, `userCode`, `userType`

### 管理端API (Admin)

Base URL (Test): `https://dev-logisticsplatform.goliveplus.cn`  
Base URL (Prod): `https://zhhq.huanghuai.edu.cn`

- Endpoint: `/api/open-api/auth/verify-user`
- 参数: `token` (Authorization token from 青橄榄管理平台)

## 代码修复

### 修复位置
`backend/apps/sso_qingganlian/client.py:102`

**修复前:**
```python
endpoint = '/saas_api/open-api/user-center/user-code-by-token'
```

**修复后:**
```python
endpoint = '/open-api/user-center/user-code-by-token'
```

### 验证状态

- ✅ Endpoint路径已根据官方文档修正
- ✅ 签名生成算法正确
- ✅ Header参数正确
- ⚠️ 端到端测试需要真实token（当前测试使用dummy数据）

## 为什么之前测试返回404

1. **Endpoint路径错误** - 第一个移动端API使用了错误的 `/saas_api` 前缀
2. **测试数据不完整** - 没有真实的 `saas_wap_token`，API可能拒绝请求

## 下一步测试计划

### 需要的测试数据

1. **移动端测试:**
   ```
   - 真实的 saas_wap_token（从青橄榄移动端跳转获取）
   - tenant_code: S10405
   - appid: c6qgh2
   ```

2. **管理端测试:**
   ```
   - 真实的 Authorization token（从青橄榄管理平台获取）
   ```

### 测试步骤

1. 从青橄榄移动端（服务大厅）跳转到第三方应用，获取URL中的token
2. 使用真实token调用 `/open-api/user-center/user-code-by-token`
3. 使用返回的 `user_code` 调用 `/saas_api/open-api/user-center/user-info`
4. 验证用户信息是否正确返回
5. 测试用户映射和Django用户创建流程

## 参考文档

- `docs/移动端 - 用户信息获取接口文档.docx`
- `docs/后台管理端-单点登录对接接口文档.docx`
- 已转换文本版本: `/tmp/移动端 - 用户信息获取接口文档.txt`
- 已转换文本版本: `/tmp/后台管理端-单点登录对接接口文档.txt`

## 修复总结

关键发现：青橄榄移动端API使用**两种不同的endpoint前缀**，这在一开始的代码审计中没有被正确识别。通过重新分析官方接口文档，确认了正确的API结构并完成修复。
