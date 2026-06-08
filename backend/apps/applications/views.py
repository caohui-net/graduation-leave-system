from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Application, ApplicationStatus, DormCheckoutStatus
from .serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationListSerializer, ApplicationListResponseSerializer
from .pagination import ApplicationLimitOffsetPagination
from .providers import MockDormCheckoutProvider
from .permissions import can_view_application
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

    # Dorm Manager: applications with own pending dorm manager approvals
    elif user.role == UserRole.DORM_MANAGER:
        pending_approvals = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DORM_MANAGER,
            decision=ApprovalDecision.PENDING
        ).values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=pending_approvals)

    # Counselor: applications with own pending counselor approvals
    elif user.role == UserRole.COUNSELOR:
        pending_approvals = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR,
            decision=ApprovalDecision.PENDING
        ).values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=pending_approvals)

    # Dean: view all approved applications (archiving role, read-only)
    elif user.role == UserRole.DEAN:
        queryset = Application.objects.filter(status=ApplicationStatus.APPROVED)

    # Admin: view all applications (management role)
    elif user.role == UserRole.ADMIN:
        queryset = Application.objects.all()

    else:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # Status filtering
    status_param = request.query_params.get('status')
    if status_param:
        queryset = queryset.filter(status=status_param)

    # Sort by created_at DESC
    queryset = queryset.order_by('-created_at', '-application_id')

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

    serializer = ApplicationCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
                                    'details': serializer.errors}},
                        status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        # Check for existing pending/approved applications
        existing = Application.objects.select_for_update().filter(
            student=user,
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
            from django.conf import settings
            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
            try:
                fallback_manager = User.objects.get(role=UserRole.DORM_MANAGER, user_id=fallback_id, active=True)
                dorm_managers = [fallback_manager]
            except User.DoesNotExist:
                return Response({'error': {'code': 'NOT_FOUND', 'message': '无可用宿管员',
                                            'details': {'building': building or '未分配', 'fallback_id': fallback_id}}},
                                status=status.HTTP_404_NOT_FOUND)

        # Check for existing draft, convert if exists
        draft = Application.objects.select_for_update().filter(student=user, status=ApplicationStatus.DRAFT).first()

        if draft:
            # Update draft to submitted application
            draft.contact_phone = serializer.validated_data['contact_phone']
            draft.reason = serializer.validated_data.get('reason', '')
            draft.leave_date = serializer.validated_data['leave_date']
            draft.status = ApplicationStatus.PENDING_DORM_MANAGER
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
                leave_date=serializer.validated_data['leave_date'],
                status=ApplicationStatus.PENDING_DORM_MANAGER,
                dorm_checkout_status=dorm_status.status
            )

        # Create approvals
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
        application = Application.objects.get(application_id=application_id)
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
    draft = Application.objects.create(
        application_id=f'app_{uuid.uuid4().hex[:8]}',
        student=user,
        student_name=user.name,
        class_id=user.class_id,
        status=ApplicationStatus.DRAFT
    )

    return Response(ApplicationSerializer(draft).data, status=status.HTTP_201_CREATED)
