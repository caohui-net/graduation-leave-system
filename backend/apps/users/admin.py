from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'role', 'class_id', 'active']
    list_filter = ['role', 'active', 'is_graduating']
    search_fields = ['user_id', 'name', 'class_id']
    ordering = ['user_id']
