// 附件URL构建工具 - 跨平台复用（Web/RN/小程序）

/**
 * 构建附件预览URL
 * @param {string} baseUrl - API基础地址
 * @param {string} attachmentId - 附件ID
 * @returns {string} 完整预览URL
 */
export function buildPreviewUrl(baseUrl: string, attachmentId: string): string {
  return `${baseUrl}/api/attachments/${attachmentId}/download/?preview=true`;
}

/**
 * 构建附件下载URL
 * @param {string} baseUrl - API基础地址
 * @param {string} attachmentId - 附件ID
 * @returns {string} 完整下载URL
 */
export function buildDownloadUrl(baseUrl: string, attachmentId: string): string {
  return `${baseUrl}/api/attachments/${attachmentId}/download/`;
}
