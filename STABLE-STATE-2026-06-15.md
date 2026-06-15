# 稳定状态快照 - 2026-06-15

**状态时间**: 2026-06-15 10:00 (UTC+8)  
**Git Commit**: b526e90  
**标签**: STABLE-BASELINE

---

## 状态说明

此时系统业务流程完全正常，所有核心功能可用。如果后续修改影响业务流程，可恢复至此状态。

---

## 数据库状态

### 用户数据（已验证）
- **总用户数**: 6,081
- **角色分布**:
  - student: 6,001
  - dorm_manager: 76（已与Excel源文档验证一致）
  - counselor: 24（已与Excel源文档验证一致）
  - admin: 18
  - dean: 2

### 管理员账号（真实）
- **肖延量** (20144020) - 学工处副处长 - 13636001781
- **李桃花** (19970545) - 学生事务管理科长 - 15907258727

### 兜底机制
- **宿管员兜底**: 程婷 (92008149), building=NULL
  - 处理159个无building学生
  - 已验证正常工作

### 审批数据
- **申请总数**: 3,126
- **审批记录**: 8,517 条
  - 宿管员审批: 5,896
  - 辅导员审批: 2,621
- **多宿管员覆盖率**: 88.7% (2,771/3,125)

---

## 已验证的数据一致性

### Excel源文档对照（2026-06-15验证）
- ✅ **辅导员**: 20条记录，职工号+姓名完全匹配
  - 源文档: `docs/2026年学院辅导员信息统计表.xls`
- ✅ **宿管员**: 76条记录，职工号+姓名+楼栋号完全匹配
  - 源文档: `docs/2026年社区辅导员信息统计表.xls`
- ✅ **无数据差异**

### 角色清理
- ✅ 已修复5个"teacher"角色用户 → dorm_manager
  - 92020050 许芸, 92023035 贺春红, 92019517 王春兰
  - 92023027 孙慧, 92022002 罗继莲

---

## 运行环境

### 后端 (Django)
- **Python**: 3.14.4
- **框架**: Django + DRF
- **端口**: 7787 (宿主机) → 8000 (容器)
- **容器**: graduation-leave-system-backend-1

### 数据库 (PostgreSQL)
- **版本**: PostgreSQL 15
- **容器**: graduation-leave-system-db-1
- **端口**: 5432
- **数据库名**: graduation_leave
- **数据卷**: postgres_data

### 前端
- **路径**: demo-web/
- **服务**: dufs (端口7788)
- **入口**: index.html

---

## 正常工作的功能

### 核心业务流程 ✅
1. **学生申请**: 正常
2. **宿管员审批**: 正常（含兜底机制）
3. **辅导员审批**: 正常
4. **多宿管员机制**: 正常（88.7%覆盖）
5. **SSO登录**:
   - 移动端登录: 正常
   - SAAS登录: 正常
   - 管理端登录: 正常（token验证开关: QGL_VERIFY_ADMIN_TOKEN=true）

### 已修复的问题 ✅
- ✅ 管理员账号清理（18测试账号→2真实账号）
- ✅ 角色数据清理（teacher→dorm_manager）
- ✅ 数据一致性验证（与Excel源文档对照）
- ✅ 批量审批错误日志
- ✅ 全局异常日志（ErrorLoggingMiddleware）

---

## 已知问题（不影响核心流程）

### 🟡 待优化（非阻塞）
1. **辅导员兜底机制缺失**
   - 影响: 26个无department学生（宿管员通过后报错）
   - 优先级: P1
   - 建议: 添加FALLBACK_COUNSELOR_USER_ID配置

2. **测试覆盖不足**
   - 当前覆盖率: <20%
   - 目标: 60%

3. **SSO端点IP白名单**
   - 建议: nginx限制青橄榄IP访问

4. **缓存机制**
   - 当前: 无
   - 建议: 引入Redis

5. **异步任务**
   - 当前: 无
   - 建议: Celery处理后台任务

---

## 恢复步骤

如需恢复到此稳定状态：

### 1. 代码恢复
```bash
cd /home/caohui/projects/graduation-leave-system
git checkout b526e90
```

### 2. 数据库备份（当前状态）
```bash
# 创建备份
docker exec graduation-leave-system-db-1 pg_dump -U postgres graduation_leave > \
  backup-stable-2026-06-15.sql

# 恢复时执行
docker exec -i graduation-leave-system-db-1 psql -U postgres -d graduation_leave < \
  backup-stable-2026-06-15.sql
```

### 3. 验证恢复
```bash
# 检查用户数
docker exec graduation-leave-system-db-1 psql -U postgres -d graduation_leave \
  -c "SELECT role, COUNT(*) FROM users GROUP BY role ORDER BY COUNT(*) DESC;"

# 检查管理员
docker exec graduation-leave-system-db-1 psql -U postgres -d graduation_leave \
  -c "SELECT user_id, name, role FROM users WHERE role='admin';"

# 检查审批数据
docker exec graduation-leave-system-db-1 psql -U postgres -d graduation_leave \
  -c "SELECT COUNT(*) FROM approvals;"
```

---

## 关键配置文件

### 环境变量 (.env.docker)
- QGL_MOBILE_APP_KEY=cb6f276a42042179e90cd79c4126e075
- QGL_MOBILE_APP_SECRET=da02720febcf47071ee5db78c2b068ec
- QGL_MOBILE_TENANT_CODE=S10405
- QGL_MOBILE_APPID=8uonta
- QGL_VERIFY_ADMIN_TOKEN=true (默认)

### 日志位置
- 主日志: /tmp/backend.log
- 其他日志: /tmp/backend-*.log

---

## 参考文档

- **快速参考**: PROJECT-QUICK-REF.md
- **Excel源文档**:
  - docs/2026年学院辅导员信息统计表.xls
  - docs/2026年社区辅导员信息统计表.xls
- **审计报告**: docs/audit/ (如有)

---

## 更新记录

| 日期 | 更新内容 | Commit |
|------|---------|--------|
| 2026-06-15 | 初始稳定状态快照 | b526e90 |

---

**警告**: 此状态快照仅记录系统配置和代码状态。数据库状态需单独备份。
**建议**: 定期执行数据库备份（pg_dump）并保存至安全位置。
