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
      throw data as ApiError;
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
