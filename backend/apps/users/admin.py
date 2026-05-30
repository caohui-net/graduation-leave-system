from django.contrib import admin
from .models import User
from .class_mapping import ClassMapping


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'role', 'class_id', 'active']
    list_filter = ['role', 'active', 'is_graduating']
    search_fields = ['user_id', 'name', 'class_id']
    ordering = ['user_id']


@admin.register(ClassMapping)
class ClassMappingAdmin(admin.ModelAdmin):
    list_display = ['class_id', 'counselor', 'counselor_name', 'active']
    list_filter = ['active']
    search_fields = ['class_id', 'counselor__user_id', 'counselor_name']
    ordering = ['class_id']
