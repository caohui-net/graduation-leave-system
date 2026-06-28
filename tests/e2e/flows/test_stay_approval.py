#!/usr/bin/env python3
"""留校审批业务流程测试

测试场景：
1. 辅导员登录
2. 进入留校审批模块
3. 筛选指定学号
4. 验证数据显示
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config.test_config import BASE_URL, TEST_ACCOUNTS
from helpers.common import login, check_login_success, filter_by_student_id, get_page_state

def test_stay_approval_flow():
    """测试留校审批流程"""
    print("=== 留校审批流程测试 ===\n")

    # 1. 访问系统
    print("1. 访问系统...")
    new_tab(BASE_URL)
    wait_for_load()

    # 2. 辅导员登录
    print("2. 辅导员登录...")
    counselor = TEST_ACCOUNTS['counselor']
    login(counselor['user_id'], counselor['password'], business_type='stay')

    # 3. 验证登录
    print("3. 验证登录...")
    state = check_login_success()
    if not state['hasApprovalList']:
        print("❌ 登录失败：未进入审批界面")
        return False
    print("✓ 登录成功")

    # 4. 测试筛选
    print("\n4. 测试学号筛选...")
    test_student_id = '2024180340308'
    found = filter_by_student_id(test_student_id)

    if found:
        print(f"✓ 筛选成功：找到学号 {test_student_id}")
    else:
        print(f"✗ 筛选失败：未找到学号 {test_student_id}")

    # 5. 获取页面状态
    print("\n5. 页面状态:")
    page_state = get_page_state()
    print(f"  URL: {page_state['url']}")
    print(f"  表格行数: {page_state['tableRows']}")
    print(f"  可用按钮: {', '.join(page_state['buttons'][:5])}")

    return found

if __name__ == '__main__':
    try:
        success = test_stay_approval_flow()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
        sys.exit(1)
