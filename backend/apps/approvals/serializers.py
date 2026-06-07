from rest_framework import serializers
from .models import Approval


class ApplicationBriefSerializer(serializers.Serializer):
    """Brief application info for approval list"""
    id = serializers.CharField(source='application_id')
    status = serializers.CharField()


class ApprovalListSerializer(serializers.ModelSerializer):
    """Lean serializer for approval lists - nested application structure"""
    id = serializers.CharField(source='approval_id', read_only=True)
    application = ApplicationBriefSerializer(read_only=True)
    approver_id = serializers.CharField(source='approver.user_id', read_only=True)

    class Meta:
        model = Approval
        fields = ['id', 'application', 'step', 'approver_id',
                  'approver_name', 'decision', 'created_at']
        read_only_fields = ['id', 'step', 'approver_id',
                            'approver_name', 'decision', 'created_at']


class ApprovalSerializer(serializers.ModelSerializer):
    """Full approval detail with nested application info"""
    application_id = serializers.CharField(source='application.application_id', read_only=True)
    student_name = serializers.CharField(source='application.student.name', read_only=True)
    student_id = serializers.CharField(source='application.student.user_id', read_only=True)
    contact_phone = serializers.CharField(source='application.contact_phone', read_only=True)
    reason = serializers.CharField(source='application.reason', read_only=True)
    approver_id = serializers.CharField(source='approver.user_id', read_only=True)

    class Meta:
        model = Approval
        fields = ['approval_id', 'application_id', 'student_name', 'student_id',
                  'contact_phone', 'reason', 'step', 'approver_id',
                  'approver_name', 'decision', 'comment', 'decided_at']
        read_only_fields = ['approval_id', 'application_id', 'student_name', 'student_id',
                            'contact_phone', 'reason', 'step',
                            'approver_id', 'approver_name', 'decision', 'decided_at']


class ApprovalActionSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False, allow_blank=True)


class ApprovalListResponseSerializer(serializers.Serializer):
    """Schema-only: approval list response with pagination"""
    count = serializers.IntegerField()
    results = ApprovalListSerializer(many=True)
