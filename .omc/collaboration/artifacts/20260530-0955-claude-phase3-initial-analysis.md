# Phase 3 Initial Analysis: Week 3 Day 0 Preparation

**Agent:** Claude  
**Task:** TASK-20260530-06 Phase 3  
**Timestamp:** 2026-05-30T09:55:00Z  
**Type:** Initial proposal (awaiting Codex independent review)

---

## Context

Phase 2 validation passed. Protocol proven stable. Now pilot on real Week 3 Day 0 task.

**Pilot scope:** Environment strategy + seed data + acceptance checklist

**Reference:** `docs/discussions/week3-direction-2026-05-30/06-consensus.md`

---

## Part 1: Environment Strategy Decision

### Current System Check Required

Before deciding strategy, must verify:

1. **Python environment**
   - Check: `python3 --version`
   - Required: Python 3.8+
   - Check: `pip3 list | grep -E "(Django|Flask|psycopg2)"`

2. **Database availability**
   - Check: `psql --version` or `which psql`
   - Check: PostgreSQL service status
   - Check: Can connect to local PostgreSQL

3. **Project dependencies**
   - Read: `requirements.txt` or `Pipfile`
   - Check: Are dependencies already installed locally?

### Decision Tree (from Week 3 consensus)

**Priority 1:** Local run (if dependencies exist)
- Condition: Python + Django/Flask + PostgreSQL all available locally
- Action: Run directly, no Docker
- Rationale: Fastest iteration, no container overhead

**Priority 2:** Docker PostgreSQL only
- Condition: Python/Django OK, but PostgreSQL missing or version mismatch
- Action: `docker run -d -p 5432:5432 postgres:14`
- Rationale: Isolate DB, keep app local for debugging

**Priority 3:** Full Docker Compose
- Condition: Python dependencies missing or version conflicts
- Action: Create `docker-compose.yml` with app + db
- Rationale: Reproducible environment, but slower iteration

### Proposed Action

1. Run system checks (commands above)
2. Document findings
3. Apply decision tree
4. Document chosen strategy with rationale

---

## Part 2: Seed Data Requirements

### Required Accounts (from Week 3 consensus)

**Students (minimum 2, different classes):**
- student_001: 班级A, 姓名"张三"
- student_002: 班级B, 姓名"李四"

**Counselors (minimum 2, map to classes):**
- counselor_001: 负责班级A
- counselor_002: 负责班级B

**Dean (1):**
- dean_001: 院长角色

### Required Data Mappings

**Class-Counselor mapping:**
```
班级A → counselor_001
班级B → counselor_002
```

**Role-Permission mapping:**
- Student: submit application, query own application
- Counselor: approve applications from assigned classes
- Dean: approve all applications (final approval)

### Seed Data Format

Need to determine:
1. Does project use Django fixtures (JSON/YAML)?
2. Does project use SQL seed scripts?
3. Does project use management commands (`python manage.py createsuperuser`)?

**Proposed approach:**
1. Check `backend/` or `server/` for existing seed data
2. If exists, extend it
3. If not, create minimal seed script

---

## Part 3: Acceptance Checklist Creation

### 8-Item Checklist (from Week 3 consensus)

**Must prove:**

1. **Migration success**
   - Command: `python manage.py migrate`
   - Expected: No errors, all tables created
   - Verification: `psql -c "\dt"` shows all tables

2. **Seed data loaded**
   - Command: Load seed script
   - Expected: 2 students, 2 counselors, 1 dean, class mappings
   - Verification: Query user table, count by role

3. **Student login and submit**
   - Action: Login as student_001
   - Action: Submit application
   - Expected: Returns application_id, status="draft" or "pending"
   - Verification: Query applications table

4. **Counselor approval (first level)**
   - Action: Login as counselor_001
   - Action: Approve student_001's application
   - Expected: Status changes to "pending_dean" or similar
   - Verification: Only sees applications from 班级A

5. **Dean approval (final level)**
   - Action: Login as dean_001
   - Action: Approve application
   - Expected: Status changes to "approved"
   - Verification: Sees all applications

6. **Student query status**
   - Action: Login as student_001
   - Action: Query application status
   - Expected: Shows "approved"
   - Verification: Only sees own application

7. **Negative permission test**
   - Action: student_001 tries to query student_002's application
   - Expected: 403 Forbidden or empty result
   - Verification: Permission boundary enforced

8. **Mock dorm checkout**
   - Action: Trigger dorm checkout check
   - Expected: MockDormCheckoutProvider returns fixed value
   - Verification: Interface contract documented, timeout/failure branches defined

---

## Validation Checkpoints

**Before starting Phase 3 work:**
```bash
.omc/collaboration/scripts/validate-journal.sh
```

**After each major step:**
- After environment decision → validate
- After seed data creation → validate
- After checklist creation → validate

**All validations must pass.**

---

## Open Questions for Codex Review

1. **Environment strategy:** Should we check system first, or assume local and fallback to Docker?
2. **Seed data format:** Should we create Django fixtures, SQL scripts, or management commands?
3. **Checklist granularity:** Are 8 items sufficient, or should we break down further?
4. **Mock service:** Should we implement MockDormCheckoutProvider now, or just document interface?
5. **Validation frequency:** After each step, or only at phase boundaries?

---

## Proposed Next Steps

1. Run system checks (Python, PostgreSQL, dependencies)
2. Document findings in artifact
3. Decide environment strategy
4. Create seed data specification
5. Create acceptance checklist document
6. Hand off to Codex for independent review

---

## Request for Codex

**Please review independently:**
- Do you agree with the decision tree priority?
- Do you see gaps in seed data requirements?
- Do you think 8-item checklist is sufficient?
- Do you have concerns about validation frequency?
- Do you see risks I missed?

**Critical thinking encouraged:**
- Challenge assumptions
- Propose alternatives
- Identify edge cases
- Question feasibility

**Goal:** Reach consensus through discussion, not rubber-stamp approval.

---

**Status:** Awaiting Codex independent review
