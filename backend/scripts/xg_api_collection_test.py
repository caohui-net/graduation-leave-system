#!/usr/bin/env python
"""XG API全面数据采集测试脚本

测试范围：
1. 数据范围：分页、过滤、排序
2. 数据内容：字段完整性、数据类型
3. 数据量：总量统计、批量采集

使用方法：
  export XG_RUN_LIVE_API_TEST=1
  python scripts/xg_api_collection_test.py --output reports/
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from apps.users.integrations.xg_user_client import XGUserAPIClient, XGUserAPIConfig


class XGAPICollectionTester:
    """XG API全面采集测试器"""

    def __init__(self, output_dir='reports'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.config = XGUserAPIConfig()
        self.client = XGUserAPIClient(self.config)
        self.results = {
            'test_time': datetime.now().isoformat(),
            'scope_tests': {},
            'content_tests': {},
            'volume_tests': {}
        }

    def test_pagination(self, max_pages=5):
        """测试1：分页数据采集"""
        print("\n=== 测试1：分页采集 ===")
        results = []

        for page in range(1, max_pages + 1):
            print(f"采集第{page}页...")
            try:
                response = self.client.fetch_users_page(page=page, page_num=10)
                if response['code'] != 200:
                    print(f"✗ 第{page}页失败: {response.get('msg')}")
                    break

                page_info = {
                    'page': page,
                    'current_page': response.get('current_page', page),
                    'per_page': int(response.get('per_page', 10)),
                    'total': response.get('total', 0),
                    'record_count': len(response.get('users', [])),
                    'has_next': page * int(response.get('per_page', 10)) < response.get('total', 0)
                }
                results.append(page_info)
                print(f"✓ 第{page}页: {page_info['record_count']}条记录")

                if not page_info['has_next']:
                    print(f"已到最后一页（共{page}页）")
                    break

                time.sleep(0.5)  # 避免频繁请求

            except Exception as e:
                print(f"✗ 第{page}页异常: {e}")
                break

        self.results['scope_tests']['pagination'] = {
            'status': 'completed' if results else 'failed',
            'pages_tested': len(results),
            'results': results
        }
        return results

    def test_filters(self):
        """测试2：过滤条件测试"""
        print("\n=== 测试2：过滤条件采集 ===")
        print("⚠ 注意：当前客户端不支持过滤参数，跳过过滤测试")
        filter_tests = []

        self.results['scope_tests']['filters'] = {
            'status': 'completed' if filter_tests else 'failed',
            'tests': filter_tests
        }
        return filter_tests

    def test_field_completeness(self, sample_size=10):
        """测试3：字段完整性检查"""
        print("\n=== 测试3：数据内容完整性 ===")

        try:
            response = self.client.fetch_users_page(page=1, page_num=sample_size)
            if response['code'] != 200:
                print(f"✗ 获取数据失败: {response.get('msg')}")
                return None

            users = response.get('users', [])
            print(f"采样{len(users)}条记录...")

            # 必填字段检查
            required_fields = ['number', 'name', 'phone', 'status']
            field_stats = {field: {'present': 0, 'null': 0, 'empty': 0} for field in required_fields}

            for user in users:
                for field in required_fields:
                    value = user.get(field)
                    if value is None:
                        field_stats[field]['null'] += 1
                    elif value == '':
                        field_stats[field]['empty'] += 1
                    else:
                        field_stats[field]['present'] += 1

            print("\n字段完整性统计：")
            for field, stats in field_stats.items():
                total = sum(stats.values())
                present_pct = (stats['present'] / total * 100) if total > 0 else 0
                status = '✓' if present_pct == 100 else '⚠'
                print(f"{status} {field}: {stats['present']}/{total} ({present_pct:.1f}%)")

            # 关联对象检查
            related_stats = {
                'user_identity': 0,
                'department': 0,
                'parent_dep': 0,
                'user': 0
            }

            for user in users:
                if user.get('user_identity'):
                    related_stats['user_identity'] += 1
                if user.get('department') and len(user['department']) > 0:
                    related_stats['department'] += 1
                if user.get('parent_dep') and len(user['parent_dep']) > 0:
                    related_stats['parent_dep'] += 1
                if user.get('user'):
                    related_stats['user'] += 1

            print("\n关联对象统计：")
            for obj, count in related_stats.items():
                pct = (count / len(users) * 100) if users else 0
                status = '✓' if pct >= 90 else '⚠'
                print(f"{status} {obj}: {count}/{len(users)} ({pct:.1f}%)")

            self.results['content_tests']['field_completeness'] = {
                'status': 'completed',
                'sample_size': len(users),
                'required_fields': field_stats,
                'related_objects': related_stats
            }

            return field_stats

        except Exception as e:
            print(f"✗ 字段完整性检查失败: {e}")
            return None

    def test_data_volume(self):
        """测试4：数据量统计"""
        print("\n=== 测试4：数据量统计 ===")

        try:
            response = self.client.fetch_users_page(page=1, page_num=1)
            if response['code'] != 200:
                print(f"✗ 获取数据失败: {response.get('msg')}")
                return None

            volume_info = {
                'total_records': response.get('total', 0),
                'total_pages': (response.get('total', 0) + int(response.get('per_page', 10)) - 1) // int(response.get('per_page', 10)),
                'per_page': int(response.get('per_page', 10)),
                'estimated_fetch_time_minutes': ((response.get('total', 0) + int(response.get('per_page', 10)) - 1) // int(response.get('per_page', 10))) * 0.5 / 60
            }

            print(f"✓ 总记录数: {volume_info['total_records']}")
            print(f"✓ 总页数: {volume_info['total_pages']}")
            print(f"✓ 每页记录数: {volume_info['per_page']}")
            print(f"✓ 预估全量采集时间: {volume_info['estimated_fetch_time_minutes']:.1f}分钟")

            self.results['volume_tests']['statistics'] = volume_info
            return volume_info

        except Exception as e:
            print(f"✗ 数据量统计失败: {e}")
            return None

    def save_report(self):
        """保存测试报告"""
        report_file = self.output_dir / f"xg_collection_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n报告已保存: {report_file}")
        return report_file

    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("XG API 全面数据采集测试")
        print("=" * 60)

        # 检查环境变量
        if os.getenv('XG_RUN_LIVE_API_TEST') != '1':
            print("\n⚠ 警告: XG_RUN_LIVE_API_TEST != 1")
            print("此脚本需要真实API凭证。设置环境变量后运行：")
            print("  export XG_RUN_LIVE_API_TEST=1")
            print("  python scripts/xg_api_collection_test.py")
            return False

        try:
            # 测试1：分页
            self.test_pagination(max_pages=3)

            # 测试2：过滤
            self.test_filters()

            # 测试3：字段完整性
            self.test_field_completeness(sample_size=20)

            # 测试4：数据量
            self.test_data_volume()

            # 保存报告
            report_file = self.save_report()

            print("\n" + "=" * 60)
            print("测试完成")
            print("=" * 60)
            return True

        except Exception as e:
            print(f"\n✗ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='XG API全面数据采集测试')
    parser.add_argument('--output', default='reports', help='输出目录')
    args = parser.parse_args()

    tester = XGAPICollectionTester(output_dir=args.output)
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
