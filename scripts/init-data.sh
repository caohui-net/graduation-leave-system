#!/bin/bash
# 数据初始化脚本 - 开发/staging/生产通用
# 用法: ./scripts/init-data.sh [staging|production]
# 开发环境: ./scripts/init-data.sh (无参数)
set -euo pipefail

ENV=${1:-local}
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== 数据初始化: $ENV ==="

run_manage() {
    case "$ENV" in
        production)
            ssh caohui@172.17.12.196 "docker exec production-backend-1 python manage.py shell -c \"$1\""
            ;;
        staging)
            ssh caohui@172.17.12.196 "docker exec staging-backend-1 python manage.py shell -c \"$1\""
            ;;
        *)
            cd "$PROJECT_ROOT/backend" && venv/bin/python manage.py shell -c "$1"
            ;;
    esac
}

copy_file() {
    local src="$1" dest="$2" container="$3"
    case "$ENV" in
        production|staging)
            scp "$src" "caohui@172.17.12.196:/tmp/$(basename $src)"
            ssh caohui@172.17.12.196 "docker cp /tmp/$(basename $src) $container:/tmp/$(basename $src)"
            ;;
        *)
            cp "$src" "$dest"
            ;;
    esac
}

CONTAINER=$( [ "$ENV" = "production" ] && echo "production-backend-1" || echo "staging-backend-1" )

# 1. 导入辅导员（从Excel）
echo "[1/3] 导入辅导员..."
EXCEL="$PROJECT_ROOT/backend/docs/20260622-暑期留校名单审批的辅导员教师信息统计表.xlsx"
COUNSELORS_JSON="/tmp/counselors_init.json"

python3 - <<'PYEOF' "$EXCEL" "$COUNSELORS_JSON"
import sys, json, re, openpyxl
wb = openpyxl.load_workbook(sys.argv[1])
ws = wb.active
out = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if not row[0]: continue
    dept = str(row[1]).strip()
    names = [n.strip() for n in re.split(r'[，,\n]+', str(row[2]).strip()) if n.strip()]
    ids   = [i.strip() for i in re.split(r'[\s，,\n]+', str(row[3]).strip()) if i.strip()]
    phones = [p.strip() for p in re.split(r'[\s，,\n]+', str(row[4]).strip()) if row[4] and p.strip()] if row[4] else []
    for i, uid in enumerate(ids):
        out.append({'user_id': uid, 'name': names[i] if i < len(names) else names[-1],
                    'department': dept, 'phone': phones[i] if i < len(phones) else ''})
with open(sys.argv[2], 'w') as f:
    json.dump(out, f, ensure_ascii=False)
print(f"  解析 {len(out)} 名辅导员")
PYEOF

copy_file "$COUNSELORS_JSON" "$COUNSELORS_JSON" "$CONTAINER"

run_manage "
import json
from apps.users.models import User
with open('/tmp/counselors_init.json') as f:
    counselors = json.load(f)
created = updated = 0
for c in counselors:
    obj, is_new = User.objects.update_or_create(
        user_id=c['user_id'],
        defaults={'name': c['name'], 'role': 'counselor', 'department': c['department'],
                  'phone': c['phone'], 'email': '', 'building': '', 'active': True}
    )
    if is_new:
        obj.set_password(c['user_id']); obj.save(update_fields=['password']); created += 1
    else:
        updated += 1
print(f'辅导员: 新建{created} 更新{updated}')
"

# 2. 学生辅导员分配
echo "[2/3] 按院系分配辅导员..."
run_manage "
from apps.users.models import User
counselors = list(User.objects.filter(role='counselor').values('user_id','department'))
cids = set(c['user_id'] for c in counselors)
# 院系名称映射（处理同义名称）
dept_map = {'地理与旅游学院': '旅游文化与地理科学学院', '建筑工程学院': '建筑与工程学院'}
assigned = 0
for c in counselors:
    dept = c['department']
    n = User.objects.filter(role='student', department=dept).exclude(class_id__in=cids).update(class_id=c['user_id'])
    assigned += n
    # 同义院系名
    for alias, canonical in dept_map.items():
        if canonical == dept:
            n2 = User.objects.filter(role='student', department=alias).exclude(class_id__in=cids).update(class_id=c['user_id'])
            assigned += n2
total = User.objects.filter(role='student').count()
with_c = User.objects.filter(role='student', class_id__in=list(cids)).count()
print(f'学生总数:{total} 已分配:{with_c} 新增分配:{assigned} 未分配:{total-with_c}')
"

# 3. 功能开关
echo "[3/3] 检查功能开关..."
case "$ENV" in
    production)
        ssh caohui@172.17.12.196 "grep -q 'ENABLE_STAY_SCHOOL' /opt/graduation-leave-system/production/.env.docker \
            || echo 'ENABLE_STAY_SCHOOL=true' >> /opt/graduation-leave-system/production/.env.docker"
        echo "  ENABLE_STAY_SCHOOL: OK"
        ;;
    staging)
        ssh caohui@172.17.12.196 "grep -q 'ENABLE_STAY_SCHOOL' /opt/graduation-leave-system/staging/.env.docker \
            || echo 'ENABLE_STAY_SCHOOL=true' >> /opt/graduation-leave-system/staging/.env.docker"
        echo "  ENABLE_STAY_SCHOOL: OK"
        ;;
    *)
        echo "  本地开发环境，请检查 .env 中 ENABLE_STAY_SCHOOL=true"
        ;;
esac

echo "=== 初始化完成: $ENV ==="
