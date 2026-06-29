from rest_framework import serializers
from .models import Approval


class ApplicationBriefSerializer(serializers.Serializer):
    """Brief application info for approval list"""
    id = serializers.CharField(source='application_id')
    status = serializers.CharField()
    student_name = serializers.CharField(source='student.name')
    student_id = serializers.CharField(source='student.user_id')
    department = serializers.CharField(source='student.department', allow_null=True)
    major = serializers.CharField(source='student.major', allow_null=True)
    class_id = serializers.CharField(source='student.class_id', allow_null=True)
    contact_phone = serializers.CharField(allow_null=True)
    leave_date = serializers.DateField(allow_null=True)
    stay_start_date = serializers.DateField(allow_null=True)
    stay_end_date = serializers.DateField(allow_null=True)
    stay_reason = serializers.CharField(allow_null=True)
    building = serializers.CharField(source='student.building', allow_null=True)
    room_number = serializers.CharField(source='student.room_number', allow_null=True)
    created_at = serializers.DateTimeField()


class ApprovalListSerializer(serializers.ModelSerializer):
    """Lean serializer for approval lists - nested application structure"""
    id = serializers.CharField(source='approval_id', read_only=True)
    application = ApplicationBriefSerializer(read_only=True)
    approver_id = serializers.CharField(source='approver.user_id', read_only=True)

    class Meta:
        model = Approval
        fields = ['id', 'application', 'step', 'approver_id',
                  'approver_name', 'decision', 'comment', 'decided_at', 'created_at']
        read_only_fields = ['id', 'step', 'approver_id',
                            'approver_name', 'decision', 'comment', 'decided_at', 'created_at']


class ApprovalBriefSerializer(serializers.ModelSerializer):
    """Brief approval info without attachments - for nested use in ApplicationSerializer"""
    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
    decided_by_id = serializers.CharField(source='decided_by.user_id', read_only=True, allow_null=True)
    decided_by_name = serializers.CharField(source='decided_by.name', read_only=True, allow_null=True)

    class Meta:
        model = Approval
        fields = ['approval_id', 'step', 'approver_id', 'approver_name',
                  'decided_by_id', 'decided_by_name', 'decision', 'comment', 'decided_at']
        read_only_fields = fields


class ApprovalSerializer(serializers.ModelSerializer):
    """Full approval detail with nested application info"""
    application_id = serializers.CharField(source='application.application_id', read_only=True)
    student_name = serializers.CharField(source='application.student.name', read_only=True)
    student_id = serializers.CharField(source='application.student.user_id', read_only=True)
    contact_phone = serializers.CharField(source='application.contact_phone', read_only=True)
    reason = serializers.CharField(source='application.reason', read_only=True)
    leave_date = serializers.DateField(source='application.leave_date', read_only=True)
    building = serializers.CharField(source='application.student.building', read_only=True, allow_null=True)
    room_number = serializers.CharField(source='application.student.room_number', read_only=True, allow_null=True)
    attachments = serializers.SerializerMethodField()
    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
    decided_by_id = serializers.CharField(source='decided_by.user_id', read_only=True, allow_null=True)
    decided_by_name = serializers.CharField(source='decided_by.name', read_only=True, allow_null=True)

    class Meta:
        model = Approval
        fields = ['approval_id', 'application_id', 'student_name', 'student_id',
                  'contact_phone', 'reason', 'leave_date', 'building', 'room_number',
                  'attachments', 'step', 'approver_id',
                  'approver_name', 'decided_by_id', 'decided_by_name', 'decision', 'comment', 'decided_at']
        read_only_fields = ['approval_id', 'application_id', 'student_name', 'student_id',
                            'contact_phone', 'reason', 'leave_date', 'building', 'room_number',
                            'attachments', 'step',
                            'approver_id', 'approver_name', 'decided_by_id', 'decided_by_name', 'decision', 'decided_at']

    def get_attachments(self, obj):
        from apps.attachments.serializers import AttachmentSerializer
        return AttachmentSerializer(
            obj.application.attachments.filter(is_deleted=False),
            many=True
        ).data


class ApprovalActionSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False, allow_blank=True)


class ApprovalListResponseSerializer(serializers.Serializer):
    """Schema-only: approval list response with pagination"""
    count = serializers.IntegerField()
    results = ApprovalListSerializer(many=True)
