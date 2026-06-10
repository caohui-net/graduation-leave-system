[RESPONSE_START]
{
  "consensus": true,
  "decision": "同意修复方向：demo-web不应再通过手动角色选择器切换身份，而应改为用户名/密码登录表单，调用现有POST /api/auth/login，由后端基于user_id/password验证并返回user.role，前端只根据返回的role切换UI。演示环境可继续使用简化密码规则（种子数据中密码等于user_id），但不应继续使用role参数登录作为主流程。",
  "blocking_issues": [],
  "reasoning": "我同意DISCUSS-DEMO-WEB登录设计缺陷修复-当前手动选择角色的方式不符合真实登录流程-1780841849-r2-codex的结论。最弱的旧假设是“demo-login(role)已经足够安全/真实”：它虽然比前端明文TestAccounts好，但仍允许用户声明角色，本质上不是认证。更稳妥的设计是把demo-web登录入口改为user_id/password表单，统一走现有auth_login契约；演示简化只体现在测试账号密码策略和种子数据，而不是体现在前端可选角色或后端按role发token。",
  "previous_responses": [
    "DISCUSS-DEMO-WEB登录设计缺陷修复-当前手动选择角色的方式不符合真实登录流程-1780841849-r2-codex"
  ],
  "targeted_challenges": [],
  "dissent": "历史实现曾为解决前端明文TestAccounts引入/api/auth/demo-login并用DEMO_AUTH_ENABLED守卫；这解决了部分安全问题，但与本轮“真实登录流程”的目标冲突。应明确把该历史方案降级为调试辅助，而不是demo-web产品流程。",
  "evidence": [
    "demo-web/index.html:313-321仍显示“演示角色”select，选项包含dorm_manager、student、counselor、dean。",
    "demo-web/index.html:525-557的switchRole(role)调用apiLogin(role)，再用roleMap/currentRole控制UI。",
    "demo-web/index.html:646-648页面加载时自动读取roleSelector并调用switchRole，默认无需用户名/密码即可进入某个角色。",
    "demo-web/js/api.js:12-19的apiLogin只提交{role: role}到/api/auth/demo-login。",
    "backend/apps/users/serializers.py:20-45的LoginSerializer已经按user_id/password验证用户，并返回access_token、token_type、user，其中user包含role。",
    "backend/apps/users/views.py:26-32提供login视图，backend/apps/users/urls.py:5注册path('login', views.login, name='login')，对应/api/auth/login。",
    "backend/apps/users/management/commands/seed_data.py为演示用户设置密码等于user_id，已经支持演示环境简化密码验证而不需要前端选择角色。"
  ],
  "action_items": [
    {
      "owner": "implementer",
      "task": "用user_id/password登录表单替换demo-web角色选择器，提交POST /api/auth/login，成功后保存access_token和user。",
      "due": "before implementation acceptance",
      "verification": "输入2020001/2020001返回student并显示学生申请表单；输入T001/T001或M001/M001返回审批角色并显示审批列表。"
    },
    {
      "owner": "implementer",
      "task": "重构前端角色状态：删除roleSelector、switchRole(role)、currentRole由控件赋值的路径，改为从login响应user.role派生UI。",
      "due": "before implementation acceptance",
      "verification": "源码中demo-web主流程不再调用apiLogin(role)或读取roleSelector；UI切换只读取currentUser.role。"
    },
    {
      "owner": "implementer",
      "task": "保留或清理demo-login端点需形成明确契约：若保留，必须默认禁用且不被demo-web登录页调用。",
      "due": "before release notes",
      "verification": "demo-web/js/api.js不再引用/auth/demo-login；生产/默认环境DEMO_AUTH_ENABLED=false时demo-login不可用于正常登录。"
    },
    {
      "owner": "tester",
      "task": "添加最小登录验收覆盖：学生账号、审批员账号、错误密码、禁用账号或不存在账号。",
      "due": "before concluding",
      "verification": "API测试验证/api/auth/login响应shape和错误状态；浏览器或轻量DOM测试验证不同role显示对应首屏。"
    }
  ]
}
[RESPONSE_END]
