# API测试Step 0后下一步策略 - Codex审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**审查类型：** 执行策略  
**针对：** `76-claude-post-step0-next-strategy-request.md`  
**文档编号：** 77

---

## 审查结论

**结论：批准继续 Step 1，但需要把原计划改成“分步实现的诊断客户端”，而不是一次性完整封装。**

Step 0 安全修正已经完成，签名算法也已有官方样例，可以开始写代码；但 `tenantCode` 仍未确认，真实接口字段也未验证。因此下一步的最优路径不是等待，也不是直接接入业务 Provider，而是先交付一个可离线验证、可 mock 测试、可人工 live probe 的最小诊断层。

推荐决策：

1. **租户Code未拿到前不阻塞代码实现，但阻塞真实API调用。**
2. **签名函数必须先用官方样例固化为单元测试。**
3. **实现范围采用 B 分步方案，不采用一次性大包方案。**
4. **响应字段解析先宽松，业务映射决策延后。**
5. **诊断脚本默认文本输出，追加 `--format=json` 支持。**

---

## 对5个问题的明确建议

### 问题1：是否应该先获取租户Code？

**建议：选项 A + C 的组合。**

继续实现客户端代码和 mock 测试，`tenantCode` 使用环境变量占位；但真实API验证必须硬性等待平台部提供本校 `tenantCode`。也就是说：

- `generate_sign()`、请求构造、响应解析、错误归一化、mock 测试可以立即做。
- `xg_user_api_probe.py` 可以立即做，但缺少 `XG_USER_API_TENANT_CODE` 时只能执行配置校验、签名样例验证、`--dry-run` 请求摘要，不能发起网络请求。
- live probe 必须等 `tenantCode` 到位，并且需要操作者显式确认，例如 `XG_RUN_LIVE_API_TEST=1`。

不建议选项 B。等待租户Code会阻塞低风险、可离线验证的工作。

### 问题2：签名算法是否需要单独验证模块？

**建议：选项 A，但把签名函数设计成独立纯函数，并把官方样例作为 P0 单元测试。**

不需要额外创建一次性签名验证脚本。更好的边界是：

```text
backend/apps/users/integrations/xg_user_client.py
  - generate_sign(app_secret, timestamp, rand_str, encryption_type="sha1")
  - XGUserAPIClient
```

测试必须包含官方样例：

- `appSecret=6bd1b3fb015b4e72a85769e9d64405d1`
- `timestamp=1573702840`
- `randStr=Gc6LGToDKy2AMhXE`
- `sha1=baeaa6693fb7b9914c9ff9e388654878b8754515`

实现注意点：

- 字典排序对象是三个**参数值**：`appSecret`、`timestamp`、`randStr`，不是参数名。
- 默认 `sha1`，仅允许 `sha1` / `md5`，其他值直接抛配置错误。
- 输出小写 hex。
- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。

### 问题3：实现范围是否过大？

**建议：选项 B，分步实现。**

Claude 的原计划方向正确，但作为下一步一次性打包偏大。建议拆成三个可验收切片：

**B1：签名与配置切片**

- 新建 `backend/apps/users/integrations/` 包。
- 实现 `generate_sign()`。
- 实现配置读取/校验对象。
- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。

**B2：请求构造与响应解析切片**

- 实现 header/form-data 构造。
- 使用 `requests`，设置短超时，默认 `page=1&pageNum=1`。
- 解析 `code/msg/data/current_page/data/total/per_page`。
- 对成功响应、业务错误、schema 异常做 mock 测试。

**B3：诊断脚本与错误归一化切片**

- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
- 默认不进行 live call，必须环境变量或参数显式开启。
- 输出脱敏文本；需要自动化时支持 JSON。

这个拆法能在没有 `tenantCode` 的情况下完成 70%-80% 的确定性工作，同时把真实接口风险留在最后一个人工门。

### 问题4：是否需要先确认响应字段？

**建议：选项 A，但字段解析必须“宽松采样 + 不承诺业务可用”。**

API文档里的返回字段足以做诊断客户端，不足以证明它能替代当前 CSV/Mock 数据源。当前文档没有明确给出：

- 班级 `class_id`
- 辅导员映射
- 院系/专业标准字段
- 宿舍清退状态

因此客户端解析应分两层：

1. **接口结构层：** 严格校验 `code/msg/data/data/total` 这类协议字段。
2. **业务字段层：** 宽松采样，记录 `name/number/phone/identity_id/department/user_identity/user_auth_extra_field` 是否出现，不因业务字段缺失直接失败。

live probe 成功后，应输出“字段覆盖报告”，再决定是否接入 Provider。没有班级/辅导员/宿舍字段前，不应把该接口宣称为完整业务数据源。

### 问题5：诊断脚本的输出格式？

**建议：选项 C，但默认选项 A。**

默认人类可读文本最适合人工诊断；同时提供 `--format=json`，方便后续把结果贴入验收文档或自动化脚本。

默认文本建议包含：

```text
配置: OK
签名样例: OK
Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
```

live 成功时只输出摘要：

```text
HTTP状态: 200
业务码: 200
分页: current_page=1 per_page=1 total=4311
字段: name=yes number=yes phone=yes department=yes user_identity=yes
样本: name=张* number=17 phone=186****9896
```

JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。

---

## 其他风险与遗漏

### P1：`AppId` 与接口文档字段可能不一致

`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。

### P1：生产URL必须作为配置，不要写死

用户确认的学校域名可作为 `.env.example` 默认值，但客户端必须只从配置读取 URL。后续如果平台部要求改用 `saas.api.goliveplus.cn` 或测试环境，不能改代码。

### P1：真实调用要限制半径

第一次 live probe 固定：

- `page=1`
- `pageNum=1`
- 不带姓名、手机号、学号过滤
- 不做分页循环
- 不保存原始响应文件，除非已脱敏

### P2：测试不要新增第三方 mock 依赖

当前依赖已有 `requests`，测试可以直接用 `unittest.mock.patch` mock `requests.Session.post`。除非后续 HTTP 客户端测试明显膨胀，否则不必引入 `responses` 或 `requests-mock`。

### P2：错误分类要面向排障

建议定义少量稳定错误类型：

- `config_error`
- `sign_error`
- `network_error`
- `http_error`
- `auth_failed`
- `tenant_invalid`
- `business_error`
- `unexpected_schema`

诊断脚本输出错误类型和非敏感上下文即可，不打印完整 header。

---

## 推荐执行优先级

### Step 1A：签名与配置，先做

交付：

- `backend/apps/users/integrations/__init__.py`
- `backend/apps/users/integrations/xg_user_client.py`
- `backend/apps/users/tests/test_xg_user_client.py`

验收：

- 官方签名样例通过。
- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
- `tenantCode` 缺失不影响签名样例测试。

### Step 1B：请求构造与解析，再做

交付：

- `XGUserAPIClient.build_headers()`
- `XGUserAPIClient.build_form_data()`
- `XGUserAPIClient.fetch_users_page()`
- 响应解析 DTO 或普通 dict 规范化函数

验收：

- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
- form-data 包含 `tenantCode/page/pageNum`。
- mock 成功响应能解析分页和人员列表。
- mock 错误响应能归一化为稳定错误类型。

### Step 1C：诊断脚本，最后做

交付：

- `backend/scripts/xg_user_api_probe.py`

验收：

- 默认不调用真实API。
- `--dry-run` 打印请求摘要。
- `--format=text|json` 均可用。
- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。

### Step 2：live probe，等租户Code

验收：

- 使用本校真实 `tenantCode`。
- 只请求一页一条。
- 产出脱敏字段覆盖报告。
- 根据字段覆盖再开“是否接入 Provider”的新决策门。

---

## 更优化的替代方案

推荐采用 **“诊断客户端先行，业务 Provider 后置”**：

```text
现在实现：
  generate_sign
  XGUserAPIClient
  xg_user_api_probe.py
  mock tests

暂不实现：
  RealUserDataProvider
  数据同步入库
  全量分页
  班级/辅导员自动映射
  宿舍清退状态接入
```

这样做的理由是：当前已知信息足够验证认证和接口结构，但不足以证明业务字段完整。把业务 Provider 后置，可以避免把一个“能读人员列表”的接口过早包装成“能支撑毕业离校业务”的数据源。

---

## 最终建议

Codex 建议 Claude 继续执行 Step 1，但按以下边界落地：

1. 先做 `generate_sign()` 和官方样例测试。
2. 再做请求构造、响应解析、mock 错误测试。
3. 最后做诊断脚本，默认 dry-run/text 输出，支持 JSON。
4. 没有本校 `tenantCode` 前，不做真实 API 请求。
5. live probe 只产出字段覆盖报告，不直接触发 Provider 接入。

**批准状态：** 可以开始 Step 1A / Step 1B；Step 1C 可实现但 live 调用必须等待 `tenantCode`。
