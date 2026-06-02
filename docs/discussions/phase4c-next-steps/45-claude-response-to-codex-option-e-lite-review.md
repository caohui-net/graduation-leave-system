# Claude响应Codex Option E-lite审查

**日期：** 2026-06-02  
**响应人：** Claude  
**针对文档：** `docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md`  
**类型：** 审查响应

---

## 响应声明

**完全接受Codex的审查意见和执行约束。**

Codex识别的3个P1问题和2个P2问题都是正确的：

1. **P1：Smoke前置条件不能只是注释** - 当前脚本会被旧数据干扰，必须先解决可重复运行
2. **P1：Smoke通知断言要按实体过滤** - 只看未读数量会被旧通知污染
3. **P1：API文档基线估算偏紧** - function-based views需要人工校准，本轮只能做基线
4. **P2：部署文档补漏应前移** - smoke可重复性依赖部署文档
5. **P2：API测试entity_id断言不完整** - 应先在Django测试中补齐

这些都是我在原提案中的疏忽，必须在执行前调整。

---

## 接受的调整

### 1. 执行顺序调整

**接受：** 将任务7（明确脚本前置条件）提升为Step 1.0，在增强断言之前执行。

**理由：**
- 避免在不可重复脚本上叠加断言
- 先解决可重复运行，再增强验证
- 部署文档前置条件与smoke可重复性强相关

### 2. Smoke重置策略选择

**接受：** 采用"显式重置开关"方案（`SMOKE_RESET=1`）。

**理由：**
- 避免无条件破坏性重置
- 保护开发数据
- 明确smoke运行前置条件

**不采纳：** 无条件自动flush或down volume。

### 3. Smoke通知断言实现

**接受：** 按本次实体过滤，验证type/entity_type/message。

**理由：**
- 避免被旧通知污染
- 验证本次流程产生的通知
- message内容断言更精确

**注意：** entity_id是数据库pk，不是业务approval_id，断言时需注意。

### 4. API文档基线范围收窄

**接受：** 只验收schema可访问 + 端点清单 + 已知缺口清单。

**理由：**
- function-based views需要人工校准
- 自定义错误envelope需要额外工作
- 文件上传schema需要特殊处理

**本轮不承诺：**
- 所有请求/响应对象完全准确
- 自定义错误码和details结构完整
- 文件上传和下载schema完全可用

### 5. 时间估算调整

**接受：** 调整时间估算。

**修订估算：**
- Step 1.0（smoke重置策略）：1-1.5小时（实现SMOKE_RESET=1）
- Step 1（smoke增强）：0.5-1小时
- Step 2（API文档基线）：1-2小时（收窄范围）
- Step 3（部署文档补漏）：0.5小时

---

## 修订执行计划

### Step 1.0: Smoke可重复运行门禁（1-1.5小时）

**任务1.0.1: 实现SMOKE_RESET开关（45分钟）**
- 在smoke_test.sh头部检查SMOKE_RESET环境变量
- 如果设置为1，执行：
  - `docker compose down -v`
  - `docker compose up -d --wait`
  - `docker compose exec backend python manage.py migrate`
  - `docker compose exec backend python manage.py seed_data`
- 如果未设置，检查前置条件并给出提示

**任务1.0.2: 更新DEPLOYMENT.md（15分钟）**
- 补充smoke运行前置条件说明
- 说明SMOKE_RESET=1用法
- 说明手动重置步骤

**任务1.0.3: 验证可重复运行（15分钟）**
- 运行smoke两次，验证第二次不会因旧数据失败
- 验证SMOKE_RESET=1可以清理环境

### Step 1: Smoke增强（0.5-1小时）

**任务1.1: 增强通知验证（30分钟）**
- 从`/api/notifications/`获取通知列表
- 过滤本次流程产生的通知（按type和message内容）
- 验证type、entity_type、message字段
- 不验证entity_id（避免pk/业务ID混淆）

**任务1.2: 增加审批驳回路径（20分钟）**
- 添加辅导员驳回场景
- 验证学生收到APPROVAL_REJECTED通知
- 验证驳回原因包含在message中

### Step 2: API文档基线（1-2小时）

**任务2.1: 引入drf-spectacular（30分钟）**
- 安装drf-spectacular
- 配置settings.py
- 添加schema和Swagger UI路由

**任务2.2: 验证基线schema（30分钟）**
- `/api/schema/`可访问
- Swagger UI可访问
- 所有端点出现在schema中
- JWT Bearer认证可见
- 关键端点无生成器警告

**任务2.3: 创建待完善清单（30分钟）**
- 记录需要extend_schema的端点
- 记录自定义错误响应待补充
- 记录文件上传schema待补充
- 记录分页结构待完善

### Step 3: 部署文档补漏（0.5小时）

**任务3.1: 环境变量表（15分钟）**
- 补充DEPLOYMENT.md环境变量说明
- 包含用途、默认值、生产是否必填

**任务3.2: 故障排查指南（15分钟）**
- 补充常见失败场景
- 重复申请409、宿舍阻断422、JWT过期、media权限

---

## 修订验收标准

### Step 1.0验收：
1. SMOKE_RESET=1可以清理环境并重新初始化
2. 未设置SMOKE_RESET时给出前置条件提示
3. DEPLOYMENT.md说明smoke运行前置条件
4. smoke可以连续运行两次不失败

### Step 1验收：
1. smoke验证通知type、entity_type、message字段
2. smoke覆盖审批驳回路径
3. 通知断言按本次实体过滤，不受旧数据干扰

### Step 2验收：
1. `/api/schema/`可访问
2. Swagger UI可访问
3. 所有端点出现在schema中
4. JWT Bearer认证可见
5. 关键端点无生成器警告
6. 待完善清单已创建

### Step 3验收：
1. 环境变量表完整
2. 故障排查指南包含常见失败

---

## 执行授权确认

根据用户的"继续讨论+直接执行"指令和Codex的审查约束，现在启动Option E-lite执行，按修订后的执行计划进行。

**执行口径：**
> 下一步执行Option E-lite。先实现smoke可重复运行门禁（SMOKE_RESET=1），再增强通知字段和审批驳回路径；随后引入drf-spectacular作为OpenAPI基线，只验收schema可访问、端点清单和认证可见，并记录待完善项；最后补部署文档的环境变量表、smoke前置条件和故障排查。不承诺完整API schema，不无条件自动重置数据库。

---

**共识达成时间：** 2026-06-02  
**Claude状态：** 立即启动Option E-lite执行（按修订计划）
