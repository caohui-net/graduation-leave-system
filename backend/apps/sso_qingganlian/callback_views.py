"""SSO HTML Callback Views - 直接跳转业务页面"""
import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from .models import SSOUserMapping
from .client import QingganlanClient
from . import settings as sso_settings
from .exceptions import SSOAPIError, SSOTokenExpiredError

logger = logging.getLogger(__name__)


@csrf_exempt
def sso_callback(request):
    """
    SSO统一回调入口 - 直接跳转业务页面

    支持参数格式：
    - authorization + username（管理端）
    - authorization + user_id（移动端）
    - Authorization（大写）
    """
    # 兼容GET/POST
    params = request.GET if request.method == 'GET' else request.POST

    # 兼容多种参数名
    authorization = params.get('authorization') or params.get('Authorization')
    username = params.get('username') or params.get('user_id')
    real_name = params.get('real_name', '')
    identity_name = params.get('identity_name', '管理员')

    # 容错：去除"bearer "前缀（SAAS平台可能错误添加）
    if authorization and authorization.lower().startswith('bearer '):
        authorization = authorization[7:].strip()

    # 容错：如果没有username，调用青橄榄API获取user_code
    if authorization and not username:
        try:
            client = QingganlanClient(
                app_key=sso_settings.MOBILE_APP_KEY,
                app_secret=sso_settings.MOBILE_APP_SECRET,
                env='prod',
                api_type='mobile'
            )
            # 使用移动端API获取user_code
            token_response = client.get_user_code_by_token(
                tenant_code=sso_settings.MOBILE_TENANT_CODE,
                appid=sso_settings.MOBILE_APPID,
                saas_wap_token=authorization
            )
            username = token_response.get('data', {}).get('user_code')
            if username:
                logger.info(f"Extracted user_code from API: {username}")
            else:
                logger.error(f"API returned no user_code: {token_response}")
        except (SSOAPIError, SSOTokenExpiredError) as e:
            logger.error(f"Failed to get user_code from API: {e.code} - {e.message}")
        except Exception as e:
            logger.error(f"Failed to call SSO API: {str(e)}")

    if not authorization or not username:
        logger.error(f"SSO callback missing params: {dict(params)}")
        return HttpResponse("""
            <!DOCTYPE html>
            <html>
            <head><meta charset="UTF-8"><title>登录失败</title></head>
            <body style="text-align:center; padding-top:100px; font-family: Arial;">
                <h2>缺少认证信息</h2>
                <p>未找到authorization或username参数</p>
                <button onclick="window.location.href='http://218.75.196.218:7788/'">返回首页</button>
            </body>
            </html>
        """, status=400)

    try:
        # SSO仅做身份验证，不创建用户
        # 用户必须预先存在于本地数据库
        try:
            user = User.objects.get(user_id=username, active=True)
            logger.info(f"SSO login existing user: {username}, role={user.role}")
        except User.DoesNotExist:
            logger.warning(f"SSO rejected unknown user: {username}, identity={identity_name}")
            return HttpResponse("""
                <!DOCTYPE html>
                <html>
                <head><meta charset="UTF-8"><title>登录失败</title></head>
                <body style="text-align:center; padding-top:100px; font-family: Arial;">
                    <h2>用户不存在</h2>
                    <p>您的账号未在系统中注册，请联系管理员</p>
                    <button onclick="window.location.href='http://218.75.196.218:7788/'">返回首页</button>
                </body>
                </html>
            """, status=403)

        # 更新SSO映射（使用用户真实角色）
        SSOUserMapping.objects.update_or_create(
            user_code=username,
            defaults={
                'user': user,
                'tenant_code': 'default',
                'user_type': user.role,  # 使用数据库中的真实角色
                'real_name': user.name,  # 使用数据库中的真实姓名
                'identity_name': identity_name,
                'role_name': identity_name,
                'last_login_at': timezone.now()
            }
        )

        # 生成JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        logger.info(f"SSO callback success: user={username}")

        # 通过URL参数传递token和user_info（避免localStorage跨域问题）
        import urllib.parse
        import json

        user_info = {
            'user_id': user.user_id,
            'name': user.name,
            'role': user.role,
            'building': user.building or '',
            'room_number': user.room_number or ''
        }

        redirect_url = (
            f'http://218.75.196.218:7788/sso-receiver.html'
            f'?token={urllib.parse.quote(access_token)}'
            f'&user_info={urllib.parse.quote(json.dumps(user_info))}'
        )

        return HttpResponse(f"""
            <!DOCTYPE html>
            <html>
            <head><meta charset="UTF-8"><title>登录中</title></head>
            <body>
                <script>
                    window.location.href = '{redirect_url}';
                </script>
                <p style="text-align:center; padding-top:100px;">登录成功，正在跳转...</p>
            </body>
            </html>
        """)

    except Exception as e:
        logger.exception(f"SSO callback failed: {str(e)}")
        return HttpResponse(f"""
            <!DOCTYPE html>
            <html>
            <head><meta charset="UTF-8"><title>登录失败</title></head>
            <body style="text-align:center; padding-top:100px; font-family: Arial;">
                <h2>登录失败</h2>
                <p>{str(e)}</p>
                <button onclick="window.location.href='http://218.75.196.218:7788/'">返回首页</button>
            </body>
            </html>
        """, status=500)
