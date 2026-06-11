#!/usr/bin/env python3
"""测试学生界面逻辑"""
import requests

API_BASE = 'http://218.75.196.218:7787'

def test_student_login_and_applications(user_id, password='123456'):
    """测试学生登录并获取申请列表"""
    print(f'\n=== 测试账号: {user_id} ===')

    # 登录
    login_resp = requests.post(f'{API_BASE}/api/auth/login', json={
        'user_id': user_id,
        'password': password
    })

    if not login_resp.ok:
        print(f'❌ 登录失败: {login_resp.status_code}')
        return

    login_data = login_resp.json()
    if not login_data.get('success'):
        print(f'❌ 登录失败: {login_data.get("error")}')
        return

    token = login_data['token']
    user = login_data['user']
    print(f'✅ 登录成功: {user["name"]}')

    # 获取申请列表
    apps_resp = requests.get(f'{API_BASE}/api/applications/my', headers={
        'Authorization': f'Bearer {token}'
    })

    if not apps_resp.ok:
        print(f'❌ 获取申请失败: {apps_resp.status_code}')
        return

    apps_data = apps_resp.json()
    applications = apps_data.get('results', [])

    print(f'申请数: {len(applications)}')

    # 分析申请状态
    if not applications:
        print('📝 前端行为: 显示 screen-0 (提交表单)')
        print('   无横幅，直接提交')
        return 'screen-0-new'

    has_active = any(app['status'] in ['pending_dorm_manager', 'pending_counselor', 'approved']
                     for app in applications)
    has_rejected = any(app['status'] == 'rejected' for app in applications)

    for app in applications:
        status_map = {
            'pending_dorm_manager': '待宿管员',
            'pending_counselor': '待辅导员',
            'approved': '已通过',
            'rejected': '已驳回'
        }
        print(f'  - {app["application_id"]}: {status_map.get(app["status"], app["status"])}')

    if has_active:
        print('📱 前端行为: 显示 screen-1 (申请进度)')
        return 'screen-1-progress'
    elif has_rejected:
        print('📝 前端行为: 显示 screen-0 (提交表单)')
        print('⚠️  显示黄色横幅: "您的申请已被驳回"')
        return 'screen-0-rejected'
    else:
        print('📝 前端行为: 显示 screen-0 (提交表单)')
        return 'screen-0-new'

if __name__ == '__main__':
    print('=== 学生界面双模式测试 ===\n')

    # 测试场景1: 有驳回申请
    test_student_login_and_applications('2020220040131')

    # 测试场景2: 有已通过申请
    test_student_login_and_applications('2022160440105')

    # 测试场景3: 无申请
    test_student_login_and_applications('2024220220207')

    print('\n=== 测试完成 ===')
