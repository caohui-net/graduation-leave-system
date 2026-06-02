"""学工系统用户API客户端"""
import hashlib
from typing import Literal


def generate_sign(
    app_secret: str,
    timestamp: str,
    rand_str: str,
    encryption_type: Literal['sha1', 'md5'] = 'sha1'
) -> str:
    """
    生成API签名

    签名规则：
    1. 将appSecret, timestamp, randStr三个参数值进行字典排序
    2. 拼接成字符串
    3. 进行sha1或md5加密

    Args:
        app_secret: AppSecret密钥
        timestamp: Unix时间戳（字符串）
        rand_str: 随机字符串
        encryption_type: 加密类型，'sha1'或'md5'，默认'sha1'

    Returns:
        签名字符串（十六进制小写）
    """
    if encryption_type not in ('sha1', 'md5'):
        raise ValueError(f"encryption_type must be 'sha1' or 'md5', got '{encryption_type}'")

    # 1. 字典排序
    params = [app_secret, timestamp, rand_str]
    params.sort()

    # 2. 拼接
    sign_str = ''.join(params)

    # 3. 加密
    if encryption_type == 'md5':
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    else:
        return hashlib.sha1(sign_str.encode('utf-8')).hexdigest()


class XGUserAPIClient:
    """学工系统用户API客户端（待实现）"""
    pass
