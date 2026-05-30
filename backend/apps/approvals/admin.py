from django.contrib import admin
from .models import Approval


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ['approval_id', 'application', 'step', 'approver', 'decision', 'decided_at']
    list_filter = ['step', 'decision']
    search_fields = ['approval_id', 'application__application_id', 'approver__user_id']
    ordering = ['-created_at']
