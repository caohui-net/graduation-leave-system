# Codex Review - Post Option E-lite Next Strategy

**Review date:** 2026-06-02  
**Reviewer:** Codex  
**Reviewed document:** `docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md`  
**Review type:** Strategy / execution-plan review  

---

## Review Conclusion

**Decision:** support Option A, with required modifications.

Option A is the best substantive next step among the four options because it has clear internal value, no external dependency, and follows naturally from the OpenAPI baseline. However, the current execution plan is too optimistic and has several schema-accuracy risks. I recommend executing **B-mini first**, then a narrowed **A-corrected** pass:

1. Fix the known smoke typo in `tests/smoke_test.sh` first. This is a low-risk 5-10 minute cleanup and removes noise before another documentation/validation pass.
2. Proceed with API Schema P1, but treat it as schema fidelity work, not a broad behavior change.
3. Do not start Track 3 Phase 2B/2C yet.
4. Do not use passive waiting as the main strategy.

Estimated time should be adjusted from **2-3 hours** to **3-4 hours** if the work includes accurate serializers, binary/multipart schema, warning-free schema generation, docs updates, and validation.

---

## Findings

### P1 - Login schema plan does not match the current API

**Location:** `backend/apps/users/urls.py:5`, `backend/apps/users/views.py:10`, `backend/apps/users/views.py:13`, `backend/apps/users/views.py:14`, `backend/apps/users/serializers.py:20`

The plan describes `/api/auth/login/` and a token response containing a refresh token. The current route is `path('login', ...)`, so the canonical route is `/api/auth/login` without a trailing slash. The current login serializer returns `access_token`, `token_type`, and `user`; it does not return `refresh_token`.

The error shape also differs from the rest of the API: invalid login currently returns raw serializer errors from `serializer.errors`, not the project error envelope.

**Required adjustment:** document the current route and response exactly, or intentionally change the login behavior with tests. Do not publish an OpenAPI response that claims a refresh token or uniform error envelope unless the code is changed to match.

---

### P1 - Uniform `ErrorSerializer` can make the schema lie unless auth/framework errors are handled

**Location:** `backend/apps/applications/views.py:79`, `backend/apps/applications/views.py:93`, `backend/apps/attachments/views.py:43`, `backend/apps/notifications/views.py:67`, `backend/apps/users/views.py:14`

Most application-level errors already use:

```json
{"error": {"code": "...", "message": "...", "details": {...}}}
```

But serializer errors and DRF/framework-level errors are not uniformly wrapped everywhere. In particular, login validation errors currently return raw serializer errors, and unauthenticated `401` responses are produced by DRF authentication before view code runs.

**Required adjustment:** choose one of these two approaches before adding `401`/`400` responses everywhere:

- **Documentation-only approach:** use `ErrorSerializer` only for endpoints and status codes that actually return the project envelope; document DRF default auth errors separately.
- **Behavioral approach:** add a global exception/authentication error handler and update tests so framework errors also use the project envelope.

For this phase, I recommend the documentation-only approach unless the user explicitly authorizes an API behavior normalization pass.

---

### P1 - Multi-method function views need per-method schema, not one generic decorator

**Location:** `backend/apps/applications/views.py:18`, `backend/apps/applications/views.py:20`, `backend/apps/attachments/views.py:17`, `backend/apps/attachments/views.py:20`

`applications_view` dispatches both `GET` and `POST`; `attachments_view` dispatches both `GET` and `POST`. A single generic `@extend_schema` risks mixing list and create/upload request/response schemas.

**Required adjustment:** use method-scoped decorators, for example stacked `@extend_schema(methods=['GET'], ...)` and `@extend_schema(methods=['POST'], ...)`, or refactor to class-based/generic views only if that remains tightly scoped. Keep behavior unchanged unless tests cover the refactor.

---

### P1 - Attachment endpoint ownership is mislabeled in the plan

**Location:** `backend/apps/attachments/views.py:17`, `backend/apps/attachments/views.py:87`, `backend/apps/attachments/views.py:118`, `docs/api/api-schema-todo.md:141`

The attachment list/upload URL is nested under `/api/applications/{application_id}/attachments/`, but the implementation lives in `apps.attachments`, not `apps.applications`. The plan lists it under the applications module and then again under attachments work, which can lead to duplicated or misplaced schema definitions.

**Required adjustment:** handle all attachment schemas in `apps.attachments`:

- `GET /api/applications/{application_id}/attachments/`
- `POST /api/applications/{application_id}/attachments/`
- `GET /api/attachments/{attachment_id}/download/`
- `DELETE /api/attachments/{attachment_id}/`

---

### P2 - Notification pagination schema in the plan is not the current response

**Location:** `backend/apps/notifications/views.py:22`, `backend/apps/notifications/views.py:23`, `backend/apps/notifications/views.py:37`

Notifications use custom `limit`/`offset` parsing and return only:

```json
{"count": 100, "results": [...]}
```

They do not return `next` or `previous`, unlike DRF limit-offset pagination.

**Required adjustment:** document the current custom response shape, or change the API to use a DRF paginator with tests. For this phase, schema should match the current response.

---

### P2 - Acceptance criterion "`Swagger UI` no generator warnings" is not precise

**Location:** `docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md`

Generator warnings are emitted during schema generation, not by Swagger UI as an acceptance surface.

**Required adjustment:** validate with a command such as schema generation plus warning inspection, and separately smoke-check `/api/schema/` and `/api/schema/swagger-ui/` accessibility. The acceptance criterion should be "schema generation has no warnings for the 13 function-based views and no operationId collision warnings."

---

## Revised Execution Plan

### Step 0 - Smoke typo cleanup

Fix `STUDENT_NOTIF_COUNT` in `tests/smoke_test.sh`. Either assign it before line 255 or remove that echo if the final unread-count assertion is the real check. Run the smoke test once with the existing reset strategy if the environment is available.

### Step 1 - Schema inventory and exact contract alignment

Before editing decorators, reconcile the schema plan with:

- `backend/apps/*/urls.py`
- `backend/apps/*/views.py`
- `backend/apps/*/serializers.py`
- `docs/api/contract-v0.2.md`
- `docs/api/contract-v0.3.md`
- `docs/api/notification-contract-v0.1.md`

Pay special attention to login path/response, notification pagination, attachment wrapper shape, and error envelopes.

### Step 2 - Add schema-only serializers/helpers

Create schema-only serializers where wrappers are needed:

- `ErrorBodySerializer` / `ErrorSerializer`
- paginated application list response if not inferred correctly
- paginated approval list response if not inferred correctly
- notification list response with `count` and `results`
- attachment list response with `attachments`
- delete `204` response
- binary download response

Keep these serializers clearly separated from behavior serializers if they are documentation-only.

### Step 3 - Add method-scoped `extend_schema`

Decorate all 13 function-based API views. For the two dispatchers, use method-specific schemas:

- `applications_view`: GET list, POST create
- `attachments_view`: GET list, POST multipart upload

Set explicit operation IDs for all operations, not only the current collision pair. This avoids client-generation churn later.

### Step 4 - Validate mechanically

Recommended checks:

- Generate schema and inspect warnings.
- Verify `/api/schema/` returns 200.
- Verify `/api/schema/swagger-ui/` returns 200.
- Assert the path/operation count remains intentional.
- Assert operation IDs are unique.
- Run focused backend tests for touched modules if behavior was changed.
- Run smoke only if Step 0 or schema work touched runtime behavior or if environment is already available.

### Step 5 - Update docs

Update `docs/api/api-schema-todo.md` with precise status:

- P1 complete only for items actually completed.
- Keep P2 examples/examples-rich documentation separate if not implemented.
- Record any intentionally documented DRF default error responses.

---

## Answer to Review Questions

1. **Is Option A the best current choice?**  
   Yes, after a small B-mini cleanup. Option A is the best internal, non-blocked work. Track 3 Phase 2B/2C should remain deferred because dorm-blocked notification semantics and Celery introduction are larger architectural decisions.

2. **Is the execution plan feasible and is the estimate reasonable?**  
   Feasible with modifications. The estimate should be **3-4 hours**, not 2-3, if the result must be accurate and mechanically validated.

3. **Missing risks or issues?**  
   Yes: login schema mismatch, raw login errors, framework `401` error shape, multi-method dispatcher schemas, notification pagination shape, attachment module ownership, and imprecise warning acceptance.

4. **Better next-step strategy?**  
   Execute **B-mini + A-corrected**. Fix the smoke typo first, then do a schema-fidelity pass. Do not broaden into new notification features or Celery work until external blockers and explicit user authorization are resolved.

---

## Final Recommendation

Proceed with Option A only after these corrections are accepted:

- Fix the smoke typo first.
- Make schema match actual runtime behavior unless behavior changes are explicitly tested.
- Use method-scoped schema for multi-method function views.
- Document auth/login and notification pagination accurately.
- Treat uniform error schema as documentation-only for view-level errors unless a global error-envelope behavior change is authorized.
