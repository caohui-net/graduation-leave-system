# 青橄榄SSO代码审计 - Bug修复记录

**审计时间:** 2026-06-09  
**审计方式:** Claude-Gemini多轮讨论  
**Codex状态:** json_parse_failed (未参与)

## 修复的Critical Bugs

### 1. ✅ 安全漏洞：空用户名账户接管 (Task #12)

**问题描述:** views.py中mobile_login和admin_login使用空字符串作为username fallback，导致所有缺少标识符的用户共享同一账户。

**修复位置:**
- `backend/apps/sso_qingganlian/views.py:71-74` (mobile_login)
- `backend/apps/sso_qingganlian/views.py:192-195` (admin_login)

**修复方式:** 添加验证，拒绝空标识符请求，返回400错误。

### 2. ✅ Payload格式错误 (Task #10)

**问题描述:** client.py使用`data=data`发送form-encoded数据，应使用`json=data`发送JSON payload。导致API返回404/415错误。

**修复位置:** `backend/apps/sso_qingganlian/client.py:65`

**修复方式:** 将`data=data`改为`json=data`

### 3. ✅ API路径前缀不一致 (Task #11)

**问题描述:** client.py移动端API使用不同前缀：`/open-api/`和`/saas_api/open-api/`，导致404错误。

**修复位置:** `backend/apps/sso_qingganlian/client.py:102`

**修复方式:** 统一移动端API前缀为`/saas_api/open-api/`

### 4. ✅ 生产环境URL配置 (Task #13)

**状态:** 已确认为配置缺口，非代码bug

**位置:** `backend/apps/sso_qingganlian/client.py:11`

**说明:** MOBILE_API_BASE['prod']指向dev环境，已标记TODO。需要青橄榄团队提供正式生产URL。管理端prod URL已正确配置。

## 待验证

修复后需要真实token进行端到端测试：
- 使用真实青橄榄移动端token测试移动端登录流程
- 使用真实管理端token测试管理端登录流程
- 验证API路径修复后能否正常调用

## 下一步

提交代码re-review (taolun)，确认修复有效，达成共识。
