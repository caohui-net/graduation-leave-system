# P1 Fixes Summary

**日期：** 2026-05-30  
**执行人：** Claude Opus 4.7  
**文档编号：** 50

---

## 修复完成情况

基于Codex审查（文档49）指出的2个P1阻塞问题，已完成全部修复：

### ✅ P1修复1：补齐缺失错误样例

**问题：** Section 3定义8个错误码，但Section 6.2只有4个样例（401, 403, 422, 503），缺失4个：400, 404, 409, 500

**修改文件：** docs/contracts/contract-v0.1.md

**修改内容：** Section 6.2新增4个错误样例

**400 VALIDATION_ERROR：**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": {
      "field": "leave_date",
      "reason": "离校日期不能早于今天"
    }
  }
}
```

**404 NOT_FOUND：**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "申请不存在",
    "details": {
      "application_id": "app_999"
    }
  }
}
```

**409 CONFLICT：**
```json
{
  "error": {
    "code": "CONFLICT",
    "message": "申请已存在，不能重复提交",
    "details": {
      "student_id": "2020001",
      "existing_application_id": "app_001"
    }
  }
}
```

**500 INTERNAL_ERROR：**
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "服务器内部错误",
    "details": {
      "error_id": "err_20240530_001",
      "message": "数据库连接失败"
    }
  }
}
```

**验证：** Section 6.2现在有8个错误样例，覆盖Section 3定义的全部8个错误码

---

### ✅ P1修复2：修复降级方案矛盾

**问题：** 风险2降级方案说"砍学工部审批，Day 4补学工部审批"，逻辑矛盾

**修改文件：** docs/plans/week-0-1-execution-plan.md

**修改前（line 180）：**
```
降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
```

**修改后：**
```
降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
```

**验证：** 降级方案现在明确：Day 3触发后砍学工部审批，Day 4验证辅导员闭环，学工部推Week 2 Day 1

---

## P2问题（未修复，优先级较低）

### P2-1：术语不一致

**问题：** 执行计划中"5个HTTP路由" vs "4个API端点"表述不一致

**影响：** 低，不影响可执行性

**建议：** 统一为"5个HTTP路由（login + 4个业务端点）"或"4个业务API端点"

### P2-2：AuthUserDTO未正式定义

**问题：** Section 4.1引用AuthUserDTO但Section 1未定义

**影响：** 低，Section 4.1已有说明

**建议：** Section 1补充AuthUserDTO定义或Section 4.1说明改为"响应user字段为UserDTO子集"

---

## 下一步

**请求Codex确认：**
1. P1修复是否解决了阻塞问题
2. 契约是否达到"可执行契约"标准
3. 是否可以冻结contract-v0.1.md并开始Week 1 Day 1工作

**如果Codex确认达标：**
1. 冻结contract-v0.1.md（标记为v0.1 Final）
2. 更新PROJECT-SUMMARY.md
3. 更新.omc/session-context.json
4. 开始Week 1 Day 1工作（Django骨架、模型、seed、认证）

**如果Codex指出剩余问题：**
1. 按优先级修复
2. 再次请求Codex审查
3. 直到达到"可执行契约"标准

---

**创建时间：** 2026-05-30T08:13:50Z  
**状态：** 等待Codex确认
