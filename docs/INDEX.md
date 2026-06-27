# 文档索引

本目录包含项目的技术文档、操作说明、设计讨论和技术审查记录。

---

## 🚀 部署与运维

### 环境与执行规范
- [环境执行规范速查](./环境执行规范速查.md) - Python/Django/数据库正确执行方式，避免常见错误

### 三环境治理框架（2026-06-27新增）
- [数据库账号管理指南](./数据库账号管理指南.md) - 生产环境数据库账号隔离和权限管理
- [Schema漂移检测指南](./Schema漂移检测指南.md) - 自动检测数据库实际状态与代码定义差异
- [配置中心管理指南](./配置中心管理指南.md) - 统一管理三环境配置，消除配置漂移

### 部署与运维文档
- [三环境同步机制详解](./三环境同步机制详解.md) - 开发、Staging、Production三环境同步流程、数据库迁移和故障处理
- [异地Docker自动化部署方案](./异地Docker自动化部署方案.md) - Docker异地部署方案
- [环境部署说明-三环境架构](./环境部署说明-三环境架构.md) - 三环境架构部署说明
- [三环境部署体系方案](./deployment/三环境部署体系方案.md) - 三环境部署体系
- [部署检查清单](./部署检查清单.md) - 部署前验证清单（v2.0已集成治理框架）
- [留校请假审批部署计划](./留校请假审批部署计划.md) - 部署计划
- [DEPLOYMENT_AUTO](./DEPLOYMENT_AUTO.md) - 自动部署文档
- [DEPLOYMENT_PROD](./DEPLOYMENT_PROD.md) - 生产环境部署文档
- [SYSTEM-OPERATIONS-GUIDE](./SYSTEM-OPERATIONS-GUIDE.md) - 系统运维指南
- [UAT-CHECKLIST](./UAT-CHECKLIST.md) - 用户验收测试清单

---

## 📋 操作与实施

- [操作说明书](./操作说明书.md) - 系统操作指南
- [留校请假审批实施方案](./留校请假审批实施方案.md) - 功能实施方案
- [API测试流程演示](./API测试流程演示.md) - API测试操作流程
- [API测试演示使用说明](./API测试演示使用说明.md) - API测试使用说明
- [Phase0数据验证后执行逻辑调整总结](./Phase0数据验证后执行逻辑调整总结.md) - Phase0执行逻辑调整

---

## 📊 数据处理

- [数据处理流程](./数据处理流程.md) - 数据处理标准流程
- [数据库字段映射](./数据库字段映射.md) - 数据库字段映射表
- [数据确认清单](./数据确认清单.md) - 数据验证检查清单
- [数据速查](./数据速查.md) - 数据快速查询
- [数据流程深度分析](./数据流程深度分析.md) - 数据流程详细分析
- [CSV字段映射](./CSV字段映射.md) - CSV字段映射表
- [数据导入记录](./数据导入记录.md) - 数据导入日志
- [19名额外研究生待确认清单](./19名额外研究生待确认清单.md) - 研究生数据待确认
- [271名研究生学号比对分析报告](./271名研究生学号比对分析报告.md) - 研究生学号分析
- [Excel数据源分析与需求对比](./Excel数据源分析与需求对比.md) - Excel数据源分析
- [Excel数据源实际分析结果](./Excel数据源实际分析结果.md) - Excel数据分析结果
- [missing_building_data_discrepancy_analysis](./missing_building_data_discrepancy_analysis.md) - 楼栋数据差异分析

---

## 🔌 XG-API集成

- [获取租户下人员信息（信息中心数据）](./获取租户下人员信息（信息中心数据）.md) - 信息中心数据接口
- [XG-API数据不足解决方案讨论](./XG-API数据不足解决方案讨论.md) - XG-API数据问题讨论
- [XG-API-数据源全面分析报告](./XG-API-数据源全面分析报告.md) - XG-API数据源分析
- [XG-API与项目数据表对比分析](./XG-API与项目数据表对比分析.md) - 数据表对比分析
- [XG-API-ACTUAL-DATA-SAMPLES](./XG-API-ACTUAL-DATA-SAMPLES.md) - 实际数据样本
- [XG-API-COLLECTION-TEST-GUIDE](./XG-API-COLLECTION-TEST-GUIDE.md) - 集合测试指南
- [XG-API-DATA-EXAMPLES](./XG-API-DATA-EXAMPLES.md) - 数据示例
- [XG-API-DATA-SAMPLES](./XG-API-DATA-SAMPLES.md) - 数据样本
- [API-DATA-EXAMPLES](./API-DATA-EXAMPLES.md) - API数据示例
- [phase4c-xg-field-coverage](./phase4c-xg-field-coverage.md) - XG字段覆盖分析

---

## 🔐 SSO集成

- [青橄榄SSO对接-三方技术审查](./青橄榄SSO对接-三方技术审查.md) - SSO技术审查文档
- [青橄榄SSO对接完成报告-2026-06-10](./青橄榄SSO对接完成报告-2026-06-10.md) - SSO对接完成报告
- [SSO对接框架通讯架构说明](./SSO对接框架通讯架构说明.md) - SSO通讯架构说明
- [移动端界面适配问题总结](./移动端界面适配问题总结.md) - 移动端适配问题
- [移动端SSO修复测试方案](./移动端SSO修复测试方案.md) - 移动端SSO修复方案
- [SSO部署和验收文档](./SSO部署和验收文档.md) - SSO部署验收文档
- [SSO集成进度快照-20260610](./SSO集成进度快照-20260610.md) - SSO集成进度快照
- [SSO模块通用化可行性分析报告](./SSO模块通用化可行性分析报告.md) - SSO模块通用化分析

---

## 🎨 系统设计

- [2026-05-27-system-design](./design/2026-05-27-system-design.md) - 系统设计方案
- [2026-06-08-sso-qingganlian-integration](./design/2026-06-08-sso-qingganlian-integration.md) - SSO集成设计

---

## 📈 性能与缓存

- [PERFORMANCE](./PERFORMANCE.md) - 性能优化文档
- [cache-control-guide](./cache-control-guide.md) - 缓存控制指南

---

## 📝 项目总结与共识

- [PROJECT-SUMMARY](./PROJECT-SUMMARY.md) - 项目总结
- [PROJECT-SUMMARY-2026-06-07](./PROJECT-SUMMARY-2026-06-07.md) - 项目总结快照
- [PROJECT-COMPLETION-DECLARATION](./PROJECT-COMPLETION-DECLARATION.md) - 项目完成声明
- [COMPLETION-STATUS](./COMPLETION-STATUS.md) - 完成状态
- [P0-fix-consensus-2026-06-07](./P0-fix-consensus-2026-06-07.md) - P0修复共识
- [P1-approval-workflow-consensus-2026-06-07](./P1-approval-workflow-consensus-2026-06-07.md) - P1审批流程共识

---

## 🔍 Codex技术审查

### 审查流程与协议
- [Codex审查流程指南](./Codex审查流程指南.md) - Codex审查流程
- [codex-review-protocol](./codex-review-protocol.md) - 审查协议
- [codex-review-action-plan-2026-06-07](./codex-review-action-plan-2026-06-07.md) - 审查行动计划
- [code-review-request-2026-06-16](./code-review-request-2026-06-16.md) - 代码审查请求

### 项目审计
- [project-audit-consolidated-report-2026-06-15](./project-audit-consolidated-report-2026-06-15.md) - 项目审计报告

### 2026-05-27 技术审查
- [00-CONSENSUS-SUMMARY](./discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md) - 共识总结
- [21-final-consensus](./discussions/codex-review-2026-05-27/21-final-consensus.md) - 最终共识
- [架构审查系列](./discussions/codex-review-2026-05-27/) - 01-03: 架构审查
- [数据库设计系列](./discussions/codex-review-2026-05-27/) - 04-09: 数据库设计
- [功能审查系列](./discussions/codex-review-2026-05-27/) - 10-12: 功能审查
- [深度分析系列](./discussions/codex-review-2026-05-27/) - 13-20: 深度分析与比较
- [字段审查系列](./discussions/codex-review-2026-05-27/) - 22-25: 字段审查
- [用户文档系列](./discussions/codex-review-2026-05-27/) - 26-28: 用户文档
- [数据源分析系列](./discussions/codex-review-2026-05-27/) - 29-37: 数据源分析与实施

### 2026-06-02 技术审查
- [02-claude-response-migration-strategy](./discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.md)
- [03-phase4-regression-findings](./discussions/codex-review-2026-06-02/03-phase4-regression-findings.md)
- [04-phase4-progress-summary](./discussions/codex-review-2026-06-02/04-phase4-progress-summary.md)

---

## 📖 快速导航

### 速查手册（推荐首先阅读）
- [项目速查手册](../PROJECT-QUICKREF.md) - **综合速查**，包含环境、命令、端口、故障排查
- [环境执行规范速查](./环境执行规范速查.md) - Python/Django/数据库正确执行方式
- [数据速查](./数据速查.md) - 数据导入命令、统计、路由逻辑

### 按主题浏览

| 主题 | 核心文档 |
|------|---------|
| **部署运维** | [三环境同步机制](./三环境同步机制详解.md), [部署检查清单](./部署检查清单.md), [运维指南](./SYSTEM-OPERATIONS-GUIDE.md) |
| **数据处理** | [数据处理流程](./数据处理流程.md), [字段映射](./数据库字段映射.md), [深度分析](./数据流程深度分析.md) |
| **XG-API** | [数据源分析](./XG-API-数据源全面分析报告.md), [对比分析](./XG-API与项目数据表对比分析.md) |
| **SSO集成** | [技术审查](./青橄榄SSO对接-三方技术审查.md), [架构说明](./SSO对接框架通讯架构说明.md) |
| **项目总结** | [PROJECT-SUMMARY](./PROJECT-SUMMARY.md), [完成声明](./PROJECT-COMPLETION-DECLARATION.md) |
| **技术审查** | [审查流程](./Codex审查流程指南.md), [审计报告](./project-audit-consolidated-report-2026-06-15.md) |

### 新人上手路径

1. **项目概览**: [PROJECT-SUMMARY](./PROJECT-SUMMARY.md)
2. **系统设计**: [design/2026-05-27-system-design.md](./design/2026-05-27-system-design.md)
3. **操作指南**: [操作说明书](./操作说明书.md)
4. **部署流程**: [三环境同步机制详解](./三环境同步机制详解.md)
5. **技术审查共识**: [discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md](./discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md)

---

**维护说明**: 
- 新增文档请更新此索引
- 保持文档分类清晰
- 定期审查文档时效性

**统计**:
- 根目录文档: 94+ 个
- 技术审查讨论: 50+ 个
- 最后更新: 2026-06-23
