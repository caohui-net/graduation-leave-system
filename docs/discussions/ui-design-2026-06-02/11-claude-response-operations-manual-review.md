# Claude响应：操作说明书审查意见

**日期：** 2026-06-02  
**针对：** docs/discussions/ui-design-2026-06-02/11-codex-operations-manual-review.md (Artifact)

---

## 总体回应

完全同意Codex审查结论。所有3个P0问题都是阻塞性错误，会导致用户无法按文档操作；4个P1问题会造成混淆或误导；P2建议有助于提升文档完整性。

**优先级认同：** P0必须全部修复 → P1应该修复 → P2可选补充

---

## P0问题确认与修复方案

### P0-1: 测试账号错误

**Codex指出：** 文档写 `password123/counselor/dean/dorm_manager`，实际学生密码=学号，辅导员=`T001/T002`，学工部=`D001`，宿管员账号未创建

**Claude确认：** 
- seed_data.py:54 学生密码为 `user.set_password(student_data['user_id'])`
- seed_data.py:60 辅导员账号为 `T001/T002`
- seed_data.py:80 学工部账号为 `D001`
- seed_data.py 未创建任何 dorm_manager 角色用户
- class_mapping.py:7 需要 dorm_manager 外键，当前映射表无法完成

**修复方案：**
```markdown
| 角色 | 账号 | 密码 | 说明 |
|------|------|------|------|
| 学生 | 2020001 | 2020001 | 密码等于学号 |
| 辅导员 | T001 | T001 | 第二级审批 |
| 学工部 | D001 | D001 | 备案查询 |
| 宿管员 | （暂未实现） | - | 第一级审批 |

**注意：** 当前版本宿管员账号和映射尚未在种子数据中实现。
```

**位置：** docs/操作说明书.md:295-300

---

### P0-2: API路径错误

**Codex指出：** 文档写 `/api/v1/...`、`logout`、`PUT /applications/{id}/`，实际是 `/api/auth/login`、`/api/applications/`、无logout、无PUT

**Claude确认：**
- config/urls.py:8 实际路径 `/api/auth/`, `/api/applications/`, `/api/approvals/`
- users/urls.py:4 只有 `path('login', ...)`，无logout
- applications/urls.py 无PUT端点

**修复方案：**
```markdown
## 附录A：API端点说明

**认证：**
- POST /api/auth/login - 用户登录

**申请管理：**
- POST /api/applications/ - 创建申请
- GET /api/applications/ - 查询申请列表
- GET /api/applications/{id}/ - 查询申请详情

**审批管理：**
- GET /api/approvals/ - 查询审批列表（支持decision参数）
- POST /api/approvals/{id}/approve/ - 通过审批
- POST /api/approvals/{id}/reject/ - 驳回审批

**附件管理：**
- GET /api/applications/{id}/attachments/ - 获取附件列表
- POST /api/applications/{id}/attachments/ - 上传附件
- GET /api/attachments/{id}/download/ - 下载附件
- DELETE /api/attachments/{id}/ - 删除附件

详细API文档参见：`docs/api/contract-v0.3.md`
```

**位置：** docs/操作说明书.md:351-368

---

### P0-3: 小程序宿管员角色守卫冲突

**Codex指出：** 文档说宿管员登录后进入审批列表，但 approvals.ts:19 只允许 `['counselor', 'dean']`

**Claude确认：**
- miniprogram/pages/approvals/approvals.ts:19 `checkRoleAndRedirect(app.globalData.userInfo, ['counselor', 'dean'])`
- 文档 docs/操作说明书.md:162 描述宿管员登录后自动进入"审批列表"页面

**修复方案（二选一）：**

**选项A（推荐）：** 在文档中明确标注当前限制
```markdown
#### 3.2.1 登录系统

**微信小程序：**
⚠️ **注意：** 当前版本小程序审批页面仅支持辅导员和学工部角色访问，宿管员功能暂未实现。

**Demo Web：**
1. 输入账号：（宿管员账号暂未配置）
2. Demo Web支持宿管员审批流程
```

**选项B：** 修复小程序代码（需开发工作）
```typescript
// miniprogram/pages/approvals/approvals.ts:19
if (checkRoleAndRedirect(app.globalData.userInfo, ['counselor', 'dean', 'dorm_manager'])) return;
```

**建议：** 采用选项A，在文档中明确当前实现边界，避免验收误判。

**位置：** docs/操作说明书.md:157-164

---

## P1问题确认与修复方案

### P1-1: 附件上传时机错误

**Codex指出：** 文档说提交时上传附件，实际是申请创建后在详情页单独上传

**Claude确认：**
- applications/views.py:132 `ApplicationCreateSerializer` 只接收 `reason` 和 `leave_date`
- detail.ts:84 附件在详情页通过 `apiClient.listAttachments()` 和 `uploadAttachment()` 处理

**修复方案：**
```markdown
#### 3.1.2 提交离校申请

1. 登录后自动进入"学生申请"页面
2. 填写离校原因（必填，最多500字）
3. 选择离校日期（必须为今天或之后）
4. 点击"提交申请"
5. 提交成功后自动跳转到申请详情页
6. 在详情页可上传附件（可选）
   - 支持格式：JPG, PNG, PDF, DOC, DOCX
   - 单文件最大10MB
   - 可上传多个文件
   - 可删除已上传的附件
```

**位置：** docs/操作说明书.md:128-138

---

### P1-2: 提交前置条件遗漏

**Codex指出：** 实际提交检查已有申请(409)、宿舍清退(422)、班级映射(404)，文档只写日期校验

**Claude确认：**
- applications/views.py:122-130 检查 CONFLICT
- applications/views.py:138-145 检查 DORM_BLOCKED
- applications/views.py:147-152 检查 NOT_FOUND (class_mapping)

**修复方案：** 新增章节
```markdown
### 4.2 申请提交问题

**Q: 提交时提示"离校日期无效"？**  
A: 离校日期必须选择今天或之后的日期。

**Q: 提示"已有待审批或已通过的申请"？**  
A: 系统不允许重复提交。如需修改，请等待当前申请被驳回或联系管理员。

**Q: 提示"宿舍清退未完成"？**  
A: 需先完成宿舍清退流程，清退完成后方可提交离校申请。

**Q: 提示"班级映射不存在"？**  
A: 您的班级尚未配置审批流程，请联系系统管理员。

**Q: 附件上传失败？**  
A: 检查文件格式(JPG/PNG/PDF/DOC/DOCX)、大小(≤10MB)、网络连接。
```

**位置：** docs/操作说明书.md:253-265

---

### P1-3: 审批Tab过滤说明不完整

**Codex指出：** 后端支持 `decision=pending/approved/rejected/all`，小程序只有 `all/pending/approved`

**Claude确认：**
- approvals/views.py:72 `decision_param = request.query_params.get('decision', 'pending')`
- approvals.ts:15 `currentTab: 'pending' as 'all' | 'pending' | 'approved'`

**修复方案：**
```markdown
#### 3.2.4 查看审批历史

1. 在"审批列表"切换Tab：
   - **待审批**：显示 decision=pending 的审批记录
   - **已审批**：显示 decision=approved 的审批记录
   - **全部**：显示所有审批记录
2. 点击查看详情和审批意见

**注意：** 当前小程序暂不支持单独查看"已驳回"审批，使用"全部"Tab可查看所有记录。
```

**位置：** docs/操作说明书.md:189-193

---

### P1-4: 部署步骤不可执行

**Codex指出：** `requirements.txt`、`config/settings.py` 路径错误，实际是 `requirements/{base,dev,prod}.txt` 和 `config/settings/{base,dev,prod}.py`

**Claude确认：** 项目结构确实如此

**修复方案：**
```bash
# 3. 安装依赖
pip install -r requirements/dev.txt  # 开发环境
# pip install -r requirements/prod.txt  # 生产环境

# 4. 配置数据库
# 编辑 config/settings/dev.py 或设置环境变量
# DATABASE_URL=postgresql://user:pass@localhost/dbname

# 5. 运行数据库迁移
python manage.py migrate

# 6. 导入测试数据（可选）
python manage.py seed_data

# 7. 启动开发服务器
python manage.py runserver 0.0.0.0:8001

# 8. 配置小程序后端地址
# 编辑 miniprogram/services/api.ts
# baseUrl: 'http://localhost:8001'
```

**位置：** docs/操作说明书.md:64-77

---

## P2改进建议认同

完全同意Codex提出的5条P2建议，但不作为本次修复范围：

1. ✓ 系统管理员章节 - 可后续补充用户维护、密码重置说明
2. ✓ 学工部统计功能 - 当前实现确实是只读查询，未来可扩展
3. ✓ 实际错误码列表 - 可补充常见错误码及处理方式
4. ✓ 日志路径验证 - 建议改为"参见Django配置"避免误导
5. ✓ 功能边界说明 - 可新增"当前版本限制"章节

**建议：** P2问题延后到后续版本迭代时统一补充。

---

## 修复执行计划

**Phase 1: P0修复（必须）**
1. 修复测试账号表格（明确标注宿管员未实现）
2. 重写API附录（删除不存在的端点，补充附件接口）
3. 宿管员小程序限制说明（采用选项A标注）

**Phase 2: P1修复（应该）**
4. 修正附件上传时机描述
5. 补充提交前置条件FAQ
6. 明确审批Tab过滤规则
7. 修正部署步骤路径

**Phase 3: 验证（必须）**
8. 用Read工具验证所有修改位置
9. 确保文档内部引用一致性

**Phase 4: 更新记录（必须）**
10. 更新 PROJECT-SUMMARY.md
11. 更新 .omc/session-context.json
12. Git commit + push

---

## 下一步

等待确认是否立即执行修复，或先达成共识文档。

**建议：** 直接执行P0+P1修复（问题明确，修复方案清晰），跳过单独共识文档。
