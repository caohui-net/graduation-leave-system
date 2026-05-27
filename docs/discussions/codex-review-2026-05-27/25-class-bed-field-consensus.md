# 数据对接字段补充 - 最终共识

**日期：** 2026-05-27  
**参与方：** Codex (GPT-5.5) + Claude Opus 4.7

---

## 一、审查结论

**状态：** 已修复所有问题，达成共识

**修改内容：**
1. ✓ 统一class_name字段必填性标注为"可选"
2. ✓ 修正Excel示例表格列错位
3. ✓ 统一系统设计文档字段命名

---

## 二、已完成的修复

### 修复1：class_name标注为可选

**文件：** `docs/数据对接说明文档.md:105`

**修改前：**
```
| class_name | String | 班级 | "计算机2020级1班" |
```

**修改后：**
```
| class_name | String | 班级（可选） | "计算机2020级1班" |
```

**理由：** 与文件导入字段表保持一致，宿舍系统可能无法提供班级信息。

---

### 修复2：Excel示例列对齐

**文件：** `docs/数据对接说明文档.md:241`

**修改前：**
```
| 2020010102 | 李四 | 计算机2020级1班 | 1号楼 | 102 | 2 | 否 |  |  | 未开始 | 尚未办理清退手续 |
```
（11列，多出1个空列）

**修改后：**
```
| 2020010102 | 李四 | 计算机2020级1班 | 1号楼 | 102 | 2 | 否 |  | 未开始 | 尚未办理清退手续 |
```
（10列，与表头一致）

**理由：** 确保所有行列数一致，避免用户填写数据时产生混淆。

---

### 修复3：统一字段命名

**文件：** `docs/design/2026-05-27-system-design.md:1629-1642`

**修改前：**
```json
{
  "code": 200,
  "data": {
    "student_id": "2020001",
    "name": "张三",
    "class_name": "计算机2020级1班",
    "is_cleared": true,
    "clearance_date": "2026-05-25",
    "room_no": "A101",
    "bed_number": "1"
  }
}
```

**修改后：**
```json
{
  "code": 200,
  "data": {
    "student_id": "2020001",
    "name": "张三",
    "class_name": "计算机2020级1班",
    "dorm_building": "1号楼",
    "dorm_room": "101",
    "bed_number": "1",
    "is_checked_out": true,
    "checkout_date": "2026-05-25",
    "checkout_status": "completed"
  }
}
```

**字段映射：**
- `is_cleared` → `is_checked_out`
- `clearance_date` → `checkout_date`
- `room_no` → `dorm_building` + `dorm_room`
- 新增 `checkout_status`

**理由：** 统一为数据对接文档的命名规范，确保前后端实现一致。

---

## 三、最终字段定义

### API响应字段（统一版本）

| 字段名 | 类型 | 说明 | 必填 | 示例 |
|--------|------|------|------|------|
| student_id | String | 学号 | 是 | "2020010101" |
| name | String | 姓名 | 是 | "张三" |
| class_name | String | 班级 | **否** | "计算机2020级1班" |
| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
| dorm_room | String | 宿舍房间号 | 是 | "101" |
| bed_number | String | 床号 | **否** | "1" |
| is_checked_out | Boolean | 是否已清退 | 是 | true |
| checkout_date | String | 清退日期 | 否 | "2026-05-25" |
| checkout_status | String | 清退状态 | 是 | "completed" |

**可选字段说明：**
- `class_name`：宿舍系统可能无法提供班级信息
- `bed_number`：部分宿舍系统无床号管理
- `checkout_date`：未清退时为null

---

## 四、数据库存储决策

### class_name字段
- **决策：** 不在applications表存储
- **理由：** users表已有，避免冗余

### bed_number字段
- **决策：** 暂不存储
- **理由：** 当前只用于验证，后续按需添加

---

## 五、文档一致性确认

**已更新文档：**
- ✓ `docs/数据对接说明文档.md` - API字段定义
- ✓ `docs/数据对接说明文档.md` - Excel示例
- ✓ `docs/数据对接说明文档.md` - 文件导入字段表
- ✓ `docs/templates/宿舍清退数据模板.csv` - CSV模板
- ✓ `docs/design/2026-05-27-system-design.md` - 系统设计API定义

**字段命名统一：**
- ✓ 所有文档使用相同字段名
- ✓ 所有文档必填性标注一致
- ✓ 所有示例数据格式一致

---

## 六、审查通过确认

**Codex审查：** 3个P2问题已全部修复  
**Claude确认：** 所有修改已应用并验证  
**最终状态：** 通过

**可以进入实施阶段。**

---

**共识达成时间：** 2026-05-27  
**文档版本：** v1.0（最终版）
