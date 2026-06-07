import { createDefaultApiClient, formatApiError } from '../../services/api';
import { checkRoleAndRedirect } from '../../utils/role-guard';
import { getShanghaiDateString } from '../../utils/date';

const app = getApp<IAppOption>();
const apiClient = createDefaultApiClient();

Page({
  data: {
    contactPhone: '',
    reason: '',
    leaveDate: '',
    draftId: null as number | null,
    attachments: [] as any[],
    uploading: false,
    submitting: false,
    savingDraft: false,
    error: '',
    today: getShanghaiDateString(),
    userName: '',
    userId: '',
  },

  onLoad() {
    if (checkRoleAndRedirect(app.globalData.userInfo, ['student'])) return;
    const userInfo = app.globalData.userInfo;
    if (userInfo) {
      this.setData({
        userName: userInfo.name || '',
        userId: userInfo.user_id || ''
      });
    }
  },

  onShow() {
    if (checkRoleAndRedirect(app.globalData.userInfo, ['student'])) return;
    this.setData({ today: getShanghaiDateString() });
  },

  onPhoneInput(e: any) {
    this.setData({ contactPhone: e.detail.value });
  },

  onReasonInput(e: any) {
    this.setData({ reason: e.detail.value });
  },

  onDateChange(e: any) {
    this.setData({ leaveDate: e.detail.value });
  },

  async onSaveDraft() {
    const { contactPhone } = this.data;

    if (!contactPhone || !contactPhone.trim()) {
      this.setData({ error: '请输入联系电话' });
      return;
    }
    if (!/^1[3-9]\d{9}$/.test(contactPhone.trim())) {
      this.setData({ error: '请输入有效的手机号码' });
      return;
    }

    this.setData({ savingDraft: true, error: '' });
    wx.showLoading({ title: '保存中', mask: true });

    try {
      const res = await apiClient.createDraft({
        contact_phone: this.data.contactPhone.trim(),
        reason: this.data.reason.trim() || undefined,
        leave_date: this.data.leaveDate || undefined,
      });

      wx.hideLoading();
      wx.showToast({ title: '草稿已保存', icon: 'success', duration: 1500 });

      this.setData({
        draftId: res.application_id,
        savingDraft: false
      });

      this.loadAttachments();
    } catch (err: any) {
      wx.hideLoading();
      const errorMsg = formatApiError(err, {
        VALIDATION_ERROR: (d) => typeof d === 'string' ? d : '保存失败，请检查输入',
      });
      this.setData({ error: errorMsg, savingDraft: false });
    }
  },

  async loadAttachments() {
    if (!this.data.draftId) return;
    try {
      const attachments = await apiClient.listAttachments(String(this.data.draftId));
      this.setData({ attachments });
    } catch (err) {
      console.error('Failed to load attachments:', err);
    }
  },

  onChooseFile() {
    if (!this.data.draftId) {
      this.setData({ error: '请先保存草稿' });
      return;
    }

    wx.chooseMessageFile({
      count: 1,
      type: 'file',
      success: (res) => {
        const file = res.tempFiles[0];
        this.uploadFile(file.path, file.name);
      },
      fail: (err) => {
        this.setData({ error: '选择文件失败' });
      }
    });
  },

  async uploadFile(filePath: string, fileName: string) {
    this.setData({ uploading: true, error: '' });
    wx.showLoading({ title: '上传中', mask: true });

    try {
      const attachment = await apiClient.uploadAttachment(
        String(this.data.draftId),
        filePath,
        'other'
      );

      wx.hideLoading();
      wx.showToast({ title: '上传成功', icon: 'success' });

      this.setData({
        attachments: [...this.data.attachments, attachment],
        uploading: false
      });
    } catch (err: any) {
      wx.hideLoading();
      const errorMsg = formatApiError(err, {
        VALIDATION_ERROR: (d) => typeof d === 'string' ? d : '上传失败',
      });
      this.setData({ error: errorMsg, uploading: false });
    }
  },

  async onDeleteAttachment(e: any) {
    const attachmentId = e.currentTarget.dataset.id;
    if (!attachmentId) return;

    try {
      await apiClient.deleteAttachment(attachmentId);
      wx.showToast({ title: '删除成功', icon: 'success' });

      this.setData({
        attachments: this.data.attachments.filter(a => a.attachment_id !== attachmentId)
      });
    } catch (err) {
      this.setData({ error: '删除失败' });
    }
  },

  onSubmit() {
    const { contactPhone, reason, leaveDate } = this.data;

    if (!contactPhone || !contactPhone.trim()) {
      this.setData({ error: '请输入联系电话' });
      return;
    }
    if (!/^1[3-9]\d{9}$/.test(contactPhone.trim())) {
      this.setData({ error: '请输入有效的手机号码' });
      return;
    }
    if (reason && reason.trim().length > 500) {
      this.setData({ error: '离校原因不能超过500字' });
      return;
    }
    if (!leaveDate) {
      this.setData({ error: '请选择离校日期' });
      return;
    }
    const today = getShanghaiDateString();
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
      const requestData: any = {
        contact_phone: this.data.contactPhone.trim(),
        reason: this.data.reason.trim(),
        leave_date: this.data.leaveDate
      };

      if (this.data.draftId) {
        requestData.draft_id = this.data.draftId;
      }

      const res = await apiClient.createApplication(requestData);

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
