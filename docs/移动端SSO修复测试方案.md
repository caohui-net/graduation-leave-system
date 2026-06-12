# 移动端SSO修复验证测试方案

## 测试目标
验证移动端SSO从青橄榄回调后：
1. 不再出现404错误
2. 正确设置localStorage
3. 自动跳转到首页
4. 无需再次输入密码

## 测试环境准备

### 1. 确认后端运行
```bash
# 检查后端进程
pgrep -f "manage.py runserver"

# 如未运行，启动后端
cd /home/caohui/projects/graduation-leave-system/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:7787
```

### 2. 确认前端服务
```bash
# 前端文件位置
# demo-web/mobile-sso-callback.html
# 通过后端static serve或单独文件服务器访问
```

---

## 测试步骤

### 测试1：直接测试callback接口

**测试callback是否正确处理移动端参数**

```bash
# 模拟青橄榄移动端回调参数
curl -X GET "http://127.0.0.1:7787/api/sso/qingganlian/callback?authorization=test_token_123&user_id=19970545&real_name=测试用户&identity_name=学生" \
  -v 2>&1 | grep -E "(HTTP|Location|auth_token)"
```

**预期结果：**
- HTTP 200
- 返回HTML包含localStorage.setItem('auth_token')
- 返回HTML包含window.location.href = '/'
- HTML中user_info包含building和room_number字段

---

### 测试2：浏览器端到端测试

**步骤：**

1. **清除浏览器localStorage**
```javascript
// 在浏览器console执行
localStorage.clear();
console.log('localStorage cleared');
```

2. **构造测试URL访问mobile-sso-callback.html**
```
http://218.75.196.218:7788/mobile-sso-callback.html?authorization=test_auth_token&user_id=19970545&real_name=测试学生&identity_name=学生
```

3. **观察页面行为**
- 页面应立即跳转（不再停留在"正在登录..."）
- 浏览器URL应变为`/api/sso/qingganlian/callback?...`
- 然后自动跳转到首页`/`

4. **验证localStorage**
```javascript
// 在首页console执行
console.log('auth_token:', localStorage.getItem('auth_token'));
console.log('user_info:', localStorage.getItem('user_info'));
// 应显示token和用户信息JSON
```

5. **验证登录状态**
- 首页应显示用户信息（不要求输入密码）
- 能正常访问需要认证的功能

**预期现象：**
- ✅ 不再出现"登录失败: 青橄榄API错误[404]"
- ✅ 页面快速跳转（<1秒）
- ✅ localStorage包含auth_token
- ✅ 首页识别登录状态

---

### 测试3：真实青橄榄回调测试（生产验证）

**前提：需要青橄榄后台配置**

1. 登录青橄榄管理后台
2. 配置移动端应用回调URL为：
   ```
   http://218.75.196.218:7788/mobile-sso-callback.html
   ```

3. 在青橄榄移动端应用点击"宿舍门禁系统"

4. 观察回调流程：
   - 青橄榄 → mobile-sso-callback.html
   - 自动跳转 → /api/sso/qingganlian/callback
   - 自动跳转 → 首页

5. 验证登录成功且无需密码

---

## 测试用例

### 用例1：学生用户
```bash
# 参数
authorization=test_token
user_id=19970545
real_name=张三
identity_name=学生

# 预期
- role: student
- building/room_number: 显示或为空
- 能访问学生功能
```

### 用例2：教师用户
```bash
# 参数
authorization=test_token
user_id=T001
real_name=李老师
identity_name=教师

# 预期
- role: teacher
- 能访问教师功能
```

### 用例3：管理员用户
```bash
# 参数
authorization=test_token
username=admin001
identity_name=管理员

# 预期
- role: admin
- 能访问管理功能
```

---

## 故障排查

### 问题1：仍然显示404
- 检查：后端是否运行？
- 检查：callback路由是否正确？
- 查看：后端日志 `/tmp/backend.log`

### 问题2：localStorage为空
- 检查：callback_views.py的HTML是否正确执行？
- 检查：浏览器console是否有JavaScript错误？
- 验证：curl测试callback返回的HTML内容

### 问题3：跳转后仍需密码
- 检查：index.html是否正确读取localStorage？
- 检查：auth_token是否有效？
- 验证：API调用是否包含Authorization header

---

## 日志监控

### 后端日志
```bash
# 实时查看SSO登录日志
tail -f /tmp/backend.log | grep -E "(SSO|callback|login)"
```

**关键日志：**
- "SSO callback success: user=19970545"
- "Mobile login success: user=19970545"

### 前端调试
```javascript
// 浏览器console监控
localStorage.setItem = new Proxy(localStorage.setItem, {
  apply(target, thisArg, args) {
    console.log('localStorage.setItem:', args);
    return Reflect.apply(target, thisArg, args);
  }
});
```

---

## 成功标准

✅ **所有测试通过标准：**
1. callback接口返回200和正确HTML
2. mobile-sso-callback.html快速跳转（不停留）
3. localStorage包含有效auth_token和user_info
4. 首页显示登录状态，无需密码
5. 后端日志显示"SSO callback success"
6. 用户体验流畅，无错误页面

---

## 回归测试

**确认未影响PC端：**
```bash
# PC端callback测试
curl -X GET "http://127.0.0.1:7787/api/sso/qingganlian/callback?authorization=pc_token&username=admin001" \
  -v 2>&1 | grep "登录成功"
```

预期：PC端登录仍然正常
