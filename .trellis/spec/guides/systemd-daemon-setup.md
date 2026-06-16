# systemd User Service 守护进程配置指南

> **Purpose**: systemd用户级服务配置最佳实践，确保服务自动重启、开机启动和故障告警。

---

## 何时使用

- 需要长期运行的用户级服务（HTTP服务器、后台任务）
- 服务崩溃时需要自动重启
- 系统重启后需要自动启动（无需登录）
- 需要标准化的日志和监控

---

## 基础配置模板

**位置**: `~/.config/systemd/user/<service-name>.service`

```ini
[Unit]
Description=<服务描述>
After=network.target

[Service]
Type=simple
WorkingDirectory=<工作目录>
ExecStart=<启动命令>
Restart=always
RestartSec=10s
StartLimitBurst=5
StartLimitIntervalSec=300
StandardOutput=journal
StandardError=journal
OnFailure=alert-<service-name>.service

[Install]
WantedBy=default.target
```

---

## 关键配置项说明

### 自动重启策略

```ini
Restart=always              # 任何退出状态都重启
RestartSec=10s             # 失败后等待10秒再重启
StartLimitBurst=5          # 5分钟内最多重启5次
StartLimitIntervalSec=300  # 限制统计间隔
```

**避坑点**:
- `Restart=on-failure` 只在非零退出时重启，可能漏掉kill信号导致的崩溃
- `RestartSec` 太短会导致快速失败循环，太长影响恢复速度（推荐10-30s）

### 日志配置

```ini
StandardOutput=journal
StandardError=journal
```

查看日志:
```bash
journalctl --user -u <service-name> -f     # 实时查看
journalctl --user -u <service-name> --since "1 hour ago"  # 最近1小时
```

### 开机自启（登出后持续运行）

```bash
# 1. 启用服务
systemctl --user enable <service-name>

# 2. 允许用户服务在登出后继续运行
loginctl enable-linger $USER
```

**避坑点**: 忘记 `enable-linger` 会导致登出后服务停止。

---

## 告警机制

### 创建告警服务

**位置**: `~/.config/systemd/user/alert-<service-name>.service`

```ini
[Unit]
Description=Alert for <service-name> failures

[Service]
Type=oneshot
ExecStart=/home/<user>/.local/bin/alert-<service-name>.sh
```

### 告警脚本示例

**位置**: `~/.local/bin/alert-<service-name>.sh` (chmod +x)

```bash
#!/bin/bash
LOG_FILE="/tmp/<service-name>-alerts.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Service <service-name> failed" >> "$LOG_FILE"
systemctl --user status <service-name> >> "$LOG_FILE" 2>&1
journalctl --user -u <service-name> -n 10 >> "$LOG_FILE" 2>&1
echo "---" >> "$LOG_FILE"
```

**触发条件**: 服务达到 `StartLimitBurst` 限制时触发。

---

## 常用管理命令

```bash
# 加载配置（修改service文件后）
systemctl --user daemon-reload

# 启动/停止/重启
systemctl --user start <service-name>
systemctl --user stop <service-name>
systemctl --user restart <service-name>

# 查看状态
systemctl --user status <service-name>

# 查看日志
journalctl --user -u <service-name> -f

# 从启动限制中恢复
systemctl --user reset-failed <service-name>
systemctl --user start <service-name>

# 查看告警日志
cat /tmp/<service-name>-alerts.log
```

---

## 零停机迁移流程

从手动启动或system服务迁移到user服务:

```bash
# 1. 创建user service文件
mkdir -p ~/.config/systemd/user
vim ~/.config/systemd/user/<service-name>.service

# 2. 启动新服务（旧服务继续运行）
systemctl --user daemon-reload
systemctl --user start <service-name>

# 3. 验证新服务运行正常
systemctl --user status <service-name>
curl http://localhost:<port>  # 验证可访问

# 4. 停止旧服务
kill <old-pid>
# 或: sudo systemctl stop <old-system-service>

# 5. 启用开机自启
systemctl --user enable <service-name>
loginctl enable-linger $USER

# 6. 禁用旧system服务（可选，保留作为备份）
# sudo systemctl disable <old-system-service>
```

---

## 验证检查清单

部署后验证:

- [ ] 服务状态: `systemctl --user status <service-name>` 显示 `active (running)`
- [ ] 自启配置: `systemctl --user is-enabled <service-name>` 显示 `enabled`
- [ ] HTTP可访问: `curl http://localhost:<port>` 返回200
- [ ] 自动重启测试: `kill <pid>` 后10秒内服务恢复
- [ ] 日志可查看: `journalctl --user -u <service-name>` 有输出
- [ ] 告警脚本可执行: `ls -l ~/.local/bin/alert-<service-name>.sh` 有 `x` 权限
- [ ] Linger已启用: `loginctl show-user $USER | grep Linger` 显示 `Linger=yes`

---

## 案例: 毕业离校系统前端服务

**需求**: demo-web前端服务（port 7788）需要守护进程保证业务连续性。

**实施**:
- User service: `~/.config/systemd/user/graduation-frontend.service`
- 告警服务: `~/.config/systemd/user/alert-graduation-frontend.service`
- 告警脚本: `~/.local/bin/alert-graduation-frontend.sh`
- 告警日志: `/tmp/graduation-frontend-alerts.log`

**关键决策**:
- 使用 `scripts/serve-frontend.py` (ThreadingHTTPServer) 替代 `python3 -m http.server`，防止slow-client hang问题
- 从system-level迁移到user-level，避免sudo依赖
- 保留旧system服务作为备份，禁用但不删除

**验证结果**: 所有检查项通过，包括自动重启测试和HTTP可访问性验证。

---

## 参考资料

- systemd官方文档: https://www.freedesktop.org/software/systemd/man/systemd.service.html
- 本项目实施: `.trellis/tasks/06-16-frontend-daemon-setup/`
- 运维文档: `PROJECT-QUICK-REF.md` lines 66-89

---

**Last Updated**: 2026-06-16  
**Source Task**: `.trellis/tasks/06-16-frontend-daemon-setup`
