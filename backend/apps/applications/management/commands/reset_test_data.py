from django.core.management.base import BaseCommand
from apps.applications.models import Application
from apps.approvals.models import Approval
from apps.attachments.models import Attachment


class Command(BaseCommand):
    help = '清空申请和审批数据，保留用户数据'

    def handle(self, *args, **options):
        # Delete all attachments
        attachment_count = Attachment.objects.count()
        Attachment.objects.all().delete()
        self.stdout.write(f'删除 {attachment_count} 条附件记录')

        # Delete all approvals
        approval_count = Approval.objects.count()
        Approval.objects.all().delete()
        self.stdout.write(f'删除 {approval_count} 条审批记录')

        # Delete all applications
        application_count = Application.objects.count()
        Application.objects.all().delete()
        self.stdout.write(f'删除 {application_count} 条申请记录')

        self.stdout.write(self.style.SUCCESS('✓ 测试数据重置完成'))
