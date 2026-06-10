#!/usr/bin/env python
"""SSO端到端集成测试"""
import os
import sys
import django
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.users.models import User
from apps.sso_qingganlian.views import admin_login
from rest_framework.test import APIRequestFactory

def test_sso_flow():
    """测试SSO完整流程"""
    print("=== SSO端到端流程测试 ===\n")

    factory = APIRequestFactory()

    # 模拟青橄榄API返回
    mock_result = {
        'data': {
            'user_code': 'test_admin_001',
            'name': '测试管理员',
            'phone': '13800138000',
            'email': 'test@example.com',
            'tenant_code': 'S10405'
        }
    }

    with patch('apps.sso_qingganlian.views.QingganlanClient') as MockClient:
        mock_client = MagicMock()
        MockClient.return_value = mock_client
        mock_client.verify_admin_user.return_value = mock_result

        # 模拟请求
        request = factory.post(
            '/api/sso/qingganlian/admin/login',
            {'authorization': 'bearer test_token'},
            format='json'
        )

        # 调用登录API
        response = admin_login(request)

        # 验证响应
        print(f"1. API响应状态: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.data
        print(f"2. 返回JWT token: {data.get('token', 'N/A')[:20]}...")
        assert 'token' in data, "Missing token in response"

        print(f"3. 用户信息: {data.get('user')}")
        assert data['user']['username'] == 'test_admin_001'

        # 验证数据库
        user = User.objects.get(user_id='test_admin_001')
        print(f"4. 数据库用户创建: {user.user_id} - {user.name}")
        assert user.name == '测试管理员'
        assert user.is_staff == True

        # 验证SSO映射
        from apps.sso_qingganlian.models import SSOUserMapping
        mapping = SSOUserMapping.objects.get(user_code='test_admin_001')
        print(f"5. SSO映射创建: {mapping.user_code} → {mapping.user.user_id}")
        assert mapping.tenant_code == 'S10405'

        print("\n✓ 所有测试通过")
        print("\n完整流程验证:")
        print("  1. 接收authorization token ✓")
        print("  2. 调用青橄榄API验证 ✓")
        print("  3. 自动创建本地User ✓")
        print("  4. 创建SSO映射关系 ✓")
        print("  5. 生成JWT token ✓")

        # 清理测试数据
        user.delete()
        print("\n✓ 测试数据已清理")

if __name__ == "__main__":
    try:
        test_sso_flow()
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
