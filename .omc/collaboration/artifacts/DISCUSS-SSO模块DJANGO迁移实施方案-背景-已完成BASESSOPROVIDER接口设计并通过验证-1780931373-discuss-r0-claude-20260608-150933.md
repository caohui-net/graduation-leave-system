# Pre-Discuss Initial Analysis

Response ID: DISCUSS-SSO模块DJANGO迁移实施方案-背景-已完成BASESSOPROVIDER接口设计并通过验证-1780931373-r0-claude
Agent: claude

## Topic

SSO模块Django迁移实施方案

背景：已完成BaseSSOProvider接口设计并通过验证，现需实施3步零停机迁移。

当前状态：
- BaseSSOProvider抽象接口已创建（backend/apps/sso_qingganlian/providers/base.py）
- QingganlanProvider实现已完成（backend/apps/sso_qingganlian/providers/qingganlian.py）
- SSOUserMapping模型当前字段：tenant_code, user_code
- 目标字段：provider, external_uid, provider_data

请讨论：
1. Phase 1迁移脚本实现细节
   - 添加3个新字段（nullable）
   - RunPython数据回填逻辑
   - tenant_code→external_uid映射规则
   - provider_data初始值设置

2. 数据回填策略
   - 如何处理现有SSOUserMapping记录
   - provider字段默认值（是否硬编码"qingganlian"）
   - provider_data结构（是否回填tenant_code）

3. 风险评估
   - 迁移失败回滚方案
   - 数据一致性检查点
   - 生产环境执行建议

请提供具体的migration代码框架和验证步骤。

## Initial Analysis

- Clarify the decision or implementation change requested by the topic.
- Identify compatibility, state persistence, and verification risks before participants respond.
- Ask Codex and Gemini to challenge this framing directly and cite prior response IDs.

## Open Questions

- What assumptions in the initial framing are weakest?
- Which compatibility contracts must remain stable?
- What evidence or tests are required before concluding?
