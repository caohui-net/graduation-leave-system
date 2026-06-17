# 执行计划：附件流程修复与UI完善

## 前置检查

- [ ] 快照当前代码
- [ ] 后端服务运行中
- [ ] 测试环境准备

## 执行步骤

### 步骤1：后端修改 - 接收草稿ID参数

**文件：** `backend/apps/applications/views.py`

**修改点1：** `create_application()` 函数（行139起）

在解析请求数据后，添加草稿ID查找逻辑：

```python
# Line 152后：解析serializer后
application_id = request.data.get('application_id')  # 新增

# Line 154: 修改草稿查找逻辑
if application_id:
    # 优先：精确查找指定草稿
    draft = Application.objects.select_for_update().filter(
        student=user,
        application_id=application_id,
        status=ApplicationStatus.DRAFT
    ).first()
    
    if not draft:
        return Response({
            'error': {'code': 'NOT_FOUND', 'message': '草稿不存在或已提交'}
        }, status=status.HTTP_404_NOT_FOUND)
else:
    # 回退：自动查找任意草稿（向后兼容）
    draft = Application.objects.select_for_update().filter(
        student=user,
        status=ApplicationStatus.DRAFT
    ).first()
```

**验证：** 代码编译通过

---

### 步骤2：后端优化 - 添加附件数量字段

**文件：** `backend/apps/applications/serializers.py`

**修改：** `ApplicationListSerializer` 添加 `attachment_count`

```python
class ApplicationListSerializer(serializers.ModelSerializer):
    # 现有字段...
    attachment_count = serializers.SerializerMethodField()
    
    class Meta:
        fields = [..., 'attachment_count']  # 添加到fields列表
    
    def get_attachment_count(self, obj):
        return obj.attachments.filter(is_deleted=False).count()
```

**验证：** API返回包含 `attachment_count` 字段

---

### 步骤3：前端修改 - 传递草稿ID

**文件：** `demo-web/js/api.js`

**修改点1：** `apiSubmitApplication()` 签名（行145）

```javascript
// 原签名
async function apiSubmitApplication(phone, reason, leaveDate)

// 新签名
async function apiSubmitApplication(phone, reason, leaveDate, applicationId)
```

**修改点2：** FormData添加字段（行149后）

```javascript
formData.append('leave_date', leaveDate);
if (applicationId) {
    formData.append('application_id', applicationId);
}
```

**验证：** 函数签名修改完成

---

### 步骤4：前端修改 - 提交流程传递ID

**文件：** `demo-web/index.html`

**修改：** 行1201附近

```javascript
// 原代码
const result = await apiSubmitApplication(phone, reason, leaveDate);

// 新代码
const result = await apiSubmitApplication(phone, reason, leaveDate, draftId);
```

**验证：** draftId正确传递

---

### 步骤5：前端优化 - 列表显示附件

**文件：** `demo-web/index.html`

**修改：** 行288附近

```javascript
// 原代码
const attachmentIcon = app.has_attachments ? '📎' : '';

// 新代码
const attachmentInfo = app.has_attachments 
    ? `<span style="color: #1890ff; font-size: 12px;">📎 ${app.attachment_count || ''}个附件</span>` 
    : '';

// 在卡片渲染中使用 attachmentInfo 替换 attachmentIcon
```

**验证：** 列表显示附件数量

---

### 步骤6：前端优化 - 详情页附件UI

**文件：** `demo-web/index.html`

**修改：** 行446-454，替换为优化版

**优化内容：**
- 显示文件大小
- 添加预览/下载按钮
- 改进卡片样式

**新增全局变量：** `let currentAppId = '';`

**新增函数：**
```javascript
function previewAttachment(attachmentId) {
    const url = `${API_BASE_URL}/applications/${currentAppId}/attachments/${attachmentId}/download/?preview=true`;
    window.open(url, '_blank');
}

function downloadAttachment(attachmentId) {
    const url = `${API_BASE_URL}/applications/${currentAppId}/attachments/${attachmentId}/download/`;
    window.open(url, '_blank');
}
```

**修改详情页函数：** 设置 `currentAppId = appData.application_id`

**验证：** 附件UI显示正确，预览/下载功能正常

---

### 步骤7：测试验证

#### 7.1 后端单元测试

```bash
cd backend
pytest tests/ -k attachment -v
```

#### 7.2 前端集成测试

**清理测试数据：**
```bash
bash /tmp/clean_user_2021140140429.sh
```

**执行自动化测试：**
```bash
python3 /tmp/test_attachment_upload.py
```

**预期结果：**
- ✓ 创建草稿成功
- ✓ 上传2个附件成功
- ✓ 提交申请成功（传递draftId）
- ✓ 附件数量：2个
- ✓ 附件列表正确

#### 7.3 浏览器手工测试

**测试账号：** 2021140140429 / 2021140140429

**测试流程：**
1. 登录学生账号
2. 填写表单 + 上传2个附件（test.jpg, test.pdf）
3. 观察按钮变化（创建草稿→上传附件→提交）
4. **验证列表：** 显示 📎 2个附件
5. **验证详情：** 点击申请，查看附件列表
6. **验证预览：** 点击"预览"按钮，新窗口打开
7. **验证下载：** 点击"下载"按钮，文件下载

**管理员测试：**
1. 登录辅导员账号
2. 查看待审批列表，找到测试申请
3. 点击查看详情
4. **验证：** 附件列表显示正常，可预览/下载

---

### 步骤8：移动端测试

**测试设备：** 手机浏览器或Chrome DevTools模拟

**验证点：**
- [ ] 列表附件图标可见
- [ ] 详情附件列表布局正常
- [ ] 按钮触摸友好（大小、间距）
- [ ] 预览/下载功能正常

---

### 步骤9：代码提交

**检查修改：**
```bash
git status
git diff backend/apps/applications/views.py
git diff backend/apps/applications/serializers.py
git diff demo-web/js/api.js
git diff demo-web/index.html
```

**提交：**
```bash
git add backend/apps/applications/views.py \
        backend/apps/applications/serializers.py \
        demo-web/js/api.js \
        demo-web/index.html

git commit -m "fix: 修复附件流程bug并完善UI

**Bug修复：**
- 后端接收草稿ID参数，精确转化草稿
- 前端传递草稿ID到提交API，避免附件丢失

**功能完善：**
- 列表显示附件状态（📎图标+数量）
- 详情页附件UI优化（文件名、大小、预览/下载按钮）
- 后端返回attachment_count字段

**测试：**
- 自动化测试：附件上传+提交+验证 ✓
- 浏览器测试：列表、详情、预览/下载 ✓
- 移动端适配 ✓

**修改文件：**
- backend/apps/applications/views.py: 接收application_id参数
- backend/apps/applications/serializers.py: 添加attachment_count
- demo-web/js/api.js: apiSubmitApplication新增参数
- demo-web/index.html: 传递draftId，优化附件UI

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"

git push origin main
```

---

## 回滚命令

```bash
# 如遇严重问题
git revert HEAD
git push origin main
```

## 检查清单

**实施前：**
- [ ] 快照已创建
- [ ] 后端服务运行
- [ ] 测试账号准备

**实施中：**
- [ ] 后端修改完成
- [ ] 前端修改完成
- [ ] 自动化测试通过
- [ ] 浏览器测试通过
- [ ] 移动端测试通过

**实施后：**
- [ ] 代码已提交推送
- [ ] 规范文档已更新
- [ ] 任务已归档

## 预估时间

- 步骤1-2（后端修改）: 15分钟
- 步骤3-6（前端修改）: 30分钟
- 步骤7（测试验证）: 20分钟
- 步骤8（移动端测试）: 10分钟
- 步骤9（提交）: 5分钟
- **总计：** ~80分钟
