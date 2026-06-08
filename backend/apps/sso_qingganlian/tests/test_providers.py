import unittest
from unittest.mock import patch, MagicMock
from apps.sso_qingganlian.providers.qingganlian import QingganlanProvider
from apps.sso_qingganlian.exceptions import SSOAPIError


class TestQingganlanProvider(unittest.TestCase):
    """测试QingganlanProvider"""

    @patch('apps.sso_qingganlian.providers.qingganlian.QingganlanClient')
    def setUp(self, mock_client_class):
        self.mock_client = MagicMock()
        mock_client_class.return_value = self.mock_client
        self.provider = QingganlanProvider(api_type='mobile')

    def test_mobile_authentication_success(self):
        """测试移动端认证成功"""
        self.mock_client.get_user_code_by_token.return_value = {
            'data': {
                'user_code': 'U001',
                'user_type': 'student'
            }
        }
        self.mock_client.get_user_info.return_value = {
            'data': {
                'number': '20210001',
                'real_name': '张三',
                'phone': '13800138000',
                'email': 'zhangsan@example.com',
                'identity_name': '学生',
                'role_name': '本科生'
            }
        }

        result = self.provider.authenticate({
            'tenant_code': 'T001',
            'appid': 'app123',
            'saas_wap_token': 'token123'
        })

        self.assertEqual(result['external_uid'], 'U001')
        self.assertEqual(result['real_name'], '张三')
        self.mock_client.get_user_code_by_token.assert_called_once()
        self.mock_client.get_user_info.assert_called_once()

    @patch('apps.sso_qingganlian.providers.qingganlian.QingganlanClient')
    def test_admin_authentication_success(self, mock_admin_client_class):
        """测试管理端认证成功"""
        mock_admin_client = MagicMock()
        mock_admin_client_class.return_value = mock_admin_client
        mock_admin_client.verify_admin_user.return_value = {
            'data': {
                'username': 'admin',
                'name': '李四',
                'phone': '13900139000',
                'email': 'lisi@example.com',
                'tenant_code': 'T002'
            }
        }

        admin_provider = QingganlanProvider(api_type='admin')
        result = admin_provider.authenticate({
            'authorization': 'Bearer token123'
        })

        self.assertEqual(result['external_uid'], 'admin')
        self.assertEqual(result['real_name'], '李四')
        mock_admin_client.verify_admin_user.assert_called_once()

    def test_authentication_failure(self):
        """测试认证失败"""
        self.mock_client.get_user_code_by_token.side_effect = SSOAPIError(400, '认证失败')

        with self.assertRaises(SSOAPIError):
            self.provider.authenticate({
                'tenant_code': 'T001',
                'appid': 'app123',
                'saas_wap_token': 'invalid_token'
            })

    def test_provider_name(self):
        """测试provider_name属性"""
        self.assertEqual(self.provider.provider_name, 'qingganlian')


if __name__ == '__main__':
    unittest.main()
