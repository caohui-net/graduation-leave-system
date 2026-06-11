#!/usr/bin/env python3
"""检查所有用户的building和room_number字段情况"""
import os
import sys
import django

# 设置Django环境
sys.path.insert(0, '/home/caohui/projects/graduation-leave-system/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.users.models import User

# 查询所有用户
users = User.objects.all()
total = users.count()

# 统计字段情况
null_building = users.filter(building__isnull=True).count()
null_room = users.filter(room_number__isnull=True).count()
both_null = users.filter(building__isnull=True, room_number__isnull=True).count()

print(f"总用户数: {total}")
print(f"building为NULL的用户: {null_building} ({null_building*100/total:.1f}%)")
print(f"room_number为NULL的用户: {null_room} ({null_room*100/total:.1f}%)")
print(f"两者都为NULL的用户: {both_null} ({both_null*100/total:.1f}%)")

# 检查用户19970545
try:
    user = User.objects.get(user_id='19970545')
    print(f"\n用户19970545:")
    print(f"  building: {user.building}")
    print(f"  room_number: {user.room_number}")
except User.DoesNotExist:
    print("\n用户19970545不存在")

# 显示最近5个用户的字段情况
print("\n最近5个用户的字段情况:")
for user in users.order_by('-id')[:5]:
    print(f"  {user.user_id}: building={user.building}, room_number={user.room_number}")
