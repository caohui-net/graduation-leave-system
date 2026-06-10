from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SSOUserMapping(models.Model):
    """青橄榄用户 → 本地用户映射表"""

    USER_TYPE_CHOICES = [
        ('mobile_student', '移动端-学生'),
        ('mobile_teacher', '移动端-教师'),
        ('admin', '管理端-管理员'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='sso_mapping'
    )
    tenant_code = models.CharField(max_length=50)
    user_code = models.CharField(max_length=200, unique=True, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    real_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    identity_name = models.CharField(max_length=50, blank=True)
    role_name = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'sso_user_mapping'
        indexes = [
            models.Index(fields=['user_code']),
            models.Index(fields=['username']),
        ]

    def __str__(self):
        return f"{self.real_name} ({self.user_type})"
