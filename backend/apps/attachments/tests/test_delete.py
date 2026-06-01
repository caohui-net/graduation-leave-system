from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping
from apps.applications.models import Application, ApplicationStatus
from apps.attachments.models import Attachment, AttachmentType


class AttachmentDeleteTestCase(TestCase):
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
            graduation_year=2024
        )

        self.other_student = User.objects.create_user(
            user_id='2020002',
            password='2020002',
            name='李四',
            role=UserRole.STUDENT,
            class_id='CS2020-02',
            is_graduating=True,
            graduation_year=2024
        )

        # Create counselor
        self.counselor = User.objects.create_user(
            user_id='T001',
            password='T001',
            name='李老师',
            role=UserRole.COUNSELOR
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

        # Create attachment
        test_file = SimpleUploadedFile("test.pdf", b"test content", content_type="application/pdf")
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

    def test_delete_owner_success(self):
        """Owner student can soft-delete attachment"""
        self.client.force_authenticate(user=self.student)

        response = self.client.delete(
            f'/api/attachments/{self.attachment.attachment_id}/'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify soft delete
        self.attachment.refresh_from_db()
        self.assertTrue(self.attachment.is_deleted)
        self.assertIsNotNone(self.attachment.deleted_at)

    def test_delete_non_owner_student_forbidden(self):
        """Non-owner student cannot delete attachment"""
        self.client.force_authenticate(user=self.other_student)

        response = self.client.delete(
            f'/api/attachments/{self.attachment.attachment_id}/'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

        # Verify not deleted
        self.attachment.refresh_from_db()
        self.assertFalse(self.attachment.is_deleted)

    def test_delete_counselor_forbidden(self):
        """Counselor cannot delete attachment"""
        self.client.force_authenticate(user=self.counselor)

        response = self.client.delete(
            f'/api/attachments/{self.attachment.attachment_id}/'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

    def test_delete_already_deleted_returns_404(self):
        """Deleting already-deleted attachment returns 404"""
        self.attachment.is_deleted = True
        self.attachment.save()

        self.client.force_authenticate(user=self.student)

        response = self.client.delete(
            f'/api/attachments/{self.attachment.attachment_id}/'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error']['code'], 'NOT_FOUND')
