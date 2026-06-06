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
    currentTab: 'pending' as 'all' | 'pending' | 'approved',
  },

  onLoad() {
    if (checkRoleAndRedirect(app.globalData.userInfo, ['dorm_manager', 'counselor', 'dean', 'admin'])) return;

    const userInfo = app.globalData.userInfo!;
    const roleMap: Record<string, string> = {
      student: '学生',
      dorm_manager: '宿管员',
      counselor: '辅导员',
      dean: '学工部',
      admin: '学工管理员',
    };

    this.setData({
      userInfo,
      roleText: roleMap[userInfo.role] || userInfo.role,
    });

    this.loadApprovals();
  },

  onShow() {
    if (checkRoleAndRedirect(app.globalData.userInfo, ['dorm_manager', 'counselor', 'dean', 'admin'])) return;
    this.loadApprovals();
  },

  onTabChange(e: any) {
    const tab = e.currentTarget.dataset.tab as 'all' | 'pending' | 'approved';
    this.setData({ currentTab: tab });
    this.loadApprovals();
  },

  async loadApprovals() {
    this.setData({ loading: true, error: '' });
    const decision = this.data.currentTab === 'all' ? 'all' :
                     this.data.currentTab === 'pending' ? 'pending' : 'approved';

    try {
      const res = await apiClient.listApprovals(decision, 20, 0);
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
