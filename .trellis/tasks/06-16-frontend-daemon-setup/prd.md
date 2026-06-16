# 为毕业离校系统前端服务配置守护进程保证业务连续性

## Goal

为毕业离校系统前端服务（demo-web on port 7788）配置守护进程机制，确保系统重启、进程崩溃时服务自动恢复，保证业务连续性。同时建立监控、日志和告警机制。

## Current State

**前端服务**:
- 路径: `/home/caohui/projects/graduation-leave-system/demo-web`
- 当前运行: `python3 -m http.server 7788` (PID 1778253, 手动启动)
- 端口: 7788
- 访问: http://218.75.196.218:7788
- 问题: 无守护进程，系统重启/崩溃后不会自动启动

**后端/数据库**:
- Docker容器，restart policy: always
- 已保证自动重启

## Requirements

### 1. 守护进程配置
- [ ] 创建 systemd user service: `graduation-frontend.service`
- [ ] 配置自动启动：`systemctl --user enable graduation-frontend`
- [ ] 配置自动重启：`Restart=always`
- [ ] 重启策略：
  - `RestartSec=10s` - 失败后等10秒重启
  - `StartLimitBurst=5` - 5分钟内最多重启5次
  - `StartLimitIntervalSec=300` - 统计间隔5分钟

### 2. 日志管理
- [ ] 配置服务日志通过 systemd journal 记录
- [ ] 日志轮转：每天轮转，保留最近7天
- [ ] 可通过 `journalctl --user -u graduation-frontend` 查看
- [ ] 日志级别：info（标准输出）+ error（标准错误）

### 3. 监控机制
- [ ] 依赖 systemd 自动重启机制（无需额外监控脚本）
- [ ] 通过 `systemctl --user status graduation-frontend` 查看服务状态
- [ ] 通过 `journalctl --user -u graduation-frontend` 查看运行日志

### 4. 告警机制
- [ ] 服务故障时写入告警日志
- [ ] 告警方式：写入专用告警日志文件 `/tmp/graduation-frontend-alerts.log`
- [ ] 告警阈值配置（连续失败N次才告警）
- [ ] 告警日志包含：时间戳、故障类型、服务状态

## Acceptance Criteria

- [ ] systemd service 文件创建并启用
- [ ] 服务可通过 `systemctl --user status/start/stop/restart` 管理
- [ ] 系统重启后前端服务自动启动并可访问
- [ ] 手动 kill 前端进程后10秒内自动重启
- [ ] 日志文件正确记录服务输出，可通过 `journalctl --user -u <service>` 查看
- [ ] 监控脚本运行并记录服务状态
- [ ] 测试：模拟服务崩溃和系统重启，验证自动恢复
- [ ] 文档：更新 PROJECT-QUICK-REF.md 记录守护进程配置

## Constraints

- **不能中断现有服务**: 配置过程中前端服务必须保持运行
- **最小侵入**: 不修改前端代码，仅配置基础设施
- **用户权限**: 使用 systemd --user（无需 sudo）

## Notes

这是一个复杂任务，需要：
- `design.md`: 技术方案设计（systemd配置、监控架构、告警方案）
- `implement.md`: 执行计划（分步骤实施、回滚点、验证命令）
