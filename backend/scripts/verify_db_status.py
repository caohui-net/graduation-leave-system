#!/usr/bin/env python3
"""数据库状态验证脚本"""

import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.conf import settings
from apps.users.models import User
from apps.applications.models import Application
from apps.approvals.models import Approval


def main():
    print("=== 数据库连接信息 ===")
    db_config = settings.DATABASES['default']
    print(f"数据库名: {db_config['NAME']}")
    print(f"主机: {db_config['HOST']}")
    print(f"端口: {db_config['PORT']}")
    print(f"用户: {db_config['USER']}")

    print("\n=== 当前数据统计 ===")
    total = User.objects.count()
    students = User.objects.filter(role='student').count()
    dorm_mgrs = User.objects.filter(role='dorm_manager').count()
    counselors = User.objects.filter(role='counselor').count()
    admins = User.objects.filter(role='admin').count()

    print(f"总用户: {total}")
    print(f"- 学生: {students}")
    print(f"- 宿管: {dorm_mgrs}")
    print(f"- 辅导: {counselors}")
    print(f"- 管理: {admins}")
    print(f"申请数: {Application.objects.count()}")
    print(f"审批数: {Approval.objects.count()}")

    print("\n=== 数据状态判断 ===")
    if total == 16:
        print("✓ 当前为测试数据（16用户）")
        print("→ 可以安全执行真实数据导入")
        return 0
    elif total > 6000:
        print("✓ 当前为真实数据（>6000用户）")
        print("→ 真实数据已导入，无需重复导入")
        return 0
    else:
        print(f"⚠ 异常用户数（{total}），需人工确认数据状态")
        return 1


if __name__ == '__main__':
    sys.exit(main())
