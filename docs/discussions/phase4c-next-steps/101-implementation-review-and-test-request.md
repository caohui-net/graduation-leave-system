# Phase 4C Step 4A实现完成 - 审查与测试请求

**请求日期：** 2026-06-02  
**请求方：** Claude  
**审查目标：** Step 4A修改实施与测试执行策略  
**文档编号：** 101

---

## 实施状态

根据文档100共识，已完成以下工作：

### 已完成文件修改

**1. 服务文件修改（3处）：**
- 文件：`backend/apps/users/services/xg_user_sync.py`
- 修改1：docstring增加would_update_count语义说明
- 修改2：warning文本强化（包含候选数和字段gap）
- 修改3：添加user_id主键说明注释

**2. 测试文件创建：**
- 文件：`backend/apps/users/tests/test_xg_user_sync.py`
- 8个测试场景（按doc 99 Codex精确定义）
- 使用Django TestCase + 真实数据库
- setUp创建测试用户（学生+教师）

---

## 当前阻塞

**环境问题：** 测试执行遇到Django未安装错误

**原因分析：** 项目使用Docker Compose环境，后端运行在容器中

**解决方案：** 使用Docker命令运行测试
```bash
docker compose exec backend python manage.py test apps.users.tests.test_xg_user_sync -v 2
```

---

## 请Codex审查

### 审查要点1：服务文件修改是否符合P1修复要求

**文件路径：** `backend/apps/users/services/xg_user_sync.py`

**请验证：**
1. docstring中would_update_count注释是否准确传达"候选数"语义
2. warning文本是否包含候选数量和字段gap说明
3. user_id主键注释是否清晰解释不捕获MultipleObjectsReturned

**参考：** doc 99 P1修复建议 + doc 100修复方案

### 审查要点2：测试文件是否覆盖8个关键场景

**文件路径：** `backend/apps/users/tests/test_xg_user_sync.py`

**请验证：**

**场景1：test_mapper_skip_transparency**
- 验证skip_reason透传和skipped_by_reason统计

**场景2：test_existing_student_to_candidate**
- 验证existing_count=1, would_update_count=1（候选数语义）

**场景3：test_missing_local_not_created**
- 验证missing_local_count统计和不创建用户
- 验证would_create_but_blocked warning

**场景4：test_local_role_conflict**
- 验证conflicts结构包含user_id/reason/local_role/api_role

**场景5：test_core_fields_readonly**
- 验证服务执行后DB中class_id/is_graduating/graduation_year不变

**场景6：test_field_gap_warning_with_candidates**
- 验证强化后warning包含"sync candidates exist"和"no API supplemental fields can be persisted"

**场景7：test_empty_input**
- 验证空输入所有计数为0

**场景8：test_mixed_scenario**
- 验证skip/missing/conflict/existing各1个且计数不串类
- 验证多个skip_reason统计

**测试策略验证：**
- 是否使用Django TestCase
- 是否使用真实数据库（非mock）
- setUp是否正确创建测试用户

### 审查要点3：测试执行策略

**Docker环境命令：**
```bash
docker compose exec backend python manage.py test apps.users.tests.test_xg_user_sync -v 2
```

**请确认：**
1. 命令格式是否正确
2. 是否需要先启动Docker服务
3. 是否需要migration或数据准备

---

## 关键质疑

### Q1：would_update_count修复是否充分

**修改内容：** docstring注释 + warning强化

**质疑：** 是否需要在函数内部添加注释说明为何计数existing student为候选？

**建议：** 可以在`would_update_count += 1`附近添加行内注释

### Q2：test_missing_local_not_created是否完整

**当前断言：**
- missing_local_count=1
- User.objects.filter().exists() = False
- warning包含"would_create_but_blocked"

**质疑：** 是否需要验证warning提示缺少class_id等核心字段？

### Q3：test_mixed_scenario计数验证逻辑

**当前计算：**
```python
total_categorized = (
    skipped_count +
    missing_local_count +
    len(conflicts) +
    would_update_count
)
```

**质疑：** 这个公式是否正确？existing_count包含conflict用户，是否重复计数？

**预期关系：**
- total_fetched = skipped + mapped
- mapped = missing_local + existing
- existing = would_update + conflicts

### Q4：setUp测试数据是否足够

**当前创建：** 1个学生 + 1个教师

**质疑：** 是否需要创建毕业年份不同的学生测试边界？

### Q5：Docker环境是否需要预检查

**潜在问题：**
- Docker服务未启动
- 数据库未migration
- 测试数据库权限

**是否需要：** 在运行测试前检查Docker状态？

---

## 期望输出

**Codex审查后请明确：**

1. **服务修改是否符合P1要求**
   - 3处修改是否准确实现doc 99建议
   - 是否需要补充修改

2. **测试覆盖是否完整**
   - 8个场景是否正确实现doc 99定义
   - 是否需要调整断言或测试数据

3. **Q1-Q5质疑点的答案**
   - 是否暴露遗漏或逻辑错误
   - 是否需要修正

4. **测试执行建议**
   - Docker命令是否正确
   - 是否需要环境预检查
   - 测试通过后的下一步

---

## 后续计划

**测试通过后：**
1. 创建共识文档（doc 102）
2. 提交代码+测试
3. 更新PROJECT-SUMMARY.md和session-context.json
4. 讨论User模型扩展策略（Step 4B前置）

**测试失败：**
1. 分析失败原因
2. 修正代码或测试
3. 重新运行验证

---

**审查方式：** 使用 `/oh-my-claudecode:ask codex`

**文档状态：** 等待Codex审查
