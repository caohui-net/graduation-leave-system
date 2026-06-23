"""留校审批功能测试"""
from django.test import TestCase
from apps.applications.models import Application, ApplicationType, ApplicationStatus
from apps.applications.services import get_approval_flow, get_initial_status


class ApprovalFlowTest(TestCase):
    def test_stay_school_flow(self):
        """留校申请应该只需要辅导员审批"""
        flow = get_approval_flow(ApplicationType.STAY_SCHOOL)
        self.assertEqual(flow, ['counselor'])

    def test_leave_school_flow(self):
        """离校申请需要宿管员和辅导员审批"""
        flow = get_approval_flow(ApplicationType.LEAVE_SCHOOL)
        self.assertEqual(flow, ['dorm_manager', 'counselor'])

    def test_stay_school_initial_status(self):
        """留校申请初始状态应为待辅导员审批"""
        status = get_initial_status(ApplicationType.STAY_SCHOOL)
        self.assertEqual(status, ApplicationStatus.PENDING_COUNSELOR)

    def test_leave_school_initial_status(self):
        """离校申请初始状态应为待宿管员审批"""
        status = get_initial_status(ApplicationType.LEAVE_SCHOOL)
        self.assertEqual(status, ApplicationStatus.PENDING_DORM_MANAGER)
