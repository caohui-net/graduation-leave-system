# Quality Guidelines

> Code quality standards for frontend development.

---

## Overview

<!--
Document your project's quality standards here.

Questions to answer:
- What patterns are forbidden?
- What linting rules do you enforce?
- What are your testing requirements?
- What code review standards apply?
-->

(To be filled by the team)

---

## Forbidden Patterns

### Don't: Single-threaded frontend static server

**Problem**:
```python
from http.server import SimpleHTTPRequestHandler, HTTPServer
server = HTTPServer(('0.0.0.0', 7788), Handler)
```

**Why it's bad**: A slow or partial client can occupy the only request handler. In production this made `http://172.17.12.199:7788` hang while other traffic still appeared active externally.

**Instead**:
```python
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer as HTTPServer
server = HTTPServer(('0.0.0.0', 7788), Handler)
```

---

## Required Patterns

## Scenario: Frontend static service on port 7788

### 1. Scope / Trigger
- Trigger: infra integration for serving `demo-web/` through systemd on port 7788.
- Applies when changing `scripts/serve-frontend.py`, systemd frontend service files, or static hosting behavior.

### 2. Signatures
- Runtime command: `/usr/bin/python3 /home/caohui/projects/graduation-leave-system/scripts/serve-frontend.py 7788 demo-web`
- Script arguments: `serve-frontend.py [port:int=7788] [directory:str=demo-web]`
- Live service observed in production: `graduation-frontend-nocache.service`

### 3. Contracts
- Binds `0.0.0.0:<port>` so localhost, LAN IP, and mapped public IP can reach the same service.
- Serves files from requested `directory` after `os.chdir(directory)`.
- HTML and `/` responses include `Cache-Control: no-cache, no-store, must-revalidate`, `Pragma: no-cache`, and `Expires: 0`.
- `.js` and `.css` responses include `Cache-Control: public, max-age=31536000`.
- Other static resources include `Cache-Control: public, max-age=86400`.
- Must use `ThreadingHTTPServer` behavior so one slow or partial client cannot block unrelated requests.

### 4. Validation & Error Matrix
- Partial request holds socket open -> another request to `/` still returns `200` within test timeout.
- Missing file -> returns `404`; does not crash service.
- Invalid directory at startup -> process exits; systemd restart policy handles recovery.
- Port already occupied -> startup fails; operator must inspect listener before retry.

### 5. Good/Base/Bad Cases
- Good: incomplete `GET /` on one socket plus normal `GET /` on another socket returns `200` quickly.
- Base: `GET /` returns `index.html` and no-cache headers.
- Bad: single-thread `HTTPServer` blocks normal request behind slow socket.

### 6. Tests Required
- Unit/regression: `tests/test_serve_frontend.py::test_slow_client_does_not_block_other_requests`
  - Start server on ephemeral port.
  - Open socket and send incomplete request.
  - Assert normal HTTP request returns `200` and expected body before timeout.
- Runtime verification after service restart:
  - `curl --noproxy '*' http://127.0.0.1:7788/` -> 200
  - `curl --noproxy '*' http://172.17.12.199:7788/` -> 200
  - `curl --noproxy '*' http://218.75.196.218:7788/` -> 200

### 7. Wrong vs Correct
#### Wrong
```python
from http.server import SimpleHTTPRequestHandler, HTTPServer
```

#### Correct
```python
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer as HTTPServer
```

---

## Testing Requirements

- Any change to `scripts/serve-frontend.py` must run `pytest tests/test_serve_frontend.py -q` or equivalent raw pytest command.
- Any restart/runtime change for frontend port 7788 must verify localhost, LAN IP, and public mapped IP access.

---

## Code Review Checklist

- [ ] Static server uses `ThreadingHTTPServer`, not single-thread `HTTPServer`.
- [ ] Cache-Control behavior for HTML, JS/CSS, and other resources remains intact.
- [ ] Runtime service command still points at `scripts/serve-frontend.py 7788 demo-web`.
- [ ] Slow-client regression test passes.
