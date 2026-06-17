# 执行计划：草稿流程附件上传

## 前置检查

- [x] 快照已创建：commit `2c30429`
- [ ] 后端服务运行中
- [ ] 前端静态服务运行中

## 执行步骤

### 步骤1：修改前端API函数（demo-web/js/api.js）

**文件：** `demo-web/js/api.js`

#### 1.1 新增 apiGetOrCreateDraft()

**位置：** 在 `apiSubmitApplication()` 之前

**代码：**
```javascript
async function apiGetOrCreateDraft() {
    try {
        const response = await fetch(API_BASE_URL + '/applications/draft/', {
            method: 'POST',
            headers: getAuthHeaders()
        });
        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json().catch(() => ({error: {message: '创建草稿失败'}}));
            return { success: false, error: error.error || {message: '创建草稿失败'} };
        }
    } catch (e) {
        console.error("Create draft failed:", e);
        return { success: false, error: {message: '网络错误'} };
    }
}
```

**验证：** 函数添加成功

#### 1.2 修改 apiSubmitApplication()

**修改点：**
1. 移除 `files` 参数
2. 删除 `files.forEach(f => formData.append('attachments', f));`

**原签名：**
```javascript
async function apiSubmitApplication(phone, reason, leaveDate, files)
```

**新签名：**
```javascript
async function apiSubmitApplication(phone, reason, leaveDate)
```

**验证：** 参数列表和formData构建已修改

#### 1.3 修改 apiUploadAttachment() 超时

**位置：** 行240附近

**修改：** 增加超时到30秒（附件上传可能较慢）

**原调用：**
```javascript
const response = await fetch(...)
```

**新调用：**
```javascript
const response = await fetchWithTimeout(url, options, 30000);
```

**验证：** 超时参数已添加

---

### 步骤2：重构提交流程（demo-web/index.html）

**文件：** `demo-web/index.html`

**位置：** 行1173-1198（`submitApplication` 函数内）

#### 2.1 替换提交逻辑

**原代码（行1179）：**
```javascript
const result = await apiSubmitApplication(phone, reason, leaveDate, uploadedFiles);
```

**新代码：**
```javascript
// 步骤1: 创建草稿
btn.textContent = '创建草稿中...';
const draftResult = await apiGetOrCreateDraft();
if (!draftResult || draftResult.error) {
    showToast('创建草稿失败：' + (draftResult?.error?.message || '未知错误'), 'error');
    return;
}
const draftId = draftResult.application_id;

// 步骤2: 上传附件
if (uploadedFiles.length > 0) {
    for (let i = 0; i < uploadedFiles.length; i++) {
        btn.textContent = `上传附件 ${i+1}/${uploadedFiles.length}...`;
        const uploadResult = await apiUploadAttachment(draftId, uploadedFiles[i]);
        if (!uploadResult) {
            showToast(`附件上传失败。草稿已保存(ID: ${draftId})，请重试`, 'error');
            return;
        }
    }
}

// 步骤3: 提交申请
btn.textContent = '提交申请中...';
const result = await apiSubmitApplication(phone, reason, leaveDate);
```

**验证：** 流程已拆分为3步，UI反馈清晰

---

### 步骤3：后端验证

#### 3.1 启动后端服务

```bash
cd backend
python manage.py runserver 0.0.0.0:7787
```

**验证：** 服务运行在 `http://localhost:7787`

#### 3.2 测试草稿API

```bash
# 登录获取token（使用已有测试账号）
TOKEN=$(curl -s -X POST http://localhost:7787/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id":"20241001","password":"test123"}' | jq -r .access_token)

# 测试创建草稿
curl -X POST http://localhost:7787/api/applications/draft/ \
  -H "Authorization: Bearer $TOKEN" | jq
```

**预期输出：**
```json
{
  "application_id": "app_xxx",
  "status": "draft",
  "student_id": "20241001",
  ...
}
```

**验证：** 返回草稿数据，包含 `application_id`

#### 3.3 测试附件上传到草稿

```bash
# 创建测试文件
echo "test attachment" > /tmp/test.txt

# 上传附件
APP_ID="app_xxx"  # 使用上一步返回的ID
curl -X POST http://localhost:7787/api/applications/$APP_ID/attachments/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test.txt" \
  -F "attachment_type=other" | jq
```

**预期输出：**
```json
{
  "attachment_id": "att_yyy",
  "file_name": "test.txt",
  "file_size": 15,
  ...
}
```

**验证：** 附件上传成功

#### 3.4 测试提交草稿转申请

```bash
# 提交申请
curl -X POST http://localhost:7787/api/applications/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "contact_phone=13800138000" \
  -F "reason=测试提交" \
  -F "leave_date=2026-07-01" | jq
```

**预期输出：**
```json
{
  "application_id": "app_xxx",
  "status": "pending_dorm_manager",
  ...
}
```

**验证：** 草稿转为正式申请，status已更新

---

### 步骤4：前端集成测试

#### 4.1 启动前端服务

```bash
cd demo-web
python3 -m http.server 7788
```

**访问：** `http://localhost:7788`

#### 4.2 测试正常流程

1. 登录学生账号：`20241001` / `test123`
2. 填写表单：
   - 联系电话：13800138000
   - 离校原因：测试附件上传
   - 离校日期：2026-07-01
3. 上传2个附件：`test1.jpg`, `test2.pdf`
4. 点击提交
5. 观察按钮文字变化：
   - "创建草稿中..."
   - "上传附件 1/2..."
   - "上传附件 2/2..."
   - "提交申请中..."
6. 提交成功后，查看"我的申请"

**验证点：**
- [ ] 按钮文字按步骤变化
- [ ] 提交成功后跳转到申请列表
- [ ] 申请列表显示新申请
- [ ] 申请详情显示2个附件

#### 4.3 测试无附件流程

1. 填写表单，不上传附件
2. 点击提交

**验证点：**
- [ ] 跳过"上传附件"步骤
- [ ] 直接从"创建草稿中..."到"提交申请中..."
- [ ] 提交成功

#### 4.4 测试错误处理

**场景1：后端服务停止**
1. 停止后端服务
2. 填写表单并提交
3. 观察错误提示

**验证点：**
- [ ] 显示"创建草稿失败：网络错误"
- [ ] 不继续后续步骤

**场景2：附件上传失败（模拟）**
1. 上传超大文件（>10MB，前端会拒绝）
2. 或修改后端权限（临时禁止学生上传）

**验证点：**
- [ ] 显示错误信息
- [ ] 提示"草稿已保存，请重试"

---

### 步骤5：数据库验证

#### 5.1 查看草稿记录

```bash
cd backend
python manage.py shell
```

```python
from apps.applications.models import Application
from apps.attachments.models import Attachment

# 查看所有草稿
drafts = Application.objects.filter(status='draft')
print(f"草稿数量: {drafts.count()}")
for d in drafts:
    print(f"  {d.application_id} - {d.student_id}")

# 查看某草稿的附件
app_id = "app_xxx"  # 替换为实际ID
app = Application.objects.get(application_id=app_id)
attachments = Attachment.objects.filter(application=app, is_deleted=False)
print(f"\n附件数量: {attachments.count()}")
for att in attachments:
    print(f"  {att.attachment_id} - {att.file_name} ({att.file_size} bytes)")
```

**验证：**
- [ ] 草稿记录存在
- [ ] 附件关联正确

#### 5.2 验证草稿转申请后附件保留

```python
# 查看已提交申请
app = Application.objects.get(application_id=app_id)
print(f"状态: {app.status}")  # 应为 pending_dorm_manager

# 附件仍关联
attachments = app.attachments.filter(is_deleted=False)
print(f"附件数量: {attachments.count()}")  # 应保持不变
```

**验证：** 
- [ ] 状态已更新
- [ ] 附件未丢失

---

### 步骤6：回归测试

#### 6.1 辅导员/学工部查看申请

1. 登录辅导员账号
2. 查看审批列表
3. 点击学生申请，查看附件列表

**验证：**
- [ ] 附件列表正常显示
- [ ] 点击附件可下载

#### 6.2 重复提交测试

1. 学生账号已有待审批申请
2. 再次提交新申请
3. 观察错误提示

**验证：**
- [ ] 后端返回409错误
- [ ] 前端显示："已有待审批或已通过的申请，不能重复提交"

---

### 步骤7：代码提交

#### 7.1 检查修改

```bash
git status
git diff demo-web/js/api.js
git diff demo-web/index.html
```

**验证：** 仅修改目标文件，无意外改动

#### 7.2 提交修改

```bash
git add demo-web/js/api.js demo-web/index.html
git commit -m "fix: 实施草稿流程修复附件上传问题

**问题：** 前端提交申请时发送附件，但后端不处理，导致附件全部丢失

**修复：** 使用草稿流程
1. 创建草稿
2. 上传附件到草稿
3. 提交草稿转正式申请

**修改文件：**
- demo-web/js/api.js: 新增apiGetOrCreateDraft()，修改apiSubmitApplication()签名
- demo-web/index.html: 重构submitApplication()流程，UI反馈优化

**测试：**
- 正常流程（2附件）: ✓
- 无附件流程: ✓
- 错误处理: ✓
- 数据库验证: 附件保留 ✓
- 回归测试: 辅导员查看附件 ✓

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

#### 7.3 推送代码

```bash
git push origin main
```

**验证：** 推送成功

---

## 回滚命令（如遇严重问题）

```bash
git reset --hard 2c30429
git push -f origin main
```

## 检查清单

**实施前：**
- [ ] 快照commit已创建
- [ ] 后端API已验证可用
- [ ] 测试环境准备完毕

**实施中：**
- [ ] API函数修改完成
- [ ] 提交流程重构完成
- [ ] 后端API测试通过
- [ ] 前端集成测试通过
- [ ] 数据库验证通过
- [ ] 回归测试通过

**实施后：**
- [ ] 代码已提交
- [ ] 代码已推送
- [ ] 任务状态更新
- [ ] 文档已更新（如需要）

## 预估时间

- 步骤1-2（代码修改）: 20分钟
- 步骤3（后端验证）: 15分钟
- 步骤4（前端测试）: 20分钟
- 步骤5-6（数据验证+回归）: 15分钟
- 步骤7（提交代码）: 10分钟
- **总计：** ~80分钟
