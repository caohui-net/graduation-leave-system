"""审批流程路由服务"""
from .models import ApplicationType, ApplicationStatus


def get_approval_flow(application_type):
    """根据申请类型返回审批流程"""
    if application_type == ApplicationType.STAY_SCHOOL:
        return ['counselor']
    elif application_type == ApplicationType.LEAVE_SCHOOL:
        return ['dorm_manager', 'counselor']
    elif application_type == ApplicationType.LEAVE_REQUEST:
        return []
    return ['dorm_manager', 'counselor']


def get_initial_status(application_type):
    """根据申请类型返回初始状态"""
    if application_type == ApplicationType.STAY_SCHOOL:
        return ApplicationStatus.PENDING_COUNSELOR
    elif application_type == ApplicationType.LEAVE_SCHOOL:
        return ApplicationStatus.PENDING_DORM_MANAGER
    return ApplicationStatus.DRAFT
