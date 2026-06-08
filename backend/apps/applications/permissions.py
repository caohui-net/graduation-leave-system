from apps.users.models import UserRole, User
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision


def can_view_application(user, application):
    """Check if user can view application and its attachments."""
    if user.role == UserRole.STUDENT:
        return application.student_id == user.user_id

    if user.role == UserRole.DORM_MANAGER:
        student = User.objects.filter(user_id=application.student_id).first()
        if not student or not student.building:
            return False
        return user.building == student.building

    if user.role == UserRole.COUNSELOR:
        student = User.objects.filter(user_id=application.student_id).first()
        if not student or not student.department:
            return False
        return user.department == student.department

    if user.role in [UserRole.DEAN, UserRole.ADMIN]:
        # Dean/Admin can view all applications (archiving and management role)
        return True

    return False
