# 共识文档：Phase 0执行逻辑调整方案

**参与方：** Codex + Claude  
**日期：** 2026-06-06  
**任务：** TASK-20260606-08  
**文档基础：**
- Codex审查：`.omc/collaboration/artifacts/20260606-1019-codex-phase0-execution-logic-review.md`
- Claude响应：`.omc/collaboration/artifacts/20260606-claude-response-phase0-execution-logic-review.md`

---

## 达成的共识

### 1. 方案B实现修正（立即执行）

**共识：** 方案B合理但当前实现有bug，需立即修正。

**必须修复的bug：**
- ✓ 补充User模型导入（Line 14）
- ✓ 硬编码职工号改为settings配置
- ✓ 增加fallback用户存在性和角色验证

**Fallback边界（折中方案）：**
- **Phase 2阶段**：保持宽松fallback（有楼栋找不到宿管也fallback）
- **Phase 3.2后**：根据宿管员覆盖率决定是否收紧
  - 覆盖率=100% → 收紧（只对无楼栋fallback）
  - 覆盖率<100% → 保持当前逻辑

**理由：** 避免因File3数据不完整导致有楼栋学生无法提交。

**配置位置：**
```python
# settings.py
FALLBACK_DORM_MANAGER_USER_ID = '92008149'
```

---

### 2. 271人学号更新策略

**共识：** 采用"源数据修正 + File5 v2 + 干净导入"策略。

**实施路径：**
```
Step 1: 创建update_file5_student_no.py脚本
  - 读取file5_students_merged.csv
  - 读取missing_student_no_filled.csv
  - 匹配user_id_source='tmp_generated'的行
  - 替换user_id为真实学号
  - 输出file5_students_merged_v2.csv

Step 2: Phase 3.1使用v2版本导入
  - python3 manage.py import_students --file file5_students_merged_v2.csv
```

**优点：**
- 无临时ID残留
- 无需FK-aware迁移命令
- 数据库保持干净

**前置条件：**
- 创建import_students命令（支持File5表头）
- 支持building字段导入
- 提供dry-run和冲突检测

---

### 3. 19人额外研究生处理

**共识：** 暂不纳入5946人主批次。

**处理方式：**
- 创建待确认清单文档
- 用户确认后作为Phase 3.5补充批次
- 不回写污染File1/File2原始口径

---

### 4. Phase 3任务调整

**共识：** 需要工具前置，调整执行顺序。

**调整后的Phase 3任务：**
```
Phase 3前置：工具补齐
├─ 3.0a: 创建update_file5_student_no.py脚本
├─ 3.0b: 生成file5_students_merged_v2.csv
├─ 3.0c: 创建import_students命令（支持File5表头+building）
├─ 3.0d: 创建import_staff命令
└─ 3.0e: 更新UserRole.ADMIN迁移

Phase 3数据导入：
├─ 3.1: 导入学生（使用v2版本，5946人，无临时ID）
├─ 3.2: 导入宿管员（File3）
├─ 3.3: 导入辅导员（File4）
└─ 3.4: 导入3名管理员（additional_staff.csv）

Phase 3验收：
├─ 学生总数=5946
├─ 无TMP2026_前缀用户
├─ 271人使用真实学号
├─ 116人无楼栋，可路由到程婷
├─ 宿管员覆盖率验证
├─ 辅导员覆盖率=100%
└─ 3名管理员角色正确

Phase 3.5（可选）：
└─ 19人补充批次（用户确认后）
```

---

## 立即执行的修改清单

### 修改1：applications/views.py Bug修复

**文件：** `backend/apps/applications/views.py`

**修改内容：**
1. Line 14：补充User导入
   ```python
   from apps.users.models import UserRole, User
   ```

2. Line 146-166：修正fallback逻辑
   ```python
   # Find dorm manager with fallback mechanism
   dorm_manager = None
   building = user.building

   # Try to find dorm manager by building
   if building and building.strip():
       try:
           dorm_manager = User.objects.get(
               role=UserRole.DORM_MANAGER,
               building=building,
               active=True
           )
       except User.DoesNotExist:
           pass  # Will try fallback
       except User.MultipleObjectsReturned:
           dorm_manager = User.objects.filter(
               role=UserRole.DORM_MANAGER,
               building=building,
               active=True
           ).first()

   # Fallback: use default dorm manager
   if not dorm_manager:
       from django.conf import settings
       fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
       try:
           dorm_manager = User.objects.get(
               role=UserRole.DORM_MANAGER,
               user_id=fallback_id,
               active=True
           )
       except User.DoesNotExist:
           return Response({
               'error': {
                   'code': 'NOT_FOUND',
                   'message': '无可用宿管员',
                   'details': {'building': building or '未分配'}
               }
           }, status=status.HTTP_404_NOT_FOUND)
   ```

### 修改2：settings.py 配置新增

**文件：** `backend/config/settings.py`

**新增内容：**
```python
# Fallback dorm manager for students without building assignment
FALLBACK_DORM_MANAGER_USER_ID = '92008149'
```

### 修改3：创建19人待确认清单

**文件：** `docs/19名额外研究生待确认清单.md`

**内容：** 记录19人基本信息，等待用户确认。

---

## Phase 3前置工具开发清单

### 工具1：update_file5_student_no.py

**路径：** `backend/scripts/update_file5_student_no.py`

**功能：**
- 读取file5_students_merged.csv
- 根据missing_student_no_filled.csv更新临时ID为真实学号
- 输出file5_students_merged_v2.csv
- 提供验证：271条映射、唯一性检查、姓名一致性

### 工具2：import_students命令

**路径：** `backend/apps/users/management/commands/import_students.py`

**功能：**
- 支持File5表头（user_id, name, department, class_id, building_name, phone, email...）
- 将building_name映射到User.building字段
- 提供--dry-run模式
- 冲突检测和报告
- 支持--mode clean（清空后导入）

### 工具3：import_staff命令

**路径：** `backend/apps/users/management/commands/import_staff.py`

**功能：**
- 支持additional_staff.csv格式
- 导入宿管员（DORM_MANAGER）、辅导员（COUNSELOR）、学工管理员（ADMIN）
- 验证职工号唯一性
- 处理程婷的空building字段

### 工具4：UserRole.ADMIN迁移更新

**路径：** `backend/apps/users/migrations/000X_update_role_choices.py`

**内容：** 更新role字段的choices，增加'admin'选项。

---

## 验收标准

### Phase 2验收（Bug修复）
- [ ] User模型已导入
- [ ] fallback配置化（settings.FALLBACK_DORM_MANAGER_USER_ID）
- [ ] fallback用户存在性验证
- [ ] 代码可通过Django检查（python manage.py check）

### Phase 3.0验收（工具补齐）
- [ ] update_file5_student_no.py脚本完成并测试
- [ ] file5_students_merged_v2.csv生成成功
- [ ] 271人学号100%替换，无临时ID残留
- [ ] import_students命令完成并dry-run通过
- [ ] import_staff命令完成并dry-run通过
- [ ] UserRole.ADMIN迁移完成

### Phase 3验收（数据导入）
- [ ] 学生表5946条记录
- [ ] 无TMP2026_前缀
- [ ] 271人使用真实学号（抽样验证）
- [ ] 116人无building或building为空
- [ ] 程婷（92008149）存在且role=DORM_MANAGER
- [ ] 宿管员覆盖率报告生成
- [ ] 辅导员覆盖率100%
- [ ] 2名学工管理员role=ADMIN

---

## 风险与缓解

### 风险1：File3宿管员数据覆盖率<100%
**缓解：** Phase 3.2后执行覆盖率验证，不足100%保持宽松fallback。

### 风险2：import工具开发周期超预期
**缓解：** 优先开发import_students（阻塞Phase 3.1），import_staff可并行。

### 风险3：v2文件生成失败
**缓解：** update_file5_student_no.py增加详细校验和错误报告。

---

## 下一步行动

**当前阶段：** 立即执行Phase 2 Bug修复

**执行顺序：**
1. 修复applications/views.py（User导入 + fallback逻辑）
2. 新增settings.py配置
3. 运行python manage.py check验证
4. 提交代码并推送
5. 更新session-context.json和PROJECT-SUMMARY.md

**后续阶段：** Phase 3.0工具补齐（另开session）

---

**共识达成日期：** 2026-06-06  
**共识状态：** 已确认，可执行
