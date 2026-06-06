from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.users.class_mapping import ClassMapping


class ApprovalPermissionsTestCase(TestCase):
    def setUp(self):
        # Create students
        self.student1 = User.objects.create_user(
            user_id='2020001',
            name='张三',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            password='2020001',
            building='1号楼',
            department='计算机学院'
        )
        self.student2 = User.objects.create_user(
            user_id='2020002',
            name='李四',
            role=UserRole.STUDENT,
            class_id='CS2020-02',
            password='2020002',
            building='2号楼',
            department='软件学院'
        )

        # Create counselors
        self.counselor1 = User.objects.create_user(
            user_id='T001',
            name='李老师',
            role=UserRole.COUNSELOR,
            password='T001',
            department='计算机学院'
        )
        self.counselor2 = User.objects.create_user(
            user_id='T002',
            name='王老师',
            role=UserRole.COUNSELOR,
            password='T002',
            department='软件学院'
        )
        self.dorm_manager1 = User.objects.create_user(
            user_id='M001',
            name='宿管员1',
            role=UserRole.DORM_MANAGER,
            password='M001',
            building='1号楼'
        )
        self.dorm_manager2 = User.objects.create_user(
            user_id='M002',
            name='宿管员2',
            role=UserRole.DORM_MANAGER,
            password='M002',
            building='2号楼'
        )
        self.dean1 = User.objects.create_user(
            user_id='D001',
            name='赵主任',
            role=UserRole.DEAN,
            password='D001'
        )
        self.dean2 = User.objects.create_user(
            user_id='D002',
            name='钱主任',
            role=UserRole.DEAN,
            password='D002'
        )

        # Create class mappings
        ClassMapping.objects.create(
            class_id='CS2020-01',
            dorm_manager=self.dorm_manager1,
            dorm_manager_name='宿管员1',
            counselor=self.counselor1,
            counselor_name='李老师',
            active=True
        )
        ClassMapping.objects.create(
            class_id='CS2020-02',
            dorm_manager=self.dorm_manager2,
            dorm_manager_name='宿管员2',
            counselor=self.counselor2,
            counselor_name='王老师',
            active=True
        )

        # Create application for student1
        self.application1 = Application.objects.create(
            application_id='app_test001',
            student=self.student1,
            student_name='张三',
            class_id='CS2020-01',
            reason='测试原因',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        # Create counselor approval for application1
        self.approval1 = Approval.objects.create(
            approval_id='apv_test001',
            application=self.application1,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor1,
            approver_name='李老师',
            decision=ApprovalDecision.PENDING
        )

        self.client = APIClient()

    def _create_dorm_manager_approval(self):
        self.application1.status = ApplicationStatus.PENDING_DORM_MANAGER
        self.application1.save()
        return Approval.objects.create(
            approval_id='apv_test002',
            application=self.application1,
            step=ApprovalStep.DORM_MANAGER,
            approver=self.dorm_manager1,
            approver_name='宿管员1',
            decision=ApprovalDecision.PENDING
        )

    def test_student_cannot_approve_or_reject(self):
        """学生不能调用审批操作接口"""
        self.client.force_authenticate(user=self.student1)

        approve_response = self.client.post(
            f'/api/approvals/{self.approval1.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )
        reject_response = self.client.post(
            f'/api/approvals/{self.approval1.approval_id}/reject/',
            {'comment': '不同意'},
            format='json'
        )

        self.assertEqual(approve_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reject_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_dean_cannot_act_on_counselor_step(self):
        """学工部不能处理辅导员审批步骤"""
        self.client.force_authenticate(user=self.dean1)

        response = self.client.post(
            f'/api/approvals/{self.approval1.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_counselor_cannot_act_on_dorm_manager_step(self):
        """辅导员不能处理宿管员审批步骤"""
        dorm_manager_approval = self._create_dorm_manager_approval()
        self.client.force_authenticate(user=self.counselor1)

        response = self.client.post(
            f'/api/approvals/{dorm_manager_approval.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_assigned_dorm_manager_forbidden(self):
        """同角色但非指定宿管员审批人不能处理审批"""
        dorm_manager_approval = self._create_dorm_manager_approval()
        self.client.force_authenticate(user=self.dorm_manager2)

        response = self.client.post(
            f'/api/approvals/{dorm_manager_approval.approval_id}/reject/',
            {'comment': '不同意'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cross_counselor_approve_forbidden(self):
        """测试跨辅导员审批返回403"""
        # T002 tries to approve T001's application
        self.client.force_authenticate(user=self.counselor2)
        response = self.client.post(
            f'/api/approvals/{self.approval1.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cross_counselor_reject_forbidden(self):
        """测试跨辅导员驳回返回403"""
        # T002 tries to reject T001's application
        self.client.force_authenticate(user=self.counselor2)
        response = self.client.post(
            f'/api/approvals/{self.approval1.approval_id}/reject/',
            {'comment': '不同意'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
