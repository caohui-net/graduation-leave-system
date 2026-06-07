### 登录设计修复及审计（2026-06-07下午）

**问题背景:**
- demo-web使用角色选择器手动切换身份（student/dorm_manager/counselor/dean）
- 不符合真实登录流程，缺乏身份验证
- 需要改为用户名/密码登录，系统根据后端返回的role确定UI

**修复实施:**
- ✓ 移除角色选择器，新增登录表单（user_id + password输入框）
- ✓ apiLogin改为调用POST /api/auth/login（真实认证端点）
- ✓ 新增doLogin()处理登录逻辑，updateUIForRole()根据role显示UI
- ✓ 新增logout()清除登录状态
- ✓ 新增用户状态栏显示当前用户信息

**三方审计（Claude-Codex-Gemini，3轮讨论）:**

审计主题：验证登录表单实现、apiLogin函数、前端登录逻辑、后端集成正确性

审计发现（3个问题）:
1. ❌ **showScreen索引冲突（阻塞）** - #screen-login包含.screen class导致业务页面索引偏移+1
   - 影响：doLogin调用showScreen(0)重新激活登录页而非学生申请页
2. ❌ **登录失败状态未清理** - apiLogin失败时未清除currentToken/currentUser
   - 影响：可能残留旧认证状态
3. ⚠️ **admin角色未处理** - updateUIForRole无admin分支
   - 判断：demo-web仅支持4个演示角色，admin不在范围

审计结论：集成逻辑正确但前端导航逻辑损坏，必须修复后才能通过

**问题修复（2026-06-07下午）:**

*修复showScreen索引冲突:*
- ✓ 将#screen-login的class从"screen"改为"login-screen"
- ✓ 新增.login-screen CSS样式保持显示行为一致
- ✓ 解决业务页面索引错位问题

*修复登录失败状态清理:*
- ✓ apiLogin在else分支和catch块中清除currentToken和currentUser
- ✓ 确保失败登录不残留认证状态

*admin角色处理:*
- ✓ 确认demo-web仅支持4个演示角色（student/dorm_manager/counselor/dean）
- ✓ admin角色不在demo-web范围，无需处理

**验证状态:**
- ✓ 后端API正常（curl测试通过）
- ✓ showScreen索引冲突已修复
- ✓ 登录失败状态清理已修复
- ⏳ 需浏览器手动测试验证完整登录流程

**演示账号:**
- 学生: 2020001 / 2020001
- 宿管员: M001 / M001
- 辅导员: T001 / T001
- 学工部: D001 / D001

**提交记录:**
- Commit: fix(demo-web): 修复登录流程DOM索引冲突和状态清理问题
- Files: demo-web/index.html, demo-web/js/api.js
- Changes: +12 insertions, -1 deletion

**下一步:**
- [ ] 浏览器测试登录流程（4个角色）
- [ ] 验证不同角色登录后显示正确UI
- [ ] Task #18: 实现动态时间线渲染
- [ ] 端到端集成测试
