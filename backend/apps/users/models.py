from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserRole(models.TextChoices):
    STUDENT = 'student', '学生'
    DORM_MANAGER = 'dorm_manager', '宿管员'
    COUNSELOR = 'counselor', '辅导员'
    DEAN = 'dean', '学工部'
    ADMIN = 'admin', '学工管理员'


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
    building = models.CharField(max_length=100, null=True, blank=True)

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
