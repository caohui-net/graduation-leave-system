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

## Deployment: systemd User Service (graduation-frontend.service)

### Configuration Location
- Service file: `~/.config/systemd/user/graduation-frontend.service`
- Alert service: `~/.config/systemd/user/alert-graduation-frontend.service`
- Alert script: `~/.local/bin/alert-graduation-frontend.sh`

### Service Configuration
```ini
[Unit]
Description=Graduation Leave System Frontend Service
After=network.target
OnFailure=alert-graduation-frontend.service
StartLimitIntervalSec=300
StartLimitBurst=5

[Service]
Type=simple
WorkingDirectory=/home/caohui/projects/graduation-leave-system/demo-web
ExecStart=/usr/bin/python3 -m http.server 7788
Restart=always
RestartSec=10s
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

### Key Design Decisions
1. **Simple http.server over custom script**: Changed from `serve-frontend.py` to `python3 -m http.server` for simplicity and maintainability
2. **User-level systemd**: Uses `systemctl --user` to avoid sudo requirements and run under user context
3. **Auto-restart policy**: 10-second delay, max 5 failures in 300 seconds before stopping
4. **OnFailure alert**: Triggers alert service to log failures to `/tmp/graduation-frontend-alerts.log`
5. **Journal logging**: stdout/stderr to systemd journal for centralized log access

### Management Commands
```bash
systemctl --user status graduation-frontend
systemctl --user start graduation-frontend
systemctl --user stop graduation-frontend
systemctl --user restart graduation-frontend
journalctl --user -u graduation-frontend -f
```

### Verification
- Service active: `systemctl --user is-active graduation-frontend` → `active`
- Auto-start enabled: `systemctl --user is-enabled graduation-frontend` → `enabled`
- HTTP accessible: `curl http://127.0.0.1:7788/` → `200`
- Auto-restart: Kill process → recovers within 12s

---

## API Integration Patterns

### Required: Multi-step Form Submission with Attachments

**Context**: User form submissions that include file uploads must follow a multi-step flow to ensure data integrity and provide proper user feedback.

**Pattern**: Draft → Upload → Submit

```javascript
async function submitApplication() {
    // Step 1: Create draft
    btn.textContent = '创建草稿中...';
    const draft = await apiGetOrCreateDraft();
    if (!draft || draft.error) {
        showToast('创建草稿失败：' + draft.error.message, 'error');
        return;
    }

    // Step 2: Upload attachments
    if (uploadedFiles.length > 0) {
        for (let i = 0; i < uploadedFiles.length; i++) {
            btn.textContent = `上传附件 ${i+1}/${uploadedFiles.length}...`;
            const result = await apiUploadAttachment(draft.application_id, uploadedFiles[i]);
            if (!result) {
                showToast(`附件上传失败。草稿已保存(ID: ${draft.application_id})，请重试`, 'error');
                return; // Stop on failure, preserve draft
            }
        }
    }

    // Step 3: Submit final application
    btn.textContent = '提交申请中...';
    const result = await apiSubmitApplication(phone, reason, leaveDate);
}
```

**Why**: 
- Backend APIs are separated: `/applications/draft/` → `/applications/{id}/attachments/` → `/applications/`
- Fail-fast with preserved state: draft + uploaded files remain on failure
- Clear user feedback at each step

**Wrong: One-shot submission with ignored attachments**
```javascript
// ❌ Don't send files directly in FormData - backend ignores them
const formData = new FormData();
formData.append('contact_phone', phone);
files.forEach(f => formData.append('attachments', f)); // Silently dropped
await fetch('/applications/', {method: 'POST', body: formData});
```

**API timeout for file uploads**: Use 30-second timeout (not default 8s)
```javascript
const response = await fetchWithTimeout(url, options, 30000);
```

**Tested**: 
- Normal flow (2 attachments): ✓ All steps complete, attachments saved
- No attachments: ✓ Skips upload step
- Upload failure: ✓ Preserves draft, prompts retry
- Verified: commit `3d83628`, test script `/tmp/test_attachment_upload.py`

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
