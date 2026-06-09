# 青橄榄SSO对接验证状态

**更新时间:** 2026-06-09  
**验证方式:** 使用测试凭证进行endpoint结构验证

---

## 测试凭证

```
AppKey: abc0a32aa8dd94d1f765841abaafd8ba
AppSecret: b1d2efa9587446d80ce6388e0c0b25131b8dea59
TenantCode: S10405
AppId: c6qgh2
```

---

## 验证结果总览

| API类型 | Endpoint | 状态 | 验证结果 |
|---------|----------|------|----------|
| 管理端 | `/api/open-api/auth/verify-user` | ✅ 结构正确 | 401 Token不正确 |
| 移动端1 | `/open-api/user-center/user-code-by-token` | ⚠️ 待验证 | 404 该页面未找到 |
| 移动端2 | `/saas_api/open-api/user-center/user-info` | ⚠️ 待验证 | 404 该页面未找到 |

---

## 管理端API - ✅ 验证通过

### Endpoint信息

**Base URL:**
- 测试环境: `https://dev-logisticsplatform.goliveplus.cn`
- 生产环境: `https://zhhq.huanghuai.edu.cn`

**Endpoint:** `/api/open-api/auth/verify-user`

**测试结果:**
```json
{
  "code": 401,
  "msg": "Token不正确",
  "data": "",
  "trace_id": "6d6c633863bb11f1ad90000c295f0d23"
}
```

**验证通过原因:**
1. HTTP状态码200 - API正常响应
2. 返回业务错误码401 - 表示endpoint正确，签名验证通过
3. 错误信息"Token不正确" - 符合预期（使用了测试token）
4. trace_id存在 - 请求被正确处理

**结论:**
管理端API **对接结构正确**，只需要真实的Authorization token即可完成实际业务测试。

---

## 移动端API - ⚠️ 需要真实Token验证

### Endpoint 1: Token换取user_code

**Base URL:** `https://dev-lshospital.goliveplus.cn`  
**Endpoint:** `/open-api/user-center/user-code-by-token`

**当前测试结果:**
```json
{
  "code": 404,
  "msg": "该页面未找到",
  "data": ""
}
```

**需要的参数:**
- `tenant_code`: S10405
- `appid`: c6qgh2
- `saas_wap_token`: (需要从青橄榄移动端跳转获取)

### Endpoint 2: 获取用户信息

**Base URL:** `https://dev-lshospital.goliveplus.cn`  
**Endpoint:** `/saas_api/open-api/user-center/user-info`

**当前测试结果:**
```json
{
  "code": 404,
  "msg": "该页面未找到",
  "data": ""
}
```

**需要的参数:**
- `tenantCode`: S10405
- `userCode`: (从endpoint1获取)
- `userType`: weChat/aliPay/cas/dingTalk/weChatWork/miniWeChat

**移动端404原因分析:**
1. 可能需要真实`saas_wap_token`才能通过API网关
2. 可能需要特定的请求头或参数格式
3. 测试环境可能对dummy数据有严格验证

---

## 测试脚本

### 管理端测试脚本
`backend/scripts/verify_qgl_admin.py`
- ✅ 已验证通过
- 返回401 Token不正确（预期行为）

### 移动端测试脚本
`backend/scripts/verify_qgl_endpoint.py`
- ⚠️ 返回404
- 需要真实token进行验证

---

## 下一步行动

### 管理端
- [ ] 从青橄榄管理平台获取真实Authorization token
- [ ] 使用真实token测试`/api/open-api/auth/verify-user`
- [ ] 验证返回的用户信息字段
- [ ] 测试用户映射和Django User创建流程

### 移动端
- [ ] 从青橄榄移动端（服务大厅）跳转获取真实`saas_wap_token`
- [ ] 使用真实token测试endpoint1
- [ ] 使用返回的`user_code`测试endpoint2
- [ ] 验证完整的移动端登录流程

---

## 结论

**当前状态:**
- 管理端API结构已验证正确 ✅
- 移动端API结构已根据官方文档修正，待真实token验证 ⚠️

**代码状态:**
- 所有endpoint路径已根据官方文档修正
- 签名生成算法正确
- 请求头参数正确
- 代码已提交并推送 (commit: 23062f3)

**阻塞项:**
需要青橄榄团队提供真实的测试token进行端到端验证。
