import hashlib
import random
import string
import time


def generate_rand_str(length=16):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_signature(app_secret, timestamp, rand_str, encryption_type='sha1'):
    """
    生成签名

    Args:
        app_secret: 应用密钥
        timestamp: Unix时间戳（字符串）
        rand_str: 随机字符串
        encryption_type: 加密类型（sha1或md5）

    Returns:
        签名字符串
    """
    # 将三个参数进行字典排序
    params = sorted([app_secret, str(timestamp), rand_str])
    # 拼接字符串
    concat_str = ''.join(params)

    # 根据加密类型生成签名
    if encryption_type.lower() == 'md5':
        return hashlib.md5(concat_str.encode()).hexdigest()
    else:
        return hashlib.sha1(concat_str.encode()).hexdigest()


def generate_request_params(app_key, app_secret, encryption_type='sha1'):
    """
    生成请求参数（appKey、timestamp、randStr、sign）

    Args:
        app_key: 应用ID
        app_secret: 应用密钥
        encryption_type: 加密类型（sha1或md5）

    Returns:
        dict: 包含请求头参数
    """
    timestamp = str(int(time.time()))
    rand_str = generate_rand_str()
    sign = generate_signature(app_secret, timestamp, rand_str, encryption_type)

    return {
        'appKey': app_key,
        'timestamp': timestamp,
        'randStr': rand_str,
        'sign': sign,
        'encryptionType': encryption_type
    }
