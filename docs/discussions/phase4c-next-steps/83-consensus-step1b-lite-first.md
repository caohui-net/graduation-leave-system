# Step 1A审查与下一步策略 - 最终共识

**日期：** 2026-06-02  
**参与方：** Codex + Claude  
**文档编号：** 83

---

## 审查结论

**状态：** Step 1A通过，达成执行共识

**Step 1A评价：**
- 签名函数实现正确，官方样例测试通过
- 无P0问题
- P1：MD5测试需补固定期望值
- 范围定义：签名函数切片（配置对象移至Step 1B-lite）

---

## 策略共识

**执行顺序：Step 1A补丁 → Step 1B-lite → Step 1C**

**关键决策：**
1. ✅ 不先写孤立Step 1C诊断脚本
2. ✅ 先实现Step 1B-lite提供可复用客户端
3. ✅ Step 1C调用Step 1B-lite避免逻辑重复

**共识理由：**
- 诊断脚本需完整请求构造/签名/脱敏逻辑
- 孤立实现会重复Step 1B核心代码
- 复用客户端保证签名/脱敏/错误分类一致性

---

## 执行计划

### 第一步：Step 1A补丁（立即）

**文件：** `backend/apps/users/tests/test_xg_user_client.py`

**修改：**
```python
def test_md5_encryption(self):
    """测试md5加密（固定期望值）"""
    sign = generate_sign('secret', '1234567890', 'random', 'md5')
    self.assertEqual(sign, '2a471e23465cf11561ef7455fff00a86')
```

**验证：** 4/4 tests passed

---

### 第二步：Step 1B-lite（随后）

**范围：**
- `XGUserAPIConfig`：环境读取+校验+归一化
- `XGUserAPIClient`：headers构造+form-data构造+单页请求
- 响应解析：协议层+分页+人员列表（宽松采样）
- Mock测试：配置校验+请求构造+成功/错误场景

**排除：**
- 分页循环、重试机制、Provider接入、数据库写入

---

### 第三步：Step 1C诊断脚本（最后）

**范围：**
- 环境检查+官方样例自检
- Dry-run默认（请求摘要不发网络）
- Live probe硬门禁（XG_RUN_LIVE_API_TEST=1+单页）
- 错误分类+脱敏输出

**复用：** Step 1B-lite的客户端能力

---

## 文档一致性确认

- ✅ doc 80：审查请求
- ✅ doc 81：Codex响应
- ✅ doc 82：Claude响应
- ✅ doc 83：共识文档（本文档）
- ⏳ PROJECT-SUMMARY.md：待执行后更新
- ⏳ session-context.json：待执行后更新

---

## 执行授权

根据用户指令"在得到统一可靠可行的执行方案后，无需我的干预，直接执行"：

✅ Codex与Claude已达成完整共识  
✅ 执行方案明确可行  
✅ 无分歧点  

**授权执行，无需用户额外确认。**
