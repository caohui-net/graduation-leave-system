# 毕业生离校申请审批系统

高校毕业生离校申请审批管理系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送。

## 技术栈

- **后端**: Python Django 4.2 + Django REST Framework
- **数据库**: PostgreSQL 15
- **前端**: React Native + 微信小程序
- **部署**: Docker + docker-compose

## 功能特性

- ✅ 学生在线提交离校申请（联系电话、离校原因、离校日期）
- ✅ 草稿保存功能（支持分步填写）
- ✅ 附件上传（宿舍清退、图书馆清账等证明文件）
- ✅ 两级审批流程（辅导员 → 学工部）
- ✅ **批量审批功能**（宿管员/辅导员可批量通过/驳回）
  - 全选当前页待审批项
  - 批量操作确认弹窗（防误操作）
  - 统一审批意见输入
  - 原子事务保障（全部成功或全部失败）
- ✅ 宿舍管理系统对接（清退状态检查）
- ✅ 微信通知推送（申请状态变更通知）
- ✅ 权限控制（学生、辅导员、学工部、宿管、系统管理员）

## 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+

### 部署步骤

1. **克隆项目**
```bash
git clone https://github.com/caohui-net/graduation-leave-system.git
cd graduation-leave-system
```

2. **配置环境变量**
```bash
cp .env.docker.example .env.docker
# 编辑 .env.docker 配置数据库、密钥等
```

3. **启动服务**
```bash
docker-compose up -d
```

4. **初始化数据库**
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

5. **访问系统**
- 后端 API: http://localhost:8001
- 管理后台: http://localhost:8001/admin

### 开发环境

**后端开发**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver 8001
```

**运行测试**
```bash
# 单元测试
cd backend
pytest

# 集成测试（需要后端服务运行）
bash tests/smoke_test.sh
```

## 项目状态

**当前版本**: MVP v1.1.1 ⚠️ 重要更新  
**完成度**: 98%  
**最后更新**: 2026-06-13

**v1.1.1 重要修复**:
- 🔴 详情页重复显示问题
- 🔴 审批按钮消失问题
- 楼栋号和房间号字段显示

**已完成功能**:
- ✅ 后端 API 全部实现（20个端点）
- ✅ 数据库模型与迁移（7个核心表）
- ✅ 单元测试覆盖（29个测试全部通过）
- ✅ 小程序 UI 实现（联系电话、草稿保存、附件上传）
- ✅ 审批流程状态机
- ✅ 宿舍管理系统对接
- ✅ **批量审批功能**（提升审批效率）

**待完成**:
- 🔄 生产环境部署配置优化
- 🔄 性能测试与优化
- 🔄 微信小程序完整UI开发

## 文档

### 📚 完整文档索引

查看 **[docs/INDEX.md](docs/INDEX.md)** 获取完整分类索引（94+篇技术文档，涵盖部署运维、数据处理、SSO集成、技术审查等9大类）。

### 核心文档快速访问

- **[三环境同步机制详解](docs/三环境同步机制详解.md)** - 部署架构与运维指南
- **[异地Docker自动化部署方案](docs/异地Docker自动化部署方案.md)** - Docker异地部署
- **[系统设计文档](docs/design/2026-05-27-system-design.md)** - 系统架构设计
- **[项目总结](docs/PROJECT-SUMMARY.md)** - 项目完成总结
- **[操作说明书](docs/操作说明书.md)** - 系统操作指南

## 许可证

MIT License
# Auto-sync test 2026年 06月 18日 星期四 05:59:08 CST
# Sync Test 2026-06-18 06:09:57
Test
# Sync test at 2026-06-18 19:03:48
