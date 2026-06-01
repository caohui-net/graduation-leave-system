from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping
from apps.applications.models import Application, ApplicationStatus
from apps.attachments.models import Attachment, AttachmentType


class AttachmentUploadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create student
        self.student = User.objects.create_user(
            user_id='2020001',
            password='2020001',
            name='张三',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            is_graduating=True,
            graduation_year=2024
        )

        # Create another student
        self.other_student = User.objects.create_user(
            user_id='2020002',
            password='2020002',
            name='李四',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
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

        # Create application for student
        self.application = Application.objects.create(
            application_id='app_test001',
            student=self.student,
            student_name='张三',
            class_id='CS2020-01',
            reason='毕业离校',
            leave_date='2024-07-01',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        # Create application for other student
        self.other_application = Application.objects.create(
            application_id='app_test002',
            student=self.other_student,
            student_name='李四',
            class_id='CS2020-01',
            reason='毕业离校',
            leave_date='2024-07-01',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

    def test_upload_success(self):
        """Student can upload attachment to own application"""
        self.client.force_authenticate(user=self.student)

        file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        response = self.client.post(
            f'/api/applications/{self.application.application_id}/attachments/',
            {
                'file': file,
                'attachment_type': AttachmentType.DORM_CHECKOUT,
                'description': '宿舍退房证明'
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('attachment_id', response.data)
        self.assertTrue(response.data['attachment_id'].startswith('att_'))
        self.assertEqual(len(response.data['attachment_id']), 16)  # att_ + 12 hex chars
        self.assertEqual(response.data['attachment_type'], AttachmentType.DORM_CHECKOUT)
        self.assertEqual(response.data['file_name'], 'test.pdf')

    def test_upload_forbidden_other_student(self):
        """Student cannot upload to another student's application"""
        self.client.force_authenticate(user=self.student)

        file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        response = self.client.post(
            f'/api/applications/{self.other_application.application_id}/attachments/',
            {
                'file': file,
                'attachment_type': AttachmentType.DORM_CHECKOUT
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

    def test_upload_forbidden_counselor(self):
        """Counselor cannot upload attachments"""
        self.client.force_authenticate(user=self.counselor)

        file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        response = self.client.post(
            f'/api/applications/{self.application.application_id}/attachments/',
            {
                'file': file,
                'attachment_type': AttachmentType.DORM_CHECKOUT
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

    def test_upload_validation_missing_file(self):
        """Upload fails with missing file"""
        self.client.force_authenticate(user=self.student)

        response = self.client.post(
            f'/api/applications/{self.application.application_id}/attachments/',
            {
                'attachment_type': AttachmentType.DORM_CHECKOUT
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
        self.assertIn('details', response.data['error'])
        self.assertIn('file', response.data['error']['details'])

    def test_upload_validation_missing_type(self):
        """Upload fails with missing attachment_type"""
        self.client.force_authenticate(user=self.student)

        file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        response = self.client.post(
            f'/api/applications/{self.application.application_id}/attachments/',
            {
                'file': file
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
        self.assertIn('details', response.data['error'])
        self.assertIn('attachment_type', response.data['error']['details'])
