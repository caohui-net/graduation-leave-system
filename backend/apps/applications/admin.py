from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_id', 'student', 'student_name', 'class_id', 'status', 'created_at']
    list_filter = ['status', 'dorm_checkout_status']
    search_fields = ['application_id', 'student__user_id', 'student_name', 'class_id']
    ordering = ['-created_at']
