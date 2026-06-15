from apps.users.models import UserRole, User
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision


def can_view_application(user, application):
    """Check if user can view application and its attachments."""
    if user.role == UserRole.STUDENT:
        return application.student_id == user.user_id

    if user.role == UserRole.DORM_MANAGER:
        # Check if user has dorm manager approval assigned for this application
        return Approval.objects.filter(
            application=application,
            approver=user,
            step=ApprovalStep.DORM_MANAGER
        ).exists()

    if user.role == UserRole.COUNSELOR:
        # Check if user has counselor approval assigned for this application
        return Approval.objects.filter(
            application=application,
            approver=user,
            step=ApprovalStep.COUNSELOR
        ).exists()

    if user.role in [UserRole.DEAN, UserRole.ADMIN]:
        # Dean/Admin can view all applications
        return True

    return False
