"""学工系统用户API客户端测试"""
from django.test import TestCase
from unittest.mock import Mock, patch
from apps.users.integrations.xg_user_client import generate_sign, XGUserAPIConfig, XGUserAPIClient


class GenerateSignTests(TestCase):
    """签名生成函数测试"""

    def test_official_sample_sha1(self):
        """测试官方签名样例（sha1）"""
        app_secret = '6bd1b3fb015b4e72a85769e9d64405d1'
        timestamp = '1573702840'
        rand_str = 'Gc6LGToDKy2AMhXE'

        sign = generate_sign(app_secret, timestamp, rand_str, 'sha1')

        self.assertEqual(sign, 'baeaa6693fb7b9914c9ff9e388654878b8754515')

    def test_official_sample_default_sha1(self):
        """测试官方样例（默认sha1）"""
        sign = generate_sign(
            '6bd1b3fb015b4e72a85769e9d64405d1',
            '1573702840',
            'Gc6LGToDKy2AMhXE'
        )
        self.assertEqual(sign, 'baeaa6693fb7b9914c9ff9e388654878b8754515')

    def test_md5_encryption(self):
        """测试md5加密（固定期望值）"""
        sign = generate_sign('secret', '1234567890', 'random', 'md5')
        # 验证固定期望值（字典排序：1234567890, random, secret）
        self.assertEqual(sign, '2a471e23465cf11561ef7455fff00a86')

    def test_invalid_encryption_type(self):
        """测试非法加密类型"""
        with self.assertRaises(ValueError) as cm:
            generate_sign('secret', '1234567890', 'random', 'sha256')
        self.assertIn("must be 'sha1' or 'md5'", str(cm.exception))


@patch.dict('os.environ', {
    'XG_USER_API_URL': 'https://api.example.com',
    'XG_USER_API_APP_KEY': 'test_key',
    'XG_USER_API_APP_SECRET': 'test_secret',
    'XG_USER_API_TENANT_CODE': 'S10405',
    'XG_USER_API_ENCRYPTION_TYPE': 'sha1'
})
class XGUserAPIConfigTests(TestCase):
    """配置对象测试"""

    def test_valid_config(self):
        """测试有效配置"""
        config = XGUserAPIConfig()
        self.assertEqual(config.url, 'https://api.example.com')
        self.assertEqual(config.app_key, 'test_key')
        self.assertEqual(config.app_secret, 'test_secret')
        self.assertEqual(config.tenant_code, 'S10405')
        self.assertEqual(config.encryption_type, 'sha1')

    @patch.dict('os.environ', {'XG_USER_API_URL': ''})
    def test_missing_url(self):
        """测试缺失URL"""
        with self.assertRaises(ValueError) as cm:
            XGUserAPIConfig()
        self.assertIn('XG_USER_API_URL is required', str(cm.exception))

    @patch.dict('os.environ', {'XG_USER_API_APP_KEY': ''})
    def test_missing_app_key(self):
        """测试缺失appKey"""
        with self.assertRaises(ValueError) as cm:
            XGUserAPIConfig()
        self.assertIn('XG_USER_API_APP_KEY is required', str(cm.exception))

    @patch.dict('os.environ', {'XG_USER_API_APP_SECRET': ''})
    def test_missing_app_secret(self):
        """测试缺失appSecret"""
        with self.assertRaises(ValueError) as cm:
            XGUserAPIConfig()
        self.assertIn('XG_USER_API_APP_SECRET is required', str(cm.exception))

    @patch.dict('os.environ', {'XG_USER_API_TENANT_CODE': ''})
    def test_missing_tenant_code(self):
        """测试缺失tenantCode"""
        with self.assertRaises(ValueError) as cm:
            XGUserAPIConfig()
        self.assertIn('XG_USER_API_TENANT_CODE is required', str(cm.exception))

    @patch.dict('os.environ', {'XG_USER_API_ENCRYPTION_TYPE': 'sha256'})
    def test_invalid_encryption_type(self):
        """测试非法加密类型"""
        with self.assertRaises(ValueError) as cm:
            XGUserAPIConfig()
        self.assertIn("must be 'sha1' or 'md5'", str(cm.exception))

    @patch.dict('os.environ', {'XG_USER_API_ENCRYPTION_TYPE': '  SHA1  '})
    def test_encryption_type_normalization(self):
        """测试加密类型归一化"""
        config = XGUserAPIConfig()
        self.assertEqual(config.encryption_type, 'sha1')

    @patch.dict('os.environ', {'XG_RUN_LIVE_API_TEST': '1'})
    def test_live_test_enabled(self):
        """测试live测试开关启用"""
        config = XGUserAPIConfig()
        self.assertTrue(config.is_live_test_enabled())

    @patch.dict('os.environ', {'XG_RUN_LIVE_API_TEST': '0'})
    def test_live_test_disabled(self):
        """测试live测试开关禁用"""
        config = XGUserAPIConfig()
        self.assertFalse(config.is_live_test_enabled())


class XGUserAPIClientTests(TestCase):
    """客户端测试"""

    def setUp(self):
        self.env_patcher = patch.dict('os.environ', {
            'XG_USER_API_URL': 'https://api.example.com',
            'XG_USER_API_APP_KEY': 'test_key',
            'XG_USER_API_APP_SECRET': 'test_secret',
            'XG_USER_API_TENANT_CODE': 'S10405',
            'XG_USER_API_ENCRYPTION_TYPE': 'sha1'
        })
        self.env_patcher.start()
        self.config = XGUserAPIConfig()
        self.client = XGUserAPIClient(self.config)

    def tearDown(self):
        self.env_patcher.stop()

    def test_build_headers_with_fixed_params(self):
        """测试headers构造（固定参数）"""
        headers = self.client.build_headers(timestamp='1234567890', rand_str='test_rand')

        self.assertEqual(headers['appKey'], 'test_key')
        self.assertEqual(headers['timestamp'], '1234567890')
        self.assertEqual(headers['randStr'], 'test_rand')
        self.assertEqual(headers['encryptionType'], 'sha1')
        self.assertIn('sign', headers)
        # 验证签名确定性
        expected_sign = generate_sign('test_secret', '1234567890', 'test_rand', 'sha1')
        self.assertEqual(headers['sign'], expected_sign)

    def test_build_headers_auto_generate(self):
        """测试headers自动生成timestamp和randStr"""
        headers = self.client.build_headers()

        self.assertEqual(headers['appKey'], 'test_key')
        self.assertIn('timestamp', headers)
        self.assertIn('randStr', headers)
        self.assertIn('sign', headers)
        self.assertEqual(headers['encryptionType'], 'sha1')

    def test_build_form_data_default(self):
        """测试form-data构造（默认参数）"""
        data = self.client.build_form_data()

        self.assertEqual(data['tenantCode'], 'S10405')
        self.assertEqual(data['page'], '1')
        self.assertEqual(data['pageNum'], '1')

    def test_build_form_data_custom(self):
        """测试form-data构造（自定义参数）"""
        data = self.client.build_form_data(page=2, page_num=10)

        self.assertEqual(data['tenantCode'], 'S10405')
        self.assertEqual(data['page'], '2')
        self.assertEqual(data['pageNum'], '10')

    def test_fetch_users_page_success(self):
        """测试成功响应解析"""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            'code': 200,
            'msg': 'success',
            'data': {
                'current_page': 1,
                'per_page': 10,
                'total': 100,
                'data': [
                    {'name': '张三', 'number': '2021001'},
                    {'name': '李四', 'number': '2021002'}
                ]
            }
        }
        mock_session.post.return_value = mock_response

        result = self.client.fetch_users_page(session=mock_session)

        self.assertEqual(result['code'], 200)
        self.assertEqual(result['msg'], 'success')
        self.assertEqual(result['current_page'], 1)
        self.assertEqual(result['per_page'], 10)
        self.assertEqual(result['total'], 100)
        self.assertEqual(len(result['users']), 2)

    def test_fetch_users_page_http_error(self):
        """测试HTTP错误"""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception('HTTP 500')
        mock_session.post.return_value = mock_response

        with self.assertRaises(Exception):
            self.client.fetch_users_page(session=mock_session)

    def test_fetch_users_page_missing_code(self):
        """测试响应缺失code字段"""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {'msg': 'no code'}
        mock_session.post.return_value = mock_response

        with self.assertRaises(ValueError) as cm:
            self.client.fetch_users_page(session=mock_session)
        self.assertIn("missing 'code'", str(cm.exception))

    def test_fetch_users_page_business_error(self):
        """测试业务错误响应"""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            'code': 401,
            'msg': 'unauthorized'
        }
        mock_session.post.return_value = mock_response

        result = self.client.fetch_users_page(session=mock_session)

        self.assertEqual(result['code'], 401)
        self.assertEqual(result['msg'], 'unauthorized')
