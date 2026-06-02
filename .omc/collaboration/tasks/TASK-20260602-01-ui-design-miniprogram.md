# TASK-20260602-01: 微信小程序UI设计优化

**任务ID:** TASK-20260602-01  
**创建时间:** 2026-06-02T07:41:00Z  
**创建者:** Claude  
**主导角色:** Gemini  
**参与角色:** Claude (orchestrator), Codex (reviewer)  
**状态:** open_for_collaboration

---

## 1. 任务目标

根据3张UI参考图片，优化微信小程序的学生申请页、审批列表页、详情页UI设计，并实施改进方案。

## 2. 背景

当前微信小程序已完成基础功能实现（Phase 4B），包括：
- 学生申请页面（基础表单）
- 审批列表页面（基础列表）
- 详情页面（基础信息展示+审批操作）
- 附件管理（上传/下载/删除）

现需要根据参考图片进行UI优化，使界面更美观、易用。

## 3. 输入材料

### 参考图片
1. `docs/微信图片_20260528210617_553_47.jpg` - 离校申请表单页
2. `docs/微信图片_20260528210618_554_47.jpg` - 审批列表页（含Tab切换）
3. `docs/微信图片_20260528210619_555_47.jpg` - 申请详情页（含审批操作）

### 需求分析文档
- `docs/discussions/ui-design-2026-06-02/01-ui-requirements-analysis.md`

### 当前实现代码
- `miniprogram/pages/student-application/` - 学生申请页
- `miniprogram/pages/approvals/` - 审批列表页
- `miniprogram/pages/detail/` - 详情页

## 4. 期望输出

### Phase 1: UI设计方案（Gemini主导）
输出文档：`.omc/collaboration/artifacts/20260602-HHMM-gemini-ui-design-proposal.md`

内容包括：
1. **UI设计方案**（1-2页）
   - 整体设计原则和风格指南
   - 颜色主题和配色方案
   - 组件结构和复用策略
   - 响应式适配方案

2. **技术实现建议**（1页）
   - 关键组件实现方案（Tab切换、时间线等）
   - WXSS样式组织策略
   - 性能优化建议

3. **实施计划建议**（1页）
   - 3个页面的实施优先级和理由
   - 每个页面的预估工作量
   - 分阶段实施方案（如需要）

4. **风险和问题识别**（0.5-1页）
   - 潜在的技术风险
   - UI/UX问题和改进建议
   - 与现有实现的兼容性考虑

### Phase 2: 三方讨论与共识
- Claude和Codex审查Gemini方案
- 讨论并达成共识
- 形成最终实施方案

### Phase 3: 代码实施
- 按共识方案实施UI改进
- 实施完成后再次三方讨论代码
- 确认质量后完成任务

## 5. 任务范围

### 包含内容
- 3个页面的UI优化（学生申请、审批列表、详情）
- WXML/WXSS改进（不修改TS逻辑）
- 用户信息展示、Tab切换、审批时间线等组件

### 不包含内容
- 后端API修改
- 现有TS逻辑重构
- 新功能开发
- 其他页面（登录页已有基础实现）

## 6. 技术约束

- 使用微信小程序原生WXML/WXSS
- 保持现有TS逻辑不变（仅UI层面改动）
- 颜色主题：蓝色主色调（#1890ff或类似）
- 响应式适配：适配不同屏幕宽度
- 性能要求：首屏渲染<500ms

## 7. 协作模式

采用独立分析协议（Section 15）：
1. Gemini首先独立完成UI设计方案（不读其他artifact）
2. Claude和Codex独立审查Gemini方案（可读Gemini artifact）
3. Claude综合Gemini/Codex意见，形成共识文档
4. 按共识方案实施
5. 实施完成后，三方再次讨论代码质量

## 8. 接受标准

- [ ] Gemini完成UI设计方案文档
- [ ] Claude和Codex完成方案审查
- [ ] 三方达成共识并形成最终方案
- [ ] 按方案完成代码实施
- [ ] 代码通过三方审查
- [ ] UI改进在WeChat DevTools中验证通过（如可用）

## 9. 当前状态

**Status:** open_for_collaboration  
**Next:** Gemini创建UI设计方案artifact

---

**创建者备注：** 此任务使用三方协作模式，Gemini为UI设计主导角色，Claude负责协调和综合，Codex负责技术审查。
