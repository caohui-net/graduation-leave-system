#!/usr/bin/env python
"""导出管理员账号列表供青橿榄同步"""
import os
import sys
import django
import csv
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.users.models import User

def export_admin_accounts():
    """导出管理员账号"""

    # 查询所有管理员（is_staff=True 或 role=admin/counselor）
    admins = User.objects.filter(
        is_staff=True
    ).order_by('user_id')

    print(f"共找到 {admins.count()} 个管理员账号\n")

    # 生成CSV文件
    timestamp = datetime.now().strftime('%Y%m%d')
    filename = f'管理员账号清单-青橿榄同步-{timestamp}.csv'

    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['工号', '姓名', '角色', '手机号', '邮箱', '备注'])

        for user in admins:
            writer.writerow([
                user.user_id,
                user.name,
                user.role,
                getattr(user, 'phone', ''),
                getattr(user, 'email', ''),
                '管理员' if user.is_staff else ''
            ])

    print(f"✓ 已导出到: {filename}")
    print("\n账号清单预览（前10条）：")
    print("-" * 60)

    for user in admins[:10]:
        print(f"{user.user_id:12} | {user.name:10} | {user.role}")

    if admins.count() > 10:
        print(f"... 还有 {admins.count() - 10} 条记录")

    print("-" * 60)
    print(f"\n请将 {filename} 提交给青橿榄技术团队")

if __name__ == "__main__":
    export_admin_accounts()
