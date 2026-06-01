from django.db import models
from apps.applications.models import Application
from apps.users.models import User


class AttachmentType(models.TextChoices):
    DORM_CHECKOUT = 'dorm_checkout', '宿舍清退证明'
    LIBRARY_CLEARANCE = 'library_clearance', '图书馆清书证明'
    FINANCE_CLEARANCE = 'finance_clearance', '财务结清证明'
    OTHER = 'other', '其他'


class Attachment(models.Model):
    attachment_id = models.CharField(max_length=50, primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='attachments')
    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT)
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    attachment_type = models.CharField(max_length=50, choices=AttachmentType.choices)
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField()
    content_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'attachments'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.attachment_id} - {self.file_name}"
