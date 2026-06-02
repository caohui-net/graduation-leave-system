from apps.applications.models import ApplicationStatus


EXPECTED_STATUS_BY_STEP = {
    'dorm_manager': ApplicationStatus.PENDING_DORM_MANAGER,
    'counselor': ApplicationStatus.PENDING_COUNSELOR,
    'dean': ApplicationStatus.PENDING_DEAN,
}


def approval_step_matches_application_status(approval):
    expected_status = EXPECTED_STATUS_BY_STEP.get(approval.step)
    if expected_status is None:
        return False
    return approval.application.status == expected_status
