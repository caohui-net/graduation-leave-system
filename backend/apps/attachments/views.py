from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.http import FileResponse, Http404
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from apps.users.models import UserRole
from apps.applications.models import Application
from apps.applications.permissions import can_view_application
from apps.approvals.models import Approval, ApprovalStep
from .models import Attachment
from .serializers import AttachmentUploadSerializer, AttachmentSerializer, AttachmentListResponseSerializer
from schema import ErrorResponseSerializer
import uuid


@extend_schema(
    methods=['GET'],
    operation_id='attachments_list',
    summary='获取附件列表',
    description='获取指定申请的附件列表',
    responses={
        200: AttachmentListResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
    tags=['附件']
)
@extend_schema(
    methods=['POST'],
    operation_id='attachments_upload',
    summary='上传附件',
    description='为指定申请上传附件（仅申请所有者可上传）',
    request=AttachmentUploadSerializer,
    responses={
        201: AttachmentSerializer,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
    tags=['附件']
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def attachments_view(request, application_id):
    """Dispatcher for attachment list (GET) and upload (POST)"""
    if request.method == 'GET':
        return list_attachments(request, application_id)
    else:
        return upload_attachment(request, application_id)


def upload_attachment(request, application_id):
    user = request.user

    # Get application
    try:
        application = Application.objects.get(application_id=application_id)
    except Application.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在'}},
                        status=status.HTTP_404_NOT_FOUND)

    # Permission: only student who owns the application
    if user.role != UserRole.STUDENT or application.student_id != user.user_id:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限上传附件'}},
                        status=status.HTTP_403_FORBIDDEN)

    # Validate
    serializer = AttachmentUploadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
                                    'details': serializer.errors}},
                        status=status.HTTP_400_BAD_REQUEST)

    # Create attachment
    file = serializer.validated_data['file']
    attachment = Attachment.objects.create(
        attachment_id=f'att_{uuid.uuid4().hex[:12]}',
        application=application,
        uploaded_by=user,
        file=file,
        attachment_type=serializer.validated_data['attachment_type'],
        file_name=file.name,
        file_size=file.size,
        content_type=file.content_type or 'application/octet-stream'
    )

    return Response(AttachmentSerializer(attachment).data, status=status.HTTP_201_CREATED)


def list_attachments(request, application_id):
    user = request.user

    # Get application
    try:
        application = Application.objects.get(application_id=application_id)
    except Application.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在'}},
                        status=status.HTTP_404_NOT_FOUND)

    # Permission check using shared helper
    if not can_view_application(user, application):
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限查看附件'}},
                        status=status.HTTP_403_FORBIDDEN)

    # List attachments (exclude soft-deleted)
    attachments = Attachment.objects.filter(application=application, is_deleted=False)
    serializer = AttachmentSerializer(attachments, many=True)
    return Response({'attachments': serializer.data})


@extend_schema(
    operation_id='attachments_download',
    summary='下载附件',
    description='下载指定附件文件',
    responses={
        200: OpenApiResponse(response=OpenApiTypes.BINARY, description='附件文件内容'),
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
    tags=['附件']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_attachment(request, attachment_id):
    user = request.user

    # Get attachment
    try:
        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
    except Attachment.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
                        status=status.HTTP_404_NOT_FOUND)

    # Check if soft-deleted
    if attachment.is_deleted:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
                        status=status.HTTP_404_NOT_FOUND)

    # Permission check using shared helper
    application = attachment.application
    if not can_view_application(user, application):
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限下载附件'}},
                        status=status.HTTP_403_FORBIDDEN)

    # Return file
    try:
        return FileResponse(attachment.file.open('rb'), as_attachment=True, filename=attachment.file_name, content_type=attachment.content_type)
    except FileNotFoundError:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '文件不存在'}},
                        status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    operation_id='attachments_delete',
    summary='删除附件',
    description='软删除指定附件（仅申请所有者可删除）',
    request=None,
    responses={
        204: OpenApiResponse(description='删除成功'),
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
    tags=['附件']
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_attachment(request, attachment_id):
    user = request.user

    # Get attachment
    try:
        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
    except Attachment.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
                        status=status.HTTP_404_NOT_FOUND)

    # Check if already deleted
    if attachment.is_deleted:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
                        status=status.HTTP_404_NOT_FOUND)

    # Permission: only student who owns the application
    if user.role != UserRole.STUDENT or attachment.application.student_id != user.user_id:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限删除附件'}},
                        status=status.HTTP_403_FORBIDDEN)

    # Soft delete
    attachment.is_deleted = True
    attachment.deleted_at = timezone.now()
    attachment.save()

    return Response(status=status.HTTP_204_NO_CONTENT)
