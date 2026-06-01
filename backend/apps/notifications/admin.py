from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notification_id', 'recipient', 'type', 'title', 'read_at', 'created_at']
    list_filter = ['type', 'entity_type', 'read_at', 'created_at']
    search_fields = ['notification_id', 'title', 'message', 'recipient__user_id']
    readonly_fields = ['notification_id', 'created_at']
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False
