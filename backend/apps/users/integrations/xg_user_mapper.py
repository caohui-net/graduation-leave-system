"""学工系统用户数据映射器"""


def map_xg_user_to_internal(xg_user: dict) -> dict:
    """
    将学工API用户映射为内部User字段

    Args:
        xg_user: 学工API返回的用户字典

    Returns:
        dict: {
            'user_id': str | None,
            'name': str | None,
            'role': str | None,
            'phone': str | None,
            'department': str | None,
            'class_id': None,  # API不提供
            'is_graduating': None,  # API不提供
            'graduation_year': None,  # API不提供
            'skip_reason': str | None  # 如果应跳过，说明原因
        }
    """
    result = {
        'user_id': None,
        'name': None,
        'role': None,
        'phone': None,
        'department': None,
        'class_id': None,
        'is_graduating': None,
        'graduation_year': None,
        'skip_reason': None
    }

    # 提取字段
    number = xg_user.get('number')
    name = xg_user.get('name')
    user_identity = xg_user.get('user_identity')
    phone = xg_user.get('phone')
    department = xg_user.get('department')

    # 必填字段检查
    if not number:
        result['skip_reason'] = 'missing_user_id'
        return result

    if not name:
        result['user_id'] = number
        result['skip_reason'] = 'missing_name'
        return result

    # 角色映射（只接受明确的学生值）
    role = None
    if user_identity is not None:
        user_identity_str = str(user_identity)
        if user_identity_str == '1':
            role = 'student'
        elif user_identity_str.lower() == 'student':
            role = 'student'
        else:
            result['user_id'] = number
            result['name'] = name
            result['skip_reason'] = f'unknown_user_identity: {user_identity_str}'
            return result
    else:
        result['user_id'] = number
        result['name'] = name
        result['skip_reason'] = 'missing_user_identity'
        return result

    # 映射成功
    result['user_id'] = number
    result['name'] = name
    result['role'] = role
    result['phone'] = phone
    result['department'] = department

    return result
