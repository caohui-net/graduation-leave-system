# 青橄榄SSO接口清单

## 1. 现有实现接口

### 1.1 移动端接口（QingganlanClient）

| 方法名 | 功能 | 端点 | 请求方式 | 状态 |
|--------|------|------|----------|------|
| get_user_code_by_token | Token换user_code | /api/open-api/token-usercode-query | POST | ✅已实现 |
| get_user_info | 获取用户详细信息 | /api/open-api/getUserInfo | POST | ✅已实现 |

### 1.2 管理端接口

| 方法名 | 功能 | 端点 | 请求方式 | 状态 |
|--------|------|------|----------|------|
| verify_admin_user | 验证管理员token | /api/sso/auth/getUserInfo | POST | ✅已实现 |

## 2. 用户提供的新接口

### 2.1 信息中心数据接口

| 接口名 | 功能 | 端点 | 请求方式 | 状态 |
|--------|------|------|----------|------|
| 获取租户人员信息 | 批量获取师生数据 | /api/open-api/user-center/tenant/auth-user-info | POST | ❌未实现 |

**接口详情：**
- URL: https://xuegongmj.hgnu.edu.cn/api/open-api/user-center/tenant/auth-user-info
- 测试环境: https://dev-saas-api.goliveplus.cn/api/open-api/user-center/tenant/auth-user-info
- 生产环境: https://saas.api.goliveplus.cn/api/open-api/user-center/tenant/auth-user-info

**Credentials:**
- AppId: c6qgh2
- AppKey: abc0a32aa8dd94d1f765841abaafd8ba
- AppSecret: b1d2efa9587446d80ce6388e0c0b25131b8dea59
- TenantCode: S10405

## 3. 测试计划

### 3.1 现有接口测试
- [ ] 移动端token换user_code
- [ ] 移动端获取用户信息
- [ ] 管理端验证用户

### 3.2 新接口测试（信息中心）
- [ ] 测试AppId映射（方案A: appKey=c6qgh2）
- [ ] 测试AppKey映射（方案B: appKey=abc0a32...）
- [ ] 验证正确的credentials组合

### 3.3 业务流程测试
- [ ] 完整移动端登录流程
- [ ] 完整管理端登录流程
- [ ] 用户数据同步流程
