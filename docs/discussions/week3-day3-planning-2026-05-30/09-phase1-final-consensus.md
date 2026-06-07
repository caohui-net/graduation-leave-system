# Phase 1 最终共识

**日期:** 2026-05-30  
**状态:** ✓ 共识达成  
**参与方:** Codex + Claude

---

## 共识声明

**Codex裁决: 同意执行**

修订后的Phase 1方案核心权限逻辑符合Day 3共识，可以开始执行。

---

## 已确认的方案要点

### 1. GET /api/approvals/ 权限
- ✓ 学生: 403 Forbidden
- ✓ 辅导员: approver=user + step=counselor + decision=pending
- ✓ 学工部: approver=user + step=dean + decision=pending

### 2. GET /api/applications/ 权限
- ✓ 学生: student=user
- ✓ 辅导员: class_id via ClassMapping
- ✓ 学工部: 通过自己pending dean approvals反查

### 3. 响应格式
- ✓ `{"count": N, "results": [...]}`
- ✓ 支持?status=过滤
- ✓ 排序: created_at DESC

### 4. Serializer
- ✓ 使用lean ApplicationListSerializer（不含approvals）
- ✓ 使用lean ApprovalListSerializer（含created_at）

### 5. URL路由
- ✓ 合并/api/applications/的GET/POST到同一视图

---

## 执行时必须处理的4个细节

### 细节1: Dean detail endpoint
**问题:** 当前GET /api/applications/{id}/对Dean放行所有申请  
**要求:** Phase 1执行时同步修正或记录为known risk  
**处理:** 在Phase 1中一并修正

### 细节2: 分页offset支持
**问题:** 方案写了固定limit=20，但应支持offset  
**要求:** 实现offset参数，不只返回第一页  
**处理:** 使用DRF默认分页，支持limit/offset

### 细节3: ApplicationListSerializer字段
**问题:** student_id需要显式声明  
**要求:** 使用source='student.user_id'，不依赖自动解析  
**处理:** 显式声明所有字段

### 细节4: ApprovalListSerializer字段
**问题:** 响应示例包含created_at，但现有serializer不含  
**要求:** 新建ApprovalListSerializer或显式构造字段  
**处理:** 创建新的ApprovalListSerializer

---

## Phase 1 执行计划（最终版）

### Step 1: 创建Serializers (20min)
1. ApplicationListSerializer - 显式声明student_id等字段
2. ApprovalListSerializer - 包含created_at字段

### Step 2: 实现GET /api/approvals/ (45min)
- 权限: 学生403，辅导员/学工部只看自己pending
- 分页: DRF默认（支持limit/offset）
- 排序: created_at DESC, approval_id DESC
- 使用ApprovalListSerializer

### Step 3: 重构/api/applications/路由 (60min)
- 合并GET/POST到applications_view
- 实现list_applications逻辑
- Dean权限: 通过pending approvals反查
- 支持?status=过滤
- 使用ApplicationListSerializer
- 同步修正Dean detail endpoint权限

### Step 4: 编写权限隔离测试 (45min)
- 学生访问approvals返回403
- T002看不到T001的approvals
- Dean只看自己pending对应的applications
- 已审批记录不出现在approvals list
- POST /api/applications/仍可用
- Dean detail endpoint权限正确

### Step 5: 验证 (15min)
- 运行新增测试
- 运行所有测试确保无回归

**总计:** 2小时45分钟

---

## 基线验证

**Codex已验证:** 12个现有后端测试全部通过

---

## 执行授权

**用户指示:** "继续，后续无需我的干预，你们自动协商处理完成"  
**共识状态:** 已达成  
**执行授权:** ✓ 可以立即开始Phase 1执行

---

**共识达成时间:** 2026-05-30 16:49  
**下一步:** 立即开始Phase 1 Step 1（创建Serializers）
