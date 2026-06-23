"""
Tests for stay school application workflow
"""
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from apps.applications.models import Application, ApplicationType, ApplicationStatus
from apps.applications.services import get_initial_status

User = get_user_model()


class StaySchoolApplicationTestCase(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            user_id='test001',
            name='测试学生',
            role='student',
            building='1号楼',
            room_number='101'
        )
        self.counselor = User.objects.create_user(
            user_id='counselor001',
            name='辅导员',
            role='counselor'
        )

    @override_settings(FEATURE_FLAGS={'stay_school_approval': True})
    def test_stay_school_initial_status(self):
        """留校申请初始状态应为PENDING_COUNSELOR"""
        status = get_initial_status(ApplicationType.STAY_SCHOOL)
        self.assertEqual(status, ApplicationStatus.PENDING_COUNSELOR)

    def test_leave_school_initial_status(self):
        """离校申请初始状态应为PENDING_DORM_MANAGER"""
        status = get_initial_status(ApplicationType.LEAVE_SCHOOL)
        self.assertEqual(status, ApplicationStatus.PENDING_DORM_MANAGER)

    @override_settings(FEATURE_FLAGS={'stay_school_approval': True})
    def test_create_stay_school_application(self):
        """测试创建留校申请"""
        app = Application.objects.create(
            student=self.student,
            application_type=ApplicationType.STAY_SCHOOL,
            stay_start_date='2026-07-01',
            stay_end_date='2026-08-31',
            stay_reason='exam_prep',
            contact_phone='13800138000',
            status=get_initial_status(ApplicationType.STAY_SCHOOL)
        )
        self.assertEqual(app.application_type, ApplicationType.STAY_SCHOOL)
        self.assertEqual(app.status, ApplicationStatus.PENDING_COUNSELOR)
        self.assertIsNotNone(app.stay_start_date)

    def test_create_leave_school_application(self):
        """测试创建离校申请"""
        app = Application.objects.create(
            student=self.student,
            application_type=ApplicationType.LEAVE_SCHOOL,
            leave_date='2026-06-30',
            contact_phone='13800138000',
            status=get_initial_status(ApplicationType.LEAVE_SCHOOL)
        )
        self.assertEqual(app.application_type, ApplicationType.LEAVE_SCHOOL)
        self.assertEqual(app.status, ApplicationStatus.PENDING_DORM_MANAGER)
