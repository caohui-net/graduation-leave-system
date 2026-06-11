"""SSO HTML Callback Views - 直接跳转业务页面"""
import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from .models import SSOUserMapping

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

    if not authorization or not username:
        logger.error(f"SSO callback missing params: {dict(params)}")
        return HttpResponse("""
            <!DOCTYPE html>
            <html>
            <head><meta charset="UTF-8"><title>登录失败</title></head>
            <body style="text-align:center; padding-top:100px; font-family: Arial;">
                <h2>缺少认证信息</h2>
                <p>未找到authorization或username参数</p>
                <button onclick="window.location.href='/'">返回首页</button>
            </body>
            </html>
        """, status=400)

    try:
        # 根据identity_name确定角色
        if identity_name == '学生':
            role = 'student'
            is_staff = False
        elif identity_name in ['教师', '教职工']:
            role = 'teacher'
            is_staff = False
        else:  # 管理员或其他
            role = 'admin'
            is_staff = True

        # 创建/获取用户
        with transaction.atomic():
            user, created = User.objects.select_for_update().get_or_create(
                user_id=username,
                defaults={
                    'name': real_name or username,
                    'role': role,
                    'is_staff': is_staff,
                    'active': True
                }
            )

        # 更新SSO映射
        SSOUserMapping.objects.update_or_create(
            user_code=username,
            defaults={
                'user': user,
                'tenant_code': 'default',
                'user_type': role,
                'real_name': real_name or username,
                'identity_name': identity_name,
                'role_name': identity_name,
                'last_login_at': timezone.now()
            }
        )

        # 生成JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        logger.info(f"SSO callback success: user={username}")

        # 直接跳转到业务页面（设置token到localStorage）
        return HttpResponse(f"""
            <!DOCTYPE html>
            <html>
            <head><meta charset="UTF-8"><title>登录中</title></head>
            <body>
                <script>
                    // 保存token到localStorage
                    localStorage.setItem('auth_token', '{access_token}');
                    localStorage.setItem('user_info', JSON.stringify({{
                        'user_id': '{user.user_id}',
                        'name': '{user.name}',
                        'role': '{user.role}'
                    }}));
                    // 直接跳转到业务页面
                    window.location.href = '/';
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
                <button onclick="window.location.href='/'">返回首页</button>
            </body>
            </html>
        """, status=500)
