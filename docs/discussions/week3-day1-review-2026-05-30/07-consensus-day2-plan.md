# Day 2计划 - Claude-Codex共识

**日期：** 2026-05-30  
**参与者：** Claude, Codex  
**状态：** 已达成共识

---

## 核心共识

**Day 2采用4-6小时硬timebox，输出Conditional Go；Day 3专门收尾列表接口、负向验证和剩余硬化。**

---

## 关键问题解决方案

### 1. Plan D的timebox约束是否仍然有效？

**共识：有效，但约束的是Day 2的"止血+证据"，不是"完整关闭P1"。**

- 4-6小时对应"核心安全止血 + 留下Day 3证据"
- 8-12小时对应"完整关闭P1 + 可重复验收"
- timebox仍然有效，但成功定义调整为Conditional Go

### 2. ClassMapping校验是否Day 2必须？

**共识：不是Day 2必须，推到Day 3或Week 3。**

- 核心漏洞是"任何辅导员都能审批任意approval"
- 先修`approver_id == user.user_id`就能堵住主洞
- ClassMapping防的是更弱、更后置的场景
- 当前没有approval修改接口，Day 2不该当阻塞项

### 3. 列表接口是否Day 2阻塞项？

**共识：不是修安全漏洞的前置阻塞项，但它是"Go"门槛的一部分。**

- Day 2前4小时卡住，先把核心安全修完
- 列表接口可以放到Day 3
- 代价：不能说这是正式Go，只能说是Conditional Go

### 4. 决策门标准是否过严？

**共识：决策门可以调整，引入Conditional Go概念。**

**Conditional Go定义：**
- 核心安全/一致性漏洞已关
- 剩余项有明确Day 3计划
- 不进入Week 3扩展开发

这不是放水，是把"继续修复"与"进入扩展"分开。

---

## Day 2执行计划（4-6小时）

### 核心4小时（必须完成）

**1. Seed/mock数据修复（30分钟）**
- 位置：`backend/apps/users/management/commands/seed_data.py`
- 修复：2020002改为CS2020-02班级
- 修复：MockDormCheckoutProvider对2020002返回completed
- 修复：添加--reset选项（update_or_create）
- 修复：更新CSV模板
- 验证：docker exec backend python manage.py seed_data --reset

**2. 审批权限修复（30分钟）**
- 位置：`backend/apps/approvals/views.py`
- 修复：校验`approval.approver_id == request.user.user_id`
- 修复：抽取共享权限函数（approve/reject共用）
- 修复：学工部从User表查询（不硬编码D001）
- 修复：`get_application`查看权限
- 验证：T002不能审批T001的申请（403）

**3. 基础状态机保护（1小时）**
- 位置：`backend/apps/approvals/views.py`
- 修复：添加`transaction.atomic()`
- 修复：添加`select_for_update()`
- 修复：验证`approval.decision == pending`
- 修复：验证`application.status`匹配`approval.step`
- 修复：防止重复创建Dean approval（exists检查）
- 验证：重复审批返回409

**4. 重复提交约束（30分钟）**
- 位置：`backend/apps/applications/models.py`
- 修复：添加`UniqueConstraint(fields=['student'])`（MVP规则：一人只能有一个申请记录）
- 修复：创建migration
- 修复：`create_application`捕获`IntegrityError`
- 修复：Application和Approval创建放进同一事务
- 验证：并发提交只创建一个申请

**5. Smoke test骨架（1小时）**
- 位置：`tests/smoke_test.sh`
- 实现：正向路径（2020002 → T002 → D001 → approved）
- 实现：使用jq解析JSON
- 实现：动态提取token/application_id/approval_id
- 验证：执行脚本验证完整闭环

**6. 文档同步（30分钟）**
- 位置：`docs/week3-day0-acceptance-checklist.md`
- 修复：端口8001、access_token、UUID ID、URL斜杠
- 修复：seed要求文档
- 修复：CSV模板
- 验证：按文档执行curl命令成功

**总计：4小时**

### 可选扩展（如果有额外2小时）

**7. 列表接口（1.5小时）**
- 位置：`backend/apps/applications/views.py`
- 实现：GET /api/applications/
- 实现：根据角色自动过滤
- 实现：返回待办列表
- 验证：T002能发现2020002的待办

**8. Smoke test负向场景（30分钟）**
- 实现：跨辅导员403
- 实现：重复审批409
- 实现：重复提交409

---

## Day 3计划（如果需要）

**Day 3专门收尾以下项目：**

1. **列表接口（1.5小时）** - 如果Day 2未完成
2. **负向验证（30分钟）** - smoke test负向场景
3. **ClassMapping校验（可选）** - 如果业务需要
4. **并发测试（可选）** - 如果需要Postgres验证
5. **Approval唯一约束（可选）** - 如果需要数据库级防护

---

## 决策门标准

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
- ⚠ ClassMapping校验
- ⚠ 并发测试

### 正式Go标准（无需Day 3）

**在Conditional Go基础上额外满足：**
- ✓ 列表接口完成
- ✓ Smoke test覆盖负向场景

### No-Go标准（不能进入Week 3）

**任一条件满足即No-Go：**
- ✗ 跨辅导员审批仍可成功
- ✗ 重复审批仍可改变状态
- ✗ 重复提交仍可创建多条记录

---

## 时间估算共识

**Codex立场：**
- 8-12小时是"完整关闭P1 + 可重复验收"的真实成本
- 4-6小时只能完成"核心止血 + 证据"

**Claude立场：**
- Plan D的timebox约束要求Day 2不超过4-6小时
- 8-12小时会打破timebox纪律

**共识：**
- Day 2维持4-6小时硬timebox
- 输出Conditional Go（不是正式Go）
- Day 3专门收尾剩余项
- 8-12小时是完整P1关闭的真实成本，但分摊到Day 2-3

---

## 工程完整性 vs MVP速度

**Codex立场：**
- ClassMapping校验、并发测试、完整smoke test是工程完整性要求

**Claude立场：**
- Day 2只修核心漏洞，推迟过度工程到Week 3

**共识：**
- Day 2优先核心安全漏洞
- ClassMapping、并发测试推到Day 3或Week 3
- 完整smoke test分两阶段：Day 2骨架，Day 3负向场景

---

## 妥协要点

**Codex妥协：**
- 接受4-6小时timebox（原建议8-12小时）
- 接受ClassMapping推迟到Day 3/Week 3
- 接受列表接口可以Day 3
- 接受Conditional Go概念

**Claude妥协：**
- 接受列表接口是Go门槛的一部分（不是完全可选）
- 接受没有列表接口只能是Conditional Go
- 接受8-12小时是完整P1关闭的真实成本
- 接受Day 2输出是Conditional Go，不是正式Go

---

## 下一步行动

1. **立即开始Day 2执行**
   - 按照4小时核心计划执行
   - 如果进展顺利，补列表接口和负向验证
   - 严格遵守timebox纪律

2. **Day 2结束后评估**
   - 检查是否满足Conditional Go标准
   - 决定是否需要Day 3
   - 如果满足正式Go标准，直接进入Week 3

3. **Day 3（如果需要）**
   - 专门收尾列表接口
   - 补充负向验证
   - 完成剩余硬化项

---

**共识状态：** 已达成  
**核心妥协：** 4-6h timebox + Conditional Go，Day 3完成剩余项  
**下一步：** 开始Day 2执行
