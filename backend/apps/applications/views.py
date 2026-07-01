from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Application, ApplicationStatus, DormCheckoutStatus, ApplicationType
from .serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationListSerializer, ApplicationListResponseSerializer
from .pagination import ApplicationLimitOffsetPagination
from .providers import MockDormCheckoutProvider
from .permissions import can_view_application
from .services import get_initial_status, get_approval_flow
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.users.models import UserRole, User
from apps.notifications.services import notify_application_submitted
from schema import ErrorResponseSerializer
import uuid
import logging


@extend_schema(
    methods=['GET'],
    operation_id='applications_list',
    summary='获取申请列表',
    description='获取当前用户的申请列表（学生/辅导员/学工部）',
    parameters=[
        OpenApiParameter('status', str, description='状态过滤'),
        OpenApiParameter('student_name', str, description='学生姓名模糊查询'),
        OpenApiParameter('student_id', str, description='学号精确查询'),
        OpenApiParameter('class_id', str, description='班级筛选'),
        OpenApiParameter('building', str, description='宿舍楼筛选'),
        OpenApiParameter('limit', int, description='每页数量（默认20）'),
        OpenApiParameter('offset', int, description='偏移量（默认0）'),
    ],
    responses={
        200: ApplicationListResponseSerializer,
        403: ErrorResponseSerializer,
    },
    tags=['申请']
)
@extend_schema(
    methods=['POST'],
    operation_id='applications_create',
    summary='提交离校申请',
    description='学生提交新的离校申请',
    request=ApplicationCreateSerializer,
    responses={
        201: ApplicationSerializer,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
        422: ErrorResponseSerializer,
    },
    tags=['申请']
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def applications_view(request):
    if request.method == 'GET':
        return list_applications(request)
    else:
        return create_application(request)


def list_applications(request):
    user = request.user

    # Student: own applications only
    if user.role == UserRole.STUDENT:
        queryset = Application.objects.filter(student=user)

    # Dorm Manager: applications with own dorm manager approvals
    elif user.role == UserRole.DORM_MANAGER:
        my_approvals_qs = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DORM_MANAGER
        )

        # Decision filtering for dorm manager
        decision_param = request.query_params.get('decision')
        if decision_param and decision_param != 'all':
            my_approvals_qs = my_approvals_qs.filter(decision=decision_param)

        my_approvals = my_approvals_qs.values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=my_approvals)

    # Counselor: applications with own counselor approvals
    elif user.role == UserRole.COUNSELOR:
        my_approvals_qs = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR
        )

        # Decision filtering for counselor
        decision_param = request.query_params.get('decision')
        if decision_param and decision_param != 'all':
            my_approvals_qs = my_approvals_qs.filter(decision=decision_param)

        my_approvals = my_approvals_qs.values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=my_approvals)

    # Dean/Admin: view all applications
    elif user.role in [UserRole.DEAN, UserRole.ADMIN]:
        queryset = Application.objects.all()

    else:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # Application type filtering
    app_type = request.query_params.get('application_type')
    if app_type:
        queryset = queryset.filter(application_type=app_type)

    # Status filtering
    status_param = request.query_params.get('status')
    if status_param:
        queryset = queryset.filter(status=status_param)

    # Additional query filters (for non-students)
    if user.role in [UserRole.DEAN, UserRole.ADMIN, UserRole.DORM_MANAGER, UserRole.COUNSELOR]:
        student_name = request.query_params.get('student_name')
        if student_name:
            queryset = queryset.filter(student_name__icontains=student_name)

        student_id = request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student__user_id__icontains=student_id)

        class_id = request.query_params.get('class_id')
        if class_id:
            queryset = queryset.filter(class_id__icontains=class_id)

        building = request.query_params.get('building')
        if building:
            queryset = queryset.filter(student__building__icontains=building)

    # Sort by created_at DESC
    queryset = queryset.order_by('-created_at', '-application_id')

    # Optimize queries: prefetch related objects to avoid N+1
    queryset = queryset.select_related('student').prefetch_related('approvals__approver')

    # Paginate
    paginator = ApplicationLimitOffsetPagination()
    page = paginator.paginate_queryset(queryset, request)

    # Serialize
    serializer = ApplicationListSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


def create_application(request):
    from django.db import transaction

    user = request.user

    if user.role != UserRole.STUDENT:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以提交申请'}},
                        status=status.HTTP_403_FORBIDDEN)

    # Feature Flag检查
    app_type = request.data.get('application_type', ApplicationType.LEAVE_SCHOOL)
    if app_type == ApplicationType.STAY_SCHOOL and not settings.FEATURE_FLAGS.get('stay_school_approval', False):
        return Response({'error': {'code': 'FEATURE_DISABLED', 'message': '留校申请功能未开放'}},
                        status=status.HTTP_403_FORBIDDEN)
    if app_type == ApplicationType.LEAVE_REQUEST and not settings.FEATURE_FLAGS.get('leave_request_approval', False):
        return Response({'error': {'code': 'FEATURE_DISABLED', 'message': '请假申请功能未开放'}},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = ApplicationCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
                                    'details': serializer.errors}},
                        status=status.HTTP_400_BAD_REQUEST)

    # 获取草稿ID参数（可选）
    application_id = request.data.get('application_id')

    with transaction.atomic():
        # Check for existing pending/approved applications
        existing = Application.objects.select_for_update().filter(
            student=user,
            application_type=app_type,
            status__in=[ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.APPROVED]
        ).first()
        if existing:
            return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
                                        'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
                            status=status.HTTP_409_CONFLICT)

        provider = MockDormCheckoutProvider()
        dorm_status = provider.check_status(user.user_id)

        if dorm_status.status != DormCheckoutStatus.COMPLETED:
            return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
                                        'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
                                                    'blocking_reason': dorm_status.blocking_reason}}},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Find dorm managers
        dorm_managers = []
        building = user.building

        if building and building.strip():
            dorm_managers = list(User.objects.filter(
                role=UserRole.DORM_MANAGER,
                building=building,
                active=True
            ).order_by('user_id'))

        if not dorm_managers:
            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
            try:
                fallback_manager = User.objects.get(role=UserRole.DORM_MANAGER, user_id=fallback_id, active=True)
                dorm_managers = [fallback_manager]
            except User.DoesNotExist:
                return Response({'error': {'code': 'NOT_FOUND', 'message': '无可用宿管员',
                                            'details': {'building': building or '未分配', 'fallback_id': fallback_id}}},
                                status=status.HTTP_404_NOT_FOUND)

        # Find counselors: support manual selection or auto-match by department
        counselor_id = request.data.get('counselor_id')
        counselors = []

        if counselor_id:
            # Student selected a specific counselor
            try:
                # 研究生允许选择研工部辅导员
                if user.level == '研究生':
                    counselor = User.objects.get(
                        user_id=counselor_id,
                        role=UserRole.COUNSELOR,
                        department='研工部',
                        active=True
                    )
                else:
                    counselor = User.objects.get(
                        user_id=counselor_id,
                        role=UserRole.COUNSELOR,
                        department=user.department,
                        active=True
                    )
                counselors = [counselor]
            except User.DoesNotExist:
                return Response({'error': {'code': 'NOT_FOUND', 'message': '选择的辅导员不存在或不属于该学院',
                                            'details': {'counselor_id': counselor_id}}},
                                status=status.HTTP_404_NOT_FOUND)
        elif user.level == '研究生':
            # 研究生特殊处理：直接指定金玲老师（研工部）
            counselors = list(User.objects.filter(
                user_id='20210066',
                role=UserRole.COUNSELOR,
                active=True
            ))
        elif user.department:
            # Auto-match all counselors in student's department
            counselors_query = User.objects.filter(
                role=UserRole.COUNSELOR,
                department=user.department,
                active=True
            )

            # 留校业务：排除胡乐老师（工号20220052，仅参与离校业务）
            if app_type == ApplicationType.STAY_SCHOOL:
                counselors_query = counselors_query.exclude(user_id='20220052')

            counselors = list(counselors_query)

        # Check for existing draft, convert if exists
        if application_id:
            # 精确查找指定草稿
            draft = Application.objects.select_for_update().filter(
                student=user,
                application_id=application_id,
                status=ApplicationStatus.DRAFT
            ).first()
            if not draft:
                return Response({'error': {'code': 'NOT_FOUND', 'message': '草稿不存在或已提交'}},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            # 回退：自动查找任意草稿（向后兼容）
            draft = Application.objects.select_for_update().filter(student=user, status=ApplicationStatus.DRAFT).first()

        if draft:
            # Update draft to submitted application
            if not draft.application_id:
                draft.application_id = f'app_{uuid.uuid4().hex[:8]}'
            draft.contact_phone = serializer.validated_data['contact_phone']
            draft.reason = serializer.validated_data.get('reason', '')
            draft.leave_date = serializer.validated_data.get('leave_date')
            draft.application_type = app_type
            draft.stay_start_date = serializer.validated_data.get('stay_start_date')
            draft.stay_end_date = serializer.validated_data.get('stay_end_date')
            draft.stay_reason = serializer.validated_data.get('stay_reason')
            draft.status = get_initial_status(app_type)
            draft.dorm_checkout_status = dorm_status.status
            draft.save()
            application = draft
        else:
            # Create new application
            application = Application.objects.create(
                application_id=f'app_{uuid.uuid4().hex[:8]}',
                student=user,
                student_name=user.name,
                class_id=user.class_id,
                contact_phone=serializer.validated_data['contact_phone'],
                reason=serializer.validated_data.get('reason', ''),
                leave_date=serializer.validated_data.get('leave_date'),
                application_type=app_type,
                stay_start_date=serializer.validated_data.get('stay_start_date'),
                stay_end_date=serializer.validated_data.get('stay_end_date'),
                stay_reason=serializer.validated_data.get('stay_reason'),
                status=get_initial_status(app_type),
                dorm_checkout_status=dorm_status.status
            )

        # Create approvals based on flow
        approval_flow = get_approval_flow(app_type)

        if 'dorm_manager' in approval_flow:
            for dorm_manager in dorm_managers:
                dorm_manager_approval = Approval.objects.create(
                    approval_id=f'apv_{uuid.uuid4().hex[:8]}',
                    application=application,
                    step=ApprovalStep.DORM_MANAGER,
                    approver=dorm_manager,
                    approver_name=dorm_manager.name,
                    decision=ApprovalDecision.PENDING
                )
                notify_application_submitted(application, dorm_manager_approval)

        if 'counselor' in approval_flow:
            if not counselors:
                return Response({'error': {'code': 'NOT_FOUND', 'message': '未找到辅导员',
                                            'details': {'department': user.department}}},
                                status=status.HTTP_404_NOT_FOUND)
            for counselor in counselors:
                counselor_approval = Approval.objects.create(
                    approval_id=f'apv_{uuid.uuid4().hex[:8]}',
                    application=application,
                    step=ApprovalStep.COUNSELOR,
                    approver=counselor,
                    approver_name=counselor.name,
                    decision=ApprovalDecision.PENDING
                )
                notify_application_submitted(application, counselor_approval)

        # Sync phone to User table
        if not user.phone:
            user.phone = serializer.validated_data['contact_phone']
            user.save()

    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)


@extend_schema(
    operation_id='applications_get',
    summary='获取申请详情',
    description='获取指定申请的详细信息（包括审批记录）',
    responses={
        200: ApplicationSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
    tags=['申请']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_application(request, application_id):
    try:
        application = Application.objects.select_related('student').prefetch_related('approvals__approver').get(application_id=application_id)
    except Application.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在',
                                    'details': {'application_id': application_id}}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user

    # Check permission using shared helper
    if not can_view_application(user, application):
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
                        status=status.HTTP_403_FORBIDDEN)

    return Response(ApplicationSerializer(application).data)


@extend_schema(
    operation_id='applications_draft',
    summary='获取或创建草稿申请',
    description='学生获取或创建草稿申请，用于附件上传前置',
    responses={
        200: ApplicationSerializer,
        201: ApplicationSerializer,
        403: ErrorResponseSerializer,
    },
    tags=['申请']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_or_create_draft(request):
    from django.db import transaction

    user = request.user

    if user.role != UserRole.STUDENT:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以创建草稿'}},
                        status=status.HTTP_403_FORBIDDEN)

    with transaction.atomic():
        # Get existing draft or create new one
        draft = Application.objects.select_for_update().filter(student=user, status=ApplicationStatus.DRAFT).first()

    if draft:
        return Response(ApplicationSerializer(draft).data, status=status.HTTP_200_OK)

    # Create new draft
    # Refresh user from DB if class_id is None (JWT token may not include all fields)
    if user.class_id is None:
        user.refresh_from_db()

    draft = Application.objects.create(
        application_id=f'app_{uuid.uuid4().hex[:8]}',
        student=user,
        student_name=user.name,
        class_id=user.class_id,
        status=ApplicationStatus.DRAFT
    )

    return Response(ApplicationSerializer(draft).data, status=status.HTTP_201_CREATED)


@extend_schema(
    operation_id='applications_stats',
    summary='获取申请统计',
    description='学工部获取各状态申请统计数据',
    responses={
        200: {
            'type': 'object',
            'properties': {
                'total': {'type': 'integer'},
                'draft': {'type': 'integer'},
                'pending_dorm_manager': {'type': 'integer'},
                'pending_counselor': {'type': 'integer'},
                'approved': {'type': 'integer'},
                'rejected': {'type': 'integer'}
            }
        },
        403: ErrorResponseSerializer,
    },
    tags=['申请']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stats(request):
    if request.user.role not in [UserRole.DEAN, UserRole.ADMIN]:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '仅学工部/管理员可查看统计'}},
            status=status.HTTP_403_FORBIDDEN
        )

    from django.db.models import Count

    # Filter by application_type
    queryset = Application.objects.all()
    app_type = request.query_params.get('application_type')
    if app_type:
        queryset = queryset.filter(application_type=app_type)

    stats = queryset.values('status').annotate(count=Count('status'))

    result = {
        'total': queryset.count(),
        'draft': 0,
        'pending_dorm_manager': 0,
        'pending_counselor': 0,
        'approved': 0,
        'rejected': 0
    }

    for item in stats:
        status_key = item['status']
        result[status_key] = item['count']

    return Response(result)
