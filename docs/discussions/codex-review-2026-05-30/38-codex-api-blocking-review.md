# Codex审查：API阻塞问题解决方案

**文档编号：** 38  
**审查日期：** 2026-05-30  
**审查人：** Codex (GPT-5.5)  
**审查对象：** 37-api-blocking-solution-review-request.md

---

## 审查结论

**评分：** 7/10

**总体评价：** Mock + 接口抽象方向是合理的，但当前方案不能按原文直接通过。

**核心问题：** 方案把"用户主数据 API 化"当成默认终局，偏离了此前已达成的首版共识：学生、辅导员、班级映射应优先走 CSV/Excel 导入，宿舍清退才是实时 API。

**共识依据：**
- [31-data-source-requirements-consensus-v2.md](../codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md) 第35行
- [数据对接说明文档.md](../../数据对接说明文档.md) 第24行

---

## P0问题（必须修复）

### P0-1：RealUserDataProvider不应成为运行时依赖

**问题描述：**

`RealUserDataProvider` 不应成为认证、审批、班级映射的运行时依赖。用户、辅导员、班级映射是本系统的基础主数据，影响登录、权限、审批人分配和历史追溯。

**应该的做法：**

应落入本地数据库，通过 CSV/API Provider 输入到 staging，再校验、upsert、软停用。此前设计已经定义了 staging + upsert + 软停用、导入审计和校验报告：[31-data-source-requirements-consensus-v2.md](../codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md) 第282行。

**风险：**

如果直接在业务中查询 Provider，会引入：
- 外部 API 可用性风险
- 分页问题
- 延迟问题
- 字段缺失
- 历史变更不可追溯

**修复建议：**

1. 用户主数据（学生、辅导员、班级映射）通过CSV导入到本地数据库
2. Provider只用于宿舍清退状态的实时查询
3. 保留Provider抽象层，但明确其用途：数据导入（非运行时查询）

---

### P0-2：+3天生产就绪评估过于乐观

**问题描述：**

3天只适用于"API 契约已冻结、测试环境可用、认证已跑通、字段完全覆盖、只写一个薄适配器"的场景。

**当前现状：**

文档明确缺少：
- 完整 API 文档
- 认证信息
- 字段映射
- 交付时间

参考：[37-api-blocking-solution-review-request.md](./37-api-blocking-solution-review-request.md) 第25行

**修复建议：**

真实集成应预留：
- **宿舍清退API：** 1-2周
- **用户主数据API（如果坚持）：** 2-4周（牵涉数据模型、导入/同步策略、账号状态、审批人映射和验收演练）

**推荐工期：**

"10周 + 3天" → **10周演示版 + 1-2周生产集成缓冲**

---

## P1问题（重要改进）

### P1-1：接口设计粒度不够

**问题描述：**

`get_students(filters) -> List[Student]`、`get_counselors()`、`get_class_mapping() -> Dict[str, str]` 太粗，缺少：
- 分页
- 增量同步
- 源数据更新时间
- 数据质量报告
- 批次标识
- 字段映射版本
- 错误分类
- 健康检查

**修复建议：**

拆分为：
- `StudentSourceProvider` / `CounselorSourceProvider` / `ClassMappingSourceProvider`
- `DormCheckoutProvider`
- `ProviderHealthCheck`
- `ImportAdapter` 或 `SyncService`

**返回值设计：**

返回值应是 DTO，不是 Django ORM Model。
- Provider 负责：取数和标准化
- Import/Sync 层负责：校验、落库、审计、软停用

---

### P1-2：USE_MOCK_DATA太粗且有生产风险

**问题描述：**

当前设计用一个开关同时切用户数据和宿舍清退：[37-api-blocking-solution-review-request.md](./37-api-blocking-solution-review-request.md) 第160行。

**修复建议：**

改为细粒度配置：
```python
USER_DATA_SOURCE = 'seed' | 'csv' | 'api'
DORM_CHECKOUT_SOURCE = 'mock' | 'api' | 'csv'
WECHAT_PROVIDER = 'mock' | 'real'
```

**安全措施：**
- 生产环境禁止 `mock`
- 启动时 system check 直接失败
- 支持"用户主数据 CSV + 宿舍清退 API"的混合模式

---

### P1-3：Mock数据真实性不足

**问题描述：**

100学生、10辅导员可以支撑演示，但不足以覆盖风险。

**必须包含边界样本：**
- 无班级映射
- 辅导员停用
- 重复 class_id
- 多辅导员
- 延期毕业/非毕业生
- 姓名不一致
- 宿舍状态：`completed/pending/not_started/unknown`
- API错误：404/401/429/500
- 超时
- 数据过期

**参考：**

宿舍清退枚举和降级规则已有定义：[数据对接说明文档.md](../../数据对接说明文档.md) 第306行

---

## 工期评估

### 当前方案评估

10周做"Mock/Seed 数据可演示版本"基本可行，但 **Week 7 才做接口抽象偏晚**。

**问题：**

Provider 契约、DTO、种子数据、导入接口应在 Week 1-2 完成，否则认证、审批、前端都会先绑定临时模型，后续返工。

### 调整后的工期

**建议调整为：**

| 周次 | 任务 | 交付物 |
|------|------|--------|
| Week 1 | 数据契约、DTO、Provider接口、种子数据、导入模型 | 数据契约文档、DTO定义、Provider接口 |
| Week 2-3 | CSV/staging/upsert/审计和核心账号数据 | CSV导入功能、staging表、审计日志 |
| Week 3-6 | 申请、审批、附件、通知 | 核心业务模块 |
| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
| Week 8-9 | 前端 | React Native、微信小程序 |
| Week 10 | 联调、演示、验收清单 | 演示版本 |

**API到位后：**
- 宿舍清退 API：1周
- 用户主数据 API 替换 CSV：另计 2-4周

**总工期：**

"10周 + 3天" → **10周演示版 + 1-2周生产集成缓冲**

**重要提示：**

若外部 API 字段继续缺失，首版应坚持 CSV/Excel 主数据导入，不等待 API。

---

## 架构建议

### 推荐架构：反腐层 + 本地主数据

```
┌─────────────────────────────────────────────┐
│         外部数据源（External Sources）        │
│  CSV / API / DB View / Mock                │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Provider层（Data Providers）         │
│  只负责读取外部数据并转换为标准 DTO           │
│  - StudentSourceProvider                    │
│  - CounselorSourceProvider                  │
│  - ClassMappingSourceProvider               │
│  - DormCheckoutProvider                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│    Import/Sync Service（导入/同步服务）      │
│  校验必填字段、唯一性、班级覆盖率、辅导员有效性 │
│  - Staging表                                │
│  - Upsert逻辑                               │
│  - 软停用                                   │
│  - 导入审计                                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      本地数据库（Local Database）            │
│  作为认证、权限、审批和历史记录的唯一运行时依据 │
│  - users表                                  │
│  - applications表                           │
│  - approvals表                              │
└─────────────────────────────────────────────┘
                    ↑
                    │ (运行时查询)
┌─────────────────────────────────────────────┐
│    DormCheckoutProvider（宿舍清退查询）      │
│  运行时查询，可缓存，可降级到人工证明          │
└─────────────────────────────────────────────┘
```

### 关键设计原则

1. **外部数据源：** CSV/API/DB view/Mock
2. **Provider：** 只负责读取外部数据并转换为标准 DTO
3. **Import/Sync Service：** 校验必填字段、唯一性、班级覆盖率、辅导员有效性
4. **本地数据库：** 作为认证、权限、审批和历史记录的唯一运行时依据
5. **DormCheckoutProvider：** 运行时查询，可缓存，可降级到人工证明

---

## 缓存策略

### 用户信息缓存

按现有设计 30分钟左右缓存：[2026-05-27-system-design.md](../../design/2026-05-27-system-design.md) 第2433行

### 宿舍清退状态缓存

**建议：**
- `completed`：可缓存 10-30分钟
- `pending/not_started`：缓存 1-5分钟
- `unknown/error`：只短缓存 30-60秒，避免故障恢复后仍误判
- **提交申请前必须重新校验**或记录"校验时间 + source_updated_at"

---

## 错误处理

### 错误分类

需要区分：
- 认证失败
- 字段缺失
- 学生不存在
- 限流
- 超时
- 服务不可用
- 数据不一致

### 监控指标

现有设计已有重试和降级方向：[2026-05-27-system-design.md](../../design/2026-05-27-system-design.md) 第1697行

**需要补充监控指标：**
- 成功率
- P95延迟
- 降级次数
- unknown 比例
- 认证失败次数
- 429 次数

---

## 最终建议

### 修正后的方案

**"Seed/Mock + Provider 抽象 + CSV 主数据导入 + 宿舍清退 API 适配"**

### 关键原则

1. **不要把用户主数据 API 集成放到首版关键路径**
2. **不要承诺 API 到位后三天生产就绪**
3. **真正的关键交付物：**
   - 稳定的数据契约
   - 导入校验
   - 降级流程
   - 契约测试
   - 上线验收清单

### 首版实施路径

1. **Week 1-3：** CSV导入 + 种子数据
2. **Week 3-6：** 核心业务逻辑
3. **Week 6-7：** 宿舍清退API对接
4. **Week 8-9：** 前端开发
5. **Week 10：** 联调和演示
6. **API到位后：** 1-2周生产集成

### 后续优化

如果数据变更频率高，可升级为API/DB同步。但首版应坚持CSV导入，快速上线。

---

**审查人：** Codex (GPT-5.5)  
**审查时间：** 2026-05-30  
**Token使用：** 66,035
