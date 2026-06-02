import string
import random
from django.db import models
from django.conf import settings


def generate_notification_id():
    """生成格式为 not_xxxxxxxx 的通知ID"""
    chars = string.ascii_lowercase + string.digits
    random_str = ''.join(random.choices(chars, k=8))
    return f'not_{random_str}'


class NotificationType(models.TextChoices):
    APPLICATION_SUBMITTED = 'application_submitted', '申请已提交'
    APPROVAL_APPROVED = 'approval_approved', '审批通过'
    APPROVAL_REJECTED = 'approval_rejected', '审批驳回'
    APPROVAL_TIMEOUT_WARNING = 'approval_timeout_warning', '审批超时提醒'


class EntityType(models.TextChoices):
    APPLICATION = 'application', '离校申请'
    APPROVAL = 'approval', '审批记录'


class Notification(models.Model):
    notification_id = models.CharField(
        max_length=12,
        primary_key=True,
        default=generate_notification_id,
        editable=False,
        verbose_name='通知ID'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='notifications_received',
        verbose_name='接收者'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='notifications_triggered',
        null=True,
        blank=True,
        verbose_name='触发者'
    )
    type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        verbose_name='通知类型'
    )
    entity_type = models.CharField(
        max_length=50,
        choices=EntityType.choices,
        verbose_name='实体类型'
    )
    entity_id = models.CharField(
        max_length=50,
        verbose_name='实体ID'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='标题'
    )
    message = models.TextField(
        verbose_name='消息内容'
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='已读时间'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )

    class Meta:
        db_table = 'notifications'
        verbose_name = '通知'
        verbose_name_plural = '通知'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'created_at']),
            models.Index(fields=['recipient', 'read_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['recipient', 'entity_type', 'entity_id', 'type'],
                name='unique_notification_per_recipient_entity'
            )
        ]

    def __str__(self):
        return f'{self.notification_id}: {self.title}'
