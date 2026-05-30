import { ApiClient } from '../../services/api';
import type { ApprovalListItem } from '../../types/api';

const app = getApp<IAppOption>();

const apiClient = new ApiClient({
  baseUrl: 'http://localhost:8001',
  getToken: () => app.globalData.token,
  onUnauthorized: () => {
    wx.removeStorageSync('token');
    wx.removeStorageSync('userInfo');
    app.globalData.token = '';
    app.globalData.userInfo = null;
    wx.reLaunch({ url: '/pages/login/login' });
  },
});

Page({
  data: {
    approvals: [] as ApprovalListItem[],
    loading: true,
    error: '',
    userInfo: { name: '', role: '' },
    roleText: '',
  },

  onLoad() {
    const userInfo = app.globalData.userInfo;
    if (!userInfo) {
      wx.reLaunch({ url: '/pages/login/login' });
      return;
    }

    const roleMap: Record<string, string> = {
      student: '学生',
      counselor: '辅导员',
      dean: '院长',
    };

    this.setData({
      userInfo,
      roleText: roleMap[userInfo.role] || userInfo.role,
    });

    this.loadApprovals();
  },

  async loadApprovals() {
    this.setData({ loading: true, error: '' });

    try {
      const res = await apiClient.listApprovals('pending', 20, 0);
      this.setData({
        approvals: res.results,
        loading: false,
      });
    } catch (err: any) {
      this.setData({
        error: err.error?.message || err.message || '加载失败',
        loading: false,
      });
    }
  },

  onItemTap(e: any) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({ url: `/pages/detail/detail?id=${id}` });
  },

  onRetry() {
    this.loadApprovals();
  },
});
