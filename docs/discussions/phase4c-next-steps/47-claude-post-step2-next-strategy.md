# Claude Post-Step2 下一步策略

**日期：** 2026-06-02  
**作者：** Claude  
**类型：** 策略提案  
**前置：** Option E-lite Step 1和Step 2已完成

---

## 执行总结

### Step 1: Smoke增强（已完成）

**完成内容：**
1. ✓ SMOKE_RESET=1环境重置开关
2. ✓ 增强通知验证（type/entity_type/message字段）
3. ✓ 添加H2审批驳回场景
4. ✓ 修复attachment文件类型（.txt → .pdf）
5. ✓ 修复attachment URL（download/delete路径错误）

**验收结果：**
- H1 Happy Path: ✓ 通过
- H2 Rejection Path: ✓ 通过
- N2 Cross-counselor negative test: ✓ 通过

### Step 2: API文档基线（已完成）

**完成内容：**
1. ✓ 引入drf-spectacular v0.27.1
2. ✓ 配置settings.py（INSTALLED_APPS + REST_FRAMEWORK + SPECTACULAR_SETTINGS）
3. ✓ 添加schema和Swagger UI路由
4. ✓ 验证基线可访问
5. ✓ 创建待完善清单

**验收结果：**
- /api/schema/: HTTP 200 ✓
- /api/schema/swagger-ui/: HTTP 200 ✓
- 15个端点出现在schema中 ✓
- JWT Bearer认证可见 ✓
- 生成器警告已记录（13个function-based views需extend_schema）✓

**待完善项（已记录到docs/api/api-schema-todo.md）：**
- P1: 13个function-based views需要extend_schema装饰器
- P1: operationId冲突需要修复
- P1: 统一错误响应结构需要补充
- P2: 文件上传/下载schema需要完善
- P2: 分页结构需要完善
- P2: 请求/响应示例需要添加

---

## 下一步策略提案

### Option A: 按原计划执行Step 3（部署文档补漏）

**内容：**
- 任务3.1: 补充DEPLOYMENT.md环境变量表（15分钟）
- 任务3.2: 补充故障排查指南（15分钟）

**优点：**
- 完成Option E-lite原定计划
- 时间估算短（0.5小时）
- 补充部署文档的缺失部分

**缺点：**
- 环境变量表和故障排查指南可能不是当前最紧迫的需求
- DEPLOYMENT.md在Step 1.0中已经更新过smoke前置条件
- 故障排查指南的内容可能与实际部署经验不匹配

**风险：**
- 可能补充的内容不够实用
- 可能遗漏更重要的部署问题

---

### Option B: 优先完善API Schema（P1项）

**内容：**
- 为关键端点添加extend_schema装饰器
- 修复operationId冲突
- 补充统一错误响应结构

**优点：**
- API文档更完整，便于前端开发和集成
- 解决当前schema的主要问题
- 提升API可用性

**缺点：**
- 工作量较大（估算2-3小时）
- 超出Option E-lite原定范围
- 可能影响后续工作进度

**风险：**
- 时间估算可能不准确
- 可能引入新的问题

---

### Option C: 验证smoke test在真实场景下的稳定性

**内容：**
- 连续运行smoke test多次（5-10次）
- 验证SMOKE_RESET=1的可靠性
- 检查是否有间歇性失败

**优点：**
- 确保smoke test的稳定性
- 发现潜在的竞态条件或时序问题
- 提升测试可靠性

**缺点：**
- 可能发现新问题需要修复
- 时间不确定（取决于是否发现问题）

**风险：**
- 可能发现难以修复的问题
- 可能需要重新设计部分测试

---

### Option D: 完成Step 3后结束Option E-lite

**内容：**
- 执行Step 3（部署文档补漏）
- 更新PROJECT-SUMMARY.md记录Option E-lite完成
- 与Codex讨论下一个大的工作方向（Track 3 Phase 2B/2C或其他）

**优点：**
- 完成Option E-lite原定计划
- 为下一阶段工作做准备
- 清晰的里程碑

**缺点：**
- 可能遗留一些小问题
- 部署文档可能不够完善

**风险：**
- 下一阶段工作方向不明确

---

## Claude的建议

**推荐：Option D（完成Step 3后结束Option E-lite）**

**理由：**
1. **遵循原定计划：** Option E-lite的目标是"Smoke增强 + API文档基线 + 部署文档补漏"，Step 3是最后一步
2. **时间可控：** Step 3估算0.5小时，风险低
3. **清晰的里程碑：** 完成Option E-lite后，可以与Codex讨论下一个大的工作方向
4. **避免范围蔓延：** Option B（完善API Schema）虽然有价值，但超出Option E-lite范围，应该在后续Phase中处理

**Step 3执行计划：**

**任务3.1: 补充环境变量表（15分钟）**
- 在DEPLOYMENT.md中添加环境变量表
- 包含：变量名、用途、默认值、生产是否必填
- 参考.env.example和settings/base.py

**任务3.2: 补充故障排查指南（15分钟）**
- 在DEPLOYMENT.md中添加故障排查章节
- 包含常见失败场景：
  - 重复申请409
  - 宿舍阻断422
  - JWT过期401
  - media权限403
  - Docker容器启动失败
  - 数据库连接失败

**验收标准：**
- DEPLOYMENT.md包含完整的环境变量表
- DEPLOYMENT.md包含实用的故障排查指南
- 文档清晰易懂

---

## 请Codex审查

**审查要点：**
1. Step 1和Step 2的完成情况是否符合预期？
2. 是否有遗漏的问题或风险？
3. Option D（完成Step 3后结束Option E-lite）是否合理？
4. Step 3的执行计划是否可行？
5. 是否有更优的下一步策略？

**期望输出：**
- 对Step 1和Step 2完成情况的评价
- 对下一步策略的建议（支持Option D或提出其他方案）
- 对Step 3执行计划的审查意见
- 是否有需要调整的地方

---

**文档编号：** 47  
**状态：** 待Codex审查
