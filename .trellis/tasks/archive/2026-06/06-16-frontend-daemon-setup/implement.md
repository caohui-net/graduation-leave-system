# 执行计划：前端服务守护进程配置

## 前置验证

- [ ] 确认当前前端服务运行中（7788端口）
- [ ] 确认 systemd 用户实例启用：`systemctl --user status`
- [ ] 确认目标目录存在：`ls -ld ~/.config/systemd/user/`

**验证命令**:
```bash
lsof -i :7788 && curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:7788/
```

---

## 阶段1：创建服务配置

### 1.1 创建 systemd user 目录
```bash
mkdir -p ~/.config/systemd/user/
```

### 1.2 创建 service 文件
**文件**: `~/.config/systemd/user/graduation-frontend.service`
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

### 1.3 重载配置
```bash
systemctl --user daemon-reload
```

### 1.4 验证配置
```bash
systemctl --user cat graduation-frontend
systemctl --user status graduation-frontend  # 应显示 "loaded" 但 "inactive"
```

**回滚点1**: 配置文件可删除，无副作用

---

## 阶段2：创建告警脚本

### 2.1 创建告警脚本
**文件**: `~/.local/bin/alert-graduation-frontend.sh`
```bash
#!/bin/bash
ALERT_LOG="/tmp/graduation-frontend-alerts.log"
TIMESTAMP=$(date -Iseconds)
SERVICE_STATUS=$(systemctl --user is-failed graduation-frontend 2>&1)

echo "[$TIMESTAMP] CRITICAL: graduation-frontend service failed" >> "$ALERT_LOG"
echo "[$TIMESTAMP] Status: $SERVICE_STATUS" >> "$ALERT_LOG"

# 记录最近10行日志
journalctl --user -u graduation-frontend -n 10 --no-pager >> "$ALERT_LOG"
echo "---" >> "$ALERT_LOG"
```

### 2.2 添加执行权限
```bash
chmod +x ~/.local/bin/alert-graduation-frontend.sh
```

### 2.3 测试脚本
```bash
~/.local/bin/alert-graduation-frontend.sh
cat /tmp/graduation-frontend-alerts.log
```

### 2.4 更新 service 文件添加告警
在 `[Unit]` 段添加：
```ini
OnFailure=alert-graduation-frontend.service
```

创建告警触发服务：`~/.config/systemd/user/alert-graduation-frontend.service`
```ini
[Unit]
Description=Alert on graduation-frontend failure

[Service]
Type=oneshot
ExecStart=/home/caohui/.local/bin/alert-graduation-frontend.sh
```

### 2.5 重载配置
```bash
systemctl --user daemon-reload
```

**回滚点2**: 可删除告警脚本，不影响主服务

---

## 阶段3：零停机切换到 systemd

### 3.1 记录当前进程信息
```bash
CURRENT_PID=$(lsof -ti :7788)
echo "Current PID: $CURRENT_PID"
ps -p $CURRENT_PID -o pid,cmd --no-headers
```

### 3.2 启动 systemd 服务（会失败，因端口占用）
此步骤预期失败，验证配置正确：
```bash
systemctl --user start graduation-frontend
# 预期输出：Address already in use
```

### 3.3 停止旧进程
```bash
kill $CURRENT_PID
sleep 2
```

### 3.4 立即启动 systemd 服务
```bash
systemctl --user start graduation-frontend
```

### 3.5 验证服务运行
```bash
systemctl --user status graduation-frontend
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:7788/
# 预期：200
```

### 3.6 启用开机自启
```bash
systemctl --user enable graduation-frontend
```

### 3.7 验证自启配置
```bash
systemctl --user is-enabled graduation-frontend
# 预期输出：enabled
```

**回滚点3**: 
```bash
systemctl --user stop graduation-frontend
cd /home/caohui/projects/graduation-leave-system/demo-web
nohup python3 -m http.server 7788 > /tmp/frontend-7788.log 2>&1 &
```

---

## 阶段4：验证自动重启机制

### 4.1 获取服务进程PID
```bash
SERVICE_PID=$(systemctl --user show graduation-frontend -p MainPID --value)
echo "Service PID: $SERVICE_PID"
```

### 4.2 手动杀死进程
```bash
kill $SERVICE_PID
```

### 4.3 等待重启
```bash
sleep 12  # RestartSec=10s + 2s buffer
```

### 4.4 验证服务恢复
```bash
systemctl --user status graduation-frontend
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:7788/
# 预期：200

# 验证PID已变化
NEW_PID=$(systemctl --user show graduation-frontend -p MainPID --value)
echo "New PID: $NEW_PID (should differ from $SERVICE_PID)"
```

### 4.5 查看重启日志
```bash
journalctl --user -u graduation-frontend --since "2 minutes ago" | grep -i restart
```

---

## 阶段5：验证告警机制

### 5.1 模拟连续失败（触发 StartLimitBurst）
```bash
# 修改 service 使其立即失败
sed -i 's|ExecStart=.*|ExecStart=/usr/bin/false|' ~/.config/systemd/user/graduation-frontend.service
systemctl --user daemon-reload
systemctl --user restart graduation-frontend

# 等待5次重启失败
sleep 60
```

### 5.2 验证服务进入 failed 状态
```bash
systemctl --user status graduation-frontend
# 预期：failed, start-limit-hit
```

### 5.3 检查告警日志
```bash
cat /tmp/graduation-frontend-alerts.log
# 应包含 CRITICAL 告警记录
```

### 5.4 恢复服务配置
```bash
sed -i 's|ExecStart=.*|ExecStart=/usr/bin/python3 -m http.server 7788|' ~/.config/systemd/user/graduation-frontend.service
systemctl --user daemon-reload
systemctl --user reset-failed graduation-frontend
systemctl --user start graduation-frontend
```

### 5.5 验证恢复
```bash
systemctl --user status graduation-frontend
curl http://127.0.0.1:7788/
```

---

## 阶段6：文档更新

### 6.1 更新 PROJECT-QUICK-REF.md
在"前端服务"章节添加：
```markdown
### 守护进程管理（systemd）
- 服务名：graduation-frontend.service
- 启动：systemctl --user start graduation-frontend
- 停止：systemctl --user stop graduation-frontend
- 重启：systemctl --user restart graduation-frontend
- 状态：systemctl --user status graduation-frontend
- 日志：journalctl --user -u graduation-frontend -f
- 告警日志：/tmp/graduation-frontend-alerts.log
```

### 6.2 提交变更
```bash
git add ~/.config/systemd/user/graduation-frontend.service
git add ~/.local/bin/alert-graduation-frontend.sh
git add PROJECT-QUICK-REF.md
git commit -m "feat: 配置前端服务systemd守护进程保证业务连续性"
git push
```

---

## 验证检查清单

- [ ] 服务运行：`systemctl --user is-active graduation-frontend` → active
- [ ] 开机自启：`systemctl --user is-enabled graduation-frontend` → enabled
- [ ] HTTP可访问：`curl http://127.0.0.1:7788/` → 200
- [ ] 自动重启：kill进程后10秒内恢复
- [ ] 日志可查：`journalctl --user -u graduation-frontend -n 10`
- [ ] 告警可用：StartLimitBurst触发后写入 `/tmp/graduation-frontend-alerts.log`
- [ ] 文档更新：PROJECT-QUICK-REF.md 包含守护进程管理命令

---

## 常见问题

**Q: systemctl --user 命令失败**
```bash
# 启用 systemd 用户实例
loginctl enable-linger $USER
systemctl --user daemon-reload
```

**Q: 服务无法启动，报 "Failed to connect to bus"**
```bash
export XDG_RUNTIME_DIR=/run/user/$(id -u)
systemctl --user status
```

**Q: 服务启动但无法访问7788端口**
```bash
# 检查WorkingDirectory是否正确
systemctl --user cat graduation-frontend | grep WorkingDirectory
# 检查端口占用
lsof -i :7788
```

**Q: 开机后服务未自动启动**
```bash
# 检查 linger 状态
loginctl show-user $USER | grep Linger
# 应为 Linger=yes

# 启用 linger
loginctl enable-linger $USER
```
