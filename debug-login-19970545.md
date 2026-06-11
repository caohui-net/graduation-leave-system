# 用户19970545登录问题排查

## 问题描述
移动端SSO登录卡在"正在登录..."页面，未跳转

## 需要收集的信息

### 1. 浏览器Console日志
打开微信开发者工具或Chrome Remote Debugging，查看：
```
Console标签页的错误信息
Network标签页的请求状态
```

### 2. 后端日志
```bash
# 查看SSO登录日志（用户19970545）
cd /home/caohui/projects/graduation-leave-system/backend
grep -A 5 "19970545" logs/django.log | tail -50

# 或查看最近登录请求
tail -100 logs/django.log | grep -E "(Mobile login|SSO|19970545)"
```

### 3. URL参数
记录完整的回调URL（脱敏后）：
```
http://218.75.196.218:7787/sso-callback.html?authorization=xxx&user_id=19970545&...
```

### 4. 快速测试API
```bash
# 测试移动端登录接口
curl -X POST http://218.75.196.218:7787/api/sso/qingganlian/mobile/login \
  -H "Content-Type: application/json" \
  -d '{
    "authorization": "test_token",
    "user_id": "19970545",
    "real_name": "测试",
    "identity_name": "学生"
  }'
```

## 可能的修复方案

### A. 添加超时处理（前端）
问题：fetch无超时控制，网络慢时无反馈

### B. 检查用户数据（后端）
问题：用户19970545可能缺少必需字段（building/room_number）

### C. 增强错误日志（后端）
问题：后端异常未记录详细堆栈

## 下一步
提供上述调试信息后，可精准定位问题
