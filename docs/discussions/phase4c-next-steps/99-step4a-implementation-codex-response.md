# Phase 4C Step 4A实现 - Codex审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对文档：** `docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md`  
**审查范围：** `backend/apps/users/services/xg_user_sync.py`、`docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md`、`docs/phase4c-xg-field-coverage.md`

## 审查结论

**结论：需要小修改后再创建测试。**

当前服务实现整体符合文档97的Step 4A只读计划服务方向：调用mapper、不写DB、本地不存在计入missing、角色冲突进入conflicts、输出9字段summary，这些主路径是正确的。

但有一个必须先澄清并落地的小问题：`would_update_count`现在按"本地存在且role=student"计数。若该字段表示"真实可写更新数"，当前User模型没有`phone/email/department`，`name`是否允许API覆盖也未决，因此真实可更新字段数应为0。若该字段表示"未来可更新候选数"，则字段名有误导性，测试必须明确锁定这个语义。

我的建议：Step 4A保持9字段结构不扩展，但在实现和测试中明确把`would_update_count`定义为"现有学生同步候选数，不代表当前模型可持久化写入数"，同时warning必须指出当前无补充字段可落库、真实upsert仍被Step 4B阻塞。

## 发现的问题

### 问题1：`would_update_count`语义容易锁错测试 [P1]

**位置：** `backend/apps/users/services/xg_user_sync.py:69`

**问题描述：** 当前实现只要本地用户存在且角色为`student`，就执行`would_update_count += 1`。这符合文档97第4条"已存在学生计入would_update_count"，但与字段覆盖文档的Phase 1事实存在张力：User模型当前没有`phone/email/department`字段，`name`是否允许由API覆盖仍未决。

**影响：** 如果后续测试把`would_update_count`理解为"当前会真实更新DB的记录数"，测试会锁定错误业务语义。Step 4B实现时也可能误以为已有可写字段，可以直接做upsert。

**修复建议：**
- 在函数docstring或返回注释中明确：`would_update_count`是"existing student candidate count"，不是当前可持久化更新数。
- 保留当前计数也可以，但warning文本应更强：`would_update_count` candidates exist, but no supplemental API fields can be persisted until User model adds phone/email/department or name overwrite policy is approved。
- 如果团队希望`would_update_count`严格表示真实可写更新数，则当前实现应改为0，并把现有学生只计入`existing_count`。不过这会偏离文档97的9字段契约，需先改共识文档。

### 问题2：字段gap warning触发条件偏窄 [P2]

**位置：** `backend/apps/users/services/xg_user_sync.py:77`

**问题描述：** 当前只有`would_update_count > 0`时才输出模型字段gap warning。若输入中只有missing_local用户，但mapper已经产出`phone/department`，仍然存在同一个字段gap和Phase 1创建阻塞问题，只是现在只有逐用户`would_create_but_blocked` warning。

**影响：** 空更新候选但有API补充字段的批次，不会给出全局字段gap提示。对dry-run summary阅读者来说，可能不清楚Step 4B为什么仍不可做真实upsert。

**修复建议：**
- 至少在`mapped_count > 0`且任一mapped结果包含`phone`或`department`时输出字段gap warning。
- 如果保持当前规则，则测试场景6必须明确为"存在would_update候选时输出warning"，不要声称所有字段gap场景都会输出全局warning。

### 问题3：`MultipleObjectsReturned`无需实际捕获，但应在测试/说明中记录原因 [P3]

**位置：** `backend/apps/users/services/xg_user_sync.py:55`

**问题描述：** 审查请求Q1提到`MultipleObjectsReturned`。当前查询字段`user_id`是User主键且unique，正常数据库约束下不会出现多条记录。

**影响：** 无实际实现缺陷。额外捕获`MultipleObjectsReturned`反而可能掩盖数据完整性损坏。

**修复建议：**
- 不需要捕获`MultipleObjectsReturned`。
- 可以在测试策略或代码注释中说明：`user_id`是主键，重复记录属于数据库完整性问题，不在同步计划服务中降级处理。

## 审查通过的部分

1. `map_xg_user_to_internal()`调用位置正确，每条输入先走mapper。
2. mapper返回`skip_reason`时直接计入`skipped_count`和`skipped_by_reason`，不会继续查库，符合skip透传规则。
3. `User.objects.get(user_id=user_id)`用于本地存在性判断是正确的。
4. `User.DoesNotExist`计入`missing_local_count`，且不创建用户，符合Phase 1边界。
5. 本地存在但`role != 'student'`进入`conflicts`，结构包含`user_id`、`reason`、`local_role`、`api_role`，足够支撑后续报告。
6. 返回结构包含文档97要求的9个字段，字段类型也基本正确。
7. 服务没有写DB，不会覆盖`class_id/is_graduating/graduation_year`。

## 对关键质疑点的回答

### Q1：User.objects.get异常处理

`User.DoesNotExist`捕获正确。`MultipleObjectsReturned`不需要捕获，因为`user_id`是主键和unique字段；如果发生，说明数据库完整性已破坏，应让异常暴露。

### Q2：would_update计数准确性

这是本轮唯一需要先处理的语义问题。

如果`would_update_count`表示"现有学生同步候选"，当前实现正确。如果表示"当前真实可写更新"，当前实现不准确，因为可安全写入字段未成立：`phone/email/department`不存在，`name`覆盖策略未决。建议在Step 4A把它定义为候选数，并用warning明确真实写入仍不可执行。

### Q3：conflicts结构完整性

当前结构足够：`user_id`、`reason='role_mismatch'`、`local_role`、`api_role`。可选增强是加入`name`，便于人工排查，但不应作为Step 4A阻塞项。

### Q4：skipped_by_reason统计

当前累加逻辑正确，不会把`None`作为key，因为只有`mapped['skip_reason']` truthy时才进入分支。多个skip reason也能正确累计。建议测试补充"两个不同skip_reason + 一个重复skip_reason"混合场景。

### Q5：测试场景5的必要性

有必要保留，但应调整断言目标。Step 4A只读，不需要测试"写入后未覆盖"；应该测试：

- 服务执行后本地User的`class_id/is_graduating/graduation_year`保持不变；
- summary不暴露任何会覆盖这些核心字段的计划项；
- missing_local不会被创建。

## 测试覆盖建议

文档97列出的8个场景覆盖了关键路径，可以执行，但建议对其中两个场景做精确定义：

1. "已存在学生进入existing"：断言`existing_count=1`，并按最终语义断言`would_update_count`。
2. "不覆盖class_id/is_graduating/graduation_year"：断言服务只读后DB原值不变，不要模拟Step 4B写入行为。
3. "phone/department无模型字段warning"：断言warning文本明确说明不能持久化补充字段，并且不会影响`existing_count`。
4. "混合场景"：应包含至少一个skip、一个missing_local、一个role conflict、一个existing student，并断言所有计数互不串类。
5. 建议补充多个skip reason统计，或纳入混合场景，避免只测单一reason。

测试实现建议使用Django `TestCase` 和真实测试数据库创建User，不建议mock `User.objects.get`。原因是此服务的关键边界正是Django模型主键查询、DoesNotExist异常、角色字段值和"不写DB"保证，真实DB测试更有价值且成本很低。

## 后续执行建议

1. 先小改服务注释/warning，解决`would_update_count`语义歧义。
2. 创建`backend/apps/users/tests/test_xg_user_sync.py`，使用真实Django测试数据库覆盖8个场景。
3. 运行用户服务相关测试：`backend/apps/users/tests/test_xg_user_mapper.py`和新增`test_xg_user_sync.py`。
4. 测试通过后再进入Step 4B模型扩展决策，不要直接做真实upsert。

