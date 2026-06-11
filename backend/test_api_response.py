#!/usr/bin/env python3
"""测试API返回数据"""
import requests
import json

API_BASE = 'http://127.0.0.1:7787'

# 登录
login_resp = requests.post(f'{API_BASE}/api/auth/login', json={
    'user_id': '2020220040131',
    'password': '123456'
})

print('=== 登录测试 ===')
if login_resp.ok:
    data = login_resp.json()
    if data.get('success'):
        print(f"✅ 登录成功")
        print(f"用户: {data['user']['name']}")
        print(f"楼栋: {data['user'].get('building', 'N/A')}")
        print(f"房间: {data['user'].get('room_number', 'N/A')}")

        token = data['token']

        # 获取申请列表
        print('\n=== 申请列表 ===')
        apps_resp = requests.get(f'{API_BASE}/api/applications/my', headers={
            'Authorization': f'Bearer {token}'
        })
        if apps_resp.ok:
            apps_data = apps_resp.json()
            print(f"申请数: {len(apps_data.get('results', []))}")
            for app in apps_data.get('results', []):
                print(f"\n申请ID: {app['application_id']}")
                print(f"状态: {app['status']}")

                # 获取审批记录
                print(f'\n=== 审批记录 (申请 {app["application_id"]}) ===')
                approvals_resp = requests.get(
                    f'{API_BASE}/api/approvals/',
                    params={'application_id': app['application_id']},
                    headers={'Authorization': f'Bearer {token}'}
                )
                if approvals_resp.ok:
                    approvals_data = approvals_resp.json()
                    print(f"审批记录数: {len(approvals_data.get('results', []))}")
                    for appr in approvals_data.get('results', []):
                        print(f"  步骤: {appr['step']}, 决定: {appr['decision']}, 意见: '{appr.get('comment', '')}'")
                else:
                    print(f"❌ 获取审批记录失败: {approvals_resp.status_code}")
        else:
            print(f"❌ 获取申请失败: {apps_resp.status_code}")
    else:
        print(f"❌ 登录失败: {data.get('error')}")
else:
    print(f"❌ 登录请求失败: {login_resp.status_code}")
