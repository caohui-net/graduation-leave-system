# Codex Completion Boundary Analysis

**Date:** 2026-05-31 Asia/Shanghai  
**Task context:** TASK-20260530-06 / Week 3 direction after Phase 2 + Phase A  
**Role:** Critical analysis and next-step recommendation

## Executive Conclusion

“全部完成”不应定义为完整小程序功能完成，也不应定义为已经通过 WeChat DevTools 验证。合理边界是：

1. 已交付的 Phase 2 后端/契约/测试工作有可复现验证证据。
2. 小程序 skeleton 在无法打开 WeChat DevTools 的前提下完成静态与契约级验证。
3. DevTools 导入/运行被明确登记为唯一外部阻塞。
4. 随后回到 Week 3 原始主线：核心闭环补强 + v0.2 契约收敛。

因此推荐路径不是单纯路径2或路径3，而是路径5：**先用短收尾封口当前 skeleton 风险，再立刻回 Week 3 主线；禁止继续扩展未验证的小程序功能。**

## Completion Boundary

选项A“skeleton 文件创建 = 完成”过低。文件存在只能证明产物落盘，不能证明它可被后续协作可靠接手。

选项B“skeleton + 静态验证 = 完成”是当前环境下的最小合理完成定义，但必须限定为“Phase A skeleton 完成”，不能扩张成“Week 3 全部完成”。

选项C“skeleton + DevTools 验证 = 完成”是理想验收，但当前依赖外部工具，不应让整个工作流无限等待。它应作为外部阻塞项进入验收说明。

选项D“完整小程序功能 = 完成”明显越界。Week 3 共识强调可复现后端闭环、P0 修复、契约收敛，而不是在未通过 DevTools 的 skeleton 上继续堆页面。

## Recommended Path

选择路径5：

1. **短收尾，不扩展功能。**
   - 复跑后端 smoke / 单元测试 / 类型或契约检查。
   - 对小程序做静态结构检查：`app.json` 页面注册、页面文件成组存在、API client 使用 `wx.request`、mock fixture 与 TypeScript 类型/后端样例字段一致。
   - 生成一份“完成与阻塞说明”：哪些已验证、哪些只能在 DevTools 验证、如何验证。

2. **回到 Week 3 主线。**
   - 补强核心流程：提交、审批列表/详情、审批/驳回、状态机、权限负向验证。
   - 收敛 v0.2 契约：请求/响应样例、状态枚举、错误码、mock provider 边界。
   - 保留小程序 skeleton 为后续接入点，不在 DevTools 验证前继续扩展。

## Risk Analysis

路径1“停止等待 DevTools”过于保守。DevTools 验证是 UI runtime 门槛，不是后端核心闭环门槛；停止会浪费当前可推进的确定性工作。

路径2“短收尾”必要但不充分。它能把 Phase A 变成可交接状态，但不能回答 Week 3 原始目标是否完成。

路径3“回 Week 3 轨道”方向正确，但如果不先封口 skeleton，会留下一个模糊状态：产物存在、未验证、后续又被误认为可继续扩展。

路径4“继续扩展 skeleton”不建议。当前没有 WeChat DevTools 反馈，继续写页面很容易在组件语法、路由、生命周期、网络限制上返工，而且收益偏离 Week 3 共识。

## Concrete Priority

P0-A：冻结小程序范围，完成静态/契约验证和阻塞说明。

P0-B：复现后端核心 smoke，确保 Phase 2 修复不是“只在某次运行通过”。

P0-C：创建 Week 3 后续清单，优先推进核心闭环和 v0.2 契约，不再扩大 UI 面。

P1：补充 API 样例与 mock fixture 对齐检查，降低小程序后续接入成本。

P2：等 DevTools 可用后做导入、mock 模式首屏、真实 API 登录/列表验证。

## Consensus Position

在外部阻塞下，“完成”的严谨定义应分层：

- **Phase A skeleton：** 可以在静态验证 + 阻塞说明后标记为“当前环境内完成”。
- **DevTools runtime 验收：** 未完成，外部阻塞。
- **Week 3：** 未因 skeleton 完成而自动完成，应回到核心流程补强 + v0.2 契约。

最终建议：执行路径5，先做 30-90 分钟短收尾，然后转入 Week 3 原始目标。继续扩展 skeleton 应明确禁止，直到 DevTools 验证通过。
