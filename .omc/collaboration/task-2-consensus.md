# Task #2 共识：修复repair()使用journal lock

**达成时间：** 2026-05-30  
**讨论轮次：** 2轮  
**参与方：** Claude, Codex

---

## 问题描述

**Bug位置：** `collab_validate.py:124`

```python
def repair():
    # ... 省略前面代码 ...
    state_file = collab_dir / 'state.json'
    state_file.write_text(json.dumps(state, indent=2) + '\n')  # BUG: 无锁写入
```

**问题：** repair()函数直接写入state.json，未获取locks/journal.lock，违反协议要求。

**风险场景：** collab_event.py持锁写入时，repair()无锁覆盖state.json，导致状态不一致或数据丢失。

---

## 最终方案

### 1. 核心修复要求

1. ✅ 必须写owner.json
2. ✅ 原子写入（tmp file + rename）
3. ✅ 锁范围覆盖完整read-check-write
4. ✅ 严格解析events.jsonl，拒绝malformed
5. ✅ 默认fail fast，不自动删除锁
6. ✅ 可选--wait参数
7. ✅ 单独的stale-lock恢复路径

### 2. repair()流程

```python
def repair(base_dir=".", wait_seconds=0, force_stale_lock=False):
    collab_dir = Path(base_dir) / '.omc' / 'collaboration'
    
    # 1. 获取锁
    lock = acquire_journal_lock(
        collab_dir,
        agent="repair",
        task_id=None,
        reason="manual repair: state.json rebuild"
    )
    if not lock:
        report_lock_owner()
        return 1
    
    try:
        # 2. 备份现有文件
        backup_state_json_and_events_jsonl()
        
        # 3. 严格解析events.jsonl
        events = parse_events_strict(events_file)
        if events has malformed lines or duplicate ids:
            print error
            print backup path
            return 1
        
        # 4. 从有效事件重建state
        state = rebuild_state_from_valid_events(events)
        
        # 5. 追加state_rebuilt事件
        state_rebuilt_event = {
            "id": max_event_id + 1,
            "type": "state_rebuilt",
            "agent": "repair",
            "timestamp": now_iso8601(),
            "summary": "Rebuilt collaboration state from valid event log.",
            "status": state["status"],  # 从事件流重建出的最终status
            "details": {
                "rebuilt_from_event_count": len(events),
                "last_valid_event_id": max_event_id,
                "repair_reason": "state.json missing",
                "backup_path": backup_path
            }
        }
        append_event(state_rebuilt_event)
        
        # 6. 更新state.last_event_id
        state["last_event_id"] = max_event_id + 1
        
        # 7. 原子写入state.json
        write_state_atomic(
            collab_dir,
            state,
            temp_name="state.json.tmp.repair"
        )
        
        # 8. 验证
        validate_state_json()
        validate last_event_id == max_event_id + 1
        
        return 0
    finally:
        release_lock(lock)
```

### 3. owner.json格式

```json
{
    "agent": "repair",
    "task_id": null,
    "created_at": "2026-05-30T15:38:00.847Z",
    "heartbeat_at": "2026-05-30T15:38:00.847Z",
    "reason": "manual repair: state.json rebuild",
    "pid": 12345,
    "hostname": "localhost"
}
```

**说明：**
- `task_id: null` 可接受（repair不属于特定任务）
- `heartbeat_at` 对短操作写初始值即可，不要求持续心跳
- 增加 `pid` / `hostname` 用于调试和stale lock检测

### 4. state_rebuilt事件

**分类：** STATUS_OVERRIDE_EVENTS

```python
STATUS_OVERRIDE_EVENTS = {
    'state_corrected',
    'state_rebuilt',  # 新增
}
```

**事件格式：**

```json
{
    "id": 53,
    "type": "state_rebuilt",
    "agent": "repair",
    "timestamp": "2026-05-30T15:38:00.847Z",
    "summary": "Rebuilt collaboration state from valid event log.",
    "status": "waiting",
    "details": {
        "rebuilt_from_event_count": 52,
        "last_valid_event_id": 52,
        "repair_reason": "state.json missing",
        "backup_path": ".omc/collaboration/backups/state-20260530-153800.json"
    }
}
```

**关键语义：**
- `status` 使用从有效事件流重建出的最终status，不信任损坏或缺失的旧state.json
- 作用是审计 + 推进last_event_id，不改变业务状态
- **仅适用于：** events.jsonl严格解析通过，但state.json缺失/无效/落后的场景
- **不适用于：** events.jsonl已损坏的场景（应fail fast）

### 5. 严格解析边界

**严格拒绝（repair失败）：**
- 非JSON行（除尾部单个空行）
- duplicate id
- id非正整数
- 缺少必填字段（id/type/timestamp）

**警告但允许：**
- id跳号（记录gap）
- 未知字段（forward compatibility）
- 时间戳格式异常（记录但不阻止）

**完全禁止：**
- 注释行（events.jsonl是机器日志，不是配置文件）

### 6. 锁竞争处理

**默认行为：** fail fast

- lock不存在：正常acquire
- lock存在且owner.json正常：打印owner/created_at/heartbeat_at/age，退出
- lock存在且超过stale阈值：提示"suspected stale lock"，仍退出

**可选参数：**
- `--wait N`：等待N秒后重试（用于自动化脚本）
- `--force-stale-lock`：强制移除stale lock（需要用户确认，备份owner.json）

**原因：** repair是手动、侵入式操作，默认fail fast并报告owner/age/reason最安全。

### 7. events.jsonl损坏处理

**如果events.jsonl已损坏：**
- 不能追加state_rebuilt
- 不应该只修state.json后宣称成功
- 应fail fast：保留原日志、写repair artifact
- 如果能安全写state则设needs_repair标记

**原因：** 避免用"部分事件日志"重建状态，掩盖真实故障。

---

## 实现位置

- **collab_validate.py：** 修改repair()函数
- **collab_event.py：** 提取acquire_lock/release_lock为共享helper
- **protocol.md：** 更新锁协议和repair语义

---

## 下一步

1. 提取锁管理为共享helper函数
2. 实现严格events.jsonl解析器
3. 实现原子state.json写入
4. 修改repair()按新流程执行
5. 添加回归测试

**状态：** ✅ 共识达成，待实施
