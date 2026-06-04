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
            'email': str | None,
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
        'email': None,
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
    email = xg_user.get('email')
    department_raw = xg_user.get('department')

    # 处理department数组: [{"name": "计算机学院", "level": 2}]
    department = None
    if isinstance(department_raw, list) and len(department_raw) > 0:
        if isinstance(department_raw[0], dict):
            department = department_raw[0].get('name')
    elif isinstance(department_raw, str):
        # 向后兼容：支持字符串格式
        department = department_raw

    # 处理phone空字符串：归一化为None
    if phone == '':
        phone = None

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
        # XG API实际返回对象: {"id": 4, "name": "学生"}
        if isinstance(user_identity, dict):
            identity_name = user_identity.get('name', '')
            identity_id = user_identity.get('id')
            if identity_name == '学生' or identity_id == 4:
                role = 'student'
            else:
                result['user_id'] = number
                result['name'] = name
                result['skip_reason'] = f'unknown_user_identity: name={identity_name}, id={identity_id}'
                return result
        # 向后兼容：支持字符串格式
        else:
            user_identity_str = str(user_identity)
            if user_identity_str == '1' or user_identity_str.lower() == 'student':
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
    result['email'] = email
    result['department'] = department

    return result
