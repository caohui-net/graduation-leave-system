// 小程序审批详情页面逻辑
import { wxRequest, wxDownloadFile } from '../../utils/request';
import { buildPreviewUrl, buildDownloadUrl } from '../../utils/attachment';

const app = getApp();

Page({
  data: {
    approval: null,
  },

  onLoad(options) {
    const approvalId = options.id;
    this.loadApprovalDetail(approvalId);
  },

  // 加载审批详情
  async loadApprovalDetail(approvalId) {
    wx.showLoading({ title: '加载中...' });
    try {
      const res = await wxRequest({
        url: `${app.globalData.apiBase}/api/approvals/${approvalId}/`,
        method: 'GET',
        header: {
          'Authorization': `Bearer ${app.globalData.token}`
        }
      });
      this.setData({ approval: res.data });
    } catch (error) {
      wx.showToast({ title: '加载失败', icon: 'none' });
    } finally {
      wx.hideLoading();
    }
  },

  // 附件预览
  async handlePreview(e) {
    const attachmentId = e.currentTarget.dataset.id;
    const url = buildPreviewUrl(app.globalData.apiBase, attachmentId);

    try {
      const res = await wxDownloadFile({
        url: url,
        header: {
          'Authorization': `Bearer ${app.globalData.token}`
        }
      });
      const filePath = res.tempFilePath;
      const fileType = this.getFileType(filePath);

      // 根据文件类型预览
      if (fileType === 'image') {
        wx.previewImage({
          urls: [filePath],
          current: filePath
        });
      } else if (fileType === 'pdf' || fileType === 'doc') {
        wx.openDocument({
          filePath: filePath,
          showMenu: true
        });
      } else {
        wx.showToast({ title: '不支持预览此文件类型', icon: 'none' });
      }
    } catch (error) {
      wx.showToast({ title: '预览失败', icon: 'none' });
    }
  },

  // 下载附件
  async handleDownload(e) {
    const attachmentId = e.currentTarget.dataset.id;
    const url = buildDownloadUrl(app.globalData.apiBase, attachmentId);

    try {
      const res = await wxDownloadFile({
        url: url,
        header: {
          'Authorization': `Bearer ${app.globalData.token}`
        }
      });
      wx.saveFile({
        tempFilePath: res.tempFilePath,
        success: () => {
          wx.showToast({ title: '下载成功', icon: 'success' });
        }
      });
    } catch (error) {
      wx.showToast({ title: '下载失败', icon: 'none' });
    }
  },

  // 判断文件类型
  getFileType(filePath) {
    const ext = filePath.split('.').pop().toLowerCase();
    if (['jpg', 'jpeg', 'png', 'gif'].includes(ext)) return 'image';
    if (ext === 'pdf') return 'pdf';
    if (['doc', 'docx'].includes(ext)) return 'doc';
    return 'other';
  },

  // 通过审批
  handleApprove() {
    wx.showModal({
      title: '确认通过',
      content: '确定通过该申请吗？',
      success: (res) => {
        if (res.confirm) {
          this.submitApproval('approve');
        }
      }
    });
  },

  // 驳回审批
  handleReject() {
    wx.showModal({
      title: '确认驳回',
      content: '确定驳回该申请吗？',
      success: (res) => {
        if (res.confirm) {
          this.submitApproval('reject');
        }
      }
    });
  },

  // 提交审批
  async submitApproval(action) {
    wx.showLoading({ title: '提交中...' });
    try {
      await wxRequest({
        url: `${app.globalData.apiBase}/api/approvals/${this.data.approval.approval_id}/${action}/`,
        method: 'POST',
        header: {
          'Authorization': `Bearer ${app.globalData.token}`
        },
        data: { comment: '' }
      });
      wx.showToast({ title: '提交成功', icon: 'success' });
      setTimeout(() => wx.navigateBack(), 1500);
    } catch (error) {
      wx.showToast({ title: '提交失败', icon: 'none' });
    } finally {
      wx.hideLoading();
    }
  }
});
