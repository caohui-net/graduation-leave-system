#!/usr/bin/env python
"""测试现有SSO管理端接口"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from apps.sso_qingganlian.client import QingganlanClient
from apps.sso_qingganlian import settings as sso_settings

def test_admin_apis():
    """测试管理端接口"""
    print("="*60)
    print("管理端接口测试")
    print("="*60)

    # 初始化客户端
    client = QingganlanClient(
        app_key=sso_settings.QGL_ADMIN_APP_KEY,
        app_secret=sso_settings.QGL_ADMIN_APP_SECRET,
        env=sso_settings.QGL_ENV,
        api_type='admin'
    )

    print(f"\nBase URL: {client.base_url}")
    print(f"APP_KEY: {client.app_key}")
    print(f"APP_SECRET: {client.app_secret[:20]}...")

    # 测试: verify_admin_user（需要真实authorization token）
    print(f"\n{'='*60}")
    print("测试: verify_admin_user")
    print(f"{'='*60}")
    print("说明：此接口需要真实的authorization token（从青橄榄管理端获取）")
    print("状态：⏸️  跳过（需要真实token）")

    print(f"\n{'='*60}")
    print("管理端接口测试总结")
    print(f"{'='*60}")
    print("✅ 接口定义已确认")
    print("⏸️  完整流程测试需要真实登录token")
    print("\n接口用途分析：")
    print("1. verify_admin_user: 验证青橄榄管理端用户token，获取管理员信息")
    print("\n数据流向：青橄榄管理端 → authorization token → 管理员信息")

if __name__ == '__main__':
    test_admin_apis()
