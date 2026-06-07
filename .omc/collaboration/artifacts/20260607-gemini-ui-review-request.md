# Gemini UI/UX Review Request

**Date:** 2026-06-07  
**Reviewer:** Gemini  
**Requester:** Claude (team-lead)

---

## Context

demo-web UI已完成基础API集成，但需要UI/UX优化达到生产标准。

**Backend API:** http://localhost:8001  
**Demo UI:** http://localhost:8080 (demo-web/index.html)

---

## Completed API Integration

api-integrator agent完成：
1. ✅ approve/reject API调用 (demo-web/index.html:89-103)
2. ✅ 状态映射 pending_dorm_manager/pending_counselor/approved/rejected (index.html:422-432)
3. ✅ 附件上传API (demo-web/js/api.js:102-147)

---

## Production Standards Gap

### 1. User Feedback - 使用alert()不够专业
**Current:** `alert('审批通过')` / `alert('审批失败')`  
**Need:** 内联消息提示（成功/错误/加载状态）

### 2. Loading States - 缺少加载状态
**Current:** 按钮点击后无反馈  
**Need:** 按钮禁用+加载提示，防止重复提交

### 3. Error Details - 错误信息太泛化
**Current:** 只显示"审批失败"  
**Need:** 具体错误原因（网络错误/权限不足/参数错误）

### 4. Data Loading - 列表数据仍为静态mock
**Current:** 硬编码APP-001/APP-002  
**Need:** 从apiGetApprovals()加载真实数据

### 5. Detail View - 申请详情未关联真实数据
**Current:** currentApprovalId未初始化  
**Need:** 点击列表项→设置currentApprovalId→显示详情

---

## Review Request

**请Gemini审查demo-web/index.html并提供：**

1. **UI/UX改进方案**
   - 替换alert()为内联消息组件
   - 添加按钮加载状态（禁用+spinner/文字变化）
   - 设计错误消息显示区域
   - 改进空状态/加载状态设计

2. **数据流完整性检查**
   - 审批列表加载流程 (apiGetApprovals → 渲染列表)
   - 点击列表项 → 设置currentApprovalId → 跳转详情页
   - 详情页数据绑定（基本信息+审批记录timeline）

3. **生产就绪度评估**
   - 响应式设计检查（移动端/桌面端）
   - 无障碍访问（ARIA标签/键盘导航）
   - 错误处理覆盖率
   - 用户体验流畅度

---

## Expected Output

**Gemini审查文档应包含：**
- 现状分析（问题清单+严重程度）
- 改进方案（UI组件设计+代码实现建议）
- 优先级排序（P0必须修复/P1推荐/P2可选）

**格式：** Markdown，保存到 `.omc/collaboration/artifacts/20260607-gemini-ui-review-response.md`
