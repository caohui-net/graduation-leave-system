# Contract Fixes - Codex Review Response

**审查日期：** 2026-05-30  
**审查人：** Codex  
**针对文档：** 47-contract-fixes-review-request.md  
**审查类型：** 契约修复验证

---

## 审查结论

**结论：尚未完全达到可执行契约标准，但已经非常接近。**

4个修复方向都正确，且主要阻塞点已经明显收敛：契约正文现在只有5个HTTP路由，列表端点已移除；503 `PROVIDER_UNAVAILABLE`样例已补；登录响应的DTO子集问题已说明；原先“申请未完成却只做查询”的降级方向已被替换。

但冻结前仍建议用半天完成3个收尾修正：

1. **P1：错误样例未覆盖Section 3定义的全部错误码。**
2. **P1：降级方案仍有一句口径冲突，且Day 3提交未完成时的措辞不够可执行。**
3. **P2：计划文档仍混用“5个HTTP路由”和“4个API端点/能力”的口径；AuthUserDTO最好正式纳入Section 1。**

完成这些收尾后，可以冻结契约并开始Week 1工作。

---

## 逐项修复验证

### 修复1：统一API端点数量

**验证结果：基本解决，但计划文档仍需术语收口。**

契约Section 4现在实际列出5个HTTP路由：

1. `POST /api/auth/login`
2. `POST /api/applications`
3. `GET /api/applications/{application_id}`
4. `POST /api/approvals/{approval_id}/approve`
5. `POST /api/approvals/{approval_id}/reject`

列表端点 `GET /api/applications` 已不在契约中。移除列表端点是合理的，因为v0.1纵向切片只需要“登录 -> 提交 -> 审批 -> 查询单个申请”，不需要审批队列或学生申请列表。

剩余问题是计划文档仍写“4个API端点可用（登录、提交、审批、查询）”。这更像4个核心能力，而不是HTTP路由。建议统一术语：

- HTTP路由：5个
- 核心能力：4个，登录、提交、审批、查询
- Day 3-4新增HTTP路由：4个，不含Day 1-2已完成的login

否则后续验收时仍可能出现“到底是4个还是5个端点”的争议。

### 修复2：添加503 PROVIDER_UNAVAILABLE样例

**验证结果：部分解决。**

契约已经新增503样例，且与宿舍清退外部服务不可用场景匹配：

- `PROVIDER_UNAVAILABLE`
- HTTP 503
- `provider: dorm_checkout`
- timeout细节

这解决了上一轮指出的503缺口。

但Section 3定义了8个错误码，而Section 6.2当前只提供了4类错误样例：401、403、422、503。缺少：

- `VALIDATION_ERROR` 400
- `NOT_FOUND` 404
- `CONFLICT` 409
- `INTERNAL_ERROR` 500

如果v0.1目标是“前端可用mock跑通并处理错误态”，错误样例应至少覆盖Section 3列出的全部错误码。否则前端mock、契约测试和后端异常处理仍会自行发挥。

### 修复3：澄清登录响应DTO

**验证结果：说明清晰，但建议正式定义AuthUserDTO。**

Section 4.1说明 `user` 是 `AuthUserDTO`，是 `UserDTO` 的子集，只包含 `user_id/name/role/class_id`。这解决了“登录响应到底是不是完整UserDTO”的歧义。

仍建议在Section 1加入正式定义：

```python
@dataclass
class AuthUserDTO:
    """登录响应中的用户摘要"""
    user_id: str
    name: str
    role: UserRole
    class_id: Optional[str] = None
```

原因是契约已经命名了 `AuthUserDTO`，但核心DTO章节没有定义它。对后端实现、前端类型生成、契约测试来说，正式定义比正文说明更可靠。

### 修复4：移除矛盾的降级条件

**验证结果：方向正确，但风险表还需要改一句。**

计划已经移除了“申请提交API未完成 -> 只做查询API”的矛盾逻辑，新的方向是优先保留“提交 -> 辅导员审批 -> 查询”最短闭环。这符合纵向切片目标。

但风险表仍写：

> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批

这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：

> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。

这样降级条件才真正可执行：先保住最短闭环，不在同一天又承诺补回被砍范围。

---

## 剩余问题与修复建议

### P1：错误样例覆盖不完整

**位置：** `docs/contracts/contract-v0.1.md` Section 3和Section 6.2

**问题：** Section 3定义8个错误码，但错误Mock只覆盖4个。

**影响：** 前端mock、后端异常格式、契约测试无法完整对齐。

**修复建议：** 在Section 6.2补齐400、404、409、500样例。每个样例都保持统一结构：

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数校验失败",
    "details": {
      "field": "leave_date",
      "reason": "must be YYYY-MM-DD"
    }
  }
}
```

### P1：降级条件仍有口径冲突

**位置：** `docs/plans/week-0-1-execution-plan.md` 风险2

**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。

**影响：** Day 3风险触发后团队不知道是保闭环，还是继续追两级审批。

**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。

### P2：API端点术语仍不够统一

**位置：** `docs/plans/week-0-1-execution-plan.md` Day 3-4交付物、Week 1验收

**问题：** 计划中“4个API端点”实际指4个核心能力或Day 3-4新增HTTP路由，不等于契约的5个HTTP路由。

**影响：** 不一定阻塞实现，但会继续制造验收口径争议。

**修复建议：** 改为：

- Week 0：5个HTTP路由样例
- Day 3-4交付物：4个业务HTTP路由可用，不含登录
- Week 1验收：5个HTTP路由可用，覆盖4个核心能力

### P2：AuthUserDTO应正式定义

**位置：** `docs/contracts/contract-v0.1.md` Section 1

**问题：** Section 4.1引用了 `AuthUserDTO`，但Section 1没有该DTO定义。

**影响：** 对人工阅读影响小，对类型生成和契约测试有轻微歧义。

**修复建议：** 在UserDTO之后添加 `AuthUserDTO`，并调整后续编号。

---

## 可执行性判断

**当前状态：未完全达到可执行契约标准。**

不是因为方向错，而是因为仍有两个会影响执行验收的P1口径缺口：错误样例未全覆盖，降级风险表仍有冲突措辞。它们都属于半天内可以修完的收尾问题。

**修完上述P1后：可以冻结contract-v0.1.md，并开始Week 1 Day 1工作。**

如果团队已经要启动Week 1，也可以先启动不受这些问题影响的Day 1-2工作：Django骨架、基础模型、seed、登录认证。但不建议在P1修完前把契约标记为Final并全面进入Day 3-4业务API实现。

---

## 下一步建议

1. 立即补齐4个缺失错误样例：400、404、409、500。
2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
3. 将计划中的“4个API端点”改成“4个核心能力”或“4个业务HTTP路由”，避免和5个HTTP路由冲突。
4. 在Section 1补 `AuthUserDTO` 正式定义。
5. 完成后可直接冻结v0.1，不需要再开一轮长审查；只需做一次差异核对。

