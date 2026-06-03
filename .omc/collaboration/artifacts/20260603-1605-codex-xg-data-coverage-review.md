# XG API数据覆盖度审查报告

**审查方：** Codex  
**请求标记：** `--model opus`  
**审查时间：** 2026-06-03 16:05 UTC  
**审查类型：** 数据对接覆盖度 / 映射策略审查  
**输入文档：**
- `docs/数据对接说明文档.md`
- `docs/XG-API-ACTUAL-DATA-SAMPLES.md`
- `docs/phase4c-xg-field-coverage.md`

## 1. 总体结论

**结论：XG用户API可以作为“已有用户补充信息源”，不能替代当前CSV主数据源。**

实际采集数据证明，XG API对身份识别基础字段覆盖较好：`number`、`name`、`status`为100%完整，`user_identity`、`department`、`parent_dep`关联对象为100%存在，`phone`为80%有效。数据量侧也确认有32,039条用户记录。

但毕业生离校审批的核心业务字段没有被实际样本覆盖：`class_id`、`graduation_year`、`is_graduating`、班级-辅导员映射、宿舍清退状态均缺失或不属于该用户API。缺这些字段时，系统无法可靠完成申请资格判定、辅导员自动分配、毕业批次归档和宿舍清退阻断。

推荐策略维持：**CSV主导 + XG API补充**。API仅更新已存在学生的非核心字段，如 `phone`、`email`、`department`、`active/status`；不创建新学生、不覆盖核心业务字段、不自动停用本地用户。

## 2. 证据摘要

### 2.1 需求侧字段

需求文档要求学生数据包含：`student_id`、`name`、`department`、`major`、`class_id`、`grade`、`graduation_year`、`is_graduating`，其中 `class_id`、`graduation_year`、`is_graduating`为核心字段。见 `docs/数据对接说明文档.md:61-69`。

需求文档明确 `class_id` 用于班级-辅导员映射和审批人分配，且导入后需要验证班级映射覆盖率。见 `docs/数据对接说明文档.md:195`、`:237`。

宿舍清退是独立实时API需求，提交申请时需要查询 `checkout_status`。见 `docs/数据对接说明文档.md:247-354`。

### 2.2 实际XG样本字段

实际样本文档显示：
- 总记录数：32,039，分页测试每页10条。见 `docs/XG-API-ACTUAL-DATA-SAMPLES.md:27-29`。
- 20条采样中：`number`、`name`、`status`完整率100%，`phone`完整率80%。见 `docs/XG-API-ACTUAL-DATA-SAMPLES.md:47-54`。
- `user_identity`、`department`、`parent_dep`存在率100%，`user`对象90%。见 `docs/XG-API-ACTUAL-DATA-SAMPLES.md:65-67`。
- 实际单条用户样本包含 `number`、`name`、`phone`、`status`、`parent_dep`、`department`、`user_identity`。见 `docs/XG-API-ACTUAL-DATA-SAMPLES.md:88-94`。

### 2.3 映射方案状态

现有映射方案已正确识别 `class_id`、`is_graduating`、`graduation_year`为API缺失字段，并建议继续由CSV/手工维护。见 `docs/phase4c-xg-field-coverage.md:119-121`。

现有方案也提出当前阶段使用“CSV导入（主）+ 学工API（补充）”，并明确学工API不创建新用户。见 `docs/phase4c-xg-field-coverage.md:188-196`。

## 3. 字段覆盖度评估

| 业务域 | 需求字段 | XG实际覆盖 | 覆盖结论 |
|---|---|---|---|
| 学生身份识别 | `student_id/name` | `number/name` 100% | 可用于匹配已有用户 |
| 学生展示信息 | `department/phone/email` | `department`存在，`phone`80%，`email`未验证 | 可补充，但需空值策略 |
| 学生专业年级 | `major/grade` | 未见实际字段 | 不能由XG用户API满足 |
| 申请资格 | `is_graduating/graduation_year` | 未见实际字段 | P0缺口 |
| 审批路由 | `class_id` + `ClassMapping` | 未见稳定班级ID或映射关系 | P0缺口 |
| 辅导员数据 | `employee_id/name/department/is_active` | 用户API可能有基础字段，但未验证辅导员样本和值域 | 不能作为辅导员主数据 |
| 班级-辅导员映射 | `class_id/counselor_employee_id` | 未覆盖 | P0缺口 |
| 宿舍清退 | `checkout_status/checkout_date/source_updated_at` | 当前XG用户API未覆盖 | 需独立宿舍API或人工凭证流程 |
| 账号状态 | `active` | `status` 100%，示例规则为1=>True | 可作为补充字段，但需枚举确认 |

从“学生CSV必填字段”角度看，XG实际样本只稳定覆盖 `student_id/name/department` 中的基础身份展示字段；`major/class_id/grade/graduation_year/is_graduating` 未覆盖。因此它不具备创建毕业生账号主数据的完整性。

## 4. 关键缺失字段影响

### P0：`class_id`缺失

**影响：** 无法自动分配辅导员审批人。系统依赖 `class_id -> ClassMapping -> counselor`，缺失或错误会导致学生无法提交、提交后无人审批，或被错误辅导员看到。

**建议：** `class_id`继续由CSV/手工来源维护。禁止用院系、专业、班级名称临时拼接为 `class_id`，除非XG提供唯一、稳定、跨学期不复用的班级编码并完成映射验证。

### P0：`is_graduating`缺失

**影响：** 无法判断学生是否属于本批次离校申请对象。XG API总量为32,039条，明显不是“当届毕业生约1000人”的目标集合；如果直接按全量同步，会扩大账号范围和申请入口。

**建议：** 继续由CSV导入本批次毕业生名单；API不得自行创建申请资格。

### P0：`graduation_year`缺失

**影响：** 无法稳定归档毕业批次，也无法区分往届、当届、下一届学生。后续统计、审核、批次关闭都会失去依据。

**建议：** 继续由CSV维护；只有XG提供可信毕业年份或可验证毕业批次字段后，才允许进入API主导模式。

### P0：班级-辅导员映射缺失

**影响：** 即使XG可识别学生，也无法生成 `class_id -> counselor_employee_id` 映射。审批链路首个关键分派点不可落地。

**建议：** 班级映射CSV保持主数据源；后续可向XG或教务/人事系统申请独立班级与辅导员关系接口。

### P1：宿舍清退状态不在XG用户API中

**影响：** XG用户API不能替代宿舍清退实时API。提交申请前的阻断逻辑仍依赖宿舍系统接口或降级上传证明。

**建议：** 将宿舍清退集成作为独立外部数据源处理，不纳入XG用户同步完成标准。

## 5. 数据质量评估

| 维度 | 评价 | 依据 | 风险 |
|---|---|---|---|
| 身份基础字段完整性 | 高 | `number/name/status` 20/20有效 | 样本量仅20，需要扩大验证 |
| 手机号质量 | 中 | `phone` 16/20有效，4个空字符串 | 需空字符串归一化为NULL/空值 |
| 关联对象质量 | 中高 | `user_identity/department/parent_dep` 20/20，`user` 18/20 | `user`对象缺失需容错 |
| 结构一致性 | 中 | 实际样本使用 `users`数组；`per_page`可能为字符串 | 需统一“原始响应”和“客户端归一化响应”定义 |
| 业务覆盖质量 | 低 | 缺核心毕业/班级/映射字段 | 阻断API替代CSV |
| 可运营性 | 中 | 客户端暂不支持姓名/学号过滤 | 全量扫描成本高，增量/定向校验困难 |

特别注意：`backend/reports/xg_collection_test_20260603_033437.json` 中分页测试记录每页10条，但 `volume_tests.statistics` 使用 `per_page=1`，导致总页数和全量耗时估算与文档摘要不一致。该问题不影响字段覆盖结论，但会影响全量同步计划和运维估算。

## 6. 当前映射方案/实现风险

### P1：实际 `user_identity` 结构与 mapper 假设不一致

实际样本为：

```json
"user_identity": {"id": 4, "name": "学生"}
```

当前 `backend/apps/users/integrations/xg_user_mapper.py` 将 `user_identity` 直接 `str()`，仅接受 `'1'`或`'student'`，因此对实际样本会判定为 `unknown_user_identity` 并跳过。见 `backend/apps/users/integrations/xg_user_mapper.py:41`、`:59-67`。

**建议：** mapper应支持对象结构，优先按 `user_identity.name == "学生"` 判定，记录并测试 `id=4` 的含义；不能继续使用假设值 `'1'` 作为主要路径。

### P1：实际 `department` 为数组，mapper按原值写入

实际样本为：

```json
"department": [{"name": "计算机学院", "level": 2}]
```

当前 mapper 直接 `department = xg_user.get('department')` 并赋给 `result['department']`。如果写库，`department`可能变成列表而不是字符串。见 `backend/apps/users/integrations/xg_user_mapper.py:44`、`:81`。

**建议：** 明确规则为取 `department[0].name` 或按最高/最低层级选择，并添加空数组测试。

### P1：字段覆盖文档仍是“待live测试确认”状态

`docs/phase4c-xg-field-coverage.md`仍标记为基于文档样例的草案和待live测试确认，但实际采集已完成。见 `docs/phase4c-xg-field-coverage.md:5`、`:18`。

**建议：** 将该文档升级为基于2026-06-03 live样本的版本，修正 `user_identity`、`department`、`status`、响应结构和缺失字段结论。

## 7. 推荐对接策略

### 当前阶段：方案A，CSV主导 + XG API补充

**允许：**
- CSV创建和维护学生、辅导员、班级-辅导员映射主数据。
- XG API只匹配本地已存在学生。
- XG API补充更新 `phone`、`email`、`department`、`active/status`。
- 对 `phone=""`、缺失 `user`对象、空 `department`数组做容错。
- 输出 dry-run 报告：匹配数、跳过数、缺失本地用户、角色冲突、字段空值分布。

**禁止：**
- 用XG API直接创建新学生。
- 用XG API覆盖 `class_id`、`is_graduating`、`graduation_year`。
- 因XG本次未返回某用户而自动停用本地用户。
- 用部门名/班级名推导 `class_id`。
- 把XG用户API视为宿舍清退接口。

### 进入API主导模式的门槛

只有同时满足以下条件，才建议从方案A切换到“API主导 + CSV补充”：

1. XG或其他权威系统提供稳定唯一的 `class_id`，且能与系统 `ClassMapping`逐项对齐。
2. 提供 `is_graduating`和`graduation_year`，或提供等价、可审计的毕业批次字段。
3. 提供辅导员 `employee_id`及班级-辅导员关系，且能覆盖所有目标毕业班。
4. 支持按学号、身份、部门、毕业批次等过滤，或提供可靠增量同步字段。
5. 全量采集/分页/重试/限流测试稳定，且报告口径统一。
6. 至少完成一轮目标毕业生名单与CSV的差异对账，并由业务方确认差异处理规则。

## 8. 问题清单

| 优先级 | 问题 | 影响 | 建议 |
|---|---|---|---|
| P0 | 缺 `class_id` | 无法自动分配辅导员 | CSV继续主导；禁止推导 |
| P0 | 缺 `is_graduating` | 无法判定申请资格 | CSV维护毕业生名单 |
| P0 | 缺 `graduation_year` | 无法按毕业批次归档 | CSV维护毕业年份 |
| P0 | 缺班级-辅导员映射 | 审批链路无法生成 | 继续导入ClassMapping |
| P1 | mapper不支持实际 `user_identity`对象 | 实际学生可能被全部跳过 | 支持 `{id,name}`结构和中文“学生” |
| P1 | mapper不支持 `department`数组 | 可能写入错误类型 | 映射为 `department[0].name` |
| P1 | 过滤能力缺失 | 全量扫描成本高，不能定向校验 | 扩展客户端过滤或确认API限制 |
| P1 | 采集报告口径不一致 | 全量同步耗时估算不可靠 | 统一 page/pageNum/per_page 含义 |
| P2 | `phone` 20%空字符串 | 联系信息不完整 | 空字符串归一化，避免覆盖已有有效值 |
| P2 | `user`对象10%缺失 | 账号关联字段不可依赖 | mapper对关联对象缺失容错 |
| P2 | 实际样本文档仍有占位符 | 后续实现易误读 | 补全身份/部门/user特殊案例 |

## 9. 最终建议

短期按当前方案继续推进，但先修 mapper 与实际样本结构：

1. 更新 `map_xg_user_to_internal()`：支持 `user_identity.name == "学生"`、`user_identity.id == 4`、`department`数组、`phone=""`归一化、`status`映射。
2. 增加基于 `docs/XG-API-ACTUAL-DATA-SAMPLES.md` 的真实结构单元测试。
3. 更新 `docs/phase4c-xg-field-coverage.md`，从“待live确认”改为“基于2026-06-03 live样本”，明确不可替代CSV。
4. 同步命令保持 `dry-run`优先，apply模式只更新已存在学生的补充字段。
5. 向XG/教务/人事/宿舍系统分别确认缺失接口：毕业批次、班级编码、班级辅导员关系、宿舍清退状态。

**审查结论：通过“CSV主导 + API补充”的策略；不通过“XG API替代CSV主数据源”的策略。**
