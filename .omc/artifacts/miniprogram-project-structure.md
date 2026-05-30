# Mini-Program Project Structure

**Version:** v0.1 Narrow Slice  
**Tech Stack:** Native WeChat Mini Program + TypeScript

---

## Directory Structure

```
miniprogram/
├── pages/
│   ├── login/              # 登录页
│   │   ├── login.ts
│   │   ├── login.wxml
│   │   ├── login.wxss
│   │   └── login.json
│   ├── approvals/          # 待审批列表（辅导员/学工部）
│   │   ├── approvals.ts
│   │   ├── approvals.wxml
│   │   ├── approvals.wxss
│   │   └── approvals.json
│   ├── applications/       # 我的申请（学生）
│   │   ├── applications.ts
│   │   ├── applications.wxml
│   │   ├── applications.wxss
│   │   └── applications.json
│   └── detail/             # 申请详情
│       ├── detail.ts
│       ├── detail.wxml
│       ├── detail.wxss
│       └── detail.json
├── services/
│   ├── api.ts              # API client (baseUrl, JWT, error handling)
│   └── mock.ts             # Mock fixtures from Week 3 samples
├── stores/
│   └── auth.ts             # Auth store (token, user, role)
├── types/
│   └── api.ts              # TypeScript types from v0.2 contract
├── utils/
│   ├── request.ts          # wx.request wrapper
│   └── config.ts           # Environment config (dev/mock/prod)
├── app.ts                  # App entry
├── app.json                # App config (pages, window, tabBar)
├── app.wxss                # Global styles
├── project.config.json     # WeChat DevTools config
└── tsconfig.json           # TypeScript config
```

---

## Key Files

### 1. services/api.ts

**Responsibilities:**
- Base URL management (dev: localhost:8001, prod: HTTPS)
- JWT token injection (Authorization: Bearer)
- 401 handling (redirect to login)
- Error normalization (map HTTP status to user messages)
- Loading state management

**API Methods:**
```typescript
login(userId: string, password: string): Promise<LoginResponse>
getApprovals(limit?: number, offset?: number): Promise<ApprovalsResponse>
getApplications(limit?: number, offset?: number): Promise<ApplicationsResponse>
getApplicationDetail(id: number): Promise<ApplicationDetailResponse>
approveApplication(approvalId: number, comment?: string): Promise<ApprovalResponse>
```

---

### 2. stores/auth.ts

**State:**
- token: string | null
- user: User | null (user_id, name, role)
- isLoggedIn: boolean

**Methods:**
- login(userId, password): save token + user to wx.storage
- logout(): clear token + user
- getToken(): read from wx.storage
- getUser(): read from wx.storage
- checkAuth(): verify token exists, redirect if not

---

### 3. types/api.ts

**Types from v0.2 contract:**
```typescript
interface LoginRequest { user_id: string; password: string }
interface LoginResponse { access_token: string; user: User }
interface User { user_id: string; name: string; role: 'student' | 'counselor' | 'dean' }
interface Application { application_id: number; student: string; reason: string; leave_date: string; status: string; created_at: string; updated_at: string }
interface Approval { approval_id: number; application: ApplicationSummary; approver: string; role: string; decision: string; comment: string | null; decided_at: string | null }
interface PaginatedResponse<T> { count: number; next: string | null; previous: string | null; results: T[] }
```

---

### 4. utils/config.ts

**Environment config:**
```typescript
const ENV = 'dev'; // 'dev' | 'mock' | 'prod'

const config = {
  dev: { baseUrl: 'http://localhost:8001' },
  mock: { baseUrl: '', useMock: true },
  prod: { baseUrl: 'https://api.example.com' }
};

export const BASE_URL = config[ENV].baseUrl;
export const USE_MOCK = config[ENV].useMock || false;
```

---

## Page Flow

### Login Flow
1. User enters user_id + password
2. Call `api.login()`
3. Save token + user to auth store
4. Redirect based on role:
   - student → /pages/applications/applications
   - counselor/dean → /pages/approvals/approvals

### Approvals Flow (Counselor/Dean)
1. Load pending approvals: `api.getApprovals()`
2. Display list with student name, reason, leave_date
3. Click item → navigate to detail with application_id
4. Detail page: `api.getApplicationDetail(id)`
5. Click "通过" → `api.approveApplication(approvalId, comment)`
6. Success → navigate back to list, refresh

### Applications Flow (Student)
1. Load own applications: `api.getApplications()`
2. Display list with reason, leave_date, status
3. Click item → navigate to detail
4. Detail page shows approval progress

---

## Mock Mode

**Mock fixtures location:** `services/mock.ts`

**Data source:** Week 3 API samples (`.omc/artifacts/api-samples/*.json`)

**Mock responses:**
- login-student.json → student login
- login-counselor.json → counselor login
- list-approvals-counselor.json → pending approvals
- list-applications-student.json → student applications
- get-application-detail.json → detail with approvals
- approve.json → approve success
- error-conflict.json → 409 error

---

## Development Workflow

1. **Setup:** Init project in WeChat DevTools with TypeScript
2. **Config:** Set baseUrl to localhost:8001, enable "不校验合法域名"
3. **Types:** Copy types from v0.2 contract
4. **API Client:** Implement request wrapper + error handling
5. **Auth Store:** Implement token storage + user management
6. **Login:** Build login page + integration
7. **Lists:** Build approvals/applications lists
8. **Detail:** Build detail page
9. **Approve:** Implement approve action
10. **Test:** Follow acceptance checklist

---

**Next:** Start skeleton setup in WeChat DevTools
