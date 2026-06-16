# Codex API连接失败问题记录

**问题ID:** codex-api-failure-20260614  
**发现时间:** 2026-06-14 13:04  
**状态:** 待修复  
**优先级:** 中

---

## 问题描述

在执行三模型协作讨论（taolun技能）时，Codex agent持续失败，导致无法达成tri-model共识。

### 错误信息

```
❌ [Codex] failed: json_parse_failed
ERROR: stream disconnected before completion: error sending request for url (https://dm-fox.rjj.cc/codex/v1/responses)
ERROR: Reconnecting... 1/5
ERROR: Reconnecting... 2/5
ERROR: Reconnecting... 3/5
ERROR: Reconnecting... 4/5
ERROR: Reconnecting... 5/5
```

### 根本原因

Codex CLI配置使用Fox代理后端（`dm-fox.rjj.cc`），网络连接不稳定或服务不可达，导致：
1. API请求stream中断
2. 重连5次失败
3. 返回空响应
4. JSON解析失败

### 影响范围

- **受影响功能:** claude-codex-gemini-collab技能的讨论功能
- **受影响讨论:**
  - DISCUSS-异地DOCKER自动化部署方案V2-0技术评审-1781442182 (Round 1-3失败)
  - DISCUSS-异地DOCKER自动化部署方案V2-0技术评审-1781442271 (Round 1-3失败)

- **可正常工作:**
  - Gemini agent评审（成功完成）
  - 单独调用Codex CLI测试命令（`echo "test" | codex exec -` 工作正常）

### 对比

| Agent | 状态 | 后端 |
|-------|------|------|
| Codex | ❌ 失败 | Fox代理 (dm-fox.rjj.cc) |
| Gemini | ✅ 成功 | Google API |
| Claude | ✅ 成功 | Anthropic API |

---

## 调试日志

**日志位置:** `/tmp/codex_parse_debug.log`

**关键片段:**
```
Parse failed at 2026-06-14 21:05:59
Full stdout length: 2963
Has 'tokens used': False
Has 'codex': False
ERROR: stream disconnected before completion
```

---

## 解决方案

### 方案1: 修复Codex配置（推荐）

检查Codex配置文件中的provider设置：

```bash
# 查看配置
cat ~/.codex/config.toml

# 可能需要切换到更稳定的endpoint
# 或检查Fox代理网络连通性
```

### 方案2: 临时降级为双模型讨论

在Fox代理修复前，使用Claude + Gemini双模型讨论：

```bash
python3 ~/.claude/skills/claude-codex-gemini-collab/scripts/collab_discuss.py \
  discuss --participants claude,gemini --topic "..."
```

### 方案3: 使用omc ask单独咨询Codex

绕过协作框架，直接使用omc ask：

```bash
omc ask codex "评审问题..." --project graduation-leave-system
```

---

## 当前状态

### 已完成工作

1. ✅ 部署文档v2.0已创建并提交
   - 文件: `docs/异地Docker自动化部署方案.md`
   - Commit: `eef2f86`
   - 已推送到GitHub

2. ✅ Gemini评审已完成
   - Artifact: `.collab/artifacts/DISCUSS-...-r2-gemini-20260614-130534.md`
   - 结果: consensus=false, 提出2个阻塞问题

### Gemini评审要点

**阻塞问题:**
1. 未验证假设 - 不确定容器是否依赖NFS并发读写
2. 同步触发缺失 - 未明确rsync触发机制

**核心质疑:**
- rsync不等价于NFS（无分布式锁，不支持并发写）
- 需确认系统无运行时状态依赖（用户上传/日志/数据库）

**行动项:**
- Claude需确认系统有状态架构
- Gemini需审查文档同步目录清单

### 待处理任务

1. [ ] 响应Gemini评审，提供证据：
   - 本系统无用户文件上传
   - 状态数据已本地化（PostgreSQL/Redis）
   - rsync仅同步代码artifacts

2. [ ] 修复Codex API连接问题

3. [ ] 重新发起讨论达成三模型共识

---

## 相关文件

- 部署文档: `docs/异地Docker自动化部署方案.md`
- Gemini评审: `.collab/artifacts/DISCUSS-异地DOCKER自动化部署方案V2-0技术评审-基于RSYNC选择性同步替代NFS方案-1781442271-discuss-r2-gemini-20260614-130534.md`
- Codex调试日志: `/tmp/codex_parse_debug.log`
- 协作脚本: `~/.claude/skills/claude-codex-gemini-collab/scripts/agent_cli.py`

---

## 时间线

- **13:02** - 创建部署文档v2.0
- **13:03** - 提交并推送文档
- **13:03** - 发起taolun讨论
- **13:04** - Codex连接失败（Round 1-3）
- **13:04** - 修复协作状态
- **13:04** - 重试讨论，Codex仍失败
- **13:05** - Gemini第2轮成功
- **13:06** - 分析Codex失败原因
- **13:07** - 记录问题检查点

---

**创建人:** Claude  
**最后更新:** 2026-06-14 13:07
## 验证更新 (2026-06-15)
- 已通过运行 `echo "test codex connection" | codex exec -` 验证基本连接成功。
- 已通过运行 `python3 ~/.claude/skills/claude-codex-gemini-collab/scripts/collab_discuss.py discuss --participants claude,gemini,codex --topic "测试Codex连接恢复情况"` 验证Codex成功参与讨论并生成了artifact，未发生解析或流中断错误。
