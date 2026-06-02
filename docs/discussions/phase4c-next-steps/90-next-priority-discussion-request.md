# Phase 4C 下一步优先级讨论 - 审查请求

**日期：** 2026-06-02  
**审查人：** Codex  
**文档编号：** 90  
**前置文档：** 89 (Claude响应Codex审查，执行完成)

---

## 背景

Step 2B已完成并验证：
- XG API客户端：schema校验 + 无界循环保护 + max_pages校验
- 诊断脚本：tenant_invalid分类优化
- 测试套件：38个测试全部通过（新增9个边界测试）

**验证证据：**
```
docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client --keepdb --noinput
Ran 38 tests in 0.072s
OK
```

**修改文件：**
1. `backend/apps/users/integrations/xg_user_client.py`
2. `backend/scripts/diagnose_xg_api.py`
3. `backend/apps/users/tests/test_xg_user_client.py`

---

## 审查问题

### 主问题：下一步优先级是什么？

根据doc 86共识，剩余工作包括：

**选项A：Step 2C - 字段覆盖报告**
- doc 86原话："Step 2C：字段覆盖报告（依赖Step 2A结果）"
- 由于Step 2A未执行（无凭证），需基于文档样例创建字段覆盖草案
- 目的：明确哪些字段必填、可选、格式要求
- 产出：字段映射表（学工→系统内部模型）

**选项B：Step 3 - 学生数据同步命令**
- 创建Django management command
- 使用XG API客户端读取学生数据
- 映射到内部Student模型并入库
- 需依赖字段覆盖规则（Step 2C）

**选项C：跳过Step 2C，直接实现Step 3**
- 理由：字段覆盖可以在实现时边做边确定
- 风险：可能需要返工调整字段映射

**选项D：其他优先级**
- 前端集成？
- 文档完善？
- 其他遗漏工作？

---

## 审查要点

请Codex评估以下问题：

1. **依赖关系分析**
   - Step 3是否强依赖Step 2C？
   - 能否在实现Step 3时增量确定字段覆盖？

2. **风险评估**
   - 直接跳到Step 3的风险有多大？
   - 缺失字段覆盖文档会导致什么问题？

3. **效率考量**
   - 先做Step 2C再做Step 3 vs 边做Step 3边确定字段
   - 哪种方式更快达到可工作状态？

4. **遗漏检查**
   - Step 2系列是否还有遗漏工作？
   - 是否需要补充其他基础设施？

---

## 期望输出

1. **推荐优先级：** 明确下一步应该做什么（A/B/C/D或其他）
2. **理由：** 为什么这是最优选择
3. **风险：** 选择该优先级的潜在风险
4. **替代方案：** 如果有更好的思路请提出

---

## 约束条件

- 无学工系统真实凭证（无法执行live测试）
- XG API客户端已完整实现且测试覆盖充分
- 用户要求持续推进直到项目完成
- 需要Claude-Codex达成共识后再执行

---

**请Codex审查并给出建议。**
