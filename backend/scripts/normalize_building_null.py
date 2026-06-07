#!/usr/bin/env python3
"""统一building字段：NULL转为空字符串"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.users.models import User

print("Building字段标准化：NULL→空字符串")
print("="*60)

# 学生：NULL→''
students_null = User.objects.filter(role='student', building__isnull=True)
count = students_null.count()
print(f"\n学生building=NULL: {count}人")

if count > 0:
    updated = students_null.update(building='')
    print(f"✓ 已更新为空字符串: {updated}人")
else:
    print("无需更新")

# 宿管：保持NULL（兜底机制）
print(f"\n宿管building=NULL: 保持不变（兜底机制）")

print(f"\n{'='*60}")
print("完成")
