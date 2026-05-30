# 毕业生离校申请审批系统 - 项目总结

## 项目概述

**项目名称：** 毕业生离校申请审批系统  
**项目状态：** Week 0契约已冻结，准备启动Week 1 Day 1  
**当前阶段：** contract-v0.1.md已冻结为v0.1 Final（可执行契约标准）  
**创建日期：** 2026-05-27  
**最后更新：** 2026-05-30

## 项目目标

实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。

## 技术选型

- **平台：** iOS/Android + 微信小程序
- **前端：** React Native + 小程序原生
- **后端：** Python Django 4.2 + Django REST Framework
- **数据库：** PostgreSQL（本项目）+ 外部系统对接（MySQL/SQL Server/Oracle）
- **认证：** 混合认证（学号+密码 + 微信OAuth2）+ 5项安全增强
- **部署：** Docker容器化部署（本地部署，单实例）
- **缓存：** Redis
- **任务队列：** Celery
- **文件存储：** 本地文件系统

## 已完成工作

### 2026-05-27

**需求分析：**
- ✓ 收集业务需求
- ✓ 确认技术选型
- ✓ 明确部署方式（本地部署）
- ✓ 确认系统集成需求（宿舍管理系统）

**系统设计：**
- ✓ 完成系统架构设计
- ✓ 完成数据库设计（7个核心表）
- ✓ 完成API设计（19个API端点）
- ✓ 完成认证授权设计（RBAC权限模型）
- ✓ 完成审批流程设计（状态机、3个审批节点）
- ✓ 完成外部系统集成设计
- ✓ 完成部署架构设计
- ✓ 完成安全设计
- ✓ 完成性能优化设计
- ✓ 完成测试策略

**实施计划：**
- ✓ 完成9个阶段的实施计划
- ✓ 明确每个阶段的任务清单
- ✓ 定义验证标准
- ✓ 识别风险和缓解措施
- ✓ 规划文件结构
- ✓ 预计工期：8-10周

**设计审查（Codex Review）：**

**Round 1 - 架构和数据库审查：**
- ✓ 审查第1-2章（架构、数据库）
- ✓ 识别2个CRITICAL + 8个MAJOR问题
- ✓ 达成共识并应用所有修改
- ✓ 关键决策：PostgreSQL单数据库、外部系统API优先、SQLAlchemy fallback

**Round 2 - 剩余章节审查：**
- ✓ 审查第3、5、7、8、9、10章（API、审批、部署、安全、性能、测试）
- ✓ 识别2个CRITICAL + 21个MAJOR + 6个MINOR问题
- ✓ 达成共识并应用所有修改（5个批次）
- ✓ 批次1：第7章完全重写（PostgreSQL + 单实例部署）
- ✓ 批次2：第3章API设计（微信绑定、版本检查、上传安全）
- ✓ 批次3：第5章审批流程（工作日计算、字段更新、历史审计）
- ✓ 批次4：第8章安全设计（限流、上传安全、审计日志）
- ✓ 批次5：第9-10章性能测试（索引、连接池、TDD、覆盖率）

**Round 3 - P0修改（2026-05-27完成）：**
- ✓ SQL语法标注（添加概念示例说明）
- ✓ 删除多数据库残留引用（PROJECT-SUMMARY、实施计划）
- ✓ 修正外键约束冲突（6处ON DELETE SET NULL改为PROTECT）
- ✓ 清理第6章合并残留
- ✓ 统一工作日时限口径
- ✓ 简化微信绑定安全措施（5项→2项核心+3项可选）
- ✓ 整理requirements依赖（删除多数据库驱动，添加缺失依赖）
- ✓ 删除SQLAlchemy备选方案（第6章）

**Round 3 - 字段补充审查（2026-05-27完成）：**
- ✓ 宿舍对接添加class_name和bed_number字段
- ✓ Codex审查发现3个P2问题并修复
- ✓ 统一class_name标注为可选字段
- ✓ 修正Excel示例表格列错位
- ✓ 统一系统设计文档字段命名（is_checked_out、checkout_date、dorm_building/dorm_room）
- ✓ 达成最终共识（文档22-25）
- ✓ 修正CSV模板文件扩展名（.xlsx → .csv）

**Round 3 - 用户文档审查（2026-05-27完成）：**
- ✓ Codex审查用户文档发现9个问题
- ✓ P0修复：初始密码改为学号+强制修改（安全风险）
- ✓ P1修复：HTTPS改为双模式（HTTP内网+HTTPS公网）、删除id_card参数
- ✓ P2修复：删除Postman引用、明确认证方式、统一审批时限、修改辅导员权限范围、统一性能指标
- ✓ 达成HTTPS/SSL证书问题共识（支持双模式）

### 2026-05-28

**数据对接文档完善：**
- ✓ 更新CSV模板（学生、辅导员、班级映射）
  - 统一使用英文字段名（student_id, employee_id, class_id等）
  - 布尔值格式统一为true/false
  - 匹配v2共识文档规范
- ✓ 创建数据确认清单（docs/数据确认清单.md）
  - 15个待确认问题（6个分类）
  - 5阶段实施计划
  - 风险和应对措施
- ✓ 打包用户文档并提供下载
  - 包含3个文档+4个CSV模板
  - 使用dufs文件服务器共享

**Codex审查流程固化：**
- ✓ 删除重复的自定义skill（.claude/skills/codex-review-dialogue.md）
- ✓ 创建Codex审查流程指南
  - 项目级：docs/Codex审查流程指南.md
  - 全局级：~/.claude/docs/Codex审查流程指南.md
  - 包含完整7步审查流程
  - 添加Load Trigger章节（遵循handoff.md规范）
- ✓ 固化到CLAUDE.md配置
  - 项目级：CLAUDE.md（新建）
  - 全局级：~/.claude/CLAUDE.md（懒加载模式）
  - 统一使用 /oh-my-claudecode:ask codex
  - 明确6个触发条件

**配置文件规范建立：**
- ✓ 在全局CLAUDE.md添加Configuration File Standards章节
  - 要求所有配置文件必须有Load Trigger章节
  - 引用handoff.md作为标准格式
  - 提供操作前检查清单
- ✓ 创建配置文件模板（~/.claude/templates/config-file-template.md）
  - 标准Load Trigger章节
  - 使用说明和示例
- ✓ 项目记忆固化规范要求
  - 添加高优先级指令
  - 修改配置文件前必须先读取handoff.md
- ✓ 达成最终共识（文档26-28）

**微信小程序文档整理：**
- ✓ 整理微信小程序申请说明（docs/微信小程序申请说明.md）
  - 主体选择建议（学校主体 vs 校友会主体）
  - 注册流程（4个步骤）
  - 注意事项和相关文档
- ✓ 整理微信小程序备案说明（docs/微信小程序备案说明.md）
  - 备案所需材料汇总（法人证书、主体负责人、小程序负责人）
  - 备案整体流程
  - 备案信息填写流程
  - 注意事项（手机号、邮箱、授权书要求）

**开发环境修复：**
- ✓ 修复OMC HUD状态栏显示问题
  - 问题：HUD wrapper调用错误函数（renderHud不存在）
  - 修复：更新~/.claude/hud/omc-hud.mjs调用main()而非renderHud()
  - 验证：HUD v4.14.0正常显示

**Phase 1 实施（进行中）：**
- ✓ 创建项目目录结构（backend/、frontend/、docker/）
- ✓ 配置.gitignore（Python、Django、Docker、Node、IDE）
- ✓ 创建Python依赖配置（base.txt、dev.txt、prod.txt）
- ⏸ 安装Django依赖（已暂停）
- ⏸ 创建Django项目（待继续）
- ⏸ 配置settings分层（待继续）
- ⏸ 配置Docker环境（待继续）
- ⏸ 配置Celery（待继续）
- ⏸ 配置开发工具（待继续）

### 2026-05-30

**API阻塞问题解决方案（Codex审查）：**
- ✓ 识别外部API信息缺失阻塞开发问题
- ✓ Claude提出Mock + 接口抽象方案（文档37）
- ✓ Codex审查识别核心偏离：用户主数据不应API化（文档38，评分7/10）
- ✓ Claude完全接受Codex建议并修正方案（文档39）
- ✓ 达成最终共识：Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配（文档40）
- ✓ 关键修正：
  - 用户主数据通过CSV导入到本地数据库（非运行时API查询）
  - ImportSource接口用于数据导入（非运行时查询）
  - 宿舍清退保持实时API查询（可缓存、可降级）
  - 配置细粒度化（USER_DATA_SOURCE/DORM_CHECKOUT_SOURCE/WECHAT_PROVIDER）
  - 工期调整：10周演示版 + 1-2周生产集成缓冲
  - Week 1提前做数据契约和接口设计（避免返工）

**下一步工作批判性讨论（Codex多轮讨论）：**
- ✓ Claude提出方案A：更新实施计划 + Week 1数据契约（文档41）
- ✓ Codex第一轮批判：瀑布式排期、前端后置、Week 10过载（文档42）
- ✓ Claude第一轮回应：质疑v0.1冻结时机、Week 1工作量、前端启动条件（文档43）
- ✓ Codex第二轮回应：澄清v0.1现在冻结、7-10人日现实、Week 4启动条件（文档44）
- ✓ Claude第二轮回应：完全接受Codex修正，达成共识（文档45）
- ✓ 最终共识：纵向切片/MVP优先方法，Week 0-1拆分执行（文档46）
- ✓ 核心决策：
  - Week 0（1-2工作日）：冻结v0.1最小可执行契约
  - Week 1（5工作日）：后端纵向切片（保留最小权限校验）
  - Week 2：CSV导入v1
  - Week 3：核心流程补强 + v0.2契约
  - Week 4-6：微信小程序并行开发
  - Week 6-7：宿舍真实API或降级
  - Week 8-9：UAT和完善
  - Week 10：验收演示（不新增功能）
  - 单端交付（微信小程序优先）
- ✓ 关键修正：
  - 从瀑布式到纵向切片（避免Week 8-10才发现集成问题）
  - 从前端后置到并行开发（Week 4启动，不等后端完全稳定）
  - 从双端到单端（微信小程序优先）
  - 从Week 1数据契约到Week 0（1-2工作日timebox）
  - 保留最小权限校验（纵向切片验证完整链路）

**Week 0 契约冻结工作（进行中）：**
- ✓ 创建contract-v0.1.md初稿（核心DTO、状态枚举、错误码、API端点、样例数据、Mock响应）
- ✓ 创建week-0-1-execution-plan.md初稿（Week 0契约冻结 + Week 1后端纵向切片）
- ✓ Codex第一轮审查发现6个问题：
  - UserDTO字段对教师/学工部不可选
  - 缺少状态机契约表
  - Dorm Mock默认completed掩盖失败路径
  - Seed数据不完整（仅3学生，无密码）
  - API端点数量不一致
  - 降级条件破坏纵向切片
- ✓ 修复全部6个问题（UserDTO可选字段、状态机表、Dorm Mock默认NOT_STARTED、扩展seed到10学生+密码、统一端点描述、优化降级条件）
- ✓ Codex第二轮审查发现3-4个剩余问题：
  - 登录响应DTO不一致（部分字段 vs 完整UserDTO）
  - 缺少503 PROVIDER_UNAVAILABLE样例
  - API端点数量仍不一致（契约6个，计划说5个/4个）
  - 降级条件仍有矛盾（"只做查询API"）
- ✓ 修复全部4个剩余问题：
  - 移除GET /api/applications列表端点（统一为5个HTTP路由）
  - 添加503错误样例（student_id: 2020503）
  - 澄清登录响应为AuthUserDTO子集
  - 修复降级条件保持纵向切片完整性
- ✓ Codex第三轮审查：尚未达标，2个P1阻塞问题
  - P1-1：错误样例覆盖不完整（Section 3定义8个错误码，Section 6.2只有4个样例）
  - P1-2：降级方案逻辑矛盾（风险2说"砍学工部审批"又说"Day 4补学工部审批"）
  - P2-1：术语不一致（"5个HTTP路由" vs "4个API端点"）
  - P2-2：AuthUserDTO未正式定义
- ✓ 修复全部2个P1阻塞问题：
  - P1-1修复：补齐4个缺失错误样例（400 VALIDATION_ERROR, 404 NOT_FOUND, 409 CONFLICT, 500 INTERNAL_ERROR）
  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
- ✓ Codex第四轮审查确认：达到可执行契约标准
  - 错误样例完整性：通过（8个错误码全部有对应样例）
  - 降级方案逻辑：通过（不再有矛盾，保持纵向切片完整性）
  - 剩余3个P2问题不阻塞Week 1启动
- ✓ 冻结contract-v0.1.md为v0.1 Final（可执行契约标准）
- ✓ 创建最终共识文档（文档53）
- ✓ Week 0契约冻结工作完成，准备启动Week 1 Day 1

**Week 1 Day 1实施（2026-05-30完成）：**
- ✓ Django项目骨架
  - manage.py、settings分层（base/dev/prod）、urls、wsgi
  - .env配置文件
- ✓ User模型和认证
  - User模型（user_id、name、role、class_id、is_graduating、graduation_year）
  - UserRole枚举（student、counselor、dean）
  - JWT认证系统（login API）
  - 序列化器（UserSerializer、AuthUserSerializer、LoginSerializer）
- ✓ Seed数据管理命令
  - 10学生（2020001-2020010，默认密码为学号）
  - 2辅导员（T001、T002，默认密码为工号）
  - 1学工部（D001，默认密码为工号）
- ✓ Django admin配置
- ⏳ 验证步骤（需要环境准备：虚拟环境、依赖安装、PostgreSQL）

**Week 1 Day 3-4实施（2026-05-30完成）：**
- ✓ Application模型和API
  - Application模型（application_id、student、reason、leave_date、status、dorm_checkout_status）
  - ApplicationStatus枚举（draft、pending_counselor、pending_dean、approved、rejected）
  - DormCheckoutStatus枚举（completed、pending、not_started、unknown）
  - POST /api/applications（提交申请）
  - GET /api/applications/{id}（查询申请）
- ✓ Approval模型和API
  - Approval模型（approval_id、application、step、approver、decision、comment、decided_at）
  - ApprovalStep枚举（counselor、dean）
  - ApprovalDecision枚举（pending、approved、rejected）
  - POST /api/approvals/{id}/approve（通过审批）
  - POST /api/approvals/{id}/reject（驳回审批）
- ✓ MockDormCheckoutProvider
  - 宿舍清退状态Mock服务
  - 覆盖completed、pending、not_started、unknown四种状态
- ✓ 状态机实现
  - 提交申请→pending_counselor（创建辅导员审批记录）
  - 辅导员通过→pending_dean（创建学工部审批记录）
  - 辅导员驳回→rejected
  - 学工部通过→approved
  - 学工部驳回→rejected
- ✓ 权限校验
  - 学生只能提交和查看自己的申请
  - 辅导员只能审批辅导员步骤
  - 学工部只能审批学工部步骤
- ✓ 错误处理
  - DORM_BLOCKED（宿舍清退未完成）
  - CONFLICT（重复提交申请）
  - FORBIDDEN（无权限）
  - NOT_FOUND（资源不存在）
  - VALIDATION_ERROR（参数验证失败）
- ✓ Django admin配置（Application、Approval）
- ⏳ 验证步骤（需要环境准备：虚拟环境、依赖安装、PostgreSQL）

**Week 1 Day 5实施（2026-05-30完成）：**
- ✓ 端到端测试（test_application_flow.py）
  - 完整流程：登录→提交→辅导员审批→学工部审批→查询
  - 验证状态流转：pending_counselor→pending_dean→approved
  - 验证审批记录创建和更新
- ✓ 错误场景测试（test_error_cases.py）
  - DORM_BLOCKED：宿舍清退未完成阻断提交
  - CONFLICT：重复提交申请
  - FORBIDDEN：学生访问他人申请
  - NOT_FOUND：申请不存在
  - VALIDATION_ERROR：参数验证失败
- ✓ 驳回流程测试（test_rejection_flow.py）
  - 辅导员驳回：pending_counselor→rejected
  - 学工部驳回：pending_dean→rejected
- ⏳ 测试执行（需要环境准备：虚拟环境、依赖安装、PostgreSQL）

**Week 2实施（2026-05-30完成）：**
- ✓ ClassMapping模型
  - class_id、counselor、counselor_name、active
  - 班级到辅导员的映射关系
- ✓ CSV导入命令（import_csv）
  - 支持导入students CSV（student_id、name、class_id等）
  - 支持导入counselors CSV（employee_id、name等）
  - 支持导入mappings CSV（class_id、counselor_id）
- ✓ 动态辅导员分配
  - 移除硬编码辅导员ID（T001）
  - 根据学生class_id查找ClassMapping
  - 自动分配对应辅导员到审批流程
- ✓ seed_data更新
  - 创建2个班级映射（CS2020-01→T001, CS2020-02→T002）
- ✓ admin配置
  - ClassMapping管理界面
- ⏳ CSV模板文件（待创建）

**Week 3工作方向讨论（2026-05-30完成）：**
- ✓ Claude-Codex 4轮批判性讨论达成共识（docs/discussions/week3-direction-2026-05-30/）
- ✓ 最终方案：Plan D（2天硬timebox + 决策门 + 可选P0修复日）
- ✓ 核心决策：快速暴露问题、建立可复现证据、做继续/降范围/重设计决策
- ✓ 验收标准：8项必须证明（迁移成功、完整闭环、负向权限验证等）
- ⏳ 待执行：Day 0准备（环境策略、seed数据、验收清单）

## 文档清单

1. **系统设计文档**
   - 路径：`docs/design/2026-05-27-system-design.md`
   - 内容：完整的系统设计，包含10个主要部分
   - 行数：1780行

2. **实施计划文档**
   - 路径：`docs/superpowers/plans/2026-05-27-implementation-plan.md`
   - 内容：9个阶段的详细实施计划
   - 工期：8-10周

3. **项目总结文档**
   - 路径：`docs/PROJECT-SUMMARY.md`
   - 内容：项目概述、技术选型、已完成工作

4. **用户设计说明书**
   - 路径：`docs/用户设计说明书.md`
   - 内容：面向最终用户的项目设计说明，包含业务流程、系统特色、常见问题
   - 受众：学校管理人员、辅导员、学工部

5. **数据对接说明文档**
   - 路径：`docs/数据对接说明文档.md`
   - 内容：宿舍管理系统对接规范，包含API接口和数据文件两种方式
   - 受众：宿舍管理系统管理员、数据对接负责人
   - 附件：`docs/templates/宿舍清退数据模板.csv`

## 核心功能

### 1. 用户管理
- 学生、辅导员、学工部三种角色
- 学号+密码登录
- 微信OAuth2授权登录
- RBAC权限控制

### 2. 离校申请
- 在线填写申请表
- 上传附件（宿舍清退证明、图书馆清书证明、财务结清截图）
- 申请状态跟踪
- 申请历史查询

### 3. 审批流程
- 两级审批（辅导员→学工部）
- 审批意见记录
- 驳回重新提交
- 超时提醒机制

### 4. 附件管理
- 文件上传（最大10MB）
- 支持格式：jpg、png、pdf、doc、docx
- 文件下载
- 权限控制

### 5. 通知系统
- 微信模板消息推送
- 审批状态变更通知
- 超时提醒通知
- 异步发送

### 6. 外部系统集成
- 宿舍管理系统对接
- 重试机制
- 降级策略

## 数据库设计

### 核心表

1. **users** - 用户表
2. **applications** - 离校申请表
3. **approvals** - 审批记录表
4. **attachments** - 附件表
5. **notifications** - 通知表
6. **system_configs** - 系统配置表
7. **audit_logs** - 审计日志表

### 关键特性

- 本项目使用PostgreSQL数据库
- 外部系统通过API对接（支持MySQL/SQL Server/Oracle等异构系统）
- 软删除设计
- 完整的索引策略
- 审计日志记录

## 实施阶段

### 阶段1：项目初始化和基础设施（第1周）
- Django项目初始化
- Docker环境配置
- Celery配置
- 开发工具配置

### 阶段2：用户认证模块（第2周）
- 用户模型
- 学号密码认证
- 微信OAuth2认证
- 权限系统

### 阶段3：离校申请模块（第3周）
- 申请模型
- 状态机
- 申请CRUD API
- 申请提交逻辑

### 阶段4：审批管理模块（第4周）
- 审批记录模型
- 审批API
- 审批流程逻辑
- 超时监控

### 阶段5：附件管理模块（第5周）
- 附件模型
- 文件存储配置
- 上传下载API

### 阶段6：通知模块（第6周）
- 通知模型
- 微信通知
- Celery异步任务
- 通知API

### 阶段7：外部系统集成（第7周）
- 集成接口设计
- 宿舍系统对接
- 重试机制
- 降级策略

### 阶段8：前端开发（第8-9周）
- React Native应用
- 微信小程序

### 阶段9：测试和部署（第10周）
- 单元测试
- 集成测试
- 端到端测试
- 性能测试
- 部署配置

## 下一步工作

1. **审查设计和计划**
   - 确认设计文档无遗漏
   - 确认实施计划可行

2. **准备开发环境**
   - 安装开发工具
   - 配置开发环境
   - 申请微信公众平台账号

3. **开始实施**
   - 按照实施计划执行
   - 采用TDD开发模式
   - 频繁提交代码

## 风险和挑战

1. **外部系统API不稳定** - 已有重试和降级策略
2. **微信公众平台审核延迟** - 提前申请账号
3. **数据库性能问题** - 已有优化策略
4. **前端开发延期** - 后端API优先完成
5. **测试覆盖不足** - 采用TDD模式

## 团队和资源

- **开发人员：** 2-3人
- **预计工期：** 8-10周
- **开发模式：** TDD（测试驱动开发）
- **协作方式：** Git Flow工作流

## 成功标准

- ✓ 所有核心功能实现并通过测试
- ✓ 单元测试覆盖率 > 80%
- ✓ API响应时间 < 200ms（P95）
- ✓ 支持1000+并发用户
- ✓ Docker一键部署成功

---

**最后更新：** 2026-05-30  
**更新人：** Claude Opus 4.7
