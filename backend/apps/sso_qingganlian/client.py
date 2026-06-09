import requests
from django.conf import settings
from .auth import generate_request_params
from .exceptions import SSOAPIError, SSOTokenExpiredError, SSOUserInfoError


class QingganlanClient:
    """青橄榄平台API客户端"""

    MOBILE_API_BASE = {
        'dev': 'https://dev-lshospital.goliveplus.cn',
        'prod': 'https://dev-lshospital.goliveplus.cn'  # TODO: 确认正式环境地址
    }

    ADMIN_API_BASE = {
        'dev': 'https://dev-logisticsplatform.goliveplus.cn',
        'prod': 'https://zhhq.huanghuai.edu.cn'
    }

    def __init__(self, app_key, app_secret, env='prod', api_type='mobile'):
        """
        初始化客户端

        Args:
            app_key: 应用ID
            app_secret: 应用密钥
            env: 环境 (dev/prod)
            api_type: API类型 (mobile/admin)
        """
        self.app_key = app_key
        self.app_secret = app_secret
        self.env = env
        self.api_type = api_type

        if api_type == 'mobile':
            self.base_url = self.MOBILE_API_BASE[env]
        else:
            self.base_url = self.ADMIN_API_BASE[env]

        self.session = requests.Session()

    def _make_request(self, method, endpoint, data=None, encryption_type='sha1'):
        """
        发起HTTP请求

        Args:
            method: HTTP方法
            endpoint: API端点
            data: 请求数据
            encryption_type: 加密类型

        Returns:
            响应JSON

        Raises:
            SSOAPIError: API业务错误
            SSOTokenExpiredError: Token过期
            SSOUserInfoError: 用户信息获取失败
        """
        url = f"{self.base_url}{endpoint}"
        headers = generate_request_params(self.app_key, self.app_secret, encryption_type)

        try:
            if method.upper() == 'POST':
                response = self.session.post(url, headers=headers, json=data, timeout=30)
            else:
                response = self.session.get(url, headers=headers, params=data, timeout=30)

            response.raise_for_status()
            result = response.json()

            # 检查业务错误码
            code = result.get('code')
            if code != 200:
                msg = result.get('msg', '未知错误')

                # 根据错误码抛出特定异常
                if code == 88890006:
                    raise SSOTokenExpiredError(code, 'TOKEN已使用或已过期', result)
                elif code == 88890007:
                    raise SSOUserInfoError(code, '用户信息获取失败', result)
                else:
                    raise SSOAPIError(code, msg, result)

            return result

        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")

    def get_user_code_by_token(self, tenant_code, appid, saas_wap_token):
        """
        Token换取user_code（移动端）

        Args:
            tenant_code: 租户Code
            appid: 产品标识
            saas_wap_token: 用户登录token

        Returns:
            dict: 包含user_code等信息
        """
        endpoint = '/saas_api/open-api/user-center/user-code-by-token'
        data = {
            'tenant_code': tenant_code,
            'appid': appid,
            'saas_wap_token': saas_wap_token
        }
        return self._make_request('POST', endpoint, data)

    def get_user_info(self, tenant_code, user_code, user_type):
        """
        获取用户详细信息（移动端）

        Args:
            tenant_code: 租户Code
            user_code: 用户Code
            user_type: 用户类型

        Returns:
            dict: 用户详细信息
        """
        endpoint = '/saas_api/open-api/user-center/user-info'
        data = {
            'tenantCode': tenant_code,
            'userCode': user_code,
            'userType': user_type
        }
        return self._make_request('POST', endpoint, data)

    def verify_admin_user(self, token):
        """
        验证管理员用户（管理端）

        Args:
            token: Authorization token

        Returns:
            dict: 管理员用户信息
        """
        endpoint = '/api/open-api/auth/verify-user'
        data = {
            'token': token
        }
        return self._make_request('POST', endpoint, data)
