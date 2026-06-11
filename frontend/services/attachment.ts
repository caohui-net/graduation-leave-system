// 附件服务 - 跨平台复用
export class AttachmentService {
  private baseUrl: string;
  private getToken: () => string | null;

  constructor(baseUrl: string, getToken: () => string | null) {
    this.baseUrl = baseUrl;
    this.getToken = getToken;
  }

  // 生成预览URL
  getPreviewUrl(attachmentId: string): string {
    return `${this.baseUrl}/api/attachments/${attachmentId}/download/?preview=true`;
  }

  // 生成下载URL
  getDownloadUrl(attachmentId: string): string {
    return `${this.baseUrl}/api/attachments/${attachmentId}/download/`;
  }

  // Web平台预览（带鉴权）
  async previewWeb(attachmentId: string): Promise<void> {
    const url = this.getPreviewUrl(attachmentId);
    const token = this.getToken();

    if (!token) {
      throw new Error('未登录');
    }

    try {
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error(response.status === 403 ? '无权限访问' : '预览失败');
      }

      const blob = await response.blob();
      const blobUrl = URL.createObjectURL(blob);
      window.open(blobUrl, '_blank');

      // 清理Blob URL（延迟以确保窗口打开）
      setTimeout(() => URL.revokeObjectURL(blobUrl), 100);
    } catch (error) {
      throw new Error('预览失败：' + (error instanceof Error ? error.message : '未知错误'));
    }
  }

  // Web平台下载（带鉴权）
  async downloadWeb(attachmentId: string, fileName: string): Promise<void> {
    const url = this.getDownloadUrl(attachmentId);
    const token = this.getToken();

    if (!token) {
      throw new Error('未登录');
    }

    try {
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error(response.status === 403 ? '无权限访问' : '下载失败');
      }

      const blob = await response.blob();
      const blobUrl = URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      URL.revokeObjectURL(blobUrl);
    } catch (error) {
      throw new Error('下载失败：' + (error instanceof Error ? error.message : '未知错误'));
    }
  }
}

// 单例
export const attachmentService = new AttachmentService(
  process.env.API_BASE_URL || 'http://localhost:8000'
);
