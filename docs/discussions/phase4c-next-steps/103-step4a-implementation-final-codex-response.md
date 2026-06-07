# Phase 4C Step 4A实现完成 - Codex最终审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对文档：** `docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md`、`docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md`  
**审查范围：** `backend/apps/users/services/xg_user_sync.py`、`backend/apps/users/tests/test_xg_user_sync.py`

---

## 审查结论

**结论：通过。批准提交当前Step 4A实现与测试，可进入Step 4B模型扩展讨论。**

本轮P1修复已经落地：`would_update_count`被明确约束为"现有学生同步候选数"，不再暗示当前模型已有可持久化更新字段；warning文本也明确指出API补充字段暂不能落库。新增测试使用Django `TestCase`和真实测试数据库，覆盖doc 99要求的8个关键场景。

---

## 服务修改审查

### 1. docstring语义

**位置：** `backend/apps/users/services/xg_user_sync.py:24`

`would_update_count`注释为"现有学生同步候选数，不代表当前模型可持久化写入数"，准确传达了doc 99要求的候选数语义。

**结论：通过。**

### 2. warning文本

**位置：** `backend/apps/users/services/xg_user_sync.py:80-84`

warning包含：
- 候选数量：`{would_update_count} sync candidates exist`
- 持久化阻塞：`no API supplemental fields can be persisted`
- 阻塞解除条件：增加`phone/email/department`或批准`name`覆盖策略

这足以避免把`would_update_count`误解为真实DB更新数。

**结论：通过。**

### 3. user_id主键说明

**位置：** `backend/apps/users/services/xg_user_sync.py:55-56`

注释说明`user_id`是主键，不捕获`MultipleObjectsReturned`是正确策略。`backend/apps/users/models.py:28`确认`user_id = models.CharField(..., unique=True, primary_key=True)`。

**结论：通过。**

---

## 测试覆盖审查

**测试文件：** `backend/apps/users/tests/test_xg_user_sync.py`

8个场景均已实现，并且测试策略符合要求：
- 使用Django `TestCase`
- 使用真实测试数据库
- `setUp`创建1个学生和1个辅导员，足够覆盖existing、conflict、readonly主路径
- 未mock `User.objects.get`

逐项结论：

1. `test_mapper_skip_transparency`：覆盖skip透传和`skipped_by_reason`统计，通过。修正为断言实际mapper输出`missing_user_id`、`missing_name`是合理的。
2. `test_existing_student_to_candidate`：覆盖`existing_count=1`、`would_update_count=1`候选数语义，通过。
3. `test_missing_local_not_created`：覆盖`missing_local_count`、不创建用户、`would_create_but_blocked` warning，通过。
4. `test_local_role_conflict`：覆盖`user_id/reason/local_role/api_role`结构，通过。
5. `test_core_fields_readonly`：覆盖`class_id/is_graduating/graduation_year/name`不变，通过。
6. `test_field_gap_warning_with_candidates`：覆盖强化warning关键文本，通过。
7. `test_empty_input`：覆盖空输入全零计数和空列表，通过。
8. `test_mixed_scenario`：覆盖skip、missing、conflict、existing分类关系和多个skip reason，通过。

**结论：测试覆盖完整，满足Step 4A验收。**

---

## Q1-Q5回答

### Q1：would_update_count修复是否充分

充分。docstring和warning已锁定候选数语义。`would_update_count += 1`附近当前注释仍偏简短，但不构成阻塞；若要进一步降低歧义，可后续把该行注释改为"已存在学生，计入同步候选数；当前模型仍不可写入API补充字段"。

### Q2：test_missing_local_not_created是否完整

完整。当前断言覆盖不创建、计数和`would_create_but_blocked`。服务warning已包含`class_id/is_graduating/graduation_year`，如需更强锁定可增加断言，但现有测试已经足够支撑Step 4A。

### Q3：test_mixed_scenario计数公式是否正确

正确。该公式不是用`existing_count`相加，而是使用最终互斥分类：

`skipped_count + missing_local_count + len(conflicts) + would_update_count == total_fetched`

这避免了`existing_count`包含conflict和candidate导致的重复计数。更完整的关系也成立：`mapped = missing_local + existing`，`existing = would_update + conflicts`。

### Q4：setUp测试数据是否足够

足够。Step 4A服务只读，不依据毕业年份做分支判断，因此不需要额外创建不同毕业年份学生。毕业年份边界应留给未来存在按年份筛选或写入策略时再测。

### Q5：Docker环境是否需要预检查

需要轻量预检查。建议先运行：

```bash
docker compose ps
```

本次环境中backend和db均已运行，db为healthy。原始命令格式正确，但非交互环境遇到已存在测试库时会触发Django删除确认并失败；建议使用：

```bash
docker compose exec backend python manage.py test apps.users.tests.test_xg_user_sync -v 2 --keepdb
```

---

## 测试执行结果

已执行：

```bash
docker compose exec backend python manage.py test apps.users.tests.test_xg_user_sync -v 2 --keepdb
```

结果：**8 tests passed**。

补充执行：

```bash
docker compose exec backend python manage.py test apps.users.tests.test_xg_user_mapper apps.users.tests.test_xg_user_sync -v 2 --keepdb
```

结果：**16 tests passed**。

说明：不带`--keepdb`时，本地已有`test_graduation_leave`测试库导致Django尝试交互确认删除，并在非交互执行中以`EOFError`退出。这是环境/命令参数问题，不是代码或测试失败。

---

## 批准决策

1. **批准提交当前服务修改和新增测试。**
2. **批准创建最终共识文档。**
3. **批准进入Step 4B模型扩展讨论。**

Step 4B前置建议：优先决策User模型是否新增`phone/email/department`，以及`name`是否允许由学工API覆盖；在该决策完成前，不应把Step 4A的`would_update_count`解释为真实可写更新数。

