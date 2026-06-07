"""学工系统用户API客户端"""
import hashlib
from typing import Literal


def generate_sign(
    app_secret: str,
    timestamp: str,
    rand_str: str,
    encryption_type: Literal['sha1', 'md5'] = 'sha1'
) -> str:
    """
    生成API签名

    签名规则：
    1. 将appSecret, timestamp, randStr三个参数值进行字典排序
    2. 拼接成字符串
    3. 进行sha1或md5加密

    Args:
        app_secret: AppSecret密钥
        timestamp: Unix时间戳（字符串）
        rand_str: 随机字符串
        encryption_type: 加密类型，'sha1'或'md5'，默认'sha1'

    Returns:
        签名字符串（十六进制小写）
    """
    if encryption_type not in ('sha1', 'md5'):
        raise ValueError(f"encryption_type must be 'sha1' or 'md5', got '{encryption_type}'")

    # 1. 字典排序
    params = [app_secret, timestamp, rand_str]
    params.sort()

    # 2. 拼接
    sign_str = ''.join(params)

    # 3. 加密
    if encryption_type == 'md5':
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    else:
        return hashlib.sha1(sign_str.encode('utf-8')).hexdigest()


class XGUserAPIConfig:
    """学工系统API配置"""

    def __init__(self):
        import os
        self.url = os.getenv('XG_USER_API_URL', '').strip()
        self.app_id = os.getenv('XG_USER_API_APP_ID', '').strip()
        self.app_key = os.getenv('XG_USER_API_APP_KEY', '').strip()
        self.app_secret = os.getenv('XG_USER_API_APP_SECRET', '').strip()
        self.tenant_code = os.getenv('XG_USER_API_TENANT_CODE', '').strip()
        encryption_type = os.getenv('XG_USER_API_ENCRYPTION_TYPE', 'sha1').strip().lower()

        if encryption_type not in ('sha1', 'md5'):
            raise ValueError(f"XG_USER_API_ENCRYPTION_TYPE must be 'sha1' or 'md5', got '{encryption_type}'")
        self.encryption_type = encryption_type

        self._validate()

    def _validate(self):
        """校验必填配置项"""
        if not self.url:
            raise ValueError("XG_USER_API_URL is required")
        if not self.app_key:
            raise ValueError("XG_USER_API_APP_KEY is required")
        if not self.app_secret:
            raise ValueError("XG_USER_API_APP_SECRET is required")
        if not self.tenant_code:
            raise ValueError("XG_USER_API_TENANT_CODE is required")

    def is_live_test_enabled(self) -> bool:
        """检查是否启用真实API测试"""
        import os
        return os.getenv('XG_RUN_LIVE_API_TEST', '0').strip() == '1'


class XGUserAPIClient:
    """学工系统用户API客户端"""

    def __init__(self, config: XGUserAPIConfig):
        self.config = config

    def build_headers(self, timestamp: str = None, rand_str: str = None) -> dict:
        """构造请求headers"""
        import time
        import random
        import string

        if timestamp is None:
            timestamp = str(int(time.time()))
        if rand_str is None:
            rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        sign = generate_sign(self.config.app_secret, timestamp, rand_str, self.config.encryption_type)

        return {
            'appKey': self.config.app_key,
            'timestamp': timestamp,
            'randStr': rand_str,
            'sign': sign,
            'encryptionType': self.config.encryption_type
        }

    def build_form_data(self, page: int = 1, page_num: int = 1) -> dict:
        """构造form-data"""
        return {
            'tenantCode': self.config.tenant_code,
            'page': str(page),
            'pageNum': str(page_num)
        }

    def fetch_users_page(self, page: int = 1, page_num: int = 1, timeout: int = 5, session=None) -> dict:
        """请求单页用户数据"""
        if session is None:
            import requests
            session = requests.Session()

        headers = self.build_headers()
        data = self.build_form_data(page, page_num)

        response = session.post(self.config.url, headers=headers, data=data, timeout=timeout)
        response.raise_for_status()

        result = response.json()

        # 协议层解析
        if 'code' not in result:
            raise ValueError("Response missing 'code' field")

        data = result.get('data')
        if data is None:
            raise ValueError("Response missing 'data' field")
        if 'data' not in data:
            raise ValueError("Response data missing 'data' (user list) field")
        users = data['data']
        if not isinstance(users, list):
            raise ValueError(f"Response data.data must be list, got {type(users).__name__}")

        return {
            'code': result.get('code'),
            'msg': result.get('msg', ''),
            'current_page': data.get('current_page'),
            'per_page': data.get('per_page'),
            'total': data.get('total'),
            'users': users
        }

    def fetch_all_users(self, page_size: int = 100, max_pages: int = None, timeout: int = 5, session=None) -> dict:
        """分页读取所有用户"""
        if page_size <= 0:
            raise ValueError(f"page_size must be positive, got {page_size}")
        if max_pages is not None and max_pages <= 0:
            raise ValueError(f"max_pages must be positive or None, got {max_pages}")

        if session is None:
            import requests
            session = requests.Session()

        all_users = []
        page = 1
        total = None
        prev_current_page = None

        while True:
            result = self.fetch_users_page(page=page, page_num=page_size, timeout=timeout, session=session)

            if result['code'] != 200:
                raise ValueError(f"Business error: code={result['code']}, msg={result['msg']}")

            users = result['users']
            if not isinstance(users, list):
                raise ValueError(f"users must be list, got {type(users).__name__}")

            all_users.extend(users)

            current_page = result['current_page']
            per_page = result['per_page']
            total = result['total']

            # 转换per_page为整数并校验
            if per_page is not None:
                per_page = int(per_page) if isinstance(per_page, str) else per_page
                if per_page <= 0:
                    raise ValueError(f"Invalid per_page: {per_page}, must be positive")

            # 校验current_page前进
            if current_page is not None:
                current_page_int = int(current_page) if isinstance(current_page, str) else current_page
                if prev_current_page is not None and current_page_int <= prev_current_page:
                    raise ValueError(f"Pagination not advancing: current_page={current_page_int}, previous={prev_current_page}")
                prev_current_page = current_page_int

            # 判断是否结束
            if max_pages and page >= max_pages:
                return {'users': all_users, 'total': total, 'pages_fetched': page, 'stopped_reason': 'max_pages'}

            if not users:
                return {'users': all_users, 'total': total, 'pages_fetched': page, 'stopped_reason': 'empty'}

            if total is not None and current_page is not None and per_page is not None:
                total_pages = (int(total) + per_page - 1) // per_page
                if int(current_page) >= total_pages:
                    return {'users': all_users, 'total': total, 'pages_fetched': page, 'stopped_reason': 'complete'}

            page += 1
