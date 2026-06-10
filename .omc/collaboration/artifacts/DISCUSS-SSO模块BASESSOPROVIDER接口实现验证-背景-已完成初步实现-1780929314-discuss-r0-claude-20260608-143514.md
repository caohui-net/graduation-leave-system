# Pre-Discuss Initial Analysis

Response ID: DISCUSS-SSO模块BASESSOPROVIDER接口实现验证-背景-已完成初步实现-1780929314-r0-claude
Agent: claude

## Topic

SSO模块BaseSSOProvider接口实现验证

**背景：**
已完成初步实现，需Codex代码审查和技术验证。

**已实现：**
1. BaseSSOProvider抽象基类（base.py, 38行）
   - authenticate()抽象方法
   - provider_name抽象属性
   - 标准化返回格式

2. QingganlanProvider实现（qingganlian.py, 109行）
   - 包装QingganlanClient
   - mobile/admin双端支持
   - 标准化输出

**请Codex审查：**

1. **接口设计验证**
   - BaseSSOProvider抽象是否over-fitted青橄榄3步流程？
   - authenticate(credentials: Dict)签名是否足够通用？
   - 返回格式(external_uid/provider_data)是否适配未来平台？

2. **Django迁移方案**
   需要3步迁移SSOUserMapping模型：
   - tenant_code → provider (CharField)
   - user_code → external_uid (CharField)
   - 新增provider_data (JSONField)
   
   请提供RunPython迁移脚本骨架，确保零停机时间。

3. **测试策略**
   - Mock BaseSSOProvider测试views.py
   - 不调用真实青橄榄API的单元测试方案

**代码位置：**
- backend/apps/sso_qingganlian/providers/base.py
- backend/apps/sso_qingganlian/providers/qingganlian.py

**限制：**
- 不能破坏现有mobile_login/admin_login API
- 必须向后兼容青橄榄对接

## Initial Analysis

- Clarify the decision or implementation change requested by the topic.
- Identify compatibility, state persistence, and verification risks before participants respond.
- Ask Codex and Gemini to challenge this framing directly and cite prior response IDs.

## Open Questions

- What assumptions in the initial framing are weakest?
- Which compatibility contracts must remain stable?
- What evidence or tests are required before concluding?
