from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    """
    GET /api/notifications/
    列出当前用户的通知
    查询参数：
    - read: all/read/unread (默认all)
    - limit: 每页数量 (默认20)
    - offset: 偏移量 (默认0)
    """
    user = request.user
    read_filter = request.query_params.get('read', 'all')
    limit = int(request.query_params.get('limit', 20))
    offset = int(request.query_params.get('offset', 0))

    queryset = Notification.objects.filter(recipient=user)

    if read_filter == 'read':
        queryset = queryset.filter(read_at__isnull=False)
    elif read_filter == 'unread':
        queryset = queryset.filter(read_at__isnull=True)

    count = queryset.count()
    notifications = queryset[offset:offset + limit]
    serializer = NotificationSerializer(notifications, many=True)

    return Response({
        'count': count,
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_count(request):
    """
    GET /api/notifications/unread_count/
    获取当前用户的未读通知数
    """
    user = request.user
    count = Notification.objects.filter(recipient=user, read_at__isnull=True).count()
    return Response({'unread_count': count})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id):
    """
    PATCH /api/notifications/{notification_id}/read/
    标记通知为已读（幂等）
    """
    user = request.user

    try:
        notification = Notification.objects.get(notification_id=notification_id)
    except Notification.DoesNotExist:
        return Response(
            {'error': {'code': 'NOT_FOUND', 'message': '通知不存在'}},
            status=status.HTTP_404_NOT_FOUND
        )

    if notification.recipient != user:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '无权访问此通知'}},
            status=status.HTTP_403_FORBIDDEN
        )

    if notification.read_at is None:
        notification.read_at = timezone.now()
        notification.save(update_fields=['read_at'])

    serializer = NotificationSerializer(notification)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_read(request):
    """
    POST /api/notifications/mark_all_read/
    标记当前用户的所有未读通知为已读
    """
    user = request.user
    now = timezone.now()
    updated_count = Notification.objects.filter(
        recipient=user,
        read_at__isnull=True
    ).update(read_at=now)

    return Response({'marked_count': updated_count})
