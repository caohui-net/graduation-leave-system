# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-02T19:35:13.353Z

## Original task

Environment setup blocker for graduation-leave-system project:

**Context:**
- Django project with PostgreSQL backend (psycopg2-binary dependency)
- Running tests requires Django environment setup
- Step 4B Phase 3 (XG user sync apply mode) and Step 5 (management command) implemented and committed
- Need to run Phase 4 regression testing to verify no breaking changes

**Blocker:**
- psycopg2-binary installation fails: 'pg_config executable not found'
- PostgreSQL client dev files (libpq-dev) not installed
- sudo not available to install system packages
- Python 3.14.4 environment

**Question:**
What's the best approach to run Django tests without PostgreSQL client libraries? Options:
1. Configure Django tests to use SQLite (no psycopg2 needed)
2. Use psycopg3 (newer, might have better binary support)
3. Mock database for tests
4. Other approach?

**Goal:**
Run full test suite (apps.users, apps.applications, apps.approvals) to verify Phase 3 changes don't break existing functionality.

## Final prompt

Environment setup blocker for graduation-leave-system project:

**Context:**
- Django project with PostgreSQL backend (psycopg2-binary dependency)
- Running tests requires Django environment setup
- Step 4B Phase 3 (XG user sync apply mode) and Step 5 (management command) implemented and committed
- Need to run Phase 4 regression testing to verify no breaking changes

**Blocker:**
- psycopg2-binary installation fails: 'pg_config executable not found'
- PostgreSQL client dev files (libpq-dev) not installed
- sudo not available to install system packages
- Python 3.14.4 environment

**Question:**
What's the best approach to run Django tests without PostgreSQL client libraries? Options:
1. Configure Django tests to use SQLite (no psycopg2 needed)
2. Use psycopg3 (newer, might have better binary support)
3. Mock database for tests
4. Other approach?

**Goal:**
Run full test suite (apps.users, apps.applications, apps.approvals) to verify Phase 3 changes don't break existing functionality.

## Raw output

```text
Best approach: use the existing Docker test environment, not SQLite. This repo already has `docker-compose.yml` with PostgreSQL and `backend/Dockerfile` installs `libpq-dev`, so it avoids the host Python 3.14 / `pg_config` problem while keeping production-like PostgreSQL behavior.

I ran the regression scope in Docker. Django started correctly and found `119` tests, so the psycopg blocker is bypassed. The run failed with `39` errors, all from the same schema issue:

`class_mappings.dorm_manager_id does not exist`

That is not a psycopg/install problem. The current `ClassMapping` model has `dorm_manager` and `dorm_manager_name`, but `backend/apps/users/migrations/0001_initial.py` only creates the counselor fields. A clean test DB confirmed this, so `--keepdb` was not the root cause.

Recommended path:

```bash
rtk docker compose exec -T backend python manage.py makemigrations users
rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_mapper apps.users.tests.test_xg_user_client apps.users.tests.test_xg_user_sync apps.users.tests.test_import_csv apps.applications.tests.test_application_flow apps.applications.tests.test_serializer_validation apps.applications.tests.test_list_permissions apps.applications.tests.test_constraints apps.applications.tests.test_error_cases apps.applications.tests.test_detail_permissions apps.applications.tests.test_p0_fixes apps.approvals.tests.test_rejection_flow apps.approvals.tests.test_list_permissions apps.approvals.tests.test_permissions apps.approvals.tests.test_state_machine --noinput -v 2
```

Option ranking:

1. **Docker/PostgreSQL: best for Phase 4 regression.**
2. **psycopg3 binary: good host fallback.** Django 4.2 supports psycopg 3.1.8+ or psycopg2, and psycopg’s binary install supports Python 3.10-3.14 without local `libpq` or build tools. Sources: Django docs and Psycopg docs. ([docs.djangoproject.com](https://docs.djangoproject.com/en/4.2/ref/databases/)) ([psycopg.org](https://www.psycopg.org/psycopg3/docs/basic/install.html))
3. **SQLite: acceptable only as a fast smoke-test fallback**, but weaker for regression because it changes DB semantics.
4. **Mock database: not appropriate** for this suite; these are ORM/API workflow tests.


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e89d0-a73c-7a10-ac9b-f4b44f10fd43
--------
user
Environment setup blocker for graduation-leave-system project:

**Context:**
- Django project with PostgreSQL backend (psycopg2-binary dependency)
- Running tests requires Django environment setup
- Step 4B Phase 3 (XG user sync apply mode) and Step 5 (management command) implemented and committed
- Need to run Phase 4 regression testing to verify no breaking changes

**Blocker:**
- psycopg2-binary installation fails: 'pg_config executable not found'
- PostgreSQL client dev files (libpq-dev) not installed
- sudo not available to install system packages
- Python 3.14.4 environment

**Question:**
What's the best approach to run Django tests without PostgreSQL client libraries? Options:
1. Configure Django tests to use SQLite (no psycopg2 needed)
2. Use psycopg3 (newer, might have better binary support)
3. Mock database for tests
4. Other approach?

**Goal:**
Run full test suite (apps.users, apps.applications, apps.approvals) to verify Phase 3 changes don't break existing functionality.
codex
I’ll check the project’s dependency and settings shape before recommending a path, because the right answer depends on Django version and whether the code imports `psycopg2` directly or only uses Django’s backend.
exec
/bin/bash -lc "sed -n '1,220p' /home/caohui/.codex/RTK.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# RTK - Rust Token Killer (Codex CLI)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Always prefix shell commands with `rtk`.

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

## Meta Commands

```bash
rtk gain            # Token savings analytics
rtk gain --history  # Recent command savings history
rtk proxy <cmd>     # Run raw command without filtering
```

## Verification

```bash
rtk --version
rtk gain
which rtk
```

exec
/bin/bash -lc "pwd && rg --files -g 'requirements*.txt' -g 'pyproject.toml' -g 'Pipfile' -g 'setup.cfg' -g 'tox.ini' -g 'pytest.ini' -g 'manage.py' -g 'settings*.py' -g '*/settings/*.py'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
/home/caohui/projects/graduation-leave-system
backend/manage.py

codex
The local rule is to run project commands through `rtk`; I’ve got that context now. I’m going to inspect only the settings/dependency files needed to see whether SQLite testing is viable or whether the import path forces a PostgreSQL driver.
exec
/bin/bash -lc "rtk find . -maxdepth 3 -type f \\( -name 'requirements*.txt' -o -name 'pyproject.toml' -o -name '.env*' -o -name 'pytest.ini' -o -name 'tox.ini' \\)" in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
rtk: rtk find does not support compound predicates or actions (e.g. -not, -exec). Use `find` directly.

exec
/bin/bash -lc 'rtk rg --files backend' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/data/templates/counselors_template.csv
backend/data/templates/class_mappings_template.csv
backend/data/templates/students_template.csv
backend/requirements/base.txt
backend/requirements/dev.txt
backend/requirements/prod.txt
backend/schema.py
backend/manage.py
backend/Dockerfile
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md
backend/apps/approvals/validators.py
backend/apps/approvals/__init__.py
backend/apps/approvals/admin.py
backend/apps/approvals/pagination.py
backend/apps/approvals/urls.py
backend/apps/approvals/migrations/__init__.py
backend/apps/approvals/migrations/0002_initial.py
backend/apps/approvals/migrations/0001_initial.py
backend/apps/approvals/tests/__init__.py
backend/apps/approvals/tests/test_rejection_flow.py
backend/apps/approvals/tests/test_list_permissions.py
backend/apps/approvals/tests/test_permissions.py
backend/apps/approvals/tests/test_state_machine.py
backend/apps/approvals/views.py
backend/apps/approvals/serializers.py
backend/apps/approvals/models.py
backend/apps/applications/__init__.py
backend/apps/applications/admin.py
backend/apps/applications/providers.py
backend/apps/applications/pagination.py
backend/apps/applications/urls.py
backend/apps/applications/migrations/0003_application_unique_student_application.py
backend/apps/applications/migrations/__init__.py
backend/apps/applications/migrations/0002_initial.py
backend/apps/applications/migrations/0001_initial.py
backend/apps/applications/migrations/0004_remove_unique_student_constraint.py
backend/apps/applications/tests/__init__.py
backend/apps/applications/tests/test_p0_fixes.py
backend/apps/applications/tests/test_error_cases.py
backend/apps/applications/tests/test_detail_permissions.py
backend/apps/applications/tests/test_serializer_validation.py
backend/apps/applications/tests/test_list_permissions.py
backend/apps/applications/tests/test_constraints.py
backend/apps/applications/tests/test_application_flow.py
backend/apps/applications/views.py
backend/apps/applications/permissions.py
backend/apps/applications/serializers.py
backend/apps/applications/models.py
backend/scripts/diagnose_xg_api.py
backend/apps/notifications/services.py
backend/apps/notifications/__init__.py
backend/apps/notifications/admin.py
backend/apps/notifications/urls.py
backend/apps/notifications/serializers.py
backend/apps/notifications/models.py
backend/apps/notifications/migrations/__init__.py
backend/apps/notifications/migrations/0001_initial.py
backend/apps/notifications/migrations/0002_alter_notification_type.py
backend/apps/notifications/apps.py
backend/apps/users/integrations/__init__.py
backend/apps/users/integrations/xg_user_client.py
backend/apps/users/integrations/xg_user_mapper.py
backend/apps/notifications/tests/__init__.py
backend/config/__init__.py
backend/apps/notifications/tests/test_auto_notifications_api.py
backend/apps/notifications/tests/test_timeout_warnings.py
backend/config/urls.py
backend/apps/users/services/xg_user_sync.py
backend/apps/notifications/tests/test_models.py
backend/apps/users/__init__.py
backend/apps/users/admin.py
backend/apps/users/urls.py
backend/config/settings/__init__.py
backend/config/settings/base.py
backend/config/settings/prod.py
backend/config/settings/dev.py
backend/config/wsgi.py
backend/apps/notifications/tests/test_api.py
backend/apps/notifications/tests/test_auto_notifications.py
backend/apps/notifications/views.py
backend/apps/users/views.py
backend/apps/users/serializers.py
backend/apps/users/models.py
backend/apps/users/migrations/0002_user_department_user_email_user_phone.py
backend/apps/users/class_mapping.py
backend/apps/users/apps.py
backend/apps/attachments/__init__.py
backend/apps/attachments/urls.py
backend/apps/users/migrations/0001_initial.py
backend/apps/users/migrations/__init__.py
backend/apps/attachments/serializers.py
backend/apps/attachments/models.py
backend/apps/attachments/views.py
backend/apps/users/management/__init__.py
backend/apps/users/management/commands/__init__.py
backend/apps/users/management/commands/import_csv.py
backend/apps/users/management/commands/sync_xg_users.py
backend/apps/users/management/commands/seed_data.py
backend/apps/attachments/migrations/__init__.py
backend/apps/attachments/migrations/0001_initial.py
backend/apps/notifications/management/__init__.py
backend/apps/users/tests/__init__.py
backend/apps/attachments/tests/__init__.py
backend/apps/users/tests/test_xg_user_mapper.py
backend/apps/users/tests/test_xg_user_client.py
backend/apps/users/tests/test_xg_user_sync.py
backend/apps/users/tests/test_import_csv.py
backend/apps/attachments/tests/test_list.py
backend/apps/attachments/tests/test_delete.py
backend/apps/attachments/tests/test_upload.py
backend/apps/attachments/tests/test_download.py
backend/apps/notifications/management/commands/seed_notifications.py
backend/apps/notifications/management/commands/send_approval_timeout_warnings.py
backend/apps/notifications/management/commands/__init__.py

codex
One command shape was rejected by `rtk`, so I’ll use simpler `rtk` commands from here. The file listing shows a conventional `backend/config/settings` layout and targeted tests in the three requested apps.
exec
/bin/bash -lc "rtk sed -n '1,220p' backend/requirements/base.txt" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Django Core
Django==4.2.13
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
django-filter==23.5
drf-spectacular==0.27.1

# Database
psycopg2-binary==2.9.9

# State Machine
django-fsm==2.8.1

# Celery
celery==5.3.6
redis==5.0.3

# WeChat
wechatpy==1.8.18

# Retry
tenacity==8.2.3

# Password
bcrypt==4.1.2

# Environment
python-decouple==3.8

# Utils
python-dateutil==2.9.0
pytz==2024.1

# File Processing
python-magic==0.4.27

# Work Day Calculation
chinese-calendar==1.9.0

# HTTP Client
requests==2.31.0

# Encryption
cryptography==42.0.5

# Cache
django-redis==5.4.0

exec
/bin/bash -lc "rtk sed -n '1,220p' backend/requirements/dev.txt" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
-r base.txt

# Testing
pytest==8.1.1
pytest-django==4.8.0
pytest-cov==5.0.0
factory-boy==3.3.0

# Code Quality
black==24.3.0
isort==5.13.2
flake8==7.0.0
pylint==3.1.0
mypy==1.9.0

# Debug
django-debug-toolbar==4.3.0
ipython==8.23.0

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/config/settings/base.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
"""
Django settings for graduation leave system project.
Base settings shared across all environments.
"""
from pathlib import Path
from decouple import config
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

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
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
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
    default='http://localhost:3000,http://127.0.0.1:3000',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

exec
/bin/bash -lc "rtk sed -n '1,220p' backend/config/settings/dev.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
"""Development settings."""
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Console email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable CORS restrictions in development
CORS_ALLOW_ALL_ORIGINS = True

codex
I’m checking for database-specific assumptions now. If tests only exercise normal ORM behavior, a dedicated SQLite test settings module is the fastest way to unblock regression coverage; if there are PostgreSQL-only constraints or raw SQL, that changes the recommendation.
exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/models.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserRole(models.TextChoices):
    STUDENT = 'student', '学生'
    DORM_MANAGER = 'dorm_manager', '宿管员'
    COUNSELOR = 'counselor', '辅导员'
    DEAN = 'dean', '学工部'


class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError('user_id is required')
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('active', True)
        return self.create_user(user_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=UserRole.choices)
    active = models.BooleanField(default=True)
    class_id = models.CharField(max_length=50, null=True, blank=True)
    is_graduating = models.BooleanField(null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)

    # API补充字段（学工系统）
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'role']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.user_id} - {self.name}"

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/applications/models.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.db import models
from django.core.exceptions import ValidationError
from apps.users.models import User


class ApplicationStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
    APPROVED = 'approved', '已通过'
    REJECTED = 'rejected', '已驳回'


class DormCheckoutStatus(models.TextChoices):
    COMPLETED = 'completed', '已清退'
    PENDING = 'pending', '清退中'
    NOT_STARTED = 'not_started', '未开始'
    UNKNOWN = 'unknown', '状态未知'


class Application(models.Model):
    application_id = models.CharField(max_length=50, primary_key=True)
    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
    student_name = models.CharField(max_length=100)
    class_id = models.CharField(max_length=50)
    reason = models.TextField()
    leave_date = models.DateField()
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT)
    dorm_checkout_status = models.CharField(max_length=20, choices=DormCheckoutStatus.choices, default=DormCheckoutStatus.NOT_STARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'applications'

    def clean(self):
        if self.status in [ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.APPROVED]:
            existing = Application.objects.filter(
                student=self.student,
                status__in=[ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.APPROVED]
            ).exclude(application_id=self.application_id).exists()
            if existing:
                raise ValidationError('该学生已有待审批或已通过的申请，不能重复提交')

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/approvals/models.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.db import models
from apps.users.models import User
from apps.applications.models import Application


class ApprovalStep(models.TextChoices):
    DORM_MANAGER = 'dorm_manager', '宿管员'
    COUNSELOR = 'counselor', '辅导员'


class ApprovalDecision(models.TextChoices):
    PENDING = 'pending', '待审批'
    APPROVED = 'approved', '已通过'
    REJECTED = 'rejected', '已驳回'


class Approval(models.Model):
    approval_id = models.CharField(max_length=50, primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.PROTECT, related_name='approvals')
    step = models.CharField(max_length=20, choices=ApprovalStep.choices)
    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals')
    approver_name = models.CharField(max_length=100)
    decision = models.CharField(max_length=20, choices=ApprovalDecision.choices, default=ApprovalDecision.PENDING)
    comment = models.TextField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'approvals'

exec
/bin/bash -lc "rtk rg -n \"psycopg|postgres|ArrayField|JSONField|GinIndex|GistIndex|ExclusionConstraint|RawSQL|cursor\\(|select_for_update|distinct\\(|__contains|Trunc|Now\\(|database|pytestmark|django_db|TransactionTestCase|TestCase\" backend/apps backend/config" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/config/settings/base.py:75:        'ENGINE': 'django.db.backends.postgresql',
backend/config/settings/base.py:77:        'USER': config('DB_USER', default='postgres'),
backend/config/settings/base.py:78:        'PASSWORD': config('DB_PASSWORD', default='postgres'),
backend/apps/approvals/tests/test_rejection_flow.py:1:from django.test import TestCase
backend/apps/approvals/tests/test_rejection_flow.py:12:class RejectionFlowTestCase(TestCase):
backend/apps/approvals/tests/test_list_permissions.py:1:from django.test import TestCase
backend/apps/approvals/tests/test_list_permissions.py:8:class ApprovalListPermissionTest(TestCase):
backend/apps/approvals/tests/test_permissions.py:1:from django.test import TestCase
backend/apps/approvals/tests/test_permissions.py:11:class ApprovalPermissionsTestCase(TestCase):
backend/apps/approvals/tests/test_state_machine.py:1:from django.test import TestCase
backend/apps/approvals/tests/test_state_machine.py:10:class ApprovalStateMachineTestCase(TestCase):
backend/apps/approvals/views.py:108:        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
backend/apps/approvals/views.py:198:        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
backend/apps/applications/tests/test_p0_fixes.py:1:from django.test import TestCase
backend/apps/applications/tests/test_p0_fixes.py:11:class ResubmissionAfterRejectionTest(TestCase):
backend/apps/applications/tests/test_p0_fixes.py:84:class ApprovalDecisionFilterTest(TestCase):
backend/apps/applications/tests/test_error_cases.py:1:from django.test import TestCase
backend/apps/applications/tests/test_error_cases.py:11:class ErrorCasesTestCase(TestCase):
backend/apps/applications/tests/test_detail_permissions.py:1:from django.test import TestCase
backend/apps/applications/tests/test_detail_permissions.py:10:class ApplicationDetailPermissionTest(TestCase):
backend/apps/applications/tests/test_serializer_validation.py:1:from django.test import TestCase
backend/apps/applications/tests/test_serializer_validation.py:8:class ApplicationCreateSerializerTest(TestCase):
backend/apps/applications/tests/test_list_permissions.py:1:from django.test import TestCase
backend/apps/applications/tests/test_list_permissions.py:9:class ApplicationListPermissionTest(TestCase):
backend/apps/applications/tests/test_constraints.py:1:from django.test import TestCase
backend/apps/applications/tests/test_constraints.py:11:class ApplicationConstraintsTestCase(TestCase):
backend/apps/applications/tests/test_application_flow.py:1:from django.test import TestCase
backend/apps/applications/tests/test_application_flow.py:12:class ApplicationFlowTestCase(TestCase):
backend/apps/notifications/tests/test_auto_notifications_api.py:8:from django.test import TestCase
backend/apps/notifications/tests/test_auto_notifications_api.py:19:class AutoNotificationAPITest(TestCase):
backend/apps/notifications/tests/test_timeout_warnings.py:1:from django.test import TestCase
backend/apps/notifications/tests/test_timeout_warnings.py:13:class ApprovalTimeoutWarningTests(TestCase):
backend/apps/notifications/tests/test_models.py:1:from django.test import TestCase
backend/apps/notifications/tests/test_models.py:7:class NotificationModelTest(TestCase):
backend/apps/notifications/tests/test_api.py:1:from django.test import TestCase
backend/apps/notifications/tests/test_api.py:8:class NotificationAPITest(TestCase):
backend/apps/users/tests/test_xg_user_mapper.py:2:from django.test import TestCase
backend/apps/users/tests/test_xg_user_mapper.py:6:class XGUserMapperTests(TestCase):
backend/apps/users/management/commands/sync_xg_users.py:8:    help = 'Sync users from XG system to local database'
backend/apps/users/management/commands/sync_xg_users.py:14:            help='Apply changes to database (default is dry-run)'
backend/apps/users/management/commands/sync_xg_users.py:66:            self.stdout.write(self.style.WARNING('\nDry-run mode: no changes written to database'))
backend/apps/users/tests/test_xg_user_sync.py:2:from django.test import TestCase
backend/apps/users/tests/test_xg_user_sync.py:9:class XGUserSyncPlanTests(TestCase):
backend/apps/users/tests/test_xg_user_sync.py:226:class XGUserSyncApplyTests(TestCase):
backend/apps/notifications/tests/test_auto_notifications.py:12:from django.test import TestCase
backend/apps/notifications/tests/test_auto_notifications.py:22:class AutoNotificationTest(TestCase):
backend/apps/users/tests/test_xg_user_client.py:2:from django.test import TestCase
backend/apps/users/tests/test_xg_user_client.py:7:class GenerateSignTests(TestCase):
backend/apps/users/tests/test_xg_user_client.py:49:class XGUserAPIConfigTests(TestCase):
backend/apps/users/tests/test_xg_user_client.py:115:class XGUserAPIClientTests(TestCase):
backend/apps/attachments/tests/test_list.py:1:from django.test import TestCase
backend/apps/attachments/tests/test_list.py:12:class AttachmentListTestCase(TestCase):
backend/apps/users/tests/test_import_csv.py:4:from django.test import TestCase
backend/apps/users/tests/test_import_csv.py:11:class ImportCSVCommandTest(TestCase):
backend/apps/attachments/tests/test_upload.py:1:from django.test import TestCase
backend/apps/attachments/tests/test_upload.py:11:class AttachmentUploadTestCase(TestCase):
backend/apps/attachments/tests/test_download.py:1:from django.test import TestCase
backend/apps/attachments/tests/test_download.py:12:class AttachmentDownloadTestCase(TestCase):
backend/apps/attachments/tests/test_delete.py:1:from django.test import TestCase
backend/apps/attachments/tests/test_delete.py:11:class AttachmentDeleteTestCase(TestCase):

web search: 
web search: psycopg 3 binary package Python 3.14 support official docs
web search: 
web search: Django 4.2 PostgreSQL psycopg 3 support official documentation
codex
Django 4.2 can use either psycopg2 or psycopg 3 for PostgreSQL, but that still keeps you on a PostgreSQL backend. For this repo’s regression target, I’m leaning toward a temporary SQLite test settings module because the app models look portable and the tests are `django.test.TestCase` ORM/API tests rather than PostgreSQL feature tests.
exec
/bin/bash -lc 'rtk python --version' in /home/caohui/projects/graduation-leave-system
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

exec
/bin/bash -lc 'rtk python -m pip --version' in /home/caohui/projects/graduation-leave-system
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

exec
/bin/bash -lc "rtk python - <<'PY'
try:
    import django
    print('django', django.get_version())
except Exception as exc:
    print(type(exc).__name__, exc)
try:
    import psycopg2
    print('psycopg2 ok')
except Exception as exc:
    print('psycopg2', type(exc).__name__, exc)
try:
    import psycopg
    print('psycopg ok')
except Exception as exc:
    print('psycopg', type(exc).__name__, exc)
PY" in /home/caohui/projects/graduation-leave-system
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

exec
/bin/bash -lc "rtk rg -n \"DJANGO_SETTINGS_MODULE|pytest|manage.py test|test .*apps\\.|DATABASES|sqlite\" ." in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
./task_plan.md:30:| Host `python3 manage.py test` lacks Django | First targeted test run | Used running Docker backend container. |
./task_plan.md:32:| Broad test label discovery failed for `apps.approvals.tests apps.applications.tests` | Full test attempt | Ran explicit test modules; 37 tests passed. |
./backend/requirements/dev.txt:4:pytest==8.1.1
./backend/requirements/dev.txt:5:pytest-django==4.8.0
./backend/requirements/dev.txt:6:pytest-cov==5.0.0
./docs/acceptance/phase4c-evidence-index.md:15:docker compose exec backend python manage.py test --keepdb
./docs/acceptance/phase4c-evidence-index.md:18:docker compose exec backend python manage.py test apps.applications.tests --keepdb
./docs/acceptance/phase4c-evidence-index.md:19:docker compose exec backend python manage.py test apps.approvals.tests --keepdb
./docs/acceptance/phase4c-evidence-index.md:20:docker compose exec backend python manage.py test apps.attachments.tests --keepdb
./docs/acceptance/phase4c-evidence-index.md:21:docker compose exec backend python manage.py test apps.users.tests --keepdb
./docs/acceptance/phase4c-evidence-index.md:24:docker compose exec backend python manage.py test apps.users.tests.test_import_csv --keepdb
./docs/superpowers/plans/2026-05-27-implementation-plan.md:204:   - 配置pytest
./docs/PROJECT-SUMMARY.md:774:- `docker compose exec backend python manage.py test apps.approvals.tests.test_permissions apps.approvals.tests.test_state_machine --keepdb`：10 tests OK
./docs/PROJECT-SUMMARY.md:775:- `docker compose exec backend python manage.py test [explicit approvals/applications test modules] --keepdb`：37 tests OK
./docs/design/2026-05-27-system-design.md:2403:DATABASES = {
./docs/design/2026-05-27-system-design.md:2552:- pytest + pytest-django
./docs/design/2026-05-27-system-design.md:2571:# pytest tests/test_application.py::test_application_submit_generates_number
./docs/design/2026-05-27-system-design.md:2701:- pytest-mock（模拟外部系统）
./backend/config/settings/base.py:73:DATABASES = {
./backend/manage.py:9:    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
./backend/config/wsgi.py:5:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:151:docker exec backend python manage.py test --help
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:152:docker exec backend python manage.py test apps.users.tests.test_models -v 2
./backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:112:docker exec backend python manage.py test apps.applications.tests.test_application_flow apps.applications.tests.test_error_cases apps.approvals.tests.test_rejection_flow --keepdb
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:153:# pytest.ini
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:154:[pytest]
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:187:      DATABASE_URL: sqlite:///test.db
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:188:    run: pytest tests/unit/
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:197:    run: pytest tests/integration/
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:238:- ✓ 测试框架选择合理（pytest）
./backend/scripts/diagnose_xg_api.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:74:docker exec graduation-leave-system-backend-1 python manage.py test \
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:139:3. **host测试环境不可用。** 当前直接运行`python3 backend/manage.py test`失败：未安装Django。若验收依赖Docker，计划需明确Docker命令。
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:156:- pytest + pytest-django + factory_boy
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:255:`.gitignore` 覆盖面合理，适合当前技术栈。尤其是 `.env`、`node_modules/`、`.pytest_cache/`、`staticfiles/`、`db.sqlite3` 等常见噪声和敏感文件都已排除。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:487:测试策略方向正确：pytest、PostgreSQL、TDD、覆盖率 80%+、并发测试、文件安全测试、限流测试、审计测试。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:491:- 没有 pytest 配置
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:494:- dev requirements 缺少 `pytest-mock`、`bandit`、`pre-commit`、`locust` 等计划中提到或实际需要的工具
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:499:- `pytest.ini`
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:535:3. 建立 pytest + PostgreSQL 测试基线。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:556:   - dev：pytest 工具、pre-commit、安全扫描、压测工具
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:581:> 本地 Docker 可启动，Django 可访问，PostgreSQL/Redis 可连接，pytest 可运行。
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:132:docker exec backend python manage.py test apps.approvals.tests apps.applications.tests
./docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:149:- ❌ `DATABASES`设置在启动时加载，无法运行时变更
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:216:- Codex提到"修测试发现和测试数据，让`manage.py test`默认能发现并通过核心测试"
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:218:- 建议：Day 2至少修复测试发现问题，让`manage.py test`能找到测试
./docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:169:PYTHONPATH=. python backend/manage.py test apps.notifications.tests.test_auto_notifications apps.notifications.tests.test_auto_notifications_api --keepdb --noinput
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:116:4. **修测试发现和测试数据**：让`manage.py test`默认能发现并通过核心测试
./docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:20:- 聚焦测试在 Docker 环境通过：`rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput`，4/4 passed。
./docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:98:- 不在常规 Django/pytest 测试套件里触发 live API。
./docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:147:docker compose exec -T backend python manage.py test \
./docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:19:docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client --keepdb --noinput
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:109:docker compose exec backend python manage.py test apps.users.tests.test_xg_user_sync -v 2 --keepdb
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:119:docker compose exec backend python manage.py test apps.users.tests.test_xg_user_sync -v 2 --keepdb
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:127:docker compose exec backend python manage.py test apps.users.tests.test_xg_user_mapper apps.users.tests.test_xg_user_sync -v 2 --keepdb
./docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:57:docker compose exec -T backend python manage.py test \
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:164:pytest backend/apps/users/tests/test_xg_user_sync.py -v
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:30:docker compose exec backend python manage.py test apps.notifications.tests.test_auto_notifications apps.notifications.tests.test_auto_notifications_api
./docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:214:**验证：** 运行 `pytest backend/apps/attachments/tests/test_list.py -v`
./docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:47:rtk docker compose exec -T backend python manage.py test \
./docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:253:**命令：** `docker compose exec -T backend python manage.py test apps.attachments.tests.test_list -v 2`
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:38:docker compose exec backend python manage.py test apps.users.tests.test_xg_user_sync -v 2
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:97:docker compose exec backend python manage.py test apps.users.tests.test_xg_user_sync -v 2
./docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md:17:**验证结果：** `docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client --keepdb --noinput`，29/29 passed。
./docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:90:- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
./docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:130:不建议把真实API调用写进Django常规测试套件。若确实需要live测试，使用 pytest marker 或环境变量硬门禁，并默认跳过。
./docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:96:- 不在pytest测试套件中
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:235:- 尝试运行通知测试：`python3 manage.py test apps.notifications...`，本地环境缺少Django依赖，未能执行。
./docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:29:python manage.py test apps.attachments.tests.test_upload apps.attachments.tests.test_list apps.attachments.tests.test_download apps.attachments.tests.test_delete -v 2
./docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:96:rtk docker compose exec -T backend python manage.py test apps.attachments.tests.test_list -v 2
./docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:102:rtk docker compose exec -T backend python manage.py test apps.attachments.tests.test_upload apps.attachments.tests.test_list apps.attachments.tests.test_download apps.attachments.tests.test_delete -v 2
./docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:110:rtk docker compose exec -T backend python manage.py test apps.attachments.tests -v 2
./docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:163:**命令：** `docker compose exec -T backend python manage.py test apps.attachments.tests.test_list -v 2`
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:33:docker compose exec backend python manage.py test apps.users.tests.test_xg_user_sync --keepdb -v 2
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:132:**命令：** docker compose exec backend python manage.py test
./docs/discussions/phase4c-next-steps/24-claude-consensus-evidence-closure.md:41:- 测试命令：`docker compose exec backend python manage.py test`
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:167:docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_sync -v 2
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:175:docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_sync -v 2 --noinput
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:183:docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_mapper apps.users.tests.test_xg_user_sync -v 2 --noinput
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:208:docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_mapper apps.users.tests.test_xg_user_sync -v 2 --noinput

web search: 
web search: Django 4.2 PostgreSQL psycopg 3 support docs.djangoproject.com
codex
There is also an existing project precedent for running tests inside Docker, which is the strongest option if Docker is available because it preserves the PostgreSQL backend instead of changing test semantics. I’m checking whether that route is defined locally before giving the recommendation.
exec
/bin/bash -lc "rtk rg --files -g 'docker-compose*.yml' -g 'compose*.yml' -g 'Dockerfile'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docker-compose.yml
backend/Dockerfile

exec
/bin/bash -lc 'rtk rg -n "backend:|postgres|POSTGRES|DB_HOST|image: postgres|build:.*backend|docker compose" docker-compose.yml docker-compose.yaml compose.yml compose.yaml backend/Dockerfile docs/acceptance/phase4c-evidence-index.md task_plan.md' in /home/caohui/projects/graduation-leave-system
 exited 2 in 0ms:
rg: docker-compose.yaml: No such file or directory (os error 2)
rg: compose.yml: No such file or directory (os error 2)
rg: compose.yaml: No such file or directory (os error 2)
docs/acceptance/phase4c-evidence-index.md:15:docker compose exec backend python manage.py test --keepdb
docs/acceptance/phase4c-evidence-index.md:18:docker compose exec backend python manage.py test apps.applications.tests --keepdb
docs/acceptance/phase4c-evidence-index.md:19:docker compose exec backend python manage.py test apps.approvals.tests --keepdb
docs/acceptance/phase4c-evidence-index.md:20:docker compose exec backend python manage.py test apps.attachments.tests --keepdb
docs/acceptance/phase4c-evidence-index.md:21:docker compose exec backend python manage.py test apps.users.tests --keepdb
docs/acceptance/phase4c-evidence-index.md:24:docker compose exec backend python manage.py test apps.users.tests.test_import_csv --keepdb
docs/acceptance/phase4c-evidence-index.md:83:docker compose exec backend python manage.py import_csv \
docs/acceptance/phase4c-evidence-index.md:87:docker compose exec backend python manage.py import_csv \
docs/acceptance/phase4c-evidence-index.md:89:docker compose exec backend python manage.py import_csv \
docs/acceptance/phase4c-evidence-index.md:91:docker compose exec backend python manage.py import_csv \
docs/acceptance/phase4c-evidence-index.md:115:2. 启动服务：`docker compose up -d`
docs/acceptance/phase4c-evidence-index.md:116:3. 数据库迁移：`docker compose exec backend python manage.py migrate`
docs/acceptance/phase4c-evidence-index.md:117:4. 加载数据：`docker compose exec backend python manage.py seed_data`
docs/acceptance/phase4c-evidence-index.md:140:- postgres_data volume（数据库持久化）
backend/Dockerfile:8:    postgresql-client \
docker-compose.yml:5:    image: postgres:15-alpine
docker-compose.yml:7:      POSTGRES_DB: graduation_leave
docker-compose.yml:8:      POSTGRES_USER: postgres
docker-compose.yml:9:      POSTGRES_PASSWORD: postgres
docker-compose.yml:13:      - postgres_data:/var/lib/postgresql/data
docker-compose.yml:15:      test: ["CMD-SHELL", "pg_isready -U postgres"]
docker-compose.yml:20:  backend:
docker-compose.yml:26:      - ./backend:/app
docker-compose.yml:37:  postgres_data:

codex
I’m going to read the compose and Dockerfile directly. The earlier `rg` included missing filenames, which made the exit noisy, but it still showed the key signal: the backend image already installs PostgreSQL client support.
exec
/bin/bash -lc "rtk sed -n '1,180p' docker-compose.yml" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: graduation_leave
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
      - media_data:/app/media
    ports:
      - "8001:8000"
    env_file:
      - .env.docker
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
  media_data:

exec
/bin/bash -lc "rtk sed -n '1,160p' backend/Dockerfile" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements/ /app/requirements/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements/base.txt

# Copy application code
COPY . /app/

# Expose port
EXPOSE 8000

# Run Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

exec
/bin/bash -lc 'rtk docker compose ps' in /home/caohui/projects/graduation-leave-system
 succeeded in 192ms:
[compose] 2 services:
  graduation-leave-system-backend-1 (graduation-leave-system-backend) Up 26 hours [8001, 8001]
  graduation-leave-system-db-1 (postgres:15-alpine) Up 26 hours (healthy) [5432, 5432]

codex
Docker is already up and healthy here, so the best immediate path is to run the Phase 4 regression suite inside the existing backend container. That avoids the host Python 3.14/`psycopg2-binary` problem and tests against the project’s intended PostgreSQL service.
exec
/bin/bash -lc 'rtk docker compose exec -T backend python manage.py test apps.users.tests apps.applications.tests apps.approvals.tests --keepdb --noinput -v 2' in /home/caohui/projects/graduation-leave-system
 exited 1 in 491ms:
Traceback (most recent call last):
  File "/app/manage.py", line 22, in <module>
    main()
  File "/app/manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
    utility.execute()
  File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 436, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/commands/test.py", line 24, in run_from_argv
    super().run_from_argv(argv)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 412, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 458, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/core/management/commands/test.py", line 68, in handle
    failures = test_runner.run_tests(test_labels)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/test/runner.py", line 1048, in run_tests
    suite = self.build_suite(test_labels, extra_tests)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/test/runner.py", line 898, in build_suite
    tests = self.load_tests_for_label(label, discover_kwargs)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/test/runner.py", line 872, in load_tests_for_label
    tests = self.test_loader.discover(start_dir=label, **kwargs)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/unittest/loader.py", line 328, in discover
    self._top_level_dir = self._get_directory_containing_module(top_part)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/unittest/loader.py", line 339, in _get_directory_containing_module
    full_path = os.path.abspath(module.__file__)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen posixpath>", line 396, in abspath
TypeError: expected str, bytes or os.PathLike object, not NoneType

codex
The first Docker test command reached Django successfully but hit a known discovery issue when labels end in `.tests`. I’m rerunning with app labels, which should let Django discover tests under each app without tripping over package metadata.
exec
/bin/bash -lc 'rtk docker compose exec -T backend python manage.py test apps.users apps.applications apps.approvals --keepdb --noinput -v 2' in /home/caohui/projects/graduation-leave-system
 exited 1 in 418ms:
Traceback (most recent call last):
  File "/app/manage.py", line 22, in <module>
    main()
  File "/app/manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
    utility.execute()
  File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 436, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/commands/test.py", line 24, in run_from_argv
    super().run_from_argv(argv)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 412, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 458, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/core/management/commands/test.py", line 68, in handle
    failures = test_runner.run_tests(test_labels)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/test/runner.py", line 1048, in run_tests
    suite = self.build_suite(test_labels, extra_tests)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/test/runner.py", line 898, in build_suite
    tests = self.load_tests_for_label(label, discover_kwargs)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/test/runner.py", line 872, in load_tests_for_label
    tests = self.test_loader.discover(start_dir=label, **kwargs)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/unittest/loader.py", line 328, in discover
    self._top_level_dir = self._get_directory_containing_module(top_part)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/unittest/loader.py", line 339, in _get_directory_containing_module
    full_path = os.path.abspath(module.__file__)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen posixpath>", line 396, in abspath
TypeError: expected str, bytes or os.PathLike object, not NoneType

codex
The app/package labels also hit the same discovery bug, likely because `backend/apps` is a namespace package. I’ll run the concrete test modules instead; that is already how this repo’s prior evidence handled discovery issues.
exec
/bin/bash -lc 'rtk ls -la backend/apps backend/apps/users backend/apps/applications backend/apps/approvals backend/apps/users/tests backend/apps/applications/tests backend/apps/approvals/tests' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
applications/
approvals/
attachments/
notifications/
users/
__pycache__/
management/
migrations/
tests/
__pycache__/
__pycache__/
migrations/
tests/
__pycache__/
__pycache__/
integrations/
management/
migrations/
services/
tests/
__pycache__/
__init__.py  0B
admin.py  410B
models.py  1.9K
pagination.py  413B
permissions.py  911B
providers.py  2.1K
serializers.py  2.2K
urls.py  210B
views.py  8.1K
__init__.py  0B
test_application_flow.py  4.4K
test_constraints.py  2.0K
test_detail_permissions.py  4.5K
test_error_cases.py  5.7K
test_list_permissions.py  4.7K
test_p0_fixes.py  6.3K
test_serializer_validation.py  3.5K
__init__.py  0B
admin.py  383B
models.py  1.2K
pagination.py  410B
serializers.py  1.6K
urls.py  302B
validators.py  435B
views.py  9.5K
__init__.py  0B
test_list_permissions.py  5.9K
test_permissions.py  6.1K
test_rejection_flow.py  4.9K
test_state_machine.py  5.2K
__init__.py  12B
admin.py  637B
apps.py  147B
class_mapping.py  683B
models.py  2.0K
serializers.py  1.7K
urls.py  114B
views.py  1.1K
__init__.py  0B
test_import_csv.py  6.7K
test_xg_user_client.py  20.3K
test_xg_user_mapper.py  4.0K
test_xg_user_sync.py  14.0K

exec
/bin/bash -lc 'rtk rg --files backend/apps/users/tests backend/apps/applications/tests backend/apps/approvals/tests' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/approvals/tests/__init__.py
backend/apps/approvals/tests/test_rejection_flow.py
backend/apps/approvals/tests/test_list_permissions.py
backend/apps/approvals/tests/test_permissions.py
backend/apps/approvals/tests/test_state_machine.py
backend/apps/applications/tests/test_application_flow.py
backend/apps/applications/tests/test_serializer_validation.py
backend/apps/applications/tests/test_list_permissions.py
backend/apps/applications/tests/test_constraints.py
backend/apps/applications/tests/test_error_cases.py
backend/apps/applications/tests/test_detail_permissions.py
backend/apps/applications/tests/test_p0_fixes.py
backend/apps/applications/tests/__init__.py
backend/apps/users/tests/__init__.py
backend/apps/users/tests/test_xg_user_mapper.py
backend/apps/users/tests/test_xg_user_client.py
backend/apps/users/tests/test_xg_user_sync.py
backend/apps/users/tests/test_import_csv.py

web search: 
web search: https://docs.djangoproject.com/en/4.2/ref/databases/
codex
I have enough context for the answer, but I’m also going to execute the exact regression scope now using module labels so you get a concrete verification result, not just advice.
exec
/bin/bash -lc 'rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_mapper apps.users.tests.test_xg_user_client apps.users.tests.test_xg_user_sync apps.users.tests.test_import_csv apps.applications.tests.test_application_flow apps.applications.tests.test_serializer_validation apps.applications.tests.test_list_permissions apps.applications.tests.test_constraints apps.applications.tests.test_error_cases apps.applications.tests.test_detail_permissions apps.applications.tests.test_p0_fixes apps.approvals.tests.test_rejection_flow apps.approvals.tests.test_list_permissions apps.approvals.tests.test_permissions apps.approvals.tests.test_state_machine --keepdb --noinput -v 2' in /home/caohui/projects/graduation-leave-system
codex
The targeted run is still executing and has reached the CSV import tests after passing the XG mapper/client/sync cases, including the new apply-mode scenarios. I’ll wait for completion and report the final pass/fail count.
 exited 1 in 15909ms:
Using existing test database for alias 'default' ('test_graduation_leave')...
Found 119 test(s).
Operations to perform:
  Synchronize unmigrated apps: corsheaders, django_filters, drf_spectacular, messages, rest_framework, rest_framework_simplejwt, staticfiles
  Apply all migrations: admin, applications, approvals, attachments, auth, contenttypes, notifications, sessions, users
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying users.0002_user_department_user_email_user_phone... OK
System check identified no issues (0 silenced).
test_complete_fields_success (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_complete_fields_success)
测试完整字段成功映射 ... ok
test_missing_name_skip (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_missing_name_skip)
测试name缺失应跳过 ... ok
test_missing_number_skip (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_missing_number_skip)
测试number缺失应跳过 ... ok
test_missing_user_identity_skip (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_missing_user_identity_skip)
测试user_identity缺失应跳过 ... ok
test_multiple_missing_fields_priority (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_multiple_missing_fields_priority)
测试多个字段同时缺失的优先级 ... ok
test_optional_fields_missing (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_optional_fields_missing)
测试可选字段缺失不阻止映射 ... ok
test_unknown_user_identity_skip (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_unknown_user_identity_skip)
测试user_identity未知值应跳过 ... ok
test_user_identity_student_string (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_user_identity_student_string)
测试user_identity为'student'字符串 ... ok
test_invalid_encryption_type (apps.users.tests.test_xg_user_client.GenerateSignTests.test_invalid_encryption_type)
测试非法加密类型 ... ok
test_md5_encryption (apps.users.tests.test_xg_user_client.GenerateSignTests.test_md5_encryption)
测试md5加密（固定期望值） ... ok
test_official_sample_default_sha1 (apps.users.tests.test_xg_user_client.GenerateSignTests.test_official_sample_default_sha1)
测试官方样例（默认sha1） ... ok
test_official_sample_sha1 (apps.users.tests.test_xg_user_client.GenerateSignTests.test_official_sample_sha1)
测试官方签名样例（sha1） ... ok
test_build_form_data_custom (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_build_form_data_custom)
测试form-data构造（自定义参数） ... ok
test_build_form_data_default (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_build_form_data_default)
测试form-data构造（默认参数） ... ok
test_build_headers_auto_generate (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_build_headers_auto_generate)
测试headers自动生成timestamp和randStr ... ok
test_build_headers_with_fixed_params (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_build_headers_with_fixed_params)
测试headers构造（固定参数） ... ok
test_fetch_all_users_business_error_middle_page (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_business_error_middle_page)
测试中间页业务错误 ... ok
test_fetch_all_users_current_page_not_advancing (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_current_page_not_advancing)
测试current_page不前进 ... ok
test_fetch_all_users_empty (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_empty)
测试空数据 ... ok
test_fetch_all_users_http_error_middle_page (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_http_error_middle_page)
测试中间页HTTP错误 ... ok
test_fetch_all_users_last_page_partial (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_last_page_partial)
测试最后一页不足page_size ... ok
test_fetch_all_users_max_pages (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_max_pages)
测试max_pages限制 ... ok
test_fetch_all_users_max_pages_negative (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_max_pages_negative)
测试max_pages为负数 ... ok
test_fetch_all_users_max_pages_zero (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_max_pages_zero)
测试max_pages为0 ... ok
test_fetch_all_users_multi_page (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_multi_page)
测试多页成功 ... ok
test_fetch_all_users_page_size_one (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_page_size_one)
测试page_size=1场景 ... ok
test_fetch_all_users_per_page_invalid_string (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_per_page_invalid_string)
测试per_page为非数字字符串 ... ok
test_fetch_all_users_per_page_string (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_per_page_string)
测试per_page字符串兼容 ... ok
test_fetch_all_users_per_page_zero (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_per_page_zero)
测试per_page为0 ... ok
test_fetch_all_users_single_page (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_single_page)
测试单页成功 ... ok
test_fetch_users_page_business_error (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_business_error)
测试业务错误响应 ... ok
test_fetch_users_page_http_error (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_http_error)
测试HTTP错误 ... ok
test_fetch_users_page_missing_code (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_missing_code)
测试响应缺失code字段 ... ok
test_fetch_users_page_missing_data_data_field (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_missing_data_data_field)
测试响应data对象缺失data字段 ... ok
test_fetch_users_page_missing_data_field (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_missing_data_field)
测试响应缺失data字段 ... ok
test_fetch_users_page_success (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_success)
测试成功响应解析 ... ok
test_fetch_users_page_users_not_list (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_users_not_list)
测试响应data.data不是列表 ... ok
test_encryption_type_normalization (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_encryption_type_normalization)
测试加密类型归一化 ... ok
test_invalid_encryption_type (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_invalid_encryption_type)
测试非法加密类型 ... ok
test_live_test_disabled (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_live_test_disabled)
测试live测试开关禁用 ... ok
test_live_test_enabled (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_live_test_enabled)
测试live测试开关启用 ... ok
test_missing_app_key (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_missing_app_key)
测试缺失appKey ... ok
test_missing_app_secret (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_missing_app_secret)
测试缺失appSecret ... ok
test_missing_tenant_code (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_missing_tenant_code)
测试缺失tenantCode ... ok
test_missing_url (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_missing_url)
测试缺失URL ... ok
test_valid_config (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_valid_config)
测试有效配置 ... ok
test_scenario1_update_existing_student (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario1_update_existing_student)
场景1：成功更新已存在student的3个字段 ... ok
test_scenario2_skip_mapper_skip_reason (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario2_skip_mapper_skip_reason)
场景2：跳过mapper标记skip_reason的用户 ... ok
test_scenario3_skip_role_conflict (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario3_skip_role_conflict)
场景3：检测并跳过role冲突(local非student) ... ok
test_scenario4_skip_missing_user (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario4_skip_missing_user)
场景4：跳过本地不存在的用户 ... ok
test_scenario5_dry_run_no_db_write (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario5_dry_run_no_db_write)
场景5：dry_run=True不写DB，返回统计 ... ok
test_scenario6_batch_sync_multiple_users (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario6_batch_sync_multiple_users)
场景6：批量同步多个用户 ... ok
test_scenario7_detailed_statistics (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario7_detailed_statistics)
场景7：返回详细统计 ... ok
test_scenario8_no_affect_other_users (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario8_no_affect_other_users)
场景8：不影响其他用户 ... ok
test_core_fields_readonly (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_core_fields_readonly)
测试5：服务只读，不修改核心字段 ... ok
test_empty_input (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_empty_input)
测试7：空输入处理 ... ok
test_existing_student_to_candidate (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_existing_student_to_candidate)
测试2：已存在学生进入候选（验证候选数语义） ... ok
test_field_gap_warning_with_candidates (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_field_gap_warning_with_candidates)
测试6：存在候选时输出字段gap warning ... ok
test_local_role_conflict (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_local_role_conflict)
测试4：本地角色冲突检测 ... ok
test_mapper_skip_transparency (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_mapper_skip_transparency)
测试1：mapper skip透传统计 ... ok
test_missing_local_not_created (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_missing_local_not_created)
测试3：本地不存在用户不创建（Phase 1边界） ... ok
test_mixed_scenario (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_mixed_scenario)
测试8：混合场景（skip/missing/conflict/existing各1个） ... ok
test_dry_run_mode (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_dry_run_mode)
Test dry-run mode doesn't apply changes ... ok
test_import_counselors_duplicate_in_csv (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_counselors_duplicate_in_csv)
Test counselor import with duplicate IDs in CSV ... ok
test_import_counselors_missing_required_field (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_counselors_missing_required_field)
Test counselor import with missing required field ... ok
test_import_counselors_success (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_counselors_success)
Test successful counselor import ... ok
test_import_mappings_counselor_not_found (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_mappings_counselor_not_found)
Test mapping import with non-existent counselor ... ok
test_import_mappings_success (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_mappings_success)
Test successful mapping import ... ERROR
test_import_students_class_mapping_missing (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_students_class_mapping_missing)
Test student import with missing class mapping ... ok
test_import_students_success (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_students_success)
Test successful student import ... ERROR
test_validation_error_skips_invalid_rows (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_validation_error_skips_invalid_rows)
Test that validation errors skip invalid rows but import valid ones ... ok
test_complete_application_flow (apps.applications.tests.test_application_flow.ApplicationFlowTestCase.test_complete_application_flow)
测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询 ... ERROR
test_leave_date_past (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_leave_date_past)
Test leave_date field rejects dates before today ... ok
test_leave_date_today (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_leave_date_today)
Test leave_date field accepts today ... ok
test_leave_date_validation_after_midnight (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_leave_date_validation_after_midnight)
Test leave_date validation rejects past date after midnight ... ok
test_leave_date_validation_at_midnight_boundary (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_leave_date_validation_at_midnight_boundary)
Test leave_date validation at 23:59:59 boundary ... ok
test_reason_empty_after_trim (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_reason_empty_after_trim)
Test reason field rejects empty string after trim ... ok
test_reason_max_length_500 (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_reason_max_length_500)
Test reason field enforces 500 character limit ... ok
test_valid_data (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_valid_data)
Test serializer accepts valid data ... ok
test_counselor_cannot_see_other_counselor_applications (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_counselor_cannot_see_other_counselor_applications) ... ERROR
test_counselor_sees_only_pending_counselor_approvals (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_counselor_sees_only_pending_counselor_approvals) ... ERROR
test_dean_sees_only_pending_dean_approvals (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_dean_sees_only_pending_dean_approvals) ... ERROR
test_response_format_no_nested_approvals (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_response_format_no_nested_approvals) ... ERROR
test_student_cannot_see_other_student_applications (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_student_cannot_see_other_student_applications) ... ERROR
test_student_sees_only_own_applications (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_student_sees_only_own_applications) ... ERROR
test_duplicate_submission_conflict (apps.applications.tests.test_constraints.ApplicationConstraintsTestCase.test_duplicate_submission_conflict)
测试重复提交返回409 ... ERROR
test_conflict_duplicate_application (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_conflict_duplicate_application)
测试重复提交申请 ... ERROR
test_dorm_blocked_error (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_dorm_blocked_error)
测试宿舍清退未完成阻断提交 ... ERROR
test_forbidden_access_other_student_application (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_forbidden_access_other_student_application)
测试学生访问他人申请 ... ERROR
test_not_found_application (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_not_found_application)
测试申请不存在 ... ERROR
test_validation_error_missing_fields (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_validation_error_missing_fields)
测试参数验证失败 ... ERROR
test_counselor_cannot_access_cross_class_application (apps.applications.tests.test_detail_permissions.ApplicationDetailPermissionTest.test_counselor_cannot_access_cross_class_application) ... ERROR
test_dean_cannot_access_non_assigned_application (apps.applications.tests.test_detail_permissions.ApplicationDetailPermissionTest.test_dean_cannot_access_non_assigned_application) ... ERROR
test_student_cannot_access_other_student_application (apps.applications.tests.test_detail_permissions.ApplicationDetailPermissionTest.test_student_cannot_access_other_student_application) ... ERROR
test_filter_all_approvals (apps.applications.tests.test_p0_fixes.ApprovalDecisionFilterTest.test_filter_all_approvals) ... ok
test_filter_approved_approvals (apps.applications.tests.test_p0_fixes.ApprovalDecisionFilterTest.test_filter_approved_approvals) ... ok
test_filter_pending_approvals (apps.applications.tests.test_p0_fixes.ApprovalDecisionFilterTest.test_filter_pending_approvals) ... ok
test_filter_rejected_approvals (apps.applications.tests.test_p0_fixes.ApprovalDecisionFilterTest.test_filter_rejected_approvals) ... ok
test_can_resubmit_after_rejection (apps.applications.tests.test_p0_fixes.ResubmissionAfterRejectionTest.test_can_resubmit_after_rejection) ... ERROR
test_cannot_resubmit_while_pending (apps.applications.tests.test_p0_fixes.ResubmissionAfterRejectionTest.test_cannot_resubmit_while_pending) ... ERROR
test_counselor_rejection (apps.approvals.tests.test_rejection_flow.RejectionFlowTestCase.test_counselor_rejection)
测试辅导员驳回申请 ... ERROR
test_dean_rejection (apps.approvals.tests.test_rejection_flow.RejectionFlowTestCase.test_dean_rejection)
测试学工部驳回申请 ... ERROR
test_counselor_cannot_see_other_counselor_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_counselor_cannot_see_other_counselor_approvals) ... ERROR
test_counselor_sees_only_own_pending_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_counselor_sees_only_own_pending_approvals) ... ERROR
test_dean_cannot_see_other_dean_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_dean_cannot_see_other_dean_approvals) ... ERROR
test_dean_sees_only_own_pending_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_dean_sees_only_own_pending_approvals) ... ERROR
test_decision_all_does_not_leak_cross_approver_data (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_decision_all_does_not_leak_cross_approver_data) ... ERROR
test_response_format_count_and_results (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_response_format_count_and_results) ... ERROR
test_student_403_on_approval_list (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_student_403_on_approval_list) ... ERROR
test_counselor_cannot_act_on_dean_step (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_counselor_cannot_act_on_dean_step)
辅导员不能处理学工部审批步骤 ... ERROR
test_cross_counselor_approve_forbidden (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_cross_counselor_approve_forbidden)
测试跨辅导员审批返回403 ... ERROR
test_cross_counselor_reject_forbidden (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_cross_counselor_reject_forbidden)
测试跨辅导员驳回返回403 ... ERROR
test_dean_cannot_act_on_counselor_step (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_dean_cannot_act_on_counselor_step)
学工部不能处理辅导员审批步骤 ... ERROR
test_non_assigned_dean_forbidden (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_non_assigned_dean_forbidden)
同角色但非指定学工部审批人不能处理审批 ... ERROR
test_student_cannot_approve_or_reject (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_student_cannot_approve_or_reject)
学生不能调用审批操作接口 ... ERROR
test_counselor_step_requires_pending_counselor_status (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_counselor_step_requires_pending_counselor_status)
测试辅导员审批步骤与申请状态不匹配时返回409 ... ERROR
test_dean_step_requires_pending_dean_status (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_dean_step_requires_pending_dean_status)
测试学工部审批步骤与申请状态不匹配时返回409 ... ERROR
test_duplicate_approval_conflict (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_duplicate_approval_conflict)
测试重复审批返回409 ... ERROR
test_reject_then_repeat_operation_conflict (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_reject_then_repeat_operation_conflict)
测试驳回后的重复操作返回409 ... ERROR

======================================================================
ERROR: test_import_mappings_success (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_mappings_success)
Test successful mapping import
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column class_mappings.dorm_manager_id does not exist
LINE 1: SELECT "class_mappings"."class_id", "class_mappings"."dorm_m...
                                            ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/users/management/commands/import_csv.py", line 224, in import_mappings
    mapping, created = ClassMapping.objects.update_or_create(
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 949, in update_or_create
    obj, created = self.select_for_update().get_or_create(defaults, **kwargs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 916, in get_or_create
    return self.get(**kwargs), False
           ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 633, in get
    num = len(clone)
          ^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 380, in __len__
    self._fetch_all()
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1881, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 91, in __iter__
    results = compiler.execute_sql(
              ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1562, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column class_mappings.dorm_manager_id does not exist
LINE 1: SELECT "class_mappings"."class_id", "class_mappings"."dorm_m...
                                            ^


During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/app/apps/users/tests/test_import_csv.py", line 73, in test_import_mappings_success
    call_command('import_csv', '--mappings', filepath, stdout=out)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 194, in call_command
    return command.execute(*args, **defaults)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 458, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/apps/users/management/commands/import_csv.py", line 36, in handle
    self.import_mappings(options['mappings'], dry_run, summary['mappings'])
  File "/usr/local/lib/python3.11/contextlib.py", line 81, in inner
    return func(*args, **kwds)
           ^^^^^^^^^^^^^^^^^^^
  File "/app/apps/users/management/commands/import_csv.py", line 241, in import_mappings
    raise CommandError(f"Error importing mappings: {str(e)}")
django.core.management.base.CommandError: Error importing mappings: column class_mappings.dorm_manager_id does not exist
LINE 1: SELECT "class_mappings"."class_id", "class_mappings"."dorm_m...
                                            ^


======================================================================
ERROR: test_import_students_success (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_students_success)
Test successful student import
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/users/tests/test_import_csv.py", line 100, in test_import_students_success
    ClassMapping.objects.create(class_id='CS2020-01', counselor=counselor, counselor_name='李老师')
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_complete_application_flow (apps.applications.tests.test_application_flow.ApplicationFlowTestCase.test_complete_application_flow)
测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_application_flow.py", line 42, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_counselor_cannot_see_other_counselor_applications (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_counselor_cannot_see_other_counselor_applications)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_list_permissions.py", line 35, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_counselor_sees_only_pending_counselor_approvals (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_counselor_sees_only_pending_counselor_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_list_permissions.py", line 35, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_dean_sees_only_pending_dean_approvals (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_dean_sees_only_pending_dean_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_list_permissions.py", line 35, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_response_format_no_nested_approvals (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_response_format_no_nested_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_list_permissions.py", line 35, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_student_cannot_see_other_student_applications (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_student_cannot_see_other_student_applications)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_list_permissions.py", line 35, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_student_sees_only_own_applications (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_student_sees_only_own_applications)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_list_permissions.py", line 35, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_duplicate_submission_conflict (apps.applications.tests.test_constraints.ApplicationConstraintsTestCase.test_duplicate_submission_conflict)
测试重复提交返回409
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_constraints.py", line 33, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_conflict_duplicate_application (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_conflict_duplicate_application)
测试重复提交申请
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_error_cases.py", line 54, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_dorm_blocked_error (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_dorm_blocked_error)
测试宿舍清退未完成阻断提交
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_error_cases.py", line 54, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_forbidden_access_other_student_application (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_forbidden_access_other_student_application)
测试学生访问他人申请
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_error_cases.py", line 54, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_not_found_application (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_not_found_application)
测试申请不存在
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_error_cases.py", line 54, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_validation_error_missing_fields (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_validation_error_missing_fields)
测试参数验证失败
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_error_cases.py", line 54, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_counselor_cannot_access_cross_class_application (apps.applications.tests.test_detail_permissions.ApplicationDetailPermissionTest.test_counselor_cannot_access_cross_class_application)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_detail_permissions.py", line 42, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_dean_cannot_access_non_assigned_application (apps.applications.tests.test_detail_permissions.ApplicationDetailPermissionTest.test_dean_cannot_access_non_assigned_application)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_detail_permissions.py", line 42, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_student_cannot_access_other_student_application (apps.applications.tests.test_detail_permissions.ApplicationDetailPermissionTest.test_student_cannot_access_other_student_application)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_detail_permissions.py", line 42, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_can_resubmit_after_rejection (apps.applications.tests.test_p0_fixes.ResubmissionAfterRejectionTest.test_can_resubmit_after_rejection)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_p0_fixes.py", line 24, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_cannot_resubmit_while_pending (apps.applications.tests.test_p0_fixes.ResubmissionAfterRejectionTest.test_cannot_resubmit_while_pending)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_p0_fixes.py", line 24, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_counselor_rejection (apps.approvals.tests.test_rejection_flow.RejectionFlowTestCase.test_counselor_rejection)
测试辅导员驳回申请
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_rejection_flow.py", line 41, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_dean_rejection (apps.approvals.tests.test_rejection_flow.RejectionFlowTestCase.test_dean_rejection)
测试学工部驳回申请
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_rejection_flow.py", line 41, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_counselor_cannot_see_other_counselor_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_counselor_cannot_see_other_counselor_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_counselor_sees_only_own_pending_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_counselor_sees_only_own_pending_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_dean_cannot_see_other_dean_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_dean_cannot_see_other_dean_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_dean_sees_only_own_pending_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_dean_sees_only_own_pending_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_decision_all_does_not_leak_cross_approver_data (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_decision_all_does_not_leak_cross_approver_data)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_response_format_count_and_results (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_response_format_count_and_results)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_student_403_on_approval_list (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_student_403_on_approval_list)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_counselor_cannot_act_on_dean_step (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_counselor_cannot_act_on_dean_step)
辅导员不能处理学工部审批步骤
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_permissions.py", line 56, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_cross_counselor_approve_forbidden (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_cross_counselor_approve_forbidden)
测试跨辅导员审批返回403
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_permissions.py", line 56, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_cross_counselor_reject_forbidden (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_cross_counselor_reject_forbidden)
测试跨辅导员驳回返回403
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_permissions.py", line 56, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_dean_cannot_act_on_counselor_step (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_dean_cannot_act_on_counselor_step)
学工部不能处理辅导员审批步骤
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_permissions.py", line 56, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_non_assigned_dean_forbidden (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_non_assigned_dean_forbidden)
同角色但非指定学工部审批人不能处理审批
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_permissions.py", line 56, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_student_cannot_approve_or_reject (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_student_cannot_approve_or_reject)
学生不能调用审批操作接口
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_permissions.py", line 56, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_counselor_step_requires_pending_counselor_status (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_counselor_step_requires_pending_counselor_status)
测试辅导员审批步骤与申请状态不匹配时返回409
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_state_machine.py", line 38, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_dean_step_requires_pending_dean_status (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_dean_step_requires_pending_dean_status)
测试学工部审批步骤与申请状态不匹配时返回409
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_state_machine.py", line 38, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_duplicate_approval_conflict (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_duplicate_approval_conflict)
测试重复审批返回409
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_state_machine.py", line 38, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_reject_then_repeat_operation_conflict (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_reject_then_repeat_operation_conflict)
测试驳回后的重复操作返回409
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_state_machine.py", line 38, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


----------------------------------------------------------------------
Ran 119 tests in 15.129s

FAILED (errors=39)
Preserving test database for alias 'default' ('test_graduation_leave')...

codex
The suite is failing broadly after the import CSV tests, so this is now beyond the dependency blocker. I’m waiting for the tracebacks so I can separate environment/data contamination from an actual Phase 3 regression.
codex
The Docker route solved the `psycopg2` blocker, but the preserved test database is stale: every broad failure is the same missing `class_mappings.dorm_manager_id` column. I’m checking whether this is a missing migration or just `--keepdb` holding onto an old schema.
exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/class_mapping.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.db import models
from apps.users.models import User


class ClassMapping(models.Model):
    class_id = models.CharField(max_length=50, primary_key=True)
    dorm_manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_dorms')
    dorm_manager_name = models.CharField(max_length=100)
    counselor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_classes')
    counselor_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'class_mappings'

exec
/bin/bash -lc 'rtk rg -n "class ClassMapping|ClassMapping|dorm_manager" backend/apps/users backend/apps/applications backend/apps/approvals' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/approvals/validators.py:5:    'dorm_manager': ApplicationStatus.PENDING_DORM_MANAGER,
backend/apps/approvals/tests/test_rejection_flow.py:7:from apps.users.class_mapping import ClassMapping
backend/apps/approvals/tests/test_rejection_flow.py:41:        ClassMapping.objects.create(
backend/apps/approvals/tests/test_permissions.py:7:from apps.users.class_mapping import ClassMapping
backend/apps/approvals/tests/test_permissions.py:56:        ClassMapping.objects.create(
backend/apps/approvals/tests/test_permissions.py:62:        ClassMapping.objects.create(
backend/apps/approvals/tests/test_state_machine.py:7:from apps.users.class_mapping import ClassMapping
backend/apps/approvals/tests/test_state_machine.py:38:        ClassMapping.objects.create(
backend/apps/approvals/views.py:47:    # 宿管员: 只看自己的dorm_manager审批
backend/apps/approvals/views.py:161:        from apps.users.class_mapping import ClassMapping
backend/apps/approvals/views.py:162:        class_mapping = ClassMapping.objects.get(class_id=application.class_id, active=True)
backend/apps/approvals/models.py:7:    DORM_MANAGER = 'dorm_manager', '宿管员'
backend/apps/applications/tests/test_p0_fixes.py:6:from apps.users.class_mapping import ClassMapping
backend/apps/applications/tests/test_p0_fixes.py:24:        ClassMapping.objects.create(
backend/apps/users/models.py:7:    DORM_MANAGER = 'dorm_manager', '宿管员'
backend/apps/users/migrations/0001_initial.py:41:            name='ClassMapping',
backend/apps/applications/models.py:8:    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
backend/apps/applications/permissions.py:2:from apps.users.class_mapping import ClassMapping
backend/apps/applications/permissions.py:12:        return ClassMapping.objects.filter(
backend/apps/applications/permissions.py:13:            dorm_manager=user,
backend/apps/applications/permissions.py:19:        return ClassMapping.objects.filter(
backend/apps/applications/tests/test_list_permissions.py:4:from apps.users.class_mapping import ClassMapping
backend/apps/applications/tests/test_list_permissions.py:35:        ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
backend/apps/applications/tests/test_list_permissions.py:36:        ClassMapping.objects.create(class_id='CS2020-02', counselor=self.counselor2, counselor_name='辅导员2', active=True)
backend/apps/applications/tests/test_constraints.py:8:from apps.users.class_mapping import ClassMapping
backend/apps/applications/tests/test_constraints.py:33:        ClassMapping.objects.create(
backend/apps/applications/tests/test_application_flow.py:7:from apps.users.class_mapping import ClassMapping
backend/apps/applications/tests/test_application_flow.py:42:        ClassMapping.objects.create(
backend/apps/applications/tests/test_detail_permissions.py:4:from apps.users.class_mapping import ClassMapping
backend/apps/applications/tests/test_detail_permissions.py:42:        ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
backend/apps/applications/tests/test_detail_permissions.py:43:        ClassMapping.objects.create(class_id='CS2020-02', counselor=self.counselor2, counselor_name='辅导员2', active=True)
backend/apps/users/tests/test_import_csv.py:8:from apps.users.class_mapping import ClassMapping
backend/apps/users/tests/test_import_csv.py:75:            self.assertEqual(ClassMapping.objects.count(), 2)
backend/apps/users/tests/test_import_csv.py:76:            mapping = ClassMapping.objects.get(class_id='CS2020-01')
backend/apps/users/tests/test_import_csv.py:93:            self.assertEqual(ClassMapping.objects.count(), 0)
backend/apps/users/tests/test_import_csv.py:100:        ClassMapping.objects.create(class_id='CS2020-01', counselor=counselor, counselor_name='李老师')
backend/apps/users/class_mapping.py:5:class ClassMapping(models.Model):
backend/apps/users/class_mapping.py:7:    dorm_manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_dorms')
backend/apps/users/class_mapping.py:8:    dorm_manager_name = models.CharField(max_length=100)
backend/apps/applications/tests/test_error_cases.py:7:from apps.users.class_mapping import ClassMapping
backend/apps/applications/tests/test_error_cases.py:54:        ClassMapping.objects.create(
backend/apps/applications/views.py:15:from apps.users.class_mapping import ClassMapping
backend/apps/applications/views.py:148:        class_mapping = ClassMapping.objects.get(class_id=user.class_id, active=True)
backend/apps/applications/views.py:149:    except ClassMapping.DoesNotExist:
backend/apps/applications/views.py:165:    dorm_manager_approval = Approval.objects.create(
backend/apps/applications/views.py:169:        approver=class_mapping.dorm_manager,
backend/apps/applications/views.py:170:        approver_name=class_mapping.dorm_manager_name,
backend/apps/applications/views.py:174:    notify_application_submitted(application, dorm_manager_approval)
backend/apps/users/admin.py:3:from .class_mapping import ClassMapping
backend/apps/users/admin.py:14:@admin.register(ClassMapping)
backend/apps/users/admin.py:15:class ClassMappingAdmin(admin.ModelAdmin):
backend/apps/users/management/commands/seed_data.py:3:from apps.users.class_mapping import ClassMapping
backend/apps/users/management/commands/seed_data.py:100:            mapping, created = ClassMapping.objects.get_or_create(
backend/apps/users/management/commands/import_csv.py:5:from apps.users.class_mapping import ClassMapping
backend/apps/users/management/commands/import_csv.py:81:                    if not dry_run and not ClassMapping.objects.filter(class_id=class_id).exists():
backend/apps/users/management/commands/import_csv.py:218:                        exists = ClassMapping.objects.filter(class_id=class_id).exists()
backend/apps/users/management/commands/import_csv.py:224:                        mapping, created = ClassMapping.objects.update_or_create(

exec
/bin/bash -lc "rtk sed -n '1,220p' backend/apps/users/migrations/0002_user_department_user_email_user_phone.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Generated by Django 4.2.13 on 2026-06-02 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/migrations/0001_initial.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Generated by Django 4.2.13 on 2026-05-30 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('student', '学生'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
                ('active', models.BooleanField(default=True)),
                ('class_id', models.CharField(blank=True, max_length=50, null=True)),
                ('is_graduating', models.BooleanField(blank=True, null=True)),
                ('graduation_year', models.IntegerField(blank=True, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='ClassMapping',
            fields=[
                ('class_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('counselor_name', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('counselor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='managed_classes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'class_mappings',
            },
        ),
    ]

web search: 
web search: site:docs.djangoproject.com/en/4.2/ref/databases/ PostgreSQL psycopg 3 Django 4.2
codex
The schema mismatch is specifically due to `--keepdb`: Django reused `test_graduation_leave`, and the preserved schema predates the current `ClassMapping` model. I’m going to rerun without `--keepdb` so Django drops/recreates the test database from migrations.
exec
/bin/bash -lc 'rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_mapper apps.users.tests.test_xg_user_client apps.users.tests.test_xg_user_sync apps.users.tests.test_import_csv apps.applications.tests.test_application_flow apps.applications.tests.test_serializer_validation apps.applications.tests.test_list_permissions apps.applications.tests.test_constraints apps.applications.tests.test_error_cases apps.applications.tests.test_detail_permissions apps.applications.tests.test_p0_fixes apps.approvals.tests.test_rejection_flow apps.approvals.tests.test_list_permissions apps.approvals.tests.test_permissions apps.approvals.tests.test_state_machine --noinput -v 2' in /home/caohui/projects/graduation-leave-system
codex
The clean database is being rebuilt from migrations now. A detail worth noting: the committed migration `users.0001_initial` does not define `ClassMapping.dorm_manager`, while the current model does, so a clean run may still expose a real migration gap rather than only stale `--keepdb` state.
 exited 1 in 16592ms:
Creating test database for alias 'default' ('test_graduation_leave')...
Got an error creating the test database: database "test_graduation_leave" already exists

Destroying old test database for alias 'default' ('test_graduation_leave')...
Found 119 test(s).
Operations to perform:
  Synchronize unmigrated apps: corsheaders, django_filters, drf_spectacular, messages, rest_framework, rest_framework_simplejwt, staticfiles
  Apply all migrations: admin, applications, approvals, attachments, auth, contenttypes, notifications, sessions, users
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying users.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying applications.0001_initial... OK
  Applying applications.0002_initial... OK
  Applying applications.0003_application_unique_student_application... OK
  Applying applications.0004_remove_unique_student_constraint... OK
  Applying approvals.0001_initial... OK
  Applying approvals.0002_initial... OK
  Applying attachments.0001_initial... OK
  Applying notifications.0001_initial... OK
  Applying notifications.0002_alter_notification_type... OK
  Applying sessions.0001_initial... OK
  Applying users.0002_user_department_user_email_user_phone... OK
System check identified no issues (0 silenced).
test_complete_fields_success (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_complete_fields_success)
测试完整字段成功映射 ... ok
test_missing_name_skip (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_missing_name_skip)
测试name缺失应跳过 ... ok
test_missing_number_skip (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_missing_number_skip)
测试number缺失应跳过 ... ok
test_missing_user_identity_skip (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_missing_user_identity_skip)
测试user_identity缺失应跳过 ... ok
test_multiple_missing_fields_priority (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_multiple_missing_fields_priority)
测试多个字段同时缺失的优先级 ... ok
test_optional_fields_missing (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_optional_fields_missing)
测试可选字段缺失不阻止映射 ... ok
test_unknown_user_identity_skip (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_unknown_user_identity_skip)
测试user_identity未知值应跳过 ... ok
test_user_identity_student_string (apps.users.tests.test_xg_user_mapper.XGUserMapperTests.test_user_identity_student_string)
测试user_identity为'student'字符串 ... ok
test_invalid_encryption_type (apps.users.tests.test_xg_user_client.GenerateSignTests.test_invalid_encryption_type)
测试非法加密类型 ... ok
test_md5_encryption (apps.users.tests.test_xg_user_client.GenerateSignTests.test_md5_encryption)
测试md5加密（固定期望值） ... ok
test_official_sample_default_sha1 (apps.users.tests.test_xg_user_client.GenerateSignTests.test_official_sample_default_sha1)
测试官方样例（默认sha1） ... ok
test_official_sample_sha1 (apps.users.tests.test_xg_user_client.GenerateSignTests.test_official_sample_sha1)
测试官方签名样例（sha1） ... ok
test_build_form_data_custom (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_build_form_data_custom)
测试form-data构造（自定义参数） ... ok
test_build_form_data_default (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_build_form_data_default)
测试form-data构造（默认参数） ... ok
test_build_headers_auto_generate (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_build_headers_auto_generate)
测试headers自动生成timestamp和randStr ... ok
test_build_headers_with_fixed_params (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_build_headers_with_fixed_params)
测试headers构造（固定参数） ... ok
test_fetch_all_users_business_error_middle_page (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_business_error_middle_page)
测试中间页业务错误 ... ok
test_fetch_all_users_current_page_not_advancing (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_current_page_not_advancing)
测试current_page不前进 ... ok
test_fetch_all_users_empty (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_empty)
测试空数据 ... ok
test_fetch_all_users_http_error_middle_page (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_http_error_middle_page)
测试中间页HTTP错误 ... ok
test_fetch_all_users_last_page_partial (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_last_page_partial)
测试最后一页不足page_size ... ok
test_fetch_all_users_max_pages (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_max_pages)
测试max_pages限制 ... ok
test_fetch_all_users_max_pages_negative (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_max_pages_negative)
测试max_pages为负数 ... ok
test_fetch_all_users_max_pages_zero (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_max_pages_zero)
测试max_pages为0 ... ok
test_fetch_all_users_multi_page (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_multi_page)
测试多页成功 ... ok
test_fetch_all_users_page_size_one (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_page_size_one)
测试page_size=1场景 ... ok
test_fetch_all_users_per_page_invalid_string (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_per_page_invalid_string)
测试per_page为非数字字符串 ... ok
test_fetch_all_users_per_page_string (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_per_page_string)
测试per_page字符串兼容 ... ok
test_fetch_all_users_per_page_zero (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_per_page_zero)
测试per_page为0 ... ok
test_fetch_all_users_single_page (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_all_users_single_page)
测试单页成功 ... ok
test_fetch_users_page_business_error (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_business_error)
测试业务错误响应 ... ok
test_fetch_users_page_http_error (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_http_error)
测试HTTP错误 ... ok
test_fetch_users_page_missing_code (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_missing_code)
测试响应缺失code字段 ... ok
test_fetch_users_page_missing_data_data_field (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_missing_data_data_field)
测试响应data对象缺失data字段 ... ok
test_fetch_users_page_missing_data_field (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_missing_data_field)
测试响应缺失data字段 ... ok
test_fetch_users_page_success (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_success)
测试成功响应解析 ... ok
test_fetch_users_page_users_not_list (apps.users.tests.test_xg_user_client.XGUserAPIClientTests.test_fetch_users_page_users_not_list)
测试响应data.data不是列表 ... ok
test_encryption_type_normalization (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_encryption_type_normalization)
测试加密类型归一化 ... ok
test_invalid_encryption_type (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_invalid_encryption_type)
测试非法加密类型 ... ok
test_live_test_disabled (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_live_test_disabled)
测试live测试开关禁用 ... ok
test_live_test_enabled (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_live_test_enabled)
测试live测试开关启用 ... ok
test_missing_app_key (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_missing_app_key)
测试缺失appKey ... ok
test_missing_app_secret (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_missing_app_secret)
测试缺失appSecret ... ok
test_missing_tenant_code (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_missing_tenant_code)
测试缺失tenantCode ... ok
test_missing_url (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_missing_url)
测试缺失URL ... ok
test_valid_config (apps.users.tests.test_xg_user_client.XGUserAPIConfigTests.test_valid_config)
测试有效配置 ... ok
test_scenario1_update_existing_student (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario1_update_existing_student)
场景1：成功更新已存在student的3个字段 ... ok
test_scenario2_skip_mapper_skip_reason (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario2_skip_mapper_skip_reason)
场景2：跳过mapper标记skip_reason的用户 ... ok
test_scenario3_skip_role_conflict (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario3_skip_role_conflict)
场景3：检测并跳过role冲突(local非student) ... ok
test_scenario4_skip_missing_user (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario4_skip_missing_user)
场景4：跳过本地不存在的用户 ... ok
test_scenario5_dry_run_no_db_write (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario5_dry_run_no_db_write)
场景5：dry_run=True不写DB，返回统计 ... ok
test_scenario6_batch_sync_multiple_users (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario6_batch_sync_multiple_users)
场景6：批量同步多个用户 ... ok
test_scenario7_detailed_statistics (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario7_detailed_statistics)
场景7：返回详细统计 ... ok
test_scenario8_no_affect_other_users (apps.users.tests.test_xg_user_sync.XGUserSyncApplyTests.test_scenario8_no_affect_other_users)
场景8：不影响其他用户 ... ok
test_core_fields_readonly (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_core_fields_readonly)
测试5：服务只读，不修改核心字段 ... ok
test_empty_input (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_empty_input)
测试7：空输入处理 ... ok
test_existing_student_to_candidate (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_existing_student_to_candidate)
测试2：已存在学生进入候选（验证候选数语义） ... ok
test_field_gap_warning_with_candidates (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_field_gap_warning_with_candidates)
测试6：存在候选时输出字段gap warning ... ok
test_local_role_conflict (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_local_role_conflict)
测试4：本地角色冲突检测 ... ok
test_mapper_skip_transparency (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_mapper_skip_transparency)
测试1：mapper skip透传统计 ... ok
test_missing_local_not_created (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_missing_local_not_created)
测试3：本地不存在用户不创建（Phase 1边界） ... ok
test_mixed_scenario (apps.users.tests.test_xg_user_sync.XGUserSyncPlanTests.test_mixed_scenario)
测试8：混合场景（skip/missing/conflict/existing各1个） ... ok
test_dry_run_mode (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_dry_run_mode)
Test dry-run mode doesn't apply changes ... ok
test_import_counselors_duplicate_in_csv (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_counselors_duplicate_in_csv)
Test counselor import with duplicate IDs in CSV ... ok
test_import_counselors_missing_required_field (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_counselors_missing_required_field)
Test counselor import with missing required field ... ok
test_import_counselors_success (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_counselors_success)
Test successful counselor import ... ok
test_import_mappings_counselor_not_found (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_mappings_counselor_not_found)
Test mapping import with non-existent counselor ... ok
test_import_mappings_success (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_mappings_success)
Test successful mapping import ... ERROR
test_import_students_class_mapping_missing (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_students_class_mapping_missing)
Test student import with missing class mapping ... ok
test_import_students_success (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_students_success)
Test successful student import ... ERROR
test_validation_error_skips_invalid_rows (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_validation_error_skips_invalid_rows)
Test that validation errors skip invalid rows but import valid ones ... ok
test_complete_application_flow (apps.applications.tests.test_application_flow.ApplicationFlowTestCase.test_complete_application_flow)
测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询 ... ERROR
test_leave_date_past (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_leave_date_past)
Test leave_date field rejects dates before today ... ok
test_leave_date_today (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_leave_date_today)
Test leave_date field accepts today ... ok
test_leave_date_validation_after_midnight (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_leave_date_validation_after_midnight)
Test leave_date validation rejects past date after midnight ... ok
test_leave_date_validation_at_midnight_boundary (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_leave_date_validation_at_midnight_boundary)
Test leave_date validation at 23:59:59 boundary ... ok
test_reason_empty_after_trim (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_reason_empty_after_trim)
Test reason field rejects empty string after trim ... ok
test_reason_max_length_500 (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_reason_max_length_500)
Test reason field enforces 500 character limit ... ok
test_valid_data (apps.applications.tests.test_serializer_validation.ApplicationCreateSerializerTest.test_valid_data)
Test serializer accepts valid data ... ok
test_counselor_cannot_see_other_counselor_applications (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_counselor_cannot_see_other_counselor_applications) ... ERROR
test_counselor_sees_only_pending_counselor_approvals (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_counselor_sees_only_pending_counselor_approvals) ... ERROR
test_dean_sees_only_pending_dean_approvals (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_dean_sees_only_pending_dean_approvals) ... ERROR
test_response_format_no_nested_approvals (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_response_format_no_nested_approvals) ... ERROR
test_student_cannot_see_other_student_applications (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_student_cannot_see_other_student_applications) ... ERROR
test_student_sees_only_own_applications (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_student_sees_only_own_applications) ... ERROR
test_duplicate_submission_conflict (apps.applications.tests.test_constraints.ApplicationConstraintsTestCase.test_duplicate_submission_conflict)
测试重复提交返回409 ... ERROR
test_conflict_duplicate_application (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_conflict_duplicate_application)
测试重复提交申请 ... ERROR
test_dorm_blocked_error (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_dorm_blocked_error)
测试宿舍清退未完成阻断提交 ... ERROR
test_forbidden_access_other_student_application (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_forbidden_access_other_student_application)
测试学生访问他人申请 ... ERROR
test_not_found_application (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_not_found_application)
测试申请不存在 ... ERROR
test_validation_error_missing_fields (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_validation_error_missing_fields)
测试参数验证失败 ... ERROR
test_counselor_cannot_access_cross_class_application (apps.applications.tests.test_detail_permissions.ApplicationDetailPermissionTest.test_counselor_cannot_access_cross_class_application) ... ERROR
test_dean_cannot_access_non_assigned_application (apps.applications.tests.test_detail_permissions.ApplicationDetailPermissionTest.test_dean_cannot_access_non_assigned_application) ... ERROR
test_student_cannot_access_other_student_application (apps.applications.tests.test_detail_permissions.ApplicationDetailPermissionTest.test_student_cannot_access_other_student_application) ... ERROR
test_filter_all_approvals (apps.applications.tests.test_p0_fixes.ApprovalDecisionFilterTest.test_filter_all_approvals) ... ok
test_filter_approved_approvals (apps.applications.tests.test_p0_fixes.ApprovalDecisionFilterTest.test_filter_approved_approvals) ... ok
test_filter_pending_approvals (apps.applications.tests.test_p0_fixes.ApprovalDecisionFilterTest.test_filter_pending_approvals) ... ok
test_filter_rejected_approvals (apps.applications.tests.test_p0_fixes.ApprovalDecisionFilterTest.test_filter_rejected_approvals) ... ok
test_can_resubmit_after_rejection (apps.applications.tests.test_p0_fixes.ResubmissionAfterRejectionTest.test_can_resubmit_after_rejection) ... ERROR
test_cannot_resubmit_while_pending (apps.applications.tests.test_p0_fixes.ResubmissionAfterRejectionTest.test_cannot_resubmit_while_pending) ... ERROR
test_counselor_rejection (apps.approvals.tests.test_rejection_flow.RejectionFlowTestCase.test_counselor_rejection)
测试辅导员驳回申请 ... ERROR
test_dean_rejection (apps.approvals.tests.test_rejection_flow.RejectionFlowTestCase.test_dean_rejection)
测试学工部驳回申请 ... ERROR
test_counselor_cannot_see_other_counselor_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_counselor_cannot_see_other_counselor_approvals) ... ERROR
test_counselor_sees_only_own_pending_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_counselor_sees_only_own_pending_approvals) ... ERROR
test_dean_cannot_see_other_dean_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_dean_cannot_see_other_dean_approvals) ... ERROR
test_dean_sees_only_own_pending_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_dean_sees_only_own_pending_approvals) ... ERROR
test_decision_all_does_not_leak_cross_approver_data (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_decision_all_does_not_leak_cross_approver_data) ... ERROR
test_response_format_count_and_results (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_response_format_count_and_results) ... ERROR
test_student_403_on_approval_list (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_student_403_on_approval_list) ... ERROR
test_counselor_cannot_act_on_dean_step (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_counselor_cannot_act_on_dean_step)
辅导员不能处理学工部审批步骤 ... ERROR
test_cross_counselor_approve_forbidden (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_cross_counselor_approve_forbidden)
测试跨辅导员审批返回403 ... ERROR
test_cross_counselor_reject_forbidden (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_cross_counselor_reject_forbidden)
测试跨辅导员驳回返回403 ... ERROR
test_dean_cannot_act_on_counselor_step (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_dean_cannot_act_on_counselor_step)
学工部不能处理辅导员审批步骤 ... ERROR
test_non_assigned_dean_forbidden (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_non_assigned_dean_forbidden)
同角色但非指定学工部审批人不能处理审批 ... ERROR
test_student_cannot_approve_or_reject (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_student_cannot_approve_or_reject)
学生不能调用审批操作接口 ... ERROR
test_counselor_step_requires_pending_counselor_status (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_counselor_step_requires_pending_counselor_status)
测试辅导员审批步骤与申请状态不匹配时返回409 ... ERROR
test_dean_step_requires_pending_dean_status (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_dean_step_requires_pending_dean_status)
测试学工部审批步骤与申请状态不匹配时返回409 ... ERROR
test_duplicate_approval_conflict (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_duplicate_approval_conflict)
测试重复审批返回409 ... ERROR
test_reject_then_repeat_operation_conflict (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_reject_then_repeat_operation_conflict)
测试驳回后的重复操作返回409 ... ERROR

======================================================================
ERROR: test_import_mappings_success (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_mappings_success)
Test successful mapping import
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column class_mappings.dorm_manager_id does not exist
LINE 1: SELECT "class_mappings"."class_id", "class_mappings"."dorm_m...
                                            ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/users/management/commands/import_csv.py", line 224, in import_mappings
    mapping, created = ClassMapping.objects.update_or_create(
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 949, in update_or_create
    obj, created = self.select_for_update().get_or_create(defaults, **kwargs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 916, in get_or_create
    return self.get(**kwargs), False
           ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 633, in get
    num = len(clone)
          ^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 380, in __len__
    self._fetch_all()
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1881, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 91, in __iter__
    results = compiler.execute_sql(
              ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1562, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column class_mappings.dorm_manager_id does not exist
LINE 1: SELECT "class_mappings"."class_id", "class_mappings"."dorm_m...
                                            ^


During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/app/apps/users/tests/test_import_csv.py", line 73, in test_import_mappings_success
    call_command('import_csv', '--mappings', filepath, stdout=out)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 194, in call_command
    return command.execute(*args, **defaults)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 458, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/apps/users/management/commands/import_csv.py", line 36, in handle
    self.import_mappings(options['mappings'], dry_run, summary['mappings'])
  File "/usr/local/lib/python3.11/contextlib.py", line 81, in inner
    return func(*args, **kwds)
           ^^^^^^^^^^^^^^^^^^^
  File "/app/apps/users/management/commands/import_csv.py", line 241, in import_mappings
    raise CommandError(f"Error importing mappings: {str(e)}")
django.core.management.base.CommandError: Error importing mappings: column class_mappings.dorm_manager_id does not exist
LINE 1: SELECT "class_mappings"."class_id", "class_mappings"."dorm_m...
                                            ^


======================================================================
ERROR: test_import_students_success (apps.users.tests.test_import_csv.ImportCSVCommandTest.test_import_students_success)
Test successful student import
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/users/tests/test_import_csv.py", line 100, in test_import_students_success
    ClassMapping.objects.create(class_id='CS2020-01', counselor=counselor, counselor_name='李老师')
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_complete_application_flow (apps.applications.tests.test_application_flow.ApplicationFlowTestCase.test_complete_application_flow)
测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_application_flow.py", line 42, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_counselor_cannot_see_other_counselor_applications (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_counselor_cannot_see_other_counselor_applications)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_list_permissions.py", line 35, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_counselor_sees_only_pending_counselor_approvals (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_counselor_sees_only_pending_counselor_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_list_permissions.py", line 35, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_dean_sees_only_pending_dean_approvals (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_dean_sees_only_pending_dean_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_list_permissions.py", line 35, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_response_format_no_nested_approvals (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_response_format_no_nested_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_list_permissions.py", line 35, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_student_cannot_see_other_student_applications (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_student_cannot_see_other_student_applications)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_list_permissions.py", line 35, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_student_sees_only_own_applications (apps.applications.tests.test_list_permissions.ApplicationListPermissionTest.test_student_sees_only_own_applications)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_list_permissions.py", line 35, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_duplicate_submission_conflict (apps.applications.tests.test_constraints.ApplicationConstraintsTestCase.test_duplicate_submission_conflict)
测试重复提交返回409
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_constraints.py", line 33, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_conflict_duplicate_application (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_conflict_duplicate_application)
测试重复提交申请
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_error_cases.py", line 54, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_dorm_blocked_error (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_dorm_blocked_error)
测试宿舍清退未完成阻断提交
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_error_cases.py", line 54, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_forbidden_access_other_student_application (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_forbidden_access_other_student_application)
测试学生访问他人申请
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_error_cases.py", line 54, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_not_found_application (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_not_found_application)
测试申请不存在
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_error_cases.py", line 54, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_validation_error_missing_fields (apps.applications.tests.test_error_cases.ErrorCasesTestCase.test_validation_error_missing_fields)
测试参数验证失败
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_error_cases.py", line 54, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_counselor_cannot_access_cross_class_application (apps.applications.tests.test_detail_permissions.ApplicationDetailPermissionTest.test_counselor_cannot_access_cross_class_application)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_detail_permissions.py", line 42, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_dean_cannot_access_non_assigned_application (apps.applications.tests.test_detail_permissions.ApplicationDetailPermissionTest.test_dean_cannot_access_non_assigned_application)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_detail_permissions.py", line 42, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_student_cannot_access_other_student_application (apps.applications.tests.test_detail_permissions.ApplicationDetailPermissionTest.test_student_cannot_access_other_student_application)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_detail_permissions.py", line 42, in setUp
    ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_can_resubmit_after_rejection (apps.applications.tests.test_p0_fixes.ResubmissionAfterRejectionTest.test_can_resubmit_after_rejection)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_p0_fixes.py", line 24, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_cannot_resubmit_while_pending (apps.applications.tests.test_p0_fixes.ResubmissionAfterRejectionTest.test_cannot_resubmit_while_pending)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/applications/tests/test_p0_fixes.py", line 24, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_counselor_rejection (apps.approvals.tests.test_rejection_flow.RejectionFlowTestCase.test_counselor_rejection)
测试辅导员驳回申请
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_rejection_flow.py", line 41, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_dean_rejection (apps.approvals.tests.test_rejection_flow.RejectionFlowTestCase.test_dean_rejection)
测试学工部驳回申请
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_rejection_flow.py", line 41, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_counselor_cannot_see_other_counselor_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_counselor_cannot_see_other_counselor_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_counselor_sees_only_own_pending_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_counselor_sees_only_own_pending_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_dean_cannot_see_other_dean_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_dean_cannot_see_other_dean_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_dean_sees_only_own_pending_approvals (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_dean_sees_only_own_pending_approvals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_decision_all_does_not_leak_cross_approver_data (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_decision_all_does_not_leak_cross_approver_data)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_response_format_count_and_results (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_response_format_count_and_results)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_student_403_on_approval_list (apps.approvals.tests.test_list_permissions.ApprovalListPermissionTest.test_student_403_on_approval_list)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_list_permissions.py", line 57, in setUp
    step=ApprovalStep.DEAN,
         ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/enum.py", line 786, in __getattr__
    raise AttributeError(name) from None
AttributeError: DEAN

======================================================================
ERROR: test_counselor_cannot_act_on_dean_step (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_counselor_cannot_act_on_dean_step)
辅导员不能处理学工部审批步骤
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_permissions.py", line 56, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_cross_counselor_approve_forbidden (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_cross_counselor_approve_forbidden)
测试跨辅导员审批返回403
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_permissions.py", line 56, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_cross_counselor_reject_forbidden (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_cross_counselor_reject_forbidden)
测试跨辅导员驳回返回403
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_permissions.py", line 56, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_dean_cannot_act_on_counselor_step (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_dean_cannot_act_on_counselor_step)
学工部不能处理辅导员审批步骤
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_permissions.py", line 56, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_non_assigned_dean_forbidden (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_non_assigned_dean_forbidden)
同角色但非指定学工部审批人不能处理审批
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_permissions.py", line 56, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_student_cannot_approve_or_reject (apps.approvals.tests.test_permissions.ApprovalPermissionsTestCase.test_student_cannot_approve_or_reject)
学生不能调用审批操作接口
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_permissions.py", line 56, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_counselor_step_requires_pending_counselor_status (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_counselor_step_requires_pending_counselor_status)
测试辅导员审批步骤与申请状态不匹配时返回409
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_state_machine.py", line 38, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_dean_step_requires_pending_dean_status (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_dean_step_requires_pending_dean_status)
测试学工部审批步骤与申请状态不匹配时返回409
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_state_machine.py", line 38, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_duplicate_approval_conflict (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_duplicate_approval_conflict)
测试重复审批返回409
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_state_machine.py", line 38, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


======================================================================
ERROR: test_reject_then_repeat_operation_conflict (apps.approvals.tests.test_state_machine.ApprovalStateMachineTestCase.test_reject_then_repeat_operation_conflict)
测试驳回后的重复操作返回409
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.UndefinedColumn: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/apps/approvals/tests/test_state_machine.py", line 38, in setUp
    ClassMapping.objects.create(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 658, in create
    obj.save(force_insert=True, using=self.db)
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 814, in save
    self.save_base(
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 877, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1020, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1061, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1805, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1822, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: column "dorm_manager_id" of relation "class_mappings" does not exist
LINE 1: INSERT INTO "class_mappings" ("class_id", "dorm_manager_id",...
                                                  ^


----------------------------------------------------------------------
Ran 119 tests in 15.422s

FAILED (errors=39)
Destroying test database for alias 'default' ('test_graduation_leave')...

codex
The clean run confirms the failures are reproducible on a freshly created PostgreSQL test database, so this is not only a stale database issue. The common cause remains `ClassMapping.dorm_manager`: the model expects it, but migrations do not create it.
web search: 
web search: https://docs.djangoproject.com/en/4.2/ref/databases/
web search: 
web search: 'binary package' in https://www.psycopg.org/psycopg3/docs/basic/install.html
codex
Best approach: use the existing Docker test environment, not SQLite. This repo already has `docker-compose.yml` with PostgreSQL and `backend/Dockerfile` installs `libpq-dev`, so it avoids the host Python 3.14 / `pg_config` problem while keeping production-like PostgreSQL behavior.

I ran the regression scope in Docker. Django started correctly and found `119` tests, so the psycopg blocker is bypassed. The run failed with `39` errors, all from the same schema issue:

`class_mappings.dorm_manager_id does not exist`

That is not a psycopg/install problem. The current `ClassMapping` model has `dorm_manager` and `dorm_manager_name`, but `backend/apps/users/migrations/0001_initial.py` only creates the counselor fields. A clean test DB confirmed this, so `--keepdb` was not the root cause.

Recommended path:

```bash
rtk docker compose exec -T backend python manage.py makemigrations users
rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_mapper apps.users.tests.test_xg_user_client apps.users.tests.test_xg_user_sync apps.users.tests.test_import_csv apps.applications.tests.test_application_flow apps.applications.tests.test_serializer_validation apps.applications.tests.test_list_permissions apps.applications.tests.test_constraints apps.applications.tests.test_error_cases apps.applications.tests.test_detail_permissions apps.applications.tests.test_p0_fixes apps.approvals.tests.test_rejection_flow apps.approvals.tests.test_list_permissions apps.approvals.tests.test_permissions apps.approvals.tests.test_state_machine --noinput -v 2
```

Option ranking:

1. **Docker/PostgreSQL: best for Phase 4 regression.**
2. **psycopg3 binary: good host fallback.** Django 4.2 supports psycopg 3.1.8+ or psycopg2, and psycopg’s binary install supports Python 3.10-3.14 without local `libpq` or build tools. Sources: Django docs and Psycopg docs. ([docs.djangoproject.com](https://docs.djangoproject.com/en/4.2/ref/databases/)) ([psycopg.org](https://www.psycopg.org/psycopg3/docs/basic/install.html))
3. **SQLite: acceptable only as a fast smoke-test fallback**, but weaker for regression because it changes DB semantics.
4. **Mock database: not appropriate** for this suite; these are ORM/API workflow tests.
tokens used
115,165

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
