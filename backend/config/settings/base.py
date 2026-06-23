"""
Django settings for graduation leave system project.
Base settings shared across all environments.
"""
from pathlib import Path
from decouple import config
from datetime import timedelta
import logging

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')

# 安全检查：SECRET_KEY使用默认值时警告
if SECRET_KEY == 'django-insecure-dev-key-change-in-production':
    logging.warning(
        "⚠️  [SECURITY] SECRET_KEY使用默认值！"
        "生产环境必须设置环境变量 SECRET_KEY。"
        "当前配置存在JWT签名被预测的风险。"
    )

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Frontend URL for root redirect
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:8081/')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',

    # Local apps
    'apps.users',
    'apps.applications',
    'apps.approvals',
    'apps.attachments',
    'apps.notifications',
    'apps.sso_qingganlian',
    'apps.healthcheck',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='graduation_leave'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='postgres'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',
        'login': '5/minute',
    }
}

# API Documentation
SPECTACULAR_SETTINGS = {
    'TITLE': '毕业生离校申请审批系统 API',
    'DESCRIPTION': '毕业生离校申请审批系统后端API文档',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'user_id',
    'USER_ID_CLAIM': 'user_id',
}

# CORS Settings
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000,http://127.0.0.1:7788,http://172.17.12.199:7788',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Fallback dorm manager for students without building assignment
FALLBACK_DORM_MANAGER_USER_ID = '92008149'

# 青橄榄SSO配置
QGL_MOBILE_APP_KEY = config('QGL_MOBILE_APP_KEY', default='abc0a32aa8dd94d1f765841abaafd8ba')
QGL_MOBILE_APP_SECRET = config('QGL_MOBILE_APP_SECRET', default='b1d2efa9587446d80ce6388e0c0b25131b8dea59')
QGL_MOBILE_TENANT_CODE = config('QGL_MOBILE_TENANT_CODE', default='C10026')
QGL_MOBILE_APPID = config('QGL_MOBILE_APPID', default='c6qgh2')

QGL_ADMIN_APP_KEY = config('QGL_ADMIN_APP_KEY', default='APPKEY_TBD')
QGL_ADMIN_APP_SECRET = config('QGL_ADMIN_APP_SECRET', default='APPSECRET_TBD')

# Feature Flags
FEATURE_FLAGS = {
    'stay_school_approval': config('ENABLE_STAY_SCHOOL', default=False, cast=bool),
    'leave_request_approval': config('ENABLE_LEAVE_REQUEST', default=False, cast=bool),
}
