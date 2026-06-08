from django.db import models
from django.contrib.auth.models import User


class SSOUserMapping(models.Model):
    """青橄榄用户 → 本地用户映射表"""

    USER_TYPE_CHOICES = [
        ('mobile_student', '移动端-学生'),
        ('mobile_teacher', '移动端-教师'),
        ('admin', '管理端-管理员'),
    ]

    # 本地用户
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='sso_mapping',
        verbose_name='本地用户'
    )

    # 青橄榄标识
    tenant_code = models.CharField(max_length=50, verbose_name='租户Code')
    user_code = models.CharField(
        max_length=200,
        unique=True,
        null=True,
        blank=True,
        verbose_name='移动端user_code'
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name='管理端username'
    )

    # 用户类型
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        verbose_name='用户类型'
    )

    # 青橄榄用户信息快照（避免频繁调用API）
    real_name = models.CharField(max_length=100, verbose_name='真实姓名')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    identity_name = models.CharField(max_length=50, blank=True, verbose_name='身份名称')
    role_name = models.CharField(max_length=100, blank=True, verbose_name='角色名称')

    # 元数据
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_login_at = models.DateTimeField(null=True, blank=True, verbose_name='最后登录时间')

    class Meta:
        db_table = 'sso_user_mapping'
        verbose_name = 'SSO用户映射'
        verbose_name_plural = 'SSO用户映射'
        indexes = [
            models.Index(fields=['user_code'], name='idx_user_code'),
            models.Index(fields=['username'], name='idx_username'),
        ]

    def __str__(self):
        return f"{self.real_name} ({self.user_type})"
