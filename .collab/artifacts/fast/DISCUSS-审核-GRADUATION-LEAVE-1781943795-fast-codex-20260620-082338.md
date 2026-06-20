我会先梳理仓库结构和本次变更范围，再逐项审查脚本、compose、迁移与启动路径，最后给出风险清单和修复建议。先建立审查 TODO：锁定差异、检查脚本安全、验证迁移幂等、审查 compose/env 配置、汇总风险。我现在无法访问仓库文件或运行终端命令，因此不能对 `graduation-leave-system v0.4.0` 的实际变更做可靠审核。请提供以下任一信息，我就能继续逐项审查：

- `git diff v0.3.0..v0.4.0` 或本次 PR diff
- 相关文件内容：`docker-compose*.yml`、部署脚本、migration 脚本、`Dockerfile`、启动命令/entrypoint、环境变量模板
- 或允许我访问当前工作区的 shell/tool 输出

收到后我会按你指定的 5 点输出审查结论：脚本安全可靠性、migration 幂等性、`env_file` 绝对路径、migrate 与启动分离正确性、潜在风险与修复建议。