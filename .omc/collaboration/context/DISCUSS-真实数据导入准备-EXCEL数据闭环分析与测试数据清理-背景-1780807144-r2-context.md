# Discussion Context

**Task:** DISCUSS-真实数据导入准备-EXCEL数据闭环分析与测试数据清理-背景-1780807144
**Round:** 2

## Topic

真实数据导入准备：Excel数据闭环分析与测试数据清理

**背景：**
- Phase 3（2026-06-06）记录显示导入6040人真实数据
- 数据库分析报告（2026-06-07）实际只有16人测试数据
- 结论：真实Excel数据未实际导入到数据库

**Excel数据文件：**
1. backend/data/file5_students_merged_v2.csv (5946学生)
2. backend/data/dorm_managers_processed.csv (72宿管)
3. backend/data/counselors_processed.csv (20辅导)
4. backend/data/additional_staff.csv (3管理员)

**需要讨论的问题：**
1. Excel数据完整性验证（字段完整性、格式正确性、必填项检查）
2. 数据闭环检查（学生→楼栋→宿管员路由、学生→学院→辅导员路由、覆盖率统计）
3. 测试数据清理策略（识别哪些是测试数据、安全删除方法、数据备份策略）
4. 真实数据导入方案（导入顺序、验证步骤、回滚机制）
5. 导入后验证清单（用户总数验证、路由覆盖率验证、审批链路测试）

**期望输出：**
结构化执行方案，包含：
- 具体执行步骤（带命令）
- 每步验证点
- 风险控制措施
- 回滚方案

## Previous Discussion

[Earlier: 1 discussion events]

[claude]: Round 1 ended
[claude]: Round 2 started

