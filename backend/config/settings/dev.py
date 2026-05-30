"""Development settings."""
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Development-specific apps
INSTALLED_APPS += [
    'django_extensions',
]

# Console email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable CORS restrictions in development
CORS_ALLOW_ALL_ORIGINS = True
