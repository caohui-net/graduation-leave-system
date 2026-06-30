// API Integration Layer
// Auto-detect backend port: staging (17788→17787) / production (7788→7787)
const BACKEND_PORT = window.location.port === '17788' ? '17787' : '7787';
const API_BASE_URL = `http://${window.location.hostname}:${BACKEND_PORT}/api`;

let currentToken = null;
let currentUser = null;

// Fetch with timeout (AbortController)
async function fetchWithTimeout(url, options = {}, timeout = 8000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error(`请求超时（${timeout}ms）：${url}`);
        }
        throw error;
    }
}

// 页面加载时自动恢复登录状态
function restoreAuthState() {
    const savedToken = localStorage.getItem('auth_token');
    const savedUser = localStorage.getItem('user_info');

    if (savedToken) {
        currentToken = savedToken;
        if (savedUser) {
            try {
                currentUser = JSON.parse(savedUser);
                console.log('Auth state restored from localStorage', currentUser);
            } catch (e) {
                console.error('Failed to parse user info:', e);
            }
        }
    }
}

// 恢复登录后初始化UI
function initializeUIAfterRestore(user) {
    const loginScreen = document.getElementById('screen-login');
    const typeScreen = document.getElementById('screen-type');
    const isLoginActive = loginScreen && loginScreen.classList.contains('active');
    const isTypeActive = typeScreen && typeScreen.classList.contains('active');

    if (!isLoginActive && !isTypeActive) return;

    // screen-login激活：来自手动登录/页面刷新，跳过选择页直接进业务
    if (isLoginActive) {
        loginScreen.classList.remove('active');

        const navTabs = document.getElementById('navTabs');
        const userBar = document.getElementById('userBar');
        if (navTabs) navTabs.style.display = 'flex';
        if (userBar) userBar.style.display = 'flex';

        const userNameEl = document.getElementById('currentUserName');
        const userRoleEl = document.getElementById('currentUserRole');
        if (userNameEl && (user.name || user.real_name)) userNameEl.textContent = user.name || user.real_name;
        if (userRoleEl && user.role) {
            const roleMap = { 'student': '学生', 'dorm_manager': '宿管', 'counselor': '辅导员', 'dean': '学工部', 'admin': '管理员' };
            userRoleEl.textContent = '(' + (roleMap[user.role] || user.role) + ')';
        }
        if (typeof updateUIForRole === 'function') updateUIForRole(user.role);
        if (user.role === 'student') {
            if (typeof showScreen === 'function') showScreen(0);
            if (typeof loadMyApplications === 'function') loadMyApplications();
        } else {
            if (typeof showScreen === 'function') showScreen(1);
            if (typeof loadApprovals === 'function') loadApprovals();
        }
    }

    // screen-type激活：SSO直达，仅显示用户栏，保留类型选择页让用户点击
    if (isTypeActive) {
        const userBar = document.getElementById('userBar');
        if (userBar) userBar.style.display = 'flex';
        const userNameEl = document.getElementById('currentUserName');
        const userRoleEl = document.getElementById('currentUserRole');
        if (userNameEl && (user.name || user.real_name)) userNameEl.textContent = user.name || user.real_name;
        if (userRoleEl && user.role) {
            const roleMap = { 'student': '学生', 'dorm_manager': '宿管', 'counselor': '辅导员', 'dean': '学工部', 'admin': '管理员' };
            userRoleEl.textContent = '(' + (roleMap[user.role] || user.role) + ')';
        }
    }
}

// 页面加载时立即执行
restoreAuthState();

async function apiLogin(userId, password) {
    try {
        const response = await fetch(API_BASE_URL + '/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                password: password
            })
        });

        if (response.ok) {
            const data = await response.json();
            currentToken = data.access_token;
            currentUser = data.user;
            return { success: true, access_token: data.access_token, user: data.user };
        } else {
            currentToken = null;
            currentUser = null;
            const error = await response.json().catch(() => ({ error: 'Login failed' }));
            return { success: false, error: error };
        }
    } catch (e) {
        console.error("Login failed:", e);
        currentToken = null;
        currentUser = null;
        return { success: false, error: 'Network error' };
    }
}

function getAuthHeaders() {
    return {
        'Authorization': 'Bearer ' + currentToken
    };
}

async function apiGetOrCreateDraft() {
    try {
        const response = await fetch(API_BASE_URL + '/applications/draft/', {
            method: 'POST',
            headers: getAuthHeaders()
        });
        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json().catch(() => ({error: {message: '创建草稿失败'}}));
            return { success: false, error: error.error || {message: '创建草稿失败'} };
        }
    } catch (e) {
        console.error("Create draft failed:", e);
        const errorMsg = e.message || '网络错误';
        return { success: false, error: {message: `创建草稿失败: ${errorMsg}`} };
    }
}

async function apiSubmitApplication(phone, reason, leaveDate, applicationId, applicationType = 'leave_school', stayStartDate = null, stayEndDate = null, stayReason = null, counselorId = null) {
    const formData = new FormData();
    formData.append('contact_phone', phone);
    formData.append('reason', reason);
    formData.append('leave_date', leaveDate);
    formData.append('application_type', applicationType);
    if (stayStartDate) formData.append('stay_start_date', stayStartDate);
    if (stayEndDate) formData.append('stay_end_date', stayEndDate);
    if (stayReason) formData.append('stay_reason', stayReason);
    if (counselorId) formData.append('counselor_id', counselorId);
    if (applicationId) {
        formData.append('application_id', applicationId);
    }

    try {
        const response = await fetch(API_BASE_URL + '/applications/', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + currentToken },
            body: formData
        });
        console.log('[DEBUG] Submit response status:', response.status);
        if (response.ok) {
            return { success: true, data: await response.json() };
        } else {
            const errorText = await response.text();
            console.error('[DEBUG] Submit failed:', response.status, errorText);
            try {
                const error = JSON.parse(errorText);
                return { success: false, error: error.error || { message: error.message || '提交失败' } };
            } catch {
                return { success: false, error: { message: `提交失败(${response.status}): ${errorText.substring(0, 100)}` } };
            }
        }
    } catch (e) {
        console.error("Submit application failed:", e);
        const errorMsg = e.message || '网络连接失败';
        return { success: false, error: { message: `提交失败: ${errorMsg}` } };
    }
}

async function apiGetApplications() {
    try {
        const response = await fetch(API_BASE_URL + '/applications/', {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.error("Get applications failed:", e);
    }
    return { results: [] };
}

async function apiGetApplicationsForAdmin(status = null, limit = 20, offset = 0, filters = {}) {
    try {
        let url = API_BASE_URL + '/applications/?limit=' + limit + '&offset=' + offset;
        if (status) url += '&status=' + encodeURIComponent(status);
        if (filters.student_id) url += '&student_id=' + encodeURIComponent(filters.student_id);
        if (filters.student_name) url += '&student_name=' + encodeURIComponent(filters.student_name);
        if (filters.class_id) url += '&class_id=' + encodeURIComponent(filters.class_id);
        if (filters.building) url += '&building=' + encodeURIComponent(filters.building);
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.error("Get applications failed:", e);
    }
    return { results: [], count: 0 };
}

async function apiGetApprovals(decision = 'pending', limit = 20, offset = 0, filters = {}) {
    try {
        let url = API_BASE_URL + '/approvals/?decision=' + decision + '&limit=' + limit + '&offset=' + offset;
        if (filters.student_id) url += '&student_id=' + encodeURIComponent(filters.student_id);
        if (filters.student_name) url += '&student_name=' + encodeURIComponent(filters.student_name);
        if (filters.class_id) url += '&class_id=' + encodeURIComponent(filters.class_id);
        if (filters.building) url += '&building=' + encodeURIComponent(filters.building);
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.error("Get approvals failed:", e);
    }
    return { results: [], count: 0 };
}

async function apiApprove(approvalId, comment) {
    try {
        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/approve/', {
            method: 'POST',
            headers: Object.assign({}, getAuthHeaders(), { 'Content-Type': 'application/json' }),
            body: JSON.stringify({ comment: comment })
        });
        return response.ok;
    } catch (e) {
        console.error("Approve failed:", e);
        return false;
    }
}

async function apiReject(approvalId, comment) {
    try {
        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/reject/', {
            method: 'POST',
            headers: Object.assign({}, getAuthHeaders(), { 'Content-Type': 'application/json' }),
            body: JSON.stringify({ comment: comment })
        });
        return response.ok;
    } catch (e) {
        console.error("Reject failed:", e);
        return false;
    }
}

async function apiUploadAttachment(applicationId, file, attachmentType = 'other') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('attachment_type', attachmentType);

    try {
        const response = await fetchWithTimeout(
            API_BASE_URL + '/applications/' + applicationId + '/attachments/',
            {
                method: 'POST',
                headers: getAuthHeaders(),
                body: formData
            },
            30000
        );
        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json().catch(() => ({error: {message: '上传失败'}}));
            console.error('[ERROR] Upload failed:', response.status, error);
            alert('附件上传失败：' + (error.error?.message || '服务器错误(' + response.status + ')'));
        }
    } catch (e) {
        console.error('[ERROR] Upload exception:', e);
        const errorMsg = e.message || '网络连接失败';
        alert(`附件上传失败: ${errorMsg}\n\n请检查:\n1. 文件大小是否超过10MB\n2. 网络连接是否正常\n3. 文件格式是否支持`);
    }
    return null;
}

async function apiGetAttachments(applicationId) {
    try {
        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            const data = await response.json();
            return data.attachments || [];
        }
    } catch (e) {
        console.error("Get attachments failed:", e);
    }
    return [];
}

async function apiDeleteAttachment(applicationId, attachmentId) {
    try {
        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/' + attachmentId + '/', {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        return response.ok;
    } catch (e) {
        console.error("Delete attachment failed:", e);
        return false;
    }
}

// DOM加载完成后，如果有token则自动初始化UI
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', function() {
        if (currentToken && currentUser) {
            console.log('Initializing UI after token restore');
            initializeUIAfterRestore(currentUser);
        }
    });
}
