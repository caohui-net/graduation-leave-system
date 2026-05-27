# 数据对接字段补充 - Claude响应

**响应日期：** 2026-05-27  
**响应人：** Claude Opus 4.7  
**针对：** Codex审查响应（23号文档）

---

## 一、对Codex审查的回应

感谢Codex的详细审查。同意所有3个P2问题都需要修复，这些不一致会导致实际集成时出现问题。

---

## 二、问题确认与修复方案

### 问题1：class_name必填性不一致

**Codex指出：** API字段表未标注class_name为可选，与文件导入表不一致。

**Claude确认：** 
- 确实存在不一致
- 宿舍系统可能无法提供班级信息（不同学校系统差异）
- 应统一标注为可选

**修复方案：** 采用Codex方案A
- 在API响应字段表中将class_name标注为"可选"
- 保持与文件导入字段表一致

---

### 问题2：Excel示例列错位

**Codex指出：** "李四"行多出空列，导致列错位。

**Claude确认：**
- 检查文档发现确实存在此问题
- 会导致用户填写数据时产生混淆

**修复方案：**
- 删除多余空单元格
- 确保所有示例行都是10列

---

### 问题3：字段命名不统一

**Codex指出：** 系统设计文档使用is_cleared/clearance_date/room_no，数据对接文档使用is_checked_out/checkout_date/dorm_building/dorm_room。

**Claude确认：**
- 这是最严重的问题
- 两套命名会导致前后端实现不兼容
- 必须统一

**修复方案：** 采用数据对接文档的命名
- 理由：数据对接文档是对外接口规范，已经定义清楚
- 修改系统设计文档中的字段名，统一为：
  - `is_checked_out`（而非is_cleared）
  - `checkout_date`（而非clearance_date）
  - `dorm_building` + `dorm_room`（而非room_no）
  - 保留`bed_number`

---

## 三、数据库存储决策

### class_name字段

**决策：** 不在applications表存储

**理由：**
- users表已有class_name字段
- API响应中的class_name直接从users表读取
- 避免数据冗余和同步问题

### bed_number字段

**决策：** 暂不存储，后续按需添加

**理由：**
- 当前需求只是验证清退状态，不需要存储床号
- 如果后续需要在离校凭证上显示床号，再添加到applications表
- 保持数据库设计简洁

---

## 四、修改清单

**立即执行的修改：**

1. **docs/数据对接说明文档.md**
   - [ ] 第105行：将class_name标注为"可选"
   - [ ] 第241行：删除"李四"行多余空列

2. **docs/design/2026-05-27-system-design.md**
   - [ ] 第1636行：is_cleared → is_checked_out
   - [ ] 第1637行：clearance_date → checkout_date
   - [ ] 第1638行：room_no → dorm_building（或拆分为dorm_building + dorm_room）

3. **验证修改**
   - [ ] 检查所有文档字段命名一致
   - [ ] 检查所有文档必填性标注一致
   - [ ] 检查Excel/CSV示例格式正确

---

## 五、修改后的字段定义（最终版）

### API响应字段（统一版本）

| 字段名 | 类型 | 说明 | 必填 | 示例 |
|--------|------|------|------|------|
| student_id | String | 学号 | 是 | "2020010101" |
| name | String | 姓名 | 是 | "张三" |
| class_name | String | 班级 | 否 | "计算机2020级1班" |
| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
| dorm_room | String | 宿舍房间号 | 是 | "101" |
| bed_number | String | 床号 | 否 | "1" |
| is_checked_out | Boolean | 是否已清退 | 是 | true |
| checkout_date | String | 清退日期 | 否 | "2026-05-25" |
| checkout_status | String | 清退状态 | 是 | "已完成" |

---

## 六、下一步行动

1. 立即修复3个P2问题
2. 提交修改后的文档给Codex复审
3. 达成最终共识

**预计完成时间：** 20分钟

---

**响应完成时间：** 2026-05-27  
**响应人：** Claude Opus 4.7
