#!/bin/bash
# 生产环境监控脚本
# 用法: bash monitor-prod.sh [持续监控分钟数，默认30]

DURATION=${1:-30}
INTERVAL=60  # 检查间隔（秒）
END_TIME=$(($(date +%s) + DURATION * 60))
LOG_FILE="/var/log/graduation/monitor_$(date +%Y%m%d_%H%M%S).log"

echo "=== 生产环境监控（持续${DURATION}分钟） ===" | tee -a "$LOG_FILE"

check_health() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local status="OK"
    local errors=""

    # 1. 健康检查
    if ! curl -f -s http://localhost:8000/api/health/ > /dev/null 2>&1; then
        status="FAILED"
        errors="${errors}健康检查失败;"
    fi

    # 2. 错误日志检查
    local error_count=$(tail -100 /var/log/graduation/error.log 2>/dev/null | grep -c ERROR || echo 0)
    if [ "$error_count" -gt 10 ]; then
        status="WARNING"
        errors="${errors}错误日志过多($error_count);"
    fi

    # 3. 数据库连接检查
    local db_conn=$(psql -U postgres -d graduation_prod -c "SELECT count(*) FROM pg_stat_activity WHERE datname='graduation_prod';" -t 2>/dev/null | xargs)
    if [ -z "$db_conn" ] || [ "$db_conn" -gt 50 ]; then
        status="WARNING"
        errors="${errors}数据库连接数异常($db_conn);"
    fi

    echo "[$timestamp] $status - 错误日志:$error_count 数据库连接:$db_conn $errors" | tee -a "$LOG_FILE"

    if [ "$status" = "FAILED" ]; then
        echo "❌ 检测到严重问题，建议执行回滚" | tee -a "$LOG_FILE"
        return 1
    fi
    return 0
}

echo "开始监控..." | tee -a "$LOG_FILE"
while [ $(date +%s) -lt $END_TIME ]; do
    if ! check_health; then
        echo "监控发现问题，停止监控" | tee -a "$LOG_FILE"
        exit 1
    fi
    sleep $INTERVAL
done

echo "✅ 监控完成，系统运行正常" | tee -a "$LOG_FILE"
