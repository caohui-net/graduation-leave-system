# API数据读取测试方案 - 审查请求

**创建时间：** 2026-06-02  
**审查类型：** 技术方案设计  
**文档编号：** 69

---

## 审查目标

设计并实现学工系统人员信息API的数据读取测试方案。

---

## 背景信息

### API基本信息

**生产环境接口：**
```
URL: https://xuegongmj.hgnu.edu.cn/api/open-api/user-center/tenant/auth-user-info
Method: POST
```

**认证凭证：**
- AppId: ${XG_USER_API_APP_ID}
- AppKey: ${XG_USER_API_APP_KEY}
- AppSecret: ${XG_USER_API_APP_SECRET}

**说明：** 真实凭证存储在 `backend/.env` 中，不提交到版本库。

### 认证要求

**Header参数：**
- `appKey`: 应用ID（必填）
- `timestamp`: Unix时间戳（必填）
- `randStr`: 随机字符串（必填）
- `sign`: 认证签名（必填，算法未知）
- `encryptionType`: 加密类型，sha1或md5，默认sha1（可选）

**Form-Data参数：**
- `tenantCode`: 租户Code（必填）
- `page`: 当前页，默认1（必填）
- `pageNum`: 每页显示条数，默认10（必填）
- 其他过滤参数（name, number, phone等）可选

### 响应格式

```json
{
    "code": 200,
    "msg": "success",
    "data": {
        "current_page": 1,
        "data": [...],
        "total": 4311,
        "per_page": "1"
    }
}
```

---

## 待讨论问题

### 1. 签名算法推断

文档中提到"请参见签名校验部分"但未给出具体算法。需要推断可能的签名算法：

**候选方案：**
- **A. HMAC-SHA1：** `sign = HMAC-SHA1(appSecret, appKey + timestamp + randStr)`
- **B. 拼接SHA1：** `sign = SHA1(appKey + timestamp + randStr + appSecret)`
- **C. 参数排序SHA1：** `sign = SHA1(sorted_params + appSecret)`

**问题：**
- 哪种算法最可能正确？
- 如果首次测试失败，如何快速验证其他算法？
- 是否需要联系"平台部"获取准确算法文档？

### 2. 测试脚本组织

**候选方案：**

**A. 独立测试脚本（推荐）：**
```
backend/scripts/test_api_integration.py
backend/scripts/api_client.py  # 可复用的API客户端类
```

优点：
- 独立于Django测试框架，可快速迭代
- 便于手动调试和日志输出
- 可直接运行不需要Django环境

缺点：
- 不在pytest测试套件中

**B. Django测试用例：**
```
backend/apps/integration/tests/test_external_api.py
```

优点：
- 与现有测试体系一致
- 可使用Django测试工具

缺点：
- 需要完整Django环境
- 调试相对复杂

**问题：**
- 选择哪种组织方式？
- 是否需要两者都实现（脚本用于调试，测试用例用于CI）？

### 3. 测试范围

**最小测试范围（MVP）：**
1. **连通性测试：** 验证网络可达性
2. **认证测试：** 验证签名算法正确性（可能需要多次尝试）
3. **数据获取测试：** 成功获取第1页数据
4. **数据格式验证：** 验证响应字段完整性

**扩展测试范围（可选）：**
5. 分页测试
6. 过滤参数测试（按学号、姓名等）
7. 错误处理测试（无效签名、无效租户等）
8. 性能测试（响应时间）

**问题：**
- 第一阶段实现哪些测试？
- 是否需要Mock测试（避免频繁调用生产API）？

### 4. 租户信息

**已知信息：**
- 示例中租户Code为 `C10026`
- 我们的租户Code是什么？

**问题：**
- 需要从哪里获取我们的租户Code？
- 如果不知道，如何测试（是否可以从API响应中获取）？

### 5. 安全性

**敏感信息处理：**
- AppSecret不应硬编码在代码中
- 应使用环境变量或配置文件

**问题：**
- 测试脚本如何读取敏感信息（.env? settings.py?）
- 是否需要在.gitignore中添加配置文件？

### 6. 错误处理策略

**可能的错误场景：**
- 网络超时
- 签名错误（401/403）
- 租户Code无效
- API限流

**问题：**
- 测试脚本应如何处理这些错误？
- 是否需要重试机制？

---

## 期望审查输出

### Codex需要提供：

1. **签名算法推断：**
   - 最可能的签名算法（基于常见开放平台实践）
   - 备选算法列表
   - 验证思路

2. **测试脚本组织建议：**
   - 推荐的目录结构
   - 文件命名规范
   - 是否需要API客户端抽象类

3. **测试范围优先级：**
   - MVP测试清单
   - 可选扩展测试
   - 测试执行顺序

4. **租户信息获取策略：**
   - 如何获取租户Code
   - 测试数据准备方案

5. **安全性最佳实践：**
   - 敏感信息存储方式
   - .gitignore配置

6. **实现步骤：**
   - 分步实现计划
   - 每步验收标准

---

## 参考文档

- API文档：`docs/api说明.txt`
- 数据对接文档：`docs/数据对接说明文档.md`
- 项目总结：`docs/PROJECT-SUMMARY.md`

---

**提交给：** Codex  
**期望响应文档：** `70-api-data-reading-test-codex-response.md`
