# Phase 4A DevTools Setup Guide

**Purpose:** Install and configure WeChat DevTools for miniprogram validation  
**Target audience:** Operator/QA  
**Estimated time:** 30-60 minutes (first-time setup)

---

## Prerequisites

- **Operating System:** Windows 7+, macOS 10.10+, or Linux (Ubuntu 16.04+)
- **Network:** Internet access for download
- **Disk Space:** ~500MB free space
- **Backend:** Backend server running at `http://localhost:8001`

---

## Step 1: Download WeChat DevTools

### Official Download

**URL:** https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html

**Select version:**
- Windows: 64-bit or 32-bit installer
- macOS: Stable version (.dmg)
- Linux: .deb or .rpm package

**Version recommendation:** Use latest stable version (avoid beta/nightly)

---

## Step 2: Install

### Windows
1. Run downloaded `.exe` installer
2. Follow installation wizard
3. Accept license agreement
4. Choose installation directory (default: `C:\Program Files (x86)\Tencent\微信web开发者工具`)
5. Complete installation

### macOS
1. Open downloaded `.dmg` file
2. Drag "微信开发者工具" to Applications folder
3. Eject disk image
4. Open from Applications (may need to allow in Security & Privacy settings)

### Linux
```bash
# Ubuntu/Debian
sudo dpkg -i wechat_devtools_*.deb
sudo apt-get install -f  # Fix dependencies if needed

# Fedora/CentOS
sudo rpm -i wechat_devtools_*.rpm
```

---

## Step 3: First Launch

1. **Launch DevTools**
   - Windows: Start menu → 微信开发者工具
   - macOS: Applications → 微信开发者工具
   - Linux: `wechat-devtools` command or application menu

2. **Scan QR Code**
   - Use WeChat mobile app to scan login QR code
   - Confirm login on mobile device
   - Wait for authorization

3. **Skip Tutorial** (optional)
   - Click "跳过" to skip introductory tutorial

---

## Step 4: Import Project

1. **Click "导入项目" (Import Project)**

2. **Fill Project Information:**
   - **项目目录 (Project Directory):** Browse to `/home/caohui/projects/graduation-leave-system/miniprogram`
   - **AppID:** Use test AppID or "测试号" (test account)
   - **项目名称 (Project Name):** `毕业生离校申请审批系统`

3. **Click "导入" (Import)**

4. **Wait for Project Load**
   - DevTools will scan project structure
   - Check for `app.json`, `app.js`, `app.wxss`
   - Display project file tree in left sidebar

---

## Step 5: Project Configuration

### Verify project.config.json

**Location:** `miniprogram/project.config.json`

**Key settings:**
```json
{
  "appid": "test-appid-or-real-appid",
  "projectname": "graduation-leave-system",
  "miniprogramRoot": "./",
  "compileType": "miniprogram",
  "setting": {
    "es6": true,
    "postcss": true,
    "minified": false,
    "urlCheck": false
  }
}
```

**Critical setting:** `"urlCheck": false` - allows localhost API calls during development

---

## Step 6: Compile Project

1. **Click "编译" (Compile) button** (top toolbar)

2. **Observe Compilation:**
   - Console tab shows compilation progress
   - Check for errors (red text)
   - Check for warnings (yellow text)

3. **Expected Output:**
   - "编译成功" (Compilation successful)
   - No red errors in console
   - Simulator shows login page

---

## Step 7: Configure Network

### Enable Local Server Access

1. **Open "详情" (Details) tab** (right panel)

2. **Check "不校验合法域名..." (Don't verify domain)**
   - Full text: "不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书"
   - This allows `http://localhost:8001` API calls

3. **Verify Base URL**
   - Check `miniprogram/services/api.ts` or page files
   - Confirm `baseUrl` is `http://localhost:8001`

---

## Step 8: Start Backend Server

**Before testing miniprogram, ensure backend is running:**

```bash
cd /home/caohui/projects/graduation-leave-system/backend
source venv/bin/activate  # If using virtual environment
python manage.py runserver 0.0.0.0:8001
```

**Verify backend:**
```bash
curl http://localhost:8001/api/health/
# Expected: {"status": "ok"}
```

---

## Step 9: Test Login Flow

1. **Open Simulator** (left panel shows miniprogram UI)

2. **Navigate to Login Page**
   - Should load automatically on first launch
   - If not, click "重新编译" (Recompile)

3. **Enter Test Credentials:**
   - User ID: `2020006`
   - Password: `password`

4. **Click Login Button**

5. **Observe Network Tab:**
   - Open "Network" tab (bottom panel)
   - Check for POST request to `/api/auth/login/`
   - Verify response status 200
   - Verify token in response body

6. **Verify Redirect:**
   - Should redirect to `/pages/approvals/approvals`
   - Check console for navigation logs

---

## Common Issues

### Issue 1: "AppID不存在" (AppID does not exist)

**Cause:** Invalid or missing AppID

**Solution:**
- Use "测试号" (test account) option during import
- Or register a test AppID at https://mp.weixin.qq.com/

---

### Issue 2: "request:fail url not in domain list"

**Cause:** Domain verification enabled

**Solution:**
- Open "详情" tab → Check "不校验合法域名..."
- Or add `localhost` to safe domain list in WeChat MP backend

---

### Issue 3: "Cannot connect to localhost:8001"

**Cause:** Backend not running or wrong port

**Solution:**
- Verify backend running: `curl http://localhost:8001/api/health/`
- Check backend logs for errors
- Verify port 8001 not blocked by firewall

---

### Issue 4: Compilation errors

**Cause:** Missing dependencies or syntax errors

**Solution:**
- Check console for specific error messages
- Verify `app.json` syntax is valid JSON
- Verify all pages listed in `app.json` exist

---

### Issue 5: Blank screen after login

**Cause:** Missing page registration or navigation error

**Solution:**
- Check `app.json` includes target page in `pages` array
- Check console for navigation errors
- Verify page path matches exactly (case-sensitive)

---

## Verification Checklist

After setup, verify:

- [ ] DevTools installed and launches successfully
- [ ] Project imported without errors
- [ ] Compilation succeeds (green "编译成功")
- [ ] Simulator displays login page
- [ ] Backend server running at `http://localhost:8001`
- [ ] Network tab shows API requests
- [ ] Login flow completes successfully
- [ ] No red errors in console

---

## Next Steps

Once setup complete:
1. Proceed to Phase 4A validation checklist
2. Execute validation scenarios
3. Document evidence (screenshots, logs)
4. Report validation results

---

**Status:** Ready for operator execution  
**Blocker:** WeChat DevTools availability (external dependency)  
**Estimated setup time:** 30-60 minutes (first-time)
