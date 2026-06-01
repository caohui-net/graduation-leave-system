from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'notification_id',
            'recipient_id',
            'actor_id',
            'type',
            'entity_type',
            'entity_id',
            'title',
            'message',
            'read_at',
            'created_at'
        ]
        read_only_fields = ['notification_id', 'created_at']

    recipient_id = serializers.CharField(source='recipient.user_id', read_only=True)
    actor_id = serializers.CharField(source='actor.user_id', read_only=True, allow_null=True)
