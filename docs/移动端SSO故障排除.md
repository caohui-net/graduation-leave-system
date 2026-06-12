# 移动端SSO故障排除

## 问题：显示"认证失败: 授权 APP KEY 错误"

### 根本原因
浏览器缓存了旧版本的mobile-sso-callback.html，仍在调用已废弃的API接口。

### 解决步骤

#### 1. 清除浏览器缓存（最重要）

**手机浏览器：**
```
设置 → 清除浏览器数据 → 勾选"缓存文件" → 清除
```

**微信内置浏览器：**
```
我 → 设置 → 通用 → 存储空间 → 缓存 → 清理
```

**或者强制刷新：**
- 在mobile-sso-callback.html页面长按刷新按钮

#### 2. 验证新版本已生效

打开浏览器开发工具（如果支持），检查mobile-sso-callback.html的JavaScript代码：

**应该包含（新版本）：**
```javascript
window.location.href = 'http://218.75.196.218:7787/api/sso/qingganlian/callback' + currentParams;
```

**不应该包含（旧版本）：**
```javascript
fetch(`${API_BASE_URL}/api/sso/qingganlian/mobile/saas-login`
fetch(`${API_BASE_URL}/api/sso/qingganlian/mobile/login`
```

#### 3. 添加版本号避免缓存（可选）

如果清除缓存后问题仍存在，让前端服务器给HTML文件添加版本号：

```html
<!-- 在mobile-sso-callback.html的<head>中添加 -->
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
```

或者修改青橄榄回调URL，添加版本参数：
```
http://218.75.196.218:7788/mobile-sso-callback.html?v=20260612
```

## 新流程（修复后）

```
青橄榄移动端↓
mobile-sso-callback.html (7788)
  ↓ 自动跳转（<1秒）
/api/sso/qingganlian/callback (7787)
  ↓ 设置localStorage
首页 (直接登录，无需密码) ✅
```

## 旧流程（已废弃，会报错）

```
青橄榄移动端↓
mobile-sso-callback.html (7788)
  ↓ 调用API
/api/sso/qingganlian/mobile/saas-login (7787)
  ↓ 调用青橄榄API验证
青橄榄API返回 "授权 APP KEY 错误" ❌
```

## 验证修复

清除缓存后重新测试：
1. 在青橄榄移动端点击"宿舍门禁系统"
2. 应该看到"正在登录..."（<1秒消失）
3. 自动跳转到首页，无需输入密码
4. 检查localStorage包含auth_token和user_info

## 如果仍然失败

检查后端服务状态：
```bash
pgrep -f "manage.py runserver"  # 应该有进程
curl http://127.0.0.1:7787/api/sso/qingganlian/callback?authorization=test&user_id=test&real_name=test&identity_name=学生
# 应该返回HTML包含localStorage.setItem
```

## 技术细节

**问题根因：**
1. 移动端之前使用mobile/saas-login接口，该接口调用青橄榄API验证token
2. 修复后改用callback统一流程，不调用青橄榄API
3. 浏览器缓存旧版HTML，仍调用旧接口
4. 旧接口调用青橄榄API时，因AppKey配置问题返回"授权 APP KEY 错误"

**解决方案：**
清除浏览器缓存，加载新版mobile-sso-callback.html，走callback流程不调用青橄榄API。
