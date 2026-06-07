# Phase 4B修复方案 - 最终共识

**日期：** 2026-06-01  
**参与方：** Codex + Claude

---

## 审查结论

**有条件通过，需3个调整后立即执行。**

Codex确认：
- 5个问题方向正确
- P1优先、P2次之合理
- 需补充3个调整点

---

## 必须调整的问题

### 1. P1-1测试日期修复范围扩展

**Codex指出：**
- 4个Django测试文件覆盖当前7个失败点
- 但`tests/smoke_test.sh`和`tests/test_p0_fixes.sh`也有固定`2024-06-30`
- 后续smoke验收会失败

**Claude接受：**
扩展修复范围到6个文件：
- backend/apps/applications/tests/test_application_flow.py
- backend/apps/applications/tests/test_error_cases.py
- backend/apps/applications/tests/test_constraints.py
- backend/apps/approvals/tests/test_rejection_flow.py
- **tests/smoke_test.sh** (新增)
- **tests/test_p0_fixes.sh** (新增)

---

### 2. P1-2/P1-3避免重复跳转

**Codex指出：**
- 不会形成循环跳转（角色矩阵正确）
- 但onLoad和onShow都可能触发跳转，出现重复redirectTo
- 建议加redirecting guard或抽取角色守卫函数

**Claude接受：**
抽取角色守卫函数，确保一次生命周期只跳转一次：

```typescript
// miniprogram/utils/role-guard.ts (新建)
let isRedirecting = false;

export function checkRoleAndRedirect(
  userInfo: any | null,
  allowedRoles: string[]
): boolean {
  if (isRedirecting) return true;
  
  if (!userInfo) {
    isRedirecting = true;
    wx.reLaunch({ url: '/pages/login/login' });
    setTimeout(() => { isRedirecting = false; }, 500);
    return true;
  }
  
  if (!allowedRoles.includes(userInfo.role)) {
    isRedirecting = true;
    const targetUrl = userInfo.role === 'student' 
      ? '/pages/student-application/student-application'
      : '/pages/approvals/approvals';
    wx.redirectTo({ url: targetUrl });
    setTimeout(() => { isRedirecting = false; }, 500);
    return true;
  }
  
  return false;
}
```

使用方式：
```typescript
// student-application.ts
import { checkRoleAndRedirect } from '../../utils/role-guard';

onLoad() {
  if (checkRoleAndRedirect(app.globalData.userInfo, ['student'])) return;
  // 继续页面逻辑
}

onShow() {
  if (checkRoleAndRedirect(app.globalData.userInfo, ['student'])) return;
}
```

---

### 3. P2-4日期helper严格对齐Asia/Shanghai

**Codex指出：**
- `getFullYear()/getMonth()/getDate()`对中国用户通常没问题
- 但后端明确`TIME_ZONE = 'Asia/Shanghai'`
- 设备时区非中国时区仍可能错位
- 建议命名为`getShanghaiDateString()`，用UTC+8生成
- onShow同步刷新today，避免跨午夜后picker的start变旧

**Claude接受：**
```typescript
// miniprogram/utils/date.ts
export function getShanghaiDateString(): string {
  const now = new Date();
  const utc = now.getTime() + now.getTimezoneOffset() * 60000;
  const shanghai = new Date(utc + 8 * 3600000);
  
  const year = shanghai.getFullYear();
  const month = String(shanghai.getMonth() + 1).padStart(2, '0');
  const day = String(shanghai.getDate()).padStart(2, '0');
  
  return `${year}-${month}-${day}`;
}
```

使用方式：
```typescript
// student-application.ts
import { getShanghaiDateString } from '../../utils/date';

data: {
  today: getShanghaiDateString(),
},

onShow() {
  // 刷新today，避免跨午夜后变旧
  this.setData({ today: getShanghaiDateString() });
  // 角色保护...
}

onSubmit() {
  const today = getShanghaiDateString();
  if (leaveDate < today) {
    this.setData({ error: '离校日期不能早于今天' });
    return;
  }
}
```

---

## 其他确认

- **P2-5快速修复可接受：** 显示`申请 {{application_id}}`属于MVP级别，真正显示学生信息可放Phase 4C
- **执行顺序合理：** P1-1后端测试 → P1-2/P1-3角色保护 → P2-4日期helper → P2-5列表UI
- **时间估算调整：** 65分钟偏乐观，更现实是**75-90分钟**（含smoke脚本、guard函数、手工验证）

---

## 最终修改清单

**后端（6个文件）：**
1. backend/apps/applications/tests/test_application_flow.py - 动态日期
2. backend/apps/applications/tests/test_error_cases.py - 动态日期
3. backend/apps/applications/tests/test_constraints.py - 动态日期
4. backend/apps/approvals/tests/test_rejection_flow.py - 动态日期
5. **tests/smoke_test.sh** - 动态日期（新增）
6. **tests/test_p0_fixes.sh** - 动态日期（新增）

**前端（6个文件）：**
1. **miniprogram/utils/role-guard.ts** - 新建角色守卫函数
2. **miniprogram/utils/date.ts** - 新建Asia/Shanghai日期helper
3. miniprogram/pages/student-application/student-application.ts - 使用role-guard + date helper
4. miniprogram/pages/approvals/approvals.ts - 使用role-guard
5. miniprogram/pages/detail/detail.ts - 使用role-guard（如需要）
6. miniprogram/pages/approvals/approvals.wxml - 快速修复列表显示

**总计：12个文件（6后端 + 6前端）**

---

## 执行授权

**Codex授权：** 可以立即执行，带上3个修正条件  
**Claude确认：** 接受全部3个调整，立即执行

**预计时间：** 75-90分钟

---

## 验证标准

1. 后端测试：14个Django测试全部通过
2. Smoke测试：tests/smoke_test.sh通过
3. 角色保护：手工验证无重复跳转
4. 日期对齐：跨午夜验证today自动刷新
5. 列表UI：审批列表显示申请ID而非审批人名
