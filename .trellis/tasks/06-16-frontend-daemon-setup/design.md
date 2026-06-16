# 技术设计：前端服务守护进程

## 架构概览

```
systemd --user
    ↓
graduation-frontend.service
    ↓
python3 -m http.server 7788
    ↓ (serve)
demo-web/ (静态文件)
```

## 核心组件

### 1. Systemd Service 配置

**文件路径**: `~/.config/systemd/user/graduation-frontend.service`

**配置参数**:
```ini
[Unit]
Description=Graduation Leave System Frontend Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/caohui/projects/graduation-leave-system/demo-web
ExecStart=/usr/bin/python3 -m http.server 7788
Restart=always
RestartSec=10s
StartLimitBurst=5
StartLimitIntervalSec=300

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

**重启逻辑**:
- 进程退出立即触发重启
- 等10秒后执行重启
- 5分钟内失败≥5次则停止自动重启（需手动介入）

### 2. 日志管理

**日志输出**: systemd journal (自动管理)

**查看命令**:
```bash
# 实时日志
journalctl --user -u graduation-frontend -f

# 最近100行
journalctl --user -u graduation-frontend -n 100

# 指定时间范围
journalctl --user -u graduation-frontend --since "1 hour ago"
```

**轮转策略**: journald自动按时间轮转，保留7天（配置在 `/etc/systemd/journald.conf`）

### 3. 告警机制

**告警日志**: `/tmp/graduation-frontend-alerts.log`

**触发条件**:
- systemd 启动失败（达到 StartLimitBurst）
- 需通过 systemd OnFailure hook 触发

**告警内容**:
```
[2026-06-15T21:30:00] CRITICAL: graduation-frontend service failed to start after 5 attempts
[2026-06-15T21:30:00] Status: failed | ExitCode: 1 | RestartCount: 5
```

**实现方式**: 创建告警脚本 + systemd OnFailure directive

## 服务管理命令

```bash
# 启动服务
systemctl --user start graduation-frontend

# 停止服务
systemctl --user stop graduation-frontend

# 重启服务
systemctl --user restart graduation-frontend

# 查看状态
systemctl --user status graduation-frontend

# 启用自动启动
systemctl --user enable graduation-frontend

# 禁用自动启动
systemctl --user disable graduation-frontend

# 重载配置
systemctl --user daemon-reload
```

## 部署策略（零停机）

### 阶段1：创建服务配置（不启用）
1. 创建 service 文件
2. `systemctl --user daemon-reload`
3. 验证配置：`systemctl --user cat graduation-frontend`

### 阶段2：告警脚本部署
1. 创建告警脚本 `/home/caohui/.local/bin/alert-graduation-frontend.sh`
2. 添加执行权限
3. 更新 service 文件添加 `OnFailure=` directive

### 阶段3：切换到 systemd 管理（无缝）
1. 验证当前进程运行中（PID 1778253）
2. `systemctl --user start graduation-frontend`（新进程）
3. 验证新进程正常（HTTP 200 on 7788）
4. `kill 1778253`（停止旧进程）
5. `systemctl --user enable graduation-frontend`（开机自启）

### 阶段4：验证自动重启
1. 手动 kill 进程：`systemctl --user status graduation-frontend | grep "Main PID" | awk '{print $3}' | xargs kill`
2. 等待10秒
3. 验证服务恢复：`curl http://127.0.0.1:7788`

## 回滚方案

**如果 systemd 配置失败**:
```bash
# 停止 systemd 服务
systemctl --user stop graduation-frontend
systemctl --user disable graduation-frontend

# 手动启动原进程
cd /home/caohui/projects/graduation-leave-system/demo-web
nohup python3 -m http.server 7788 > /tmp/frontend-7788.log 2>&1 &
```

## 兼容性

- **systemd版本**: Ubuntu 26.04 默认 systemd 255+
- **Python版本**: 3.14.4 (已验证 http.server 模块可用)
- **用户权限**: 仅需用户级 systemd（无需 sudo）
- **端口**: 7788（已验证无冲突）

## 性能影响

- **内存**: systemd overhead ~2MB
- **CPU**: 守护进程监控 <0.1%
- **磁盘**: journal 日志 ~10MB/天（7天轮转 = ~70MB）

## 安全考虑

- 服务运行在用户权限（非root）
- 监听 `0.0.0.0:7788`（已有防火墙配置）
- 静态文件服务，无代码执行风险
- 日志不包含敏感信息
