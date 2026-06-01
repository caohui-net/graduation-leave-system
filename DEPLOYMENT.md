# Deployment Guide

## Quick Start

### 1. Environment Setup

Copy environment template:
```bash
cp .env.example .env.docker
```

Edit `.env.docker` and set:
- `SECRET_KEY` (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DB_PASSWORD` (secure password)
- `JWT_SECRET_KEY` (random string)
- `ALLOWED_HOSTS` (your domain)

### 2. Start Services

```bash
docker compose up -d
```

Wait for services to be healthy (~10 seconds).

### 3. Database Migration

```bash
docker compose exec backend python manage.py migrate
```

### 4. Load Initial Data

**Option A: Seed test data (development)**
```bash
docker compose exec backend python manage.py seed_data
```

**Option B: Import production data (production)**
```bash
# 1. Import counselors first
docker compose exec backend python manage.py import_csv \
  --counselors /path/to/counselors.csv \
  --dry-run  # Preview first

docker compose exec backend python manage.py import_csv \
  --counselors /path/to/counselors.csv  # Apply

# 2. Import class mappings
docker compose exec backend python manage.py import_csv \
  --mappings /path/to/mappings.csv

# 3. Import students
docker compose exec backend python manage.py import_csv \
  --students /path/to/students.csv
```

CSV templates: `backend/data/templates/*.csv`

### 5. Verify Installation

Run smoke test:
```bash
./tests/smoke_test.sh
```

Expected output: All tests pass, no errors.

### 6. Access Application

- Backend API: http://localhost:8001
- Admin: http://localhost:8001/admin

## Data Import

### CSV Field Requirements

**counselors.csv:**
- employee_id (required)
- name (required)
- department (optional)

**mappings.csv:**
- class_id (required)
- counselor_employee_id (required)

**students.csv:**
- student_id (required)
- name (required)
- class_id (required)
- is_graduating (required, true/false)
- graduation_year (required)

### Import Order

**CRITICAL:** Import in this order:
1. Counselors (creates counselor accounts)
2. Mappings (links classes to counselors)
3. Students (validates class mappings exist)

### Dry-Run Mode

Always preview before applying:
```bash
docker compose exec backend python manage.py import_csv \
  --students students.csv --dry-run
```

## Troubleshooting

**Database connection failed:**
```bash
docker compose logs db
docker compose restart db
```

**Migration failed:**
```bash
docker compose exec backend python manage.py showmigrations
docker compose exec backend python manage.py migrate --fake-initial
```

**Import validation errors:**
Check error summary in output. Common issues:
- Missing required fields
- Duplicate IDs
- Counselor not found (for mappings)
- Class mapping missing (for students)

## Maintenance

**View logs:**
```bash
docker compose logs -f backend
```

**Reset database:**
```bash
docker compose down -v
docker compose up -d
docker compose exec backend python manage.py migrate
```

**Backup media files:**
```bash
docker compose exec backend tar czf /tmp/media-backup.tar.gz /app/media
docker compose cp backend:/tmp/media-backup.tar.gz ./media-backup.tar.gz
```
