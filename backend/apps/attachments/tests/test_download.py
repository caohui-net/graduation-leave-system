from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.attachments.models import Attachment, AttachmentType


class AttachmentDownloadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create students
        self.student = User.objects.create_user(
            user_id='2020001',
            password='2020001',
            name='张三',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            is_graduating=True,
            graduation_year=2024,
            building='1号楼',
            department='计算机学院'
        )

        self.other_student = User.objects.create_user(
            user_id='2020002',
            password='2020002',
            name='李四',
            role=UserRole.STUDENT,
            class_id='CS2020-02',
            is_graduating=True,
            graduation_year=2024,
            building='2号楼',
            department='软件学院'
        )

        # Create counselor
        self.counselor = User.objects.create_user(
            user_id='T001',
            password='T001',
            name='李老师',
            role=UserRole.COUNSELOR,
            department='计算机学院'
        )

        # Create class mapping
        ClassMapping.objects.create(
            class_id='CS2020-01',
            counselor=self.counselor,
            counselor_name='李老师',
            active=True
        )

        # Create application
        self.application = Application.objects.create(
            application_id='app_test001',
            student=self.student,
            student_name='张三',
            class_id='CS2020-01',
            reason='毕业离校',
            leave_date='2024-07-01',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        # Create attachment with actual file
        test_file = SimpleUploadedFile("test.pdf", b"test file content", content_type="application/pdf")
        self.attachment = Attachment.objects.create(
            attachment_id='att_test001',
            application=self.application,
            uploaded_by=self.student,
            file=test_file,
            attachment_type=AttachmentType.DORM_CHECKOUT,
            file_name='test.pdf',
            file_size=1024,
            content_type='application/pdf'
        )

    def test_download_positive_student(self):
        """Student can download own application attachment"""
        self.client.force_authenticate(user=self.student)

        response = self.client.get(
            f'/api/attachments/{self.attachment.attachment_id}/download/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_download_positive_counselor(self):
        """Assigned counselor can download attachment"""
        self.client.force_authenticate(user=self.counselor)

        response = self.client.get(
            f'/api/attachments/{self.attachment.attachment_id}/download/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_download_forbidden(self):
        """Unauthorized student cannot download attachment"""
        self.client.force_authenticate(user=self.other_student)

        response = self.client.get(
            f'/api/attachments/{self.attachment.attachment_id}/download/'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

    def test_download_soft_deleted_returns_404(self):
        """Soft-deleted attachment returns 404"""
        self.attachment.is_deleted = True
        self.attachment.save()

        self.client.force_authenticate(user=self.student)

        response = self.client.get(
            f'/api/attachments/{self.attachment.attachment_id}/download/'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error']['code'], 'NOT_FOUND')
