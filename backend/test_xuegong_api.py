#!/usr/bin/env python
"""测试学工系统用户数据接口"""
import sys
import os
import time
import hashlib
import random
import string
import requests

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

def generate_rand_str(length=16):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_signature(app_secret, timestamp, rand_str, encryption_type='sha1'):
    """生成签名"""
    # 排序：timestamp + appSecret + randStr
    sorted_str = f"{timestamp}{app_secret}{rand_str}"

    if encryption_type == 'sha1':
        return hashlib.sha1(sorted_str.encode()).hexdigest()
    else:
        return hashlib.md5(sorted_str.encode()).hexdigest()

def test_xuegong_api():
    """测试学工系统API"""
    # Credentials
    app_id = 'c6qgh2'
    app_key = 'abc0a32aa8dd94d1f765841abaafd8ba'
    app_secret = 'b1d2efa9587446d80ce6388e0c0b25131b8dea59'

    # API URL
    url = 'https://xuegongmj.hgnu.edu.cn/api/open-api/user-center/tenant/auth-user-info'

    # 生成签名参数
    timestamp = str(int(time.time()))
    rand_str = generate_rand_str(16)
    sign = generate_signature(app_secret, timestamp, rand_str, 'sha1')

    # Headers
    headers = {
        'appKey': app_key,
        'timestamp': timestamp,
        'randStr': rand_str,
        'sign': sign,
        'encryptionType': 'sha1'
    }

    # Form data - 使用项目实际租户号
    form_data = {
        'tenantCode': 'S10405',  # 项目实际租户号
        'page': 1,
        'pageNum': 5  # 只取5条测试
    }

    print("=" * 60)
    print("测试学工系统用户数据接口")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"AppKey: {app_key}")
    print(f"Timestamp: {timestamp}")
    print(f"RandStr: {rand_str}")
    print(f"Sign: {sign}")
    print(f"TenantCode: {form_data['tenantCode']}")
    print("=" * 60)

    try:
        response = requests.post(url, headers=headers, data=form_data, timeout=30)

        print(f"\n状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"\n响应内容:")
        print(response.text[:2000])  # 只打印前2000字符

        if response.status_code == 200:
            data = response.json()
            print(f"\n解析后数据结构:")
            print(f"code: {data.get('code')}")
            print(f"msg: {data.get('msg')}")
            if 'data' in data:
                print(f"data keys: {list(data['data'].keys())}")
                if 'data' in data['data'] and len(data['data']['data']) > 0:
                    print(f"\n第一条用户数据:")
                    first_user = data['data']['data'][0]
                    for key in ['id', 'name', 'number', 'phone', 'identity_id']:
                        print(f"  {key}: {first_user.get(key)}")

    except requests.exceptions.RequestException as e:
        print(f"\n请求失败: {e}")
    except Exception as e:
        print(f"\n发生错误: {e}")

if __name__ == '__main__':
    test_xuegong_api()
