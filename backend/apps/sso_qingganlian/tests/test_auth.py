import unittest
from apps.sso_qingganlian.auth import generate_signature, generate_rand_str, generate_request_params


class TestAuth(unittest.TestCase):
    """测试签名生成工具"""

    def test_generate_rand_str(self):
        """测试随机字符串生成"""
        rand_str = generate_rand_str(16)
        self.assertEqual(len(rand_str), 16)
        self.assertTrue(rand_str.isalnum())

    def test_generate_signature_sha1(self):
        """测试SHA1签名生成（参考文档示例）"""
        # 文档示例：
        # appSecret: 6bd1b3fb015b4e72a85769e9d64405d1
        # timestamp: 1573702840
        # randStr: Gc6LGToDKy2AMhXE
        # 排序后: 15737028406bd1b3fb015b4e72a85769e9d64405d1Gc6LGToDKy2AMhXE
        # SHA1结果: baeaa6693fb7b9914c9ff9e388654878b8754515

        signature = generate_signature(
            '6bd1b3fb015b4e72a85769e9d64405d1',
            '1573702840',
            'Gc6LGToDKy2AMhXE',
            'sha1'
        )
        self.assertEqual(signature, 'baeaa6693fb7b9914c9ff9e388654878b8754515')

    def test_generate_signature_md5(self):
        """测试MD5签名生成"""
        signature = generate_signature(
            'test_secret',
            '1234567890',
            'randomstr',
            'md5'
        )
        self.assertEqual(len(signature), 32)  # MD5长度为32

    def test_generate_request_params(self):
        """测试请求参数生成"""
        params = generate_request_params('test_key', 'test_secret', 'sha1')

        self.assertIn('appKey', params)
        self.assertIn('timestamp', params)
        self.assertIn('randStr', params)
        self.assertIn('sign', params)
        self.assertIn('encryptionType', params)

        self.assertEqual(params['appKey'], 'test_key')
        self.assertEqual(params['encryptionType'], 'sha1')
        self.assertEqual(len(params['randStr']), 16)
        self.assertEqual(len(params['sign']), 40)  # SHA1长度为40


if __name__ == '__main__':
    unittest.main()
