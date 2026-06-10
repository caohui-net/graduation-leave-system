import requests
from .auth import generate_request_params


class QingganlanAPIError(Exception):
    """青橄榄API错误"""
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
        super().__init__(f"[{code}] {msg}")


class QingganlanClient:
    """青橄榄平台API客户端"""

    MOBILE_BASE_URL = 'https://dev-lshospital.goliveplus.cn'
    ADMIN_BASE_URL = 'https://zhhq.huanghuai.edu.cn'

    def __init__(self, app_key, app_secret, env='prod'):
        self.app_key = app_key
        self.app_secret = app_secret
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def _make_request(self, method, endpoint, data=None, base_url=None):
        """统一请求方法"""
        if base_url is None:
            base_url = self.MOBILE_BASE_URL

        auth_params = generate_request_params(self.app_key, self.app_secret)
        self.session.headers.update(auth_params)

        url = base_url + endpoint
        try:
            if method == 'POST':
                resp = self.session.post(url, json=data, timeout=30)
            else:
                resp = self.session.get(url, params=data, timeout=30)

            resp.raise_for_status()
            result = resp.json()

            if result.get('code') != 200:
                raise QingganlanAPIError(result.get('code'), result.get('msg', '未知错误'))

            return result.get('data')

        except requests.RequestException as e:
            raise QingganlanAPIError(500, f"网络请求失败: {str(e)}")

    def get_user_code_by_token(self, tenant_code, appid, saas_wap_token):
        """Token换取user_code（移动端）"""
        endpoint = '/saas_api/open-api/user-center/user-code'
        data = {
            'tenantCode': tenant_code,
            'appid': appid,
            'saasWapToken': saas_wap_token
        }
        return self._make_request('POST', endpoint, data)

    def get_user_info(self, tenant_code, user_code, user_type):
        """获取用户详细信息（移动端）"""
        endpoint = '/saas_api/open-api/user-center/user-info'
        data = {
            'tenantCode': tenant_code,
            'userCode': user_code,
            'userType': user_type
        }
        return self._make_request('POST', endpoint, data)

    def verify_admin_user(self, token):
        """验证管理员用户（管理端）"""
        endpoint = '/open-api/auth/verify-user'
        self.session.headers.update({'Authorization': token})
        return self._make_request('POST', endpoint, base_url=self.ADMIN_BASE_URL)
