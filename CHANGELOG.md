# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.1] - 2026-06-13 ⚠️ 重要更新

### Fixed
- **🔴 重要修复：审批筛选逻辑错误**
  - 问题：审批通过后，"通过"标签列表无数据
  - 根因：双重筛选冲突
    - `loadApprovals()`按审批决策筛选（`approval.decision`）
    - `renderApplications()`再按申请状态筛选（`application.status`）
    - 宿管审批后：`approval.decision='approved'` 但 `application.status='pending_counselor'`
    - 第二次筛选失败导致记录被过滤掉
  - 方案：
    - 在`loadApprovals()`中按当前用户的审批决策筛选（客户端筛选）
    - 删除`renderApplications()`中的重复状态筛选
    - 添加类型转换确保`approver_id`匹配（`String()`包装）
  - 影响范围：所有管理员（宿管/辅导员）的审批列表筛选功能

- **🔴 重要修复：详情页重复显示问题**
  - 问题：申请详情页基本信息和审批记录重复显示
  - 根因：静态mock卡片与动态生成内容同时渲染
  - 方案：创建专用`detail-container`容器，首次进入时删除静态卡片
  - 影响范围：所有管理员查看申请详情页面

- **🔴 重要修复：审批按钮消失问题**
  - 问题：修复重复显示后，审批操作按钮被意外删除
  - 根因：DOM操作误删`approval-section`审批按钮区
  - 方案：保留`approval-section`，只替换内容区域
  - 影响范围：宿管员/辅导员审批操作

- **楼栋号和房间号显示缺失**
  - 问题：详情页楼栋和房间号字段显示为`-`
  - 根因：序列化器未包含`building`和`room_number`字段
  - 方案：
    - `ApplicationSerializer`（详情API）：添加字段
    - `ApplicationListSerializer`（列表API）：添加字段
    - 配置`allow_null=True`支持空值
  - 影响范围：申请详情页、列表页

### Technical Details
- 前端：筛选逻辑重构，按审批决策而非申请状态筛选
- 前端：DOM结构优化，避免innerHTML覆盖关键元素
- 后端：序列化器字段统一，支持关联查询`source='student.building'`
- 测试：已验证列表加载、详情显示、审批功能、筛选功能正常

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
