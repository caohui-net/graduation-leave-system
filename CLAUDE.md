# 毕业生离校申请审批系统 - 项目配置

## 项目信息

**项目名称：** 毕业生离校申请审批系统  
**技术栈：** Python Flask + MySQL + 微信小程序  
**文档目录：** `docs/`  
**讨论记录：** `docs/discussions/codex-review-2026-05-27/`

---

## Claude-Codex协作机制

**协作协议：** `.omc/collaboration/protocol.md`

**强制规则：** When participating in Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` for task execution, artifact generation, and state management.

---

## Codex审查流程（强制要求）

**流程文档：** `docs/codex-review-protocol.md`

**强制规则：** Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.

### 核心要求

1. **统一调用方式**
   - 使用 `/oh-my-claudecode:ask codex` 进行所有审查
   - 不直接调用 `codex` CLI命令

2. **结构化审查请求**
   - 创建审查请求文档（XX-[主题]-review-request.md）
   - 明确审查范围、要点、期望输出

3. **批判性分析**
   - 不盲目接受Codex建议
   - 在Claude响应文档中说明理由
   - 深入分析根本原因和影响范围

4. **完整流程（7步）**
   - 第1步：创建审查请求文档
   - 第2步：调用 `/oh-my-claudecode:ask codex`
   - 第3步：保存Codex审查结果
   - 第4步：Claude响应Codex审查
   - 第5步：执行修复
   - 第6步：创建共识文档
   - 第7步：归档到项目文档

5. **文档一致性**
   - 修复后验证所有相关文档
   - 确保字段命名、类型、必填性统一
   - 更新PROJECT-SUMMARY.md和session-context.json

---

## 文档审查触发条件

当满足以下任一条件时，必须使用Codex审查流程：

- 创建或修改技术设计文档
- 数据库模型变更
- API接口设计
- 数据对接方案
- 系统架构调整
- 关键业务流程变更

---

## 项目约定

### 文档编号规则

**讨论文档：** `docs/discussions/codex-review-YYYY-MM-DD/XX-[主题].md`

**审查文档编号：**
- XX号：审查请求
- XX+1号：Codex响应
- XX+2号：Claude响应
- XX+3号：最终共识

### 提交规范

**Commit格式：**
```
<type>: <description>

<body>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**Type类型：**
- `docs`: 文档更新
- `feat`: 新功能
- `fix`: 修复
- `refactor`: 重构
- `chore`: 杂项

---

## 变更管理（强制）

**每次修改后必须：**
1. 检查所有关联文件是否需要同步修改
2. 用Read工具验证修改内容正确
3. 更新PROJECT-SUMMARY.md或CHANGELOG.md
4. 更新.omc/session-context.json
5. git add + commit + push（一次性包含所有变更）

---

## 参考文档

- **系统设计：** `docs/design/2026-05-27-system-design.md`
- **数据对接：** `docs/数据对接说明文档.md`
- **用户文档：** `docs/用户设计说明书.md`
- **审查流程：** `docs/codex-review-protocol.md`
- **项目总结：** `docs/PROJECT-SUMMARY.md`
