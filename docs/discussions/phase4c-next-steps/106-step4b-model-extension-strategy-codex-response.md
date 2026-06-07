# Phase 4C Step 4B前置 - User模型扩展策略Codex审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对文档：** `docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md`  
**审查类型：** 模型扩展策略 / 数据源权威性决策 / Step 4B范围确认  
**文档编号：** 106

---

## 审查结论

**推荐选项组合2：扩展User模型 + 不允许学工API覆盖name。**

Step 4B应该新增并持久化`phone`、`email`、`department`三个API补充字段，但继续保持`name`、`class_id`、`is_graduating`、`graduation_year`由CSV/手工维护。这个方案与既有Phase 1策略一致：CSV负责用户创建和核心业务字段，学工API只补充联系方式/院系等非核心字段。

不推荐组合1，因为允许API覆盖`name`会破坏已达成的CSV主导边界，并引入CSV重新导入与API同步之间的反复覆盖问题。不推荐组合3，因为它会让Step 4B没有真实写入目标，最终只能停留在Step 4A的候选报告。

---

## 问题清单

### P1：如果不扩展模型，Step 4B应取消而不是伪实现

当前`User`模型只包含`user_id/name/role/active/class_id/is_graduating/graduation_year`，mapper输出的`phone/department`无处落库。若选择“不扩展模型”，Step 4B不应改为`name`覆盖或其他轻量写入；应明确标记为跳过，保留Step 4A只读报告，并将后续Step 5命令限定为dry-run/plan命令。

### P1：name不应纳入API upsert字段

字段覆盖契约已经定义CSV负责`user_id/name/role/class_id/is_graduating/graduation_year`，API负责`phone/email/department`。`name`虽然来自API，但它是核心身份展示字段，且CSV导入当前会更新`name`。允许API覆盖会造成数据源权威性不清晰。

建议在Step 4B中完全不写`name`。如需观察差异，可以只输出`name_mismatch` warning或conflict报告，不修改数据库。

### P2：email字段需要同时补mapper和测试

字段契约包含`email`，但当前`map_xg_user_to_internal()`只提取`phone`和`department`。如果模型新增`email`，Step 4B应同步补充mapper提取和测试；否则会出现模型有字段但服务永远无法更新的半成品状态。

### P2：不要新增API语义的updated_at字段

`User`模型已有本地`updated_at = auto_now=True`。Step 4B不应直接把学工API的`updated_at`并入同名字段，也不建议现在新增`xg_updated_at`。API更新时间语义尚未live确认，且当前目标是解除补充字段落库阻塞。同步审计字段可在命令入口或审计需求明确后再设计。

---

## 字段扩展决策

### 推荐新增字段

```python
phone = models.CharField(max_length=20, null=True, blank=True)
email = models.EmailField(null=True, blank=True)
department = models.CharField(max_length=100, null=True, blank=True)
```

迁移风险低：三个字段均为nullable，不影响现有行写入，不需要数据回填，回滚也清晰。`phone`使用`CharField`而不是整数类型是正确的，因为手机号可能包含前导0、区号、分机、符号或非大陆格式。

### API缺失值处理

对已存在用户，Step 4B应采用保守规则：

- API返回非空值且与本地不同：更新该字段
- API未返回字段、返回`None`或空字符串：保持本地原值
- 不在本阶段实现“API清空本地联系方式”

这个规则能避免API抽样、权限、分页或字段缺失导致已有联系方式被误清空。若未来确认API是权威联系方式源，再单独增加“允许清空”的策略开关。

---

## name覆盖决策

**不允许API更新`name`。**

推荐冲突优先级：

| 字段类别 | 字段 | 权威来源 | API同步行为 |
|---------|------|----------|-------------|
| 身份核心 | `user_id` | CSV/本地主键 | 只匹配，不修改 |
| 身份展示 | `name` | CSV | 不修改，可报告差异 |
| 角色/权限 | `role` | CSV/本地 | 只验证学生身份，冲突则跳过 |
| 业务核心 | `class_id/is_graduating/graduation_year` | CSV | 不修改 |
| 补充资料 | `phone/email/department` | 学工API | 仅更新已存在学生 |

不需要为`name`引入`updated_at`比较策略。时间戳比较不能解决“哪个系统更权威”的问题，只会把权威性决策隐藏到时间顺序里。

---

## Step 4B实施范围

### 最小可交付范围

1. User模型新增`phone/email/department`并生成migration。
2. mapper新增`email`提取，缺失时返回`None`。
3. 新增真实同步服务，或扩展现有服务为明确的dry-run/apply双模式。
4. 仅对本地已存在且`role='student'`的用户更新补充字段。
5. 本地不存在用户继续不创建。
6. 本地角色不是student时继续输出conflict并跳过。
7. 不更新`name/class_id/is_graduating/graduation_year/role/active`。
8. 返回真实写入统计，例如`candidate_count`、`updated_count`、`unchanged_count`、`changed_fields_by_user`、`conflicts`、`warnings`。

### 不建议纳入Step 4B

- 不做`name`覆盖。
- 不创建新用户。
- 不扩展CSV导入器读取`phone/email/department`，除非另开CSV契约修订。
- 不调整REST serializer公开字段，除非产品/API契约明确需要展示这些字段。
- 不引入API时间戳权威判断。

### 预计工作量

预计40-70分钟：

- 模型+migration：10-15分钟
- mapper email补充+测试：10-15分钟
- 同步服务真实更新+测试：25-40分钟
- 回归验证：5-10分钟

---

## 验收标准

Step 4B完成时应满足：

1. `makemigrations`生成只包含`phone/email/department`的users migration。
2. mapper测试覆盖`email`存在、缺失两个场景。
3. 服务测试覆盖已存在学生更新`phone/email/department`。
4. 服务测试覆盖API缺失补充字段时保持本地原值。
5. 服务测试覆盖幂等：第二次同步`updated_count=0`或等价无变化统计。
6. 服务测试覆盖不创建本地缺失用户。
7. 服务测试覆盖角色冲突不更新。
8. 服务测试覆盖`name/class_id/is_graduating/graduation_year`不被API覆盖。
9. Step 4A中的“no API supplemental fields can be persisted” warning应被移除或改为只在字段不可写时触发。

---

## Q1-Q5回答

### Q1：字段契约定义 vs 当前需求

当前系统未证明页面或业务流程立即需要`phone/email/department`，但字段契约和Phase 1策略已经把它们定义为API补充字段；同时这三个字段是通知、联系、展示和院系统计的自然基础字段。考虑到nullable migration风险低，且Step 4B需要真实写入目标，现在扩展是合理的。

关键边界是：新增字段不等于立即扩大所有API/CSV表面。先解决存储和同步闭环即可。

### Q2：CSV与API权威性

Phase 1应明确为：CSV是用户存在性、角色、班级、毕业资格、姓名的权威来源；学工API是联系方式和院系补充来源。API不是当前阶段的用户主数据源。

因此，CSV可持续导入并覆盖核心字段；API只更新补充字段。

### Q3：migration时机

建议现在做，在Step 5命令入口前完成。原因是Step 5如果基于当前模型继续推进，只能做dry-run命令；真实同步命令仍会卡在字段gap。现在新增nullable字段影响面小，也能让后续命令、测试、验收基于同一套真实行为。

### Q4：mapper email提取

需要补充。即使live数据暂未确认`email`字段，也应让mapper支持直接字段提取：

```python
email = xg_user.get('email')
result['email'] = email
```

如果API实际字段名不是`email`，后续live样本确认后再增加别名映射。当前不要猜测复杂字段名。

### Q5：Step 4B最小范围

最小范围应包含`phone/email/department`三字段的真实持久化。若担心email数据源不确定，也仍建议模型包含email，mapper先按直接`email`字段提取，服务自然只在API提供非空email时更新。

不建议做Step 4B-lite仅更新`name`。这会绕开真正的字段gap，并制造新的CSV/API冲突。

---

## 最终建议

批准进入Step 4B实现，采用以下决策：

1. 新增`User.phone`、`User.email`、`User.department`。
2. API只更新已存在学生的补充字段。
3. API不创建用户。
4. API不覆盖`name`和毕业业务核心字段。
5. mapper补`email`。
6. 缺失/空补充字段保持本地原值。
7. Step 4B测试以“真实写入 + 幂等 + 不覆盖核心字段”为验收核心。

