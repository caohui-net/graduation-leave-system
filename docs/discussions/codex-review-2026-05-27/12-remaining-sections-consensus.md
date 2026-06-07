# 剩余章节审查共识 - Round 2

**共识时间：** 2026-05-27  
**参与方：** Claude Opus 4.7 + Codex Rescue Agent  
**审查范围：** API设计、审批流程、部署架构、安全设计、性能优化、测试策略

---

## 共识结论

**所有修改已达成共识，可以开始应用。**

---

## 关键确认

### 1. 申请编号生成时机
- ✅ **决策：提交时生成**（不是创建时）
- ✅ 数据库字段：`application_no`允许NULL直到提交
- ✅ API创建响应：返回`id`，不返回`application_no`

### 2. 第7章重写（CRITICAL）
- ✅ 必须替换MySQL为PostgreSQL
- ✅ 必须替换3副本为单实例

### 3. 批次顺序
- ✅ 从部署架构开始（最严重）是合理的

### 4. 所有发现有效
- ✅ 每个问题都与Round 1共识决策一致

---

## 修改批次（5批）

### 批次1：部署架构（CRITICAL）
**章节：** 第7章  
**问题：** 2 CRITICAL + 2 MAJOR  
**修改：** 完全重写
- PostgreSQL替换MySQL
- 单实例替换3副本
- 移除MinIO基线服务
- 更新备份脚本（pg_dump）

### 批次2：API设计
**章节：** 第3章  
**问题：** 5 MAJOR + 1 MINOR  
**修改：**
- 添加微信绑定API（/auth/wechat/bind、/auth/password/setup）
- 修正配置API示例（外部集成配置）
- 添加审批API版本检查
- 添加上传API安全措施
- 修正HTTP状态码（201/204）

### 批次3：审批流程
**章节：** 第5章  
**问题：** 5 MAJOR + 1 MINOR  
**修改：**
- 工作日计算（chinese_calendar）
- 修正is_timeout字段位置
- 添加字段更新逻辑（counselor_id、admin_id、current_approver_id、version）
- 添加历史快照和审计日志
- 明确降级策略

### 批次4：安全设计
**章节：** 第8章  
**问题：** 4 MAJOR + 1 MINOR  
**修改：**
- 添加API限流（DRF + Nginx）
- 添加文件上传安全
- 添加微信绑定安全
- 添加审计日志说明
- 添加加密配置说明

### 批次5：性能和测试
**章节：** 第9章、第10章  
**问题：** 2+5 MAJOR + 2+1 MINOR  
**修改：**
- 更新索引策略（完整复合索引）
- 修正连接池配置（CONN_MAX_AGE）
- 添加TDD工作流
- 添加PostgreSQL测试要求
- 添加安全测试用例
- 调整性能目标（500并发）

---

## 无额外关注点

Codex确认无额外关注点，可以开始应用修改。

---

## 参考文档

- 审查报告：`10-remaining-sections-review.md`
- 响应文档：`11-remaining-sections-response.md`
- 本共识文档：`12-remaining-sections-consensus.md`

---

**下一步：** 开始批次1修改（第7章完全重写）
