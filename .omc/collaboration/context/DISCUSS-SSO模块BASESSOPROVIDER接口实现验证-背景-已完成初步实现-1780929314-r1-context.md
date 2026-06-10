# Discussion Context

**Task:** DISCUSS-SSO模块BASESSOPROVIDER接口实现验证-背景-已完成初步实现-1780929314
**Round:** 1

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

## Pre-Discuss Initial Analysis

Response ID: DISCUSS-SSO模块BASESSOPROVIDER接口实现验证-背景-已完成初步实现-1780929314-r0-claude
Artifact: .omc/collaboration/artifacts/DISCUSS-SSO模块BASESSOPROVIDER接口实现验证-背景-已完成初步实现-1780929314-discuss-r0-claude-20260608-143514.md

Claude initial framing: clarify scope, challenge assumptions, preserve compatibility, and require evidence.

## Previous Discussion

[claude]: Pre-discuss initial analysis prepared
[claude]: Round 1 started

## Previous Responses

### DISCUSS-SSO模块BASESSOPROVIDER接口实现验证-背景-已完成初步实现-1780929314-r0-claude (claude)

Decision: Claude initial framing: clarify scope, challenge assumptions, preserve compatibility, and require evidence.

Reasoning: Initial framing for the discussion.

## Open Questions

- What assumptions in Claude's initial framing are weakest?
- Which compatibility contracts must remain stable?
- What evidence or tests are required before concluding?

## Referenced Artifacts

- .omc/collaboration/artifacts/DISCUSS-SSO模块BASESSOPROVIDER接口实现验证-背景-已完成初步实现-1780929314-discuss-r0-claude-20260608-143514.md

