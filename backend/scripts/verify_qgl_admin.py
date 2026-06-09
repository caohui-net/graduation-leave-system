#!/usr/bin/env python3
"""
青橄榄管理端API验证脚本
"""
import requests
import hashlib
import time
import random
import string

# 测试凭证
APP_KEY = 'abc0a32aa8dd94d1f765841abaafd8ba'
APP_SECRET = 'b1d2efa9587446d80ce6388e0c0b25131b8dea59'
BASE_URL = 'https://dev-logisticsplatform.goliveplus.cn'

def generate_signature(app_secret, timestamp, rand_str):
    params = sorted([app_secret, str(timestamp), rand_str])
    concat_str = ''.join(params)
    return hashlib.sha1(concat_str.encode()).hexdigest()

def test_admin_endpoint():
    endpoint = '/api/open-api/auth/verify-user'
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

    # 使用测试token（实际需要从青橄榄管理平台获取）
    data = {
        'token': 'test_token_placeholder'
    }

    url = BASE_URL + endpoint
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=10)
        return {
            'endpoint': endpoint,
            'status': resp.status_code,
            'body': resp.text[:500]
        }
    except Exception as e:
        return {
            'endpoint': endpoint,
            'status': 'ERROR',
            'body': str(e)
        }

if __name__ == '__main__':
    print("验证青橄榄管理端API...")
    result = test_admin_endpoint()
    print(f"\nEndpoint: {result['endpoint']}")
    print(f"状态: {result['status']}")
    print(f"响应: {result['body']}")
