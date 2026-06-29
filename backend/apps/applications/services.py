"""审批流程路由服务"""
from .models import ApplicationType, ApplicationStatus


def get_approval_flow(application_type):
    """根据申请类型返回审批流程"""
    # 统一转换为枚举值字符串进行比较
    app_type_value = application_type.value if hasattr(application_type, 'value') else application_type

    if app_type_value == ApplicationType.STAY_SCHOOL.value:
        return ['counselor']
    elif app_type_value == ApplicationType.LEAVE_SCHOOL.value:
        return ['dorm_manager', 'counselor']
    elif app_type_value == ApplicationType.LEAVE_REQUEST.value:
        return []
    return ['dorm_manager', 'counselor']


def get_initial_status(application_type):
    """根据申请类型返回初始状态"""
    # 统一转换为枚举值字符串进行比较
    app_type_value = application_type.value if hasattr(application_type, 'value') else application_type

    if app_type_value == ApplicationType.STAY_SCHOOL.value:
        return ApplicationStatus.PENDING_COUNSELOR
    elif app_type_value == ApplicationType.LEAVE_SCHOOL.value:
        return ApplicationStatus.PENDING_DORM_MANAGER
    return ApplicationStatus.DRAFT
