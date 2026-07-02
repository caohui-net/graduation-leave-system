# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.2.2] - 2026-07-01

### Added
- **📐 前端设计规范文档**
  - 新增：DESIGN.md 完整设计系统文档
  - 内容：颜色系统、字体系统、组件库、布局规范、响应式设计
  - 目的：统一前端设计标准，提升开发效率

### Fixed
- **🐛 留校业务辅导员分配逻辑**
  - 问题：辅导员胡乐(20220052)被错误分配到留校业务审批
  - 修复：views.py添加过滤逻辑，排除胡乐老师参与留校业务
  - 数据清理：删除97条历史审批记录
- **🐛 学生信息显示问题**
  - 问题：切换申请类型后，学生姓名/学号显示为"-"
  - 修复：selectApplicationType()函数添加学生信息填充逻辑

## [1.2.1] - 2026-06-30

### Fixed
- **🔴 关键修复：草稿创建功能修复**
  - 问题：学生提交申请时返回500错误，草稿无法创建
  - 根因：
    - 前端：登录后未保存JWT token到localStorage
    - 前端：apiLogin函数返回对象中缺少access_token字段
    - 数据库：applications.class_id字段NOT NULL约束，但部分用户class_id为null
  - 方案：
    - 数据库：applications.class_id改为nullable（向后兼容）
    - 后端：models.py更新字段定义为nullable
    - 前端：doLogin函数中保存token到localStorage
    - 前端：apiLogin函数返回对象中添加access_token字段
    - 前端：更新api.js版本号v=20260630
  - 回滚方案：backups/rollback_20260630.sql
  - 数据备份：backups/prod_applications_20260630_025243.json (2.7M)

## [1.2.0] - 2026-06-14

### Changed
- **💡 重大功能升级：Excel导出范围扩展**
  - 问题：导出仅包含已提交申请的学生（1846人），无法统计全体学生
  - 需求：导出所有学生数据（6002人），包括未提交申请的学生
  - 方案：
    - 后端：从 `Application` 表改为 `User` 表为主表，LEFT JOIN最新申请
    - 未提交学生显示"未提交"状态，其他审批字段为空
    - Excel标题：`审批数据` → `学生数据`
    - 文件名：`approvals_*.xlsx` → `students_*.xlsx`
  - 数据范围：
    - 已提交：1862人（含申请详情、审批信息）
    - 未提交：4140人（显示基本信息，标记"未提交"）
  - 影响范围：学工部/管理员导出功能

### Fixed
- **🔴 关键修复：导出行数限制**
  - 问题：Excel导出最多1000条，实际需要导出全部数据
  - 根因：三层限制
    - 前端：`limit=1000`
    - 后端分页：`max_limit=100`
    - 后端导出：`MAX_EXPORT_ROWS=1000` + 切片`[:1000]`
  - 方案：
    - 前端：`limit=1000` → `limit=100000`
    - 后端分页：`max_limit=100` → `max_limit=100000`
    - 后端导出：移除行数限制和切片操作
  - 影响范围：导出功能，支持导出最多100000条记录

### Performance
- **⚡ 性能优化：导出查询优化（10-20倍加速）**
  - 问题：N+1查询导致导出缓慢（18,007次数据库查询）
  - 方案：批量预加载数据
    - 使用 `Subquery` 获取每个学生的最新申请ID
    - 使用 `Prefetch` 预加载审批记录
    - Python端建立映射，循环中无DB查询
  - 效果：
    - 查询次数：18,007 → 3-4次
    - 导出速度：30-60秒 → 2-5秒
  - 影响范围：导出6002条学生数据的性能

### Technical Details
- 后端：重构 `export_approvals()` 函数，从申请表改为用户表为主表
- 后端：优化查询策略，使用子查询和预加载避免N+1问题
- 前端：提升请求limit至100000，支持大批量预览
- 测试：已验证导出6002条学生数据功能正常

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
