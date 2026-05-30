App({
  globalData: {
    token: '',
    userInfo: null as { user_id: string; name: string; role: string } | null,
  },

  onLaunch() {
    const token = wx.getStorageSync('token');
    const userInfo = wx.getStorageSync('userInfo');
    if (token) {
      this.globalData.token = token;
      this.globalData.userInfo = userInfo;
    }
  },
});
