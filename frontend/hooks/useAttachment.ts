// 附件操作Hook - 跨平台复用
import { AttachmentService } from '../services/attachment';

// 需要从API配置中获取token
const getToken = (): string | null => {
  // 从localStorage或其他存储中获取token
  return localStorage.getItem('access_token');
};

const attachmentService = new AttachmentService(
  process.env.API_BASE_URL || 'http://localhost:8000',
  getToken
);

export const useAttachment = () => {
  const handlePreview = async (attachmentId: string) => {
    try {
      await attachmentService.previewWeb(attachmentId);
    } catch (error) {
      throw error;
    }
  };

  const handleDownload = async (attachmentId: string, fileName: string) => {
    try {
      await attachmentService.downloadWeb(attachmentId, fileName);
    } catch (error) {
      throw error;
    }
  };

  const getPreviewUrl = (attachmentId: string) => {
    return attachmentService.getPreviewUrl(attachmentId);
  };

  const getDownloadUrl = (attachmentId: string) => {
    return attachmentService.getDownloadUrl(attachmentId);
  };

  return {
    handlePreview,
    handleDownload,
    getPreviewUrl,
    getDownloadUrl,
  };
};
