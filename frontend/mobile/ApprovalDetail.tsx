// 移动端审批详情组件 - React Native
import React from 'react';
import { View, Text, TouchableOpacity, Linking, StyleSheet } from 'react-native';
import { buildPreviewUrl, buildDownloadUrl } from '../utils/attachment';

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

interface Attachment {
  attachment_id: string;
  file_name: string;
  file_size: number;
}

interface ApprovalDetail {
  student_name: string;
  student_id: string;
  contact_phone: string;
  leave_date: string;
  reason: string;
  attachments: Attachment[];
  decision: string;
}

interface Props {
  approval: ApprovalDetail;
  onApprove?: () => void;
  onReject?: () => void;
}

export const ApprovalDetailView: React.FC<Props> = ({ approval, onApprove, onReject }) => {
  const handlePreview = (attachmentId: string) => {
    const url = buildPreviewUrl(API_BASE_URL, attachmentId);
    Linking.openURL(url);
  };

  const handleDownload = (attachmentId: string) => {
    const url = buildDownloadUrl(API_BASE_URL, attachmentId);
    Linking.openURL(url);
  };

  return (
    <View style={styles.container}>
      {/* 基本信息 */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>申请信息</Text>

        <View style={styles.infoRow}>
          <Text style={styles.label}>学生姓名：</Text>
          <Text style={styles.value}>{approval.student_name}</Text>
        </View>

        <View style={styles.infoRow}>
          <Text style={styles.label}>学号：</Text>
          <Text style={styles.value}>{approval.student_id}</Text>
        </View>

        <View style={styles.infoRow}>
          <Text style={styles.label}>联系电话：</Text>
          <Text style={styles.value}>{approval.contact_phone}</Text>
        </View>

        <View style={styles.infoRow}>
          <Text style={styles.label}>离校日期：</Text>
          <Text style={styles.value}>{approval.leave_date}</Text>
        </View>

        <View style={styles.infoRow}>
          <Text style={styles.label}>离校原因：</Text>
          <Text style={styles.value}>{approval.reason}</Text>
        </View>
      </View>

      {/* 附件列表 */}
      {approval.attachments && approval.attachments.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>附件材料</Text>

          {approval.attachments.map((file) => (
            <View key={file.attachment_id} style={styles.attachmentItem}>
              <View style={styles.fileInfo}>
                <Text style={styles.fileName}>{file.file_name}</Text>
                <Text style={styles.fileSize}>
                  ({(file.file_size / 1024).toFixed(2)} KB)
                </Text>
              </View>

              <View style={styles.attachmentActions}>
                {/* 附件预览按钮 */}
                <TouchableOpacity
                  style={[styles.button, styles.previewButton]}
                  onPress={() => handlePreview(file.attachment_id)}
                >
                  <Text style={styles.buttonText}>附件预览</Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={[styles.button, styles.downloadButton]}
                  onPress={() => handleDownload(file.attachment_id)}
                >
                  <Text style={styles.buttonText}>下载</Text>
                </TouchableOpacity>
              </View>
            </View>
          ))}
        </View>
      )}

      {/* 审批操作 */}
      {approval.decision === 'pending' && (
        <View style={styles.actionSection}>
          <TouchableOpacity
            style={[styles.button, styles.approveButton]}
            onPress={onApprove}
          >
            <Text style={styles.buttonText}>通过</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.rejectButton]}
            onPress={onReject}
          >
            <Text style={styles.buttonText}>驳回</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f5f5f5',
  },
  section: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
    color: '#333',
  },
  infoRow: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  label: {
    fontSize: 14,
    color: '#666',
    width: 80,
  },
  value: {
    fontSize: 14,
    color: '#333',
    flex: 1,
  },
  attachmentItem: {
    borderTopWidth: 1,
    borderTopColor: '#eee',
    paddingTop: 12,
    marginTop: 12,
  },
  fileInfo: {
    marginBottom: 8,
  },
  fileName: {
    fontSize: 14,
    color: '#333',
    marginBottom: 4,
  },
  fileSize: {
    fontSize: 12,
    color: '#999',
  },
  attachmentActions: {
    flexDirection: 'row',
    gap: 8,
  },
  button: {
    flex: 1,
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderRadius: 4,
    alignItems: 'center',
  },
  previewButton: {
    backgroundColor: '#1890ff',
  },
  downloadButton: {
    backgroundColor: '#52c41a',
  },
  buttonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '500',
  },
  actionSection: {
    flexDirection: 'row',
    gap: 12,
    marginTop: 16,
  },
  approveButton: {
    backgroundColor: '#52c41a',
  },
  rejectButton: {
    backgroundColor: '#ff4d4f',
  },
});
