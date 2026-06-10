# 登录设计修复总结 - 2026-06-07

## 问题描述

**原始设计缺陷：** demo-web通过角色选择器手动切换身份，用户可任意选择student/dorm_manager/counselor/dean，不符合真实登录流程，缺乏身份验证。

## 三方讨论共识

**参与方：** Claude + Codex + Gemini  
**讨论轮次：** 3轮  
**共识结论：**
- 用user_id/password登录表单替换角色选择器
- 调用现有`POST /api/auth/login`端点进行身份验证
- 前端根据服务端返回的`user.role`字段自动显示对应UI
- `/api/auth/demo-login`降级为调试辅助，不被主流程调用

## 实施方案

### 1. 后端API（已存在，无需修改）

**端点：** `POST /api/auth/login`  
**请求体：**
```json
{
  "user_id": "2020001",
  "password": "2020001"
}
```

**响应：**
```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "user": {
    "user_id": "2020001",
    "name": "张三",
    "role": "student",
    "class_id": "CS2020-01"
  }
}
```

### 2. 前端修改

**文件：** demo-web/js/api.js
- `apiLogin(role)` → `apiLogin(userId, password)`
- 调用`/api/auth/demo-login` → `/api/auth/login`
- 添加`currentUser`变量存储用户信息

**文件：** demo-web/index.html
- 移除角色选择器`<select id="roleSelector">`
- 添加登录表单（user_id + password输入框）
- 新增`doLogin()`函数处理登录逻辑
- 新增`logout()`函数清除登录状态
- 新增`updateUIForRole(role)`根据role显示对应UI
- 移除`switchRole(role)`旧逻辑
- 移除页面加载时的自动登录脚本

### 3. 环境变量

**文件：** .env.docker
- 添加`DEMO_AUTH_ENABLED=true`（支持demo-login调试端点）

## 测试验证

### API测试

```bash
# 学生登录
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020001","password":"2020001"}'
# ✅ 返回token + user(role=student)

# 宿管员登录
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id":"M001","password":"M001"}'
# ✅ 返回token + user(role=dorm_manager)
```

### UI测试（待手动验证）

1. 打开 http://localhost:8080
2. 应显示登录表单（不再是角色选择器）
3. 输入2020001/2020001，点击登录
4. 应显示学生申请表单
5. 退出登录，输入M001/M001
6. 应显示审批列表

## 演示账号

| 角色 | 用户ID | 密码 | 说明 |
|------|--------|------|------|
| 学生 | 2020001 | 2020001 | 张三 |
| 宿管员 | M001 | M001 | 宿管员1 |
| 辅导员 | T001 | T001 | 李老师 |
| 学工部 | D001 | D001 | 赵主任 |

**密码规则：** 演示环境密码=用户ID（由seed_data.py设置）

## 提交记录

**Commit:** 2c3ee07  
**Message:** fix(demo-web): 实现基于用户名/密码的真实登录流程  
**Files Changed:** 3 files, +109 insertions, -48 deletions

## 后续工作

- [ ] 手动UI测试验证登录表单正常工作
- [ ] 验证不同角色登录后显示正确界面
- [ ] 更新PROJECT-SUMMARY.md文档
- [ ] 更新.omc/session-context.json

## 讨论Artifacts

- `.omc/collaboration/artifacts/DISCUSS-DEMO-WEB登录设计缺陷修复-*-r1-codex-*.md`
- `.omc/collaboration/artifacts/DISCUSS-DEMO-WEB登录设计缺陷修复-*-r2-gemini-*.md`
- `.omc/collaboration/artifacts/DISCUSS-DEMO-WEB登录设计缺陷修复-*-r3-codex-*.md`

---

**完成时间：** 2026-06-07T14:30:00Z  
**状态：** 代码已提交并推送，待UI测试验证
