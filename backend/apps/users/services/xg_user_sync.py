"""学工系统用户同步服务"""
from typing import Dict, List
from django.contrib.auth import get_user_model
from apps.users.integrations.xg_user_mapper import map_xg_user_to_internal

User = get_user_model()


def plan_xg_user_sync(xg_users: List[dict]) -> Dict:
    """
    生成学工用户同步计划（不写DB）

    Args:
        xg_users: 学工API返回的用户列表

    Returns:
        {
            'total_fetched': int,
            'mapped_count': int,
            'skipped_count': int,
            'skipped_by_reason': dict,
            'existing_count': int,
            'missing_local_count': int,
            'would_update_count': int,
            'conflicts': list,
            'warnings': list
        }
    """
    result = {
        'total_fetched': len(xg_users),
        'mapped_count': 0,
        'skipped_count': 0,
        'skipped_by_reason': {},
        'existing_count': 0,
        'missing_local_count': 0,
        'would_update_count': 0,
        'conflicts': [],
        'warnings': []
    }

    for xg_user in xg_users:
        mapped = map_xg_user_to_internal(xg_user)

        # mapper skip
        if mapped['skip_reason']:
            result['skipped_count'] += 1
            reason = mapped['skip_reason']
            result['skipped_by_reason'][reason] = result['skipped_by_reason'].get(reason, 0) + 1
            continue

        result['mapped_count'] += 1
        user_id = mapped['user_id']

        # 检查本地是否存在
        try:
            local_user = User.objects.get(user_id=user_id)
            result['existing_count'] += 1

            # 角色冲突检查
            if local_user.role != 'student':
                result['conflicts'].append({
                    'user_id': user_id,
                    'reason': 'role_mismatch',
                    'local_role': local_user.role,
                    'api_role': mapped['role']
                })
                continue

            # 已存在学生，计入would_update
            result['would_update_count'] += 1

        except User.DoesNotExist:
            # 本地不存在，Phase 1不创建
            result['missing_local_count'] += 1
            result['warnings'].append(f"would_create_but_blocked: {user_id} (lacks class_id/is_graduating/graduation_year)")

    # 模型字段gap警告
    if result['would_update_count'] > 0:
        result['warnings'].append("User model lacks phone/email/department fields - cannot persist API supplemental data")

    return result
