"""青橄榄SSO配置管理"""
from decouple import config


# 移动端配置
MOBILE_APP_KEY = config(
    'QGL_MOBILE_APP_KEY',
    default='cb6f276a42042179e90cd79c4126e075'
)
MOBILE_APP_SECRET = config(
    'QGL_MOBILE_APP_SECRET',
    default='da02720febcf47071ee5db78c2b068ec'
)
MOBILE_TENANT_CODE = config('QGL_MOBILE_TENANT_CODE', default='S10405')
MOBILE_APPID = config('QGL_MOBILE_APPID', default='8uonta')

# 管理端配置
ADMIN_APP_KEY = config('QGL_ADMIN_APP_KEY', default='APPKEY_TBD')
ADMIN_APP_SECRET = config('QGL_ADMIN_APP_SECRET', default='APPSECRET_TBD')

# 环境配置
ENV = config('QGL_ENV', default='prod')  # dev or prod

# 安全配置
# admin_login是否验证authorization token（默认开启，对接失败时可临时关闭）
VERIFY_ADMIN_TOKEN = config('QGL_VERIFY_ADMIN_TOKEN', default=True, cast=bool)
