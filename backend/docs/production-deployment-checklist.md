# 生产环境部署执行清单

**部署日期**: TBD（建议凌晨2:00-6:00低峰期）
**执行人**: 运维团队 + 开发负责人
**预计耗时**: 4小时（含监控时间）

---

## 部署前检查（T-24小时）

- [ ] Staging环境测试全部通过
- [ ] 产品经理验收通过
- [ ] 所有代码已合并到main分支
- [ ] 数据库备份空间充足（至少10GB）
- [ ] 通知相关人员部署窗口时间
- [ ] 准备回滚预案和联系方式

---

## 部署执行（凌晨2:00开始）

### 第一阶段：数据库备份（2:00-2:10）

```bash
# 在生产服务器执行
cd /opt/graduation-leave-system
bash backend/scripts/deploy-prod.sh
```

**检查点**:
- [ ] 备份文件生成成功
- [ ] 备份文件大小正常（>100MB）
- [ ] 记录备份时间戳：`_________________`

### 第二阶段：数据库迁移（2:10-2:20）

脚本自动执行以下步骤：
- [ ] 执行migrate命令
- [ ] 验证新字段存在
- [ ] 检查迁移日志无错误

**如果失败**: 脚本自动回滚数据库

### 第三阶段：代码部署（2:20-2:30）

- [ ] Git拉取最新代码
- [ ] 虚拟环境依赖更新
- [ ] 静态文件收集

### 第四阶段：服务重启（2:30-2:35）

- [ ] 重启backend服务
- [ ] 等待5秒启动
- [ ] 健康检查通过

### 第五阶段：烟雾测试（2:35-2:45）

手动验证以下功能：

1. **访问首页**
```bash
curl -I http://production-domain.com/
```
- [ ] 返回200状态码

2. **提交离校申请**（原功能）
- [ ] 登录测试账号
- [ ] 提交离校申请
- [ ] 验证宿管员收到通知

3. **查看审批列表**
- [ ] 管理员登录
- [ ] 查看申请列表正常显示

**预期**: 所有原功能正常，留校功能不可见（Feature Flag关闭）

---

## 灰度开启（3:00）

### 开启Feature Flag

```bash
# 修改环境变量
sudo nano /etc/systemd/system/graduation-backend.service
# 添加: Environment="ENABLE_STAY_SCHOOL=true"

# 重启服务
sudo systemctl daemon-reload
sudo systemctl restart graduation-backend

# 验证环境变量
curl http://localhost:8000/api/feature-flags/
```

- [ ] Feature Flag已开启
- [ ] 服务重启成功
- [ ] 健康检查通过

### 小范围测试（3:10-3:30）

使用测试账号验证：

1. **流程选择页面**
- [ ] 能看到"离校申请"、"留校申请"、"请假申请（灰色）"

2. **提交留校申请**
- [ ] 填写留校时间和原因
- [ ] 提交成功
- [ ] 辅导员收到通知（跳过宿管员）

3. **辅导员审批**
- [ ] 辅导员看到留校申请
- [ ] 审批通过
- [ ] 学生收到通知

**如果发现问题**: 立即关闭Feature Flag
```bash
export ENABLE_STAY_SCHOOL=false
sudo systemctl restart graduation-backend
```

---

## 监控阶段（3:30-6:00）

### 启动自动监控

```bash
bash backend/scripts/monitor-prod.sh 150  # 监控150分钟
```

监控脚本会每分钟检查：
- [ ] 健康检查端点
- [ ] 错误日志数量
- [ ] 数据库连接数

### 手动监控指标

每30分钟检查一次：

1. **错误日志**
```bash
tail -100 /var/log/graduation/error.log | grep ERROR
```
- [ ] 3:30 - 无严重错误
- [ ] 4:00 - 无严重错误
- [ ] 4:30 - 无严重错误
- [ ] 5:00 - 无严重错误
- [ ] 5:30 - 无严重错误

2. **API响应时间**
```bash
curl -o /dev/null -s -w '%{time_total}\n' http://localhost:8000/api/applications/
```
- [ ] 3:30 - 响应时间: _____ms
- [ ] 4:00 - 响应时间: _____ms
- [ ] 4:30 - 响应时间: _____ms
- [ ] 5:00 - 响应时间: _____ms

3. **数据库负载**
```bash
psql -U postgres -d graduation_prod -c "SELECT count(*) FROM pg_stat_activity WHERE datname='graduation_prod';"
```
- [ ] 3:30 - 连接数: _____
- [ ] 4:00 - 连接数: _____
- [ ] 4:30 - 连接数: _____
- [ ] 5:00 - 连接数: _____

---

## 回滚预案

### 场景1: Feature Flag级别回滚（最快）

**触发条件**: 
- 用户报错
- 错误日志激增
- API响应时间异常

**操作**:
```bash
export ENABLE_STAY_SCHOOL=false
sudo systemctl restart graduation-backend
```
**预计恢复时间**: 10秒

### 场景2: 代码级别回滚

**触发条件**:
- 关闭Feature Flag后问题仍存在
- 发现严重bug

**操作**:
```bash
git revert HEAD
git push origin main
bash backend/scripts/deploy-prod.sh
```
**预计恢复时间**: 5分钟

### 场景3: 数据库级别回滚（最后手段）

**触发条件**:
- 数据损坏
- 迁移导致数据丢失

**操作**:
```bash
bash backend/scripts/rollback-prod.sh <backup_timestamp>
```
**预计恢复时间**: 10-15分钟

---

## 部署完成验收（6:00）

- [ ] 监控无异常
- [ ] 错误率 < 0.1%
- [ ] API P95响应时间 < 500ms
- [ ] 数据库连接数正常
- [ ] 用户无投诉

**部署状态**: ✅ 成功 / ❌ 回滚

**完成时间**: _________________

**执行人签名**: _________________

---

## 部署后跟进（D+1至D+7）

### Day 1-3（高度关注）
- [ ] 每日检查错误日志
- [ ] 监控新功能使用情况
- [ ] 收集用户反馈

### Day 4-7（常规监控）
- [ ] 每日健康检查
- [ ] 统计留校申请数量
- [ ] 对比性能指标

---

## 联系方式

**技术负责人**: _______________
**运维负责人**: _______________
**产品负责人**: _______________
**紧急联系电话**: _______________
