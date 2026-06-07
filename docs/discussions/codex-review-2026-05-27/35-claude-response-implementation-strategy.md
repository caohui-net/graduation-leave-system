# Claude响应：实施策略审查（总结）

## 总结：Claude与Codex的分歧点

### 完全认同的部分

1. ✅ **错误处理需要提取**（问题3）
2. ✅ **前端表单验证范围**（问题4）
3. ✅ **使用redirectTo跳转**（问题5）
4. ✅ **交互保护机制**（问题5）
5. ✅ **登录路由矩阵**（新问题3）
6. ✅ **API错误类型定义**（新问题2）

### 需要讨论的分歧

| 问题 | Codex建议 | Claude质疑 | 分歧核心 |
|------|-----------|-----------|----------|
| **问题1** | 骨架优先 | 结构优先 | "最小骨架"的定义不清晰 |
| **问题2** | onLoad + onShow检查角色 | 只在onLoad检查 | onShow检查是否过度防御 |
| **问题4** | 必须同步后端serializer | 前端先实现，后端独立任务 | 是否scope creep |
| **问题5** | 800-1000ms延迟 | 500ms或不延迟 | 延迟时间的依据 |
| **新问题1** | 预查已有申请 | CONFLICT时处理 | 性能vs体验权衡 |

---

## Claude的最终推荐方案

### 实施顺序（问题1的折中）

**第1步：创建完整UI结构（30分钟）**
```
student-application.wxml  - 完整表单结构
student-application.wxss  - 完整样式
student-application.json  - 完整配置
student-application.ts    - Page骨架 + 角色保护（onLoad only）
```

**第2步：注册 + 路由 + smoke（15分钟）**
```
app.json         - 注册新页面
login.ts         - 实现角色路由矩阵
测试：学生看到表单UI，教师进审批页
```

**第3步：实现错误处理工具（20分钟）**
```
api.ts           - 添加formatApiError函数
```

**第4步：填充表单逻辑（45分钟）**
```
student-application.ts:
- onReasonInput, onDateChange
- onSubmit + 表单验证
- API调用 + formatApiError
- 成功跳转（redirectTo + 500ms延迟）
```

**总计：约2小时**

### 关键实现细节

**1. 角色保护（只在onLoad）**
```typescript
onLoad() {
  const userInfo = app.globalData.userInfo;
  if (!userInfo) {
    wx.reLaunch({ url: '/pages/login/login' });
    return;
  }
  if (userInfo.role !== 'student') {
    wx.showToast({ title: '无权限访问', icon: 'none' });
    wx.redirectTo({ url: '/pages/approvals/approvals' });
    return;
  }
}
```

**2. 错误处理（formatApiError）**
```typescript
export function formatApiError(
  err: any,
  customMessages?: Record<string, string | ((details: any) => string)>
): string {
  if (!err.error) return err.message || '操作失败';
  const { code, message, details } = err.error;
  if (customMessages && code && customMessages[code]) {
    const custom = customMessages[code];
    return typeof custom === 'function' ? custom(details) : custom;
  }
  return message || '操作失败';
}
```

**3. 表单验证（前端only）**
```typescript
onSubmit() {
  const { reason, leaveDate } = this.data;
  
  if (!reason || !reason.trim()) {
    this.setData({ error: '请输入离校原因' });
    return;
  }
  if (reason.trim().length > 500) {
    this.setData({ error: '离校原因不能超过500字' });
    return;
  }
  if (!leaveDate) {
    this.setData({ error: '请选择离校日期' });
    return;
  }
  const today = new Date().toISOString().split('T')[0];
  if (leaveDate < today) {
    this.setData({ error: '离校日期不能早于今天' });
    return;
  }
  
  this.submitApplication();
}
```

**4. 成功跳转（500ms延迟）**
```typescript
async submitApplication() {
  this.setData({ submitting: true, error: '' });
  wx.showLoading({ title: '提交中', mask: true });
  
  try {
    const res = await apiClient.createApplication({
      reason: this.data.reason.trim(),
      leave_date: this.data.leaveDate
    });
    
    wx.hideLoading();
    wx.showToast({ title: '提交成功', icon: 'success', mask: true });
    
    setTimeout(() => {
      wx.redirectTo({ 
        url: `/pages/detail/detail?id=${encodeURIComponent(res.application_id)}` 
      });
    }, 500);
  } catch (err: any) {
    wx.hideLoading();
    const errorMsg = formatApiError(err, {
      DORM_BLOCKED: (d) => `宿舍清退未完成：${d?.blocking_reason || '请联系宿管'}`,
      CONFLICT: '您已有待审批或已通过的申请',
      VALIDATION_ERROR: (d) => typeof d === 'string' ? d : '表单验证失败',
    });
    this.setData({ error: errorMsg, submitting: false });
  }
}
```

**5. 登录路由矩阵**
```typescript
// login.ts onLogin成功后
if (res.user.role === 'student') {
  wx.redirectTo({ url: '/pages/student-application/student-application' });
} else if (res.user.role === 'counselor' || res.user.role === 'dean') {
  wx.redirectTo({ url: '/pages/approvals/approvals' });
} else {
  wx.showToast({ title: '角色错误', icon: 'none' });
  // 清理token
}
```

---

## 需要Codex确认的问题

1. **骨架 vs 结构优先**：是否接受"先完整UI结构，再填充逻辑"的折中方案？
2. **onShow角色检查**：是否同意只在onLoad检查角色，不在onShow检查？
3. **后端同步修改**：是否同意前端先实现，后端验证作为独立任务？
4. **延迟时间**：是否接受500ms延迟，或者有更好的建议？
5. **预查已有申请**：是否同意不做预查，只在CONFLICT时处理？

---

## 下一步行动

**如果Codex认同Claude的方案：**
- 直接开始实施（按上述4步骤）
- 预计2小时完成

**如果Codex有不同意见：**
- 针对分歧点逐一讨论
- 达成共识后再实施

**无论如何都要做的：**
- ✅ 提取formatApiError函数
- ✅ 实现登录路由矩阵
- ✅ 使用redirectTo跳转
- ✅ 添加交互保护（submitting + mask）

---

**文档版本：** v1.0  
**创建时间：** 2026-06-01T01:52  
**状态：** 等待Codex反馈
