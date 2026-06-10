001',
backend/apps/approvals/tests/test_state_machine.py:28:            password='T001
',
backend/apps/approvals/tests/test_state_machine.py:37:            password='M001
',
backend/apps/approvals/tests/test_state_machine.py:46:            password='D001
'
backend/apps/approvals/tests/test_state_machine.py:84:        self.client.force_
authenticate(user=self.counselor)
backend/apps/approvals/tests/test_state_machine.py:104:        self.client.force
_authenticate(user=self.counselor)
backend/apps/approvals/tests/test_state_machine.py:124:        self.client.force
_authenticate(user=self.counselor)
backend/apps/approvals/tests/test_state_machine.py:152:        self.client.force
_authenticate(user=self.dorm_manager)
docs/discussions/codex-review-2026-05-27/04-database-review.md:202:- 无`password
_setup_required`标志
docs/discussions/codex-review-2026-05-27/04-database-review.md:204:- 无`failed_l
ogin_attempts`计数器
docs/discussions/codex-review-2026-05-27/04-database-review.md:205:- 无`last_log
in_at`时间戳
docs/discussions/codex-review-2026-05-27/04-database-review.md:214:    password_
setup_required BOOLEAN DEFAULT FALSE COMMENT '需要设置密码',
docs/discussions/codex-review-2026-05-27/04-database-review.md:216:    failed_lo
gin_attempts INT DEFAULT 0 COMMENT '失败登录次数',
docs/discussions/codex-review-2026-05-27/04-database-review.md:217:    last_logi
n_at TIMESTAMP COMMENT '最后登录时间',
docs/discussions/codex-review-2026-05-27/04-database-review.md:218:    last_logi
n_ip VARCHAR(50) COMMENT '最后登录IP',
docs/discussions/codex-review-2026-05-27/04-database-review.md:220:    password_
changed_at TIMESTAMP COMMENT '密码修改时间',
docs/discussions/codex-review-2026-05-27/04-database-review.md:225:    CONSTRAIN
T chk_auth_method CHECK (
docs/discussions/codex-review-2026-05-27/04-database-review.md:226:        (pass
word_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
docs/acceptance/phase4c-demo-script.md:99:STUDENT_TOKEN=$(curl -s -X POST "$BASE
_URL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:101:  -d '{"user_id":"2020001","password"
:"2020001"}' \
docs/acceptance/phase4c-demo-script.md:189:T001_TOKEN=$(curl -s -X POST "$BASE_U
RL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:191:  -d '{"user_id":"T001","password":"T
001"}' \
docs/acceptance/phase4c-demo-script.md:237:DEAN_TOKEN=$(curl -s -X POST "$BASE_U
RL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:239:  -d '{"user_id":"D001","password":"D
001"}' \
docs/acceptance/phase4c-demo-script.md:283:T002_TOKEN=$(curl -s -X POST "$BASE_U
RL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:285:  -d '{"user_id":"T002","password":"T
002"}' \
docs/acceptance/phase4c-demo-script.md:361:STUDENT_TOKEN=$(curl -s -X POST "$BAS
E_URL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:363:  -d '{"user_id":"2020001","password"
:"2020001"}' \
docs/acceptance/phase4c-demo-script.md:390:T001_TOKEN=$(curl -s -X POST "$BASE_U
RL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:392:  -d '{"user_id":"T001","password":"T
001"}' \
docs/acceptance/phase4c-demo-script.md:406:DEAN_TOKEN=$(curl -s -X POST "$BASE_U
RL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:408:  -d '{"user_id":"D001","password":"D
001"}' \
docs/acceptance/phase4c-demo-script.md:427:T002_TOKEN=$(curl -s -X POST "$BASE_U
RL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:429:  -d '{"user_id":"T002","password":"T
002"}' \
docs/superpowers/plans/2026-05-27-implementation-plan.md:618:- 缓解：准备测试账
号用于开发
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:39:def setup_p
assword_for_wechat_user(user, password):
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:41:    if len(
password) < 8:
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:43:    if not
re.search(r'[A-Za-z]', password):
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:45:    if not
re.search(r'\d', password):
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:53:    user.se
t_password(password)
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:77:    if exis
ting_user.wechat_openid or not password:
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:81:    if not
existing_user.check_password(password):
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:131:`'status':
 'password_setup_required'` 在密码设置前返回token。
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:145:        's
cope': 'password_setup_only',  # 受限范围
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:152:        if
 request.auth.get('scope') == 'password_setup_only':
docs/acceptance/phase4c-known-issues.md:40:| 宿舍系统测试凭证 | 外部阻塞 | 无法
测试真实集成 | 用户提供测试账号 |
docs/acceptance/phase4c-acceptance-checklist.md:16:| JWT认证 | ✅ 通过 | `backen
d/apps/users/views.py:login` |
docs/acceptance/phase4c-acceptance-checklist.md:18:| 登录API（POST /api/auth/log
in） | ✅ 通过 | 测试通过 + smoke test步骤1 |
docs/acceptance/phase4c-acceptance-checklist.md:170:| login页面 | ✅ code-comple
te | `miniprogram/pages/login/` |
docs/acceptance/phase4c-acceptance-checklist.md:183:| 401处理 | ✅ 通过 | handle
Unauthorized |
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:85:    'scope':
 'password_setup_only',  # 只能设置密码
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:184:- password_
setup_required BOOLEAN
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:186:- failed_lo
gin_attempts INT
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:187:- last_logi
n_at TIMESTAMP
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:188:- last_logi
n_ip VARCHAR(50)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:190:- password_
changed_at TIMESTAMP
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:194:CONSTRAINT
chk_auth_method CHECK (
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:195:    (passwo
rd_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:160
:设计文档写“密码使用 bcrypt 加密存储”，requirements 也加入了 `bcrypt`。但 Django
 已有成熟 password hasher 体系，不建议自建 `password_hash` 字段和手写 bcrypt 流
程。建议：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:162
:- 使用 Django `AbstractUser`/`AbstractBaseUser` 的 `password` 字段
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:323
:- 对 `password`、`token`、`secret`、`key`、`authorization`、`verification_code`
 等字段统一遮蔽
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:541
:1. 用户模型选择：基于 Django password 体系，不自建 `password_hash`。
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:25:
 - 将添加：`/auth/wechat/bind`、`/auth/password/setup`
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:140:    p
assword_hash = models.CharField(max_length=255, null=True)
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:144:    p
assword_setup_required = models.BooleanField(default=False, help_text='需要设置
密码')
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:146:    f
ailed_login_attempts = models.IntegerField(default=0, help_text='失败登录次数')
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:147:    l
ast_login_at = models.DateTimeField(null=True, help_text='最后登录时间')
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:148:    l
ast_login_ip = models.CharField(max_length=50, null=True, help_text='最后登录IP'
)
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:150:    p
assword_changed_at = models.DateTimeField(null=True, help_text='密码修改时间')
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:174:
           check=models.Q(password_hash__isnull=False) | models.Q(wechat_openid_
_isnull=False),
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:175:
           name='chk_auth_method'
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:218:**Codex意见：** 主设计中 `users` 表有 `chk_auth_method` 约束，要求 `passwor
d_hash` 或 `wechat_openid` 非空；CSV预导入账号通常还没有密码或微信绑定，会被约束
挡住。
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:226:CONSTRAINT chk_auth_method CHECK (
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:227:    (password_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:233:2. 插入users表时：`password_hash=NULL, wechat_openid=NULL` → 违反约束，插入
失败
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:243:    password_hash VARCHAR(255),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:247:    password_setup_required BOOLEAN DEFAULT FALSE COMMENT '需要设置密码',
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:260:    CONSTRAINT chk_auth_method CHECK (
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:261:        (password_hash IS NOT NULL) OR
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:263:        (password_setup_required = true)
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:276:修正后的 `chk_auth_method` 允许三种认证状态：
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:277:1. `password_hash IS NOT NULL`：已设置密码
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:279:3. `password_setup_required = true`：预导入账号，待设置密码
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:290:            password_setup_required=True,  # 标记为待设置密码
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:300:def first_login(student_id, password):
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:305:        password_setup_required=True
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:312:    user.password_hash = hash_password(password)
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:313:    user.password_setup_required = False
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:322:def authenticate(username, password, role):
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:340:    if user.password_setup_required:
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:344:    if user.password_hash and check_password(password, user.password_hash):
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:442:- 修改 `chk_auth_method` 约束：增加 `password_setup_required` 条件
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
:469:3. ✅ 调整认证约束，增加password_setup_required支持CSV导入
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:115:
      conn_str = f"mysql+mysqldb://{db_config['user']}:{db_config['password']}@{
db_config['host']}:{db_config['port']}/{db_config['database']}"
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:117:
      conn_str = f"mssql+pyodbc://{db_config['user']}:{db_config['password']}@{d
b_config['host']}:{db_config['port']}/{db_config['database']}?driver=ODBC+Driver
+17+for+SQL+Server"
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:119:
      conn_str = f"oracle+cx_oracle://{db_config['user']}:{db_config['password']
}@{db_config['host']}:{db_config['port']}/{db_config['service_name']}"
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:170:('dorm
_db_config', '{"type":"mysql","host":"10.0.1.50","port":3306,"database":"dorm","
user":"readonly","password":"P@ssw0rd"}', 'integration', TRUE);
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:264:def bind_wech
at_to_account(student_id, wechat_openid, password):
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:268:    if not us
er or not user.check_password(password):
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:397:SENSITIVE_FIE
LDS = ['password', 'token', 'secret', 'api_key']
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:415:    'login_ip
': '10/minute',      # 每IP 10次/分钟
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:416:    'login_us
er': '5/5minute',    # 每用户 5次/5分钟
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:50
:**Codex指出：** onShow中非学生统一reLaunch到login，覆盖onLoad的角色矩阵
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:53
:- 当前逻辑：onLoad redirectTo approvals，onShow reLaunch login
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:63
:    wx.reLaunch({ url: '/pages/login/login' });
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:66
:  // 修改：按角色矩阵跳转，而非统一回login
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:92
:    wx.reLaunch({ url: '/pages/login/login' });
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:12
2:    wx.reLaunch({ url: '/pages/login/login' });
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:46:- ✅ 包
含password_setup_required, account_locked, failed_login_attempts
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:47:- ✅ 添
加Round 1的chk_auth_method约束
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:40:- password
_hash和wechat_openid都是nullable
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:61:CONSTRAINT
 chk_auth_method CHECK (
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:62:    (passw
ord_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:78:- 暴力破解
密码（/api/v1/auth/login无速率限制）
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:93:        'l
ogin': '5/minute',
docs/api/api-schema-todo.md:68:- 修复auth_login的200响应schema不匹配问题
docs/api/api-schema-todo.md:69:- 原问题：@extend_schema使用LoginSerializer（字段
：user_id, password），但运行时返回{access_token, token_type, user}
docs/api/api-schema-todo.md:99:- ✓ 修复login响应schema不匹配（LoginResponseSeria
lizer）
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:23:-
 Root cause: Tests use `/api/auth/login/` but route is `/api/auth/login` (no tra
iling slash)
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:93:-
 Fix Day 2 drift (login URL, mock, smoke): 30-60 min
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:127:
1. Fix login URL in tests (remove trailing slash)
docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.m
d:84:- Data backfill from authoritative source
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:2
1:- `test_application_flow`: 1 failure (404 on login)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:2
2:- `test_error_cases`: 5 errors (404 on login)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:2
3:- `test_rejection_flow`: 2 errors (404 on login)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:3
2:**Root Cause:** Tests use `/api/auth/login/` but route is `/api/auth/login` (n
o trailing slash)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:9
7:1. Fix login URL in all Week 1 Day 5 tests
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:9
8:   - Change `/api/auth/login/` to `/api/auth/login`
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:2
05:**YES.** I verified the test failures myself. 8 out of 12 tests are failing d
ue to login URL mismatch.
docs/操作说明书.md:132:3. 输入学号：2020001，密码：password123
docs/操作说明书.md:169:- 种子数据未包含宿管员测试账号
docs/操作说明书.md:173:宿管员功能在Demo Web中可正常使用（需先配置测试账号）
docs/操作说明书.md:213:1. 输入账号：counselor，密码：password123
docs/操作说明书.md:233:1. 输入账号：dean，密码：password123
docs/操作说明书.md:313:## 5. 测试账号
docs/操作说明书.md:315:### 5.1 默认测试账号
docs/操作说明书.md:378:- POST /api/auth/login - 用户登录
docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md:5
:**审查对象：** `15-claude-authorization-question.md`
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:22:1. Fix
login URL in all Week 1 Day 5 tests
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:23:   - Ch
ange `/api/auth/login/` to `/api/auth/login` (remove trailing slash)
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:183:- Root
 cause: Tests use `/api/auth/login/` but route is `/api/auth/login`
backend/apps/applications/tests/test_constraints.py:21:            password='202
0001',
backend/apps/applications/tests/test_constraints.py:31:            password='T00
1',
backend/apps/applications/tests/test_constraints.py:38:            password='M00
1',
backend/apps/applications/tests/test_constraints.py:56:        self.client.force
_authenticate(user=self.student)
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:19
:6. 修改login.ts添加角色路由
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:27
:**当前方案：** 先完整实现student-application页面（4个文件），最后修改login.ts路
由
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:34
:**替代方案A：** 先修改login.ts路由（添加条件判断但暂时注释），再实现页面，最后
取消注释
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:50
:    wx.reLaunch({ url: '/pages/login/login' });
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:58
:- 如果login.ts路由已正确实现，角色保护是否冗余？
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:60
:- 但如果login.ts路由有bug，角色保护会掩盖路由问题
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:62
:**替代方案A：** 先不实现角色保护，依赖login.ts路由，测试通过后再添加防御性保护
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:63
:**替代方案B：** 先实现角色保护，即使login.ts路由有bug也能防御
backend/apps/applications/tests/test_application_flow.py:19:            password
='2020001',
backend/apps/applications/tests/test_application_flow.py:31:            password
='T001',
backend/apps/applications/tests/test_application_flow.py:39:            password
='M001',
backend/apps/applications/tests/test_application_flow.py:47:            password
='D001',
backend/apps/applications/tests/test_application_flow.py:66:        response = s
elf.client.post('/api/auth/login', {
backend/apps/applications/tests/test_application_flow.py:68:            'passwor
d': '2020001'
backend/apps/applications/tests/test_application_flow.py:85:        response = s
elf.client.post('/api/auth/login', {
backend/apps/applications/tests/test_application_flow.py:87:            'passwor
d': 'M001'
backend/apps/applications/tests/test_application_flow.py:106:        response =
self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_application_flow.py:108:            'passwo
rd': 'T001'
docs/discussions/week3-direction-2026-05-30/06-consensus.md:28:2. 明确测试账号和
seed数据需求：
backend/apps/applications/tests/test_p0_fixes.py:2:from django.contrib.auth impo
rt get_user_model
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:21:3. **认证约束调整**：增加`password_setup_required`支持CSV预导入账号
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:335:INSERT INTO users (student_id, name, department, class_id, role, is_act
ive, password_setup_required, ...)
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:598:- 修改 `chk_auth_method` 约束：增加 `password_setup_required = true` 条
件
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v
2.md:725:4. ✅ 认证约束调整：支持CSV预导入账号（password_setup_required）
backend/apps/users/serializers.py:22:    password = serializers.CharField(write_
only=True)
backend/apps/users/serializers.py:26:        password = attrs.get('password')
backend/apps/users/serializers.py:33:        if not user.check_password(password
):
backend/apps/users/models.py:1:from django.contrib.auth.models import AbstractBa
seUser, PermissionsMixin, BaseUserManager
backend/apps/users/models.py:14:    def create_user(self, user_id, password=None
, **extra_fields):
backend/apps/users/models.py:18:        user.set_password(password)
backend/apps/users/models.py:22:    def create_superuser(self, user_id, password
=None, **extra_fields):
backend/apps/users/models.py:26:        return self.create_user(user_id, passwor
d, **extra_fields)
backend/apps/applications/tests/test_detail_permissions.py:16:        self.stude
nt1.set_password('2020001')
backend/apps/applications/tests/test_detail_permissions.py:20:        self.stude
nt2.set_password('2020002')
backend/apps/applications/tests/test_detail_permissions.py:25:        self.couns
elor1.set_password('T001')
backend/apps/applications/tests/test_detail_permissions.py:29:        self.couns
elor2.set_password('T002')
backend/apps/applications/tests/test_detail_permissions.py:33:        self.dorm_
manager1.set_password('M001')
backend/apps/applications/tests/test_detail_permissions.py:37:        self.dorm_
manager2.set_password('M002')
backend/apps/applications/tests/test_detail_permissions.py:42:        self.dean1
.set_password('D001')
backend/apps/applications/tests/test_detail_permissions.py:46:        self.dean2
.set_password('D002')
backend/apps/applications/tests/test_detail_permissions.py:55:        self.clien
t.force_authenticate(user=self.student1)
backend/apps/applications/tests/test_detail_permissions.py:65:        self.clien
t.force_authenticate(user=self.student2)
backend/apps/applications/tests/test_detail_permissions.py:72:        self.clien
t.force_authenticate(user=self.student1)
backend/apps/applications/tests/test_detail_permissions.py:82:        self.clien
t.force_authenticate(user=self.counselor2)
backend/apps/applications/tests/test_detail_permissions.py:89:        self.clien
t.force_authenticate(user=self.student1)
backend/apps/applications/tests/test_detail_permissions.py:99:        self.clien
t.force_authenticate(user=self.dean2)
backend/apps/users/views.py:10:    operation_id='auth_login',
backend/apps/users/views.py:27:def login(request):
backend/apps/applications/tests/test_error_cases.py:18:            password='202
0001',
backend/apps/applications/tests/test_error_cases.py:30:            password='202
0002',
backend/apps/applications/tests/test_error_cases.py:42:            password='202
0003',
backend/apps/applications/tests/test_error_cases.py:54:            password='T00
1',
backend/apps/applications/tests/test_error_cases.py:61:            password='M00
1',
backend/apps/applications/tests/test_error_cases.py:69:            password='D00
1',
backend/apps/applications/tests/test_error_cases.py:86:        response = self.c
lient.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:88:            'password': '
2020003'
backend/apps/applications/tests/test_error_cases.py:103:        response = self.
client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:105:            'password':
'2020001'
backend/apps/applications/tests/test_error_cases.py:131:        response = self.
client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:133:            'password':
'2020001'
backend/apps/applications/tests/test_error_cases.py:147:        response = self.
client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:149:            'password':
'2020002'
backend/apps/applications/tests/test_error_cases.py:160:        response = self.
client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:162:            'password':
'2020001'
backend/apps/applications/tests/test_error_cases.py:173:        response = self.
client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:175:            'password':
'2020001'
backend/apps/users/tests/test_xg_user_sync.py:3:from django.contrib.auth import
get_user_model
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:34:
1. `POST /api/auth/login`
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:46:
- Day 3-4新增HTTP路由：4个，不含Day 1-2已完成的login
backend/apps/users/tests/test_xg_user_client.py:227:            'msg': 'unauthor
ized',
backend/apps/users/tests/test_xg_user_client.py:235:        self.assertEqual(res
ult['msg'], 'unauthorized')
backend/apps/users/tests/test_import_csv.py:14:        User.objects.create_user(
user_id='T001', name='李老师', role=UserRole.COUNSELOR, password='T001', departm
ent='计算机学院')
backend/apps/users/tests/test_import_csv.py:15:        User.objects.create_user(
user_id='T002', name='王老师', role=UserRole.COUNSELOR, password='T002', departm
ent='软件学院')
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:108:**建议：**
统一为"5个HTTP路由（login + 4个业务端点）"或"4个业务API端点"
backend/apps/applications/tests/test_list_permissions.py:15:        self.student
1.set_password('S001')
backend/apps/applications/tests/test_list_permissions.py:19:        self.student
2.set_password('S002')
backend/apps/applications/tests/test_list_permissions.py:23:        self.counsel
or1.set_password('T001')
backend/apps/applications/tests/test_list_permissions.py:27:        self.counsel
or2.set_password('T002')
backend/apps/applications/tests/test_list_permissions.py:31:        self.dorm_ma
nager1.set_password('M001')
backend/apps/applications/tests/test_list_permissions.py:35:        self.dorm_ma
nager2.set_password('M002')
backend/apps/applications/tests/test_list_permissions.py:39:        self.dean.se
t_password('D001')
backend/apps/applications/tests/test_list_permissions.py:78:        self.client.
force_authenticate(user=self.student1)
backend/apps/applications/tests/test_list_permissions.py:85:        self.client.
force_authenticate(user=self.student1)
backend/apps/applications/tests/test_list_permissions.py:91:        self.client.
force_authenticate(user=self.counselor1)
backend/apps/applications/tests/test_list_permissions.py:98:        self.client.
force_authenticate(user=self.counselor2)
backend/apps/applications/tests/test_list_permissions.py:103:        self.client
.force_authenticate(user=self.dean)
backend/apps/applications/tests/test_list_permissions.py:110:        self.client
.force_authenticate(user=self.student1)
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:46:- Secti
on 4.1 POST /api/auth/login添加说明
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:70:1. **We
ek 1 Day 3-4交付物：** 需要确认是否应该从"4个API端点"改为"5个API端点"（包含login
）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:28:
  1. POST /api/auth/login
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:70:
- 在contract-v0.1.md Section 4.1 POST /api/auth/login添加说明
backend/apps/users/urls.py:5:    path('login', views.login, name='login'),
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:54:   -
建议：后续统一为"5个HTTP路由（login + 4个业务端点）"
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:76:- API
端点（5个HTTP路由：login + submit + query + approve + reject）
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:
61:| 认证 | login_id、role、access_token mock/JWT格式 | 微信OAuth |
backend/apps/users/migrations/0001_initial.py:13:        ('auth', '0012_alter_us
er_first_name_max_length'),
backend/apps/users/migrations/0001_initial.py:20:                ('password', mo
dels.CharField(max_length=128, verbose_name='password')),
backend/apps/users/migrations/0001_initial.py:21:                ('last_login',
models.DateTimeField(blank=True, null=True, verbose_name='last login')),
backend/apps/users/migrations/0001_initial.py:33:                ('groups', mode
ls.ManyToManyField(blank=True, help_text='The groups this user belongs to. A use
r will get all permissions granted to each of their groups.', related_name='user
_set', related_query_name='user', to='auth.group', verbose_name='groups')),
backend/apps/users/migrations/0001_initial.py:34:                ('user_permissi
ons', models.ManyToManyField(blank=True, help_text='Specific permissions for thi
s user.', related_name='user_set', related_query_name='user', to='auth.permissio
n', verbose_name='user permissions')),
backend/apps/users/services/xg_user_sync.py:3:from django.contrib.auth import ge
t_user_model
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:90:-
错误分类：`config_error`、`sign_error`、`network_error`、`http_error`、`auth_fai
led`、`tenant_invalid`、`business_error`、`unexpected_schema`。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:108:
请求摘要: POST auth-user-info page=1 pageNum=1 encryptionType=sha1 sign=present
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:
16:2. 发现P1级schema fidelity问题（login响应不匹配）
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:
31:- `LoginSerializer`定义在`backend/apps/users/serializers.py`，字段：`user_id`
（write_only）+ `password`（write_only）
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:
47:1. 修复login响应schema（15分钟）
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:
90:**Step 1：修复login响应schema（15分钟）**
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:
124:> 下一步执行Option A-prime：主动关闭API Schema P1验收门禁。首先修复login成功
响应schema不匹配（创建LoginResponseSerializer），然后在可用Django环境中验证schem
a生成无警告、schema/swagger-ui可访问、operationId唯一。只有P1真实绿灯后，再执行
收敛版P2（为关键端点补OpenApiExample）。如果当前环境无法完成P1验证，则硬停止并将
P1状态标记为"代码完成，未验收"，等待可验证环境。
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:
132:**下一步：** 立即执行Step 1（修复login响应schema）。
backend/apps/users/management/commands/seed_data.py:55:                user.set_
password(student_data['user_id'])
backend/apps/users/management/commands/seed_data.py:76:                user.set_
password(counselor_data['user_id'])
backend/apps/users/management/commands/seed_data.py:98:                user.set_
password(dm_data['user_id'])
backend/apps/users/management/commands/seed_data.py:112:            user.set_pas
sword('D001')
docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:37:-
小程序骨架完成（login/student-application/approvals/detail）
docs/discussions/phase4c-next-steps/34-claude-authorization-interpretation-reque
st.md:82:1. **Codex的明确警告** - event 88中Codex强调"do_not_start_phase1_withou
t_explicit_authorization"
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:109
:2. **业务字段层：** 宽松采样，记录 `name/number/phone/identity_id/department/us
er_identity/user_auth_extra_field` 是否出现，不因业务字段缺失直接失败。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:125
:请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:174
:- `auth_failed`
docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-respon
se.md:5:**针对文档：** `docs/discussions/phase4c-next-steps/34-claude-authorizat
ion-interpretation-request.md`
docs/discussions/phase4c-next-steps/54-claude-codex-consensus-option-a-execution
.md:29:- 重点：login路径/响应、notification分页、attachment wrapper、错误envelop
e
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:49:
- 当前路由是`/api/auth/login`（无尾斜杠）
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:57:
- 分别记录DRF默认auth错误
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:71:
- DRF默认auth错误单独记录
backend/apps/users/management/commands/import_csv.py:104:
     user.set_password(row.get('password', student_id))
backend/apps/users/management/commands/import_csv.py:163:
     user.set_password(row.get('password', employee_id))
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-reque
st.md:242:    this.config.onUnauthorized?.();
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-reque
st.md:243:    reject(new Error('Unauthorized'));
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-respon
se.md:82:设置 `attachmentError`，并区分“暂无附件”和“附件加载失败”。401仍交给 `Ap
iClient.onUnauthorized`；其他错误至少显示 `formatApiError(err)` 或 `err.error?.m
essage || '附件加载失败'`。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-respon
se.md:89:`wx.downloadFile` 对非200统一显示“下载失败”。如果token过期返回401，当前
不会执行 `onUnauthorized`，用户停留在详情页且无法恢复。
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-re
sponse.md:16:另外，静态检查已经发现一个P1级schema fidelity风险：`backend/apps/us
ers/views.py` 的登录成功响应使用 `LoginSerializer` 作为200响应schema，但运行时返
回的是 `access_token`、`token_type`、`user`，不是 `LoginSerializer` 声明的 `user
_id`/`password` 字段形状。这个问题属于P1准确性，不应推迟到P2示例阶段。
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-re
sponse.md:45:- 修复静态已知的login成功响应schema。
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-re
sponse.md:53:   - 修复login response schema mismatch。
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-re
sponse.md:92:- `LoginSerializer` 声明字段是 `user_id` 和 `password`。
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-re
sponse.md:108:> 下一步不直接执行API Schema P2。先执行Option A-prime：主动关闭API
 Schema P1验收门禁，修复已发现的login成功响应schema不匹配，并在可用Django环境中
验证schema生成无警告、schema/swagger-ui可访问、operationId唯一。只有P1真实绿灯后
，再执行一个收敛版P2，为登录、申请提交、审批操作、通知列表和通用错误补OpenApiExa
mple。如果当前环境无法完成P1验证，则硬停止并将P1状态标记为“代码完成，未验收”，等
待可验证环境。
backend/apps/notifications/services.py:8:from django.contrib.auth import get_use
r_model
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-str
ategy-response.md:102:- auth、applications、approvals、attachments、notification
s端点出现在schema中。
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.m
d:54:当前实现还需要补一个小缺口：前序共识要求错误分类包含 `tenant_invalid`，但 `
live_probe()` 现在只把 `401/403` 归为 `auth_failed`，其他业务码统一归为 `busines
s_error`。如果平台返回租户错误码或错误文本，应在诊断层单独归类为 `tenant_invalid
`，便于排障。
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md
:118:        wx.reLaunch({ url: '/pages/login/login' });
docs/discussions/phase4c-next-steps/59-claude-codex-final-consensus-option-2.md:
15:1. Option A-prime已部分完成（login响应schema修复）
docs/discussions/phase4c-next-steps/59-claude-codex-final-consensus-option-2.md:
46:- 已完成：6项P1修复（含login响应schema）
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md
:48:4. 保留login响应schema修复为已完成代码项
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:31:The plan describes `/api/auth/login/` and a token response containing a re
fresh token. The current route is `path('login', ...)`, so the canonical route i
s `/api/auth/login` without a trailing slash. The current login serializer retur
ns `access_token`, `token_type`, and `user`; it does not return `refresh_token`.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:33:The error shape also differs from the rest of the API: invalid login curre
ntly returns raw serializer errors from `serializer.errors`, not the project err
or envelope.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:35:**Required adjustment:** document the current route and response exactly,
or intentionally change the login behavior with tests. Do not publish an OpenAPI
 response that claims a refresh token or uniform error envelope unless the code
is changed to match.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:39:### P1 - Uniform `ErrorSerializer` can make the schema lie unless auth/fra
mework errors are handled
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:49:But serializer errors and DRF/framework-level errors are not uniformly wra
pped everywhere. In particular, login validation errors currently return raw ser
ializer errors, and unauthenticated `401` responses are produced by DRF authenti
cation before view code runs.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:53:- **Documentation-only approach:** use `ErrorSerializer` only for endpoint
s and status codes that actually return the project envelope; document DRF defau
lt auth errors separately.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:54:- **Behavioral approach:** add a global exception/authentication error han
dler and update tests so framework errors also use the project envelope.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:56:For this phase, I recommend the documentation-only approach unless the use
r explicitly authorizes an API behavior normalization pass.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:128:Pay special attention to login path/response, notification pagination, at
tachment wrapper shape, and error envelopes.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:184:   Yes: login schema mismatch, raw login errors, framework `401` error sh
ape, multi-method dispatcher schemas, notification pagination shape, attachment
module ownership, and imprecise warning acceptance.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:187:   Execute **B-mini + A-corrected**. Fix the smoke typo first, then do a
schema-fidelity pass. Do not broaden into new notification features or Celery wo
rk until external blockers and explicit user authorization are resolved.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:198:- Document auth/login and notification pagination accurately.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.
md:199:- Treat uniform error schema as documentation-only for view-level errors
unless a global error-envelope behavior change is authorized.
backend/apps/attachments/tests/test_list.py:18:            password='2020001',
backend/apps/attachments/tests/test_list.py:30:            password='2020002',
backend/apps/attachments/tests/test_list.py:43:            password='T001',
backend/apps/attachments/tests/test_list.py:51:            password='T002',
backend/apps/attachments/tests/test_list.py:60:            password='D001',
backend/apps/attachments/tests/test_list.py:105:        self.client.force_authen
ticate(user=self.student)
backend/apps/attachments/tests/test_list.py:117:        self.client.force_authen
ticate(user=self.other_student)
backend/apps/attachments/tests/test_list.py:128:        self.client.force_authen
ticate(user=self.counselor)
backend/apps/attachments/tests/test_list.py:139:        self.client.force_authen
ticate(user=self.other_counselor)
backend/apps/attachments/tests/test_list.py:150:        self.client.force_authen
ticate(user=self.dean)
backend/apps/attachments/tests/test_list.py:165:        self.client.force_authen
ticate(user=self.student)
backend/apps/attachments/tests/test_delete.py:18:            password='2020001',
backend/apps/attachments/tests/test_delete.py:30:            password='2020002',
backend/apps/attachments/tests/test_delete.py:43:            password='T001',
backend/apps/attachments/tests/test_delete.py:83:        self.client.force_authe
nticate(user=self.student)
backend/apps/attachments/tests/test_delete.py:98:        self.client.force_authe
nticate(user=self.other_student)
backend/apps/attachments/tests/test_delete.py:113:        self.client.force_auth
enticate(user=self.counselor)
backend/apps/attachments/tests/test_delete.py:127:        self.client.force_auth
enticate(user=self.student)
backend/apps/attachments/tests/test_download.py:19:            password='2020001
',
backend/apps/attachments/tests/test_download.py:31:            password='2020002
',
backend/apps/attachments/tests/test_download.py:44:            password='T001',
backend/apps/attachments/tests/test_download.py:84:        self.client.force_aut
henticate(user=self.student)
backend/apps/attachments/tests/test_download.py:95:        self.client.force_aut
henticate(user=self.counselor)
backend/apps/attachments/tests/test_download.py:104:        """Unauthorized stud
ent cannot download attachment"""
backend/apps/attachments/tests/test_download.py:105:        self.client.force_au
thenticate(user=self.other_student)
backend/apps/attachments/tests/test_download.py:119:        self.client.force_au
thenticate(user=self.student)
docs/discussions/phase4c-next-steps/58-claude-codex-consensus-option-a-prime-par
tial.md:15:- ✅ Step 1完成：修复login响应schema不匹配
docs/discussions/phase4c-next-steps/58-claude-codex-consensus-option-a-prime-par
tial.md:25:**问题：** `backend/apps/users/views.py`的login视图200响应schema不匹
配
docs/discussions/phase4c-next-steps/58-claude-codex-consensus-option-a-prime-par
tial.md:26:- 文档：使用`LoginSerializer`（字段：user_id, password）
docs/discussions/phase4c-next-steps/58-claude-codex-consensus-option-a-prime-par
tial.md:139:> Option A-prime部分完成：login响应schema不匹配已修复，但环境验证受
阻（psycopg2-binary安装失败）。P1状态标记为"代码完成，未验收"。不建议继续P2，等
待可验证环境或接受当前状态继续其他工作。
backend/apps/attachments/tests/test_upload.py:18:            password='2020001',
backend/apps/attachments/tests/test_upload.py:31:            password='2020002',
backend/apps/attachments/tests/test_upload.py:44:            password='T001',
backend/apps/attachments/tests/test_upload.py:82:        self.client.force_authe
nticate(user=self.student)
backend/apps/attachments/tests/test_upload.py:104:        self.client.force_auth
enticate(user=self.student)
backend/apps/attachments/tests/test_upload.py:121:        self.client.force_auth
enticate(user=self.counselor)
backend/apps/attachments/tests/test_upload.py:138:        self.client.force_auth
enticate(user=self.student)
backend/apps/attachments/tests/test_upload.py:155:        self.client.force_auth
enticate(user=self.student)
docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md:6
5:**小风险：** 判断顺序问题 - `401/403`会优先归为`auth_failed`，即使`msg`里包含`
tenant`或`租户`。如果平台把租户无效包装成403，会被误分类。
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.m
d:88:- Download handling now branches on 401/403/404/200 and calls centralized u
nauthorized handling for 401.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:120:-
 Re-launch/login/token expiration behavior still works.
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:1
98:- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感
参数。
docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md:3
0:- 在auth_failed (401/403)之后增加租户错误判断
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:106:
     wx.reLaunch({ url: '/pages/login/login' });
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.m
d:180:   - auth_failed：业务code=401/403
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:91:ha
ndleUnauthorized() {
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:92:
this.config.onUnauthorized?.();
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:101:-
 401: 调用 `apiClient.handleUnauthorized()` 统一处理
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:191:1
. `miniprogram/services/api.ts` - 新增 `handleUnauthorized()` 方法
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:238:
  - `apiClient.handleUnauthorized()` 调用是否正确？
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.m
d:164:- 按模块分组（auth/applications/approvals/notifications/attachments）
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.m
d:174:**任务2.1：auth模块（15分钟）**
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.m
d:175:- /api/auth/login/ - 添加@extend_schema
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:2
1:URL: https://xuegongmj.hgnu.edu.cn/api/open-api/user-center/tenant/auth-user-i
nfo
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:93:请求
文档中的401处理逻辑与 `createDefaultApiClient()` 的 `onUnauthorized` 当前实现一
致，功能上可用。但把同一段清token和跳转逻辑复制到页面，会让后续登录状态清理发生
漂移。
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:96:优先
在 `ApiClient` 内增加一个下载专用方法，或至少增加公开的 `handleUnauthorized()`
方法供页面复用。MVP最小方案：
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:99:hand
leUnauthorized() {
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:100:  t
his.config.onUnauthorized?.();
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:104:然
后页面下载401分支调用 `apiClient.handleUnauthorized()`。
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:91:
  handleUnauthorized() {
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:92:
    this.config.onUnauthorized?.();
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:110
:        apiClient.handleUnauthorized();
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:235
:- 增加 `handleUnauthorized()` 公开方法
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:238
:- 修改 `onDownloadAttachment()` 调用 `apiClient.handleUnauthorized()`
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:289
:3. Step 3: ApiClient.handleUnauthorized + 下载状态码
docs/discussions/phase4c-next-steps/89-claude-response-agree-fixes.md:146:**Clau
de确认：** 同意。当前顺序会导致`{'code': 403, 'msg': '租户不存在'}`被归为`auth_f
ailed`而非`tenant_invalid`。
docs/discussions/phase4c-next-steps/89-claude-response-agree-fixes.md:153:    re
turn {'status': 'ERROR', 'error': 'auth_failed', ...}
docs/discussions/phase4c-next-steps/89-claude-response-agree-fixes.md:163:    re
turn {'status': 'ERROR', 'error': 'auth_failed', ...}
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md
:102:1. 使用用户提供的生产URL: `https://xuegongmj.hgnu.edu.cn/api/open-api/user-
center/tenant/auth-user-info`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md
:179:XG_USER_API_URL=https://xuegongmj.hgnu.edu.cn/api/open-api/user-center/tena
nt/auth-user-info
docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:3
0:**Codex指出：** `live_probe()` 现在只把401/403归为`auth_failed`，其他业务码统
一归为`business_error`，缺少`tenant_invalid`分类。
docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:3
8:    return {'status': 'ERROR', 'error': 'auth_failed', ...}
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-res
ponse.md:57:- 保留login响应schema修复为已完成代码项。
backend/apps/notifications/tests/test_auto_notifications_api.py:10:from django.c
ontrib.auth import get_user_model
backend/apps/notifications/tests/test_auto_notifications_api.py:64:        self.
client.force_authenticate(user=self.student)
backend/apps/notifications/tests/test_auto_notifications_api.py:73:        self.
client.force_authenticate(user=self.dorm_manager)
backend/apps/notifications/tests/test_auto_notifications_api.py:106:        self
.client.force_authenticate(user=self.counselor)
backend/apps/notifications/tests/test_auto_notifications_api.py:113:        self
.client.force_authenticate(user=self.student)
backend/apps/notifications/tests/test_auto_notifications_api.py:148:        self
.client.force_authenticate(user=self.counselor)
backend/apps/notifications/tests/test_auto_notifications_api.py:155:        self
.client.force_authenticate(user=self.student)
backend/apps/notifications/tests/test_auto_notifications_api.py:195:        self
.client.force_authenticate(user=student2)
backend/apps/notifications/tests/test_auto_notifications_api.py:230:        self
.client.force_authenticate(user=self.counselor)
backend/apps/notifications/tests/test_auto_notifications_api.py:256:        self
.client.force_authenticate(user=blocked_student)
backend/apps/notifications/tests/test_timeout_warnings.py:4:from django.contrib.
auth import get_user_model
backend/apps/notifications/tests/test_api.py:48:        self.client.force_authen
ticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:75:        self.client.force_authen
ticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:98:        self.client.force_authen
ticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:126:        self.client.force_authe
nticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:150:        self.client.force_authe
nticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:167:        self.client.force_authe
nticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:187:        self.client.force_authe
nticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:208:        self.client.force_authe
nticate(user=self.student2)
backend/apps/notifications/tests/test_api.py:216:        self.client.force_authe
nticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:241:        self.client.force_authe
nticate(user=self.student1)
backend/apps/notifications/tests/test_auto_notifications.py:13:from django.contr
ib.auth import get_user_model

codex
The broad search confirms there are many documented and test credentials, but th
e web demo surface is the key decision point. I’m narrowing to the frontend impl
ementation and auth service now.
exec
/bin/bash -lc 'rtk rg --files frontend demo-web web src 2>/dev/null' in /home/ca
ohui/projects/graduation-leave-system
 exited 2 in 0ms:
demo-web/js/api.js
demo-web/index.html
demo-web/IMPLEMENTATION_NOTES.md
demo-web/css/global.css
frontend/services/mock.ts
frontend/services/api.ts
frontend/types/api.ts

exec
/bin/bash -lc "rtk rg -n \"TEST|TestAccounts|accounts|role|switchRole|apiLogin|l
ogin|access_token|localStorage|sessionStorage\" frontend demo-web web src --glob
 '"'!node_modules'"' --glob '"'!dist'"' --glob '"'!build'"'" in /home/caohui/pro
jects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,220p' backend/apps/users/views.py && rtk sed -n '1,
220p' backend/apps/users/serializers.py && rtk sed -n '1,80p' backend/apps/users
/urls.py" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,220p' frontend/services/api.ts" in /home/caohui/pro
jects/graduation-leave-system
 succeeded in 0ms:
// API Client for v0.2 Contract
// Minimal implementation - can be extended

import type {
  LoginRequest,
  LoginResponse,
  ApplicationCreateRequest,
  ApplicationDetail,
  Application,
  ApprovalListItem,
  ApprovalActionRequest,
  ApprovalActionResponse,
  PaginatedResponse,
  ApiError,
} from '../types/api';

export interface ApiConfig {
  baseUrl: string;
  getToken?: () => string | null;
  onUnauthorized?: () => void;
}

export class ApiClient {
  private config: ApiConfig;

  constructor(config: ApiConfig) {
    this.config = config;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.config.getToken?.();
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.config.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      this.config.onUnauthorized?.();
      throw new Error('Unauthorized');
    }

    const data = await response.json();

    if (!response.ok) {
      throw data as ApiError;
    }

    return data as T;
  }

  // Auth
  async login(req: LoginRequest): Promise<LoginResponse> {
    return this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(req),
    });
  }

  // Applications
  async createApplication(req: ApplicationCreateRequest): Promise<ApplicationDet
ail> {
    return this.request('/api/applications/', {
      method: 'POST',
      body: JSON.stringify(req),
    });
  }

  async listApplications(
    limit = 20,
    offset = 0
  ): Promise<PaginatedResponse<Application>> {
    return this.request(
      `/api/applications/?limit=${limit}&offset=${offset}`
    );
  }

  async getApplication(id: string): Promise<ApplicationDetail> {
    return this.request(`/api/applications/${id}/`);
  }

  // Approvals
  async listApprovals(
    decision: 'pending' | 'approved' | 'rejected' | 'all' = 'pending',
    limit = 20,
    offset = 0
  ): Promise<PaginatedResponse<ApprovalListItem>> {
    return this.request(
      `/api/approvals/?decision=${decision}&limit=${limit}&offset=${offset}`
    );
  }

  async approveApproval(
    id: string,
    req: ApprovalActionRequest
  ): Promise<ApprovalActionResponse> {
    return this.request(`/api/approvals/${id}/approve/`, {
      method: 'POST',
      body: JSON.stringify(req),
    });
  }

  async rejectApproval(
    id: string,
    req: ApprovalActionRequest
  ): Promise<ApprovalActionResponse> {
    return this.request(`/api/approvals/${id}/reject/`, {
      method: 'POST',
      body: JSON.stringify(req),
    });
  }
}

 exited 2 in 103ms:
 succeeded in 157ms:
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'role', 'class_id', 'active', 'is_graduatin
g', 'graduation_year']
        read_only_fields = ['user_id']


class AuthUserSerializer(serializers.ModelSerializer):
    """登录响应中的用户摘要（UserDTO子集）"""
    class Meta:
        model = User
        fields = ['user_id', 'name', 'role', 'class_id']


class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        password = attrs.get('password')

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')

        if not user.active:
            raise serializers.ValidationError('Account is inactive')

        refresh = RefreshToken.for_user(user)

        return {
            'access_token': str(refresh.access_token),
            'token_type': 'Bearer',
            'user': AuthUserSerializer(user).data
        }


class LoginResponseSerializer(serializers.Serializer):
    """登录成功响应（schema-only，用于OpenAPI文档）"""
    access_token = serializers.CharField(help_text="JWT access token")
    token_type = serializers.CharField(default='Bearer', help_text="Token type")
    user = AuthUserSerializer(help_text="用户信息")
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
]

codex
I have enough to form a position, but I’ll grab line-numbered snippets for the e
xact evidence fields.
exec
/bin/bash -lc "rtk nl -ba demo-web/index.html | rtk sed -n '250,520p'" in /home/
caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk nl -ba demo-web/js/api.js | rtk sed -n '1,120p'" in /home/cao
hui/projects/graduation-leave-system
 succeeded in 0ms:
   250      }
   251      .screen.active {
   252        display: block;
   253      }
   254    </style>
   255  </head>
   256  <body>
   257    <!-- 顶部导航 -->
   258    <div class="nav-tabs">
   259      <button class="nav-tab active" onclick="showScreen(0)">学生申请</but
ton>
   260      <button class="nav-tab" onclick="showScreen(1)"><span id="nav-approv
al-text">审批列表</span></button>
   261      <button class="nav-tab" onclick="showScreen(2)">申请详情</button>
   262    </div>
   263
   264    <!-- 角色选择器 -->
   265    <div style="background: white; padding: 8px 16px; border-bottom: 1px s
olid #f0f0f0; display: flex; align-items: center; gap: 10px;">
   266      <span style="font-size: 14px; color: #666;">演示角色:</span>
   267      <select id="roleSelector" onchange="switchRole(this.value)" style="p
adding: 4px 8px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;
">
   268        <option value="dorm_manager">宿管员</option>
   269        <option value="student">学生</option>
   270        <option value="counselor">辅导员</option>
   271        <option value="dean">学工部</option>
   272      </select>
   273    </div>
   274
   275    <!-- 屏幕1: 学生申请页 -->
   276    <div class="screen active" id="screen-0">
   277      <div style="padding: 20px;">
   278        <!-- 用户信息卡片 -->
   279        <div class="card" style="margin-bottom: 20px;">
   280          <div style="font-size: 16px; font-weight: 600; color: var(--prim
ary-color); margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid
#f0f0f0;">
   281            申请人信息
   282          </div>
   283          <div style="display: flex; align-items: center; padding: 10px 0;
">
   284            <span style="font-size: 14px; color: #666; width: 80px;">姓名<
/span>
   285            <span style="font-size: 14px; color: #333;">张三</span>
   286          </div>
   287          <div style="display: flex; align-items: center; padding: 10px 0;
">
   288            <span style="font-size: 14px; color: #666; width: 80px;">学号<
/span>
   289            <span style="font-size: 14px; color: #333;">2020001</span>
   290          </div>
   291        </div>
   292
   293        <!-- 表单卡片 -->
   294        <div class="card">
   295          <div style="margin-bottom: 20px;">
   296            <label style="display: block; font-size: 14px; margin-bottom:
8px; font-weight: 500;">联系电话</label>
   297            <input id="contactPhone" type="tel" name="contact_phone" maxle
ngth="20" inputmode="numeric" style="width: 100%; padding: 12px; border: 1px sol
id #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入联系电话" r
equired>
   298          </div>
   299          <div style="margin-bottom: 20px;">
   300            <label style="display: block; font-size: 14px; margin-bottom:
8px; font-weight: 500;">离校原因</label>
   301            <textarea id="applicationReason" style="width: 100%; min-heigh
t: 120px; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-siz
e: 14px;" placeholder="请输入离校原因"></textarea>
   302            <span style="display: block; text-align: right; font-size: 12p
x; color: #999; margin-top: 4px;">0/500</span>
   303          </div>
   304          <div style="margin-bottom: 20px;">
   305            <label style="display: block; font-size: 14px; margin-bottom:
8px; font-weight: 500;">离校日期</label>
   306            <input id="leaveDate" type="date" name="leave_date" style="wid
th: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-siz
e: 14px;" required>
   307          </div>
   308
   309          <!-- 附件上传区域 -->
   310          <div style="margin-bottom: 20px;">
   311            <label style="display: block; font-size: 14px; margin-bottom:
8px; font-weight: 500;">附件材料（可选）</label>
   312            <div class="upload-zone">
   313              <input type="file" id="fileInput" multiple accept=".jpg,.jpe
g,.png,.pdf,.doc,.docx" style="display: none;">
   314              <div class="upload-area" onclick="document.getElementById('f
ileInput').click()">
   315                <div style="font-size: 40px; color: #999; margin-bottom: 8
px;">📎</div>
   316                <div style="font-size: 14px; color: #666;">点击或拖拽文件
到此处上传</div>
   317                <div style="font-size: 12px; color: #999; margin-top: 4px;
">支持jpg/png/pdf/doc/docx，单文件不超过10MB</div>
   318              </div>
   319            </div>
   320            <!-- 文件列表 -->
   321            <div id="fileList" style="margin-top: 12px;"></div>
   322          </div>
   323
   324          <button class="btn-primary" onclick="doSubmitApplication()">提交
申请</button>
   325        </div>
   326      </div>
   327    </div>
   328
   329    <!-- 屏幕2: 审批列表页 -->
   330    <div class="screen" id="screen-1">
   331      <div style="background: white; padding: 16px; display: flex; justify
-content: space-between; align-items: center;">
   332        <div style="font-size: 18px; font-weight: bold;" id="list-title">
审批列表</div>
   333        <div style="font-size: 12px; color: #999;" id="role-display">宿管
员</div>
   334      </div>
   335
   336      <!-- Tab切换 -->
   337      <div style="background: white; display: flex; border-bottom: 1px sol
id #f0f0f0;">
   338        <div class="nav-tab active" style="flex: 1;">全部</div>
   339        <div class="nav-tab" style="flex: 1;">待审批</div>
   340        <div class="nav-tab" style="flex: 1;">已审批</div>
   341      </div>
   342
   343      <div style="padding: 10px;">
   344        <!-- 列表项 -->
   345        <div class="card">
   346          <div class="flex-row justify-between align-center" style="margin
-bottom: 8px;">
   347            <span style="font-size: 16px; font-weight: bold;">申请 APP-001
</span>
   348            <span class="tag tag-pending">待审批</span>
   349          </div>
   350          <div style="margin-bottom: 4px;">
   351            <span style="font-size: 14px; color: #999; margin-right: 8px;"
>申请ID:</span>
   352            <span style="font-size: 14px; color: #333;">APP-001</span>
   353          </div>
   354          <div style="margin-bottom: 4px;">
   355            <span style="font-size: 14px; color: #999; margin-right: 8px;"
>审批步骤:</span>
   356            <span style="font-size: 14px; color: #333;">宿管员审批</span>
   357          </div>
   358          <div style="margin-top: 8px; padding-top: 8px; border-top: 1px s
olid #f0f0f0;">
   359            <span style="font-size: 12px; color: #999;">2024-06-01 10:30</
span>
   360          </div>
   361        </div>
   362
   363        <div class="card">
   364          <div class="flex-row justify-between align-center" style="margin
-bottom: 8px;">
   365            <span style="font-size: 16px; font-weight: bold;">申请 APP-002
</span>
   366            <span class="tag tag-approved">已通过</span>
   367          </div>
   368          <div style="margin-bottom: 4px;">
   369            <span style="font-size: 14px; color: #999; margin-right: 8px;"
>申请ID:</span>
   370            <span style="font-size: 14px; color: #333;">APP-002</span>
   371          </div>
   372          <div style="margin-bottom: 4px;">
   373            <span style="font-size: 14px; color: #999; margin-right: 8px;"
>审批步骤:</span>
   374            <span style="font-size: 14px; color: #333;">辅导员审批</span>
   375          </div>
   376          <div style="margin-top: 8px; padding-top: 8px; border-top: 1px s
olid #f0f0f0;">
   377            <span style="font-size: 12px; color: #999;">2024-05-30 14:20</
span>
   378          </div>
   379        </div>
   380      </div>
   381    </div>
   382
   383    <!-- 屏幕3: 申请详情页 -->
   384    <div class="screen" id="screen-2">
   385      <div style="background: white; padding: 16px;">
   386        <div style="font-size: 18px; font-weight: bold;">申请详情</div>
   387      </div>
   388
   389      <div style="padding: 10px;">
   390        <!-- 基本信息 -->
   391        <div class="card">
   392          <div style="font-size: 16px; font-weight: bold; margin-bottom: 1
0px;">基本信息</div>
   393          <div style="display: flex; margin-bottom: 8px;">
   394            <span style="font-size: 14px; color: #999; width: 80px;">申请I
D:</span>
   395            <span style="font-size: 14px; color: #333; flex: 1;">APP-001</
span>
   396          </div>
   397          <div style="display: flex; margin-bottom: 8px;">
   398            <span style="font-size: 14px; color: #999; width: 80px;">学生:
</span>
   399            <span style="font-size: 14px; color: #333; flex: 1;">张三 (202
0001)</span>
   400          </div>
   401          <div style="display: flex; margin-bottom: 8px;">
   402            <span style="font-size: 14px; color: #999; width: 80px;">离校
日期:</span>
   403            <span style="font-size: 14px; color: #333; flex: 1;">2024-06-1
5</span>
   404          </div>
   405          <div style="display: flex; margin-bottom: 8px;">
   406            <span style="font-size: 14px; color: #999; width: 80px;">申请
原因:</span>
   407            <span style="font-size: 14px; color: #333; flex: 1;">毕业实习
，需要提前离校</span>
   408          </div>
   409        </div>
   410
   411        <!-- 审批记录时间轴 -->
   412        <div class="card">
   413          <div style="font-size: 16px; font-weight: bold; margin-bottom: 1
0px;">审批记录</div>
   414
   415          <!-- 时间轴项 -->
   416          <div style="position: relative; padding-left: 30px; margin-botto
m: 20px;">
   417            <div style="position: absolute; left: 10px; top: 4px; width: 1
0px; height: 10px; border-radius: 50%; background: white; border: 2px solid var(
--primary-color);"></div>
   418            <div style="position: absolute; left: 14px; top: 16px; bottom:
 -20px; width: 1px; background: #e8e8e8;"></div>
   419            <div class="flex-row justify-between align-center" style="marg
in-bottom: 6px;">
   420              <span style="font-size: 15px; font-weight: 600;">宿管员审批<
/span>
   421              <span class="tag tag-pending">待审批</span>
   422            </div>
   423            <div style="font-size: 13px; color: #666;">审批人: 李老师</div
>
   424          </div>
   425
   426          <div style="position: relative; padding-left: 30px; margin-botto
m: 20px;">
   427            <div style="position: absolute; left: 10px; top: 4px; width: 1
0px; height: 10px; border-radius: 50%; background: var(--status-success); border
: 2px solid var(--status-success);"></div>
   428            <div class="flex-row justify-between align-center" style="marg
in-bottom: 6px;">
   429              <span style="font-size: 15px; font-weight: 600;">提交申请</s
pan>
   430              <span class="tag tag-approved">已完成</span>
   431            </div>
   432            <div style="font-size: 13px; color: #666;">提交时间: 2024-06-0
1 10:30</div>
   433          </div>
   434        </div>
   435
   436        <!-- 审批操作 -->
   437        <div id="approval-section" style="padding: 10px;">
   438          <div class="card" style="margin-bottom: 10px;">
   439            <label style="display: block; font-size: 14px; color: #333; ma
rgin-bottom: 6px; font-weight: 500;">审批意见（可选）</label>
   440            <textarea id="approvalComment" style="width: 100%; min-height:
 60px; padding: 8px; border: 1px solid #e8e8e8; border-radius: 4px; font-size: 1
4px;" placeholder="请输入审批意见"></textarea>
   441            <span style="display: block; text-align: right; font-size: 12p
x; color: #999; margin-top: 4px;">0/200</span>
   442          </div>
   443          <div style="display: flex; gap: 10px;" id="approval-actions">
   444            <button class="btn-primary" style="flex: 1;" onclick="doApprov
e()">通过</button>
   445            <button class="btn-outline" style="flex: 1;" onclick="doReject
()">拒绝</button>
   446          </div>
   447        </div>
   448      </div>
   449    </div>
   450
   451    <script>
   452      let currentRole = 'student';
   453
   454      // Status mapping
   455      const statusMap = {
   456        'pending_dorm_manager': { text: '待宿管审批', class: 'tag-pending'
 },
   457        'pending_counselor': { text: '待辅导员审批', class: 'tag-pending'
},
   458        'pending_dean': { text: '待学工部审批', class: 'tag-pending' },
   459        'approved': { text: '已通过', class: 'tag-approved' },
   460        'rejected': { text: '已拒绝', class: 'tag-rejected' }
   461      };
   462
   463      function getStatusDisplay(status) {
   464        return statusMap[status] || { text: status, class: 'tag' };
   465      }
   466
   467      function showScreen(index) {
   468        document.querySelectorAll('.screen').forEach((s, i) => {
   469          s.classList.toggle('active', i === index);
   470        });
   471        document.querySelectorAll('.nav-tabs .nav-tab').forEach((t, i) =>
{
   472          t.classList.toggle('active', i === index);
   473        });
   474      }
   475
   476      async function switchRole(role) {
   477        const loggedIn = await apiLogin(role);
   478        if (!loggedIn) {
   479            console.error("Failed to login as", role);
   480        } else {
   481            console.log("Logged in as", role);
   482            if (role !== "student") {
   483               loadApprovals();
   484            }
   485        }
   486        currentRole = role;
   487        const roleMap = {
   488          'student': '学生',
   489          'dorm_manager': '宿管员',
   490          'counselor': '辅导员',
   491          'dean': '学工部'
   492        };
   493        const isStudent = role === 'student';
   494        const isDean = role === 'dean';
   495
   496        // Update nav tab text
   497        document.getElementById('nav-approval-text').textContent = isStude
nt ? '我的申请' : (isDean ? '备案查询' : '审批列表');
   498
   499        // Update list page title and role display
   500        document.getElementById('list-title').textContent = isStudent ? '
我的申请' : (isDean ? '备案查询' : '审批列表');
   501        document.getElementById('role-display').textContent = roleMap[role
];
   502
   503        // Show/hide entire approval section for student/dean
   504        const approvalSection = document.getElementById('approval-section'
);
   505        if (approvalSection) {
   506          approvalSection.style.display = (isStudent || isDean) ? 'none' :
 'block';
   507        }
   508      }
   509
   510      // File upload management
   511      const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
   512      const ALLOWED_TYPES = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.do
cx'];
   513      let uploadedFiles = [];
   514
   515      const fileInput = document.getElementById('fileInput');
   516      const fileList = document.getElementById('fileList');
   517      const uploadArea = document.querySelector('.upload-area');
   518
   519      // File selection handler
   520      fileInput.addEventListener('change', (e) => {

 succeeded in 0ms:
     1  // API Integration Layer
     2  const API_BASE_URL = '/api';
     3
     4  const TestAccounts = {
     5      'student': { id: '2024220220323', password: 'test123' },
     6      'dorm_manager': { id: '92025040', password: 'test123' },
     7      'counselor': { id: '20250015', password: 'test123' },
     8      'dean': { id: '20144020', password: 'test123' } // using admin as de
an for demo
     9  };
    10
    11  let currentToken = null;
    12
    13  async function apiLogin(role) {
    14      const account = TestAccounts[role];
    15      if (!account) return false;
    16
    17      try {
    18          const response = await fetch(API_BASE_URL + '/auth/login/', {
    19              method: 'POST',
    20              headers: { 'Content-Type': 'application/json' },
    21              body: JSON.stringify({ user_id: account.id, password: accoun
t.password })
    22          });
    23
    24          if (response.ok) {
    25              const data = await response.json();
    26              currentToken = data.access_token;
    27              return true;
    28          }
    29      } catch (e) {
    30          console.error("Login failed:", e);
    31      }
    32      return false;
    33  }
    34
    35  function getAuthHeaders() {
    36      return {
    37          'Authorization': 'Bearer ' + currentToken
    38      };
    39  }
    40
    41  async function apiSubmitApplication(phone, reason, leaveDate, files) {
    42      const formData = new FormData();
    43      formData.append('contact_phone', phone);
    44      formData.append('reason', reason);
    45      formData.append('leave_date', leaveDate);
    46      files.forEach(f => formData.append('attachments', f));
    47
    48      try {
    49          const response = await fetch(API_BASE_URL + '/applications/', {
    50              method: 'POST',
    51              headers: { 'Authorization': 'Bearer ' + currentToken },
    52              body: formData
    53          });
    54          return response.ok;
    55      } catch (e) {
    56          console.error("Submit application failed:", e);
    57          return false;
    58      }
    59  }
    60
    61  async function apiGetApprovals() {
    62      try {
    63          const response = await fetch(API_BASE_URL + '/approvals/', {
    64              headers: getAuthHeaders()
    65          });
    66          if (response.ok) {
    67              return await response.json();
    68          }
    69      } catch (e) {
    70          console.error("Get approvals failed:", e);
    71      }
    72      return [];
    73  }
    74
    75  async function apiApprove(approvalId, comment) {
    76      try {
    77          const response = await fetch(API_BASE_URL + '/approvals/' + appr
ovalId + '/approve/', {
    78              method: 'POST',
    79              headers: Object.assign({}, getAuthHeaders(), { 'Content-Type
': 'application/json' }),
    80              body: JSON.stringify({ comment: comment })
    81          });
    82          return response.ok;
    83      } catch (e) {
    84          console.error("Approve failed:", e);
    85          return false;
    86      }
    87  }
    88
    89  async function apiReject(approvalId, comment) {
    90      try {
    91          const response = await fetch(API_BASE_URL + '/approvals/' + appr
ovalId + '/reject/', {
    92              method: 'POST',
    93              headers: Object.assign({}, getAuthHeaders(), { 'Content-Type
': 'application/json' }),
    94              body: JSON.stringify({ comment: comment })
    95          });
    96          return response.ok;
    97      } catch (e) {
    98          console.error("Reject failed:", e);
    99          return false;
   100      }
   101  }
   102
   103  async function apiUploadAttachment(applicationId, file, attachmentType =
 'other') {
   104      const formData = new FormData();
   105      formData.append('file', file);
   106      formData.append('attachment_type', attachmentType);
   107
   108      try {
   109          const response = await fetch(API_BASE_URL + '/applications/' + a
pplicationId + '/attachments/', {
   110              method: 'POST',
   111              headers: getAuthHeaders(),
   112              body: formData
   113          });
   114          if (response.ok) {
   115              return await response.json();
   116          }
   117      } catch (e) {
   118          console.error("Upload attachment failed:", e);
   119      }
   120      return null;

exec
/bin/bash -lc "rtk nl -ba frontend/services/api.ts | rtk sed -n '1,90p'" in /hom
e/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1  // API Client for v0.2 Contract
     2  // Minimal implementation - can be extended
     3
     4  import type {
     5    LoginRequest,
     6    LoginResponse,
     7    ApplicationCreateRequest,
     8    ApplicationDetail,
     9    Application,
    10    ApprovalListItem,
    11    ApprovalActionRequest,
    12    ApprovalActionResponse,
    13    PaginatedResponse,
    14    ApiError,
    15  } from '../types/api';
    16
    17  export interface ApiConfig {
    18    baseUrl: string;
    19    getToken?: () => string | null;
    20    onUnauthorized?: () => void;
    21  }
    22
    23  export class ApiClient {
    24    private config: ApiConfig;
    25
    26    constructor(config: ApiConfig) {
    27      this.config = config;
    28    }
    29
    30    private async request<T>(
    31      endpoint: string,
    32      options: RequestInit = {}
    33    ): Promise<T> {
    34      const token = this.config.getToken?.();
    35      const headers: HeadersInit = {
    36        'Content-Type': 'application/json',
    37        ...options.headers,
    38      };
    39
    40      if (token) {
    41        headers['Authorization'] = `Bearer ${token}`;
    42      }
    43
    44      const response = await fetch(`${this.config.baseUrl}${endpoint}`, {
    45        ...options,
    46        headers,
    47      });
    48
    49      if (response.status === 401) {
    50        this.config.onUnauthorized?.();
    51        throw new Error('Unauthorized');
    52      }
    53
    54      const data = await response.json();
    55
    56      if (!response.ok) {
    57        throw data as ApiError;
    58      }
    59
    60      return data as T;
    61    }
    62
    63    // Auth
    64    async login(req: LoginRequest): Promise<LoginResponse> {
    65      return this.request('/api/auth/login', {
    66        method: 'POST',
    67        body: JSON.stringify(req),
    68      });
    69    }
    70
    71    // Applications
    72    async createApplication(req: ApplicationCreateRequest): Promise<Applic
ationDetail> {
    73      return this.request('/api/applications/', {
    74        method: 'POST',
    75        body: JSON.stringify(req),
    76      });
    77    }
    78
    79    async listApplications(
    80      limit = 20,
    81      offset = 0
    82    ): Promise<PaginatedResponse<Application>> {
    83      return this.request(
    84        `/api/applications/?limit=${limit}&offset=${offset}`
    85      );
    86    }
    87
    88    async getApplication(id: string): Promise<ApplicationDetail> {
    89      return this.request(`/api/applications/${id}/`);
    90    }

exec
/bin/bash -lc "rtk nl -ba backend/apps/users/views.py | rtk sed -n '1,80p'; rtk
nl -ba backend/apps/users/serializers.py | rtk sed -n '1,80p'; rtk nl -ba backen
d/apps/users/urls.py | rtk sed -n '1,30p'" in /home/caohui/projects/graduation-l
eave-system
 succeeded in 139ms:
     1  from django.urls import path
     2  from . import views
     3
     4  urlpatterns = [
     5      path('login', views.login, name='login'),
     6  ]

codex
One important compatibility issue surfaced: the demo calls `/api/auth/login/` wh
ile the backend route is declared as `login` without a trailing slash. I’ll veri
fy whether Django is relying on slash redirection before I include it as an acti
on item.
exec
/bin/bash -lc "rtk rg -n \"APPEND_SLASH|CommonMiddleware|MIDDLEWARE|ROOT_URLCONF
\" backend/config backend -g '*.py'" in /home/caohui/projects/graduation-leave-s
ystem
 succeeded in 0ms:
backend/config/settings/base.py:41:MIDDLEWARE = [
backend/config/settings/base.py:45:    'django.middleware.common.CommonMiddlewar
e',
backend/config/settings/base.py:52:ROOT_URLCONF = 'config.urls'
backend/config/settings/base.py:41:MIDDLEWARE = [
backend/config/settings/base.py:45:    'django.middleware.common.CommonMiddlewar
e',
backend/config/settings/base.py:52:ROOT_URLCONF = 'config.urls'

exec
/bin/bash -lc "rtk rg -n \"class User|role|dorm_manager|dean|admin\" backend/app
s/users -g '*.py'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/users/integrations/xg_user_mapper.py:15:            'role': str | N
one,
backend/apps/users/integrations/xg_user_mapper.py:28:        'role': None,
backend/apps/users/integrations/xg_user_mapper.py:70:    role = None
backend/apps/users/integrations/xg_user_mapper.py:77:                role = 'stu
dent'
backend/apps/users/integrations/xg_user_mapper.py:87:                role = 'stu
dent'
backend/apps/users/integrations/xg_user_mapper.py:102:    result['role'] = role
backend/apps/users/class_mapping.py:7:    dorm_manager = models.ForeignKey(User,
 on_delete=models.PROTECT, related_name='managed_dorms', null=True, blank=True)
backend/apps/users/class_mapping.py:8:    dorm_manager_name = models.CharField(m
ax_length=100, null=True, blank=True)
backend/apps/users/services/xg_user_sync.py:62:            if local_user.role !=
 'student':
backend/apps/users/services/xg_user_sync.py:65:                    'reason': 'ro
le_mismatch',
backend/apps/users/services/xg_user_sync.py:66:                    'local_role':
 local_user.role,
backend/apps/users/services/xg_user_sync.py:67:                    'api_role': m
apped['role']
backend/apps/users/services/xg_user_sync.py:138:            if local_user.role !
= 'student':
backend/apps/users/services/xg_user_sync.py:141:                    'reason': 'r
ole_mismatch',
backend/apps/users/services/xg_user_sync.py:142:                    'local_role'
: local_user.role,
backend/apps/users/services/xg_user_sync.py:143:                    'api_role':
mapped['role']
backend/apps/users/admin.py:1:from django.contrib import admin
backend/apps/users/admin.py:5:@admin.register(User)
backend/apps/users/admin.py:6:class UserAdmin(admin.ModelAdmin):
backend/apps/users/admin.py:7:    list_display = ['user_id', 'name', 'role', 'cl
ass_id', 'active']
backend/apps/users/admin.py:8:    list_filter = ['role', 'active', 'is_graduatin
g']
backend/apps/users/tests/test_xg_user_mapper.py:24:        self.assertEqual(resu
lt['role'], 'student')
backend/apps/users/tests/test_xg_user_mapper.py:43:        self.assertEqual(resu
lt['role'], 'student')
backend/apps/users/tests/test_xg_user_mapper.py:84:        self.assertIsNone(res
ult['role'])
backend/apps/users/tests/test_xg_user_mapper.py:98:        self.assertIsNone(res
ult['role'])
backend/apps/users/tests/test_xg_user_mapper.py:113:        self.assertEqual(res
ult['role'], 'student')
backend/apps/users/tests/test_xg_user_mapper.py:141:        self.assertEqual(res
ult['role'], 'student')
backend/apps/users/tests/test_xg_user_sync.py:18:            role='student',
backend/apps/users/tests/test_xg_user_sync.py:29:            role='counselor',
backend/apps/users/tests/test_xg_user_sync.py:99:    def test_local_role_conflic
t(self):
backend/apps/users/tests/test_xg_user_sync.py:119:        self.assertEqual(confl
ict['reason'], 'role_mismatch')
backend/apps/users/tests/test_xg_user_sync.py:120:        self.assertEqual(confl
ict['local_role'], 'counselor')
backend/apps/users/tests/test_xg_user_sync.py:121:        self.assertEqual(confl
ict['api_role'], 'student')
backend/apps/users/tests/test_xg_user_sync.py:234:            role='student',
backend/apps/users/tests/test_xg_user_sync.py:246:            role='counselor',
backend/apps/users/tests/test_xg_user_sync.py:282:    def test_scenario3_skip_ro
le_conflict(self):
backend/apps/users/tests/test_xg_user_sync.py:283:        """场景3：检测并跳过ro
le冲突(local非student)"""
backend/apps/users/tests/test_xg_user_sync.py:290:        self.assertEqual(resul
t['conflicts'][0]['reason'], 'role_mismatch')
backend/apps/users/tests/test_xg_user_sync.py:326:            role='student',
backend/apps/users/tests/test_xg_user_sync.py:370:            role='student',
backend/apps/users/tests/test_xg_user_sync.py:383:        self.assertEqual(couns
elor.role, 'counselor')
backend/apps/users/migrations/0001_initial.py:25:                ('role', models
.CharField(choices=[('student', '学生'), ('counselor', '辅导员'), ('dean', '学工
部')], max_length=20)),
backend/apps/users/migrations/0006_add_admin_role.py:1:# Generated migration to
add ADMIN role to User.role choices
backend/apps/users/migrations/0006_add_admin_role.py:15:            name='role',
backend/apps/users/migrations/0006_add_admin_role.py:19:                    ('do
rm_manager', '宿管员'),
backend/apps/users/migrations/0006_add_admin_role.py:21:                    ('de
an', '学工部'),
backend/apps/users/migrations/0006_add_admin_role.py:22:                    ('ad
min', '学工管理员')
backend/apps/users/migrations/0004_backfill_dorm_manager.py:6:def backfill_dorm_
manager(apps, schema_editor):
backend/apps/users/migrations/0004_backfill_dorm_manager.py:8:    for mapping in
 ClassMapping.objects.filter(dorm_manager__isnull=True):
backend/apps/users/migrations/0004_backfill_dorm_manager.py:9:        mapping.do
rm_manager_id = mapping.counselor_id
backend/apps/users/migrations/0004_backfill_dorm_manager.py:10:        mapping.d
orm_manager_name = mapping.counselor_name
backend/apps/users/migrations/0004_backfill_dorm_manager.py:11:        mapping.s
ave(update_fields=["dorm_manager", "dorm_manager_name"])
backend/apps/users/migrations/0004_backfill_dorm_manager.py:16:    ClassMapping.
objects.all().update(dorm_manager=None, dorm_manager_name=None)
backend/apps/users/migrations/0004_backfill_dorm_manager.py:22:        ('users',
 '0003_classmapping_dorm_manager_and_more'),
backend/apps/users/migrations/0004_backfill_dorm_manager.py:26:        migration
s.RunPython(backfill_dorm_manager, reverse_backfill),
backend/apps/users/migrations/0005_user_building.py:7:        ('users', '0004_ba
ckfill_dorm_manager'),
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:17:
        name='dorm_manager',
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:22:
        name='dorm_manager_name',
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:27:
        name='role',
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:28:
        field=models.CharField(choices=[('student', '学生'), ('dorm_manager', '
宿管员'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20),
backend/apps/users/apps.py:4:class UsersConfig(AppConfig):
backend/apps/users/models.py:5:class UserRole(models.TextChoices):
backend/apps/users/models.py:7:    DORM_MANAGER = 'dorm_manager', '宿管员'
backend/apps/users/models.py:9:    DEAN = 'dean', '学工部'
backend/apps/users/models.py:10:    ADMIN = 'admin', '学工管理员'
backend/apps/users/models.py:13:class UserManager(BaseUserManager):
backend/apps/users/models.py:29:class User(AbstractBaseUser, PermissionsMixin):
backend/apps/users/models.py:32:    role = models.CharField(max_length=20, choic
es=UserRole.choices)
backend/apps/users/models.py:51:    REQUIRED_FIELDS = ['name', 'role']
backend/apps/users/tests/test_import_csv.py:14:        User.objects.create_user(
user_id='T001', name='李老师', role=UserRole.COUNSELOR, password='T001', departm
ent='计算机学院')
backend/apps/users/tests/test_import_csv.py:15:        User.objects.create_user(
user_id='T002', name='王老师', role=UserRole.COUNSELOR, password='T002', departm
ent='软件学院')
backend/apps/users/tests/test_import_csv.py:33:            self.assertEqual(User
.objects.filter(role=UserRole.COUNSELOR).count(), 4)
backend/apps/users/tests/test_import_csv.py:109:            self.assertEqual(Use
r.objects.filter(role=UserRole.STUDENT).count(), 1)
backend/apps/users/tests/test_import_csv.py:129:            self.assertEqual(Use
r.objects.filter(role=UserRole.STUDENT).count(), 0)
backend/apps/users/tests/test_import_csv.py:155:            initial_count = User
.objects.filter(role=UserRole.COUNSELOR).count()
backend/apps/users/tests/test_import_csv.py:161:            final_count = User.o
bjects.filter(role=UserRole.COUNSELOR).count()
backend/apps/users/serializers.py:6:class UserSerializer(serializers.ModelSerial
izer):
backend/apps/users/serializers.py:9:        fields = ['user_id', 'name', 'role',
 'class_id', 'active', 'is_graduating', 'graduation_year']
backend/apps/users/serializers.py:17:        fields = ['user_id', 'name', 'role'
, 'class_id']
backend/apps/users/management/commands/cleanup_test_data.py:28:        # Get cou
nts by role
backend/apps/users/management/commands/cleanup_test_data.py:31:            'stud
ents': User.objects.filter(role='student').count(),
backend/apps/users/management/commands/cleanup_test_data.py:32:            'dorm
_managers': User.objects.filter(role='dorm_manager').count(),
backend/apps/users/management/commands/cleanup_test_data.py:33:            'coun
selors': User.objects.filter(role='counselor').count(),
backend/apps/users/management/commands/cleanup_test_data.py:34:            'admi
ns': User.objects.filter(role='admin').count(),
backend/apps/users/management/commands/cleanup_test_data.py:42:            self.
stdout.write(f'  - 宿管: {stats["dorm_managers"]}')
backend/apps/users/management/commands/cleanup_test_data.py:44:            self.
stdout.write(f'  - 管理: {stats["admins"]}')
backend/apps/users/management/commands/import_csv.py:97:
        'role': UserRole.STUDENT,
backend/apps/users/management/commands/import_csv.py:159:
         'role': UserRole.COUNSELOR,
backend/apps/users/management/commands/import_csv.py:211:
     counselor = User.objects.get(user_id=counselor_id, role=UserRole.COUNSELOR)
backend/apps/users/management/commands/seed_data.py:45:                    'role
': UserRole.STUDENT,
backend/apps/users/management/commands/seed_data.py:70:                    'role
': UserRole.COUNSELOR,
backend/apps/users/management/commands/seed_data.py:81:        dorm_managers = [
backend/apps/users/management/commands/seed_data.py:87:        for dm_data in do
rm_managers:
backend/apps/users/management/commands/seed_data.py:92:                    'role
': UserRole.DORM_MANAGER,
backend/apps/users/management/commands/seed_data.py:100:                self.std
out.write(f'Created dorm_manager: {user.user_id}')
backend/apps/users/management/commands/seed_data.py:107:                'role':
UserRole.DEAN,
backend/apps/users/management/commands/seed_data.py:114:            self.stdout.
write(f'Created dean: {user.user_id}')
backend/apps/users/management/commands/import_students.py:63:                del
eted = User.objects.filter(role=UserRole.STUDENT).delete()
backend/apps/users/management/commands/import_students.py:115:
  'role': UserRole.STUDENT,
backend/apps/users/management/commands/import_staff.py:18:    help = 'Import sta
ff (dorm managers, counselors, admins) from CSV'
backend/apps/users/management/commands/import_staff.py:41:            'by_role':
 {}
backend/apps/users/management/commands/import_staff.py:67:        role_str = (ro
w.get('角色') or row.get('role') or '').strip()
backend/apps/users/management/commands/import_staff.py:72:        if not user_id
 or not name or not role_str:
backend/apps/users/management/commands/import_staff.py:74:            stats['err
ors'].append(f'Missing required fields: user_id={user_id}, name={name}, role={ro
le_str}')
backend/apps/users/management/commands/import_staff.py:77:        # Map role str
ing to UserRole
backend/apps/users/management/commands/import_staff.py:78:        role_map = {
backend/apps/users/management/commands/import_staff.py:87:        role = role_ma
p.get(role_str)
backend/apps/users/management/commands/import_staff.py:88:        if not role:
backend/apps/users/management/commands/import_staff.py:90:            stats['err
ors'].append(f'{user_id}: Unknown role "{role_str}"')
backend/apps/users/management/commands/import_staff.py:94:        if role == Use
rRole.COUNSELOR and department:
backend/apps/users/management/commands/import_staff.py:105:        if role == Us
erRole.DORM_MANAGER and not building:
backend/apps/users/management/commands/import_staff.py:122:            stats['by
_role'][role] = stats['by_role'].get(role, 0) + 1
backend/apps/users/management/commands/import_staff.py:128:                    '
role': role,
backend/apps/users/management/commands/import_staff.py:141:            stats['by
_role'][role] = stats['by_role'].get(role, 0) + 1
backend/apps/users/management/commands/import_staff.py:151:        if stats['by_
role']:
backend/apps/users/management/commands/import_staff.py:152:            self.stdo
ut.write('\nBy role:')
backend/apps/users/management/commands/import_staff.py:153:            for role,
 count in stats['by_role'].items():
backend/apps/users/management/commands/import_staff.py:154:                self.
stdout.write(f'  {role}: {count}')

exec
/bin/bash -lc 'rtk rg -n "auth/login/|auth/login[''^a-zA-Z0-9_-]" demo-web front
end docs/contracts docs/testing-guide.md docs/SYSTEM-OPERATIONS-GUIDE.md --glob
'"'"'!node_modules'"'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/SYSTEM-OPERATIONS-GUIDE.md:60:curl http://localhost:8001/api/auth/login \
docs/SYSTEM-OPERATIONS-GUIDE.md:217:- **端点：** `POST /api/auth/login`
docs/SYSTEM-OPERATIONS-GUIDE.md:383:curl http://localhost:8001/api/auth/login \
docs/testing-guide.md:34:- 登录: `POST /api/auth/login/`
docs/testing-guide.md:85:curl -X POST http://localhost:8001/api/auth/login/ \
docs/testing-guide.md:165:curl -X POST http://localhost:8001/api/auth/login/ \
docs/testing-guide.md:220:curl -X POST http://localhost:8001/api/auth/login/ \
docs/testing-guide.md:431:- [ ] POST /api/auth/login/ - 登录
frontend/services/api.ts:65:    return this.request('/api/auth/login', {
demo-web/js/api.js:18:        const response = await fetch(API_BASE_URL + '/auth
/login/', {
docs/contracts/contract-v0.2.md:146:### POST `/api/auth/login`
docs/contracts/contract-v0.1.md:598:  rest.post('/api/auth/login', (req, res, ct
x) => {
docs/contracts/contract-v0.1.md:626:    response = client.post('/api/auth/login'
, {

codex
[RESPONSE_START]
{
  "consensus": false,
  "decision": "建议采用混合方案：保留 demo-web 的角色选择器以满足演示效率，但移
除前端 TestAccounts 明文账号密码；新增仅在 DEMO_AUTH_ENABLED=true 时可用的后端 d
emo-login 端点，由后端按角色选择受控演示用户并返回与现有 /api/auth/login 相同的
LoginResponse。完整登录页面不应作为本轮 demo-web 的必要前置，但生产路径必须继续
使用标准 /api/auth/login。",
  "blocking_issues": [
    "必须明确 demo-login 只在演示/开发环境启用，生产环境默认关闭并返回 404 或 40
3。",
    "必须定义演示角色到真实用户的后端配置来源，不能把账号密码或固定测试凭证提交
到前端仓库。",
    "必须修正 demo-web 当前登录路径的兼容性问题：前端调用 /api/auth/login/，而后
端 canonical 路由是 /api/auth/login。"
  ],
  "reasoning": "我同意 DISCUSS-DEMO-WEB认证方案-如何移除TESTACCOUNTS明文凭证-178
0838572-r0-claude 提出的先澄清兼容性、状态持久化和验证风险，但该 framing 还没有
给出安全边界。完整登录页可以提升生产体验，但不能解决 demo-web 角色快速切换的演示
需求；继续保留前端 TestAccounts 又明显泄露凭证。后端受控 demo-login 是更小改动：
保留角色选择器和 JWT 后端授权链路，前端只提交 role，不接触密码；同时通过环境开关
避免把角色一键登录能力带入生产。",
  "previous_responses": [
    "DISCUSS-DEMO-WEB认证方案-如何移除TESTACCOUNTS明文凭证-1780838572-r0-claude"
  ],
  "targeted_challenges": [
    {
      "target_agent": "claude",
      "target_response_id": "DISCUSS-DEMO-WEB认证方案-如何移除TESTACCOUNTS明文凭
证-1780838572-r0-claude",
      "question": "你是否接受把本轮范围限定为“后端受控 demo-login + 保留角色选择
器”，并把完整登录页面拆为后续生产体验任务？",
      "rationale": "如果不先限定范围，方案会在演示便利性和生产登录体验之间扩张，
导致本轮无法收敛。"
    },
    {
      "target_agent": "claude",
      "target_response_id": "DISCUSS-DEMO-WEB认证方案-如何移除TESTACCOUNTS明文凭
证-1780838572-r0-claude",
      "question": "请明确 demo-login 的生产禁用策略应是返回 404、403，还是构建时
完全不挂载路由？",
      "rationale": "这决定安全验收方式，也影响部署误配置时的暴露面。"
    }
  ],
  "dissent": "不建议把“完整登录页面实现”作为移除 TestAccounts 的唯一方案；它会牺
牲演示角色快速切换能力，而且现有 demo-web 已经围绕角色选择器组织流程。",
  "evidence": [
    "demo-web/js/api.js:4-9 当前在前端定义 TestAccounts，包含 student、dorm_mana
ger、counselor、dean 的账号和明文 password。",
    "demo-web/js/api.js:18-22 当前 apiLogin 直接把 account.id 和 account.passwor
d 从浏览器提交到登录接口。",
    "demo-web/index.html:264-272 已存在演示角色选择器；demo-web/index.html:476-4
83 的 switchRole 已经把角色切换绑定到 apiLogin 和审批列表加载。",
    "backend/apps/users/serializers.py:20-44 现有 LoginSerializer 已完成用户密码
校验并返回 access_token、token_type、user；demo-login 应复用同等响应形状。",
    "backend/apps/users/urls.py:4-5 声明的是 path('login')，frontend/services/ap
i.ts:64-68 也使用 /api/auth/login，而 demo-web/js/api.js:18 使用 /auth/login/，
存在 trailing slash 不一致。"
  ],
  "action_items": [
    {
      "owner": "claude",
      "task": "提出 demo-login 最小设计：请求只含 role，响应复用 LoginResponse，
环境变量 DEMO_AUTH_ENABLED 默认 false，角色到用户映射由后端配置或数据库标记提供
。",
      "due": "next round",
      "verification": "设计中不得包含前端明文密码；生产关闭时 demo-login 不可用
。"
    },
    {
      "owner": "codex",
      "task": "审查实现方案的安全边界、路径兼容性和测试清单。",
      "due": "next round",
      "verification": "至少覆盖前端无 TestAccounts、demo-login 关闭、demo-login
开启按角色返回 JWT、/api/auth/login 路径一致性。"
    },
    {
      "owner": "implementer",
      "task": "修改 demo-web：移除 TestAccounts，role selector 调用后端 demo-log
in；同时统一登录路径为无 trailing slash 或明确后端兼容策略。",
      "due": "implementation phase",
      "verification": "rg 不再在 demo-web 中找到 TestAccounts 或 password 明文映
射；浏览器切换四类角色仍能拿到 token 并加载对应页面。"
    }
  ]
}
[RESPONSE_END]
tokens used
75,377

