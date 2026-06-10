import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
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
@permission_classes([])
def mobile_login(request):
    """
    移动端登录端点

    流程：
    1. 验证请求参数
    2. 调用青橄榄API: token → user_code
    3. 调用青橄榄API: user_code → 用户信息
    4. 查询/创建SSOUserMapping
    5. 查询/创建本地User
    6. 生成JWT token
    7. 返回token和用户信息
    """
    # 1. 验证请求参数
    serializer = MobileLoginRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': '参数错误', 'details': serializer.errors},
                       status=status.HTTP_400_BAD_REQUEST)

    tenant_code = serializer.validated_data['tenant_code']
    appid = serializer.validated_data['appid']
    saas_wap_token = serializer.validated_data['saas_wap_token']

    logger.info(f"Mobile login attempt: tenant={tenant_code}, appid={appid}")

    try:
        # 2. 初始化客户端并获取user_code
        client = QingganlanClient(
            app_key=sso_settings.QGL_MOBILE_APP_KEY,
            app_secret=sso_settings.QGL_MOBILE_APP_SECRET,
            env=sso_settings.QGL_ENV,
            api_type='mobile'
        )

        user_code_result = client.get_user_code_by_token(tenant_code, appid, saas_wap_token)
        user_code = user_code_result['data']['user_code']
        user_type = user_code_result['data']['user_type']

        # 3. 获取用户详细信息
        user_info_result = client.get_user_info(tenant_code, user_code, user_type)
        user_data = user_info_result['data']

        # 4. 查询或创建本地User（通过学号/工号匹配）
        number = user_data.get('number', '')
        real_name = user_data.get('real_name', '')
        identity_name = user_data.get('identity_name', '')
        phone = user_data.get('phone', '')

        # 安全检查：拒绝空标识符
        if not number:
            logger.error(f"Mobile login failed: missing user number, tenant={tenant_code}")
            return Response({'error': '用户标识缺失，无法登录'},
                           status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            user_id=number,
            defaults={
                'name': real_name,
                'role': 'student' if identity_name == '学生' else 'counselor',
                'is_staff': False,
                'active': True
            }
        )

        # 5. 确定用户类型
        if identity_name == '学生':
            sso_user_type = 'mobile_student'
            role = 'student'
        elif identity_name in ['教师', '教职工']:
            sso_user_type = 'mobile_teacher'
            role = 'teacher'
        else:
            sso_user_type = 'mobile_student'
            role = 'student'

        # 6. 创建或更新SSOUserMapping
        mapping, _ = SSOUserMapping.objects.update_or_create(
            user_code=user_code,
            defaults={
                'user': user,
                'tenant_code': tenant_code,
                'user_type': sso_user_type,
                'real_name': real_name,
                'phone': phone,
                'identity_name': identity_name,
                'role_name': identity_name,
                'last_login_at': timezone.now()
            }
        )

        # 7. 生成JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # 8. 返回响应
        response_data = {
            'token': access_token,
            'user': {
                'id': user.user_id,
                'username': user.user_id,
                'real_name': real_name,
                'role': role,
                'phone': phone
            }
        }

        logger.info(f"Mobile login success: user={user.username}, role={role}")
        return Response(response_data, status=status.HTTP_200_OK)

    except SSOTokenExpiredError as e:
        logger.warning(f"Mobile login failed: token expired, tenant={tenant_code}")
        return Response({'error': 'TOKEN已过期，请重新登录'},
                       status=status.HTTP_401_UNAUTHORIZED)
    except SSOUserInfoError as e:
        logger.warning(f"Mobile login failed: user info error, tenant={tenant_code}")
        return Response({'error': '用户信息获取失败，请重新登录'},
                       status=status.HTTP_401_UNAUTHORIZED)
    except SSOAPIError as e:
        logger.error(f"Mobile login failed: SSO API error {e.code}, tenant={tenant_code}")
        return Response({'error': f'登录失败: {e.message}'},
                       status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception(f"Mobile login failed: unexpected error, tenant={tenant_code}")
        return Response({'error': f'登录失败: {str(e)}'},
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([])
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
    serializer = AdminLoginRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': '参数错误', 'details': serializer.errors},
                       status=status.HTTP_400_BAD_REQUEST)

    authorization = serializer.validated_data['authorization']

    logger.info("Admin login attempt")

    try:
        # 2. 初始化客户端并验证管理员用户
        client = QingganlanClient(
            app_key=sso_settings.QGL_ADMIN_APP_KEY,
            app_secret=sso_settings.QGL_ADMIN_APP_SECRET,
            env=sso_settings.QGL_ENV,
            api_type='admin'
        )

        admin_result = client.verify_admin_user(authorization)
        admin_data = admin_result['data']

        # 3. 获取管理员信息
        user_code = admin_data.get('user_code', '')
        name = admin_data.get('name', '')
        tenant_code = admin_data.get('tenant_code', '')
        role_name = admin_data.get('role_name', '')
        phone = admin_data.get('phone', '')

        # 安全检查：拒绝空标识符
        if not user_code:
            logger.error("Admin login failed: missing user_code")
            return Response({'error': '管理员标识缺失，无法登录'},
                           status=status.HTTP_400_BAD_REQUEST)

        # 4. 查询或创建本地管理员User
        user, created = User.objects.get_or_create(
            user_id=user_code,
            defaults={
                'name': name,
                'role': 'admin',
                'is_staff': True,
                'active': True
            }
        )

        # 5. 创建或更新SSOUserMapping
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
