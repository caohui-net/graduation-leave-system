# API数据读取测试方案 - Codex审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**审查类型：** 技术方案设计  
**针对：** 69-api-data-reading-test-review-request.md  
**说明：** 原请求期望输出 `70-api-data-reading-test-codex-response.md`，但本目录已有 `70-codex-post-phase2b-step1-next-strategy-response.md`；为避免覆盖既有讨论文档，本响应使用编号 `73`。

---

## 审查结论

**结论：需要修改后再执行生产API读取测试。**

方向上可以做“独立诊断脚本 + 可Mock客户端 + 后续接入Provider”的小范围验证，但当前方案有两个硬阻塞：

1. **P0：审查请求文档暴露了疑似真实 `AppId/AppKey/AppSecret`，应立即从文档中移除并推动凭证轮换。**
2. **P1：签名算法不能靠猜测进入正式实现；最多允许在一次性诊断脚本中按候选算法快速验证，正式代码必须等待平台部提供签名校验文档或可确认的样例。**

另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。

---

## 发现的问题

### P0：凭证已进入讨论文档，应先止血

**位置：** `docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:24-28`

文档中包含疑似真实生产凭证。即使仓库当前是私有，也不应把第三方API密钥写入审查文档、历史讨论或测试脚本。

**建议：**

- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
- 联系平台部轮换已暴露凭证；如果无法轮换，至少确认该凭证权限范围、IP白名单、调用限额和审计日志。
- 后续脚本只从环境变量读取，不接受命令行明文参数，避免进入shell history。
- 不在日志中打印完整 header、secret、sign 原文；最多打印尾部4位或哈希摘要。

### P1：签名算法缺失，不能作为正式实现假设

**位置：**
- `docs/api说明.txt:14-19`
- `docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:64-84`

当前文档明确写“请参见签名校验部分”，但仓库内文档没有该部分。候选算法 A/B/C 都只是合理猜测，不能作为生产实现依据。

**建议：**

- 向平台部索要签名校验文档，至少需要：参与签名的字段、字段顺序、是否包含 form-data、secret位置、大小写、编码、输出hex/base64、时间戳单位、randStr长度、签名有效窗口。
- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
- 诊断脚本可以内置候选算法枚举，但必须标注为 `diagnostic only`，不得把猜测算法直接接入业务Provider。

### P1：接口URL存在来源不一致，需要确认环境边界

**位置：**
- `docs/api说明.txt:5-7`
- `docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:20-22`

参考文档写的是 `dev-saas-api.goliveplus.cn` 和 `saas.api.goliveplus.cn`，审查请求写的是学校域名 `xuegongmj.hgnu.edu.cn`。这可能是学校反向代理，也可能是不同网关。

**建议：**

- 先确认应测试“测试环境”还是“生产环境”。
- 优先要求平台部提供测试环境凭证和测试租户。
- 若必须打生产接口，限制为 `page=1&pageNum=1`，只做一次连通/结构验证，不做批量分页。

### P1：租户Code不能从响应中反推

**位置：**
- `docs/api说明.txt:23`
- `docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:130-140`

`tenantCode` 是必填请求参数。没有正确租户Code时，通常无法拿到可用响应，也就不能依赖响应反推。

**建议：**

- 从平台部或学工系统管理员处获取本校真实 `tenantCode`。
- 要求对方确认示例 `C10026` 是否只是文档样例，默认不要使用。
- 测试配置中把 `tenantCode` 作为必填环境变量；缺失时脚本直接退出。

### P2：测试范围需要区分“诊断脚本”和“CI测试”

**位置：** `docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:86-128`

真实生产API调用不应进入常规CI，否则会引入外网依赖、限流、数据泄露和不稳定失败。

**建议：**

- 独立脚本用于人工诊断真实API。
- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。

---

## 对审查要点的回答

### 1. 签名算法推断

在没有官方签名校验章节前，最可能的顺序建议如下：

1. **参数排序SHA1/MD5：** 将参与签名参数按key排序后拼接，再追加或混入 `appSecret`。很多开放平台采用这种方式，且文档提供 `encryptionType=sha1|md5` 更像普通摘要算法选择，而不是HMAC选择。
2. **拼接SHA1/MD5：** `SHA1(appKey + timestamp + randStr + appSecret)` 或 `SHA1(appSecret + appKey + timestamp + randStr)`。
3. **HMAC-SHA1：** 技术上更好，但如果文档只称 `encryptionType` 为 `sha1/md5`，而不是 `hmac-sha1`，优先级略低。

验证思路：

- 先用官方固定样例离线验证算法，不要直接撞生产。
- 如果没有样例，再用 `page=1&pageNum=1` 做最小 live probe。
- 每次只改变一个变量：算法、secret位置、是否包含form-data、timestamp单位、输出大小写。
- 记录响应状态码、业务 `code/msg`、响应耗时，但不记录敏感header。

必须联系平台部获取准确算法文档。靠猜测可以帮助定位问题，但不能作为交付方案。

### 2. 测试脚本组织建议

推荐采用 **A为主，B为辅**：

```text
backend/scripts/xg_user_api_probe.py
backend/apps/users/integrations/xg_user_client.py
backend/apps/users/tests/test_xg_user_client.py
```

职责划分：

- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。

不建议把真实API调用写进Django常规测试套件。若确实需要live测试，使用 pytest marker 或环境变量硬门禁，并默认跳过。

### 3. MVP测试范围

第一阶段只做以下5项：

1. 配置校验：必填环境变量齐全，缺失即退出。
2. 请求构造：header/form-data完整，timestamp/randStr/sign存在。
3. 认证验证：用最小请求验证签名算法。
4. 数据结构验证：确认 `code/msg/data/current_page/data/total/per_page` 存在，`data.data` 是列表。
5. 字段采样：仅检查人员记录是否包含 `name/number/phone/identity_id/department/user_identity/updated_at` 等文档字段。

暂不做：

- 全量分页拉取。
- 性能测试。
- 按姓名/手机号过滤的生产验证。
- 错误签名压测。
- 数据入库同步。

这些应等签名、租户、字段映射确认后再做。

### 4. 租户信息获取策略

必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。

建议向平台部一次性确认：

- 正式环境URL和测试环境URL。
- 本校 `tenantCode`。
- 凭证对应的租户和权限范围。
- 是否限制来源IP。
- 是否有测试租户和测试人员数据。
- 分页最大 `pageNum`、限流策略、时间戳有效窗口。

### 5. 安全性最佳实践

建议新增或使用以下环境变量：

```text
XG_USER_API_URL
XG_USER_API_APP_KEY
XG_USER_API_APP_SECRET
XG_USER_API_TENANT_CODE
XG_USER_API_ENCRYPTION_TYPE=sha1
XG_RUN_LIVE_API_TEST=0
```

当前 `.gitignore` 已覆盖 `.env`、`.env.local`、`.env.*.local`，方向正确。但建议增加一个可提交的示例文件：

```text
backend/.env.example
```

示例文件只放变量名和占位符，不放真实值。

日志规则：

- 不打印 secret。
- 不打印完整 sign。
- 不打印完整手机号、身份证、微信openid。
- 返回样本只输出字段名、记录数和脱敏后的1条样例。

### 6. 错误处理策略

诊断脚本建议处理并分类输出：

- `network_timeout`：默认超时5-10秒，可配置，最多重试1次。
- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感参数。
- `tenant_invalid`：提示租户Code需确认，不继续尝试分页。
- `rate_limited`：HTTP 429 或业务限流码，停止测试。
- `unexpected_schema`：保存脱敏后的字段结构摘要，便于修正文档。

不要对认证失败做大量重试。签名错误重试越多，越可能触发风控或污染审计。

---

## 推荐实现步骤

### Step 0：安全修正

验收标准：

- 69号文档中的真实凭证被替换为占位符。
- 已向平台部发起凭证轮换/确认。
- 本地 `.env` 保存真实值，不提交。

### Step 1：补齐外部信息

验收标准：

- 获得签名校验文档或固定签名样例。
- 获得本校真实 `tenantCode`。
- 确认测试/生产URL边界。

### Step 2：实现诊断客户端

验收标准：

- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
- 日志脱敏。

### Step 3：实现mock测试

验收标准：

- mock成功响应解析。
- mock认证失败、租户错误、超时、schema异常。
- 常规测试不访问真实API。

### Step 4：一次性live验证

验收标准：

- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
- 成功记录响应结构、总数、字段覆盖情况。
- 不保存未脱敏个人信息。

### Step 5：决定是否接入Provider

验收标准：

- 若字段满足学生/辅导员/班级映射需求，再接入真实Provider。
- 若缺少班级、院系、专业、辅导员映射或宿舍清退状态，维持CSV/Mock方案，不把该API误用为完整数据源。

---

## 最终方案

批准一个收窄后的测试方案：

- **先修凭证泄露和外部文档缺口。**
- **实现独立诊断脚本，不进CI。**
- **实现可mock的客户端单元测试，覆盖签名候选和响应解析。**
- **真实API只做最小读取验证，不做全量同步。**
- **签名和租户确认前，不启动生产数据读取实现。**

这能以最小风险确认API可用性，同时不破坏此前已达成的“Mock/CSV不阻塞主流程”的项目策略。
