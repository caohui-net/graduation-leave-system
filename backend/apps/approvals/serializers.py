from rest_framework import serializers
from .models import Approval


class ApprovalListSerializer(serializers.ModelSerializer):
    """Lean serializer for approval lists - includes created_at"""
    application_id = serializers.CharField(source='application.application_id', read_only=True)
    approver_id = serializers.CharField(source='approver.user_id', read_only=True)

    class Meta:
        model = Approval
        fields = ['approval_id', 'application_id', 'step', 'approver_id',
                  'approver_name', 'decision', 'created_at']
        read_only_fields = ['approval_id', 'application_id', 'step',
                            'approver_id', 'approver_name', 'decision', 'created_at']


class ApprovalSerializer(serializers.ModelSerializer):
    application_id = serializers.CharField(source='application.application_id', read_only=True)
    approver_id = serializers.CharField(source='approver.user_id', read_only=True)

    class Meta:
        model = Approval
        fields = ['approval_id', 'application_id', 'step', 'approver_id',
                  'approver_name', 'decision', 'comment', 'decided_at']
        read_only_fields = ['approval_id', 'application_id', 'step',
                            'approver_id', 'approver_name', 'decision', 'decided_at']


class ApprovalActionSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False, allow_blank=True)
