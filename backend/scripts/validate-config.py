#!/usr/bin/env python3
"""
配置校验脚本 - 验证环境配置完整性和正确性
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# 必需配置项（所有环境）
REQUIRED_FIELDS = [
    'DB_HOST',
    'DB_NAME',
    'DB_USER',
    'DB_PASSWORD',
    'SECRET_KEY',
    'ALLOWED_HOSTS',
]

# 条件必需配置（根据feature flag）
CONDITIONAL_FIELDS = {
    'SSO_ENABLED': ['SSO_QGL_APP_ID', 'SSO_QGL_APP_SECRET', 'SSO_QGL_BASE_URL', 'SSO_CALLBACK_URL'],
    'XG_API_ENABLED': ['XG_API_BASE_URL', 'XG_API_TENANT_CODE', 'XG_API_CLIENT_ID', 'XG_API_CLIENT_SECRET'],
}

# 安全检查项
SECURITY_CHECKS = {
    'SECRET_KEY': lambda v: len(v) >= 50,
    'DB_PASSWORD': lambda v: len(v) >= 8,
    'DEBUG': lambda v: v.lower() in ['false', '0', 'no'],
}


def load_env_file(file_path: Path) -> Dict[str, str]:
    """加载.env文件"""
    env_vars = {}
    if not file_path.exists():
        return env_vars

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

    return env_vars


def validate_required_fields(env_vars: Dict[str, str]) -> List[str]:
    """检查必需字段"""
    missing = []
    for field in REQUIRED_FIELDS:
        if not env_vars.get(field):
            missing.append(field)
    return missing


def validate_conditional_fields(env_vars: Dict[str, str]) -> List[str]:
    """检查条件必需字段"""
    missing = []
    for flag, fields in CONDITIONAL_FIELDS.items():
        if env_vars.get(flag, 'false').lower() in ['true', '1', 'yes']:
            for field in fields:
                if not env_vars.get(field):
                    missing.append(f"{field} (required when {flag}=true)")
    return missing


def validate_security(env_vars: Dict[str, str]) -> List[Tuple[str, str]]:
    """安全检查"""
    issues = []
    for field, check_fn in SECURITY_CHECKS.items():
        value = env_vars.get(field, '')
        if value and not check_fn(value):
            if field == 'SECRET_KEY':
                issues.append((field, 'Must be at least 50 characters'))
            elif field == 'DB_PASSWORD':
                issues.append((field, 'Must be at least 8 characters'))
            elif field == 'DEBUG':
                issues.append((field, 'Must be false in production'))
    return issues


def validate_urls(env_vars: Dict[str, str]) -> List[Tuple[str, str]]:
    """URL格式检查"""
    issues = []
    url_fields = ['SSO_QGL_BASE_URL', 'XG_API_BASE_URL', 'CORS_ALLOWED_ORIGINS']

    for field in url_fields:
        value = env_vars.get(field, '')
        if value and not (value.startswith('http://') or value.startswith('https://')):
            issues.append((field, 'Must start with http:// or https://'))

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate-config.py <env_file>")
        print("Example: python validate-config.py .env.production")
        sys.exit(1)

    env_file = Path(sys.argv[1])

    if not env_file.exists():
        print(f"❌ Error: {env_file} not found")
        sys.exit(1)

    print(f"Validating {env_file}...")
    print("=" * 50)

    # 加载配置
    env_vars = load_env_file(env_file)

    has_errors = False

    # 必需字段检查
    missing = validate_required_fields(env_vars)
    if missing:
        has_errors = True
        print("❌ Missing required fields:")
        for field in missing:
            print(f"   - {field}")

    # 条件必需字段检查
    conditional_missing = validate_conditional_fields(env_vars)
    if conditional_missing:
        has_errors = True
        print("\n❌ Missing conditional fields:")
        for field in conditional_missing:
            print(f"   - {field}")

    # 安全检查
    security_issues = validate_security(env_vars)
    if security_issues:
        has_errors = True
        print("\n❌ Security issues:")
        for field, issue in security_issues:
            print(f"   - {field}: {issue}")

    # URL格式检查
    url_issues = validate_urls(env_vars)
    if url_issues:
        has_errors = True
        print("\n❌ URL format issues:")
        for field, issue in url_issues:
            print(f"   - {field}: {issue}")

    # 配置统计
    print("\n" + "=" * 50)
    print(f"Total fields: {len(env_vars)}")
    print(f"Required fields: {len(REQUIRED_FIELDS)}")
    print(f"Filled fields: {sum(1 for v in env_vars.values() if v)}")

    if has_errors:
        print("\n❌ Validation failed")
        sys.exit(1)
    else:
        print("\n✅ Validation passed")
        sys.exit(0)


if __name__ == '__main__':
    main()
