import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import transaction
from django.shortcuts import redirect
from django.http import HttpResponse
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
def mobile_saas_login(request):
    """
    移动端SAAS登录（saas_wap_token流程）

    流程：
    1. 接收saas_wap_token + tenant_code
    2. 调用青橄榄API换取user_code
    3. 调用青橄榄API获取用户信息
    4. 创建本地User
    5. 返回JWT token
    """
    saas_wap_token = request.data.get('saas_wap_token')
    tenant_code = request.data.get('tenant_code', 'S10405')

    if not saas_wap_token:
        return Response({'error': '缺少saas_wap_token参数'},
                       status=status.HTTP_400_BAD_REQUEST)

    logger.info(f"Mobile SAAS login attempt: token={saas_wap_token[:20]}...")

    try:
        client = QingganlanClient(
            app_key=sso_settings.MOBILE_APP_KEY,
            app_secret=sso_settings.MOBILE_APP_SECRET,
            env='prod',
            api_type='mobile'
        )

        # 1. 换取user_code
        token_response = client.get_user_code_by_token(
            tenant_code=tenant_code,
            appid=sso_settings.MOBILE_APPID,
            saas_wap_token=saas_wap_token
        )
        user_code = token_response.get('data', {}).get('user_code')
        user_type = token_response.get('data', {}).get('user_type', 'weChat')

        if not user_code:
            raise Exception('未能获取user_code')

        # 2. 获取用户信息
        user_info_response = client.get_user_info(tenant_code, user_code, user_type)
        user_info = user_info_response.get('data', {})

        real_name = user_info.get('real_name', '')
        identity_name = user_info.get('identity_name', '学生')
        phone = user_info.get('phone', '')
        user_id_str = user_info.get('number', user_code)

        # 3. 创建用户
        with transaction.atomic():
            user, created = User.objects.select_for_update().get_or_create(
                user_id=user_id_str,
                defaults={
                    'name': real_name or user_id_str,
                    'role': 'student' if identity_name == '学生' else 'teacher',
                    'is_staff': False,
                    'active': True
                }
            )

        # 4. 确定角色
        if identity_name == '学生':
            sso_user_type = 'mobile_student'
            role = 'student'
        elif identity_name in ['教师', '教职工']:
            sso_user_type = 'mobile_teacher'
            role = 'teacher'
        else:
            sso_user_type = 'mobile_student'
            role = 'student'

        # 5. 更新SSOUserMapping
        SSOUserMapping.objects.update_or_create(
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

        # 6. 生成JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response_data = {
            'token': access_token,
            'user': {
                'id': user.user_id,
                'username': user.user_id,
                'real_name': real_name,
                'role': role,
                'phone': phone,
                'building': user.building,
                'room_number': user.room_number
            }
        }

        logger.info(f"Mobile SAAS login success: user={user.user_id}, role={role}")
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"Mobile SAAS login failed: {str(e)}")
        return Response({'error': f'登录失败: {str(e)}'},
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def mobile_login(request):
    """
    移动端登录端点（简化流程）

    安全假设：此接口信任青橄榄平台已完成用户认证，仅接收回调参数。
    生产部署建议：配置nginx/防火墙限制只允许青橄榄IP访问此接口。

    流程：
    1. 验证请求参数（authorization + user_id）
    2. 直接使用user_id创建本地User（青橄榄移动端无token验证API）
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
                'phone': phone,
                'building': user.building,
                'room_number': user.room_number
            }
        }

        logger.info(f"Mobile login success: user={user.user_id}, role={role}")
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"Mobile login failed: unexpected error, user_id={user_id}")
        return Response({'error': f'登录失败: {str(e)}'},
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', 'GET'])
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
    # 1. 验证请求参数 - 兼容GET/POST和大小写
    if request.method == 'GET':
        authorization = request.GET.get('authorization') or request.GET.get('Authorization')
        username = request.GET.get('username') or request.GET.get('user_id')
    else:
        authorization = request.data.get('authorization') or request.data.get('Authorization')
        username = request.data.get('username') or request.data.get('user_id')

    if not authorization or not username:
        return Response({'error': '缺少authorization或username参数'},
                       status=status.HTTP_400_BAD_REQUEST)

    logger.info(f"Admin login attempt: username={username}")

    try:
        # 2. 可选的authorization token验证（可通过QGL_VERIFY_ADMIN_TOKEN环境变量控制）
        if sso_settings.VERIFY_ADMIN_TOKEN:
            client = QingganlanClient(
                app_key=sso_settings.ADMIN_APP_KEY,
                app_secret=sso_settings.ADMIN_APP_SECRET,
                env='prod',
                api_type='admin'
            )

            try:
                verify_result = client.verify_admin_user(authorization)
                logger.info(f"Admin token verified: {verify_result}")
            except SSOAPIError as e:
                logger.error(f"Admin token verification failed: {e.code} - {e.message}")
                return Response({'error': f'认证失败: {e.message}'},
                              status=status.HTTP_401_UNAUTHORIZED)
        else:
            logger.warning(f"Admin token verification SKIPPED (QGL_VERIFY_ADMIN_TOKEN=False)")

        # 3. 使用username作为user_code
        user_code = username
        name = username
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
                'phone': phone,
                'building': user.building,
                'room_number': user.room_number
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
