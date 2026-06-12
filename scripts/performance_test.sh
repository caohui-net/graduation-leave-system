#!/bin/bash
# 性能测试脚本

API_BASE="http://localhost:7787/api"
TOKEN=""

echo "=== 毕业离校系统性能测试 ==="
echo ""

# 1. 健康检查
echo "1. 健康检查..."
time curl -s -o /dev/null -w "Status: %{http_code}, Time: %{time_total}s\n" $API_BASE/applications/

# 2. 登录性能
echo ""
echo "2. 登录接口性能测试（10次）..."
for i in {1..10}; do
  time curl -s -o /dev/null -w "Time: %{time_total}s\n" -X POST $API_BASE/sso/qingganlian/mobile/saas-login \
    -H "Content-Type: application/json" \
    -d '{"user_id":"2022180240225","token":"test"}'
done

# 3. 列表查询性能
echo ""
echo "3. 审批列表查询性能（需要token）..."
read -p "请输入测试token: " TOKEN
if [ -n "$TOKEN" ]; then
  echo "测试分页查询（limit=20）..."
  time curl -s -o /dev/null -w "Status: %{http_code}, Time: %{time_total}s\n" \
    "$API_BASE/approvals/?limit=20" \
    -H "Authorization: Bearer $TOKEN"

  echo "测试大批量查询（limit=100）..."
  time curl -s -o /dev/null -w "Status: %{http_code}, Time: %{time_total}s\n" \
    "$API_BASE/approvals/?limit=100" \
    -H "Authorization: Bearer $TOKEN"
fi

# 4. 并发测试（使用ab工具）
echo ""
echo "4. 并发性能测试..."
if command -v ab &> /dev/null; then
  echo "使用Apache Bench测试（100请求，10并发）..."
  ab -n 100 -c 10 -k $API_BASE/applications/
else
  echo "未安装ab工具，跳过并发测试"
  echo "安装: sudo apt install apache2-utils"
fi

echo ""
echo "=== 性能测试完成 ==="
echo ""
echo "性能优化建议："
echo "- API响应时间应 <200ms"
echo "- 数据库查询应使用索引"
echo "- 启用连接池（CONN_MAX_AGE=600）"
echo "- 生产环境使用Gunicorn多worker"
