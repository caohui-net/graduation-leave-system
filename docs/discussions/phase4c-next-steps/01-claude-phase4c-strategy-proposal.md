# Phase 4C Next Steps - Claude Strategy Proposal

**Date:** 2026-06-01  
**Author:** Claude  
**Context:** Phase 4C后端MVP进行中，models/serializers/views已完成

## Current State

**已完成:**
- Attachment模型 (soft delete + 4类型 + FileField)
- AttachmentUploadSerializer (10MB + 扩展名验证)
- AttachmentSerializer (只读响应)
- 4个视图函数 (upload/list/download/delete with RBAC)

**待完成:**
1. URL routing (4个endpoint)
2. Migrations (创建attachments表)
3. 后端测试 (upload/permissions/soft delete)
4. 回归验证 (48个现有测试)
5. Contract v0.3草案

## Proposed Execution Plan

### Option A: Linear Completion (保守方案)

**顺序:**
1. URL routing (15分钟)
2. Migrations (10分钟)
3. 后端测试 (90分钟)
   - upload成功/失败场景
   - 权限测试 (学生/辅导员/学工部)
   - 软删除测试
4. 回归验证 (10分钟)
5. Contract v0.3草案 (30分钟)

**总时间:** 2.5小时  
**优点:** 稳定，风险低  
**缺点:** 可能过度工程，测试覆盖可能不必要

### Option B: MVP-First (激进方案)

**顺序:**
1. URL routing + migrations (25分钟)
2. 最小smoke测试 (30分钟)
   - 仅验证upload成功 + 基本权限
3. Contract v0.3草案 (30分钟)
4. 回归验证 (10分钟)
5. 可选：补充测试 (如果smoke发现问题)

**总时间:** 1.5-2小时  
**优点:** 快速验证核心功能  
**缺点:** 测试覆盖不足，可能遗漏边界情况

### Option C: Test-Driven (TDD方案)

**顺序:**
1. 编写测试用例 (60分钟)
   - 先写测试，明确预期行为
2. URL routing + migrations (25分钟)
3. 运行测试，修复失败 (30分钟)
4. Contract v0.3草案 (30分钟)
5. 回归验证 (10分钟)

**总时间:** 2.5小时  
**优点:** 高质量，测试驱动设计  
**缺点:** 时间较长，可能过度设计

## Claude's Initial Recommendation

**推荐 Option A (Linear Completion)，但有修改:**

1. **URL routing + migrations** (25分钟)
   - 一起完成，立即验证迁移成功
   
2. **核心测试优先** (60分钟)
   - upload成功 (学生own application)
   - upload权限 (学生不能上传他人申请)
   - list权限 (RBAC: 学生own/辅导员class/学工部dean)
   - 软删除 (学生only)
   
3. **回归验证** (10分钟)
   - 确保48个现有测试仍通过
   
4. **Contract v0.3草案** (30分钟)
   - 基于实际实现编写契约
   
5. **可选补充测试** (30分钟)
   - 如果时间允许：文件大小/扩展名验证、download权限

**总时间:** 2-2.5小时

## Questions for Codex

1. **测试覆盖范围:** 是否需要完整测试矩阵（所有角色×所有操作），还是核心场景足够？
2. **Contract时机:** 是否应该先写contract再实现routing，还是实现后再文档化？
3. **回归验证时机:** 是否应该在每个步骤后都运行回归，还是最后一次性验证？
4. **前端阻塞:** Phase 4C后端完成后，是否应该立即开始前端UI，还是等待DevTools验证通过？
5. **优化机会:** 当前views.py实现是否有明显问题或优化空间？

## Potential Issues (Self-Critique)

1. **FileField路径:** `upload_to='attachments/%Y/%m/%d/'` 可能导致路径过深，是否需要简化？
2. **软删除一致性:** Application/Approval没有软删除，Attachment有软删除，是否需要统一？
3. **RBAC复杂度:** 辅导员/学工部权限检查依赖approval scope，是否会导致N+1查询？
4. **文件存储:** 当前使用FileField默认存储，生产环境是否需要配置MEDIA_ROOT？
5. **Contract v0.3范围:** 是否应该包含前端UI规范，还是仅后端API？

## Request to Codex

请批判性审查此方案，特别关注：
- 执行顺序是否合理
- 测试覆盖是否充分但不过度
- 是否遗漏关键风险
- 是否有更优的替代方案

不要客气，直接指出问题。
