"""学工用户同步计划服务测试"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.users.services.xg_user_sync import plan_xg_user_sync

User = get_user_model()


class XGUserSyncPlanTests(TestCase):
    """测试学工用户同步计划生成（不写DB）"""

    def setUp(self):
        """测试前准备：创建测试用户"""
        # 已存在的学生
        User.objects.create(
            user_id='2021001',
            name='张三',
            role='student',
            active=True,
            class_id='CS2021-1',
            is_graduating=True,
            graduation_year=2025
        )

        # 已存在的教师（角色冲突测试）
        User.objects.create(
            user_id='T001',
            name='李老师',
            role='counselor',
            active=True
        )

    def test_mapper_skip_transparency(self):
        """测试1：mapper skip透传统计"""
        xg_users = [
            {'number': None, 'name': '王五', 'user_identity': '1'},  # 缺number
            {'number': '2021003', 'name': None, 'user_identity': '1'},  # 缺name
            {'number': '2021004', 'name': '赵六', 'user_identity': '9'},  # 未知身份
        ]

        result = plan_xg_user_sync(xg_users)

        self.assertEqual(result['total_fetched'], 3)
        self.assertEqual(result['mapped_count'], 0)
        self.assertEqual(result['skipped_count'], 3)
        self.assertGreater(len(result['skipped_by_reason']), 0)
        # 验证统计了不同的skip_reason
        self.assertIn('missing_user_id', result['skipped_by_reason'])
        self.assertIn('missing_name', result['skipped_by_reason'])

    def test_existing_student_to_candidate(self):
        """测试2：已存在学生进入候选（验证候选数语义）"""
        xg_users = [
            {
                'number': '2021001',
                'name': '张三新名字',
                'user_identity': '1',
                'phone': '13800138000',
                'department': '计算机学院'
            }
        ]

        result = plan_xg_user_sync(xg_users)

        self.assertEqual(result['total_fetched'], 1)
        self.assertEqual(result['mapped_count'], 1)
        self.assertEqual(result['skipped_count'], 0)
        self.assertEqual(result['existing_count'], 1)
        self.assertEqual(result['would_update_count'], 1)  # 候选数，非真实可写数
        self.assertEqual(result['missing_local_count'], 0)
        self.assertEqual(len(result['conflicts']), 0)

    def test_missing_local_not_created(self):
        """测试3：本地不存在用户不创建（Phase 1边界）"""
        xg_users = [
            {
                'number': '2021999',
                'name': '新学生',
                'user_identity': '1',
                'phone': '13900139000'
            }
        ]

        result = plan_xg_user_sync(xg_users)

        self.assertEqual(result['mapped_count'], 1)
        self.assertEqual(result['existing_count'], 0)
        self.assertEqual(result['missing_local_count'], 1)
        self.assertEqual(result['would_update_count'], 0)

        # 验证确实没有创建
        self.assertFalse(User.objects.filter(user_id='2021999').exists())

        # 验证有warning提示不创建
        self.assertGreater(len(result['warnings']), 0)
        warning_text = ' '.join(result['warnings'])
        self.assertIn('would_create_but_blocked', warning_text)

    def test_local_role_conflict(self):
        """测试4：本地角色冲突检测"""
        xg_users = [
            {
                'number': 'T001',
                'name': '李老师',
                'user_identity': '1',  # API认为是学生
            }
        ]

        result = plan_xg_user_sync(xg_users)

        self.assertEqual(result['mapped_count'], 1)
        self.assertEqual(result['existing_count'], 1)
        self.assertEqual(result['would_update_count'], 0)  # 冲突不计入候选
        self.assertEqual(len(result['conflicts']), 1)

        # 验证conflict结构完整性
        conflict = result['conflicts'][0]
        self.assertEqual(conflict['user_id'], 'T001')
        self.assertEqual(conflict['reason'], 'role_mismatch')
        self.assertEqual(conflict['local_role'], 'counselor')
        self.assertEqual(conflict['api_role'], 'student')

    def test_core_fields_readonly(self):
        """测试5：服务只读，不修改核心字段"""
        # 记录原始值
        original_user = User.objects.get(user_id='2021001')
        original_class_id = original_user.class_id
        original_is_graduating = original_user.is_graduating
        original_graduation_year = original_user.graduation_year

        xg_users = [
            {
                'number': '2021001',
                'name': '张三',
                'user_identity': '1',
            }
        ]

        result = plan_xg_user_sync(xg_users)

        # 验证服务执行后DB不变
        user_after = User.objects.get(user_id='2021001')
        self.assertEqual(user_after.class_id, original_class_id)
        self.assertEqual(user_after.is_graduating, original_is_graduating)
        self.assertEqual(user_after.graduation_year, original_graduation_year)
        self.assertEqual(user_after.name, original_user.name)  # name也不变

    def test_field_gap_warning_with_candidates(self):
        """测试6：存在候选时输出字段gap warning"""
        xg_users = [
            {
                'number': '2021001',
                'name': '张三',
                'user_identity': '1',
                'phone': '13800138000',
                'department': '计算机学院'
            }
        ]

        result = plan_xg_user_sync(xg_users)

        self.assertEqual(result['would_update_count'], 1)
        self.assertGreater(len(result['warnings']), 0)

        # 验证强化后的warning文本
        warning_text = ' '.join(result['warnings'])
        self.assertIn('sync candidates exist', warning_text)
        self.assertIn('no API supplemental fields can be persisted', warning_text)
        self.assertIn('phone/email/department', warning_text)

    def test_empty_input(self):
        """测试7：空输入处理"""
        result = plan_xg_user_sync([])

        self.assertEqual(result['total_fetched'], 0)
        self.assertEqual(result['mapped_count'], 0)
        self.assertEqual(result['skipped_count'], 0)
        self.assertEqual(result['existing_count'], 0)
        self.assertEqual(result['missing_local_count'], 0)
        self.assertEqual(result['would_update_count'], 0)
        self.assertEqual(len(result['conflicts']), 0)
        self.assertEqual(len(result['warnings']), 0)

    def test_mixed_scenario(self):
        """测试8：混合场景（skip/missing/conflict/existing各1个）"""
        xg_users = [
            # skip - 缺number
            {'number': None, 'name': '测试1', 'user_identity': '1'},

            # skip - 未知身份（不同reason）
            {'number': '2021005', 'name': '测试2', 'user_identity': '9'},

            # missing_local
            {'number': '2021998', 'name': '测试3', 'user_identity': '1'},

            # conflict
            {'number': 'T001', 'name': '李老师', 'user_identity': '1'},

            # existing student
            {'number': '2021001', 'name': '张三', 'user_identity': '1'},
        ]

        result = plan_xg_user_sync(xg_users)

        self.assertEqual(result['total_fetched'], 5)
        self.assertEqual(result['mapped_count'], 3)  # skip的2个不计入
        self.assertEqual(result['skipped_count'], 2)
        self.assertEqual(result['existing_count'], 2)  # T001和2021001都存在
        self.assertEqual(result['missing_local_count'], 1)
        self.assertEqual(result['would_update_count'], 1)  # 只有2021001是学生候选
        self.assertEqual(len(result['conflicts']), 1)

        # 验证多个skip_reason统计
        self.assertEqual(len(result['skipped_by_reason']), 2)

        # 验证计数互不串类
        total_categorized = (
            result['skipped_count'] +
            result['missing_local_count'] +
            len(result['conflicts']) +
            result['would_update_count']
        )
        self.assertEqual(total_categorized, result['total_fetched'])
