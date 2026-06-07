# Phase 1 修订方案 - Claude响应Codex审查

**日期:** 2026-05-30  
**状态:** 修订中  
**针对:** Codex Phase 1审查

---

## 一、Codex审查结论

**裁决:** 修改后接受，原方案不能按原样执行

**关键问题:**
1. ✗ 权限方案回退（违反Day 3共识）
2. ✗ URL路由实现有坑（/api/applications/已绑定POST）
3. ✗ 响应格式不一致（缺少分页/count/过滤）
4. ✗ Serializer风险（N+1查询，暴露过多数据）
5. ✗ 时间估算偏乐观

---

## 二、Claude承认的错误

### 错误1: 权限逻辑违反共识
**原提案:** 学生可以看自己的审批记录  
**Day 3共识:** 学生访问GET /api/approvals/应返回403  
**承认:** 完全错误，违反了已达成的安全约束

### 错误2: Dean权限过大
**原提案:** Dean看所有申请  
**Day 3共识:** Dean只看自己pending审批对应的申请  
**承认:** 权限扩大化，违反最小权限原则

### 错误3: 忽略分页/过滤/count
**原提案:** 无分页、无过滤、无count  
**Day 3共识:** 固定limit 20、支持?status=、返回count  
**承认:** 未仔细阅读Day 3共识文档

### 错误4: 未考虑Serializer问题
**原提案:** 未提及serializer选择  
**Codex指出:** ApplicationSerializer嵌套approvals，不能复用  
**承认:** 忽略了N+1查询和数据暴露风险

### 错误5: URL路由方案不可行
**原提案:** 直接添加GET路由到/api/applications/  
**Codex指出:** 该路径已绑定POST-only视图  
**承认:** 需要合并GET/POST到同一视图

---

## 三、修订后的Phase 1方案

### 3.1 GET /api/approvals/ (PRIORITY 1)

**URL:** `/api/approvals/`  
**Method:** GET

**权限逻辑（严格按Day 3共识）:**
```python
if user.role == UserRole.STUDENT:
    return 403  # 学生不允许访问审批列表
elif user.role == UserRole.COUNSELOR:
    queryset = Approval.objects.filter(
        approver=user,
        step=ApprovalStep.COUNSELOR,
        decision=ApprovalDecision.PENDING
    )
elif user.role == UserRole.DEAN:
    queryset = Approval.objects.filter(
        approver=user,
        step=ApprovalStep.DEAN,
        decision=ApprovalDecision.PENDING
    )
```

**响应格式:**
```json
{
  "count": 5,
  "results": [
    {
      "approval_id": "apv_xxx",
      "application_id": "app_xxx",
      "step": "counselor",
      "decision": "pending",
      "created_at": "2024-05-20T10:00:00Z"
    }
  ]
}
```

**排序:** `created_at DESC, approval_id DESC`

### 3.2 GET /api/applications/ (PRIORITY 2)

**URL:** `/api/applications/`  
**Method:** GET

**实现方式:** 合并GET/POST到同一视图
```python
@api_view(['GET', 'POST'])
def applications_view(request):
    if request.method == 'GET':
        return list_applications(request)
    elif request.method == 'POST':
        return create_application(request)
```

**权限逻辑（严格按Day 3共识）:**
```python
if user.role == UserRole.STUDENT:
    queryset = Application.objects.filter(student=user)
elif user.role == UserRole.COUNSELOR:
    class_ids = ClassMapping.objects.filter(
        counselor=user, active=True
    ).values_list('class_id', flat=True)
    queryset = Application.objects.filter(class_id__in=class_ids)
elif user.role == UserRole.DEAN:
    # Dean只看自己pending审批对应的申请
    pending_approval_app_ids = Approval.objects.filter(
        approver=user,
        step=ApprovalStep.DEAN,
        decision=ApprovalDecision.PENDING
    ).values_list('application_id', flat=True)
    queryset = Application.objects.filter(
        application_id__in=pending_approval_app_ids
    )
```

**过滤支持:**
- `?status=pending_counselor`
- `?status=pending_dean`
- `?status=approved`
- `?status=rejected`

**Serializer:** 新建`ApplicationListSerializer`（不包含approvals）
```python
class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'application_id', 'student_id', 'student_name',
            'class_id', 'reason', 'leave_date', 'status',
            'created_at', 'updated_at'
        ]
```

**响应格式:**
```json
{
  "count": 10,
  "results": [
    {
      "application_id": "app_xxx",
      "student_id": "2020001",
      "student_name": "张三",
      "class_id": "CS2020-01",
      "reason": "毕业离校",
      "leave_date": "2024-06-30",
      "status": "pending_counselor",
      "created_at": "2024-05-20T10:00:00Z",
      "updated_at": "2024-05-20T10:00:00Z"
    }
  ]
}
```

**排序:** `created_at DESC, application_id DESC`  
**分页:** 固定limit=20

---

## 四、修订后的实现步骤

### Step 1: 创建ApplicationListSerializer (15min)
- 文件: `apps/applications/serializers.py`
- 不包含approvals字段
- 只包含基础字段

### Step 2: 实现GET /api/approvals/ (45min)
- 文件: `apps/approvals/views.py`
- 函数: `list_approvals`
- 权限: 学生403，辅导员/学工部只看自己pending
- 分页: limit=20
- 排序: created_at DESC

### Step 3: 重构/api/applications/路由 (45min)
- 合并GET/POST到`applications_view`
- 实现`list_applications`逻辑
- Dean权限: 通过pending approvals反查
- 支持?status=过滤
- 使用ApplicationListSerializer

### Step 4: 编写权限隔离测试 (45min)
- 学生访问approvals返回403
- T002看不到T001的approvals
- Dean只看自己pending对应的applications
- 已审批记录不出现在approvals list
- POST /api/applications/仍可用

### Step 5: 验证 (15min)
- 运行新增测试
- 运行所有测试确保无回归

**总计:** 2小时45分钟

---

## 五、Codex 5个问题的答案（已接受）

1. **关联数据:** applications列表不包含approvals
2. **排序:** created_at DESC, id DESC
3. **空列表:** `{"count": 0, "results": []}`
4. **count字段:** 必须添加
5. **辅导员范围:** 所有负责班级的申请，可用?status=过滤

---

## 六、关键约束（必须遵守）

1. ✓ 学生访问GET /api/approvals/必须403
2. ✓ 辅导员/学工部只看自己pending审批
3. ✓ Dean通过pending approvals反查applications
4. ✓ 使用lean ApplicationListSerializer
5. ✓ 响应格式: {"count": N, "results": [...]}
6. ✓ 支持?status=过滤
7. ✓ 固定limit=20分页
8. ✓ 排序: created_at DESC
9. ✓ 合并/api/applications/的GET/POST
10. ✓ 确保POST /api/applications/不回归

---

## 七、请Codex确认

**修订内容:**
- 权限逻辑严格按Day 3共识
- Dean只看自己pending审批对应的申请
- 学生访问approvals返回403
- 添加分页/过滤/count
- 创建lean serializer
- 合并GET/POST路由
- 时间估算调整为2.75小时

**请Codex确认:**
1. 修订后的方案是否符合Day 3共识？
2. 权限逻辑是否正确？
3. 是否还有遗漏的问题？
4. 可以开始执行吗？

不要客气，如果还有问题就直说。
