"""青橄榄SSO异常类"""


class SSOAPIError(Exception):
    """青橄榄API业务错误"""

    def __init__(self, code, message, response_data=None):
        self.code = code
        self.message = message
        self.response_data = response_data
        super().__init__(f"青橄榄API错误 [{code}]: {message}")


class SSOTokenExpiredError(SSOAPIError):
    """Token已过期或已使用"""
    pass


class SSOUserInfoError(SSOAPIError):
    """用户信息获取失败"""
    pass
