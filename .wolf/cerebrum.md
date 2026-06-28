# Cerebrum

> OpenWolf's learning memory. Updated automatically as the AI learns from interactions.
> Do not edit manually unless correcting an error.
> Last updated: 2026-06-11

## User Preferences

- **[2026-06-28] 业务流程测试使用 browser-harness**: 代码完成后，如需要进行业务流程测试（如登录、表单提交、页面跳转等），使用 browser-harness 技能进行自动化测试，而非手动操作或仅依赖单元测试。
  - 优势: 真实浏览器环境、发现生产环境问题（如本次发现HTTP/HTTPS cookies配置问题）
  - 调用: `BU_CDP_URL=http://127.0.0.1:9222 browser-harness <<'PY' ... PY` 或 `/browser-harness`
  
- **[2026-06-27] 速查方法论（懒加载）**: 遇到错误时触发加载速查文档
  - 触发条件: 命令失败、数据库错误、服务启动失败、Django/Python执行错误、用户询问环境配置
  - 核心文档: `PROJECT-QUICKREF.md` (综合), `docs/环境执行规范速查.md` (执行规范), `docs/数据速查.md` (数据导入)
  - 懒加载配置: `.claude/rules/quickref-rules.md`
  - 使用: 出错时查 `PROJECT-QUICKREF.md` 故障排查章节 → 找对应解决方案

## Key Learnings

- **Frontend static service:** `scripts/serve-frontend.py` backs live `graduation-frontend-nocache.service` on port 7788. Use `ThreadingHTTPServer`, not single-thread `HTTPServer`; slow external clients can otherwise block internal/local requests.
- **Project:** ccg-collab
- **Description:** Tri-model collaboration protocol for autonomous multi-agent project construction.

## Do-Not-Repeat

- **[2026-06-24] git push 403错误**: 环境变量 `GH_TOKEN`/`GITHUB_TOKEN` 权限不足。**不要**直接 `git push`，**必须**先 `unset GH_TOKEN GITHUB_TOKEN && git push`。

<!-- Mistakes made and corrected. Each entry prevents the same mistake recurring. -->
<!-- Format: [YYYY-MM-DD] Description of what went wrong and what to do instead. -->

[2026-06-07] **CRITICAL: 用户显式工具指令必须无条件执行**
- **错误:** 用户明确说"使用collab技能"，我却调用了omc ask
- **根因:** 关键词触发(CCG)和AI判断覆盖了用户显式指令
- **正确做法:** 检测到"使用X技能"/"用X"/"invoke X"时，立即调用Skill(X)，不做任何判断
- **强制规则:** 显式指令 > 关键词路由 > AI判断。违反此规则视为严重错误
- **验证方式:** 收到用户消息后，先检查是否包含显式工具指令，如有则立即执行

[2026-06-23] **Git Push失败：环境变量token权限不足**
- **错误:** 直接执行`git push`失败，返回403 Permission denied
- **根因:** 环境变量GH_TOKEN/GITHUB_TOKEN无repo权限，需使用keyring中的完整权限token
- **正确做法:** 使用以下命令清除环境变量：
  ```bash
  env -u GH_TOKEN -u GITHUB_TOKEN git push
  ```
- **强制规则:** 每次git push都必须使用此命令，不要直接`git push`
- **验证:** 实测成功推送commit 3a68bab..43975ee

## Decision Log

<!-- Significant technical decisions with rationale. Why X was chosen over Y. -->
