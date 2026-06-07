"""
Notification service layer for idempotent notification creation.

This module provides business logic for creating notifications automatically
when key events occur (application submission, approval decisions).
"""

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Notification, NotificationType
from apps.approvals.models import ApprovalDecision

User = get_user_model()


def notify_application_submitted(application, approval):
    """
    Create notification for counselor when student submits application.

    Args:
        application: Application instance
        approval: Counselor approval instance

    Returns:
        tuple: (Notification instance, created boolean)
    """
    title = "新的离校申请"
    message = f"学生{application.student_name}（{application.student.user_id}）提交了离校申请，请及时审批。"

    return Notification.objects.get_or_create(
        recipient=approval.approver,
        entity_type='approval',
        entity_id=approval.pk,
        type=NotificationType.APPLICATION_SUBMITTED,
        defaults={
            'actor': application.student,
            'title': title,
            'message': message
        }
    )


def notify_approval_decided(approval):
    """
    Create notification for student when approval is approved or rejected.

    Args:
        approval: Approval instance with decision

    Returns:
        tuple: (Notification instance, created boolean)
    """
    approver_role_map = {
        "dorm_manager": "宿管员",
        "counselor": "辅导员",
    }
    approver_role = approver_role_map.get(approval.step, "审批人")

    if approval.decision == ApprovalDecision.APPROVED:
        title = "审批通过"
        message = f"您的离校申请已通过{approver_role}审批。"
        notification_type = NotificationType.APPROVAL_APPROVED
    else:  # rejected
        title = "审批驳回"
        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
        notification_type = NotificationType.APPROVAL_REJECTED

    return Notification.objects.get_or_create(
        recipient=approval.application.student,
        entity_type='approval',
        entity_id=approval.pk,
        type=notification_type,
        defaults={
            'actor': approval.approver,
            'title': title,
            'message': message
        }
    )


def create_approval_timeout_warnings(now=None, dry_run=False):
    """
    Create timeout warning notifications for pending approvals.

    Args:
        now: Current time (for testing), defaults to timezone.now()
        dry_run: If True, only simulate without creating notifications

    Returns:
        dict: {created: int, skipped: int, warnings: list}
    """
    from apps.approvals.models import Approval

    if now is None:
        now = timezone.now()

    dorm_manager_threshold = now - timedelta(days=2)
    counselor_threshold = now - timedelta(days=3)

    pending_approvals = Approval.objects.filter(
        decision=ApprovalDecision.PENDING
    ).select_related('approver', 'application__student')

    created_count = 0
    skipped_count = 0
    warnings = []

    for approval in pending_approvals:
        threshold = counselor_threshold if approval.step == 'counselor' else dorm_manager_threshold

        if approval.created_at > threshold:
            continue

        days = (now - approval.created_at).days
        title = "审批超时提醒"
        message = f"学生{approval.application.student_name}的离校申请已超过{days}天未审批，请及时处理。"

        if dry_run:
            warnings.append({
                'approval_id': approval.pk,
                'approver': approval.approver.name,
                'days': days
            })
            created_count += 1
        else:
            notification, created = Notification.objects.get_or_create(
                recipient=approval.approver,
                entity_type='approval',
                entity_id=approval.pk,
                type=NotificationType.APPROVAL_TIMEOUT_WARNING,
                defaults={
                    'actor': None,
                    'title': title,
                    'message': message
                }
            )
            if created:
                created_count += 1
                warnings.append({
                    'notification_id': notification.notification_id,
                    'approval_id': approval.pk,
                    'approver': approval.approver.name,
                    'days': days
                })
            else:
                skipped_count += 1

    return {
        'created': created_count,
        'skipped': skipped_count,
        'warnings': warnings
    }
