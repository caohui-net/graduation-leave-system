#!/usr/bin/env python
"""管理端SSO对接测试脚本"""
import os
import sys
import django

# Django环境初始化
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.sso_qingganlian.client import QingganlanClient
from apps.sso_qingganlian import settings as sso_settings

def test_admin_credentials():
    """测试管理端凭证配置"""
    print("=== 管理端凭证配置 ===")
    print(f"APP_KEY: {sso_settings.QGL_ADMIN_APP_KEY}")
    print(f"APP_SECRET: {sso_settings.QGL_ADMIN_APP_SECRET[:10]}...")
    print(f"ENV: {sso_settings.QGL_ENV}")
    print()

def test_admin_client():
    """测试管理端客户端初始化"""
    print("=== 测试客户端初始化 ===")
    try:
        client = QingganlanClient(
            app_key=sso_settings.QGL_ADMIN_APP_KEY,
            app_secret=sso_settings.QGL_ADMIN_APP_SECRET,
            env=sso_settings.QGL_ENV,
            api_type='admin'
        )
        print(f"✓ 客户端初始化成功")
        print(f"  Base URL: {client.base_url}")
        print()
        return client
    except Exception as e:
        print(f"✗ 客户端初始化失败: {e}")
        return None

def test_admin_login(client, authorization_token):
    """测试管理端登录"""
    print("=== 测试管理端登录 ===")
    try:
        result = client.verify_admin_user(authorization_token)
        print("✓ 登录成功")
        print(f"  响应: {result}")
        return True
    except Exception as e:
        print(f"✗ 登录失败: {e}")
        return False

if __name__ == "__main__":
    print("青橄榄管理端SSO对接测试\n")

    # Step 1: 检查配置
    test_admin_credentials()

    # Step 2: 测试客户端
    client = test_admin_client()
    if not client:
        sys.exit(1)

    # Step 3: 测试登录（需要真实token）
    print("⚠ 需要真实的 authorization token 来测试登录")
    print("请提供格式如: bearer eyJ0eXAiOiJKV1QiLCJhbGc...")
    print()

    token = input("输入 authorization token (留空跳过): ").strip()
    if token:
        test_admin_login(client, token)
    else:
        print("跳过登录测试")
