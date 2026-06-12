# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2026-06-12

### Added
- **批量审批功能** - 宿管员和辅导员可批量处理审批
  - 复选框多选：待审批项左侧显示复选框
  - 顶部全选栏：一键全选当前页 + 已选计数显示
  - 底部操作栏：批量通过/驳回按钮（选中时显示）
  - 确认弹窗：统一审批意见输入 + 操作确认
  - 后端API：`POST /api/approvals/batch-action/` 原子事务保障
  - 移动端优化：顶部信息展示 + 底部操作按钮布局

### Changed
- API端点数量：19 → 20
- 项目完成度：95% → 98%

### Technical Details
- 后端：Django事务原子性（全部成功或全部失败）
- 前端：响应式设计（PC+移动端统一实现）
- 权限：按审批人自动过滤，确保仅处理自己的待审批

## [1.0.0] - 2026-06-07

### Added
- 学生在线提交离校申请
- 两级审批流程（辅导员 → 学工部）
- 宿舍管理系统对接
- 微信通知推送
- 附件上传管理
- 草稿保存功能
- 权限控制系统
