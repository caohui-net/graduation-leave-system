#!/usr/bin/env python3
"""登录流程测试

测试场景：
1. 学生登录
2. 辅导员登录
3. 宿管员登录
4. 验证登录状态持久性
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config.test_config import BASE_URL, TEST_ACCOUNTS
from helpers.common import login, check_login_success, get_page_state

def test_login(role):
    """测试指定角色登录

    Args:
        role: 角色类型 ('student' | 'counselor' | 'dorm_manager')
    """
    account = TEST_ACCOUNTS[role]
    print(f"\n--- 测试{account['name']}登录 ---")

    new_tab(BASE_URL)
    wait_for_load()

    login(account['user_id'], account['password'])

    state = check_login_success()
    success = state['hasApprovalList'] and state['hasCookies']

    if success:
        print(f"✓ {account['name']}登录成功")
        print(f"  - 有审批界面: {state['hasApprovalList']}")
        print(f"  - Cookies已设置: {state['hasCookies']}")
    else:
        print(f"✗ {account['name']}登录失败")
        page_state = get_page_state()
        print(f"  当前URL: {page_state['url']}")

    return success

def test_all_roles():
    """测试所有角色登录"""
    print("=== 登录流程测试 ===")

    results = {}
    for role in ['student', 'counselor', 'dorm_manager']:
        results[role] = test_login(role)

    print("\n=== 测试结果汇总 ===")
    for role, success in results.items():
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{TEST_ACCOUNTS[role]['name']}: {status}")

    return all(results.values())

if __name__ == '__main__':
    try:
        success = test_all_roles()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
        sys.exit(1)
