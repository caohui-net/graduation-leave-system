#!/usr/bin/env python
"""管理端SSO Mock测试 - 验证凭证配置"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from unittest.mock import MagicMock, patch
from apps.sso_qingganlian.providers.qingganlian import QingganlanProvider
from apps.sso_qingganlian import settings as sso_settings

def test_credentials():
    """验证凭证配置"""
    print("=== 管理端凭证验证 ===")
    print(f"APP_KEY: {sso_settings.QGL_ADMIN_APP_KEY}")
    print(f"APP_SECRET: {sso_settings.QGL_ADMIN_APP_SECRET[:10]}...")
    print(f"ENV: {sso_settings.QGL_ENV}")

    assert sso_settings.QGL_ADMIN_APP_KEY == "cb6f276a42042179e90cd79c4126e075"
    assert sso_settings.QGL_ADMIN_APP_SECRET == "da02720febcf47071ee5db78c2b068ec"
    print("✓ 凭证配置正确\n")

@patch('apps.sso_qingganlian.providers.qingganlian.QingganlanClient')
def test_admin_auth_success(mock_client_class):
    """Mock测试：管理端认证成功"""
    print("=== Mock测试：管理端认证 ===")

    # Mock client
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    mock_client.verify_admin_user.return_value = {
        'data': {
            'username': 'admin001',
            'name': '测试管理员',
            'phone': '13800138000',
            'email': 'admin@test.com',
            'tenant_code': 'S10405'
        }
    }

    # 执行认证
    provider = QingganlanProvider(api_type='admin')
    result = provider.authenticate({
        'authorization': 'Bearer mock_token_123'
    })

    # 验证结果
    assert result['external_uid'] == 'admin001'
    assert result['real_name'] == '测试管理员'
    assert result['provider_data']['tenant_code'] == 'S10405'

    print(f"✓ 认证成功")
    print(f"  用户: {result['real_name']} ({result['external_uid']})")
    print(f"  租户: {result['provider_data']['tenant_code']}")
    print(f"  手机: {result['phone']}\n")

def test_client_initialization():
    """验证客户端使用新凭证初始化"""
    print("=== 验证客户端初始化 ===")

    from apps.sso_qingganlian.client import QingganlanClient

    # 创建真实client（检查参数传递）
    client = QingganlanClient(
        app_key=sso_settings.QGL_ADMIN_APP_KEY,
        app_secret=sso_settings.QGL_ADMIN_APP_SECRET,
        env='prod',
        api_type='admin'
    )

    assert client.app_key == "cb6f276a42042179e90cd79c4126e075"
    assert client.app_secret == "da02720febcf47071ee5db78c2b068ec"
    assert client.base_url == "https://zhhq.huanghuai.edu.cn"
    print("✓ 客户端初始化参数正确")
    print(f"  Base URL: {client.base_url}\n")

if __name__ == "__main__":
    print("租号号管理端凭证Mock测试\n")

    try:
        test_credentials()
        test_admin_auth_success()
        test_client_initialization()

        print("=" * 40)
        print("✓ 所有测试通过")
        print("=" * 40)
        print("\n配置验证成功，可以替换到生产环境")

    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
