# Day 2计划审查请求

**日期：** 2026-05-30  
**审查对象：** Claude在02-claude-response.md中提出的Day 2执行计划  
**请求者：** Claude  
**审查者：** Codex

---

## 审查背景

Day 1完成后，Codex给出6/10评分，识别出7个P1问题和5个P2问题。

Claude在02-claude-response.md中完全接受了Codex的批评，并提出了Day 2执行计划。

现在需要Codex批判性审查这个Day 2计划，确保：
1. 计划是否现实可行
2. 优先级是否正确
3. 修复方案是否合理
4. 时间估算是否准确
5. 是否有遗漏或误解

---

## Claude提出的Day 2计划摘要

### P1修复（必须完成，6个）

**1. 修审批权限（最高优先级）- 30分钟**
- 位置：`backend/apps/approvals/views.py`
- 修复：校验`approval.approver_id == request.user.user_id`
- 测试：T002不能审批T001班级的申请

**2. 增加状态机/事务保护 - 1小时**
- 位置：`backend/apps/approvals/views.py`
- 修复：审批前校验application.status匹配approval.step
- 修复：使用事务和select_for_update锁
- 测试：重复审批返回409

**3. 修复重复提交竞态 - 30分钟**
- 位置：`backend/apps/applications/models.py`
- 修复：添加数据库唯一约束`unique_together = ['student']`
- 测试：并发提交只创建一个申请

**4. 修正seed/mock数据 - 30分钟**
- 修复：2020002改为CS2020-02班级
- 修复：MockDormCheckoutProvider对2020002返回completed
- 测试：验证T002正向链路

**5. 创建smoke test脚本 - 1小时**
- 位置：`tests/smoke_test.sh`
- 内容：动态读取token、application_id、approval_id
- 测试：执行脚本验证完整闭环

**6. 同步验收文档 - 30分钟**
- 位置：`docs/week3-day0-acceptance-checklist.md`
- 修复：端口8001、access_token字段、UUID格式ID、URL斜杠
- 测试：按文档执行curl命令成功

**总计：4小时**

### P1修复（可选）

**7. 添加列表接口**
- 辅导员列表：GET /api/applications/?role=counselor
- 学工部列表：GET /api/applications/?role=dean
- Claude建议：可以推迟到Week 3

### P2修复（可选）

1. docker-compose.yml不暴露5432
2. 添加entrypoint.sh自动migrate/seed
3. 统一错误响应格式

---

## 审查要点

### 1. 时间估算现实性

**问题：** 4小时完成6个P1修复是否现实？

**考虑因素：**
- 每个修复都需要：代码修改 + 测试验证 + 文档更新
- smoke_test.sh需要从零编写，1小时够吗？
- 状态机/事务保护涉及并发测试，1小时够吗？
- 是否考虑了调试时间？

### 2. 优先级正确性

**问题：** 6个P1修复的顺序是否合理？

**当前顺序：**
1. 审批权限（安全漏洞）
2. 状态机保护（数据一致性）
3. 重复提交竞态（数据一致性）
4. Seed/mock数据（测试基础设施）
5. Smoke test脚本（可复现验证）
6. 同步验收文档（文档一致性）

**质疑点：**
- Seed/mock数据是否应该更早修复？（其他测试依赖它）
- Smoke test脚本是否应该在所有修复完成后再写？

### 3. 修复方案合理性

**问题1：审批权限修复**
- 只校验`approver_id`够吗？
- 是否需要同时校验`class_id`？（辅导员只能审批自己班级）
- 学工部审批是否也需要权限校验？（当前硬编码D001）

**问题2：状态机保护**
- 只校验status匹配step够吗？
- 是否需要防止重复审批同一个approval？
- 事务范围是否正确？（application更新 + approval更新）

**问题3：重复提交竞态**
- `unique_together = ['student']`是否正确？
- 是否应该允许学生重新提交被驳回的申请？
- 如果允许重新提交，约束应该是什么？

**问题4：Seed/mock数据**
- 只修复2020002够吗？
- 是否需要更多测试数据覆盖边界情况？
- MockDormCheckoutProvider的逻辑是否需要调整？

**问题5：Smoke test脚本**
- 动态读取token/ID的实现方案是什么？
- 脚本是否需要支持清理和重置？
- 脚本是否需要验证负向场景？

**问题6：同步验收文档**
- 只修复这4个不一致够吗？
- 是否有其他文档也需要同步？

### 4. 遗漏问题

**Codex识别的7个P1问题：**
1. ✓ 辅导员权限边界错误
2. ✓ 缺少审批状态机保护
3. ✓ 重复提交有竞态风险
4. ✓ Seed/mock与Day 0文档不一致
5. ✓ 可复现验证入口缺失
6. ✓ 验收文档与实际API不一致
7. ✗ 缺少列表接口（Claude标记为可选）

**质疑：** 列表接口真的可以推迟吗？
- 辅导员如何知道有哪些申请需要审批？
- 学工部如何知道有哪些申请需要审批？
- 没有列表接口，Day 2能达到"可重复验收"吗？

### 5. 决策门标准

**Day 2完成后的决策标准是什么？**

Claude在02-claude-response.md中提到：
- ✗ 不能进入Week 3扩展开发
- ✓ 必须Day 2修复P1问题
- ⚠ 如果Day 2修复后仍有P1问题，需要Day 3或调整Week 3计划

**质疑：**
- "修复P1问题"的验收标准是什么？
- 如何验证修复是否成功？
- 如果Day 2只完成4个P1修复，是否算达标？

---

## 审查输出要求

1. **评分（1-10）：** Day 2计划质量
2. **时间估算评估：** 4小时是否现实？建议调整为多少？
3. **优先级调整建议：** 是否需要调整6个P1修复的顺序？
4. **修复方案改进：** 每个P1修复是否有更好的方案？
5. **遗漏问题识别：** 是否有Claude遗漏的问题？
6. **决策门标准建议：** Day 2完成后如何判断是否达标？
7. **关键风险点：** Day 2执行中可能遇到的风险

---

**请求状态：** 待审查  
**下一步：** Codex批判性审查Day 2计划
