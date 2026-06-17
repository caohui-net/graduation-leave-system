# 完善管理员端附件显示功能

## Goal

管理员（宿管、辅导员、学工部）在审批流程中能查看附件状态、数量，并预览附件内容。PC端与移动端体验一致。

## Requirements

**FR1: 管理员列表显示附件**
- 宿管员/辅导员/学工部待审批列表显示📎图标+附件数量（复用学生端逻辑）

**FR2: 审批详情页附件预览**
- 显示附件列表（文件名、大小）
- 提供预览/下载按钮
- 复用现有`previewAttachment()`/`downloadAttachment()`函数

**FR3: 移动端适配**
- 图标可见
- 按钮触摸友好（≥44px）

## Acceptance Criteria

- [ ] 宿管/辅导员/学工部列表显示"📎 2个附件"
- [ ] 审批详情页显示附件列表，预览/下载正常
- [ ] Chrome DevTools移动模拟测试通过

## Implementation Scope

**修改文件：**
- `demo-web/index.html`: 管理员列表渲染（3处）、详情页附件区域

**已有可复用：**
- `attachment_count`字段（API已返回）
- `previewAttachment()`/`downloadAttachment()`函数
- 附件渲染逻辑（行288-290，446-454）

**不修改：**
- 后端API（已完成）
- 学生端UI
