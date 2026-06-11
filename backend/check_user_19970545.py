#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.users.models import User
from apps.users.serializers import AuthUserSerializer

try:
    user = User.objects.get(user_id='19970545')
    print("用户存在:")
    print(f"  user_id: {user.user_id}")
    print(f"  name: {user.name}")
    print(f"  role: {user.role}")
    print(f"  building: {user.building}")
    print(f"  room_number: {user.room_number}")
    print(f"  class_id: {user.class_id}")
    print(f"  phone: {user.phone}")

    print("\n序列化测试:")
    serializer = AuthUserSerializer(user)
    print(serializer.data)

except User.DoesNotExist:
    print("用户不存在")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
