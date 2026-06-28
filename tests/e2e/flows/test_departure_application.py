#!/usr/bin/env python3
"""离校申请流程测试

测试场景：
1. 学生登录
2. 填写离校申请
3. 提交申请
4. 验证提交成功
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config.test_config import BASE_URL, TEST_ACCOUNTS
from helpers.common import login, fill_form, click_button, get_page_state
import time

def test_departure_application():
    """测试离校申请提交流程"""
    print("=== 离校申请流程测试 ===\n")

    # 1. 访问系统
    print("1. 访问系统...")
    new_tab(BASE_URL)
    wait_for_load()

    # 2. 学生登录
    print("2. 学生登录...")
    student = TEST_ACCOUNTS['student']
    login(student['user_id'], student['password'], business_type='departure')

    # 3. 验证进入申请页面
    state = get_page_state()
    print(f"✓ 当前页面: {state['url']}")

    # 4. 填写申请表单
    print("\n3. 填写离校申请...")
    fill_form({
        '联系电话': '13800138000',
        '离校日期': '2026-07-01'
    })
    time.sleep(1)

    # 5. 提交申请
    print("4. 提交申请...")
    click_button('提交')
    time.sleep(2)
    wait_for_load()

    # 6. 验证提交结果
    print("\n5. 验证提交...")
    result_state = get_page_state()

    success = (
        '提交成功' in str(result_state.get('alerts', [])) or
        '申请已提交' in js("document.body.innerText") or
        result_state['url'] != state['url']  # URL变化表示提交成功
    )

    if success:
        print("✓ 离校申请提交成功")
    else:
        print("✗ 提交状态不明确")
        print(f"  页面状态: {result_state}")

    return success

if __name__ == '__main__':
    try:
        success = test_departure_application()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
        sys.exit(1)
