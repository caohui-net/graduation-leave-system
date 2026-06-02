# API测试Step 1分步实现 - Claude-Codex共识

**日期：** 2026-06-02  
**参与方：** Codex + Claude  
**文档编号：** 79

---

## 共识结论

**状态：** 达成共识，执行Step 1A（签名与配置切片）

---

## 关键共识

### 1. 实现策略

**Codex建议：** 分步实现（B方案）

**Claude接受：** ✅ 完全同意

**共识方案：**
- Step 1A: 签名与配置
- Step 1B: 请求构造与响应解析
- Step 1C: 诊断脚本

---

### 2. 租户Code策略

**共识：** A+C组合
- 代码实现不等待
- Mock测试立即做
- 真实API调用等待租户Code

---

### 3. 签名验证

**共识：** 官方样例作为P0单元测试
- `generate_sign()` 纯函数
- 必须通过官方样例验证
- 支持sha1/md5

---

### 4. 字段处理

**共识：** 宽松采样策略
- 接口结构严格
- 业务字段宽松
- Live后输出覆盖报告

---

## Step 1A 执行计划

### 交付文件

```
backend/apps/users/integrations/__init__.py
backend/apps/users/integrations/xg_user_client.py
backend/apps/users/tests/test_xg_user_client.py
```

### 验收标准

- [ ] `generate_sign()` 实现
- [ ] 官方样例测试通过
- [ ] md5支持
- [ ] 错误处理
- [ ] 配置校验

---

**下一步：** 执行Step 1A实现
