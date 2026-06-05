# 用户业务决策记录（2026-06-05）

**背景：** Phase 0就绪后，用户回答4个开放问题

---

## 用户4项决策

### 决策1：寝室号字段（确认）

**问题：** File5是否需要room_number字段？File3何时补充？

**用户答复：**
> "文件5的数据中应该有寝室号字段，文件3中没有，后面会再确认提交文件3的寝室号字段数据，以形成单一对应关系"

**结论：**
- File5必须包含room_number字段 ✓（已在merge_student_data.py实现）
- File3后续补充room_number字段
- 升级路径：Phase 1楼栋级路由 → Phase 2寝室级精确一对一路由

---

### 决策2：楼栋名称匹配规则

**问题：** File1与File3楼栋名称是否需要规范化？如何匹配？

**用户答复：**
> "按楼栋名称吻合的匹配"

**结论：**
- 使用楼栋名称直接匹配（exact match或normalized match）
- 如File3楼栋名与File1不同，需创建building_normalization_map.json
- validate_routing_coverage.py将检测未匹配楼栋

**实施：**
- Phase 0.3：File3到达后分析楼栋名称
- 如需规范化，创建building normalization map
- 100%覆盖门禁确保所有学生可路由

---

### 决策3：File2独有116行处理

**问题：** File2中116个File1没有的学生如何处理？

**用户答复：**
> "导入"

**结论：**
- File2独有116行作为额外学生导入
- 总学生数：5830（File1）+ 116（File2 only）= 5946行
- 需修改合并策略

**影响：**

**merge_student_data.py需调整：**
```python
# 当前：只输出File1的5830行
# 修改：输出File1 + File2独有行

# 新逻辑：
# 1. File1为基准（5830行）
# 2. File2匹配的：补充字段
# 3. File2独有的（116行）：作为新行追加
#    - user_id: 从File2的XH
#    - user_id_source: 'file2_only'
#    - File1字段：空值
```

**merge_report.json需包含：**
- file1_only_count: 271（研究生等）
- file2_only_count: 116
- matched_count: 5559
- total_output_rows: 5946

---

### 决策4：学工管理员数据提供方式

**问题：** Admin角色如何实现？复用dean还是新增？

**用户答复：**
> "学工管理员数据后面会同样提供EXCEL表格或CSV数据（学工管理员，不做审批流程，但能查看全部进度数据）"

**结论：**
- 学工管理员数据单独提供（Excel/CSV格式）
- 角色定义：只读，可查看全部申请，无审批权限
- 不复用dean枚举，等待独立数据文件

**数据格式（待确认）：**
```
职工号,姓名,部门,手机号,邮箱
A001,张三,学工部,13800000001,zhangsan@example.com
```

**实施：**
- Phase 3增加：import_admins命令
- UserRole枚举：student | dorm_manager | counselor | admin
- 权限：admin可查看所有申请但不能审批

---

## 实施影响

### 立即需要修改

**1. merge_student_data.py**
- 增加File2独有行处理逻辑
- 输出5946行而非5830行
- 新增user_id_source: 'file2_only'

**2. validate_routing_coverage.py**
- 验证目标：5946行学生100%路由覆盖

**3. 文档更新**
- 实施方案：数据覆盖5830→5946
- Phase 3：增加import_admins命令

### 等待用户提供

**1. 真实数据文件**
- File1-4 Excel文件

**2. 学工管理员数据**
- Admin Excel/CSV文件
- 字段格式待确认

**3. File3寝室号补充**
- Phase 2升级时提供

---

**文档日期：** 2026-06-05  
**决策状态：** 4/4已回答  
**下一步：** 修改merge脚本支持File2独有行，更新文档反映5946行total
