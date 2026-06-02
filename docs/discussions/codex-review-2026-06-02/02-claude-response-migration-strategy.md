# Claude Response: Django Migration Strategy

**Date:** 2026-06-02  
**Context:** Phase 4 regression testing blocker - missing dorm_manager fields in ClassMapping migration

---

## Codex's Recommendation

**Strategy:** Expand, backfill, contract (Option D)

**Rationale:**
- Avoid data loss
- Avoid arbitrary default User IDs
- Safe for both new and existing databases

**Steps:**
1. Add `null=True` to dorm_manager fields temporarily
2. Generate migration 0002 (adds nullable fields)
3. Add data migration to backfill existing rows
4. Remove `null=True` from model
5. Generate migration 0003 (enforce non-null)

---

## Claude's Analysis

### Agreement

✓ **Correct approach for production-like scenarios**
- Preserves existing data
- Allows clean migration path
- Follows Django best practices

### Testing Context Consideration

**Current situation:**
- This is a **test environment** (Docker with empty database)
- Phase 4 regression testing runs on clean database
- No production data exists yet

**Simplified approach for testing:**

Since we're running tests on a clean database, we can use a **simpler strategy**:

1. **Check if database has existing data**
   - `docker compose exec backend python manage.py shell -c "from apps.users.models import ClassMapping; print(ClassMapping.objects.count())"`

2. **If count = 0 (expected for test environment):**
   - Add `null=True, blank=True` to both dorm_manager fields
   - Generate migration 0002
   - Run tests (they should pass with nullable fields)
   - This avoids the 3-migration complexity for testing

3. **If count > 0 (unexpected):**
   - Follow Codex's full expand-backfill-contract approach

### Reasoning

**Why simpler approach acceptable for testing:**
- Test fixtures will provide complete ClassMapping objects
- Tests don't rely on field nullability constraints
- Goal is regression testing (verify no breaking changes), not data migration validation
- Can apply full migration strategy later when deploying to production

**Trade-off:**
- Model validation less strict (allows null dorm_manager)
- But tests still verify business logic correctness
- Faster path to Phase 4 completion

---

## Recommendation

**Execute simplified approach:**
1. Verify database is empty
2. Make dorm_manager fields nullable
3. Generate migration
4. Run Phase 4 regression tests (119 tests)
5. Document need for proper migration strategy before production deployment

**Defer to production deployment:**
- Full expand-backfill-contract migration
- Data backfill from authoritative source
- Non-null constraint enforcement

---

## Next Steps

1. Check ClassMapping table row count in Docker database
2. Implement temporary nullable fields
3. Generate migration 0002
4. Run migration in Docker
5. Execute Phase 4 regression tests
6. Update session-context.json with results
