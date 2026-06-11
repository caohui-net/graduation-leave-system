// 审批详情组件 - 包含附件预览功能
import React from 'react';
import type { ApprovalDetail, Attachment } from '../types/api';
import { useAttachment } from '../hooks/useAttachment';

interface Props {
  approval: ApprovalDetail;
}

export const ApprovalDetailView: React.FC<Props> = ({ approval }) => {
  const { handlePreview, handleDownload } = useAttachment();
  const [loading, setLoading] = React.useState<string | null>(null);

  const onPreview = async (attachmentId: string) => {
    setLoading(attachmentId);
    try {
      await handlePreview(attachmentId);
    } catch (error) {
      alert('预览失败：' + (error instanceof Error ? error.message : '未知错误'));
    } finally {
      setLoading(null);
    }
  };

  const onDownload = async (file: Attachment) => {
    setLoading(file.attachment_id);
    try {
      await handleDownload(file.attachment_id, file.file_name);
    } catch (error) {
      alert('下载失败：' + (error instanceof Error ? error.message : '未知错误'));
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="approval-detail">
      {/* 基本信息 */}
      <div className="info-section">
        <h3>申请信息</h3>
        <div className="info-item">
          <label>学生姓名：</label>
          <span>{approval.student_name}</span>
        </div>
        <div className="info-item">
          <label>学号：</label>
          <span>{approval.student_id}</span>
        </div>
        <div className="info-item">
          <label>联系电话：</label>
          <span>{approval.contact_phone}</span>
        </div>
        <div className="info-item">
          <label>离校日期：</label>
          <span>{approval.leave_date}</span>
        </div>
        <div className="info-item">
          <label>离校原因：</label>
          <span>{approval.reason}</span>
        </div>
      </div>

      {/* 附件列表 */}
      {approval.attachments && approval.attachments.length > 0 && (
        <div className="attachments-section">
          <h3>附件材料</h3>
          {approval.attachments.map((file: Attachment) => (
            <div key={file.attachment_id} className="attachment-item">
              <span className="file-name">{file.file_name}</span>
              <span className="file-size">
                ({(file.file_size / 1024).toFixed(2)} KB)
              </span>
              <div className="attachment-actions">
                {/* 附件预览按钮 */}
                <button
                  className="btn-preview"
                  onClick={() => onPreview(file.attachment_id)}
                  disabled={loading === file.attachment_id}
                >
                  {loading === file.attachment_id ? '加载中...' : '附件预览'}
                </button>
                <button
                  className="btn-download"
                  onClick={() => onDownload(file)}
                  disabled={loading === file.attachment_id}
                >
                  {loading === file.attachment_id ? '下载中...' : '下载'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 审批操作 */}
      <div className="approval-actions">
        {approval.decision === 'pending' && (
          <>
            <button className="btn-approve">通过</button>
            <button className="btn-reject">驳回</button>
          </>
        )}
      </div>
    </div>
  );
};
