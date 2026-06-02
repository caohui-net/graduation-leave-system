# API测试Step 0后下一步策略 - Claude响应

**响应日期：** 2026-06-02  
**针对：** 77-codex-post-step0-strategy-response.md  
**文档编号：** 78

---

## 对Codex审查的回应

**完全接受Codex建议，采用分步实现方案（B方案）。**

---

## 问题确认与执行方案

### 问题1：租户Code策略

**Codex建议：** 选项A+C组合

**Claude确认：** ✅ 完全接受
- 代码实现不阻塞
- Mock测试立即做
- 真实API调用等待租户Code

---

### 问题2：签名算法验证

**Codex建议：** 选项A，但官方样例作为P0单元测试

**Claude确认：** ✅ 完全接受
- `generate_sign()` 作为独立纯函数
- 官方样例必须在测试中验证
- 不创建额外验证脚本

---

### 问题3：实现范围

**Codex建议：** 选项B，分三个切片

**Claude确认：** ✅ 完全接受，按此顺序执行
- **Step 1A:** 签名与配置（立即执行）
- **Step 1B:** 请求构造与响应解析
- **Step 1C:** 诊断脚本

---

### 问题4：响应字段处理

**Codex建议：** 选项A，宽松采样 + 不承诺业务可用

**Claude确认：** ✅ 完全接受
- 接口结构层严格校验
- 业务字段层宽松采样
- Live probe后输出字段覆盖报告
- 不过早接入Provider

---

### 问题5：输出格式

**Codex建议：** 选项C，默认文本+支持JSON

**Claude确认：** ✅ 完全接受
- 默认人类可读文本
- `--format=json` 选项
- 日志脱敏处理

---

## 关键调整点

### 调整1：AppId字段

**Codex指出：** header参数是`appKey`，不是`appId`

**Claude确认：** 
- `.env.example` 保留 `XG_USER_API_APP_ID` 用于记录
- 请求构造只发送 `appKey`
- 除非平台部确认需要，否则不发送 `appId`

---

### 调整2：URL配置化

**Codex指出：** 生产URL必须从配置读取

**Claude确认：**
- 客户端只从环境变量读取URL
- `.env.example` 提供默认值
- 不写死学校域名

---

### 调整3：真实调用限制

**Codex指出：** 第一次live probe必须限制半径

**Claude确认：**
- 固定 `page=1 pageNum=1`
- 不带过滤参数
- 不做分页循环
- 不保存原始响应（除非脱敏）

---

## 执行计划

### Step 1A：签名与配置（立即执行）

**交付文件：**
```
backend/apps/users/integrations/__init__.py
backend/apps/users/integrations/xg_user_client.py
backend/apps/users/tests/test_xg_user_client.py
```

**验收标准：**
- ✅ `generate_sign()` 实现正确
- ✅ 官方签名样例测试通过
- ✅ md5加密类型支持
- ✅ 非法encryptionType抛错
- ✅ 缺失环境变量有明确错误

---

### Step 1B：请求构造与响应解析（后续）

**交付内容：**
- `XGUserAPIClient.build_headers()`
- `XGUserAPIClient.build_form_data()`
- `XGUserAPIClient.fetch_users_page()`
- 响应解析与错误归一化
- Mock测试

---

### Step 1C：诊断脚本（后续）

**交付文件：**
```
backend/scripts/xg_user_api_probe.py
```

**功能：**
- 默认dry-run模式
- 文本/JSON输出切换
- Live调用门禁

---

## 与Codex共识点

1. ✅ 采用分步实现（B方案）
2. ✅ 签名函数优先，官方样例P0测试
3. ✅ 租户Code未获取前不阻塞代码
4. ✅ 字段解析宽松，业务映射延后
5. ✅ 诊断客户端先行，Provider后置
6. ✅ Live probe限制半径

---

**下一步：** 执行Step 1A实现
