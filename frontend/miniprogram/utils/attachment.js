// 附件URL构建工具 - 跨平台复用

/**
 * 构建附件预览URL
 * @param {string} baseUrl - API基础地址
 * @param {string} attachmentId - 附件ID
 * @returns {string} 完整预览URL
 */
export function buildPreviewUrl(baseUrl, attachmentId) {
  return `${baseUrl}/api/attachments/${attachmentId}/download/?preview=true`;
}

/**
 * 构建附件下载URL
 * @param {string} baseUrl - API基础地址
 * @param {string} attachmentId - 附件ID
 * @returns {string} 完整下载URL
 */
export function buildDownloadUrl(baseUrl, attachmentId) {
  return `${baseUrl}/api/attachments/${attachmentId}/download/`;
}
