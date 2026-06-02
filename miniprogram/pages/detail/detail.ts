import { createDefaultApiClient, formatApiError } from '../../services/api';
import type { ApplicationDetail, Attachment, AttachmentType } from '../../types/api';

const app = getApp<IAppOption>();
const apiClient = createDefaultApiClient();

Page({
  data: {
    detail: null as ApplicationDetail | null,
    loading: true,
    error: '',
    canApprove: false,
    statusText: '',
    decisionText: {
      pending: '待审批',
      approved: '已通过',
      rejected: '已拒绝',
    },
    applicationId: '',
    pendingApprovalId: '',
    attachments: [] as Attachment[],
    uploading: false,
    attachmentError: '',
    isOwner: false,
    approvalComment: '',
  },

  onLoad(options: any) {
    const userInfo = app.globalData.userInfo;
    if (!userInfo) {
      wx.reLaunch({ url: '/pages/login/login' });
      return;
    }

    const id = options.id;
    if (!id) {
      this.setData({ error: '缺少申请ID' });
      return;
    }

    this.setData({ applicationId: id });
    this.loadDetail();
  },

  async loadDetail() {
    this.setData({ loading: true, error: '' });

    try {
      const detail = await apiClient.getApplication(this.data.applicationId);

      const statusMap: Record<string, string> = {
        draft: '草稿',
        pending_counselor: '待辅导员审批',
        pending_dean: '待院长审批',
        approved: '已通过',
        rejected: '已拒绝',
      };

      const userInfo = app.globalData.userInfo!;
      const pendingApproval = detail.approvals.find(
        (a) => a.decision === 'pending' && a.approver_id === userInfo.user_id
      );

      const isOwner = userInfo.role === 'student' && detail.student_id === userInfo.user_id;

      this.setData({
        detail,
        statusText: statusMap[detail.status] || detail.status,
        canApprove: !!pendingApproval,
        pendingApprovalId: pendingApproval?.approval_id || '',
        isOwner,
        loading: false,
      });

      this.loadAttachments();
    } catch (err: any) {
      this.setData({
        error: err.error?.message || err.message || '加载失败',
        loading: false,
      });
    }
  },

  async loadAttachments() {
    try {
      const attachments = await apiClient.listAttachments(this.data.applicationId);
      this.setData({ attachments, attachmentError: '' });
    } catch (err: any) {
      console.error('加载附件失败:', err);
      this.setData({
        attachments: [],
        attachmentError: formatApiError(err) || '附件加载失败',
      });
    }
  },

  onApprove() {
    wx.showModal({
      title: '确认通过',
      content: '确定要通过此申请吗？',
      success: (res) => {
        if (res.confirm) {
          this.performAction('approve');
        }
      },
    });
  },

  onReject() {
    wx.showModal({
      title: '确认拒绝',
      content: '确定要拒绝此申请吗？',
      success: (res) => {
        if (res.confirm) {
          this.performAction('reject');
        }
      },
    });
  },

  onCommentInput(e: any) {
    this.setData({ approvalComment: e.detail.value });
  },

  async performAction(action: 'approve' | 'reject') {
    wx.showLoading({ title: '处理中...' });

    try {
      const approvalId = this.data.pendingApprovalId;
      const comment = this.data.approvalComment.trim();

      if (action === 'approve') {
        await apiClient.approveApproval(approvalId, { comment });
      } else {
        await apiClient.rejectApproval(approvalId, { comment });
      }

      wx.hideLoading();
      wx.showToast({
        title: action === 'approve' ? '已通过' : '已拒绝',
        icon: 'success',
      });

      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
    } catch (err: any) {
      wx.hideLoading();
      wx.showToast({
        title: err.error?.message || err.message || '操作失败',
        icon: 'none',
      });
    }
  },

  onChooseFile() {
    wx.chooseMessageFile({
      count: 1,
      type: 'file',
      success: (res) => {
        const file = res.tempFiles[0];

        // 文件大小检查
        if (file.size > 10 * 1024 * 1024) {
          wx.showToast({ title: '文件大小不能超过10MB', icon: 'none' });
          return;
        }

        // 文件类型预检（带兜底）
        const fileName = (file.name || file.path || '').toLowerCase();
        if (!fileName) {
          wx.showToast({ title: '无法识别文件类型', icon: 'none' });
          return;
        }

        const allowedExts = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx'];
        if (!allowedExts.some(ext => fileName.endsWith(ext))) {
          wx.showToast({
            title: '不支持的文件类型，仅支持图片、PDF、Word文档',
            icon: 'none',
            duration: 2000
          });
          return;
        }

        this.showAttachmentTypeDialog(file.path);
      },
    });
  },

  showAttachmentTypeDialog(filePath: string) {
    wx.showActionSheet({
      itemList: ['宿舍清退证明', '图书馆清书证明', '财务结清证明', '其他'],
      success: (res) => {
        const types: AttachmentType[] = ['dorm_checkout', 'library_clearance', 'finance_clearance', 'other'];
        this.uploadFile(filePath, types[res.tapIndex]);
      },
    });
  },

  async uploadFile(filePath: string, attachmentType: AttachmentType) {
    this.setData({ uploading: true, attachmentError: '' });
    wx.showLoading({ title: '上传中...', mask: true });

    try {
      await apiClient.uploadAttachment(this.data.applicationId, filePath, attachmentType);
      wx.hideLoading();
      wx.showToast({ title: '上传成功', icon: 'success' });
      this.setData({ uploading: false });
      this.loadAttachments();
    } catch (err: any) {
      wx.hideLoading();
      const errorMsg = formatApiError(err, {
        VALIDATION_ERROR: (d) => d?.file?.[0] || d?.attachment_type?.[0] || '文件验证失败',
      });
      this.setData({ uploading: false, attachmentError: errorMsg });
      wx.showToast({ title: errorMsg, icon: 'none' });
    }
  },

  onDeleteAttachment(e: any) {
    const attachmentId = e.currentTarget.dataset.id;
    wx.showModal({
      title: '确认删除',
      content: '确定要删除此附件吗？',
      success: (res) => {
        if (res.confirm) {
          this.deleteAttachment(attachmentId);
        }
      },
    });
  },

  async deleteAttachment(attachmentId: string) {
    wx.showLoading({ title: '删除中...' });

    try {
      await apiClient.deleteAttachment(attachmentId);
      wx.hideLoading();
      wx.showToast({ title: '删除成功', icon: 'success' });
      this.loadAttachments();
    } catch (err: any) {
      wx.hideLoading();
      wx.showToast({ title: err.error?.message || '删除失败', icon: 'none' });
    }
  },

  onDownloadAttachment(e: any) {
    const attachment = e.currentTarget.dataset.attachment as Attachment;
    const url = apiClient.getDownloadUrl(attachment.attachment_id);
    const token = app.globalData.token;

    wx.downloadFile({
      url,
      header: token ? { Authorization: `Bearer ${token}` } : {},
      success: (res) => {
        if (res.statusCode === 401) {
          apiClient.handleUnauthorized();
          return;
        }
        if (res.statusCode === 403) {
          wx.showToast({ title: '无权限下载附件', icon: 'none' });
          return;
        }
        if (res.statusCode === 404) {
          wx.showToast({ title: '附件不存在或已删除', icon: 'none' });
          return;
        }
        if (res.statusCode === 200) {
          const filePath = res.tempFilePath;
          if (attachment.content_type.startsWith('image/')) {
            wx.previewImage({
              urls: [filePath],
              current: filePath,
              fail: () => wx.showToast({ title: '预览失败', icon: 'none' })
            });
          } else {
            wx.openDocument({
              filePath,
              showMenu: true,
              fail: () => wx.showToast({ title: '打开失败', icon: 'none' })
            });
          }
        } else {
          wx.showToast({ title: '下载失败', icon: 'none' });
        }
      },
      fail: () => {
        wx.showToast({ title: '下载失败', icon: 'none' });
      },
    });
  },

  onRetry() {
    this.loadDetail();
  },
});
