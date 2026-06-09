#!/usr/bin/env python3
"""
青橄榄API endpoint路径验证脚本
验证 /saas_api/open-api vs /open-api 前缀
"""
import requests
import hashlib
import time
import random
import string

# 测试凭证
APP_KEY = 'abc0a32aa8dd94d1f765841abaafd8ba'
APP_SECRET = 'b1d2efa9587446d80ce6388e0c0b25131b8dea59'
BASE_URL = 'https://dev-lshospital.goliveplus.cn'

def generate_signature(app_secret, timestamp, rand_str):
    params = sorted([app_secret, str(timestamp), rand_str])
    concat_str = ''.join(params)
    return hashlib.sha1(concat_str.encode()).hexdigest()

def test_endpoint(path):
    timestamp = str(int(time.time()))
    rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    sign = generate_signature(APP_SECRET, timestamp, rand_str)

    headers = {
        'Content-Type': 'application/json',
        'appKey': APP_KEY,
        'timestamp': timestamp,
        'randStr': rand_str,
        'sign': sign,
        'encryptionType': 'sha1'
    }

    data = {
        'tenantCode': 'S10405',
        'userCode': 'test_user',
        'userType': '1'
    }

    url = BASE_URL + path
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=10)
        return {
            'path': path,
            'status': resp.status_code,
            'body': resp.text[:200]
        }
    except Exception as e:
        return {
            'path': path,
            'status': 'ERROR',
            'body': str(e)
        }

if __name__ == '__main__':
    paths = [
        '/open-api/user-center/user-code-by-token',
        '/saas_api/open-api/user-center/user-info'
    ]

    print("验证青橄榄API endpoint路径...")
    for path in paths:
        result = test_endpoint(path)
        print(f"\n路径: {result['path']}")
        print(f"状态: {result['status']}")
        print(f"响应: {result['body']}")
