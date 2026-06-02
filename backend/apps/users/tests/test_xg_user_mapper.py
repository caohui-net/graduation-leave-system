"""学工系统用户映射器测试"""
from django.test import TestCase
from apps.users.integrations.xg_user_mapper import map_xg_user_to_internal


class XGUserMapperTests(TestCase):
    """用户映射器测试"""

    def test_complete_fields_success(self):
        """测试完整字段成功映射"""
        xg_user = {
            'number': '2022001',
            'name': '张三',
            'phone': '13800138000',
            'department': '计算机学院',
            'user_identity': '1'
        }

        result = map_xg_user_to_internal(xg_user)

        self.assertEqual(result['user_id'], '2022001')
        self.assertEqual(result['name'], '张三')
        self.assertEqual(result['role'], 'student')
        self.assertEqual(result['phone'], '13800138000')
        self.assertEqual(result['department'], '计算机学院')
        self.assertIsNone(result['class_id'])
        self.assertIsNone(result['is_graduating'])
        self.assertIsNone(result['graduation_year'])
        self.assertIsNone(result['skip_reason'])

    def test_user_identity_student_string(self):
        """测试user_identity为'student'字符串"""
        xg_user = {
            'number': '2022001',
            'name': '张三',
            'user_identity': 'student'
        }

        result = map_xg_user_to_internal(xg_user)

        self.assertEqual(result['role'], 'student')
        self.assertIsNone(result['skip_reason'])

    def test_missing_number_skip(self):
        """测试number缺失应跳过"""
        xg_user = {
            'name': '张三',
            'user_identity': '1'
        }

        result = map_xg_user_to_internal(xg_user)

        self.assertIsNone(result['user_id'])
        self.assertEqual(result['skip_reason'], 'missing_user_id')

    def test_missing_name_skip(self):
        """测试name缺失应跳过"""
        xg_user = {
            'number': '2022002',
            'phone': '13800138001',
            'user_identity': '1'
        }

        result = map_xg_user_to_internal(xg_user)

        self.assertEqual(result['user_id'], '2022002')
        self.assertIsNone(result['name'])
        self.assertEqual(result['skip_reason'], 'missing_name')

    def test_unknown_user_identity_skip(self):
        """测试user_identity未知值应跳过"""
        xg_user = {
            'number': '2022003',
            'name': '李四',
            'user_identity': '999'
        }

        result = map_xg_user_to_internal(xg_user)

        self.assertEqual(result['user_id'], '2022003')
        self.assertEqual(result['name'], '李四')
        self.assertIsNone(result['role'])
        self.assertEqual(result['skip_reason'], 'unknown_user_identity: 999')

    def test_missing_user_identity_skip(self):
        """测试user_identity缺失应跳过"""
        xg_user = {
            'number': '2022004',
            'name': '王五'
        }

        result = map_xg_user_to_internal(xg_user)

        self.assertEqual(result['user_id'], '2022004')
        self.assertEqual(result['name'], '王五')
        self.assertIsNone(result['role'])
        self.assertEqual(result['skip_reason'], 'missing_user_identity')

    def test_optional_fields_missing(self):
        """测试可选字段缺失不阻止映射"""
        xg_user = {
            'number': '2022005',
            'name': '赵六',
            'user_identity': '1'
        }

        result = map_xg_user_to_internal(xg_user)

        self.assertEqual(result['user_id'], '2022005')
        self.assertEqual(result['name'], '赵六')
        self.assertEqual(result['role'], 'student')
        self.assertIsNone(result['phone'])
        self.assertIsNone(result['department'])
        self.assertIsNone(result['skip_reason'])

    def test_multiple_missing_fields_priority(self):
        """测试多个字段同时缺失的优先级"""
        xg_user = {}

        result = map_xg_user_to_internal(xg_user)

        # number缺失优先级最高
        self.assertEqual(result['skip_reason'], 'missing_user_id')
