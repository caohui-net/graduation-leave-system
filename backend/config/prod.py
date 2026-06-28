"""
Production environment configuration
"""
from config.settings.base import *
from config.base import FEATURE_FLAGS

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'graduation_prod'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# 安全配置：根据环境变量决定是否强制HTTPS
# 内网部署（如172.17.x.x）使用HTTP时设置 FORCE_HTTPS=False
FORCE_HTTPS = os.getenv('FORCE_HTTPS', 'True').lower() == 'true'

SECURE_SSL_REDIRECT = FORCE_HTTPS
SESSION_COOKIE_SECURE = FORCE_HTTPS
CSRF_COOKIE_SECURE = FORCE_HTTPS
