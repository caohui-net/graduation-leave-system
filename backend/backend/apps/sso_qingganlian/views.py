from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
import jwt
import datetime

from .client import QingganlanClient, QingganlanAPIError
from .serializers import MobileLoginSerializer, AdminLoginSerializer
from .models import SSOUserMapping

User = get_user_model()


def generate_jwt_token(user):
    """生成本地JWT token"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def get_or_create_user_from_qgl(qgl_data, user_type):
    """从青橄榄数据创建或获取本地用户"""
    if user_type in ['mobile_student', 'mobile_teacher']:
        username = qgl_data.get('number') or qgl_data.get('userCode')
        real_name = qgl_data.get('realName', '')
        identity = qgl_data.get('identityName', '')
        user_code = qgl_data.get('userCode')
        mapping_key = {'user_code': user_code}
    else:  # admin
        username = qgl_data.get('username')
        real_name = qgl_data.get('name', '')
        identity = 'admin'
        mapping_key = {'username': username}

    # 查找或创建映射
    try:
        mapping = SSOUserMapping.objects.get(**mapping_key)
        user = mapping.user
        mapping.last_login_at = timezone.now()
        mapping.save()
    except SSOUserMapping.DoesNotExist:
        # 创建本地用户
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': real_name[:30] if real_name else username,
                'is_active': True,
                'is_staff': user_type == 'admin'
            }
        )
        # 创建映射
        mapping = SSOUserMapping.objects.create(
            user=user,
            tenant_code=qgl_data.get('tenantCode', ''),
            user_code=qgl_data.get('userCode') if user_type != 'admin' else None,
            username=qgl_data.get('username') if user_type == 'admin' else None,
            user_type=user_type,
            real_name=real_name,
            phone=qgl_data.get('phone', ''),
            identity_name=identity,
            role_name=qgl_data.get('roleName', ''),
            last_login_at=timezone.now()
        )

    return user, mapping


@api_view(['POST'])
@permission_classes([AllowAny])
def mobile_login(request):
    """移动端登录"""
    serializer = MobileLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    client = QingganlanClient(
        app_key=settings.QGL_MOBILE_APP_KEY,
        app_secret=settings.QGL_MOBILE_APP_SECRET
    )

    try:
        # 1. Token换取user_code
        user_code_data = client.get_user_code_by_token(
            data['tenant_code'],
            data['appid'],
            data['saas_wap_token']
        )
        user_code = user_code_data.get('userCode')
        user_type_code = user_code_data.get('userType', '1')

        # 2. 获取用户详细信息
        user_info = client.get_user_info(
            data['tenant_code'],
            user_code,
            user_type_code
        )

        # 3. 确定用户类型
        identity = user_info.get('identityName', '')
        if '学生' in identity:
            ut = 'mobile_student'
        elif '教师' in identity:
            ut = 'mobile_teacher'
        else:
            ut = 'mobile_student'

        # 4. 创建/获取本地用户
        user, mapping = get_or_create_user_from_qgl(user_info, ut)

        # 5. 生成JWT
        token = generate_jwt_token(user)

        return Response({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'real_name': mapping.real_name,
                'role': ut
            }
        })

    except QingganlanAPIError as e:
        if e.code == 88890006:
            return Response(
                {'error': '登录凭证已过期，请重新登录'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif e.code == 88890007:
            return Response(
                {'error': '用户信息获取失败，请重新登录'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {'error': f'登录失败: {e.msg}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'登录服务异常: {str(e)}'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """管理端登录"""
    serializer = AdminLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    client = QingganlanClient(
        app_key=settings.QGL_ADMIN_APP_KEY,
        app_secret=settings.QGL_ADMIN_APP_SECRET
    )

    try:
        # 1. 验证管理员用户
        admin_info = client.verify_admin_user(data['authorization'])

        # 2. 创建/获取本地用户
        user, mapping = get_or_create_user_from_qgl(admin_info, 'admin')

        # 3. 生成JWT
        token = generate_jwt_token(user)

        return Response({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'real_name': mapping.real_name,
                'role': 'admin'
            }
        })

    except QingganlanAPIError as e:
        return Response(
            {'error': f'管理员验证失败: {e.msg}'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        return Response(
            {'error': f'登录服务异常: {str(e)}'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
