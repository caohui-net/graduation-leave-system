from rest_framework import serializers
from .models import Attachment, AttachmentType


def detect_file_type(file):
    """
    基于文件头（magic number）检测真实文件类型
    返回：(是否有效, MIME类型)
    """
    # 读取文件头（前16字节足够识别常见格式）
    file.seek(0)
    header = file.read(16)
    file.seek(0)  # 重置文件指针

    # 常见文件类型的magic number
    if header.startswith(b'\xff\xd8\xff'):
        return True, 'image/jpeg'
    elif header.startswith(b'\x89PNG\r\n\x1a\n'):
        return True, 'image/png'
    elif header.startswith(b'%PDF'):
        return True, 'application/pdf'
    elif header.startswith(b'PK\x03\x04'):
        # ZIP格式（docx也是zip）
        if b'word/' in file.read(512):
            file.seek(0)
            return True, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        file.seek(0)
        return True, 'application/zip'
    elif header.startswith(b'\xd0\xcf\x11\xe0'):
        # 旧版Office格式（.doc）
        return True, 'application/msword'

    return False, None


class AttachmentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    attachment_type = serializers.ChoiceField(choices=AttachmentType.choices)

    def validate_file(self, value):
        # Max 10MB
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError('文件大小不能超过10MB')

        # Allowed extensions
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']
        file_name = value.name.lower()
        if not any(file_name.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError(f'不支持的文件类型，仅支持：{", ".join(allowed_extensions)}')

        # 真实文件类型检测（基于文件头）
        is_valid, detected_type = detect_file_type(value)
        if not is_valid:
            raise serializers.ValidationError('文件类型校验失败：文件内容与扩展名不符或不是支持的文件类型')

        return value


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'attachment_type', 'uploaded_at']
        read_only_fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'uploaded_at']


class AttachmentListResponseSerializer(serializers.Serializer):
    """Schema-only: attachment list response with wrapper"""
    attachments = AttachmentSerializer(many=True)
