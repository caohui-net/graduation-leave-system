// API Client for v0.2 Contract
// Minimal implementation - can be extended

import type {
  LoginRequest,
  LoginResponse,
  ApplicationCreateRequest,
  ApplicationDetail,
  Application,
  ApprovalListItem,
  ApprovalActionRequest,
  ApprovalActionResponse,
  PaginatedResponse,
  ApiError,
} from '../types/api';

export class ApiClientError extends Error {
  code: string;
  details?: any;

  constructor(message: string, code: string, details?: any) {
    super(message);
    this.name = 'ApiClientError';
    this.code = code;
    this.details = details;
  }
}

export interface ApiConfig {
  baseUrl: string;
  getToken?: () => string | null;
  onUnauthorized?: () => void;
}

export class ApiClient {
  private config: ApiConfig;

  constructor(config: ApiConfig) {
    this.config = config;
  }

  private extractErrorMessage(apiError: ApiError): string {
    const { error } = apiError;

    // 字段名映射（英文 -> 中文）
    const fieldNames: Record<string, string> = {
      contact_phone: '联系电话',
      leave_date: '离校日期',
      reason: '离校原因',
      file: '附件',
      user_id: '用户ID',
      password: '密码',
      comment: '审批意见',
    };

    // 如果有详细错误信息（字段验证错误）
    if (error.details) {
      // 提取第一个字段的第一个错误
      const firstField = Object.keys(error.details)[0];
      if (firstField && Array.isArray(error.details[firstField])) {
        const fieldError = error.details[firstField][0];
        const fieldLabel = fieldNames[firstField] || firstField;

        // 如果错误消息已经很具体，直接返回
        if (fieldError.includes('不能') || fieldError.includes('超过') || fieldError.includes('支持')) {
          return fieldError;
        }

        // 否则加上字段名前缀
        return `${fieldLabel}：${fieldError}`;
      }
    }

    // 否则返回通用错误消息
    return error.message || '操作失败，请稍后重试';
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.config.getToken?.();
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.config.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      this.config.onUnauthorized?.();
      throw new Error('Unauthorized');
    }

    const data = await response.json();

    if (!response.ok) {
      const apiError = data as ApiError;
      const errorMessage = this.extractErrorMessage(apiError);
      throw new ApiClientError(errorMessage, apiError.error.code, apiError.error.details);
    }

    return data as T;
  }

  // Auth
  async login(req: LoginRequest): Promise<LoginResponse> {
    return this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(req),
    });
  }

  // Applications
  async createApplication(req: ApplicationCreateRequest): Promise<ApplicationDetail> {
    return this.request('/api/applications/', {
      method: 'POST',
      body: JSON.stringify(req),
    });
  }

  async listApplications(
    limit = 20,
    offset = 0
  ): Promise<PaginatedResponse<Application>> {
    return this.request(
      `/api/applications/?limit=${limit}&offset=${offset}`
    );
  }

  async getApplication(id: string): Promise<ApplicationDetail> {
    return this.request(`/api/applications/${id}/`);
  }

  // Approvals
  async listApprovals(
    decision: 'pending' | 'approved' | 'rejected' | 'all' = 'pending',
    limit = 20,
    offset = 0
  ): Promise<PaginatedResponse<ApprovalListItem>> {
    return this.request(
      `/api/approvals/?decision=${decision}&limit=${limit}&offset=${offset}`
    );
  }

  async approveApproval(
    id: string,
    req: ApprovalActionRequest
  ): Promise<ApprovalActionResponse> {
    return this.request(`/api/approvals/${id}/approve/`, {
      method: 'POST',
      body: JSON.stringify(req),
    });
  }

  async rejectApproval(
    id: string,
    req: ApprovalActionRequest
  ): Promise<ApprovalActionResponse> {
    return this.request(`/api/approvals/${id}/reject/`, {
      method: 'POST',
      body: JSON.stringify(req),
    });
  }
}
