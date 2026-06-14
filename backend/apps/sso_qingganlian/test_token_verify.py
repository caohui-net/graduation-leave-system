#!/usr/bin/env python3
"""验证移动端token提取"""
import sys
import os
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.sso_qingganlian.client import QingganlanClient
from apps.sso_qingganlian import settings as sso_settings
from apps.sso_qingganlian.exceptions import SSOAPIError, SSOTokenExpiredError

def test_token_extraction(saas_wap_token):
    """测试token提取user_code"""
    print(f"\n{'='*60}")
    print(f"测试token: {saas_wap_token[:30]}...")
    print(f"{'='*60}\n")

    client = QingganlanClient(
        app_key=sso_settings.MOBILE_APP_KEY,
        app_secret=sso_settings.MOBILE_APP_SECRET,
        env='prod',
        api_type='mobile'
    )

    try:
        # 1. 测试token换取user_code
        print("步骤1: 调用get_user_code_by_token...")
        token_response = client.get_user_code_by_token(
            tenant_code='S10405',
            appid=sso_settings.MOBILE_APPID,
            saas_wap_token=saas_wap_token
        )

        print(f"✓ API调用成功")
        print(f"  响应code: {token_response.get('code')}")
        print(f"  响应msg: {token_response.get('msg')}")

        data = token_response.get('data', {})
        user_code = data.get('user_code')
        user_type = data.get('user_type')

        print(f"\n提取结果:")
        print(f"  user_code: {user_code}")
        print(f"  user_type: {user_type}")

        if not user_code:
            print("\n✗ 失败: 未获取到user_code")
            return False

        # 2. 测试获取用户信息
        print(f"\n步骤2: 调用get_user_info...")
        user_info_response = client.get_user_info('S10405', user_code, user_type or 'weChat')

        print(f"✓ API调用成功")
        user_info = user_info_response.get('data', {})

        print(f"\n用户信息:")
        print(f"  real_name: {user_info.get('real_name')}")
        print(f"  number: {user_info.get('number')}")
        print(f"  identity_name: {user_info.get('identity_name')}")
        print(f"  phone: {user_info.get('phone')}")

        print(f"\n{'='*60}")
        print("✓ 验证成功: token可正确提取user_code和用户信息")
        print(f"{'='*60}\n")
        return True

    except SSOTokenExpiredError as e:
        print(f"\n✗ Token已过期或已使用")
        print(f"  错误码: {e.code}")
        print(f"  错误信息: {e.message}")
        return False

    except SSOAPIError as e:
        print(f"\n✗ API调用失败")
        print(f"  错误码: {e.code}")
        print(f"  错误信息: {e.message}")
        return False

    except Exception as e:
        print(f"\n✗ 未知错误: {type(e).__name__}: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python test_token_verify.py <saas_wap_token>")
        print("\n说明:")
        print("  验证移动端token是否可以正确提取user_code和用户信息")
        print("  测试环境变量QGL_VERIFY_MOBILE_TOKEN=True的可行性")
        print("\n示例:")
        print("  python test_token_verify.py S10405abc123...")
        sys.exit(1)

    token = sys.argv[1]
    success = test_token_extraction(token)
    sys.exit(0 if success else 1)
