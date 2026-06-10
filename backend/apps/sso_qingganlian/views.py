import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from .client import QingganlanClient
from .models import SSOUserMapping
from .serializers import (
    MobileLoginRequestSerializer,
    MobileLoginResponseSerializer,
    AdminLoginRequestSerializer,
    AdminLoginResponseSerializer
)
from .exceptions import SSOAPIError, SSOTokenExpiredError, SSOUserInfoError
from . import settings as sso_settings

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def mobile_login(request):
    """
    移动端登录端点（简化流程）

    流程：
    1. 验证请求参数（authorization + user_id）
    2. 直接使用user_id创建本地User（无需API调用）
    3. 生成JWT token
    4. 返回token和用户信息
    """
    # 1. 验证请求参数
    authorization = request.data.get('authorization')
    user_id = request.data.get('user_id')
    real_name = request.data.get('real_name', '')
    identity_name = request.data.get('identity_name', '学生')

    if not authorization or not user_id:
        return Response({'error': '缺少authorization或user_id参数'},
                       status=status.HTTP_400_BAD_REQUEST)

    logger.info(f"Mobile login attempt: user_id={user_id}")

    try:
        # 2. 直接使用user_id作为标识（青橄榄新流程）
        tenant_code = 'S10405'
        phone = ''

        # 3. 创建用户和映射（事务保护防竞态）
        with transaction.atomic():
            user, created = User.objects.select_for_update().get_or_create(
                user_id=user_id,
                defaults={
                    'name': real_name or user_id,
                    'role': 'student' if identity_name == '学生' else 'teacher',
                    'is_staff': False,
                    'active': True
                }
            )

        # 4. 确定用户类型
        if identity_name == '学生':
            sso_user_type = 'mobile_student'
            role = 'student'
        elif identity_name in ['教师', '教职工']:
            sso_user_type = 'mobile_teacher'
            role = 'teacher'
        else:
            sso_user_type = 'mobile_student'
            role = 'student'

        # 5. 创建或更新SSOUserMapping
        mapping, _ = SSOUserMapping.objects.update_or_create(
            user_code=user_id,
            defaults={
                'user': user,
                'tenant_code': tenant_code,
                'user_type': sso_user_type,
                'real_name': real_name or user_id,
                'phone': phone,
                'identity_name': identity_name,
                'role_name': identity_name,
                'last_login_at': timezone.now()
            }
        )

        # 6. 生成JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # 7. 返回响应
        response_data = {
            'token': access_token,
            'user': {
                'id': user.user_id,
                'username': user.user_id,
                'real_name': real_name or user_id,
                'role': role,
                'phone': phone
            }
        }

        logger.info(f"Mobile login success: user={user.user_id}, role={role}")
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"Mobile login failed: unexpected error, user_id={user_id}")
        return Response({'error': f'登录失败: {str(e)}'},
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """
    管理端登录端点

    流程：
    1. 验证请求参数（authorization token）
    2. 调用青橄榄API: verify-user
    3. 查询/创建本地管理员User
    4. 查询/创建SSOUserMapping
    5. 生成JWT token
    6. 返回token和用户信息
    """
    # 1. 验证请求参数
    authorization = request.data.get('authorization')
    username = request.data.get('username')

    if not authorization or not username:
        return Response({'error': '缺少authorization或username参数'},
                       status=status.HTTP_400_BAD_REQUEST)

    logger.info(f"Admin login attempt: username={username}")

    try:
        # 2. 直接使用username作为user_code（青橄榄新流程）
        user_code = username
        name = username  # 默认使用username，后续可通过其他接口补充真实姓名
        tenant_code = 'default'
        role_name = '管理员'
        phone = ''

        # 3. 创建用户和映射（事务保护防竞态）
        with transaction.atomic():
            user, created = User.objects.select_for_update().get_or_create(
                user_id=user_code,
                defaults={
                    'name': name,
                    'role': 'admin',
                    'is_staff': True,
                    'active': True
                }
            )

            # 4. 创建或更新SSOUserMapping
            mapping, _ = SSOUserMapping.objects.update_or_create(
                user_code=user_code,
                defaults={
                    'user': user,
                    'tenant_code': tenant_code,
                    'user_type': 'admin',
                    'real_name': name,
                    'phone': phone,
                    'identity_name': '管理员',
                    'role_name': role_name,
                    'last_login_at': timezone.now()
                }
            )

        # 6. 生成JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # 7. 返回响应
        response_data = {
            'token': access_token,
            'user': {
                'id': user.user_id,
                'username': user.user_id,
                'real_name': name,
                'role': 'admin',
                'phone': phone
            }
        }

        logger.info(f"Admin login success: user={user.user_id}")
        return Response(response_data, status=status.HTTP_200_OK)

    except SSOAPIError as e:
        logger.error(f"Admin login failed: SSO API error {e.code}")
        return Response({'error': f'登录失败: {e.message}'},
                       status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception("Admin login failed: unexpected error")
        return Response({'error': f'登录失败: {str(e)}'},
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)
