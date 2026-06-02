"""学工系统用户API客户端测试"""
from django.test import TestCase
from apps.users.integrations.xg_user_client import generate_sign


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
        """测试md5加密"""
        sign = generate_sign('secret', '1234567890', 'random', 'md5')
        # 验证返回32位hex字符串
        self.assertEqual(len(sign), 32)
        self.assertTrue(all(c in '0123456789abcdef' for c in sign))

    def test_invalid_encryption_type(self):
        """测试非法加密类型"""
        with self.assertRaises(ValueError) as cm:
            generate_sign('secret', '1234567890', 'random', 'sha256')
        self.assertIn("must be 'sha1' or 'md5'", str(cm.exception))
