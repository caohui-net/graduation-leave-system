# Day 2执行策略 - Claude提案

**日期：** 2026-05-30  
**提案者：** Claude  
**状态：** 待Codex审查

---

## 背景

Day 2计划已达成共识（文档07）：
- 4-6小时硬timebox
- 输出Conditional Go
- 6项核心任务 + 2项可选任务

现在需要决定：**如何执行这个计划？**

---

## 核心问题

### 1. 立即开始 vs 准备后开始？

**选项A：立即开始执行Day 2任务**
- 优势：保持momentum，timebox从现在开始计时
- 风险：可能遗漏准备工作，中途卡住

**选项B：先做准备工作，再开始Day 2**
- 优势：降低执行风险，提高成功率
- 风险：准备工作可能吃掉timebox时间

**我的建议：选项A（立即开始）**

理由：
1. Day 2任务都是明确的修复工作，不需要额外准备
2. 准备工作会模糊timebox边界（什么算准备？什么算执行？）
3. Plan D的核心是"快速暴露问题"，立即开始更符合理念
4. 如果遇到阻塞，可以记录为Day 2发现的问题

### 2. 串行执行 vs 并行执行？

**Day 2的6项核心任务：**
1. Seed/mock数据修复（30分钟）
2. 审批权限修复（30分钟）
3. 基础状态机保护（1小时）
4. 重复提交约束（30分钟）
5. Smoke test骨架（1小时）
6. 文档同步（30分钟）

**选项A：严格串行执行（按编号顺序）**
- 优势：依赖关系清晰，验证及时
- 风险：前面卡住会阻塞后面

**选项B：部分并行执行（独立任务并行）**
- 优势：提高效率，降低阻塞风险
- 风险：可能引入集成问题

**我的建议：串行执行，但允许跳过阻塞项**

理由：
1. 任务1（seed/mock）是后续验证的基础，必须先做
2. 任务2-4（权限、状态机、约束）相互独立，但都依赖任务1
3. 任务5（smoke test）依赖任务1-4全部完成
4. 任务6（文档）可以随时做

**执行顺序：**
- 第一阶段：任务1（seed/mock）- 必须完成
- 第二阶段：任务2、3、4（权限、状态机、约束）- 可以跳过阻塞项
- 第三阶段：任务5（smoke test）- 验证前面的修复
- 第四阶段：任务6（文档）- 同步文档

### 3. 验证策略？

**每个任务完成后如何验证？**

**选项A：手工验证（curl命令）**
- 优势：快速，灵活
- 风险：不可重复，容易遗漏

**选项B：自动化测试（Django测试）**
- 优势：可重复，覆盖全面
- 风险：写测试吃时间

**选项C：混合验证（核心手工，边界自动）**
- 优势：平衡速度和质量
- 风险：需要判断哪些手工、哪些自动

**我的建议：选项A（手工验证），但记录验证命令**

理由：
1. Day 2的timebox是4小时，写自动化测试会超时
2. 任务5（smoke test）本身就是自动化验证脚本
3. 手工验证命令可以作为smoke test的基础
4. Day 3或Week 3再补充完整的自动化测试

**验证方式：**
- 任务1：执行seed_data，检查数据库记录
- 任务2：curl测试跨辅导员审批，期望403
- 任务3：curl测试重复审批，期望409
- 任务4：curl测试重复提交，期望409
- 任务5：执行smoke_test.sh，期望全部通过
- 任务6：按文档执行curl，期望与实际一致

### 4. 遇到阻塞怎么办？

**如果某个任务卡住超过预期时间？**

**选项A：坚持完成，不跳过**
- 优势：保证质量
- 风险：打破timebox

**选项B：记录问题，跳过继续**
- 优势：保持timebox
- 风险：后续任务可能依赖

**选项C：评估影响，决定跳过或坚持**
- 优势：灵活应对
- 风险：需要判断力

**我的建议：选项C（评估影响）**

理由：
1. 任务1（seed/mock）不能跳过，它是基础
2. 任务2-4可以跳过，但要记录原因
3. 任务5（smoke test）可以降级为部分验证
4. 任务6（文档）可以推迟到Day 3

**跳过规则：**
- 如果任务超时50%（例如30分钟任务卡住15分钟），评估是否跳过
- 跳过前记录：卡在哪里、为什么卡住、需要什么条件解决
- 跳过后标记为Day 3待办

### 5. 时间分配策略？

**4小时如何分配？**

**我的建议：3小时执行 + 1小时缓冲**

- 0:00-0:30：任务1（seed/mock）
- 0:30-1:00：任务2（审批权限）
- 1:00-2:00：任务3（状态机）
- 2:00-2:30：任务4（重复提交）
- 2:30-3:30：任务5（smoke test）
- 3:30-4:00：任务6（文档）或缓冲

**如果有额外2小时：**
- 4:00-5:30：任务7（列表接口）
- 5:30-6:00：任务8（负向验证）

---

## 执行计划

### 阶段1：Seed/mock数据修复（30分钟）

**位置：** `backend/apps/users/management/commands/seed_data.py`

**修复内容：**
1. 2020002的class_id改为CS2020-02（当前是CS2020-01）
2. MockDormCheckoutProvider对2020002返回completed（当前返回not_started）
3. 添加--reset选项（使用update_or_create）
4. 更新CSV模板（docs/templates/）

**验证：**
```bash
docker exec backend python manage.py seed_data --reset
docker exec backend python manage.py shell -c "from apps.users.models import User; print(User.objects.get(user_id='2020002').class_id)"
# 期望输出：CS2020-02
```

**预期输出：**
- 2020002的class_id为CS2020-02
- MockDormCheckoutProvider.get_status('2020002')返回completed

### 阶段2：审批权限修复（30分钟）

**位置：** `backend/apps/approvals/views.py`

**修复内容：**
1. 添加`approval.approver_id == request.user.user_id`校验
2. 抽取共享权限函数（approve/reject共用）
3. 学工部从User表查询（不硬编码D001）
4. 修复`get_application`查看权限

**验证：**
```bash
# T002尝试审批T001的申请，期望403
curl -X POST http://localhost:8001/api/approvals/{T001的approval_id}/approve \
  -H "Authorization: Bearer {T002的token}" \
  -d '{"comment": "test"}'
# 期望：403 Forbidden
```

**预期输出：**
- 跨辅导员审批返回403
- 学工部ID从User表动态查询

### 阶段3：基础状态机保护（1小时）

**位置：** `backend/apps/approvals/views.py`

**修复内容：**
1. 添加`transaction.atomic()`
2. 添加`select_for_update()`
3. 验证`approval.decision == pending`
4. 验证`application.status`匹配`approval.step`
5. 防止重复创建Dean approval（exists检查）

**验证：**
```bash
# 重复审批同一个approval，期望409
curl -X POST http://localhost:8001/api/approvals/{approval_id}/approve \
  -H "Authorization: Bearer {token}" \
  -d '{"comment": "first"}'
# 第一次：200 OK

curl -X POST http://localhost:8001/api/approvals/{approval_id}/approve \
  -H "Authorization: Bearer {token}" \
  -d '{"comment": "second"}'
# 第二次：409 Conflict
```

**预期输出：**
- 重复审批返回409
- 状态不匹配返回409

### 阶段4：重复提交约束（30分钟）

**位置：** `backend/apps/applications/models.py`

**修复内容：**
1. 添加`UniqueConstraint(fields=['student'])`
2. 创建migration
3. `create_application`捕获`IntegrityError`返回409
4. Application和Approval创建放进同一事务

**验证：**
```bash
# 同一学生重复提交，期望409
curl -X POST http://localhost:8001/api/applications \
  -H "Authorization: Bearer {student_token}" \
  -d '{"reason": "first", "leave_date": "2024-07-01"}'
# 第一次：201 Created

curl -X POST http://localhost:8001/api/applications \
  -H "Authorization: Bearer {student_token}" \
  -d '{"reason": "second", "leave_date": "2024-07-01"}'
# 第二次：409 Conflict
```

**预期输出：**
- 重复提交返回409
- 数据库约束生效

### 阶段5：Smoke test骨架（1小时）

**位置：** `tests/smoke_test.sh`

**实现内容：**
1. 正向路径：2020002 → T002 → D001 → approved
2. 使用jq解析JSON
3. 动态提取token/application_id/approval_id
4. 硬编码BASE_URL=http://localhost:8001

**验证：**
```bash
chmod +x tests/smoke_test.sh
./tests/smoke_test.sh
# 期望：全部步骤通过，最终status=approved
```

**预期输出：**
- 脚本执行成功
- 输出完整流程日志
- 最终状态为approved

### 阶段6：文档同步（30分钟）

**位置：** `docs/week3-day0-acceptance-checklist.md`

**修复内容：**
1. 端口8000改为8001
2. token字段改为access_token
3. ID格式改为UUID
4. URL添加斜杠
5. 添加seed要求说明
6. 更新CSV模板路径

**验证：**
```bash
# 按文档执行curl命令，期望成功
# 从文档复制命令，直接执行
```

**预期输出：**
- 文档与实际一致
- 所有curl命令可执行

---

## 可选扩展（如果有额外2小时）

### 阶段7：列表接口（1.5小时）

**位置：** `backend/apps/applications/views.py`

**实现内容：**
1. GET /api/applications/
2. 根据角色自动过滤（学生看自己，辅导员看待审批，学工部看待审批）
3. 返回待办列表

**验证：**
```bash
curl http://localhost:8001/api/applications \
  -H "Authorization: Bearer {T002_token}"
# 期望：返回T002待审批的申请列表
```

### 阶段8：Smoke test负向场景（30分钟）

**实现内容：**
1. 跨辅导员403
2. 重复审批409
3. 重复提交409

---

## 成功标准

### Conditional Go标准（Day 2后可以进入Week 3准备）

**必须满足：**
- ✓ 跨辅导员审批已修复（403）
- ✓ 重复审批已修复（409或事务保护）
- ✓ 重复提交已修复（数据库约束）
- ✓ Seed/mock数据正确（T001/T002两条链路）
- ✓ 有smoke test骨架（正向路径可验证）
- ✓ 文档同步完成

**可选项（有Day 3计划）：**
- ⚠ 列表接口
- ⚠ 负向场景验证

### 正式Go标准（无需Day 3）

**在Conditional Go基础上额外满足：**
- ✓ 列表接口完成
- ✓ Smoke test覆盖负向场景

---

## 风险和应对

### 风险1：Seed/mock修复遇到阻塞

**可能原因：**
- MockDormCheckoutProvider逻辑复杂
- CSV模板格式问题

**应对：**
- 先修复2020002的class_id（5分钟）
- 再修复MockDormCheckoutProvider（15分钟）
- 如果卡住，记录问题，继续后续任务

### 风险2：状态机保护实现复杂

**可能原因：**
- 事务和锁的语法不熟悉
- 状态机验证逻辑复杂

**应对：**
- 先添加基础事务保护（30分钟）
- 再添加状态验证（30分钟）
- 如果超时，降级为只做事务保护

### 风险3：Smoke test脚本调试耗时

**可能原因：**
- jq语法不熟悉
- 动态提取ID逻辑复杂

**应对：**
- 先写正向路径骨架（30分钟）
- 再优化错误处理（30分钟）
- 如果超时，降级为手工验证命令集合

---

## 我的最终建议

**立即开始Day 2执行，按以下策略：**

1. **执行模式：** 串行执行，允许跳过阻塞项
2. **验证策略：** 手工验证，记录验证命令
3. **时间分配：** 3小时执行 + 1小时缓冲
4. **阻塞应对：** 评估影响，记录问题，继续或跳过
5. **成功标准：** Conditional Go（6项核心任务完成）

**不建议：**
- 不做额外准备工作（会模糊timebox边界）
- 不追求完美（Conditional Go即可）
- 不写自动化测试（smoke test骨架即可）

---

## 关键问题需要Codex回应

1. **立即开始 vs 准备后开始？**
   - 我建议立即开始，Codex是否同意？
   - 是否有必要的准备工作被我遗漏？

2. **串行执行 vs 并行执行？**
   - 我建议串行执行，Codex是否同意？
   - 是否有任务可以安全并行？

3. **手工验证 vs 自动化测试？**
   - 我建议手工验证，Codex是否同意？
   - 是否有任务必须写自动化测试？

4. **时间分配是否合理？**
   - 我建议3小时执行 + 1小时缓冲，Codex是否同意？
   - 是否有任务的时间估算过于乐观？

5. **阻塞应对策略是否合理？**
   - 我建议评估影响后决定跳过或坚持，Codex是否同意？
   - 是否有任务绝对不能跳过？

---

**提案状态：** 已完成，等待Codex审查  
**核心建议：** 立即开始，串行执行，手工验证，3+1小时分配
