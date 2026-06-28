"""E2E测试配置"""
import os

# 环境配置
BASE_URL = os.getenv('E2E_BASE_URL', 'http://localhost:7788')
API_URL = os.getenv('E2E_API_URL', 'http://localhost:8000')
CDP_URL = os.getenv('BU_CDP_URL', 'http://127.0.0.1:9222')

# 测试账号
TEST_ACCOUNTS = {
    'student': {
        'user_id': '2020001',
        'password': '2020001',
        'name': '张三',
        'role': 'student'
    },
    'counselor': {
        'user_id': '19970545',
        'password': '123456',
        'name': '辅导员',
        'role': 'counselor'
    },
    'dorm_manager': {
        'user_id': 'M001',
        'password': 'M001',
        'name': '宿管员',
        'role': 'dorm_manager'
    }
}

# 超时配置
TIMEOUTS = {
    'page_load': 5,
    'action': 2,
    'api_call': 10
}
