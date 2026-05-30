// API Types based on v0.2 Contract
// Generated: 2026-05-31

export type UserRole = 'student' | 'counselor' | 'dean';

export type ApplicationStatus =
  | 'draft'
  | 'pending_counselor'
  | 'pending_dean'
  | 'approved'
  | 'rejected';

export type ApprovalDecision = 'pending' | 'approved' | 'rejected';

export type ApprovalStep = 'counselor' | 'dean';

// Auth
export interface LoginRequest {
  user_id: string;
  password: string;
}

export interface User {
  user_id: string;
  name: string;
  role: UserRole;
}

export interface LoginResponse {
  access_token: string;
  user: User;
}

// Applications
export interface ApplicationCreateRequest {
  reason: string;
  leave_date: string; // YYYY-MM-DD
}

export interface Application {
  application_id: string;
  student_id: string;
  reason: string;
  leave_date: string;
  status: ApplicationStatus;
  created_at: string;
  updated_at: string;
}

export interface ApplicationDetail extends Application {
  student_name: string;
  class_id: string;
  dorm_checkout_status: string;
  approvals: ApprovalDetail[];
}

// Approvals
export interface ApprovalDetail {
  approval_id: string;
  application_id: string;
  step: ApprovalStep;
  approver_id: string;
  approver_name: string;
  decision: ApprovalDecision;
  comment: string | null;
  decided_at: string | null;
}

export interface ApprovalListItem {
  approval_id: string;
  application_id: string;
  step: ApprovalStep;
  approver_id: string;
  approver_name: string;
  decision: ApprovalDecision;
  created_at: string;
}

export interface ApprovalActionRequest {
  comment?: string;
}

export interface ApprovalActionResponse {
  approval_id: string;
  decision: ApprovalDecision;
  comment: string | null;
  decided_at: string;
}

// Pagination
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Errors
export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: any;
  };
}
