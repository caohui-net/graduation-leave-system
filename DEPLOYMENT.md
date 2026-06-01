# Deployment Guide

## Quick Start

### 1. Environment Setup

Copy environment template:
```bash
cp .env.example .env.docker
```

Edit `.env.docker` and configure environment variables (see Environment Variables section below).

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

**Prerequisites for smoke test:**
- Clean database (no existing applications for test users 2020001, 2020002)
- Seeded test data (users, class mappings)

**Option A: Auto-reset (recommended for first run)**
```bash
SMOKE_RESET=1 ./tests/smoke_test.sh
```

This will automatically:
1. Stop containers and remove volumes
2. Restart containers
3. Run migrations
4. Seed test data
5. Run smoke test

**Option B: Manual verification (if environment is already clean)**
```bash
./tests/smoke_test.sh
```

**Expected output:** All tests pass, no errors.

### 6. Access Application

- Backend API: http://localhost:8001
- Admin: http://localhost:8001/admin
- API Schema: http://localhost:8001/api/schema/swagger-ui/

## Environment Variables

### Core Settings

| Variable | Purpose | Default | Production Required |
|----------|---------|---------|---------------------|
| `SECRET_KEY` | Django secret key for cryptographic signing | `django-insecure-dev-key-change-in-production` | **Yes** - Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | Enable debug mode | `True` | **No** - Set to `False` in production |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` | **Yes** - Set to your domain(s) |

### Database Settings

| Variable | Purpose | Default | Production Required |
|----------|---------|---------|---------------------|
| `DB_NAME` | PostgreSQL database name | `graduation_leave` | **No** - Default is fine |
| `DB_USER` | PostgreSQL username | `postgres` | **Yes** - Use dedicated user |
| `DB_PASSWORD` | PostgreSQL password | `postgres` | **Yes** - Use secure password |
| `DB_HOST` | PostgreSQL host | `localhost` | **No** - Use `db` for Docker |
| `DB_PORT` | PostgreSQL port | `5432` | **No** - Default is fine |

### CORS Settings

| Variable | Purpose | Default | Production Required |
|----------|---------|---------|---------------------|
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed origins | `http://localhost:3000,http://127.0.0.1:3000` | **Yes** - Set to your frontend URL(s) |

### Notes

- **JWT Settings:** JWT tokens use `SECRET_KEY` for signing (no separate `JWT_SECRET_KEY` needed)
- **Media Files:** `MEDIA_URL=/media/` and `MEDIA_ROOT=/app/media` are hardcoded (not configurable via env vars)
- **Unused Variables:** `.env.example` may reference `JWT_SECRET_KEY`, `REDIS_URL`, `CELERY_BROKER_URL` - these are not currently read by the application

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

### Application Errors

**409 Conflict - Duplicate Application**
```json
{"error": {"code": "CONFLICT", "message": "You already have a pending or approved application"}}
```
**Cause:** Student already has an active application (status: pending_counselor, pending_dean, or approved)

**Solution:** Student must wait for current application to be rejected before submitting a new one, or contact administrator to check application status.

**422 Unprocessable Entity - Dorm Clearance Blocked**
```json
{"error": {"code": "DORM_BLOCKED", "message": "Cannot submit application: dorm clearance not completed"}}
```
**Cause:** Student's dorm checkout status is not `completed` (checked via mock provider or real dorm system API)

**Solution:** Student must complete dorm clearance first. Check dorm system status or contact dorm administrator.

**401 Unauthorized - JWT Expired**
```json
{"detail": "Given token not valid for any token type"}
```
**Cause:** JWT access token expired (default lifetime: 24 hours)

**Solution:** Re-login to get new token. Frontend should implement automatic token refresh or redirect to login page.

**403 Forbidden - Cross-Role Access**
```json
{"error": {"code": "FORBIDDEN", "message": "You do not have permission to perform this action"}}
```
**Common scenarios:**
- Student trying to access another student's application
- Counselor trying to approve application from different class
- Dean trying to approve counselor-step approval

**Solution:** Verify user role and permissions. Check that counselor is assigned to the student's class via class mappings.

### Media/Attachment Errors

**403 Forbidden - Media Access Denied**

**Cause:** User trying to access attachment they don't have permission to view

**Solution:** Verify RBAC rules:
- Students can only access their own application's attachments
- Counselors can access attachments for applications in their assigned classes
- Deans can access attachments for applications with pending dean approval

**404 Not Found - Attachment Missing**

**Cause:** Attachment file deleted from filesystem or soft-deleted in database

**Solution:** Check `MEDIA_ROOT` directory (`/app/media` in Docker) and verify attachment record in database.

### Infrastructure Errors

**Docker Container Startup Failed**
```bash
docker compose ps  # Check container status
docker compose logs backend  # Check backend logs
```
**Common causes:**
- Port 8001 already in use: Change `ports` in `docker-compose.yml`
- Database not ready: Wait 10 seconds and retry
- Migration failed: Check database connection and run `docker compose exec backend python manage.py migrate`

**Database Connection Failed**
```bash
docker compose logs db
docker compose restart db
```
**Common causes:**
- Database container not running: `docker compose up -d db`
- Wrong credentials: Check `DB_USER`, `DB_PASSWORD` in `.env.docker`
- Wrong host: Use `DB_HOST=db` (not `localhost`) in Docker environment

**API Schema Page Not Loading**

**URL:** http://localhost:8001/api/schema/swagger-ui/

**Common causes:**
- Backend not running: `docker compose ps`
- Wrong port: Check `docker-compose.yml` port mapping (default: 8001)
- drf-spectacular not installed: `docker compose exec backend pip list | grep spectacular`

**Solution:** Restart backend container and verify schema endpoint returns 200:
```bash
curl -I http://localhost:8001/api/schema/
```

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
