from typing import Dict, Any
from .base import BaseSSOProvider
from ..client import QingganlanClient
from ..exceptions import SSOAPIError
from .. import settings as sso_settings


class QingganlanProvider(BaseSSOProvider):
    """青橄榄平台SSO提供商"""

    def __init__(self, api_type='mobile'):
        """
        初始化青橄榄提供商

        Args:
            api_type: API类型 ('mobile' 或 'admin')
        """
        self.api_type = api_type

        if api_type == 'mobile':
            self.client = QingganlanClient(
                app_key=sso_settings.QGL_MOBILE_APP_KEY,
                app_secret=sso_settings.QGL_MOBILE_APP_SECRET,
                env=sso_settings.QGL_ENV,
                api_type='mobile'
            )
        else:
            self.client = QingganlanClient(
                app_key=sso_settings.QGL_ADMIN_APP_KEY,
                app_secret=sso_settings.QGL_ADMIN_APP_SECRET,
                env=sso_settings.QGL_ENV,
                api_type='admin'
            )

    def authenticate(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行青橄榄SSO认证

        Args:
            credentials: 认证凭证
                mobile端: {'tenant_code', 'appid', 'saas_wap_token'}
                admin端: {'authorization'}

        Returns:
            标准化用户信息
        """
        if self.api_type == 'mobile':
            return self._authenticate_mobile(credentials)
        else:
            return self._authenticate_admin(credentials)

    def _authenticate_mobile(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """移动端认证"""
        tenant_code = credentials['tenant_code']
        appid = credentials['appid']
        saas_wap_token = credentials['saas_wap_token']

        # Step 1: token → user_code
        user_code_result = self.client.get_user_code_by_token(
            tenant_code, appid, saas_wap_token
        )
        user_code = user_code_result['data']['user_code']
        user_type = user_code_result['data']['user_type']

        # Step 2: user_code → user_info
        user_info_result = self.client.get_user_info(
            tenant_code, user_code, user_type
        )
        user_data = user_info_result['data']

        # Step 3: 标准化输出
        return {
            'external_uid': user_code,
            'external_username': user_data.get('number', ''),
            'real_name': user_data.get('real_name', ''),
            'phone': user_data.get('phone', ''),
            'email': user_data.get('email', ''),
            'provider_data': {
                'tenant_code': tenant_code,
                'user_type': user_type,
                'identity_name': user_data.get('identity_name', ''),
                'role_name': user_data.get('role_name', '')
            }
        }

    def _authenticate_admin(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """管理端认证"""
        authorization = credentials['authorization']

        # 调用管理端验证API
        result = self.client.verify_admin_user(authorization)
        user_data = result['data']

        return {
            'external_uid': user_data.get('username', ''),
            'external_username': user_data.get('username', ''),
            'real_name': user_data.get('name', ''),
            'phone': user_data.get('phone', ''),
            'email': user_data.get('email', ''),
            'provider_data': {
                'tenant_code': user_data.get('tenant_code', '')
            }
        }

    @property
    def provider_name(self) -> str:
        return 'qingganlian'
