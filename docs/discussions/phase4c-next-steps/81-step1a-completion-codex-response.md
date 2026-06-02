# Step 1A完成审查与下一步策略 - Codex响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**审查类型：** 实现审查 + 策略建议  
**针对：** `80-step1a-completion-next-review-request.md`  
**文档编号：** 81

---

## 1. Step 1A审查结果

**结论：Step 1A签名纯函数可以通过，但建议在进入真实诊断前补两个小修正。**

已验证：

- `backend/apps/users/integrations/xg_user_client.py` 的 `generate_sign()` 按三个参数值排序后拼接，再做 `sha1/md5` 小写 hex，符合当前官方样例约束。
- 官方样例测试覆盖了显式 `sha1` 和默认 `sha1`。
- 非法 `encryption_type` 会失败，不会静默降级。
- 聚焦测试在 Docker 环境通过：`rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput`，4/4 passed。

### P0问题

无。

当前代码没有发现会导致官方签名样例失败、密钥泄露或错误参与字段签名的 P0 问题。

### P1问题

1. **MD5测试断言过弱。**  
   位置：`backend/apps/users/tests/test_xg_user_client.py:28`  
   现在只检查长度和 hex 字符集，即使拼接顺序错误也可能通过。建议改成固定期望值，例如 `generate_sign('secret', '1234567890', 'random', 'md5')` 应等于 `2a471e23465cf11561ef7455fff00a86`。

2. **Step 1A相对 doc 77 的“配置切片”尚未完成。**  
   位置：`backend/apps/users/integrations/xg_user_client.py:46`  
   当前只交付签名函数，`XGUserAPIClient` 仍是占位类，尚无配置读取/校验对象。若把 Step 1A 定义为“签名函数切片”，可以接受；若沿用 doc 77 验收标准，则还缺少 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 的明确错误测试。

### P2问题

1. **空字符串策略需要在边界上明确。**  
   `generate_sign()` 作为纯函数可以允许空字符串，但请求构建/配置层必须拒绝空 `appSecret/timestamp/randStr`。建议不要在签名函数里混入环境语义，在 Step 1B 的 config/header 构造处校验。

2. **特殊字符与 Unicode 不需要作为 P0，但可补一个文档化测试。**  
   当前实现使用 UTF-8 编码，行为确定。实际 header 中的 `randStr` 应限制为 ASCII 随机串；如果平台文档没有要求 Unicode，测试不必扩大为必选项。

3. **大小写/空白归一化应放在配置层。**  
   `generate_sign()` 严格接受 `sha1/md5` 是合理的；环境变量读取时可以对 `XG_USER_API_ENCRYPTION_TYPE` 做 `strip().lower()`，再传入纯函数。

### 安全评价

- 当前签名函数不会记录或返回密钥，仅返回摘要，安全面较小。
- `md5` 只因官方接口兼容而保留，不应作为默认值。
- 后续诊断脚本不得打印完整 `appSecret`、完整 `sign`、手机号、身份证号、openId 或完整原始响应。

---

## 2. 下一步策略建议

**建议选择“修正后的选项A”：先做 Step 1B-lite，再做 Step 1C。**

不建议纯选项B先写诊断脚本。诊断脚本也必须构造 headers/form-data、生成 timestamp/randStr/sign、处理超时和脱敏输出；如果没有可复用客户端层，脚本会复制 Step 1B 逻辑，后续再迁回客户端时容易产生签名字段、日志脱敏、错误分类不一致。

推荐顺序：

1. **立即补 Step 1A 小修正。**  
   固定 MD5 期望值；如坚持 doc 77 的 Step 1A 验收，再补配置校验对象与缺失配置测试。

2. **执行 Step 1B-lite。**  
   只实现配置读取、headers 构造、form-data 构造、单页请求、基础响应解析和 mock 测试。不做分页循环、不做重试、不接入业务 Provider。

3. **随后执行 Step 1C。**  
   诊断脚本调用 Step 1B-lite 的客户端能力，默认 dry-run；只有 `XG_RUN_LIVE_API_TEST=1` 且配置齐全时做一次 `page=1/pageNum=1` live probe。

这样仍然能快速验证网络/API可达性，但不会牺牲可测试性和脱敏一致性。

---

## 3. Step 1C范围确认

Step 1C范围基本合理，但需要改成“安全诊断入口”，不是完整请求/响应日志收集器。

### 必须包含

- 环境变量读取与校验：URL、appKey、appSecret、tenantCode、encryptionType、live开关。
- 官方签名样例自检。
- 默认 dry-run，请求摘要不发网络请求。
- live probe 硬门禁：`XG_RUN_LIVE_API_TEST=1`，配置齐全，固定 `page=1/pageNum=1`。
- 输出格式：默认 text，支持 `--format=json`。
- 超时参数：默认短超时，例如 5 秒，可用 `--timeout` 调整。
- 错误分类：`config_error`、`sign_error`、`network_error`、`http_error`、`auth_failed`、`tenant_invalid`、`business_error`、`unexpected_schema`。
- 脱敏输出：只显示 header/form-data 的非敏感摘要；响应 body 只允许脱敏预览。

### 应删除或限制

- 不记录完整请求 headers，因为其中包含完整 `sign`。
- 不保存完整响应 body，除非先脱敏并明确标注。
- 不做分页循环、批量读取、落库、字段映射结论。
- 不在常规 Django/pytest 测试套件里触发 live API。

### 建议输出

文本输出保持短摘要：

```text
配置: OK
签名样例: OK
Live调用: skipped (XG_RUN_LIVE_API_TEST != 1)
请求摘要: POST auth-user-info page=1 pageNum=1 encryptionType=sha1 sign=present
```

live 成功时输出：

```text
HTTP状态: 200
业务码: 200
分页: current_page=1 per_page=1 total=...
字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
样本: name=张* number=17**** phone=186****9896
```

---

## 4. Step 1B范围界定

### 应包含

- `XGUserAPIConfig` 或等价配置对象：从环境读取、校验必填项、归一化 encryptionType。
- `XGUserAPIClient.build_headers()`：
  - 包含 `appKey/timestamp/randStr/sign/encryptionType`。
  - 默认不发送 `appId`，除非平台部确认接口要求。
  - timestamp/randStr 可注入或可 patch，方便确定性测试。
- `XGUserAPIClient.build_form_data()`：
  - 包含 `tenantCode/page/pageNum`。
  - 默认 `page=1/pageNum=1`。
- `XGUserAPIClient.fetch_users_page()`：
  - 使用短超时。
  - 支持注入 session，便于 mock `post`。
  - 只请求单页。
- 响应解析：
  - 协议层解析 `code/msg/data/current_page/data/total/per_page`。
  - 人员字段先宽松采样，不做业务字段强承诺。
- Mock测试：
  - header字段完整、签名确定性。
  - form-data字段完整。
  - 成功响应解析分页和人员列表。
  - HTTP错误、网络异常、业务错误、schema异常。
  - 缺失配置和非法 encryptionType。

### 应排除

- 全量分页循环。
- 重试机制，尤其是认证失败重试。
- Provider接入、数据库写入、CSV替换。
- 班级/辅导员/宿舍字段业务映射。
- 真实API测试进入 CI 或常规测试。
- 完整原始响应日志。

---

## 最终建议

Step 1A可以作为“签名函数切片”通过；进入下一步前建议补 MD5 固定值测试。下一步不要先写孤立诊断脚本，而是先做一个很窄的 Step 1B-lite，让 Step 1C 复用同一套请求构造、签名和脱敏逻辑。真实 live probe 仍必须保持单页一条、显式开关、脱敏输出。
