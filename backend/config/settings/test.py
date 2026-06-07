"""Test settings - use SQLite instead of PostgreSQL"""
from .base import *
import tempfile

# Use SQLite for testing (no PostgreSQL client libraries required)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}

# Speed up tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

MEDIA_ROOT = tempfile.mkdtemp(prefix='graduation_leave_test_media_')
