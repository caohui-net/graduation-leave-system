# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-01T01:42:06.940Z

## Original task

审查student-application页面实现方案

**背景：**
- API集中化已完成（createDefaultApiClient工厂函数）
- 需要实现学生申请页面
- 表单字段已确认：reason + leave_date（按API契约v0.2）

**实现方案草案：**

**1. 页面文件结构**
```
miniprogram/pages/student-application/
├── student-application.ts    (页面逻辑)
├── student-application.wxml  (页面结构)
├── student-application.wxss  (页面样式)
└── student-application.json  (页面配置)
```

**2. 表单设计（student-application.wxml）**
```xml
<view class="container">
  <view class="form">
    <view class="field">
      <text class="label">离校原因</text>
      <textarea placeholder="请输入离校原因" value="{{reason}}" bindinput="onReasonInput" />
    </view>
    
    <view class="field">
      <text class="label">离校日期</text>
      <picker mode="date" value="{{leaveDate}}" bindchange="onDateChange">
        <view class="picker">{{leaveDate || '请选择日期'}}</view>
      </picker>
    </view>
    
    <button bindtap="onSubmit" disabled="{{loading}}">
      {{loading ? '提交中...' : '提交申请'}}
    </button>
    
    <view class="error" wx:if="{{error}}">{{error}}</view>
  </view>
</view>
```

**3. 页面逻辑（student-application.ts）**
- 遵循login.ts模式
- 使用createDefaultApiClient()
- 表单验证：reason非空，leaveDate非空
- 调用apiClient.createApplication({reason, leave_date})
- 成功：显示toast + 跳转（跳转到哪里？）
- 错误处理：DORM_BLOCKED(422), CONFLICT(409), VALIDATION_ERROR(400)

**4. 样式（student-application.wxss）**
- 复用login.wxss的container/form/field样式
- 添加textarea特定样式

**关键问题需要你审查：**

1. **提交成功后跳转目标？**
   - 选项A：跳转到申请详情页（需要application_id）
   - 选项B：跳转到学生申请列表页（Phase 4B不包含）
   - 选项C：显示成功toast后停留在当前页（清空表单）
   - 选项D：返回上一页（但学生登录后直接到这里，没有上一页）
   
   **我倾向选项C**：成功后清空表单，允许学生查看刚提交的内容或继续提交（虽然API会409）

2. **错误处理优先级？**
   - DORM_BLOCKED(422)：宿舍清退未完成 - 显示blocking_reason
   - CONFLICT(409)：已有待审批/已通过申请 - 显示existing_application_id
   - VALIDATION_ERROR(400)：字段验证失败 - 显示details
   - 403/401：权限/认证错误 - 已由ApiClient处理
   
   **是否需要针对每种错误定制UI？** 还是统一显示error.message？

3. **表单验证时机？**
   - 选项A：提交时验证（简单）
   - 选项B：实时验证（输入时显示错误）
   - 选项C：失焦验证（离开字段时验证）
   
   **我倾向选项A**：提交时验证，保持简单

4. **日期选择器默认值？**
   - 选项A：空（用户必须选择）
   - 选项B：今天
   - 选项C：明天
   - 选项D：一周后
   
   **我倾向选项A**：空，强制用户明确选择

5. **是否需要loading状态？**
   - 提交按钮disabled + 文字变化
   - 是否需要全屏loading遮罩？
   
   **我倾向按钮disabled即可**，不需要全屏遮罩

**请你批判性审查：**
1. 实现方案是否遗漏关键点？
2. 5个关键问题的答案是否合理？
3. 是否有更优的UX设计？
4. 错误处理是否充分？
5. 是否需要添加其他功能（如草稿保存）？

要求：批判性思考，指出潜在问题和改进建议。

## Final prompt

审查student-application页面实现方案

**背景：**
- API集中化已完成（createDefaultApiClient工厂函数）
- 需要实现学生申请页面
- 表单字段已确认：reason + leave_date（按API契约v0.2）

**实现方案草案：**

**1. 页面文件结构**
```
miniprogram/pages/student-application/
├── student-application.ts    (页面逻辑)
├── student-application.wxml  (页面结构)
├── student-application.wxss  (页面样式)
└── student-application.json  (页面配置)
```

**2. 表单设计（student-application.wxml）**
```xml
<view class="container">
  <view class="form">
    <view class="field">
      <text class="label">离校原因</text>
      <textarea placeholder="请输入离校原因" value="{{reason}}" bindinput="onReasonInput" />
    </view>
    
    <view class="field">
      <text class="label">离校日期</text>
      <picker mode="date" value="{{leaveDate}}" bindchange="onDateChange">
        <view class="picker">{{leaveDate || '请选择日期'}}</view>
      </picker>
    </view>
    
    <button bindtap="onSubmit" disabled="{{loading}}">
      {{loading ? '提交中...' : '提交申请'}}
    </button>
    
    <view class="error" wx:if="{{error}}">{{error}}</view>
  </view>
</view>
```

**3. 页面逻辑（student-application.ts）**
- 遵循login.ts模式
- 使用createDefaultApiClient()
- 表单验证：reason非空，leaveDate非空
- 调用apiClient.createApplication({reason, leave_date})
- 成功：显示toast + 跳转（跳转到哪里？）
- 错误处理：DORM_BLOCKED(422), CONFLICT(409), VALIDATION_ERROR(400)

**4. 样式（student-application.wxss）**
- 复用login.wxss的container/form/field样式
- 添加textarea特定样式

**关键问题需要你审查：**

1. **提交成功后跳转目标？**
   - 选项A：跳转到申请详情页（需要application_id）
   - 选项B：跳转到学生申请列表页（Phase 4B不包含）
   - 选项C：显示成功toast后停留在当前页（清空表单）
   - 选项D：返回上一页（但学生登录后直接到这里，没有上一页）
   
   **我倾向选项C**：成功后清空表单，允许学生查看刚提交的内容或继续提交（虽然API会409）

2. **错误处理优先级？**
   - DORM_BLOCKED(422)：宿舍清退未完成 - 显示blocking_reason
   - CONFLICT(409)：已有待审批/已通过申请 - 显示existing_application_id
   - VALIDATION_ERROR(400)：字段验证失败 - 显示details
   - 403/401：权限/认证错误 - 已由ApiClient处理
   
   **是否需要针对每种错误定制UI？** 还是统一显示error.message？

3. **表单验证时机？**
   - 选项A：提交时验证（简单）
   - 选项B：实时验证（输入时显示错误）
   - 选项C：失焦验证（离开字段时验证）
   
   **我倾向选项A**：提交时验证，保持简单

4. **日期选择器默认值？**
   - 选项A：空（用户必须选择）
   - 选项B：今天
   - 选项C：明天
   - 选项D：一周后
   
   **我倾向选项A**：空，强制用户明确选择

5. **是否需要loading状态？**
   - 提交按钮disabled + 文字变化
   - 是否需要全屏loading遮罩？
   
   **我倾向按钮disabled即可**，不需要全屏遮罩

**请你批判性审查：**
1. 实现方案是否遗漏关键点？
2. 5个关键问题的答案是否合理？
3. 是否有更优的UX设计？
4. 错误处理是否充分？
5. 是否需要添加其他功能（如草稿保存）？

要求：批判性思考，指出潜在问题和改进建议。

## Raw output

```text
**审查结论：需要小幅调整后再实施。** 草案方向基本合理，但成功跳转和登录路由不能按当前设想走，否则学生提交链路仍不闭环。

**主要问题**

1. **成功后停留当前页不是最佳方案。**  
   `createApplication()` 返回 `ApplicationDetail`，包含 `application_id`，现有详情页也已支持 `GET /api/applications/{id}/`。因此成功后应优先跳转到详情页：  
   `wx.redirectTo({ url: \`/pages/detail/detail?id=${res.application_id}\` })`  
   这比清空表单更合理，因为重复提交本来会触发 409，保留“继续提交”的入口反而制造无效操作。

2. **必须同时修复登录后的角色路由。**  
   当前 [login.ts](/home/caohui/projects/graduation-leave-system/miniprogram/pages/login/login.ts:40) 固定跳到 `/pages/approvals/approvals`，但契约规定学生禁止访问审批列表。实现 `student-application` 时应一起改成：学生跳申请页，辅导员/院长跳审批页。

3. **页面注册是必需项。**  
   [app.json](/home/caohui/projects/graduation-leave-system/miniprogram/app.json:2) 当前只注册了 login、approvals、detail。新页面实现后必须加入：
   `pages/student-application/student-application`

4. **页面自身也要做角色保护。**  
   不能只依赖登录跳转。`student-application.onLoad` 应检查 `userInfo`：未登录 `reLaunch` 到登录页；非 `student` 建议 `redirectTo` 到审批页或显示无权限。否则手动进入页面会到提交时才暴露 403。

**5 个关键问题判断**

1. **成功跳转目标：选 A，不选 C。**  
   跳详情页最符合现有页面结构和 API 返回值。C 会让用户留在一个已无有效后续动作的表单页。

2. **错误处理：不需要为每种错误做复杂 UI，但需要按 code 做文案增强。**  
   建议实现一个 `formatApplicationError(err)`：
   - `DORM_BLOCKED`：优先显示 `blocking_reason`，否则显示“宿舍清退未完成，暂不能提交”
   - `CONFLICT`：显示“已有待审批/已通过申请”，若有 `existing_application_id` 可给“查看申请”入口或直接跳详情
   - `VALIDATION_ERROR`：显示字段校验摘要
   - `FORBIDDEN`：显示“当前账号无提交权限”
   - fallback：`err.error?.message || err.message || '提交失败'`

3. **验证时机：提交时验证合理。**  
   但要补两个细节：`reason.trim()` 后再校验和提交；提交中防重复点击，`loading` 为 true 时直接 return。

4. **日期默认值：空值合理。**  
   但建议设置 `picker` 的 `start` 为今天，避免误选过去日期。默认空值 + 显式选择，比自动填今天更不容易误提交。

5. **loading：按钮 disabled 足够。**  
   不需要全屏遮罩。提交接口是单点动作，按钮态即可。失败后必须恢复 `loading=false`；成功跳转前也可以不恢复。

**建议最终方案**

- 新增 `student-application` 四个页面文件。
- `app.json` 注册新页面。
- `login.ts` 改为基于 `res.user.role` 跳转。
- `student-application.ts` 使用 `createDefaultApiClient()`。
- 成功后 `showToast`，短延迟或直接 `redirectTo` 到详情页。
- 错误用统一 formatter，针对 `DORM_BLOCKED`、`CONFLICT`、`VALIDATION_ERROR` 做轻量定制。
- 不做草稿保存。契约已把草稿、附件、通知等放到 Week 4+，现在加入草稿会扩大范围且与“单 active 申请”模型冲突。

总体上，这个页面应定位为“学生提交入口”，不是申请管理页。提交成功后的主体验证点应该落到详情页，而不是停留在表单页。


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e80d6-b3fc-7263-8a42-dfbf8d359931
--------
user
审查student-application页面实现方案

**背景：**
- API集中化已完成（createDefaultApiClient工厂函数）
- 需要实现学生申请页面
- 表单字段已确认：reason + leave_date（按API契约v0.2）

**实现方案草案：**

**1. 页面文件结构**
```
miniprogram/pages/student-application/
├── student-application.ts    (页面逻辑)
├── student-application.wxml  (页面结构)
├── student-application.wxss  (页面样式)
└── student-application.json  (页面配置)
```

**2. 表单设计（student-application.wxml）**
```xml
<view class="container">
  <view class="form">
    <view class="field">
      <text class="label">离校原因</text>
      <textarea placeholder="请输入离校原因" value="{{reason}}" bindinput="onReasonInput" />
    </view>
    
    <view class="field">
      <text class="label">离校日期</text>
      <picker mode="date" value="{{leaveDate}}" bindchange="onDateChange">
        <view class="picker">{{leaveDate || '请选择日期'}}</view>
      </picker>
    </view>
    
    <button bindtap="onSubmit" disabled="{{loading}}">
      {{loading ? '提交中...' : '提交申请'}}
    </button>
    
    <view class="error" wx:if="{{error}}">{{error}}</view>
  </view>
</view>
```

**3. 页面逻辑（student-application.ts）**
- 遵循login.ts模式
- 使用createDefaultApiClient()
- 表单验证：reason非空，leaveDate非空
- 调用apiClient.createApplication({reason, leave_date})
- 成功：显示toast + 跳转（跳转到哪里？）
- 错误处理：DORM_BLOCKED(422), CONFLICT(409), VALIDATION_ERROR(400)

**4. 样式（student-application.wxss）**
- 复用login.wxss的container/form/field样式
- 添加textarea特定样式

**关键问题需要你审查：**

1. **提交成功后跳转目标？**
   - 选项A：跳转到申请详情页（需要application_id）
   - 选项B：跳转到学生申请列表页（Phase 4B不包含）
   - 选项C：显示成功toast后停留在当前页（清空表单）
   - 选项D：返回上一页（但学生登录后直接到这里，没有上一页）
   
   **我倾向选项C**：成功后清空表单，允许学生查看刚提交的内容或继续提交（虽然API会409）

2. **错误处理优先级？**
   - DORM_BLOCKED(422)：宿舍清退未完成 - 显示blocking_reason
   - CONFLICT(409)：已有待审批/已通过申请 - 显示existing_application_id
   - VALIDATION_ERROR(400)：字段验证失败 - 显示details
   - 403/401：权限/认证错误 - 已由ApiClient处理
   
   **是否需要针对每种错误定制UI？** 还是统一显示error.message？

3. **表单验证时机？**
   - 选项A：提交时验证（简单）
   - 选项B：实时验证（输入时显示错误）
   - 选项C：失焦验证（离开字段时验证）
   
   **我倾向选项A**：提交时验证，保持简单

4. **日期选择器默认值？**
   - 选项A：空（用户必须选择）
   - 选项B：今天
   - 选项C：明天
   - 选项D：一周后
   
   **我倾向选项A**：空，强制用户明确选择

5. **是否需要loading状态？**
   - 提交按钮disabled + 文字变化
   - 是否需要全屏loading遮罩？
   
   **我倾向按钮disabled即可**，不需要全屏遮罩

**请你批判性审查：**
1. 实现方案是否遗漏关键点？
2. 5个关键问题的答案是否合理？
3. 是否有更优的UX设计？
4. 错误处理是否充分？
5. 是否需要添加其他功能（如草稿保存）？

要求：批判性思考，指出潜在问题和改进建议。
codex
我会先读取项目里的评审协议和命令规范，避免把这次方案审查做成脱离项目约定的泛泛建议。
exec
/bin/bash -lc "pwd && sed -n '1,220p' /home/caohui/.codex/RTK.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
/home/caohui/projects/graduation-leave-system
# RTK - Rust Token Killer (Codex CLI)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Always prefix shell commands with `rtk`.

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

## Meta Commands

```bash
rtk gain            # Token savings analytics
rtk gain --history  # Recent command savings history
rtk proxy <cmd>     # Run raw command without filtering
```

## Verification

```bash
rtk --version
rtk gain
which rtk
```

exec
/bin/bash -lc "sed -n '1,260p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Codex审查流程指南

**版本：** v2.0  
**更新日期：** 2026-05-28  
**适用范围：** 使用 `/oh-my-claudecode:ask codex` 进行文档审查

---

## Load Trigger (懒加载条件)

Read this file when ANY of these occur:
- 技术文档审查（Technical design documents）
- 数据库变更（Database schema changes）
- API设计（API interface design）
- 数据对接方案（Data integration plans）
- 系统架构调整（System architecture updates）
- 用户要求与Codex对话（User requests Codex review）

---

## 一、流程概述

本指南定义了与Codex进行对话式审查的标准流程，使用OMC内置的`/oh-my-claudecode:ask`技能。

**核心原则：**
- 使用统一的`/oh-my-claudecode:ask codex`方式
- 结构化的审查请求
- 批判性分析Codex建议
- 迭代式达成共识

---

## 二、完整流程（7步）

### 第1步：创建审查请求文档

**文件命名：** `XX-[主题]-review-request.md`

**文档结构：**
```markdown
# [主题] - Codex审查请求

**审查日期：** YYYY-MM-DD
**审查类型：** [类型]
**审查范围：** [范围]

## 一、背景/需求
[说明审查背景和目的]

## 二、已完成的工作
[列出已完成的修改]

## 三、审查要点
[列出需要Codex关注的具体问题]

## 四、潜在问题
[列出已知的潜在问题]

## 五、期望输出
1. 审查结论：通过/需要修改/不建议
2. 问题清单
3. 修复建议
4. 最终方案
```

---

### 第2步：调用Codex审查

**使用OMC内置技能：**
```
/oh-my-claudecode:ask codex "审查 docs/discussions/[路径]/XX-[主题]-review-request.md - [具体审查要求]"
```

**示例：**
```
/oh-my-claudecode:ask codex "审查 docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md - 这是我们对你第二轮审查的回应。请确认：1) 3个关键修正方案是否可行 2) 5个补充细节是否完整 3) 数据库模型调整方案是否有遗漏 4) 是否可以基于此创建v2共识文档"
```

**优点：**
- 自动保存结果为artifact：`.omc/artifacts/ask/codex-*.md`
- 统一的调用接口
- 更好的错误处理

---

### 第3步：保存Codex审查结果

**文件命名：** `XX+1-[主题]-codex-response.md`

**从artifact中提取关键内容：**
- 审查结论
- 发现的问题（按优先级分类）
- 具体修复建议
- 代码示例

**文档结构：**
```markdown
# [主题] - Codex审查响应

**审查日期：** YYYY-MM-DD
**审查人：** Codex
**Artifact路径：** .omc/artifacts/ask/codex-[timestamp].md

## 审查结论
[总体评价]

## 发现的问题

### 问题1：[标题] [优先级]
**位置：** 文件:行号
**问题描述：** [详细说明]
**影响：** [影响分析]
**修复建议：** [具体方案]

[重复其他问题]

## 审查通过的部分
[列出做得好的地方]
```

---

### 第4步：Claude响应Codex审查

**文件命名：** `XX+2-[主题]-claude-response.md`

**文档结构：**
```markdown
# [主题] - Claude响应

**响应日期：** YYYY-MM-DD
**针对：** Codex审查响应

## 对Codex审查的回应
[总体回应]

## 问题确认与修复方案

### 问题1：[标题]
**Codex指出：** [问题描述]
**Claude确认：** [确认分析]
**修复方案：** [具体方案]

[重复其他问题]

## 修改清单
[列出立即执行的修改]
```

---

### 第5步：执行修复

**按优先级修复：**
1. P0/CRITICAL问题 - 必须立即修复
2. P1/MAJOR问题 - 应该修复
3. P2/MINOR问题 - 可选修复

**修复后验证：**
- 使用Read工具验证修改正确
- 检查所有相关文档一致性

---

### 第6步：创建共识文档

**文件命名：** `XX+3-[主题]-consensus.md`

**文档结构：**
```markdown
# [主题] - 最终共识

**日期：** YYYY-MM-DD
**参与方：** Codex + Claude

## 审查结论
**状态：** 已修复/通过

## 已完成的修复
[列出所有修复，包含修改前后对比]

## 最终方案
[总结最终达成的方案]

## 文档一致性确认
[确认所有相关文档已更新]
```

---

### 第7步：归档到项目文档

**更新以下文件：**
1. `docs/PROJECT-SUMMARY.md` - 添加审查记录
2. `.omc/session-context.json` - 更新completed和artifacts
3. Git commit + push

---

## 三、讨论原则

### 1. 批判性思维
- **不要急于认同：** 收到Codex审查后，仔细分析每个问题
- **合理质疑：** 如果Codex建议不合理，在Claude响应中说明理由
- **深入分析：** 不只看表面问题，分析根本原因和影响范围

### 2. 迭代式讨论
- **不局限一次：** 如果修复后发现新问题，可再次提交Codex审查
- **及时发现问题：** 修复过程中发现不一致，立即记录
- **多轮达成共识：** 复杂问题可能需要2-3轮讨论才能完全解决

### 3. 分段处理
- **大篇幅分章节：** 超过500行的文档，按章节分别审查
- **分批修复：** 问题多时，按优先级分批修复和验证
- **渐进式共识：** 每个章节达成共识后再进入下一章节

---

## 四、文件编号规则

**连续编号：**
- XX号：审查请求
- XX+1号：Codex响应
- XX+2号：Claude响应
- XX+3号：最终共识

**示例：**
- 34-codex-second-review-response.md（审查请求）
- 35-response-to-codex-critical-issues.md（Claude响应）
- 36-data-confirmation-and-implementation.md（共识文档）

---

## 五、验证清单

**审查前：**
- [ ] 审查请求文档结构完整
- [ ] 审查范围明确
- [ ] 期望输出清晰

**审查中：**
- [ ] `/oh-my-claudecode:ask codex`调用成功
- [ ] Artifact已生成
- [ ] 问题优先级明确

**审查后：**
- [ ] 所有问题已修复
- [ ] 文档一致性已验证
- [ ] 项目文档已更新
- [ ] Git已提交推送

---

## 六、关键要点

### ✓ 成功要素
- 审查请求文档要详细、结构化
- 使用`/oh-my-claudecode:ask codex`（不是直接调用CLI）
- Claude响应要具体、可执行、有批判性分析

codex
评审协议确认：这次属于技术方案审查，应按“问题优先、批判性分析、给出可执行修正”的方式输出。接下来我会看现有登录页、API client 和页面路由，避免凭草案判断跳转与错误处理。
exec
/bin/bash -lc 'rtk rg -n "createDefaultApiClient|createApplication|DORM_BLOCKED|CONFLICT|VALIDATION_ERROR|login" miniprogram docs -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/api/contract-v0.2.md:93:- Attempting operations on terminal states returns `409 CONFLICT`
docs/api/contract-v0.2.md:101:- Mismatch returns `409 CONFLICT`
docs/api/contract-v0.2.md:105:- Attempting repeat operations returns `409 CONFLICT`
docs/api/contract-v0.2.md:184:| `VALIDATION_ERROR` | 400 | Request validation failed | Missing/invalid fields |
docs/api/contract-v0.2.md:187:| `CONFLICT` | 409 | State conflict | Duplicate/invalid operation |
docs/api/contract-v0.2.md:188:| `DORM_BLOCKED` | 422 | Dorm checkout incomplete | Blocking condition |
docs/api/contract-v0.2.md:203:### 6.1 VALIDATION_ERROR (400)
docs/api/contract-v0.2.md:221:    "code": "VALIDATION_ERROR",
docs/api/contract-v0.2.md:299:### 6.4 CONFLICT (409)
docs/api/contract-v0.2.md:319:    "code": "CONFLICT",
docs/api/contract-v0.2.md:347:    "code": "CONFLICT",
docs/api/contract-v0.2.md:370:    "code": "CONFLICT",
docs/api/contract-v0.2.md:376:### 6.5 DORM_BLOCKED (422)
docs/api/contract-v0.2.md:396:    "code": "DORM_BLOCKED",
docs/week3-day0-acceptance-checklist.md:67:curl -X POST http://localhost:8000/api/auth/login \
docs/week3-day0-acceptance-checklist.md:124:curl -X POST http://localhost:8000/api/auth/login \
docs/week3-day0-acceptance-checklist.md:188:curl -X POST http://localhost:8000/api/auth/login \
docs/week3-day0-acceptance-checklist.md:302:curl -X POST http://localhost:8000/api/auth/login \
docs/week3-day0-acceptance-checklist.md:422:STUDENT_TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
docs/week3-day0-acceptance-checklist.md:439:COUNSELOR_TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
docs/week3-day0-acceptance-checklist.md:452:DEAN_TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
docs/plans/week-0-1-execution-plan.md:30:  - POST /api/auth/login
docs/plans/week-0-1-execution-plan.md:71:- POST /api/auth/login 可用
docs/plans/week-0-1-execution-plan.md:122:  - 测试3：宿舍清退未完成 → 提交申请失败（DORM_BLOCKED）
docs/PROJECT-SUMMARY.md:237:  - P1-1修复：补齐4个缺失错误样例（400 VALIDATION_ERROR, 404 NOT_FOUND, 409 CONFLICT, 500 INTERNAL_ERROR）
docs/PROJECT-SUMMARY.md:254:  - JWT认证系统（login API）
docs/PROJECT-SUMMARY.md:290:  - DORM_BLOCKED（宿舍清退未完成）
docs/PROJECT-SUMMARY.md:291:  - CONFLICT（重复提交申请）
docs/PROJECT-SUMMARY.md:294:  - VALIDATION_ERROR（参数验证失败）
docs/PROJECT-SUMMARY.md:304:  - DORM_BLOCKED：宿舍清退未完成阻断提交
docs/PROJECT-SUMMARY.md:305:  - CONFLICT：重复提交申请
docs/PROJECT-SUMMARY.md:308:  - VALIDATION_ERROR：参数验证失败
docs/PROJECT-SUMMARY.md:714:  - pages/login/login.wxml（UI标记）
docs/PROJECT-SUMMARY.md:715:  - pages/login/login.wxss（样式）
docs/PROJECT-SUMMARY.md:716:  - pages/login/login.ts（登录逻辑）
docs/PROJECT-SUMMARY.md:730:- miniprogram/pages/login/*（wxml, wxss, ts）
docs/PROJECT-SUMMARY.md:855:- 4页面：login, student-application, approvals（共享）, detail（共享）
docs/contracts/contract-v0.2.md:126:- 审批记录必须仍为 `pending`，否则返回 `409 CONFLICT`。
docs/contracts/contract-v0.2.md:146:### POST `/api/auth/login`
docs/contracts/contract-v0.2.md:220:    "code": "CONFLICT",
docs/contracts/contract-v0.2.md:234:| VALIDATION_ERROR | 400 | 申请提交字段缺失或格式错误 |
docs/contracts/contract-v0.2.md:237:| CONFLICT | 409 | 重复提交、重复审批、状态与审批步骤不匹配 |
docs/contracts/contract-v0.2.md:238:| DORM_BLOCKED | 422 | 宿舍清退未完成 |
docs/contracts/contract-v0.1.md:144:| pending | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:145:| not_started | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:146:| unknown | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:166:| VALIDATION_ERROR | 400 | 请求参数校验失败 | 必填字段缺失、格式错误 |
docs/contracts/contract-v0.1.md:170:| CONFLICT | 409 | 资源冲突 | 重复提交申请 |
docs/contracts/contract-v0.1.md:171:| DORM_BLOCKED | 422 | 宿舍清退未完成 | 提交申请时宿舍未清退 |
docs/contracts/contract-v0.1.md:185:    "code": "DORM_BLOCKED",
docs/contracts/contract-v0.1.md:201:#### POST /api/auth/login
docs/contracts/contract-v0.1.md:460:    "code": "VALIDATION_ERROR",
docs/contracts/contract-v0.1.md:507:    "code": "CONFLICT",
docs/contracts/contract-v0.1.md:521:    "code": "DORM_BLOCKED",
docs/contracts/contract-v0.1.md:598:  rest.post('/api/auth/login', (req, res, ctx) => {
docs/contracts/contract-v0.1.md:626:    response = client.post('/api/auth/login', {
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:22:1. Fix login URL in all Week 1 Day 5 tests
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:23:   - Change `/api/auth/login/` to `/api/auth/login` (remove trailing slash)
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:183:- Root cause: Tests use `/api/auth/login/` but route is `/api/auth/login`
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:23:- Root cause: Tests use `/api/auth/login/` but route is `/api/auth/login` (no trailing slash)
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:93:- Fix Day 2 drift (login URL, mock, smoke): 30-60 min
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:127:1. Fix login URL in tests (remove trailing slash)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:21:- `test_application_flow`: 1 failure (404 on login)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:22:- `test_error_cases`: 5 errors (404 on login)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:23:- `test_rejection_flow`: 2 errors (404 on login)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:32:**Root Cause:** Tests use `/api/auth/login/` but route is `/api/auth/login` (no trailing slash)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:97:1. Fix login URL in all Week 1 Day 5 tests
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:98:   - Change `/api/auth/login/` to `/api/auth/login`
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:205:**YES.** I verified the test failures myself. 8 out of 12 tests are failing due to login URL mismatch.
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:127:        'login_ip': '10/minute',
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:128:        'login_user': '5/5minute',
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:78:def wechat_login(request):
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:34:Step 1: POST /api/v1/auth/wechat/login
docs/discussions/codex-review-2026-05-27/04-database-review.md:204:- 无`failed_login_attempts`计数器
docs/discussions/codex-review-2026-05-27/04-database-review.md:205:- 无`last_login_at`时间戳
docs/discussions/codex-review-2026-05-27/04-database-review.md:216:    failed_login_attempts INT DEFAULT 0 COMMENT '失败登录次数',
docs/discussions/codex-review-2026-05-27/04-database-review.md:217:    last_login_at TIMESTAMP COMMENT '最后登录时间',
docs/discussions/codex-review-2026-05-27/04-database-review.md:218:    last_login_ip VARCHAR(50) COMMENT '最后登录IP',
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:186:- failed_login_attempts INT
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:187:- last_login_at TIMESTAMP
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:188:- last_login_ip VARCHAR(50)
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:78:- 暴力破解密码（/api/v1/auth/login无速率限制）
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:93:        'login': '5/minute',
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:300:def first_login(student_id, password):
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:415:    'login_ip': '10/minute',      # 每IP 10次/分钟
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:416:    'login_user': '5/5minute',    # 每用户 5次/5分钟
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:146:    failed_login_attempts = models.IntegerField(default=0, help_text='失败登录次数')
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:147:    last_login_at = models.DateTimeField(null=True, help_text='最后登录时间')
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:148:    last_login_ip = models.CharField(max_length=50, null=True, help_text='最后登录IP')
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:46:- ✅ 包含password_setup_required, account_locked, failed_login_attempts
miniprogram/services/api.ts:68:  async login(req: LoginRequest): Promise<LoginResponse> {
miniprogram/services/api.ts:69:    return this.request('/api/auth/login', {
miniprogram/services/api.ts:75:  async createApplication(req: ApplicationCreateRequest): Promise<ApplicationDetail> {
miniprogram/services/api.ts:126:export function createDefaultApiClient(): ApiClient {
miniprogram/services/api.ts:136:      wx.reLaunch({ url: '/pages/login/login' });
miniprogram/pages/approvals/approvals.ts:1:import { createDefaultApiClient } from '../../services/api';
miniprogram/pages/approvals/approvals.ts:5:const apiClient = createDefaultApiClient();
miniprogram/pages/approvals/approvals.ts:19:      wx.reLaunch({ url: '/pages/login/login' });
miniprogram/pages/login/login.wxml:17:    <button class="login-btn" bindtap="onLogin" disabled="{{loading}}">
miniprogram/pages/login/login.wxss:45:.login-btn {
miniprogram/pages/login/login.wxss:56:.login-btn[disabled] {
miniprogram/pages/login/login.ts:1:import { createDefaultApiClient } from '../../services/api';
miniprogram/pages/login/login.ts:4:const apiClient = createDefaultApiClient();
miniprogram/pages/login/login.ts:33:      const res = await apiClient.login({ user_id: userId, password });
miniprogram/pages/detail/detail.ts:1:import { createDefaultApiClient } from '../../services/api';
miniprogram/pages/detail/detail.ts:5:const apiClient = createDefaultApiClient();
miniprogram/pages/detail/detail.ts:26:      wx.reLaunch({ url: '/pages/login/login' });
miniprogram/app.json:3:    "pages/login/login",
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:24:- 400 VALIDATION_ERROR
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:26:- 409 CONFLICT
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:54:   - 建议：后续统一为"5个HTTP路由（login + 4个业务端点）"
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:76:- API端点（5个HTTP路由：login + submit + query + approve + reject）
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:33:- 400 VALIDATION_ERROR（参数验证失败）
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:35:- 409 CONFLICT（重复提交）
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:34:1. `POST /api/auth/login`
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:46:- Day 3-4新增HTTP路由：4个，不含Day 1-2已完成的login
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:65:- `VALIDATION_ERROR` 400
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:67:- `CONFLICT` 409
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:125:    "code": "VALIDATION_ERROR",
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:46:- Section 4.1 POST /api/auth/login添加说明
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:70:1. **Week 1 Day 3-4交付物：** 需要确认是否应该从"4个API端点"改为"5个API端点"（包含login）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:34:- 错误码（VALIDATION_ERROR/AUTH_REQUIRED/FORBIDDEN/NOT_FOUND/CONFLICT/DORM_BLOCKED/PROVIDER_UNAVAILABLE）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:28:  1. POST /api/auth/login
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:70:- 在contract-v0.1.md Section 4.1 POST /api/auth/login添加说明
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:28:1. `VALIDATION_ERROR` - 400
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:32:5. `CONFLICT` - 409
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:33:6. `DORM_BLOCKED` - 422
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:41:| 400 | `VALIDATION_ERROR` | Section 6.2 | 通过 |
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:45:| 409 | `CONFLICT` | Section 6.2 | 通过 |
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:46:| 422 | `DORM_BLOCKED` | Section 6.2 | 通过 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:61:| 认证 | login_id、role、access_token mock/JWT格式 | 微信OAuth |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:62:| 错误 | VALIDATION_ERROR、AUTH_REQUIRED、FORBIDDEN、NOT_FOUND、CONFLICT、DORM_BLOCKED、PROVIDER_UNAVAILABLE | 完整国际化错误文案 |
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:21:**400 VALIDATION_ERROR：**
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:25:    "code": "VALIDATION_ERROR",
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:48:**409 CONFLICT：**
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:52:    "code": "CONFLICT",
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:108:**建议：** 统一为"5个HTTP路由（login + 4个业务端点）"或"4个业务API端点"
docs/design/2026-05-27-system-design.md:270:    failed_login_attempts INT DEFAULT 0 COMMENT '失败登录次数',
docs/design/2026-05-27-system-design.md:271:    last_login_at TIMESTAMP COMMENT '最后登录时间',
docs/design/2026-05-27-system-design.md:272:    last_login_ip VARCHAR(50) COMMENT '最后登录IP',
docs/design/2026-05-27-system-design.md:540:- `login` - 登录
docs/design/2026-05-27-system-design.md:678:POST /api/v1/auth/login
docs/design/2026-05-27-system-design.md:707:POST /api/v1/auth/wechat/login
docs/design/2026-05-27-system-design.md:2077:        'login': '5/minute',
docs/design/2026-05-27-system-design.md:2086:    scope = 'login'
docs/design/2026-05-27-system-design.md:2096:    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
docs/design/2026-05-27-system-design.md:2102:        location /api/v1/auth/login {
docs/design/2026-05-27-system-design.md:2103:            limit_req zone=login burst=2 nodelay;
docs/design/2026-05-27-system-design.md:2655:def test_login_rate_limit():
docs/design/2026-05-27-system-design.md:2658:        response = client.post('/api/v1/auth/login', data)

exec
/bin/bash -lc "rtk sed -n '1,240p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk rg --files miniprogram | rtk rg 'pages/(login|student|application)|api|app\\.(json|ts)"'$'"'" in /home/caohui/projects/graduation-leave-system
 succeeded in 214ms:
 succeeded in 250ms:
# Claude-Codex Collaboration Protocol

Version: 0.3
Status: active
Owner: Claude + Codex

## 1. Purpose

This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.

Agents must read this file before participating in the collaboration workflow.

## 2. Directory Layout

All collaboration files live under `.omc/collaboration/`.

- `protocol.md`: this protocol.
- `state.json`: current shared workflow state.
- `events.jsonl`: append-only event log.
- `tasks/`: task specifications and task handoff documents.
- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
- `locks/`: lock files or directories for serialized work.
- `codex-ready.md`: Codex readiness signal.

Filesystem requirements:

- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
- Local filesystems and NFSv4 are acceptable for this workflow.
- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
- Production testing MUST NOT proceed on an unsupported filesystem.

## 3. Authority And Conflicts

This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.

If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.

Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.

## 4. Shared State

`state.json` is the latest compact state snapshot. It must remain valid JSON.

`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.

Recommended schema:

```json
{
  "workflow_id": "claude-codex-collab-mvp",
  "current_task": null,
  "active_agent": "none",
  "status": "initialized",
  "last_event_id": 0,
  "updated_at": "2026-05-30T00:00:00.000Z"
}
```

Field meanings:

- `workflow_id`: stable collaboration workflow identifier.
- `current_task`: active task id or `null`.
- `active_agent`: `claude`, `codex`, or `none`.
- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
- `last_event_id`: numeric id of the last event written to `events.jsonl`.
- `updated_at`: UTC ISO-8601 timestamp for the state update.

State updates should be minimal and should not replace durable task or artifact content.

State write rules:

- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
- Agents MUST validate the temporary file as well-formed JSON before publishing it.
- Agents MUST atomically rename the validated temporary file into place with `mv`.
- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.

## 5. Event Log

`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.

Required event fields:

```json
{
  "id": 1,
  "type": "codex_ready",
  "agent": "codex",
  "timestamp": "2026-05-30T00:00:00.000Z",
  "summary": "Short event summary."
}
```

Recommended optional fields:

- `task_id`: related task id.
- `artifacts`: array of artifact paths.
- `status`: resulting workflow status.
- `details`: compact structured metadata.

Event id rules:

- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
- New event ids MUST be allocated while holding `locks/journal.lock`.
- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.

Common event types:

- `claude_ready`
- `codex_ready`
- `task_created`
- `task_claimed`
- `artifact_created`
- `handoff_requested`
- `review_requested`
- `blocked`
- `completed`

## 6. Tasks

Task documents belong in `.omc/collaboration/tasks/`.

Recommended task filename:

```text
TASK-YYYYMMDD-NN-short-name.md
```

Recommended task content:

- Task id.
- Owner or requesting agent.
- Objective.
- Scope.
- Inputs and relevant files.
- Expected outputs.
- Constraints and mandatory rules.
- Acceptance criteria.
- Current status.

When claiming a task, the agent MUST use this atomic claim procedure:

1. Acquire `locks/journal.lock`.
2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.

## 7. Artifacts

Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.

Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.

Recommended artifact filenames:

```text
YYYYMMDD-HHMM-agent-topic.md
```

For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.

## 8. Locks

Locks are files or directories under `.omc/collaboration/locks/`.

Use a lock when two agents might modify the same shared collaboration file at the same time.

Recommended lock filename:

```text
resource-name.lock
```

Recommended lock content:

```json
{
  "agent": "codex",
  "resource": "state.json",
  "created_at": "2026-05-30T00:00:00.000Z",
  "reason": "Updating state after event append."
}
```

Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.

### Required Journal Lock

Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.

Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:

```bash
mkdir .omc/collaboration/locks/journal.lock
```

The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.

The lock directory MUST contain `owner.json`:

```json
{
  "agent": "codex",
  "task_id": "TASK-20260530-01",
  "created_at": "2026-05-30T08:00:00.000Z",
  "heartbeat_at": "2026-05-30T08:00:00.000Z",
  "reason": "append event and update state"
}
```

The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.

## 9. Failure Recovery

Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.

If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.

If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.

If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.

Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.

## 10. Handoff Rules

When handing work to the other agent:

1. Write or update the task document.
2. Write any supporting artifact needed for context.
3. Append a `handoff_requested` event.
4. Update `state.json` with the current task, status, active agent, and last event id.
5. State the handoff clearly in the user-facing response when applicable.


exec
/bin/bash -lc "rtk sed -n '1,220p' miniprogram/types/api.ts" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
// API Types based on v0.2 Contract
// Generated: 2026-05-31

export type UserRole = 'student' | 'counselor' | 'dean';

export type ApplicationStatus =
  | 'draft'
  | 'pending_counselor'
  | 'pending_dean'
  | 'approved'
  | 'rejected';

export type ApprovalDecision = 'pending' | 'approved' | 'rejected';

export type ApprovalStep = 'counselor' | 'dean';

// Auth
export interface LoginRequest {
  user_id: string;
  password: string;
}

export interface User {
  user_id: string;
  name: string;
  role: UserRole;
  class_id?: string | null;
}

export interface LoginResponse {
  access_token: string;
  token_type: 'Bearer';
  user: User;
}

// Applications
export interface ApplicationCreateRequest {
  reason: string;
  leave_date: string; // YYYY-MM-DD
}

export interface Application {
  application_id: string;
  student_id: string;
  student_name: string;
  class_id: string;
  reason: string;
  leave_date: string;
  status: ApplicationStatus;
  created_at: string;
  updated_at: string;
}

export interface ApplicationDetail extends Application {
  dorm_checkout_status: string;
  approvals: ApprovalDetail[];
}

// Approvals
export interface ApprovalDetail {
  approval_id: string;
  application_id: string;
  step: ApprovalStep;
  approver_id: string;
  approver_name: string;
  decision: ApprovalDecision;
  comment: string | null;
  decided_at: string | null;
}

export interface ApprovalListItem {
  approval_id: string;
  application_id: string;
  step: ApprovalStep;
  approver_id: string;
  approver_name: string;
  decision: ApprovalDecision;
  created_at: string;
}

export interface ApprovalActionRequest {
  comment?: string;
}

export interface ApprovalActionResponse {
  approval_id: string;
  decision: ApprovalDecision;
  comment: string | null;
  decided_at: string;
}

// Pagination
export interface PaginatedResponse<T> {
  count: number;
  results: T[];
}

// Errors
export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: any;
  };
}

exec
/bin/bash -lc "rtk sed -n '1,240p' miniprogram/services/api.ts" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
// API Client for WeChat Mini Program (wx.request)
import type {
  LoginRequest,
  LoginResponse,
  ApplicationCreateRequest,
  ApplicationDetail,
  Application,
  ApprovalListItem,
  ApprovalActionRequest,
  ApprovalActionResponse,
  PaginatedResponse,
  ApiError,
} from '../types/api';

export interface ApiConfig {
  baseUrl: string;
  getToken?: () => string | null;
  onUnauthorized?: () => void;
}

export class ApiClient {
  private config: ApiConfig;

  constructor(config: ApiConfig) {
    this.config = config;
  }

  private async request<T>(
    endpoint: string,
    options: { method?: string; data?: any } = {}
  ): Promise<T> {
    const token = this.config.getToken?.();
    const header: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (token) {
      header['Authorization'] = `Bearer ${token}`;
    }

    return new Promise((resolve, reject) => {
      wx.request({
        url: `${this.config.baseUrl}${endpoint}`,
        method: (options.method || 'GET') as any,
        header,
        data: options.data,
        success: (res) => {
          if (res.statusCode === 401) {
            this.config.onUnauthorized?.();
            reject(new Error('Unauthorized'));
            return;
          }

          if (res.statusCode >= 400) {
            reject(res.data as ApiError);
            return;
          }

          resolve(res.data as T);
        },
        fail: (err) => {
          reject(new Error(err.errMsg));
        },
      });
    });
  }

  async login(req: LoginRequest): Promise<LoginResponse> {
    return this.request('/api/auth/login', {
      method: 'POST',
      data: req,
    });
  }

  async createApplication(req: ApplicationCreateRequest): Promise<ApplicationDetail> {
    return this.request('/api/applications/', {
      method: 'POST',
      data: req,
    });
  }

  async listApplications(
    limit = 20,
    offset = 0
  ): Promise<PaginatedResponse<Application>> {
    return this.request(
      `/api/applications/?limit=${limit}&offset=${offset}`
    );
  }

  async getApplication(id: string): Promise<ApplicationDetail> {
    return this.request(`/api/applications/${id}/`);
  }

  async listApprovals(
    decision: 'pending' | 'approved' | 'rejected' | 'all' = 'pending',
    limit = 20,
    offset = 0
  ): Promise<PaginatedResponse<ApprovalListItem>> {
    return this.request(
      `/api/approvals/?decision=${decision}&limit=${limit}&offset=${offset}`
    );
  }

  async approveApproval(
    id: string,
    req: ApprovalActionRequest
  ): Promise<ApprovalActionResponse> {
    return this.request(`/api/approvals/${id}/approve/`, {
      method: 'POST',
      data: req,
    });
  }

  async rejectApproval(
    id: string,
    req: ApprovalActionRequest
  ): Promise<ApprovalActionResponse> {
    return this.request(`/api/approvals/${id}/reject/`, {
      method: 'POST',
      data: req,
    });
  }
}

export function createDefaultApiClient(): ApiClient {
  const app = getApp<IAppOption>();
  return new ApiClient({
    baseUrl: 'http://localhost:8001',
    getToken: () => app.globalData.token,
    onUnauthorized: () => {
      wx.removeStorageSync('token');
      wx.removeStorageSync('userInfo');
      app.globalData.token = '';
      app.globalData.userInfo = null;
      wx.reLaunch({ url: '/pages/login/login' });
    }
  });
}

exec
/bin/bash -lc "rtk sed -n '1,120p' miniprogram/app.json" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
  "pages": [
    "pages/login/login",
    "pages/approvals/approvals",
    "pages/detail/detail"
  ],
  "window": {
    "navigationBarTitleText": "毕业离校申请系统",
    "navigationBarBackgroundColor": "#1890ff",
    "navigationBarTextStyle": "white",
    "backgroundColor": "#f5f5f5"
  },
  "sitemapLocation": "sitemap.json"
}

exec
/bin/bash -lc "rtk sed -n '1,220p' miniprogram/pages/login/login.ts" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
import { createDefaultApiClient } from '../../services/api';

const app = getApp<IAppOption>();
const apiClient = createDefaultApiClient();

Page({
  data: {
    userId: '',
    password: '',
    loading: false,
    error: '',
  },

  onUserIdInput(e: any) {
    this.setData({ userId: e.detail.value });
  },

  onPasswordInput(e: any) {
    this.setData({ password: e.detail.value });
  },

  async onLogin() {
    const { userId, password } = this.data;

    if (!userId || !password) {
      this.setData({ error: '请输入用户ID和密码' });
      return;
    }

    this.setData({ loading: true, error: '' });

    try {
      const res = await apiClient.login({ user_id: userId, password });

      wx.setStorageSync('token', res.access_token);
      wx.setStorageSync('userInfo', res.user);
      app.globalData.token = res.access_token;
      app.globalData.userInfo = res.user;

      wx.redirectTo({ url: '/pages/approvals/approvals' });
    } catch (err: any) {
      this.setData({
        error: err.error?.message || err.message || '登录失败',
        loading: false,
      });
    }
  },
});

exec
/bin/bash -lc "rtk sed -n '200,255p' docs/contracts/contract-v0.2.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:

响应：`200 ApprovalDetail`。

### POST `/api/approvals/{approval_id}/reject/`

请求：

```json
{"comment":"材料不齐全"}
```

响应：`200 ApprovalDetail`。

## 7. 错误响应

业务错误统一使用：

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "申请已存在，不能重复提交",
    "details": {
      "student_id": "2020001",
      "existing_application_id": "app_eb41d2f5"
    }
  }
}
```

当前 Week 3 核心错误码：

| code | HTTP | 场景 |
| --- | --- | --- |
| VALIDATION_ERROR | 400 | 申请提交字段缺失或格式错误 |
| FORBIDDEN | 403 | 角色不符、非指定审批人、越权访问 |
| NOT_FOUND | 404 | 申请或审批记录不存在 |
| CONFLICT | 409 | 重复提交、重复审批、状态与审批步骤不匹配 |
| DORM_BLOCKED | 422 | 宿舍清退未完成 |

说明：登录接口当前对凭据错误返回 DRF serializer error 结构，不保证业务错误 envelope。全局异常 envelope 属于 Week 4+ 范围。

## 8. Deferred To Week 4

- 附件、草稿、审计轨迹、通知、微信 OAuth。
- 全量 OpenAPI schema。
- 全局 DRF 异常 envelope 统一。
- 完整权限排列组合测试矩阵。

exec
/bin/bash -lc "rtk sed -n '130,260p' docs/contracts/contract-v0.2.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
- 已处于 `pending_counselor`、`pending_dean`、`approved` 的申请会阻断重复提交。

## 5. 权限矩阵

| 操作 | student | counselor | dean |
| --- | --- | --- | --- |
| 登录 | 自己账号 | 自己账号 | 自己账号 |
| 提交申请 | 允许 | 禁止 | 禁止 |
| 申请列表 | 仅本人申请 | 仅本人待处理 counselor 审批对应申请 | 仅本人待处理 dean 审批对应申请 |
| 申请详情 | 仅本人申请 | 仅负责班级申请 | 仅本人待处理 dean 审批对应申请 |
| 审批列表 | 禁止 | 仅本人 counselor 审批 | 仅本人 dean 审批 |
| counselor 审批动作 | 禁止 | 仅指定 approver | 禁止 |
| dean 审批动作 | 禁止 | 禁止 | 仅指定 approver |

## 6. 端点

### POST `/api/auth/login`

请求：

```json
{"user_id":"2020001","password":"2020001"}
```

响应：

```json
{
  "access_token": "<jwt>",
  "token_type": "Bearer",
  "user": {
    "user_id": "2020001",
    "name": "张三",
    "role": "student",
    "class_id": "CS2020-01"
  }
}
```

### POST `/api/applications/`

请求：

```json
{"reason":"毕业离校","leave_date":"2024-06-30"}
```

响应：`201 ApplicationDetail`。

### GET `/api/applications/?limit=20&offset=0`

响应：`PaginatedResponse<ApplicationListItem>`。

### GET `/api/applications/{application_id}/`

响应：`ApplicationDetail`。

### GET `/api/approvals/?decision=pending&limit=20&offset=0`

`decision` 可取 `pending | approved | rejected | all`，默认 `pending`。

响应：`PaginatedResponse<ApprovalListItem>`。

### POST `/api/approvals/{approval_id}/approve/`

请求：

```json
{"comment":"同意"}
```

响应：`200 ApprovalDetail`。

### POST `/api/approvals/{approval_id}/reject/`

请求：

```json
{"comment":"材料不齐全"}
```

响应：`200 ApprovalDetail`。

## 7. 错误响应

业务错误统一使用：

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "申请已存在，不能重复提交",
    "details": {
      "student_id": "2020001",
      "existing_application_id": "app_eb41d2f5"
    }
  }
}
```

当前 Week 3 核心错误码：

| code | HTTP | 场景 |
| --- | --- | --- |
| VALIDATION_ERROR | 400 | 申请提交字段缺失或格式错误 |
| FORBIDDEN | 403 | 角色不符、非指定审批人、越权访问 |
| NOT_FOUND | 404 | 申请或审批记录不存在 |
| CONFLICT | 409 | 重复提交、重复审批、状态与审批步骤不匹配 |
| DORM_BLOCKED | 422 | 宿舍清退未完成 |

说明：登录接口当前对凭据错误返回 DRF serializer error 结构，不保证业务错误 envelope。全局异常 envelope 属于 Week 4+ 范围。

## 8. Deferred To Week 4

- 附件、草稿、审计轨迹、通知、微信 OAuth。
- 全量 OpenAPI schema。
- 全局 DRF 异常 envelope 统一。
- 完整权限排列组合测试矩阵。

exec
/bin/bash -lc "rtk sed -n '1,260p' miniprogram/pages/detail/detail.ts" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
import { createDefaultApiClient } from '../../services/api';
import type { ApplicationDetail } from '../../types/api';

const app = getApp<IAppOption>();
const apiClient = createDefaultApiClient();

Page({
  data: {
    detail: null as ApplicationDetail | null,
    loading: true,
    error: '',
    canApprove: false,
    statusText: '',
    decisionText: {
      pending: '待审批',
      approved: '已通过',
      rejected: '已拒绝',
    },
    applicationId: '',
    pendingApprovalId: '',
  },

  onLoad(options: any) {
    const userInfo = app.globalData.userInfo;
    if (!userInfo) {
      wx.reLaunch({ url: '/pages/login/login' });
      return;
    }

    const id = options.id;
    if (!id) {
      this.setData({ error: '缺少申请ID' });
      return;
    }

    this.setData({ applicationId: id });
    this.loadDetail();
  },

  async loadDetail() {
    this.setData({ loading: true, error: '' });

    try {
      const detail = await apiClient.getApplication(this.data.applicationId);

      const statusMap: Record<string, string> = {
        draft: '草稿',
        pending_counselor: '待辅导员审批',
        pending_dean: '待院长审批',
        approved: '已通过',
        rejected: '已拒绝',
      };

      const userInfo = app.globalData.userInfo!;
      const pendingApproval = detail.approvals.find(
        (a) => a.decision === 'pending' && a.approver_id === userInfo.user_id
      );

      this.setData({
        detail,
        statusText: statusMap[detail.status] || detail.status,
        canApprove: !!pendingApproval,
        pendingApprovalId: pendingApproval?.approval_id || '',
        loading: false,
      });
    } catch (err: any) {
      this.setData({
        error: err.error?.message || err.message || '加载失败',
        loading: false,
      });
    }
  },

  onApprove() {
    wx.showModal({
      title: '确认通过',
      content: '确定要通过此申请吗？',
      success: (res) => {
        if (res.confirm) {
          this.performAction('approve');
        }
      },
    });
  },

  onReject() {
    wx.showModal({
      title: '确认拒绝',
      content: '确定要拒绝此申请吗？',
      success: (res) => {
        if (res.confirm) {
          this.performAction('reject');
        }
      },
    });
  },

  async performAction(action: 'approve' | 'reject') {
    wx.showLoading({ title: '处理中...' });

    try {
      const approvalId = this.data.pendingApprovalId;

      if (action === 'approve') {
        await apiClient.approveApproval(approvalId, { comment: '' });
      } else {
        await apiClient.rejectApproval(approvalId, { comment: '' });
      }

      wx.hideLoading();
      wx.showToast({
        title: action === 'approve' ? '已通过' : '已拒绝',
        icon: 'success',
      });

      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
    } catch (err: any) {
      wx.hideLoading();
      wx.showToast({
        title: err.error?.message || err.message || '操作失败',
        icon: 'none',
      });
    }
  },

  onRetry() {
    this.loadDetail();
  },
});

exec
/bin/bash -lc "rtk sed -n '1,260p' miniprogram/pages/approvals/approvals.ts" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
import { createDefaultApiClient } from '../../services/api';
import type { ApprovalListItem } from '../../types/api';

const app = getApp<IAppOption>();
const apiClient = createDefaultApiClient();

Page({
  data: {
    approvals: [] as ApprovalListItem[],
    loading: true,
    error: '',
    userInfo: { name: '', role: '' },
    roleText: '',
  },

  onLoad() {
    const userInfo = app.globalData.userInfo;
    if (!userInfo) {
      wx.reLaunch({ url: '/pages/login/login' });
      return;
    }

    const roleMap: Record<string, string> = {
      student: '学生',
      counselor: '辅导员',
      dean: '院长',
    };

    this.setData({
      userInfo,
      roleText: roleMap[userInfo.role] || userInfo.role,
    });

    this.loadApprovals();
  },

  async loadApprovals() {
    this.setData({ loading: true, error: '' });

    try {
      const res = await apiClient.listApprovals('pending', 20, 0);
      this.setData({
        approvals: res.results,
        loading: false,
      });
    } catch (err: any) {
      this.setData({
        error: err.error?.message || err.message || '加载失败',
        loading: false,
      });
    }
  },

  onItemTap(e: any) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({ url: `/pages/detail/detail?id=${id}` });
  },

  onRetry() {
    this.loadApprovals();
  },
});

exec
/bin/bash -lc "rtk sed -n '1,220p' miniprogram/pages/login/login.wxss" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,220p' miniprogram/pages/login/login.wxml" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
<view class="container">
  <view class="header">
    <text class="title">毕业离校申请系统</text>
  </view>

  <view class="form">
    <view class="input-group">
      <text class="label">用户ID</text>
      <input class="input" placeholder="请输入用户ID" value="{{userId}}" bindinput="onUserIdInput" />
    </view>

    <view class="input-group">
      <text class="label">密码</text>
      <input class="input" type="password" placeholder="请输入密码" value="{{password}}" bindinput="onPasswordInput" />
    </view>

    <button class="login-btn" bindtap="onLogin" disabled="{{loading}}">
      {{loading ? '登录中...' : '登录'}}
    </button>

    <view class="error" wx:if="{{error}}">{{error}}</view>
  </view>
</view>

exec
/bin/bash -lc "rtk sed -n '1,220p' miniprogram/app.ts" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk rg -n "student-application|学生申请|Phase 4B|pages/student" docs miniprogram -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 129ms:
 succeeded in 135ms:
 succeeded in 156ms:
codex
现有代码里有一个比草案更关键的前置问题：登录页现在无论角色都跳到审批列表，而 `student-application` 还未注册。这会直接影响“学生登录后是否有上一页”和成功后的合理去向。
exec
/bin/bash -lc 'rtk rg -n "GET `/api/applications|listApplications|申请列表|Phase 4B|student-application|role" docs/discussions docs/PROJECT-SUMMARY.md -S' in /home/caohui/projects/graduation-leave-system
 exited 2 in 0ms:
/bin/bash: -c: line 1: unexpected EOF while looking for matching ``'

exec
/bin/bash -lc "rtk sed -n '840,955p' docs/PROJECT-SUMMARY.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
- ✓ 达成共识：Option E' - 验证优先 + 窄MVP

**共识要点：**
1. ✓ Validation-first over build-first
2. ✓ MVP = 最小可行路径 + 必要错误处理（非全覆盖）
3. ✓ React Native推迟到下阶段（需stakeholder确认）
4. ✓ 宿舍系统对接调研立即启动

**执行计划：**
- Phase 4A: DevTools验证（1-3天）- 阻塞门控
- Phase 4B: 窄小程序MVP（3-5天）- 4页面only
- Phase 4C: 附件MVP（2-4天）
- 并行轨道：宿舍系统对接调研

**MVP范围（Phase 4B）：**
- 4页面：login, student-application, approvals（共享）, detail（共享）
- 核心功能：登录、学生提交、列表、详情、辅导员/学工部审批
- 必要状态：loading, empty, validation error, auth error, conflict error
- 排除：独立辅导员/学工部页面集、草稿、完整附件UX、高级过滤、通知中心、审计时间线、React Native

**产出物：**
- `.omc/collaboration/artifacts/20260531-0435-claude-response-next-phase-strategy.md`（Claude挑战）
- `.omc/collaboration/artifacts/20260531-0425-codex-response-to-claude-next-phase-strategy.md`（Codex共识）
- `.omc/collaboration/artifacts/20260531-0440-week4-execution-plan-consensus.md`（执行计划）
- `.omc/collaboration/artifacts/20260531-0445-dorm-provider-discovery.md`（宿舍系统调研）

**外部依赖：**
- WeChat DevTools安装（Phase 4A阻塞）
- 宿舍系统联系人/文档/凭证（生产阻塞）

**Week 4准备工作（2026-05-30晚）：**

**Claude-Codex准备工作讨论：**
- ✓ Codex分析6个选项，推荐A+C+E bundle（低返工准备）
- ✓ Claude批判性审查：3个修改建议（立即修复、3独立文档、仅文档化）
- ✓ Codex接受修改并提出1个反修改（artifacts路径）
- ✓ 达成共识：立即修复陈旧引用 + 3聚焦文档 + 2.5h硬停

**共识要点：**
1. ✓ 立即修复：dorm_provider.py → providers.py（30秒）
2. ✓ 3独立文档（非单一元文档）：validation checklist, DevTools setup, skeleton gaps
3. ✓ 仅文档化gap（student-application注册、API client重复），不修复直到DevTools验证
4. ✓ 时间盒：目标2.0h，硬停2.5h

**执行结果：**
- ✓ 修复陈旧文件引用（providers.py）
- ✓ 创建Phase 4A验证清单（8个验证场景 + pass/fail字段 + 证据槽）
- ✓ 创建DevTools设置指南（9步安装/配置 + 5个常见问题）
- ✓ 创建骨架gap审计（现有结构 + 缺失部分 + 风险区域 + 阻塞项）

**产出物：**
- `.omc/collaboration/artifacts/20260531-0439-codex-week4-blocked-prep-analysis.md`（Codex分析）
- `.omc/collaboration/artifacts/20260530-2048-claude-response-codex-prep-analysis.md`（Claude批判）
- `.omc/collaboration/artifacts/20260530-2053-codex-response-to-claude-week4-prep.md`（Codex共识）
- `.omc/collaboration/artifacts/phase4a-validation-checklist.md`（验证清单）
- `.omc/collaboration/artifacts/phase4a-devtools-setup.md`（设置指南）
- `.omc/collaboration/artifacts/phase4b-skeleton-gaps.md`（gap审计）

**状态：**
- Phase 4A准备完成，等待DevTools可用
- Phase 4B实施计划已文档化
- 已识别gap但未修复（等待验证）

**Phase 4A准备文档修复（2026-05-31凌晨）：**

**Codex发现4个问题：**
- ✓ 陈旧测试账号（checklist使用错误凭证）
- ✓ 错误401场景（停止后端=网络失败，非401）
- ✓ 陈旧skeleton gaps（api.ts和types.ts已存在）
- ✓ 学生重定向bug（学生禁止访问审批列表）

**Claude-Codex共识：**
- ✓ Codex推荐Phase 4A准备修复pass（60-90分钟）
- ✓ Claude接受所有问题并提出执行计划
- ✓ Codex确认并提出2个修正（运行时验证、协作记账）
- ✓ 达成共识，立即执行

**执行结果：**
- ✓ Step 1: 验证当前状态（运行时支持）- 所有4个问题已验证
- ✓ Step 2: 修复验证清单（正确凭证、401场景、登录流程）
- ✓ Step 3: 修复skeleton gaps（反映现有文件、添加学生主页gap）
- ✓ Step 4: 创建宿舍系统利益相关者请求模板

**产出物：**
- `.omc/collaboration/artifacts/20260531-0325-step1-verification-results.md`（验证结果）
- `.omc/collaboration/artifacts/phase4a-validation-checklist.md`（已修复）
- `.omc/collaboration/artifacts/phase4b-skeleton-gaps.md`（已修复）
- `.omc/collaboration/artifacts/dorm-system-stakeholder-request.md`（利益相关者请求）

**状态：**
- Phase 4A准备文档已修复，可执行
- 等待WeChat DevTools可用（外部依赖）

**Phase 4B准备验证（2026-05-31凌晨）：**

**Codex建议：** 硬停止实现，可选30-45分钟只读验证

**验证结果：**
- ✓ api.ts和types.ts被所有页面实际使用（非仅存在）
- ✓ 页面注册正确（3个页面，student-application未注册）
- ⚠️ ApiClient配置重复（每个页面实例化自己的ApiClient）

**Phase 4B优化机会：**
1. 高优先级：实现student-application页面 + 基于角色的路由（修复已知gap）
2. 中优先级：集中化API客户端配置（减少重复）
3. 低优先级：优化409测试场景（提高验证精度）

**产出物：**
- `.omc/collaboration/artifacts/phase4b-prep-note.md`（Phase 4B准备笔记）

**状态：**
- Phase 4A和Phase 4B准备工作完成
- 硬停止：等待DevTools或宿舍系统输入
- 下一个门控：WeChat DevTools可用性

exec
/bin/bash -lc "rtk sed -n '1,220p' .omc/collaboration/artifacts/phase4b-prep-note.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Phase 4B Prep Note - Read-Only Verification

**Date:** 2026-05-31  
**Purpose:** Compact handoff note for Phase 4B implementation  
**Method:** Read-only verification (no code changes)  
**Time:** 30-45 minutes

---

## 1. Confirmed Miniprogram Architecture

### Page Registration

**app.json pages array:**
```json
{
  "pages": [
    "pages/login/login",
    "pages/approvals/approvals",
    "pages/detail/detail"
  ]
}
```

**Status:** 3 pages registered, student-application not registered (correct - page doesn't exist yet)

---

### API Client Usage

**All pages import shared ApiClient:**
- `miniprogram/pages/login/login.ts:5` - `import { ApiClient } from '../../services/api'`
- `miniprogram/pages/approvals/approvals.ts:6` - `import { ApiClient } from '../../services/api'`
- `miniprogram/pages/detail/detail.ts:6` - `import { ApiClient } from '../../services/api'`

**Duplication pattern (all 3 pages):**
```typescript
const apiClient = new ApiClient({
  baseUrl: 'http://localhost:8001',
  getToken: () => app.globalData.token,
  onUnauthorized: () => {
    wx.removeStorageSync('token');
    wx.removeStorageSync('userInfo');
    app.globalData.token = '';
    app.globalData.userInfo = null;
    wx.reLaunch({ url: '/pages/login/login' });
  }
});
```

**Finding:** Shared ApiClient class is used, but each page instantiates with duplicate config.

---

### Type Definitions Usage

**Imports verified:**
- `miniprogram/pages/approvals/approvals.ts` - `import type { ApprovalListItem } from '../../types/api'`
- `miniprogram/pages/detail/detail.ts` - `import type { ApplicationDetail } from '../../types/api'`

**Status:** Shared types are used. Login page doesn't import types (only uses inline types for login request/response).

---

## 2. Phase 4B Optimization Opportunities

### A. Centralize API Client Configuration

**Current state:** Each page duplicates `baseUrl`, `getToken`, and `onUnauthorized` config.

**Optimization:**
```typescript
// services/api.ts - add default client factory/config
export function createDefaultApiClient() {
  const app = getApp<IAppOption>();
  return new ApiClient({
    baseUrl: 'http://localhost:8001',
    getToken: () => app.globalData.token,
    onUnauthorized: () => {
      wx.removeStorageSync('token');
      wx.removeStorageSync('userInfo');
      app.globalData.token = '';
      app.globalData.userInfo = null;
      wx.reLaunch({ url: '/pages/login/login' });
    }
  });
}

// pages/*.ts - use default
import { createDefaultApiClient } from '../../services/api';
const apiClient = createDefaultApiClient();
```

**Benefit:** Single source of truth for baseUrl and auth handling. Easier to update for production.

**Risk:** Low. Existing pattern works, this is pure refactor.

---

### B. Role-Based Post-Login Routing

**Current state:** All roles redirect to `/pages/approvals/approvals` after login (line 51 in login.ts).

**Problem:** Students hit 403 on approvals page (known Phase 4B gap).

**Optimization:**
```typescript
// After login success
const user = response.data.user;
if (user.role === 'student') {
  wx.redirectTo({ url: '/pages/student-application/student-application' });
} else {
  wx.redirectTo({ url: '/pages/approvals/approvals' });
}
```

**Prerequisite:** Student application page must exist first.

**Priority:** High - fixes known gap.

---

### C. Add Student Page Route Only When Implemented

**Current state:** student-application page not registered in app.json (correct).

**Action for Phase 4B:**
1. Implement student-application page files
2. Register in app.json
3. Update login redirect logic (see B above)

**Order matters:** Register page AFTER implementation, not before.

---

## 3. Checklist Sharp Edges

### 409 Conflict Scenario Precision

**Checklist scenario (lines 122-139):**
```
Test steps:
1. Login as counselor
2. Approve an application
3. Try to approve same application again (triggers 409)
```

**Sharp edge:** Step 3 "try to approve same application again" may be blocked by UI state.

**Potential issues:**
- Approval list may remove approved items immediately
- Detail page may disable approve button after first click
- Need to refresh or navigate back to trigger second approval attempt

**Recommendation for Phase 4A validation:**
- After step 2, explicitly refresh approval list or navigate away and back
- Or manually trigger API call via DevTools console
- Document exact steps that successfully trigger 409

**Alternative test:**
- Two counselors approve same application simultaneously (race condition)
- Requires two DevTools instances or coordination

---

## Summary

**Architecture verified:**
- ✅ Shared api.ts and types.ts are actually used by all pages
- ⚠️ ApiClient config duplicated across pages (low-priority refactor opportunity)
- ✅ Page registration correct (3 pages, student-application not registered)

**Phase 4B priorities:**
1. **High:** Implement student-application page + role-based routing (fixes known gap)
2. **Medium:** Centralize API client config (reduces duplication)
3. **Low:** Refine 409 test scenario (improve validation precision)

**No code changes made.** This is read-only verification only.

---

**Status:** Phase 4B prep note complete  
**Next gate:** WeChat DevTools availability for Phase 4A validation

exec
/bin/bash -lc 'rtk rg -n "GET /api/applications|listApplications|申请列表|student-application|role-based|学生重定向|学生主页" docs/discussions docs/PROJECT-SUMMARY.md -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/PROJECT-SUMMARY.md:227:  - 移除GET /api/applications列表端点（统一为5个HTTP路由）
docs/PROJECT-SUMMARY.md:269:  - GET /api/applications/{id}（查询申请）
docs/PROJECT-SUMMARY.md:457:  - 实现GET /api/applications/?status=过滤功能
docs/PROJECT-SUMMARY.md:771:- ✓ 前端/小程序类型对齐：登录`token_type`、用户`class_id`、申请列表字段、分页去除`next/previous`
docs/PROJECT-SUMMARY.md:855:- 4页面：login, student-application, approvals（共享）, detail（共享）
docs/PROJECT-SUMMARY.md:881:3. ✓ 仅文档化gap（student-application注册、API client重复），不修复直到DevTools验证
docs/PROJECT-SUMMARY.md:909:- ✓ 学生重定向bug（学生禁止访问审批列表）
docs/PROJECT-SUMMARY.md:920:- ✓ Step 3: 修复skeleton gaps（反映现有文件、添加学生主页gap）
docs/PROJECT-SUMMARY.md:939:- ✓ 页面注册正确（3个页面，student-application未注册）
docs/PROJECT-SUMMARY.md:943:1. 高优先级：实现student-application页面 + 基于角色的路由（修复已知gap）
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:42:2. `GET /api/applications/` (PRIORITY 2)
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:81:5. List endpoints respect role-based filtering
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:155:**Issue 2:** Dean detail endpoint (`GET /api/applications/{id}`) has no restrictions - falls through to return any application.
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:167:**Action:** Create separate list serializer without nested approvals for `GET /api/applications/`.
docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:24:### 2. GET /api/applications/ 权限
docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:46:**问题:** 当前GET /api/applications/{id}/对Dean放行所有申请  
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:12:1. `GET /api/applications/` - 申请列表
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:24:### 2.1 GET /api/applications/
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:31:- 学生: 返回自己的申请列表
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:32:- 辅导员: 返回所负责班级学生的申请列表
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:33:- 学工部: 返回所有申请列表
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:169:5. **辅导员查询申请列表的范围?**
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:118:2. `GET /api/applications/` (PRIORITY 2)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:152:5. List endpoints respect role-based filtering
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:222:1. Start with role-based queryset filtering (not parameter filtering)
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:94:### 3.2 GET /api/applications/ (PRIORITY 2)
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:68:- `GET /api/applications/`: "Dean: all applications"
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:136:2. `GET /api/applications/` (priority 2)
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:163:**Mitigation:** Start with role-based queryset filtering, not parameter filtering.
docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:14:1. `GET /api/applications/` - List applications
docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:27:3. Add permission checks (role-based filtering)
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:455:- 申请列表：P95/QPS
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:463:设计中缓存申请详情、申请状态、学生申请列表。对含个人信息和审批信息的数据，必须保证：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:475:- 学生申请列表
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:63:- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:127:- `GET /api/applications/`根据当前登录用户角色自动过滤，不依赖`role`查询参数授权。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:102:6. **list接口契约风险。** 之前契约修复曾移除 `GET /api/applications` 列表端点；Day 2 共识又把列表接口作为正式 Go 门槛。执行前需要确认这不是契约回退。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:26:- 从contract-v0.1.md移除Section 4.4 GET /api/applications（列表端点）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:30:  3. GET /api/applications/{id}
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:151:- 查看本年级学生的申请列表
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:159:- 查看负责班级学生的申请列表
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:149:- 辅导员列表：GET /api/applications/?role=counselor
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:150:- 学工部列表：GET /api/applications/?role=dean
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:36:3. `GET /api/applications/{application_id}`
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:40:列表端点 `GET /api/applications` 已不在契约中。移除列表端点是合理的，因为v0.1纵向切片只需要“登录 -> 提交 -> 审批 -> 查询单个申请”，不需要审批队列或学生申请列表。
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:65:- 辅导员列表：GET /api/applications/?role=counselor
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:66:- 学工部列表：GET /api/applications/?role=dean
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:18:- 删除Section 4.4 GET /api/applications（列表端点）
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:308:1. GET /api/applications/
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:316:# 期望：返回T002待审批的申请列表
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:112:- 实现：GET /api/applications/
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:370:- 实现：GET /api/applications/

exec
/bin/bash -lc "rtk nl -ba miniprogram/pages/login/login.ts | rtk sed -n '1,80p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	import { createDefaultApiClient } from '../../services/api';
     2	
     3	const app = getApp<IAppOption>();
     4	const apiClient = createDefaultApiClient();
     5	
     6	Page({
     7	  data: {
     8	    userId: '',
     9	    password: '',
    10	    loading: false,
    11	    error: '',
    12	  },
    13	
    14	  onUserIdInput(e: any) {
    15	    this.setData({ userId: e.detail.value });
    16	  },
    17	
    18	  onPasswordInput(e: any) {
    19	    this.setData({ password: e.detail.value });
    20	  },
    21	
    22	  async onLogin() {
    23	    const { userId, password } = this.data;
    24	
    25	    if (!userId || !password) {
    26	      this.setData({ error: '请输入用户ID和密码' });
    27	      return;
    28	    }
    29	
    30	    this.setData({ loading: true, error: '' });
    31	
    32	    try {
    33	      const res = await apiClient.login({ user_id: userId, password });
    34	
    35	      wx.setStorageSync('token', res.access_token);
    36	      wx.setStorageSync('userInfo', res.user);
    37	      app.globalData.token = res.access_token;
    38	      app.globalData.userInfo = res.user;
    39	
    40	      wx.redirectTo({ url: '/pages/approvals/approvals' });
    41	    } catch (err: any) {
    42	      this.setData({
    43	        error: err.error?.message || err.message || '登录失败',
    44	        loading: false,
    45	      });
    46	    }
    47	  },
    48	});

exec
/bin/bash -lc "rtk nl -ba miniprogram/app.json | rtk sed -n '1,30p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	{
     2	  "pages": [
     3	    "pages/login/login",
     4	    "pages/approvals/approvals",
     5	    "pages/detail/detail"
     6	  ],
     7	  "window": {
     8	    "navigationBarTitleText": "毕业离校申请系统",
     9	    "navigationBarBackgroundColor": "#1890ff",
    10	    "navigationBarTextStyle": "white",
    11	    "backgroundColor": "#f5f5f5"
    12	  },
    13	  "sitemapLocation": "sitemap.json"
    14	}

exec
/bin/bash -lc "rtk nl -ba docs/contracts/contract-v0.2.md | rtk sed -n '130,245p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   130	- 已处于 `pending_counselor`、`pending_dean`、`approved` 的申请会阻断重复提交。
   131	
   132	## 5. 权限矩阵
   133	
   134	| 操作 | student | counselor | dean |
   135	| --- | --- | --- | --- |
   136	| 登录 | 自己账号 | 自己账号 | 自己账号 |
   137	| 提交申请 | 允许 | 禁止 | 禁止 |
   138	| 申请列表 | 仅本人申请 | 仅本人待处理 counselor 审批对应申请 | 仅本人待处理 dean 审批对应申请 |
   139	| 申请详情 | 仅本人申请 | 仅负责班级申请 | 仅本人待处理 dean 审批对应申请 |
   140	| 审批列表 | 禁止 | 仅本人 counselor 审批 | 仅本人 dean 审批 |
   141	| counselor 审批动作 | 禁止 | 仅指定 approver | 禁止 |
   142	| dean 审批动作 | 禁止 | 禁止 | 仅指定 approver |
   143	
   144	## 6. 端点
   145	
   146	### POST `/api/auth/login`
   147	
   148	请求：
   149	
   150	```json
   151	{"user_id":"2020001","password":"2020001"}
   152	```
   153	
   154	响应：
   155	
   156	```json
   157	{
   158	  "access_token": "<jwt>",
   159	  "token_type": "Bearer",
   160	  "user": {
   161	    "user_id": "2020001",
   162	    "name": "张三",
   163	    "role": "student",
   164	    "class_id": "CS2020-01"
   165	  }
   166	}
   167	```
   168	
   169	### POST `/api/applications/`
   170	
   171	请求：
   172	
   173	```json
   174	{"reason":"毕业离校","leave_date":"2024-06-30"}
   175	```
   176	
   177	响应：`201 ApplicationDetail`。
   178	
   179	### GET `/api/applications/?limit=20&offset=0`
   180	
   181	响应：`PaginatedResponse<ApplicationListItem>`。
   182	
   183	### GET `/api/applications/{application_id}/`
   184	
   185	响应：`ApplicationDetail`。
   186	
   187	### GET `/api/approvals/?decision=pending&limit=20&offset=0`
   188	
   189	`decision` 可取 `pending | approved | rejected | all`，默认 `pending`。
   190	
   191	响应：`PaginatedResponse<ApprovalListItem>`。
   192	
   193	### POST `/api/approvals/{approval_id}/approve/`
   194	
   195	请求：
   196	
   197	```json
   198	{"comment":"同意"}
   199	```
   200	
   201	响应：`200 ApprovalDetail`。
   202	
   203	### POST `/api/approvals/{approval_id}/reject/`
   204	
   205	请求：
   206	
   207	```json
   208	{"comment":"材料不齐全"}
   209	```
   210	
   211	响应：`200 ApprovalDetail`。
   212	
   213	## 7. 错误响应
   214	
   215	业务错误统一使用：
   216	
   217	```json
   218	{
   219	  "error": {
   220	    "code": "CONFLICT",
   221	    "message": "申请已存在，不能重复提交",
   222	    "details": {
   223	      "student_id": "2020001",
   224	      "existing_application_id": "app_eb41d2f5"
   225	    }
   226	  }
   227	}
   228	```
   229	
   230	当前 Week 3 核心错误码：
   231	
   232	| code | HTTP | 场景 |
   233	| --- | --- | --- |
   234	| VALIDATION_ERROR | 400 | 申请提交字段缺失或格式错误 |
   235	| FORBIDDEN | 403 | 角色不符、非指定审批人、越权访问 |
   236	| NOT_FOUND | 404 | 申请或审批记录不存在 |
   237	| CONFLICT | 409 | 重复提交、重复审批、状态与审批步骤不匹配 |
   238	| DORM_BLOCKED | 422 | 宿舍清退未完成 |
   239	
   240	说明：登录接口当前对凭据错误返回 DRF serializer error 结构，不保证业务错误 envelope。全局异常 envelope 属于 Week 4+ 范围。
   241	
   242	## 8. Deferred To Week 4
   243	
   244	- 附件、草稿、审计轨迹、通知、微信 OAuth。
   245	- 全量 OpenAPI schema。

exec
/bin/bash -lc "rtk nl -ba miniprogram/services/api.ts | rtk sed -n '60,145p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    60	        },
    61	        fail: (err) => {
    62	          reject(new Error(err.errMsg));
    63	        },
    64	      });
    65	    });
    66	  }
    67	
    68	  async login(req: LoginRequest): Promise<LoginResponse> {
    69	    return this.request('/api/auth/login', {
    70	      method: 'POST',
    71	      data: req,
    72	    });
    73	  }
    74	
    75	  async createApplication(req: ApplicationCreateRequest): Promise<ApplicationDetail> {
    76	    return this.request('/api/applications/', {
    77	      method: 'POST',
    78	      data: req,
    79	    });
    80	  }
    81	
    82	  async listApplications(
    83	    limit = 20,
    84	    offset = 0
    85	  ): Promise<PaginatedResponse<Application>> {
    86	    return this.request(
    87	      `/api/applications/?limit=${limit}&offset=${offset}`
    88	    );
    89	  }
    90	
    91	  async getApplication(id: string): Promise<ApplicationDetail> {
    92	    return this.request(`/api/applications/${id}/`);
    93	  }
    94	
    95	  async listApprovals(
    96	    decision: 'pending' | 'approved' | 'rejected' | 'all' = 'pending',
    97	    limit = 20,
    98	    offset = 0
    99	  ): Promise<PaginatedResponse<ApprovalListItem>> {
   100	    return this.request(
   101	      `/api/approvals/?decision=${decision}&limit=${limit}&offset=${offset}`
   102	    );
   103	  }
   104	
   105	  async approveApproval(
   106	    id: string,
   107	    req: ApprovalActionRequest
   108	  ): Promise<ApprovalActionResponse> {
   109	    return this.request(`/api/approvals/${id}/approve/`, {
   110	      method: 'POST',
   111	      data: req,
   112	    });
   113	  }
   114	
   115	  async rejectApproval(
   116	    id: string,
   117	    req: ApprovalActionRequest
   118	  ): Promise<ApprovalActionResponse> {
   119	    return this.request(`/api/approvals/${id}/reject/`, {
   120	      method: 'POST',
   121	      data: req,
   122	    });
   123	  }
   124	}
   125	
   126	export function createDefaultApiClient(): ApiClient {
   127	  const app = getApp<IAppOption>();
   128	  return new ApiClient({
   129	    baseUrl: 'http://localhost:8001',
   130	    getToken: () => app.globalData.token,
   131	    onUnauthorized: () => {
   132	      wx.removeStorageSync('token');
   133	      wx.removeStorageSync('userInfo');
   134	      app.globalData.token = '';
   135	      app.globalData.userInfo = null;
   136	      wx.reLaunch({ url: '/pages/login/login' });
   137	    }
   138	  });
   139	}

codex
**审查结论：需要小幅调整后再实施。** 草案方向基本合理，但成功跳转和登录路由不能按当前设想走，否则学生提交链路仍不闭环。

**主要问题**

1. **成功后停留当前页不是最佳方案。**  
   `createApplication()` 返回 `ApplicationDetail`，包含 `application_id`，现有详情页也已支持 `GET /api/applications/{id}/`。因此成功后应优先跳转到详情页：  
   `wx.redirectTo({ url: \`/pages/detail/detail?id=${res.application_id}\` })`  
   这比清空表单更合理，因为重复提交本来会触发 409，保留“继续提交”的入口反而制造无效操作。

2. **必须同时修复登录后的角色路由。**  
   当前 [login.ts](/home/caohui/projects/graduation-leave-system/miniprogram/pages/login/login.ts:40) 固定跳到 `/pages/approvals/approvals`，但契约规定学生禁止访问审批列表。实现 `student-application` 时应一起改成：学生跳申请页，辅导员/院长跳审批页。

3. **页面注册是必需项。**  
   [app.json](/home/caohui/projects/graduation-leave-system/miniprogram/app.json:2) 当前只注册了 login、approvals、detail。新页面实现后必须加入：
   `pages/student-application/student-application`

4. **页面自身也要做角色保护。**  
   不能只依赖登录跳转。`student-application.onLoad` 应检查 `userInfo`：未登录 `reLaunch` 到登录页；非 `student` 建议 `redirectTo` 到审批页或显示无权限。否则手动进入页面会到提交时才暴露 403。

**5 个关键问题判断**

1. **成功跳转目标：选 A，不选 C。**  
   跳详情页最符合现有页面结构和 API 返回值。C 会让用户留在一个已无有效后续动作的表单页。

2. **错误处理：不需要为每种错误做复杂 UI，但需要按 code 做文案增强。**  
   建议实现一个 `formatApplicationError(err)`：
   - `DORM_BLOCKED`：优先显示 `blocking_reason`，否则显示“宿舍清退未完成，暂不能提交”
   - `CONFLICT`：显示“已有待审批/已通过申请”，若有 `existing_application_id` 可给“查看申请”入口或直接跳详情
   - `VALIDATION_ERROR`：显示字段校验摘要
   - `FORBIDDEN`：显示“当前账号无提交权限”
   - fallback：`err.error?.message || err.message || '提交失败'`

3. **验证时机：提交时验证合理。**  
   但要补两个细节：`reason.trim()` 后再校验和提交；提交中防重复点击，`loading` 为 true 时直接 return。

4. **日期默认值：空值合理。**  
   但建议设置 `picker` 的 `start` 为今天，避免误选过去日期。默认空值 + 显式选择，比自动填今天更不容易误提交。

5. **loading：按钮 disabled 足够。**  
   不需要全屏遮罩。提交接口是单点动作，按钮态即可。失败后必须恢复 `loading=false`；成功跳转前也可以不恢复。

**建议最终方案**

- 新增 `student-application` 四个页面文件。
- `app.json` 注册新页面。
- `login.ts` 改为基于 `res.user.role` 跳转。
- `student-application.ts` 使用 `createDefaultApiClient()`。
- 成功后 `showToast`，短延迟或直接 `redirectTo` 到详情页。
- 错误用统一 formatter，针对 `DORM_BLOCKED`、`CONFLICT`、`VALIDATION_ERROR` 做轻量定制。
- 不做草稿保存。契约已把草稿、附件、通知等放到 Week 4+，现在加入草稿会扩大范围且与“单 active 申请”模型冲突。

总体上，这个页面应定位为“学生提交入口”，不是申请管理页。提交成功后的主体验证点应该落到详情页，而不是停留在表单页。
tokens used
37,802

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
