#!/usr/bin/env bash
"""业务流程测试运行器

用法:
  ./run_tests.sh [test_name]

示例:
  ./run_tests.sh              # 运行所有测试
  ./run_tests.sh login        # 仅运行登录测试
  ./run_tests.sh stay         # 仅运行留校审批测试
"""

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查browser-harness是否可用
if ! command -v browser-harness &> /dev/null; then
    echo "❌ browser-harness未安装"
    echo "安装: uv tool install browser-harness"
    exit 1
fi

# 检查CDP端点
CDP_URL="${BU_CDP_URL:-http://127.0.0.1:9222}"
echo "🔧 CDP端点: $CDP_URL"

# 运行测试
TEST_NAME="${1:-all}"

run_test() {
    local test_file=$1
    local test_name=$(basename "$test_file" .py)

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🧪 运行测试: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    BU_CDP_URL="$CDP_URL" browser-harness < "$test_file"

    if [ $? -eq 0 ]; then
        echo "✓ $test_name 通过"
        return 0
    else
        echo "✗ $test_name 失败"
        return 1
    fi
}

case "$TEST_NAME" in
    all)
        run_test flows/test_login.py
        run_test flows/test_stay_approval.py
        run_test flows/test_departure_application.py
        ;;
    login)
        run_test flows/test_login.py
        ;;
    stay)
        run_test flows/test_stay_approval.py
        ;;
    departure)
        run_test flows/test_departure_application.py
        ;;
    *)
        echo "❌ 未知测试: $TEST_NAME"
        echo "可用测试: all, login, stay, departure"
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 测试完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
