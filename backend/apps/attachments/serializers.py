from rest_framework import serializers
from .models import Attachment, AttachmentType


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

        return value


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'attachment_type', 'uploaded_at']
        read_only_fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'uploaded_at']
