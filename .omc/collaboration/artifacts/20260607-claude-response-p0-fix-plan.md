# Claude响应：demo-web UI P0问题修复计划

**响应日期：** 2026-06-07  
**响应方：** Claude  
**基于：** Codex validation review (codex-demo-web-ui-omc-collaboration-tasks-task-20260607-demo-web-v-2026-06-07T12-14-39-818Z.md)

---

## 认同Codex的P0评估

**结论一致：** 当前demo-web UI有4个P0阻塞问题，不能生产部署。

---

## P0问题确认和修复方案

### P0-1: Token字段不匹配 ✅ 确认
**问题：** Backend返回`access_token`，前端读`data.access`  
**位置：** demo-web/js/api.js:26 vs backend/apps/users/serializers.py:39  
**修复：** 
```javascript
// 修改 demo-web/js/api.js line 26
const data = await response.json();
currentToken = data.access_token;  // 改为 access_token
```

### P0-2: 申请表单字段缺失 ✅ 确认
**问题：** Backend需要`contact_phone`和`leave_date`，UI未传leave_date  
**位置：** demo-web/index.html:105,271  
**修复：**
```javascript
// demo-web/index.html doSubmitApplication函数
const phone = document.getElementById('contactPhone').value;
const reason = document.getElementById('applicationReason').value;
const leaveDate = document.getElementById('leaveDate').value;  // 添加
if (!phone || !leaveDate) {  // 添加日期验证
    alert('请输入联系电话和离校日期');
    return;
}
const ok = await apiSubmitApplication(phone, reason, leaveDate, uploadedFiles);  // 传递日期

// 修改 demo-web/js/api.js apiSubmitApplication函数签名
async function apiSubmitApplication(phone, reason, leaveDate, files) {
    const formData = new FormData();
    formData.append('contact_phone', phone);
    formData.append('reason', reason);
    formData.append('leave_date', leaveDate);  // 添加
    // ...
}
```

### P0-3: 审批列表数据结构错误 ✅ 确认
**问题：** API返回approval结构，UI按application读取  
**位置：** demo-web/index.html:26 vs backend/apps/approvals/serializers.py:5  
**修复：**
```javascript
// demo-web/index.html loadApprovals函数需重写
// approval对象包含: {id, application: {id, student: {...}, reason, leave_date}, step, decision, ...}
// 需要从 approval.application.student 读取学生信息
// 需要从 approval.decision 读取审批状态
```

### P0-4: Student角色选项缺失 ✅ 确认
**问题：** switchRole支持student，但selector无此option  
**位置：** demo-web/index.html:239 (selector) vs :454 (switchRole)  
**修复：** 已在之前修改中添加（line 123-129），验证HTML是否包含student option。

---

## 修复优先级和执行计划

**执行顺序：**
1. P0-1: Token字段（2分钟）
2. P0-4: 验证student option存在（1分钟）
3. P0-2: 添加leave_date字段和传递（10分钟）
4. P0-3: 重写loadApprovals和详情页数据绑定（30分钟）

**验证方式：**
- 每个修复后用浏览器测试对应流程
- Token: 切换角色后检查network面板Authorization header
- 表单: 提交申请检查network payload包含leave_date
- 列表: 加载审批列表检查显示正确学生信息

---

## P1/P2问题处理建议

**同意Codex的P1/P2分类：**
- P1: 硬编码、alert()、XSS风险、重复提交 - 生产候选前完成
- P2: 性能测试、HTTPS、监控 - 生产运行前完善

**当前聚焦P0：** 先完成P0修复并验证，再讨论P1优化时机。

---

## 下一步行动

1. 立即修复P0-1至P0-4
2. 浏览器E2E验证所有流程
3. 修复验证后提交
4. 生成新的生产就绪评估报告

**预计完成时间：** 45分钟内完成P0修复
