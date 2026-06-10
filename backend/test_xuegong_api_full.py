#!/usr/bin/env python
"""测试学工系统用户数据接口 - 全面测试版"""
import sys
import os
import time
import hashlib
import random
import string
import requests
import json

sys.path.insert(0, os.path.dirname(__file__))

def generate_rand_str(length=16):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_signature(app_secret, timestamp, rand_str, encryption_type='sha1'):
    """生成签名（字典排序）"""
    params = sorted([app_secret, str(timestamp), rand_str])
    concat_str = ''.join(params)

    if encryption_type == 'sha1':
        return hashlib.sha1(concat_str.encode()).hexdigest()
    else:
        return hashlib.md5(concat_str.encode()).hexdigest()

def test_api_combination(url, header_app_key, sign_secret, tenant_code, test_name):
    """测试API组合"""
    print(f"\n{'='*60}")
    print(f"测试: {test_name}")
    print(f"{'='*60}")

    timestamp = str(int(time.time()))
    rand_str = generate_rand_str(16)
    sign = generate_signature(sign_secret, timestamp, rand_str, 'sha1')

    headers = {
        'appKey': header_app_key,
        'timestamp': timestamp,
        'randStr': rand_str,
        'sign': sign,
        'encryptionType': 'sha1'
    }

    form_data = {
        'tenantCode': tenant_code,
        'page': 1,
        'pageNum': 2
    }

    print(f"URL: {url}")
    print(f"Header appKey: {header_app_key}")
    print(f"Sign secret: {sign_secret[:20]}...")
    print(f"TenantCode: {tenant_code}")
    print(f"Sign: {sign}")

    try:
        response = requests.post(url, headers=headers, data=form_data, timeout=30)
        print(f"\n状态码: {response.status_code}")

        try:
            data = response.json()
            print(f"响应code: {data.get('code')}")
            print(f"响应msg: {data.get('msg')}")

            if data.get('code') == 200 and 'data' in data:
                print(f"\n✅ 成功！数据结构:")
                if isinstance(data['data'], dict):
                    print(f"  - current_page: {data['data'].get('current_page')}")
                    print(f"  - total: {data['data'].get('total')}")
                    if 'data' in data['data'] and len(data['data']['data']) > 0:
                        print(f"  - 记录数: {len(data['data']['data'])}")
                        user = data['data']['data'][0]
                        print(f"\n  第一条用户:")
                        print(f"    name: {user.get('name')}")
                        print(f"    number: {user.get('number')}")
                        print(f"    phone: {user.get('phone')}")
                return True
            else:
                print(f"\n❌ 失败: {data.get('msg')}")
                return False

        except json.JSONDecodeError:
            print(f"响应内容（非JSON）: {response.text[:500]}")
            return False

    except Exception as e:
        print(f"\n❌ 请求异常: {e}")
        return False

def main():
    """主测试函数"""
    # Credentials
    app_id = 'c6qgh2'
    app_key = 'abc0a32aa8dd94d1f765841abaafd8ba'
    app_secret = 'b1d2efa9587446d80ce6388e0c0b25131b8dea59'
    tenant_code = 'S10405'

    url = 'https://xuegongmj.hgnu.edu.cn/api/open-api/user-center/tenant/auth-user-info'

    print("="*60)
    print("青橄榄信息中心API测试")
    print("="*60)

    # 方案A: appKey用AppId，签名用AppSecret
    success_a = test_api_combination(
        url, app_id, app_secret, tenant_code,
        "方案A: appKey=AppId(c6qgh2), sign=AppSecret"
    )

    time.sleep(1)

    # 方案B: appKey用AppKey，签名用AppSecret
    success_b = test_api_combination(
        url, app_key, app_secret, tenant_code,
        "方案B: appKey=AppKey(abc0a32...), sign=AppSecret"
    )

    time.sleep(1)

    # 方案C: appKey用AppId，签名用AppKey（不太可能）
    success_c = test_api_combination(
        url, app_id, app_key, tenant_code,
        "方案C: appKey=AppId(c6qgh2), sign=AppKey"
    )

    print(f"\n{'='*60}")
    print("测试总结")
    print(f"{'='*60}")
    print(f"方案A: {'✅ 成功' if success_a else '❌ 失败'}")
    print(f"方案B: {'✅ 成功' if success_b else '❌ 失败'}")
    print(f"方案C: {'✅ 成功' if success_c else '❌ 失败'}")

    if success_a:
        print(f"\n✅ 推荐使用方案A")
    elif success_b:
        print(f"\n✅ 推荐使用方案B")
    elif success_c:
        print(f"\n✅ 推荐使用方案C")
    else:
        print(f"\n❌ 所有方案均失败，需进一步调试")

if __name__ == '__main__':
    main()
