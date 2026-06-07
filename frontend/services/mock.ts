// Mock fixtures from Week 3 API samples
// Use for frontend development without backend

import type {
  LoginResponse,
  Application,
  ApplicationDetail,
  ApprovalListItem,
  PaginatedResponse,
} from '../types/api';

export const mockLoginStudent: LoginResponse = {
  access_token: 'mock_token_student',
  token_type: 'Bearer',
  user: {
    user_id: '2020001',
    name: '张三',
    role: 'student',
    class_id: 'CS2020-01',
  },
};

export const mockLoginCounselor: LoginResponse = {
  access_token: 'mock_token_counselor',
  token_type: 'Bearer',
  user: {
    user_id: 'T001',
    name: '李老师',
    role: 'counselor',
    class_id: null,
  },
};

export const mockApplicationsList: PaginatedResponse<Application> = {
  count: 1,
  results: [
    {
      application_id: 'app_eb41d2f5',
      student_id: '2020001',
      student_name: '张三',
      class_id: 'CS2020-01',
      reason: '毕业离校',
      leave_date: '2024-06-30',
      status: 'pending_counselor',
      created_at: '2026-05-31T02:41:15.925017+08:00',
      updated_at: '2026-05-31T02:41:15.925069+08:00',
    },
  ],
};

export const mockApplicationDetail: ApplicationDetail = {
  application_id: 'app_eb41d2f5',
  student_id: '2020001',
  student_name: '张三',
  class_id: 'CS2020-01',
  reason: '毕业离校',
  leave_date: '2024-06-30',
  status: 'pending_counselor',
  dorm_checkout_status: 'completed',
  approvals: [
    {
      approval_id: 'apv_c9f566c2',
      application_id: 'app_eb41d2f5',
      step: 'counselor',
      approver_id: 'T001',
      approver_name: '李老师',
      decision: 'pending',
      comment: null,
      decided_at: null,
    },
  ],
  created_at: '2026-05-31T02:41:15.925017+08:00',
  updated_at: '2026-05-31T02:41:15.925069+08:00',
};

export const mockApprovalsList: PaginatedResponse<ApprovalListItem> = {
  count: 1,
  results: [
    {
      approval_id: 'apv_c9f566c2',
      application_id: 'app_eb41d2f5',
      step: 'counselor',
      approver_id: 'T001',
      approver_name: '李老师',
      decision: 'pending',
      created_at: '2026-05-31T02:41:15.930214+08:00',
    },
  ],
};
