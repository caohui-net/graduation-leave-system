#!/usr/bin/env python
"""学工系统API诊断脚本"""
import sys
import os
import json
import argparse

# Django setup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.users.integrations.xg_user_client import generate_sign, XGUserAPIConfig, XGUserAPIClient


def check_env():
    """检查环境配置"""
    try:
        config = XGUserAPIConfig()
        return {'status': 'OK', 'config': config}
    except ValueError as e:
        return {'status': 'ERROR', 'error': 'config_error', 'message': str(e)}


def check_signature():
    """检查官方签名样例"""
    try:
        sign = generate_sign('6bd1b3fb015b4e72a85769e9d64405d1', '1573702840', 'Gc6LGToDKy2AMhXE', 'sha1')
        expected = 'baeaa6693fb7b9914c9ff9e388654878b8754515'
        if sign == expected:
            return {'status': 'OK'}
        return {'status': 'ERROR', 'error': 'sign_error', 'message': f'Expected {expected}, got {sign}'}
    except Exception as e:
        return {'status': 'ERROR', 'error': 'sign_error', 'message': str(e)}


def dry_run(config):
    """Dry-run模式：显示请求摘要不发送"""
    client = XGUserAPIClient(config)
    headers = client.build_headers(timestamp='1234567890', rand_str='test_rand_str')
    data = client.build_form_data()

    return {
        'status': 'skipped',
        'reason': 'XG_RUN_LIVE_API_TEST != 1',
        'request_summary': {
            'method': 'POST',
            'url': config.url,
            'headers': {k: v if k != 'sign' else f"{v[:6]}..." for k, v in headers.items()},
            'data': data
        }
    }


def live_probe(config, timeout):
    """Live probe：真实API调用"""
    client = XGUserAPIClient(config)

    try:
        result = client.fetch_users_page(page=1, page_num=1, timeout=timeout)

        if result['code'] == 200:
            users = result.get('users', [])
            sample = {}
            if users:
                user = users[0]
                sample = {
                    'name': user.get('name', '')[:1] + '*' if user.get('name') else None,
                    'number': user.get('number', '')[:2] + '****' if user.get('number') else None,
                    'phone': user.get('phone', '')[:3] + '****' + user.get('phone', '')[-4:] if user.get('phone') and len(user.get('phone', '')) > 7 else None
                }

            return {
                'status': 'success',
                'http_status': 200,
                'business_code': result['code'],
                'pagination': {
                    'current_page': result.get('current_page'),
                    'per_page': result.get('per_page'),
                    'total': result.get('total')
                },
                'fields_coverage': {
                    'name': any('name' in u for u in users),
                    'number': any('number' in u for u in users),
                    'phone': any('phone' in u for u in users)
                },
                'sample': sample
            }

        elif 'tenant' in result.get('msg', '').lower() or '租户' in result.get('msg', ''):
            return {'status': 'ERROR', 'error': 'tenant_invalid', 'code': result['code'], 'message': result.get('msg')}
        elif result['code'] in (401, 403):
            return {'status': 'ERROR', 'error': 'auth_failed', 'code': result['code'], 'message': result.get('msg')}
        elif result['code'] in (404, 40001, 40002):
            return {'status': 'ERROR', 'error': 'tenant_invalid', 'code': result['code'], 'message': result.get('msg')}
        else:
            return {'status': 'ERROR', 'error': 'business_error', 'code': result['code'], 'message': result.get('msg')}

    except ValueError as e:
        return {'status': 'ERROR', 'error': 'unexpected_schema', 'message': str(e)}
    except Exception as e:
        error_type = 'network_error' if 'timeout' in str(e).lower() or 'connection' in str(e).lower() else 'http_error'
        return {'status': 'ERROR', 'error': error_type, 'message': str(e)}


def format_text(results):
    """文本格式输出"""
    lines = []
    lines.append(f"配置: {results['env']['status']}")
    if results['env']['status'] == 'ERROR':
        lines.append(f"  错误: {results['env']['message']}")
        return '\n'.join(lines)

    lines.append(f"签名样例: {results['signature']['status']}")
    if results['signature']['status'] == 'ERROR':
        lines.append(f"  错误: {results['signature']['message']}")

    if results['live']['status'] == 'skipped':
        lines.append(f"Live调用: {results['live']['status']} ({results['live']['reason']})")
        summary = results['live']['request_summary']
        lines.append(f"请求摘要: {summary['method']} {summary['url']}")
        lines.append(f"  Headers: {summary['headers']}")
        lines.append(f"  Data: {summary['data']}")
    elif results['live']['status'] == 'success':
        lines.append(f"HTTP状态: {results['live']['http_status']}")
        lines.append(f"业务码: {results['live']['business_code']}")
        pag = results['live']['pagination']
        lines.append(f"分页: current_page={pag['current_page']} per_page={pag['per_page']} total={pag['total']}")
        cov = results['live']['fields_coverage']
        lines.append(f"字段覆盖: name={cov['name']} number={cov['number']} phone={cov['phone']}")
        lines.append(f"样本: {results['live']['sample']}")
    else:
        lines.append(f"Live调用: {results['live']['status']}")
        lines.append(f"  错误类型: {results['live']['error']}")
        lines.append(f"  错误信息: {results['live']['message']}")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='学工系统API诊断工具')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='输出格式')
    parser.add_argument('--timeout', type=int, default=5, help='请求超时（秒）')
    args = parser.parse_args()

    results = {
        'env': check_env(),
        'signature': {},
        'live': {}
    }

    if results['env']['status'] == 'ERROR':
        if args.format == 'json':
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(format_text(results))
        sys.exit(1)

    results['signature'] = check_signature()

    config = results['env']['config']
    if config.is_live_test_enabled():
        results['live'] = live_probe(config, args.timeout)
    else:
        results['live'] = dry_run(config)

    # Remove config object from results (not JSON serializable)
    if 'config' in results['env']:
        del results['env']['config']

    if args.format == 'json':
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_text(results))

    if results['live'].get('status') == 'ERROR' or results['signature']['status'] == 'ERROR':
        sys.exit(1)


if __name__ == '__main__':
    main()
