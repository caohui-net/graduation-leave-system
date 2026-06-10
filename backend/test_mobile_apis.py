#!/usr/bin/env python
"""测试现有SSO移动端接口"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from apps.sso_qingganlian.client import QingganlanClient
from apps.sso_qingganlian import settings as sso_settings
import json

def test_mobile_apis():
    """测试移动端接口"""
    print("="*60)
    print("移动端接口测试")
    print("="*60)

    # 初始化客户端
    client = QingganlanClient(
        app_key=sso_settings.QGL_MOBILE_APP_KEY,
        app_secret=sso_settings.QGL_MOBILE_APP_SECRET,
        env=sso_settings.QGL_ENV,
        api_type='mobile'
    )

    print(f"\nBase URL: {client.base_url}")
    print(f"APP_KEY: {client.app_key}")
    print(f"APP_SECRET: {client.app_secret[:20]}...")

    # 测试数据（需要真实token和tenant_code）
    tenant_code = sso_settings.QGL_MOBILE_TENANT_CODE
    appid = sso_settings.QGL_MOBILE_APPID

    print(f"\nTenantCode: {tenant_code}")
    print(f"AppId: {appid}")

    # 测试1: get_user_code_by_token（需要真实token）
    print(f"\n{'='*60}")
    print("测试1: get_user_code_by_token")
    print(f"{'='*60}")
    print("说明：此接口需要真实的saas_wap_token（从青橄榄跳转获取）")
    print("状态：⏸️  跳过（需要真实token）")

    # 测试2: get_user_info（需要user_code）
    print(f"\n{'='*60}")
    print("测试2: get_user_info")
    print(f"{'='*60}")
    print("说明：此接口需要user_code和user_type参数")
    print("状态：⏸️  跳过（需要user_code）")

    print(f"\n{'='*60}")
    print("移动端接口测试总结")
    print(f"{'='*60}")
    print("✅ 接口定义已确认")
    print("⏸️  完整流程测试需要真实登录token")
    print("\n接口用途分析：")
    print("1. get_user_code_by_token: 青橄榄移动端跳转后，用token换取user_code")
    print("2. get_user_info: 根据user_code获取用户详细信息")
    print("\n数据流向：青橄榄移动端 → token → user_code → 用户信息")

if __name__ == '__main__':
    test_mobile_apis()
