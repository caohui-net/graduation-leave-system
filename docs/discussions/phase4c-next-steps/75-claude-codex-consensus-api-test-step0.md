# API数据读取测试 - Claude-Codex共识（Step 0安全修正）

**日期：** 2026-06-02  
**参与方：** Codex + Claude  
**文档编号：** 75

---

## 共识结论

**状态：** 达成共识，开始执行Step 0安全修正

---

## 关键共识点

### 1. 签名算法已确认

**Codex担心：** 签名算法缺失，不能靠猜测实现。

**用户提供：** 官方签名算法（字典排序+拼接+sha1/md5）

**共识：** ✅ 问题已解决，可以基于确认算法实现

---

### 2. P0凭证泄露必须立即修正

**Codex指出：** 69号文档暴露真实凭证。

**Claude同意：** 完全接受，立即修正。

**共识：** ✅ Step 0优先执行（在代码实现前）

---

### 3. 实现架构

**Codex建议：** 独立诊断脚本 + Mock客户端 + 单元测试

**Claude接受：** 完全同意，不把真实API放入CI

**共识架构：**
```
backend/scripts/xg_user_api_probe.py        # 诊断脚本
backend/apps/users/integrations/xg_user_client.py   # 客户端
backend/apps/users/tests/test_xg_user_client.py     # Mock测试
backend/.env.example                         # 模板
```

---

### 4. 执行优先级

**共识顺序：**
1. **Step 0：** 安全修正（修改69号文档+创建.env.example）
2. **Step 1：** 实现诊断客户端
3. **Step 2：** 实现Mock测试
4. **Step 3：** 可选Live验证
5. **Step 4：** 决策门（是否接入Provider）

---

## Step 0 执行计划

### 修改1：修正69号文档

**文件：** `docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md`

**修改：** 行24-28，凭证替换为占位符

---

### 修改2：创建环境变量模板

**文件：** `backend/.env.example`（新建）

**内容：** API配置变量+占位符

---

### 修改3：验证.gitignore

**检查：** 确认 `.env` 已在忽略列表

---

## 验收标准

- [ ] 69号文档不再包含真实凭证
- [ ] `.env.example` 已创建
- [ ] `.gitignore` 包含 `.env` 规则

---

**下一步：** 执行Step 0修改
