"""青橄榄SSO配置管理"""
from decouple import config


# 移动端配置
QGL_MOBILE_APP_KEY = config(
    'QGL_MOBILE_APP_KEY',
    default='abc0a32aa8dd94d1f765841abaafd8ba'
)
QGL_MOBILE_APP_SECRET = config(
    'QGL_MOBILE_APP_SECRET',
    default='b1d2efa9587446d80ce6388e0c0b25131b8dea59'
)
QGL_MOBILE_TENANT_CODE = config('QGL_MOBILE_TENANT_CODE', default='C10026')
QGL_MOBILE_APPID = config('QGL_MOBILE_APPID', default='c6qgh2')

# 管理端配置
QGL_ADMIN_APP_KEY = config('QGL_ADMIN_APP_KEY', default='APPKEY_TBD')
QGL_ADMIN_APP_SECRET = config('QGL_ADMIN_APP_SECRET', default='APPSECRET_TBD')

# 环境配置
QGL_ENV = config('QGL_ENV', default='prod')  # dev or prod
