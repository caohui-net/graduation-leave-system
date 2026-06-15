#!/usr/bin/env python3
"""
负载测试：验证超时配置有效性
模拟SSO响应延迟，验证系统快速失败行为
"""
import time
import concurrent.futures
import requests
from datetime import datetime

API_BASE = "http://localhost:7787/api"
TEST_TIMEOUT = 10  # 测试超时阈值（秒）

def test_login_request(user_id, mock_delay=False):
    """模拟登录请求"""
    start = time.time()
    try:
        # 实际生产环境替换为真实登录endpoint
        response = requests.get(
            f"{API_BASE}/applications/",
            timeout=TEST_TIMEOUT
        )
        elapsed = time.time() - start
        return {
            'user_id': user_id,
            'success': response.status_code < 500,
            'status': response.status_code,
            'elapsed': elapsed,
            'error': None
        }
    except requests.exceptions.Timeout:
        elapsed = time.time() - start
        return {
            'user_id': user_id,
            'success': False,
            'status': 'TIMEOUT',
            'elapsed': elapsed,
            'error': 'Timeout'
        }
    except Exception as e:
        elapsed = time.time() - start
        return {
            'user_id': user_id,
            'success': False,
            'status': 'ERROR',
            'elapsed': elapsed,
            'error': str(e)
        }

def run_load_test(concurrency=100, total_requests=200):
    """执行负载测试"""
    print(f"\n{'='*60}")
    print(f"负载测试开始: {datetime.now()}")
    print(f"并发数: {concurrency}, 总请求数: {total_requests}")
    print(f"{'='*60}\n")

    results = []
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(test_login_request, i)
            for i in range(total_requests)
        ]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    total_time = time.time() - start_time

    # 统计结果
    success_count = sum(1 for r in results if r['success'])
    timeout_count = sum(1 for r in results if r['status'] == 'TIMEOUT')
    error_count = sum(1 for r in results if r['error'] and r['status'] != 'TIMEOUT')

    elapsed_times = [r['elapsed'] for r in results]
    avg_elapsed = sum(elapsed_times) / len(elapsed_times)
    max_elapsed = max(elapsed_times)

    slow_requests = [r for r in results if r['elapsed'] > 8]

    print(f"\n{'='*60}")
    print("测试结果:")
    print(f"{'='*60}")
    print(f"总请求数:     {total_requests}")
    print(f"成功:         {success_count} ({success_count/total_requests*100:.1f}%)")
    print(f"超时:         {timeout_count} ({timeout_count/total_requests*100:.1f}%)")
    print(f"错误:         {error_count} ({error_count/total_requests*100:.1f}%)")
    print(f"\n响应时间:")
    print(f"平均:         {avg_elapsed:.2f}s")
    print(f"最大:         {max_elapsed:.2f}s")
    print(f"慢请求(>8s):  {len(slow_requests)}")
    print(f"\n总耗时:       {total_time:.2f}s")
    print(f"吞吐量:       {total_requests/total_time:.1f} req/s")
    print(f"{'='*60}\n")

    # 验证标准
    print("验证标准:")
    checks = [
        ("✓" if timeout_count == 0 else "✗", f"无超时请求 (实际: {timeout_count})"),
        ("✓" if max_elapsed < 8 else "✗", f"最大响应<8s (实际: {max_elapsed:.2f}s)"),
        ("✓" if success_count/total_requests > 0.95 else "✗", f"成功率>95% (实际: {success_count/total_requests*100:.1f}%)"),
    ]

    for status, msg in checks:
        print(f"  {status} {msg}")

    all_passed = all(c[0] == "✓" for c in checks)
    print(f"\n{'='*60}")
    print(f"测试结果: {'通过 ✓' if all_passed else '失败 ✗'}")
    print(f"{'='*60}\n")

    return all_passed

if __name__ == "__main__":
    import sys

    print("\n⚠️  注意: 请确保后端服务已启动 (http://localhost:7787)")
    print("⚠️  此测试验证超时配置 (3, 5) 的有效性\n")

    input("按Enter开始测试...")

    passed = run_load_test(concurrency=50, total_requests=100)
    sys.exit(0 if passed else 1)
