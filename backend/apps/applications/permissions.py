from apps.users.models import UserRole
from apps.users.class_mapping import ClassMapping
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision


def can_view_application(user, application):
    """Check if user can view application and its attachments."""
    if user.role == UserRole.STUDENT:
        return application.student_id == user.user_id

    if user.role == UserRole.COUNSELOR:
        return ClassMapping.objects.filter(
            counselor=user,
            class_id=application.class_id,
            active=True
        ).exists()

    if user.role == UserRole.DEAN:
        return Approval.objects.filter(
            application=application,
            approver=user,
            step=ApprovalStep.DEAN,
            decision=ApprovalDecision.PENDING
        ).exists()

    return False
