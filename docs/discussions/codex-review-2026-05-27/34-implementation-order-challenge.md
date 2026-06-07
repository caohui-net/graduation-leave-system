# 实施顺序挑战 - Codex审查请求

**创建时间：** 2026-06-01T01:45  
**审查类型：** 实施策略审查  
**审查人：** Codex

---

## 审查背景

Codex已完成student-application页面方案审查，给出"需要小幅调整后再实施"结论。

**当前计划的实施顺序：**
1. 创建student-application.ts（表单逻辑+角色保护+错误格式化）
2. 创建student-application.wxml（表单UI）
3. 创建student-application.wxss（样式）
4. 创建student-application.json（页面配置）
5. 注册页面到app.json
6. 修改login.ts添加角色路由

---

## 需要你批判性审查的问题

### 问题1：实施顺序是否合理？

**当前方案：** 先完整实现student-application页面（4个文件），最后修改login.ts路由

**潜在问题：**
- 如果先实现页面但不修改路由，学生登录后无法访问新页面
- 如果先修改路由但页面不存在，会导致404错误
- 4个文件一次性创建，如果中途发现问题，回滚成本高

**替代方案A：** 先修改login.ts路由（添加条件判断但暂时注释），再实现页面，最后取消注释
**替代方案B：** 先创建空页面骨架（4个文件最小化内容），注册+路由，再逐步填充逻辑
**替代方案C：** 保持当前顺序，但在app.json注册后立即测试404，确认路由前页面可访问

**你的任务：** 批判当前顺序，指出风险，推荐最优方案

---

### 问题2：角色保护的实施时机？

**当前方案：** 在student-application.ts的onLoad中检查角色

```typescript
onLoad() {
  const userInfo = app.globalData.userInfo;
  if (!userInfo || userInfo.role !== 'student') {
    wx.reLaunch({ url: '/pages/login/login' });
    return;
  }
  // ...
}
```

**潜在问题：**
- 如果login.ts路由已正确实现，角色保护是否冗余？
- 如果用户直接输入URL或通过其他方式访问，角色保护是必要的
- 但如果login.ts路由有bug，角色保护会掩盖路由问题

**替代方案A：** 先不实现角色保护，依赖login.ts路由，测试通过后再添加防御性保护
**替代方案B：** 先实现角色保护，即使login.ts路由有bug也能防御
**替代方案C：** 实现角色保护，但添加console.warn提示"不应通过此路径访问"

**你的任务：** 分析角色保护的必要性和实施时机

---

### 问题3：错误处理的实施优先级？

**当前方案：** 在student-application.ts中实现错误格式化函数

```typescript
function formatError(err: any): string {
  if (err.error?.code === 'DORM_BLOCKED') {
    return `宿舍清退未完成：${err.error.blocking_reason || '请联系宿管'}`;
  }
  if (err.error?.code === 'CONFLICT') {
    return '您已有待审批或已通过的申请';
  }
  if (err.error?.code === 'VALIDATION_ERROR') {
    return err.error.details || '表单验证失败';
  }
  return err.error?.message || err.message || '操作失败';
}
```

**潜在问题：**
- 这个函数只在student-application页面使用，是否应该提取到services/api.ts作为通用工具？
- 如果未来其他页面也需要类似错误处理，会导致代码重复
- 但如果现在提取，可能过度设计（YAGNI原则）

**替代方案A：** 先在页面内实现，等第二个页面需要时再提取
**替代方案B：** 现在就提取到api.ts，作为ApiClient的静态方法或独立函数
**替代方案C：** 实现为页面内函数，但添加TODO注释标记未来重构点

**你的任务：** 权衡YAGNI vs DRY，推荐错误处理的实施策略

---

### 问题4：表单验证的实施范围？

**当前方案：** 提交时验证reason非空且trim后非空，leave_date非空

**潜在问题：**
- 是否需要验证leave_date不早于今天？（虽然picker设置了start=today，但用户可能修改系统时间）
- 是否需要验证reason长度上限？（避免超长文本导致UI问题或数据库截断）
- 是否需要验证reason不包含特殊字符？（防止XSS或SQL注入，虽然后端应该处理）

**替代方案A：** 只验证非空，其他交给后端
**替代方案B：** 添加长度验证（如reason最多500字）
**替代方案C：** 添加日期验证（不早于今天）+ 长度验证

**你的任务：** 确定前端验证的合理边界

---

### 问题5：成功后跳转的实施细节？

**当前方案：** 成功后showToast，然后redirectTo到详情页

```typescript
wx.showToast({ title: '提交成功', icon: 'success' });
setTimeout(() => {
  wx.redirectTo({ url: `/pages/detail/detail?id=${res.application_id}` });
}, 1500);
```

**潜在问题：**
- 1500ms延迟是否合理？用户可能觉得慢
- 使用redirectTo会清空页面栈，用户无法返回表单页（但这可能是期望行为）
- 如果用户在延迟期间点击其他按钮，可能导致竞态条件

**替代方案A：** 缩短延迟到500ms
**替代方案B：** 不延迟，直接跳转（toast可能看不到）
**替代方案C：** 使用navigateTo而非redirectTo，允许用户返回
**替代方案D：** 在跳转前禁用所有交互（添加全屏遮罩）

**你的任务：** 评估跳转时机和方式的用户体验影响

---

## 审查要求

1. **批判性思考：** 不要接受当前方案，指出所有潜在问题
2. **提供证据：** 引用微信小程序最佳实践、常见坑点、性能考虑
3. **权衡分析：** 对每个问题的替代方案进行利弊分析
4. **明确推荐：** 给出你认为最优的实施策略，并说明理由
5. **发现新问题：** 如果发现我没有提到的问题，请指出

---

## 期望输出

```markdown
# 问题1：实施顺序
**风险分析：** ...
**推荐方案：** ...
**理由：** ...

# 问题2：角色保护
**必要性分析：** ...
**推荐时机：** ...
**理由：** ...

# 问题3：错误处理
**YAGNI vs DRY权衡：** ...
**推荐策略：** ...
**理由：** ...

# 问题4：表单验证
**前端验证边界：** ...
**推荐范围：** ...
**理由：** ...

# 问题5：成功跳转
**UX影响分析：** ...
**推荐方案：** ...
**理由：** ...

# 新发现的问题
**问题描述：** ...
**影响范围：** ...
**推荐方案：** ...
```
