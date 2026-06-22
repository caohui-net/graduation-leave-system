from rest_framework import serializers
from .models import Application


class ApplicationListSerializer(serializers.ModelSerializer):
    """Application list serializer with nested approvals for batch operations"""
    student_id = serializers.CharField(source='student.user_id', read_only=True)
    building = serializers.CharField(source='student.building', read_only=True, allow_null=True, required=False)
    room_number = serializers.CharField(source='student.room_number', read_only=True, allow_null=True, required=False)
    department = serializers.CharField(source='student.department', read_only=True, allow_null=True, required=False)
    has_attachments = serializers.SerializerMethodField()
    attachment_count = serializers.SerializerMethodField()
    approvals = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['application_id', 'student_id', 'student_name', 'class_id',
                  'contact_phone', 'reason', 'leave_date', 'status', 'building',
                  'room_number', 'department', 'has_attachments', 'attachment_count',
                  'created_at', 'updated_at', 'approvals']
        read_only_fields = ['application_id', 'student_id', 'student_name',
                            'class_id', 'status', 'building', 'room_number', 'department',
                            'created_at', 'updated_at']

    def get_has_attachments(self, obj):
        return obj.attachments.exists()

    def get_attachment_count(self, obj):
        return obj.attachments.filter(is_deleted=False).count()

    def get_approvals(self, obj):
        from apps.approvals.serializers import ApprovalBriefSerializer
        return ApprovalBriefSerializer(obj.approvals.all(), many=True).data


class ApplicationSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(source='student.user_id', read_only=True)
    building = serializers.CharField(source='student.building', read_only=True, allow_null=True, required=False)
    room_number = serializers.CharField(source='student.room_number', read_only=True, allow_null=True, required=False)
    department = serializers.CharField(source='student.department', read_only=True, allow_null=True, required=False)
    has_attachments = serializers.SerializerMethodField()
    approvals = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['application_id', 'student_id', 'student_name', 'class_id',
                  'contact_phone', 'reason', 'leave_date', 'status', 'dorm_checkout_status',
                  'application_type', 'stay_start_date', 'stay_end_date', 'stay_reason',
                  'building', 'room_number', 'department', 'has_attachments', 'approvals', 'created_at', 'updated_at']
        read_only_fields = ['application_id', 'student_id', 'student_name',
                            'class_id', 'status', 'dorm_checkout_status',
                            'building', 'room_number', 'department', 'created_at', 'updated_at']

    def get_has_attachments(self, obj):
        return obj.attachments.exists()

    def get_approvals(self, obj):
        from apps.approvals.serializers import ApprovalBriefSerializer
        return ApprovalBriefSerializer(obj.approvals.all(), many=True).data


class ApplicationCreateSerializer(serializers.Serializer):
    contact_phone = serializers.CharField(max_length=20, required=True)
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True, default='')
    leave_date = serializers.DateField(required=False, allow_null=True)
    application_type = serializers.CharField(required=False, default='LEAVE')
    stay_start_date = serializers.DateField(required=False, allow_null=True)
    stay_end_date = serializers.DateField(required=False, allow_null=True)
    stay_reason = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def validate(self, data):
        app_type = data.get('application_type', 'LEAVE')
        if app_type == 'LEAVE':
            if not data.get('leave_date'):
                raise serializers.ValidationError({'leave_date': '离校申请需要提供离校日期'})
        elif app_type == 'STAY':
            if not data.get('stay_start_date') or not data.get('stay_end_date'):
                raise serializers.ValidationError({'stay_start_date': '留校申请需要提供开始和结束日期'})
            if not data.get('stay_reason'):
                raise serializers.ValidationError({'stay_reason': '留校申请需要提供留校原因'})
        return data

    def validate_leave_date(self, value):
        if value:
            from django.utils import timezone
            if value < timezone.now().date():
                raise serializers.ValidationError('离校日期不能早于今天')
        return value


class ApplicationListResponseSerializer(serializers.Serializer):
    """Schema-only: application list response with pagination"""
    count = serializers.IntegerField()
    results = ApplicationListSerializer(many=True)
