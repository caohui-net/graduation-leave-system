"""Production settings."""
from .base import *
import sys

DEBUG = False

# Security settings - HTTPS enforced by default in production
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)

# Production security checks
INSECURE_KEYS = [
    'django-insecure-dev-key-change-in-production',
    'django-insecure-docker-dev-key-change-in-production',
]

if SECRET_KEY in INSECURE_KEYS:
    print("ERROR: Production deployment with insecure SECRET_KEY detected.", file=sys.stderr)
    print("Generate a new key: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'", file=sys.stderr)
    sys.exit(1)

# Block demo authentication in production
import os
if os.environ.get('DEMO_AUTH_ENABLED', 'false').lower() == 'true':
    print("ERROR: DEMO_AUTH_ENABLED=true is not allowed in production.", file=sys.stderr)
    sys.exit(1)
