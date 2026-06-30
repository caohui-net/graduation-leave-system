import os
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import LoginSerializer, LoginResponseSerializer, DemoLoginSerializer
from .models import User, UserRole
from schema import ErrorResponseSerializer


class LoginRateThrottle(AnonRateThrottle):
    rate = '5/minute'


@extend_schema(
    operation_id='auth_login',
    summary='用户登录',
    description='使用用户ID和密码登录，返回JWT access token',
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            response=LoginResponseSerializer,
            description='登录成功，返回access token和用户信息'
        ),
        400: OpenApiResponse(
            description='登录失败：DRF默认ValidationError格式（非项目envelope）'
        ),
        429: OpenApiResponse(
            description='请求过于频繁，请稍后重试'
        ),
    },
    tags=['认证']
)
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([LoginRateThrottle])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    operation_id='auth_demo_login',
    summary='演示登录（仅开发/演示环境）',
    description='按角色快速登录演示账号。生产环境必须禁用（DEMO_AUTH_ENABLED=false）。',
    request=DemoLoginSerializer,
    responses={
        200: OpenApiResponse(
            response=LoginResponseSerializer,
            description='登录成功，返回access token和用户信息'
        ),
        403: OpenApiResponse(
            description='演示登录已禁用'
        ),
        400: OpenApiResponse(
            description='无效的角色或演示用户不存在'
        ),
        429: OpenApiResponse(
            description='请求过于频繁，请稍后重试'
        ),
    },
    tags=['认证']
)
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([LoginRateThrottle])
def demo_login(request):
    # 生产环境守卫
    if os.environ.get('DEMO_AUTH_ENABLED', 'false').lower() != 'true':
        return Response({'error': 'Demo login is disabled'}, status=status.HTTP_403_FORBIDDEN)

    serializer = DemoLoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    operation_id='users_counselors_list',
    summary='获取辅导员候选列表',
    description='返回当前学生学院的辅导员列表，用于学生选择辅导员',
    responses={
        200: {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'string'},
                    'name': {'type': 'string'},
                    'department': {'type': 'string'}
                }
            }
        },
        403: ErrorResponseSerializer,
    },
    tags=['用户']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_counselors(request):
    user = request.user

    if user.role != UserRole.STUDENT:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '只有学生可以获取辅导员列表'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # 研究生特殊处理：直接返回金玲老师
    if user.level == '研究生':
        counselors = User.objects.filter(
            user_id='20210066',
            role=UserRole.COUNSELOR,
            active=True
        ).values('user_id', 'name', 'department').order_by('name')
    else:
        # 其他学生：按学院匹配辅导员
        counselors = User.objects.filter(
            role=UserRole.COUNSELOR,
            department=user.department,
            active=True
        ).values('user_id', 'name', 'department').order_by('name')

    return Response(list(counselors))
