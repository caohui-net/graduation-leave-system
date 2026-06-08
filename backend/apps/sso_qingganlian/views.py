from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .client import QingganlanClient
from .models import SSOUserMapping
from .serializers import MobileLoginRequestSerializer, MobileLoginResponseSerializer
from .exceptions import SSOAPIError, SSOTokenExpiredError, SSOUserInfoError


@api_view(['POST'])
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

    try:
        # 2. 初始化客户端并获取user_code
        # TODO: 从配置获取app_key和app_secret
        client = QingganlanClient(
            app_key='abc0a32aa8dd94d1f765841abaafd8ba',
            app_secret='b1d2efa9587446d80ce6388e0c0b25131b8dea59',
            env='prod',
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

        user, created = User.objects.get_or_create(
            username=number,
            defaults={
                'first_name': real_name[:30],  # Django限制
                'is_active': True
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
                'id': user.id,
                'username': user.username,
                'real_name': real_name,
                'role': role,
                'phone': phone
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except SSOTokenExpiredError as e:
        return Response({'error': 'TOKEN已过期，请重新登录'},
                       status=status.HTTP_401_UNAUTHORIZED)
    except SSOUserInfoError as e:
        return Response({'error': '用户信息获取失败，请重新登录'},
                       status=status.HTTP_401_UNAUTHORIZED)
    except SSOAPIError as e:
        return Response({'error': f'登录失败: {e.message}'},
                       status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'登录失败: {str(e)}'},
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)
