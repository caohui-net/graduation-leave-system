from rest_framework import serializers
from .models import Application


class ApplicationListSerializer(serializers.ModelSerializer):
    """Application list serializer with nested approvals for batch operations"""
    student_id = serializers.CharField(source='student.user_id', read_only=True)
    building = serializers.CharField(source='student.building', read_only=True, allow_null=True, required=False)
    room_number = serializers.CharField(source='student.room_number', read_only=True, allow_null=True, required=False)
    department = serializers.CharField(source='student.department', read_only=True, allow_null=True, required=False)
    has_attachments = serializers.SerializerMethodField()
    approvals = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['application_id', 'student_id', 'student_name', 'class_id',
                  'contact_phone', 'reason', 'leave_date', 'status', 'building',
                  'room_number', 'department', 'has_attachments', 'created_at', 'updated_at', 'approvals']
        read_only_fields = ['application_id', 'student_id', 'student_name',
                            'class_id', 'status', 'building', 'room_number', 'department',
                            'created_at', 'updated_at']

    def get_has_attachments(self, obj):
        return obj.attachments.exists()

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
    leave_date = serializers.DateField()

    def validate_leave_date(self, value):
        from django.utils import timezone
        today = timezone.now().date()
        if value < today:
            raise serializers.ValidationError('离校日期不能早于今天')
        return value


class ApplicationListResponseSerializer(serializers.Serializer):
    """Schema-only: application list response with pagination"""
    count = serializers.IntegerField()
    results = ApplicationListSerializer(many=True)
