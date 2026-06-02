# Option A执行共识

**日期：** 2026-06-02  
**参与方：** Claude + Codex  
**类型：** 执行共识  
**前置：** Option E-lite已完成

---

## 共识声明

**Claude和Codex达成共识：执行B-mini + A-corrected方案。**

---

## 执行方案

### B-mini: Smoke typo清理（5-10分钟）

**任务：**
- 修复`tests/smoke_test.sh` line 255的`STUDENT_NOTIF_COUNT`未赋值问题
- 在使用前赋值或移除该echo
- 运行smoke test验证

### A-corrected: API Schema P1（3-4小时）

**Step 1: Schema清单和契约对齐（30分钟）**
- 对齐实际代码与schema计划
- 重点：login路径/响应、notification分页、attachment wrapper、错误envelope

**Step 2: Schema-only serializers（45分钟）**
- ErrorSerializer（仅用于实际返回envelope的端点）
- 分页响应serializers
- Notification list响应（count + results）
- Attachment list响应
- Delete 204响应
- Binary download响应

**Step 3: Method-scoped extend_schema（90分钟）**
- 装饰13个function-based views
- 多方法dispatchers使用method-specific schemas
- 显式operation IDs

**Step 4: 机械验证（30分钟）**
- Schema生成无警告
- /api/schema/和/api/schema/swagger-ui/可访问
- Operation IDs唯一
- 运行受影响模块测试

**Step 5: 更新文档（15分钟）**
- 更新api-schema-todo.md
- 更新PROJECT-SUMMARY.md
- 更新session-context.json

---

## 执行边界

✓ Schema匹配当前API行为（不修改行为）  
✓ ErrorSerializer仅用于实际返回envelope的端点  
✓ Login/notification/attachment schema以当前代码为准  
✓ 不引入全局错误包装  
✓ 不重构为class-based views  
✓ 不修改notification分页行为

---

## 验收标准

1. ✓ Smoke typo已修复
2. ✓ 13个views有准确@extend_schema（多方法用method-scoped）
3. ✓ OperationId冲突已修复且所有IDs显式
4. ✓ ErrorSerializer仅用于实际envelope端点
5. ✓ 文件上传/下载schema完整
6. ✓ Schema生成无警告
7. ✓ Login/notification/attachment schema与实际匹配
8. ✓ 文档精确标记完成项

---

## 执行授权

**状态：** 已授权执行  
**预计耗时：** 3.6小时  
**下一步：** 立即开始B-mini

---

**文档编号：** 54  
**状态：** 共识达成，开始执行
