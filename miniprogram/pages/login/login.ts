import { createDefaultApiClient } from '../../services/api';

const app = getApp<IAppOption>();
const apiClient = createDefaultApiClient();

Page({
  data: {
    userId: '',
    password: '',
    loading: false,
    error: '',
  },

  onUserIdInput(e: any) {
    this.setData({ userId: e.detail.value });
  },

  onPasswordInput(e: any) {
    this.setData({ password: e.detail.value });
  },

  async onLogin() {
    const { userId, password } = this.data;

    if (!userId || !password) {
      this.setData({ error: '请输入用户ID和密码' });
      return;
    }

    this.setData({ loading: true, error: '' });

    try {
      const res = await apiClient.login({ user_id: userId, password });

      wx.setStorageSync('token', res.access_token);
      wx.setStorageSync('userInfo', res.user);
      app.globalData.token = res.access_token;
      app.globalData.userInfo = res.user;

      if (res.user.role === 'student') {
        wx.redirectTo({ url: '/pages/student-application/student-application' });
      } else if (res.user.role === 'counselor' || res.user.role === 'dean') {
        wx.redirectTo({ url: '/pages/approvals/approvals' });
      } else {
        wx.removeStorageSync('token');
        wx.removeStorageSync('userInfo');
        app.globalData.token = '';
        app.globalData.userInfo = null;
        this.setData({ error: '角色错误', loading: false });
      }
    } catch (err: any) {
      this.setData({
        error: err.error?.message || err.message || '登录失败',
        loading: false,
      });
    }
  },
});
