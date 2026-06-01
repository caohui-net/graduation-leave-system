from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.attachments.models import Attachment, AttachmentType


class AttachmentListTestCase(TestCase):
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

        # Create counselors
        self.counselor = User.objects.create_user(
            user_id='T001',
            password='T001',
            name='李老师',
            role=UserRole.COUNSELOR
        )

        self.other_counselor = User.objects.create_user(
            user_id='T002',
            password='T002',
            name='王老师',
            role=UserRole.COUNSELOR
        )

        # Create dean
        self.dean = User.objects.create_user(
            user_id='D001',
            password='D001',
            name='赵主任',
            role=UserRole.DEAN
        )

        # Create class mappings
        ClassMapping.objects.create(
            class_id='CS2020-01',
            counselor=self.counselor,
            counselor_name='李老师',
            active=True
        )

        ClassMapping.objects.create(
            class_id='CS2020-02',
            counselor=self.other_counselor,
            counselor_name='王老师',
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

        # Create attachment
        self.attachment = Attachment.objects.create(
            attachment_id='att_test001',
            application=self.application,
            uploaded_by=self.student,
            file='test.pdf',
            attachment_type=AttachmentType.DORM_CHECKOUT,
            file_name='test.pdf',
            file_size=1024,
            content_type='application/pdf'
        )

        # Create pending dean approval
        self.dean_approval = Approval.objects.create(
            approval_id='apv_test001',
            application=self.application,
            step=ApprovalStep.DEAN,
            approver=self.dean,
            approver_name='赵主任',
            decision=ApprovalDecision.PENDING
        )

    def test_list_student_own_positive(self):
        """Student can list own application attachments"""
        self.client.force_authenticate(user=self.student)

        response = self.client.get(
            f'/api/applications/{self.application.application_id}/attachments/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['attachment_id'], 'att_test001')

    def test_list_student_other_negative(self):
        """Student cannot list another student's attachments"""
        self.client.force_authenticate(user=self.other_student)

        response = self.client.get(
            f'/api/applications/{self.application.application_id}/attachments/'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

    def test_list_assigned_counselor_positive(self):
        """Assigned counselor can list application attachments"""
        self.client.force_authenticate(user=self.counselor)

        response = self.client.get(
            f'/api/applications/{self.application.application_id}/attachments/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_cross_counselor_negative(self):
        """Cross-counselor cannot list application attachments"""
        self.client.force_authenticate(user=self.other_counselor)

        response = self.client.get(
            f'/api/applications/{self.application.application_id}/attachments/'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

    def test_list_dean_pending_approval_positive(self):
        """Dean with pending approval can list attachments"""
        self.client.force_authenticate(user=self.dean)

        response = self.client.get(
            f'/api/applications/{self.application.application_id}/attachments/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_excludes_soft_deleted(self):
        """List excludes soft-deleted attachments"""
        # Soft delete the attachment
        self.attachment.is_deleted = True
        self.attachment.save()

        self.client.force_authenticate(user=self.student)

        response = self.client.get(
            f'/api/applications/{self.application.application_id}/attachments/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
