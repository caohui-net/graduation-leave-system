// 微信API Promise化工具
export function promisify(api) {
  return (options = {}) => {
    return new Promise((resolve, reject) => {
      api({
        ...options,
        success: resolve,
        fail: reject
      });
    });
  };
}

// Promise化的微信API
export const wxRequest = promisify(wx.request);
export const wxDownloadFile = promisify(wx.downloadFile);
export const wxUploadFile = promisify(wx.uploadFile);
