import { createDefaultApiClient } from '../../services/api';
import type { ApprovalListItem } from '../../types/api';
import { checkRoleAndRedirect } from '../../utils/role-guard';

const app = getApp<IAppOption>();
const apiClient = createDefaultApiClient();

Page({
  data: {
    approvals: [] as ApprovalListItem[],
    loading: true,
    error: '',
    userInfo: { name: '', role: '' },
    roleText: '',
  },

  onLoad() {
    if (checkRoleAndRedirect(app.globalData.userInfo, ['counselor', 'dean'])) return;

    const userInfo = app.globalData.userInfo!;
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

  onShow() {
    if (checkRoleAndRedirect(app.globalData.userInfo, ['counselor', 'dean'])) return;
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
