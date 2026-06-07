# Phase 4C Step 4A实现 - Codex审查与测试响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对文档：** `docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md`  
**审查范围：** `backend/apps/users/services/xg_user_sync.py`、`backend/apps/users/tests/test_xg_user_sync.py`  
**结论：** 通过，建议补充少量测试断言后进入共识/提交流程

---

## 审查结论

**服务修改符合doc 99 P1修复要求。**

3处服务修改已经落地：

1. `would_update_count`在docstring中被定义为"现有学生同步候选数，不代表当前模型可持久化写入数"。
2. 字段gap warning已强化，包含候选数量、`sync candidates exist`、`no API supplemental fields can be persisted`、`phone/email/department`以及name覆盖策略未批准的阻塞说明。
3. `User.objects.get(user_id=user_id)`附近已说明`user_id`是主键，不需要捕获`MultipleObjectsReturned`。

**测试文件覆盖了8个关键场景，并使用Django `TestCase` + 真实测试数据库。**

测试运行通过，说明当前实现没有暴露行为回归。

---

## 发现的问题

### 问题1：skip_reason统计断言可以更精确 [P3]

**位置：** `backend/apps/users/tests/test_xg_user_sync.py:43-49`、`backend/apps/users/tests/test_xg_user_sync.py:212-214`

当前测试已经验证`skipped_count`和部分`skipped_by_reason` key，但没有锁定完整字典和每个reason的计数。作为"透传和统计"测试，建议改成精确断言：

```python
self.assertEqual(result['skipped_by_reason'], {
    'missing_user_id': 1,
    'missing_name': 1,
    'unknown_user_identity: 9': 1,
})
```

混合场景也建议断言具体key，而不只是`len(...) == 2`。

**影响：** 非阻塞。当前测试能发现主路径错误，但对reason字符串被误改、统计计数串类的保护不够强。

### 问题2：missing_local warning建议锁定核心字段gap文本 [P3]

**位置：** `backend/apps/users/tests/test_xg_user_sync.py:94-97`

`plan_xg_user_sync()`当前warning已经包含`lacks class_id/is_graduating/graduation_year`，符合Phase 1不创建边界。测试目前只断言`would_create_but_blocked`。

建议补充：

```python
self.assertIn('class_id', warning_text)
self.assertIn('is_graduating', warning_text)
self.assertIn('graduation_year', warning_text)
```

**影响：** 非阻塞。服务实现正确，但测试还没有完全锁定Q2关心的提示语义。

### 问题3：mixed_scenario注释与数据数量不完全一致 [P3]

**位置：** `backend/apps/users/tests/test_xg_user_sync.py:184-185`

测试名/注释写"skip/missing/conflict/existing各1个"，实际数据有2个skip。这是合理的，因为同一测试还要验证多个skip reason；但建议把注释改为"覆盖skip/missing/conflict/existing，skip包含两个reason"。

**影响：** 仅可读性问题，不影响测试正确性。

---

## 服务修改审查

### 1. docstring语义

通过。`would_update_count`已明确为候选数，不是当前可持久化写入数。该定义与doc 99建议一致，也避免Step 4B误以为已有真实upsert能力。

`would_update_count += 1`附近已有"已存在学生，计入would_update"注释。更严谨的写法可以改为"已存在学生，计入同步候选数；不代表当前模型可落库更新"，但不是阻塞项，因为docstring和warning已经说明完整语义。

### 2. warning文本

通过。warning包含：

- 候选数量：`{would_update_count} sync candidates exist`
- 字段gap：`no API supplemental fields can be persisted`
- 缺失字段：`phone/email/department`
- 策略阻塞：`name overwrite policy is approved`

这满足doc 99 P1修复目标。

### 3. user_id主键说明

通过。`user_id`在`backend/apps/users/models.py`中是`primary_key=True`且`unique=True`，不捕获`MultipleObjectsReturned`是正确选择。若该异常出现，应视为数据库完整性损坏，不应在同步计划服务里静默降级。

---

## 测试覆盖审查

8个场景均已实现：

1. `test_mapper_skip_transparency`：覆盖mapper skip、`skipped_count`、`skipped_by_reason`。
2. `test_existing_student_to_candidate`：覆盖`existing_count=1`、`would_update_count=1`候选数语义。
3. `test_missing_local_not_created`：覆盖`missing_local_count=1`、不创建用户、`would_create_but_blocked` warning。
4. `test_local_role_conflict`：覆盖`user_id/reason/local_role/api_role`冲突结构。
5. `test_core_fields_readonly`：覆盖服务执行后`class_id/is_graduating/graduation_year/name`不变。
6. `test_field_gap_warning_with_candidates`：覆盖强化warning关键文本。
7. `test_empty_input`：覆盖空输入计数和列表为空。
8. `test_mixed_scenario`：覆盖skip、missing、conflict、existing并验证分区计数关系。

测试策略正确：

- 使用Django `TestCase`。
- 使用真实测试数据库。
- `setUp()`创建1个学生和1个辅导员，足够覆盖当前8个场景。
- 没有mock `User.objects.get`，能真实验证主键查询、`DoesNotExist`和只读边界。

---

## Q1-Q5回答

### Q1：would_update_count修复是否充分？

充分。docstring + warning已经解决P1语义风险。建议把`would_update_count += 1`附近注释也改成"候选数"措辞，但这只是清晰度增强，不影响通过。

### Q2：test_missing_local_not_created是否完整？

服务实现完整，测试基本完整。建议补充断言`class_id/is_graduating/graduation_year`出现在warning中，以锁定"为什么不创建"的核心字段gap。

### Q3：test_mixed_scenario计数验证逻辑是否正确？

正确。公式：

```python
skipped_count + missing_local_count + len(conflicts) + would_update_count == total_fetched
```

在当前语义下成立，因为：

- `skipped`不进入mapped；
- mapped分为`missing_local`和`existing`；
- existing再分为`conflicts`和`would_update candidates`。

`existing_count`包含conflict用户没有问题，因为公式没有把`existing_count`加入分类总和，不会重复计数。

### Q4：setUp测试数据是否足够？

足够。当前Step 4A不根据`graduation_year`做分支判断，只需要验证字段不被修改。不同毕业年份边界应留到出现年份过滤或Step 4B写入策略时再加。

### Q5：Docker环境是否需要预检查？

建议预检查，但不是复杂前置流程。最低限度：

```bash
docker compose ps
```

本次检查结果：`backend`已运行，`db`已运行且healthy。

---

## 测试执行结果

首次执行：

```bash
docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_sync -v 2
```

结果：发现旧测试库`test_graduation_leave`已存在，Django尝试询问是否删除；非交互环境下触发`EOFError`。

修正执行：

```bash
docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_sync -v 2 --noinput
```

结果：8 tests，全部通过。

补充回归：

```bash
docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_mapper apps.users.tests.test_xg_user_sync -v 2 --noinput
```

结果：16 tests，全部通过。

说明：

- `-T`适用于Codex/CI等非TTY环境；用户在交互终端运行时可省略。
- `--noinput`建议保留，避免旧测试数据库残留时卡在确认提示。
- 测试启动时会自动创建测试数据库并执行migrations，不需要额外数据准备。

---

## 最终建议

**可以进入后续流程：**

1. 可选补强3处测试断言/注释（P3，不阻塞）。
2. 创建共识文档。
3. 提交服务修改和新增测试。
4. 进入Step 4B前置讨论：User模型扩展与name覆盖策略。

**推荐测试命令：**

```bash
docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_mapper apps.users.tests.test_xg_user_sync -v 2 --noinput
```
