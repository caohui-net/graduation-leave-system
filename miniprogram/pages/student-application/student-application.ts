import { createDefaultApiClient, formatApiError } from '../../services/api';

const app = getApp<IAppOption>();
const apiClient = createDefaultApiClient();

Page({
  data: {
    reason: '',
    leaveDate: '',
    submitting: false,
    error: '',
    today: new Date().toISOString().split('T')[0],
  },

  onLoad() {
    const userInfo = app.globalData.userInfo;
    if (!userInfo) {
      wx.reLaunch({ url: '/pages/login/login' });
      return;
    }
    if (userInfo.role !== 'student') {
      wx.showToast({ title: '无权限访问', icon: 'none' });
      wx.redirectTo({ url: '/pages/approvals/approvals' });
      return;
    }
  },

  onShow() {
    const userInfo = app.globalData.userInfo;
    if (!userInfo || userInfo.role !== 'student') {
      wx.reLaunch({ url: '/pages/login/login' });
      return;
    }
  },

  onReasonInput(e: any) {
    this.setData({ reason: e.detail.value });
  },

  onDateChange(e: any) {
    this.setData({ leaveDate: e.detail.value });
  },

  onSubmit() {
    const { reason, leaveDate } = this.data;

    if (!reason || !reason.trim()) {
      this.setData({ error: '请输入离校原因' });
      return;
    }
    if (reason.trim().length > 500) {
      this.setData({ error: '离校原因不能超过500字' });
      return;
    }
    if (!leaveDate) {
      this.setData({ error: '请选择离校日期' });
      return;
    }
    const today = new Date().toISOString().split('T')[0];
    if (leaveDate < today) {
      this.setData({ error: '离校日期不能早于今天' });
      return;
    }

    this.submitApplication();
  },

  async submitApplication() {
    this.setData({ submitting: true, error: '' });
    wx.showLoading({ title: '提交中', mask: true });

    try {
      const res = await apiClient.createApplication({
        reason: this.data.reason.trim(),
        leave_date: this.data.leaveDate
      });

      wx.hideLoading();
      wx.showToast({ title: '提交成功', icon: 'success', duration: 500, mask: true });

      setTimeout(() => {
        wx.redirectTo({
          url: `/pages/detail/detail?id=${encodeURIComponent(res.application_id)}`
        });
      }, 500);
    } catch (err: any) {
      wx.hideLoading();
      const errorMsg = formatApiError(err, {
        DORM_BLOCKED: (d) => `宿舍清退未完成：${d?.blocking_reason || '请联系宿管'}`,
        CONFLICT: (d) => {
          if (d?.existing_application_id) {
            setTimeout(() => {
              wx.redirectTo({
                url: `/pages/detail/detail?id=${encodeURIComponent(d.existing_application_id)}`
              });
            }, 500);
            return '您已有待审批或已通过的申请，正在跳转...';
          }
          return '您已有待审批或已通过的申请';
        },
        VALIDATION_ERROR: (d) => typeof d === 'string' ? d : '表单验证失败',
      });
      this.setData({ error: errorMsg, submitting: false });
    }
  },
});
