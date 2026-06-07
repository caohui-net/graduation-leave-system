# Phase 0 最终共识 - 完成

**日期:** 2026-05-30  
**状态:** ✓ 完成  
**参与方:** Codex + Claude

---

## 一、共识结论

**Codex裁决:** 同意执行新方案  
**Claude执行:** 完成  
**验证结果:** 8/8 测试通过

---

## 二、执行的修复

### 修复1: 添加TEST_REQUEST_DEFAULT_FORMAT配置 ✓

**文件:** `config/settings/base.py`  
**修改:**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (...),
    'DEFAULT_PERMISSION_CLASSES': (...),
    'DEFAULT_RENDERER_CLASSES': (...),
    'DEFAULT_PARSER_CLASSES': (...),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',  # 新增
}
```

**效果:** DRF测试客户端默认使用JSON格式，对齐项目JSON-only API架构

### 修复2: 添加ClassMapping fixtures ✓

**影响文件:**
- `apps/applications/tests/test_application_flow.py`
- `apps/applications/tests/test_error_cases.py`
- `apps/approvals/tests/test_rejection_flow.py`

**修改内容:**
1. 添加import: `from apps.users.class_mapping import ClassMapping`
2. 在setUp中创建ClassMapping:
```python
ClassMapping.objects.create(
    class_id='CS2020-01',
    counselor=self.counselor,
    counselor_name='李老师',
    active=True
)
```

**效果:** 修复404错误（create_application需要ClassMapping才能正常工作）

### 修复3: 校准test_dorm_blocked_error测试数据 ✓

**文件:** `apps/applications/tests/test_error_cases.py`

**问题:** 测试使用2020002，但mock数据中2020002已改为COMPLETED状态

**修复:**
1. 添加student3 (2020003) 到setUp
2. 测试改用2020003（mock数据中为NOT_STARTED状态）

**效果:** 测试正确验证宿舍清退阻断逻辑

---

## 三、验证结果

### 测试执行
```bash
docker exec graduation-leave-system-backend-1 python manage.py test \
  apps.applications.tests.test_application_flow \
  apps.applications.tests.test_error_cases \
  apps.approvals.tests.test_rejection_flow
```

### 测试结果
```
Found 8 test(s).
System check identified no issues (0 silenced).
........
----------------------------------------------------------------------
Ran 8 tests in 6.175s

OK
```

**8/8 测试通过 ✓**

---

## 四、根因分析总结

### 问题1: KeyError: 'access_token'
**根因:** DRF默认TEST_REQUEST_DEFAULT_FORMAT='multipart'，但项目只启用JSONParser  
**修复:** 添加TEST_REQUEST_DEFAULT_FORMAT='json'配置  
**影响:** 7个测试（所有需要登录的测试）

### 问题2: 404 on POST /api/applications/
**根因:** create_application视图需要ClassMapping，测试未创建  
**修复:** 在3个测试文件的setUp中添加ClassMapping fixture  
**影响:** 6个测试（所有需要创建申请的测试）

### 问题3: test_dorm_blocked_error返回201而非422
**根因:** 测试使用2020002，但mock数据已改为COMPLETED  
**修复:** 测试改用2020003（NOT_STARTED状态）  
**影响:** 1个测试

---

## 五、Codex关键洞察

1. **根因定位准确:** 识别出TEST_REQUEST_DEFAULT_FORMAT与DEFAULT_PARSER_CLASSES不匹配
2. **遗漏风险预警:** 指出手动添加format='json'容易遗漏且无法防止回归
3. **404根因诊断:** 通过运行测试发现ClassMapping缺失导致404
4. **数据校准建议:** 指出test_dorm_blocked_error需要重新校准测试数据

---

## 六、方案对比

### 原方案（已放弃）
- 手动给~20个POST调用添加format='json'
- 时间：20-25分钟
- 风险：容易遗漏，未来回归

### 新方案（已执行）
- 添加TEST_REQUEST_DEFAULT_FORMAT='json'配置
- 添加ClassMapping fixtures
- 校准测试数据
- 时间：实际约15分钟
- 风险：低，根因修复

---

## 七、Phase 0 完成确认

**完成标准:** 目标测试全部通过  
**验证结果:** 8/8 通过 ✓  
**Phase 0状态:** **完成**

**下一步:** Phase 1 - 实现列表接口

---

## 八、文件变更清单

1. `config/settings/base.py` - 添加TEST_REQUEST_DEFAULT_FORMAT
2. `apps/applications/tests/test_application_flow.py` - 添加ClassMapping
3. `apps/applications/tests/test_error_cases.py` - 添加ClassMapping + 修复test_dorm_blocked_error
4. `apps/approvals/tests/test_rejection_flow.py` - 添加ClassMapping

**总计:** 4个文件修改

---

## 九、经验总结

1. **根因修复优于症状修复:** 配置级修复比逐点补丁更可靠
2. **测试隔离很重要:** ClassMapping缺失导致测试间相互影响
3. **Mock数据需要文档化:** 避免修改mock数据后影响其他测试
4. **Codex审查价值高:** 及时发现了手动方案的遗漏风险

---

**Phase 0 执行完成时间:** 2026-05-30 16:43  
**总耗时:** 约21分钟（从Codex第一次审查到测试通过）
